// Append losslessly compressed replacement position/normal views for accepted
// local repairs. Every other encoded stream and every index sequence is kept.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const work=path.resolve(process.argv[2]),source=path.resolve(process.argv[3]),output=path.resolve(process.argv[4]);
const accepted=JSON.parse(fs.readFileSync(work+'/local-vein-trials.json')).accepted;assert(accepted.length&&accepted.every(x=>x.passed));
const raw=fs.readFileSync(source),length=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+length)),binary=raw.subarray(28+length);assert(doc.nodes.every(n=>!n.matrix&&!n.translation&&!n.rotation&&!n.scale));
const chunks=[binary];let encodedOffset=binary.length,decodedOffset=doc.buffers[1].byteLength;const report=[];
function normalValues(id){
 const a=doc.accessors[id],v=doc.bufferViews[a.bufferView],e=v.extensions.EXT_meshopt_compression,b=Buffer.alloc(v.byteLength);MeshoptDecoder.decodeGltfBuffer(b,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);
 const out=new Float32Array(a.count*3),stride=v.byteStride??6;
 for(let i=0;i<a.count;i++)for(let k=0;k<3;k++)out[i*3+k]=a.componentType===5122?Math.max(-1,b.readInt16LE((a.byteOffset??0)+i*stride+k*2)/32767):b.readFloatLE((a.byteOffset??0)+i*stride+k*4);
 return out;
}
function add(bytes,count,stride,accessor,filter){
 const encoded=Buffer.from(MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,'ATTRIBUTES',0));const decoded=Buffer.alloc(bytes.length);MeshoptDecoder.decodeGltfBuffer(decoded,count,stride,encoded,'ATTRIBUTES',filter);if(!filter)assert(decoded.equals(bytes));
 const view=doc.bufferViews.length;doc.bufferViews.push({buffer:1,byteOffset:decodedOffset,byteLength:bytes.length,byteStride:stride,target:34962,extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:encodedOffset,byteLength:encoded.length,count,byteStride:stride,mode:'ATTRIBUTES',...(filter?{filter}:{})}}});
 const id=doc.accessors.length;doc.accessors.push({...accessor,bufferView:view,byteOffset:0,count});chunks.push(encoded,Buffer.alloc((-encoded.length)&3));encodedOffset+=encoded.length+((-encoded.length)&3);decodedOffset+=bytes.length;return id;
}
for(const row of accepted){
 const node=doc.nodes.find(n=>n.name===row.node);assert(node&&'mesh'in node);const primitive=doc.meshes[node.mesh].primitives[0],old=doc.accessors[primitive.attributes.POSITION],n=old.count;
 const bytes=fs.readFileSync(work+'/candidate/'+row.node+'.positions.bin'),normalBytes=fs.readFileSync(work+'/candidate/'+row.node+'.normals.bin');assert.equal(bytes.length,n*12);assert.equal(normalBytes.length,n*12);
 assert(fs.readFileSync(work+'/candidate/'+row.node+'.indices.bin').equals(fs.readFileSync(work+'/decoded/'+row.node+'.indices.bin')),'Index sequences must stay exact');
 const original=fs.readFileSync(work+'/decoded/'+row.node+'.positions.bin'),index=fs.readFileSync(work+'/candidate/'+row.node+'.indices.bin'),oldNormals=normalValues(primitive.attributes.NORMAL),affected=new Set(),edges=new Map();
 for(let i=0;i<index.length;i+=12){const face=[0,1,2].map(k=>index.readUInt32LE(i+k*4));if(face.some(j=>!bytes.subarray(j*12,j*12+12).equals(original.subarray(j*12,j*12+12))))face.forEach(j=>affected.add(j));for(let k=0;k<3;k++){const a=face[k],b=face[(k+1)%3],key=a<b?`${a},${b}`:`${b},${a}`;edges.set(key,(edges.get(key)??0)+1)}}
 const fixedNormals=new Set([...edges].filter(([,c])=>c===1).flatMap(([key])=>key.split(',').map(Number)));
 const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity],xyzw=new Float32Array(n*4);
 for(let i=0;i<n;i++)for(let k=0;k<3;k++){const v=bytes.readFloatLE(i*12+k*4);assert(Number.isFinite(v));lo[k]=Math.min(lo[k],v);hi[k]=Math.max(hi[k],v);xyzw[i*4+k]=affected.has(i)&&!fixedNormals.has(i)?normalBytes.readFloatLE(i*12+k*4):oldNormals[i*3+k]}
 const pa=add(bytes,n,12,{componentType:5126,type:'VEC3',min:lo,max:hi}),norm=Buffer.from(MeshoptEncoder.encodeFilterOct(xyzw,n,8,12));const na=add(norm,n,8,{componentType:5122,type:'VEC3',normalized:true},'OCTAHEDRAL');primitive.attributes={...primitive.attributes,POSITION:pa,NORMAL:na};
 report.push({node:row.node,vertices:n,positionSha256:crypto.createHash('sha256').update(bytes).digest('hex'),positionEncoding:'Lossless meshopt Float32; no additional coordinate quantisation',normalBits:12,nativeSeamNormalsRetained:true,normalUpdatesLimitedToMovedFaces:true,bounds:[lo,hi]});
}
doc.buffers[0].byteLength=encodedOffset;doc.buffers[1].byteLength=decodedOffset;
let json=Buffer.from(JSON.stringify(doc));json=Buffer.concat([json,Buffer.alloc((-json.length)&3,32)]);const bin=Buffer.concat(chunks),header=Buffer.alloc(20),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);header.writeUInt32LE(json.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bin.length,0);bh.writeUInt32LE(0x004e4942,4);const result=Buffer.concat([header,json,bh,bin]);fs.writeFileSync(output,result,{mode:0o644});
fs.writeFileSync(work+'/model-patch.json',JSON.stringify({sourceSha256:crypto.createHash('sha256').update(raw).digest('hex'),sha256:crypto.createHash('sha256').update(result).digest('hex'),bytes:result.length,changed:report,otherStreamsRetained:true,indicesRetained:true},null,2)+'\n');console.log(JSON.stringify({changed:report.map(r=>r.node),bytes:result.length}));
