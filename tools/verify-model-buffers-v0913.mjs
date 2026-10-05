import fs from 'node:fs';
import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
function read(path){
 const b=fs.readFileSync(path),n=b.readUInt32LE(12);
 if(b.readUInt32LE(8)!==b.length)throw Error(`Invalid GLB length ${path}`);
 return [JSON.parse(b.subarray(20,20+n)),b.subarray(28+n)];
}
const pairs=[['.authoring/circulation-refined.glb','public/anatomy/models/complete-circulation.glb'],['.authoring/anastomoses-refined.glb','public/anatomy/models/complete-anastomoses.glb'],['.authoring/venous/venous-raw.glb','public/anatomy/models/venous.glb']];
const files=[];
for(const [source,target] of pairs){
 const [a,ab]=read(source),[b,bb]=read(target);
 if(a.bufferViews.length!==b.bufferViews.length)throw Error('View count mismatch');
 for(let i=0;i<a.bufferViews.length;i++){
  const v=a.bufferViews[i],w=b.bufferViews[i],e=w.extensions.EXT_meshopt_compression;
  const decoded=new Uint8Array(w.byteLength);
  MeshoptDecoder.decodeGltfBuffer(decoded,e.count,e.byteStride,bb.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode);
  if(!Buffer.from(decoded).equals(ab.subarray(v.byteOffset,v.byteOffset+v.byteLength)))throw Error(`Buffer mismatch ${target} ${i}`);
 }
 files.push({source,target,buffer_views_verified:a.bufferViews.length,exact_roundtrip:true,source_bytes:fs.statSync(source).size,asset_bytes:fs.statSync(target).size});
}
const report={release:'0.9.13',files,scope:'Exact decoded buffer bytes of final on-disk GLBs compared with raw authoring sources.'};
fs.writeFileSync('docs/validation/model-buffer-roundtrip-v0.9.13.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
