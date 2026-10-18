// Lossless bounded shaft fit export with preserved corner SNORM16 values.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const [work,source,output]=process.argv.slice(2),rows=JSON.parse(fs.readFileSync(path.join(work,'normal-provenance.json')));
assert(JSON.parse(fs.readFileSync(path.join(work,'native-validation.json'))).passed);
const raw=fs.readFileSync(source),jl=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl),chunks=[binary];
let encodedOffset=binary.length,decodedOffset=doc.buffers[1].byteLength;
const cache=new Map();
function access(id){const a=doc.accessors[id],v=doc.bufferViews[a.bufferView];let bytes=cache.get(a.bufferView);if(!bytes){const e=v.extensions?.EXT_meshopt_compression;bytes=Buffer.alloc(v.byteLength);if(e)MeshoptDecoder.decodeGltfBuffer(bytes,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(bytes,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);cache.set(a.bufferView,bytes)}return {a,v,bytes};}
function primitive(n){return doc.meshes[doc.nodes.find(x=>x.name===n).mesh].primitives[0]}
function add(bytes,count,stride,accessor,mode='ATTRIBUTES'){
 const encoded=Buffer.from(MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,mode)),padding=Buffer.alloc((-encoded.length)&3),roundtrip=Buffer.alloc(bytes.length);
 MeshoptDecoder.decodeGltfBuffer(roundtrip,count,stride,encoded,mode);assert(roundtrip.equals(bytes));
 const view=doc.bufferViews.length,target=mode==='INDICES'?34963:34962;
 doc.bufferViews.push({buffer:1,byteOffset:decodedOffset,byteLength:bytes.length,...(target===34962?{byteStride:stride}:{}),target,extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:encodedOffset,byteLength:encoded.length,count,byteStride:stride,mode}}});
 const id=doc.accessors.length;doc.accessors.push({...accessor,count,bufferView:view,byteOffset:0});chunks.push(encoded,padding);encodedOffset+=encoded.length+padding.length;decodedOffset+=bytes.length;return id;
}
const changes=[];
for(const row of rows){
 const prim=primitive(row.node),oldPosition=access(prim.attributes.POSITION),oldNormal=access(prim.attributes.NORMAL);
 assert.equal(oldNormal.a.componentType,5122);assert.equal(oldNormal.a.normalized,true);
 const p=fs.readFileSync(path.join(work,'candidate',row.node+'.positions.bin')),idx=fs.readFileSync(path.join(work,'candidate',row.node+'.indices.bin')),count=p.length/12;
 const normals=fs.readFileSync(path.join(work,'candidate',row.node+'.normal-snorm16.bin'));assert.equal(normals.length,count*8);
 const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let i=0;i<count;i++)for(let k=0;k<3;k++){const x=p.readFloatLE(i*12+k*4);assert(Number.isFinite(x));lo[k]=Math.min(lo[k],x);hi[k]=Math.max(hi[k],x)}
 prim.attributes.POSITION=add(p,count,12,{componentType:5126,type:'VEC3',min:lo,max:hi});
 // No octahedral re-quantisation: candidate SNORM16 values round-trip exactly.
 prim.attributes.NORMAL=add(normals,count,8,{componentType:5122,type:'VEC3',normalized:true});
 prim.indices=add(idx,idx.length/4,4,{componentType:5125,type:'SCALAR'},'INDICES');
 fs.writeFileSync(path.join(work,'candidate',row.node+'.normal-snorm16.bin'),normals);
 changes.push({node:row.node,vertices:count,triangles:idx.length/12,retainedSourceTrianglesWithExactCornerNormals:row.retainedSourceTrianglesWithExactCornerNormals});
}
doc.buffers[0].byteLength=encodedOffset;doc.buffers[1].byteLength=decodedOffset;
let json=Buffer.from(JSON.stringify(doc));json=Buffer.concat([json,Buffer.alloc((-json.length)&3,32)]);const bin=Buffer.concat(chunks),header=Buffer.alloc(20),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);header.writeUInt32LE(json.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bin.length,0);bh.writeUInt32LE(0x004e4942,4);
const result=Buffer.concat([header,json,bh,bin]);fs.writeFileSync(output,result);
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
fs.writeFileSync(path.join(work,'model-patch.json'),JSON.stringify({sourceSha256:hash(raw),sha256:hash(result),changes},null,2)+'\n');console.log(changes);
