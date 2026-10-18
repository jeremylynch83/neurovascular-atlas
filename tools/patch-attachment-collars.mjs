// Authoring tool: append lossless geometry for accepted native attachment repairs.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const [work,source,output]=process.argv.slice(2),accepted=JSON.parse(fs.readFileSync(path.join(work,'accepted-corrections.json'))).accepted;
assert(accepted.length&&accepted.every(r=>r.passed));
const raw=fs.readFileSync(source),jl=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl),chunks=[binary];
let encodedOffset=binary.length,decodedOffset=doc.buffers[1].byteLength;
function add(bytes,count,stride,accessor,mode='ATTRIBUTES',filter){
 const encoded=Buffer.from(MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,mode)),padding=Buffer.alloc((-encoded.length)&3);
 const decoded=Buffer.alloc(bytes.length);MeshoptDecoder.decodeGltfBuffer(decoded,count,stride,encoded,mode,filter);if(!filter)assert(decoded.equals(bytes));
 const view=doc.bufferViews.length,target=mode==='INDICES'?34963:34962;
 doc.bufferViews.push({buffer:1,byteOffset:decodedOffset,byteLength:bytes.length,...(target===34962?{byteStride:stride}:{}),target,extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:encodedOffset,byteLength:encoded.length,count,byteStride:stride,mode,...(filter?{filter}:{})}}});
 const id=doc.accessors.length;doc.accessors.push({...accessor,count,bufferView:view,byteOffset:0});chunks.push(encoded,padding);encodedOffset+=encoded.length+padding.length;decodedOffset+=bytes.length;return id;
}
const changes=[];
for(const row of accepted){
 const node=doc.nodes.find(n=>n.name===row.node);if(!node)continue;const primitive=doc.meshes[node.mesh].primitives[0];assert.deepEqual(Object.keys(primitive.attributes).sort(),['NORMAL','POSITION']);
 const bytes=fs.readFileSync(path.join(work,'candidate',row.node+'.positions.bin')),indices=fs.readFileSync(path.join(work,'candidate',row.node+'.indices.bin')),normals=fs.readFileSync(path.join(work,'candidate',row.node+'.normals.bin'));
 const count=bytes.length/12;assert.equal(normals.length,count*12);
 const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity],nn=new Float32Array(count*4);
 for(let i=0;i<count;i++)for(let k=0;k<3;k++){const p=bytes.readFloatLE(i*12+k*4);assert(Number.isFinite(p));lo[k]=Math.min(lo[k],p);hi[k]=Math.max(hi[k],p);nn[i*4+k]=normals.readFloatLE(i*12+k*4);}
 primitive.attributes.POSITION=add(bytes,count,12,{componentType:5126,type:'VEC3',min:lo,max:hi});
 primitive.attributes.NORMAL=add(Buffer.from(MeshoptEncoder.encodeFilterOct(nn,count,8,12)),count,8,{componentType:5122,type:'VEC3',normalized:true},'ATTRIBUTES','OCTAHEDRAL');
 primitive.indices=add(indices,indices.length/4,4,{componentType:5125,type:'SCALAR'},'INDICES');
 changes.push({node:row.node,vertices:count,triangles:indices.length/12,positionSha256:crypto.createHash('sha256').update(bytes).digest('hex'),indexSha256:crypto.createHash('sha256').update(indices).digest('hex'),bounds:[lo,hi],positionEncoding:'lossless meshopt Float32'});
}
assert(changes.length);doc.buffers[0].byteLength=encodedOffset;doc.buffers[1].byteLength=decodedOffset;
let json=Buffer.from(JSON.stringify(doc));json=Buffer.concat([json,Buffer.alloc((-json.length)&3,32)]);const bin=Buffer.concat(chunks),header=Buffer.alloc(20),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);header.writeUInt32LE(json.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bin.length,0);bh.writeUInt32LE(0x004e4942,4);
const result=Buffer.concat([header,json,bh,bin]);fs.writeFileSync(output,result);fs.writeFileSync(path.join(work,'model-patch.json'),JSON.stringify({sourceSha256:crypto.createHash('sha256').update(raw).digest('hex'),sha256:crypto.createHash('sha256').update(result).digest('hex'),changes},null,2)+'\n');console.log(JSON.stringify(changes));
