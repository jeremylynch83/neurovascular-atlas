// 16-bit shared position grid, 12-bit octahedral normals, exact index sequences.
// Usage: node tools/compress-models.mjs ORIGINAL_UNCOMPRESSED_MODEL_DIRECTORY
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {MeshoptEncoder, MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready, MeshoptDecoder.ready]);
const root=path.resolve(import.meta.dirname,'..'), source=path.resolve(process.argv[2]);
const names=['brain-context','complete-anastomoses','complete-circulation','craniofacial','venous'];
const previousTransportHashes=Object.fromEntries(names.map(name=>[name,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'public/anatomy/models',name+'.glb'))).digest('hex')]));
const models=names.map(name=>{
 const data=fs.readFileSync(path.join(source,name+'.glb')),length=data.readUInt32LE(12);
 const doc=JSON.parse(data.subarray(20,20+length));
 assert(!doc.extensionsUsed?.includes('EXT_meshopt_compression'),'Input must be the uncompressed authoring geometry');
 assert(doc.nodes.every(n=>!n.matrix&&!n.scale&&!n.rotation&&!n.translation),'Expected world-space positions');
 return {name,data,doc,binary:data.subarray(28+length)};
});
const minimum=[Infinity,Infinity,Infinity],maximum=[-Infinity,-Infinity,-Infinity];
for(const {doc} of models)for(const m of doc.meshes)for(const p of m.primitives){
 const a=doc.accessors[p.attributes.POSITION];
 for(let k=0;k<3;k++){minimum[k]=Math.min(minimum[k],a.min[k]);maximum[k]=Math.max(maximum[k],a.max[k]);}
}
const step=Math.max(...maximum.map((v,k)=>v-minimum[k]))/65535;
// Preserve tiny existing faces. Exceptions are shared across all meshes so
// coincident points at joined boundaries still receive identical coordinates.
const protectedPositions=new Set();
function key(v){return v.join(',');}
function quantise(v){return protectedPositions.has(key(v))?v:v.map((x,k)=>Math.fround(minimum[k]+Math.round((x-minimum[k])/step)*step));}
function faceNormal(a,b,c){const u=b.map((v,k)=>v-a[k]),v=c.map((x,k)=>x-a[k]);return [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];}
for(let pass=0;pass<12;pass++){
 const before=protectedPositions.size;
 for(const {doc,binary} of models)for(const m of doc.meshes)for(const p of m.primitives){
  const a=doc.accessors[p.attributes.POSITION],v=doc.bufferViews[a.bufferView],stride=v.byteStride??12,start=(v.byteOffset??0)+(a.byteOffset??0);
  const positions=Array.from({length:a.count},(_,i)=>[0,1,2].map(k=>binary.readFloatLE(start+i*stride+k*4))),rounded=positions.map(quantise);
  const ia=doc.accessors[p.indices],iv=doc.bufferViews[ia.bufferView],is=(iv.byteOffset??0)+(ia.byteOffset??0),size=ia.componentType===5125?4:2;
  for(let i=0;i<ia.count;i+=3){
   const indices=[0,1,2].map(k=>size===4?binary.readUInt32LE(is+(i+k)*size):binary.readUInt16LE(is+(i+k)*size));
   const before=faceNormal(...indices.map(j=>positions[j])),after=faceNormal(...indices.map(j=>rounded[j]));
   if(Math.hypot(...before)>0 && before.reduce((sum,v,k)=>sum+v*after[k],0)<=0)for(const j of indices)protectedPositions.add(key(positions[j]));
  }
 }
 console.log('Tiny-face protection pass',pass+1,protectedPositions.size,'unique positions');
 if(protectedPositions.size===before)break;
 assert(pass<11,'Protection did not converge');
}
const report={release:'0.9.71',positionBits:16,positionStorage:'Float32 on a shared uniform 16-bit grid, preserving world-space coordinates',normalBits:12,normalEncoding:'OCTAHEDRAL, signed-normalised 16-bit output',stepMm:step,theoreticalMaxDisplacementMm:Math.sqrt(3)*step/2,vertexOrderPreserved:true,triangleOrderPreserved:true,assets:[]};
report.protectedPositions=protectedPositions.size;report.positionExceptions='Original coordinates retained for tiny faces that would otherwise collapse';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const model of models){
 const {name,data,doc,binary}=model,oldAccessors=doc.accessors,oldViews=doc.bufferViews;
 function values(id,width){const a=oldAccessors[id],v=oldViews[a.bufferView],stride=v.byteStride??width*4;assert.equal(a.componentType,5126);return Array.from({length:a.count},(_,i)=>Array.from({length:width},(_,k)=>binary.readFloatLE((v.byteOffset??0)+(a.byteOffset??0)+i*stride+k*4)));}
 doc.accessors=[];doc.bufferViews=[];const chunks=[];let encodedOffset=0,decodedOffset=0,vertices=0,maxDisplacement=0;
 function add(bytes,count,stride,mode,accessor,filter){
  const encoded=Buffer.from(MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,mode,0));
  const decoded=Buffer.alloc(bytes.length);MeshoptDecoder.decodeGltfBuffer(decoded,count,stride,encoded,mode,filter);
  if(!filter)assert(decoded.equals(bytes),'Lossless payload mismatch');
  const view=doc.bufferViews.length;doc.bufferViews.push({buffer:1,byteOffset:decodedOffset,byteLength:bytes.length,...(mode==='ATTRIBUTES'?{byteStride:stride,target:34962}:{target:34963}),extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:encodedOffset,byteLength:encoded.length,count,byteStride:stride,mode,...(filter?{filter}:{})}}});
  const id=doc.accessors.length;doc.accessors.push({...accessor,bufferView:view,byteOffset:0,count});
  chunks.push(encoded);const padding=Buffer.alloc((-encoded.length)&3);chunks.push(padding);encodedOffset+=encoded.length+padding.length;decodedOffset+=bytes.length;
  return id;
 }
 for(const m of doc.meshes)for(const p of m.primitives){
  assert.deepEqual(Object.keys(p.attributes).sort(),['NORMAL','POSITION']);
  const positions=values(p.attributes.POSITION,3),normals=values(p.attributes.NORMAL,3),count=positions.length;
  const bytes=Buffer.alloc(count*12),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<count;i++){
   let squared=0;
   for(let k=0;k<3;k++){
    const x=protectedPositions.has(key(positions[i]))?positions[i][k]:Math.fround(minimum[k]+Math.round((positions[i][k]-minimum[k])/step)*step);
    bytes.writeFloatLE(x,i*12+k*4);lo[k]=Math.min(lo[k],x);hi[k]=Math.max(hi[k],x);squared+=(x-positions[i][k])**2;
   }
   maxDisplacement=Math.max(maxDisplacement,Math.sqrt(squared));
  }
  const pa=add(bytes,count,12,'ATTRIBUTES',{componentType:5126,type:'VEC3',min:lo,max:hi});
  const xyzw=new Float32Array(count*4);for(let i=0;i<count;i++)for(let k=0;k<3;k++)xyzw[i*4+k]=normals[i][k];
  const normalBytes=Buffer.from(MeshoptEncoder.encodeFilterOct(xyzw,count,8,12));
  const na=add(normalBytes,count,8,'ATTRIBUTES',{componentType:5122,type:'VEC3',normalized:true},'OCTAHEDRAL');
  const index=oldAccessors[p.indices],view=oldViews[index.bufferView],size=index.componentType===5125?4:2;assert([5123,5125].includes(index.componentType));
  const start=(view.byteOffset??0)+(index.byteOffset??0),indices=Buffer.from(binary.subarray(start,start+index.count*size));
  const ia=add(indices,index.count,size,'INDICES',{componentType:index.componentType,type:'SCALAR'});
  p.attributes={POSITION:pa,NORMAL:na};p.indices=ia;vertices+=count;
 }
 doc.extensionsUsed=['EXT_meshopt_compression','KHR_mesh_quantization'];doc.extensionsRequired=[...doc.extensionsUsed];
 doc.buffers=[{byteLength:encodedOffset},{byteLength:decodedOffset,extensions:{EXT_meshopt_compression:{fallback:true}}}];
 let json=Buffer.from(JSON.stringify(doc));json=Buffer.concat([json,Buffer.alloc((-json.length)&3,32)]);
 const bin=Buffer.concat(chunks),header=Buffer.alloc(20),binHeader=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);header.writeUInt32LE(json.length,12);header.writeUInt32LE(0x4e4f534a,16);binHeader.writeUInt32LE(bin.length,0);binHeader.writeUInt32LE(0x004e4942,4);
 const output=Buffer.concat([header,json,binHeader,bin]);fs.writeFileSync(path.join(root,'public/anatomy/models',name+'.glb'),output);
 report.assets.push({name,vertices,sourceSha256:sha(data),previousTransportSha256:previousTransportHashes[name],sha256:sha(output),rawBytes:data.length,compressedGlbBytes:output.length,maxDisplacementMm:maxDisplacement});
 console.log(name,output.length,'bytes; max displacement',maxDisplacement.toFixed(6),'mm');
}
fs.writeFileSync(path.join(root,'docs/compression-validation.json'),JSON.stringify(report,null,2)+'\n');
