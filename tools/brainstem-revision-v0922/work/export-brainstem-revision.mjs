// Apply the staged deformation without changing labels, indices, UVs or vertex order.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {MeshoptEncoder, MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
assert.equal(JSON.parse(fs.readFileSync('package.json')).version,'0.9.21','Run once on the v0.9.21 baseline');
const candidate=path.resolve(process.argv[2]??'../candidate');
const revision=JSON.parse(fs.readFileSync(path.join(candidate,'revision.json')));
const changed=new Map(revision.changed.map(r=>[r.node,r]));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const fileHashes={},meshes=new Map(),checks=[];
for(const filename of ['brain-context.glb','complete-circulation.glb','venous.glb']){
 const p=`public/anatomy/models/${filename}`,raw=fs.readFileSync(p),jl=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl);
 const views=doc.bufferViews.map(v=>{const b=Buffer.alloc(v.byteLength),e=v.extensions?.EXT_meshopt_compression;if(e)MeshoptDecoder.decodeGltfBuffer(b,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(b,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);return b;});
 const modifiedViews=new Set();
 const sizes={5122:2,5123:2,5125:4,5126:4},widths={SCALAR:1,VEC2:2,VEC3:3,VEC4:4};
 function floats(id){const a=doc.accessors[id],v=doc.bufferViews[a.bufferView],b=views[a.bufferView],width=widths[a.type],stride=v.byteStride??sizes[a.componentType]*width;return Array.from({length:a.count},(_,i)=>Array.from({length:width},(_,j)=>{const o=(a.byteOffset??0)+i*stride+j*sizes[a.componentType];return a.componentType===5126?b.readFloatLE(o):a.componentType===5122?b.readInt16LE(o)/32767:a.componentType===5123?b.readUInt16LE(o):b.readUInt32LE(o);}));}
 for(const n of doc.nodes.filter(n=>'mesh' in n)){
  const prim=doc.meshes[n.mesh].primitives[0];assert.equal(doc.meshes[n.mesh].primitives.length,1);
  if(changed.has(n.name)){
   const pos=fs.readFileSync(path.join(candidate,n.name+'.positions.bin')),grad=fs.readFileSync(path.join(candidate,n.name+'.gradient.bin'));
   const pa=doc.accessors[prim.attributes.POSITION];modifiedViews.add(pa.bufferView);const pv=doc.bufferViews[pa.bufferView],pb=views[pa.bufferView];assert.equal(pos.length,pa.count*12);assert.equal(pa.componentType,5126);const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
   for(let i=0;i<pa.count;i++)for(let j=0;j<3;j++){const x=pos.readFloatLE(i*12+j*4);assert(Number.isFinite(x));pb.writeFloatLE(x,(pa.byteOffset??0)+i*(pv.byteStride??12)+j*4);lo[j]=Math.min(lo[j],x);hi[j]=Math.max(hi[j],x);}pa.min=lo;pa.max=hi;
   const na=doc.accessors[prim.attributes.NORMAL];modifiedViews.add(na.bufferView);const nv=doc.bufferViews[na.bufferView],nb=views[na.bufferView],normals=floats(prim.attributes.NORMAL),xyzw=new Float32Array(na.count*4);
   assert.equal(na.count,pa.count);
   for(let i=0;i<na.count;i++){const [nx,ny,nz]=normals[i],dx=grad.readFloatLE(i*12),dy=grad.readFloatLE(i*12+4),dz=grad.readFloatLE(i*12+8),b=ny/(1+dy),a=nx-dx*b,c=nz-dz*b,len=Math.hypot(a,b,c);xyzw.set([a/len,b/len,c/len,0],i*4);}
   if(nv.extensions?.EXT_meshopt_compression?.filter==='OCTAHEDRAL'){
    const packed=MeshoptEncoder.encodeFilterOct(xyzw,na.count,nv.byteStride??8,12);assert.equal(packed.length,nb.length);nb.set(packed);
   }else{assert.equal(na.componentType,5126);for(let i=0;i<na.count;i++)for(let j=0;j<3;j++)nb.writeFloatLE(xyzw[i*4+j],(na.byteOffset??0)+i*(nv.byteStride??12)+j*4);}
  }
  meshes.set(`${filename}:${n.name}`,{positions:floats(prim.attributes.POSITION),indices:floats(prim.indices).flat()});
 }
 const chunks=[];let encodedOffset=0,decodedOffset=0;
 for(let i=0;i<doc.bufferViews.length;i++){
  const v=doc.bufferViews[i],b=views[i],e=v.extensions.EXT_meshopt_compression,encoded=modifiedViews.has(i)?MeshoptEncoder.encodeGltfBuffer(b,e.count,e.byteStride,e.mode):binary.subarray(e.byteOffset,e.byteOffset+e.byteLength);if(modifiedViews.has(i)){const test=Buffer.alloc(b.length);MeshoptDecoder.decodeGltfBuffer(test,e.count,e.byteStride,encoded,e.mode);assert(test.equals(b),'Exact codec roundtrip before optional normal filter');}
  v.buffer=1;v.byteOffset=decodedOffset;decodedOffset+=v.byteLength;e.buffer=0;e.byteOffset=encodedOffset;e.byteLength=encoded.length;
  const pad=(-encoded.length)&3;chunks.push(Buffer.from(encoded),Buffer.alloc(pad));encodedOffset+=encoded.length+pad;
 }
 doc.buffers=[{byteLength:encodedOffset},{byteLength:decodedOffset,extensions:{EXT_meshopt_compression:{fallback:true}}}];
 let j=Buffer.from(JSON.stringify(doc));j=Buffer.concat([j,Buffer.alloc((-j.length)&3,32)]);const bin=Buffer.concat(chunks),header=Buffer.alloc(20),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+j.length+bin.length,8);header.writeUInt32LE(j.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bin.length);bh.writeUInt32LE(0x004e4942,4);const out=Buffer.concat([header,j,bh,bin]);fs.writeFileSync(p,out);fileHashes[`models/${filename}`]=sha(out);checks.push({file:filename,oldSha256:sha(raw),sha256:sha(out),labels:doc.nodes.filter(n=>'mesh' in n).length,indicesAndVertexOrderRetained:true,exactPositionCodecRoundtrip:true});
}
const mp='anatomy/generated/complete_manifest.json',m=JSON.parse(fs.readFileSync(mp)),rows=new Map(m.structures.map(r=>[r.id,r])),brainHash=fileHashes['models/brain-context.glb'];
m.release='0.9.22';m.brainRegistration.registeredAssetSha256=brainHash;
function bind(a){const r=rows.get(a.structureId);assert(r?.asset);const mesh=meshes.get(`${path.basename(r.asset.file)}:${r.asset.node}`);assert(mesh);const xyz=[0,0,0];for(let i=0;i<3;i++){const p=mesh.positions[mesh.indices[a.triangleIndex*3+i]];for(let j=0;j<3;j++)xyz[j]+=a.barycentric[i]*p[j];}a.position=xyz;a.assetSha256=brainHash;}
for(const r of m.structures){if(r.surfaceAnchor){bind(r.surfaceAnchor);r.landmark.point=r.surfaceAnchor.position;}for(const a of r.secondarySurfaceAnchors??[])bind(a);if(r.vesselCourse){r.vesselCourse.brainAssetSha256=brainHash;r.vesselCourse.geometrySha256=fileHashes[r.vesselCourse.geometry.file]??r.vesselCourse.geometrySha256;}}
for(const r of m.structures){const keys=r.vesselGuide?.anchorIds;if(keys?.length){r.landmark.course=keys.map(k=>rows.get(k).surfaceAnchor.position);r.landmark.point=r.landmark.course[0];}}
const plex=rows.get('vein.basilar_plexus');plex.asset={file:'models/venous.glb',node:'vein.basilar_plexus'};plex.geometryStatus='web-optimised';plex.notes='Restored clival/basilar plexus. Its retained channels follow the posterior clivus; anterior brainstem and attached vessels receive a separate local shape adjustment.';
plex.vesselCourse={...structuredClone(rows.get('vein.anterior_condylar.left').vesselCourse),vesselId:plex.id,side:plex.side,geometry:plex.asset,geometrySha256:fileHashes['models/venous.glb'],brainAssetSha256:brainHash,attachments:{parentId:plex.parent,incoming:m.relationships.filter(r=>r.to===plex.id),outgoing:m.relationships.filter(r=>r.from===plex.id),status:'catalogue-relationships-not-yet-verified-as-physical-junctions'},summary:'Retain the clival dural plexus against the posterior clivus and preserve its skull-base communications.'};
for(const [file,hash]of Object.entries(fileHashes)){m.assetRevisions[file]=hash.slice(0,20);m.assetByteSizes[file]=fs.statSync('public/anatomy/'+file).size;}
m.brainRegistration.brainstemAdjustment={release:'0.9.22',additionalPonsAmplitudeMm:revision.additionalPonsAmplitudeMm,additionalMidbrainAmplitudeMm:revision.additionalMidbrainAmplitudeMm,method:revision.method};
const write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');write(mp,m);write('public/anatomy/manifest.json',m);
const lm=JSON.parse(fs.readFileSync('public/anatomy/brain-landmarks.json'));lm.registration=m.brainRegistration;lm.anchors=m.structures.filter(r=>r.landmark&&r.system==='brain');write('public/anatomy/brain-landmarks.json',lm);
const vc=JSON.parse(fs.readFileSync('public/anatomy/vessel-courses.json'));vc.brainRegistration=m.brainRegistration;vc.courses=m.structures.filter(r=>r.vesselCourse).map(r=>r.vesselCourse);write('public/anatomy/vessel-courses.json',vc);
for(const p of ['package.json','package-lock.json']){const x=JSON.parse(fs.readFileSync(p));x.version='0.9.22';if(x.packages?.[''])x.packages[''].version='0.9.22';write(p,x);}
write('docs/validation/brainstem-export-v0.9.22.json',{release:'0.9.22',baseline:'0.9.21',checks,sharedLabelsAndTopologyPreserved:true,restoredPlexusNode:'vein.basilar_plexus'});
console.log(JSON.stringify(checks,null,2));
