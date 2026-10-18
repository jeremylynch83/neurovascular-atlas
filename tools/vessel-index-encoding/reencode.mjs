// Re-encode only index buffers whose every decoded index remains bit-exact.
// Triangle encoding can rotate triangle corners. Any such buffer is retained
// unchanged, as are all vertex/normal streams. No surface simplification occurs.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {MeshoptEncoder,MeshoptDecoder}from'meshoptimizer';
import {MeshoptDecoder as BrowserDecoder}from'three/addons/libs/meshopt_decoder.module.js';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready,BrowserDecoder.ready]);
const [input,output]=process.argv.slice(2);assert(input&&output,'Usage: node reencode.mjs INPUT.glb OUTPUT.glb');
const source=fs.readFileSync(input),length=source.readUInt32LE(12),original=JSON.parse(source.subarray(20,20+length)),doc=structuredClone(original),binary=source.subarray(28+length);
assert(source.toString('ascii',0,4)==='glTF'&&source.readUInt32LE(8)===source.length);
const usedIndexViews=new Set();for(const mesh of doc.meshes)for(const p of mesh.primitives)if(p.indices!==undefined)usedIndexViews.add(doc.accessors[p.indices].bufferView);
const patches=new Map();let rotated=0,unchanged=0;const records=[];
for(const id of usedIndexViews){
 const v=doc.bufferViews[id],e=v.extensions?.EXT_meshopt_compression;assert(e&&e.buffer===0);
 if(e.mode!=='INDICES'){unchanged++;continue;}
 assert(!e.filter||e.filter==='NONE');assert(e.count%3===0);assert(e.byteStride===4||e.byteStride===2);
 const raw=Buffer.alloc(v.byteLength);MeshoptDecoder.decodeGltfBuffer(raw,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode);
 const encoded=MeshoptEncoder.encodeIndexBuffer(raw,e.count,e.byteStride),check=Buffer.alloc(raw.length);
 MeshoptDecoder.decodeGltfBuffer(check,e.count,e.byteStride,encoded,'TRIANGLES');
 if(!raw.equals(check)){rotated++;continue;}
 if(encoded.length>=e.byteLength){unchanged++;continue;}
 // Test both the authoring decoder and the exact decoder bundled by Three.js.
 BrowserDecoder.decodeGltfBuffer(check,e.count,e.byteStride,encoded,'TRIANGLES');assert.deepEqual(check,raw);
 patches.set(id,encoded);records.push({bufferView:id,indices:e.count,beforeBytes:e.byteLength,afterBytes:encoded.length,decodedIndicesSha256:crypto.createHash('sha256').update(raw).digest('hex')});
}
let offset=0;const chunks=[];
for(let i=0;i<doc.bufferViews.length;i++){
 const e=doc.bufferViews[i].extensions.EXT_meshopt_compression,p=patches.get(i),data=p??binary.subarray(e.byteOffset,e.byteOffset+e.byteLength);
 const pad=(-offset)&3;if(pad){chunks.push(Buffer.alloc(pad));offset+=pad;}
 e.byteOffset=offset;e.byteLength=data.length;if(p)e.mode='TRIANGLES';chunks.push(data);offset+=data.length;
}
if(offset%4)chunks.push(Buffer.alloc(4-offset%4));const bin=Buffer.concat(chunks);doc.buffers[0].byteLength=bin.length;
let js=Buffer.from(JSON.stringify(doc));if(js.length%4)js=Buffer.concat([js,Buffer.alloc(4-js.length%4,32)]);
const header=Buffer.alloc(20),binHeader=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+js.length+bin.length,8);header.writeUInt32LE(js.length,12);header.writeUInt32LE(0x4e4f534a,16);binHeader.writeUInt32LE(bin.length);binHeader.writeUInt32LE(0x004e4942,4);
const result=Buffer.concat([header,js,binHeader,bin]);
// Compare the decoded bytes of every view, including filtered normals. This
// covers all accessors, padding, indices, and source face/corner order.
for(let i=0;i<doc.bufferViews.length;i++){
 const before=original.bufferViews[i],after=doc.bufferViews[i],x=before.extensions.EXT_meshopt_compression,y=after.extensions.EXT_meshopt_compression;
 assert.equal(before.byteLength,after.byteLength);const a=Buffer.alloc(before.byteLength),b=Buffer.alloc(after.byteLength);
 BrowserDecoder.decodeGltfBuffer(a,x.count,x.byteStride,binary.subarray(x.byteOffset,x.byteOffset+x.byteLength),x.mode,x.filter);
 BrowserDecoder.decodeGltfBuffer(b,y.count,y.byteStride,bin.subarray(y.byteOffset,y.byteOffset+y.byteLength),y.mode,y.filter);assert.deepEqual(a,b,`Changed decoded view ${i}`);
}
for(const k of Object.keys(original).filter(k=>!['buffers','bufferViews'].includes(k)))assert.deepEqual(doc[k],original[k],k);
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,result);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const report={input:path.basename(input),output:path.basename(output),beforeBytes:source.length,afterBytes:result.length,beforeSha256:hash(source),afterSha256:hash(result),changedIndexBuffers:patches.size,rotationCandidatesRejected:rotated,otherIndexBuffersRetained:unchanged,allDecodedBufferViewsExact:doc.bufferViews.length,allSceneAndAccessorMetadataExact:true,records};
fs.writeFileSync(output+'.report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,records:undefined}));
