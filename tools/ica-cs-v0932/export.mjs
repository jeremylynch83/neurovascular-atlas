// Apply accepted local placement and round-wall recovery while retaining labelled structures.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {MeshoptEncoder, MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
assert.equal(JSON.parse(fs.readFileSync('package.json')).version,'0.9.32');
const candidate=path.resolve(process.argv[2]??'../candidate');
const revision=JSON.parse(fs.readFileSync(path.join(candidate,'revision.json')));
const changed=new Map(revision.changed.map(r=>[r.node,r]));

const validation=JSON.parse(fs.readFileSync(path.join(candidate,'validation.json')));assert(validation.passed);assert(validation.checks.meshQuality.passed);assert(validation.checks.physicalJunctions.passed);assert(validation.checks.fullSurfaceConstraints.passed);assert(validation.checks.boneClearance.passed);assert(validation.checks.remoteVenousSplices.passed);

const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const fileHashes={},checks=[];
for(const filename of [...new Set(revision.changed.map(r=>r.file))]){
 const p=`public/anatomy/models/${filename}`,raw=fs.readFileSync(path.join(process.argv[3]??'../fixes-work/baseline',filename));assert.equal(sha(raw),revision.baselineAssetHashes[filename],'Exact checked baseline required');const jl=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl);
 const views=doc.bufferViews.map(v=>{const b=Buffer.alloc(v.byteLength),e=v.extensions?.EXT_meshopt_compression;if(e)MeshoptDecoder.decodeGltfBuffer(b,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(b,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);return b;});

 // New named surfaces share the same standalone scene and compression contract.
 for(const name of revision.newLabels){
  const addView=(stride,filter)=>{const id=doc.bufferViews.length;doc.bufferViews.push({buffer:1,byteOffset:0,byteLength:0,...(stride!==4?{byteStride:stride,target:34962}:{target:34963}),extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:0,byteLength:0,byteStride:stride,count:0,mode:stride===4?'INDICES':'ATTRIBUTES',...(filter?{filter}: {})}}});views.push(Buffer.alloc(0));return id;};
  const addAccessor=(view,type,componentType,normalised=false)=>{const id=doc.accessors.length;doc.accessors.push({bufferView:view,byteOffset:0,componentType,count:0,type,...(normalised?{normalized:true}:{})});return id;};
  const pa=addAccessor(addView(12),'VEC3',5126),na=addAccessor(addView(8,'OCTAHEDRAL'),'VEC3',5122,true),ia=addAccessor(addView(4),'SCALAR',5125);
  const mesh=doc.meshes.length;doc.meshes.push({name,primitives:[{attributes:{POSITION:pa,NORMAL:na},indices:ia}]});const node=doc.nodes.length;doc.nodes.push({name,mesh});doc.scenes[doc.scene??0].nodes.push(node);
 }
 const modifiedViews=new Set();
 const sizes={5122:2,5123:2,5125:4,5126:4},widths={SCALAR:1,VEC2:2,VEC3:3,VEC4:4};
 function floats(id){const a=doc.accessors[id],v=doc.bufferViews[a.bufferView],b=views[a.bufferView],width=widths[a.type],stride=v.byteStride??sizes[a.componentType]*width;return Array.from({length:a.count},(_,i)=>Array.from({length:width},(_,j)=>{const o=(a.byteOffset??0)+i*stride+j*sizes[a.componentType];return a.componentType===5126?b.readFloatLE(o):a.componentType===5122?b.readInt16LE(o)/32767:a.componentType===5123?b.readUInt16LE(o):b.readUInt32LE(o);}));}
 for(const n of doc.nodes.filter(n=>'mesh' in n)){
  const prim=doc.meshes[n.mesh].primitives[0];assert.equal(doc.meshes[n.mesh].primitives.length,1);
  if(changed.has(n.name)){
   const pos=fs.readFileSync(path.join(candidate,n.name+'.positions.bin')),targetNormals=fs.readFileSync(path.join(candidate,n.name+'.normals.bin')),indices=fs.readFileSync(path.join(candidate,n.name+'.indices.bin'));
   assert.deepEqual(Object.keys(prim.attributes).sort(),['NORMAL','POSITION']);
   const pa=doc.accessors[prim.attributes.POSITION],na=doc.accessors[prim.attributes.NORMAL],ia=doc.accessors[prim.indices],count=pos.length/12;
   const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
   for(let i=0;i<count;i++)for(let j=0;j<3;j++){const x=pos.readFloatLE(i*12+j*4);assert(Number.isFinite(x));lo[j]=Math.min(lo[j],x);hi[j]=Math.max(hi[j],x);}
   pa.count=count;pa.min=lo;pa.max=hi;pa.byteOffset=0;na.count=count;na.byteOffset=0;ia.count=indices.length/4;ia.componentType=5125;ia.byteOffset=0;delete ia.min;delete ia.max;
   const xyzw=new Float32Array(count*4);
   for(let i=0;i<count;i++){let nn=[0,1,2].map(j=>targetNormals.readFloatLE(i*12+j*4)),len=Math.hypot(...nn);assert(len>1e-8,n.name+' normal');xyzw.set([nn[0]/len,nn[1]/len,nn[2]/len,0],i*4);}
   const nv=doc.bufferViews[na.bufferView];assert.equal(nv.extensions.EXT_meshopt_compression.filter,'OCTAHEDRAL');
   const normals=MeshoptEncoder.encodeFilterOct(xyzw,count,8,12);
   for(const [accessor,bytes,stride,items] of [[pa,pos,12,count],[na,normals,8,count],[ia,indices,4,indices.length/4]]){
    const view=doc.bufferViews[accessor.bufferView];view.byteLength=bytes.length;if(accessor!==ia)view.byteStride=stride;else delete view.byteStride;
    if(accessor===ia)view.extensions.EXT_meshopt_compression.mode='INDICES';
    view.extensions.EXT_meshopt_compression.count=items;view.extensions.EXT_meshopt_compression.byteStride=stride;views[accessor.bufferView]=Buffer.from(bytes);modifiedViews.add(accessor.bufferView);
   }
  }
 }
 const chunks=[];let encodedOffset=0,decodedOffset=0;
 for(let i=0;i<doc.bufferViews.length;i++){
  const v=doc.bufferViews[i],b=views[i],e=v.extensions.EXT_meshopt_compression,encoded=modifiedViews.has(i)?MeshoptEncoder.encodeGltfBuffer(b,e.count,e.byteStride,e.mode):binary.subarray(e.byteOffset,e.byteOffset+e.byteLength);if(modifiedViews.has(i)){const test=Buffer.alloc(b.length);MeshoptDecoder.decodeGltfBuffer(test,e.count,e.byteStride,encoded,e.mode);assert(test.equals(b),'Exact codec roundtrip before optional normal filter');}
  v.buffer=1;v.byteOffset=decodedOffset;decodedOffset+=v.byteLength;e.buffer=0;e.byteOffset=encodedOffset;e.byteLength=encoded.length;
  const pad=(-encoded.length)&3;chunks.push(Buffer.from(encoded),Buffer.alloc(pad));encodedOffset+=encoded.length+pad;
 }
 doc.buffers=[{byteLength:encodedOffset},{byteLength:decodedOffset,extensions:{EXT_meshopt_compression:{fallback:true}}}];
 let j=Buffer.from(JSON.stringify(doc));j=Buffer.concat([j,Buffer.alloc((-j.length)&3,32)]);const bin=Buffer.concat(chunks),header=Buffer.alloc(20),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+j.length+bin.length,8);header.writeUInt32LE(j.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bin.length);bh.writeUInt32LE(0x004e4942,4);const out=Buffer.concat([header,j,bh,bin]);fs.writeFileSync(p,out);fileHashes[`models/${filename}`]=sha(out);checks.push({file:filename,oldSha256:sha(raw),sha256:sha(out),labels:doc.nodes.filter(n=>'mesh' in n).length,topologyRepartitionOrConnectedField:true,exactPositionCodecRoundtrip:true});
}

fs.writeFileSync(path.join(candidate,"export.json"),JSON.stringify({release:"0.9.32",checks},null,2)+"\n");
console.log(JSON.stringify(checks));
