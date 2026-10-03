// Developer-only lossless decoder for geometry authoring.
import fs from 'node:fs';
import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const [input,output]=process.argv.slice(2),src=fs.readFileSync(input),jl=src.readUInt32LE(12),doc=JSON.parse(src.subarray(20,20+jl)),bin=src.subarray(28+jl);
let offset=0;const chunks=[];
for(const bv of doc.bufferViews){const ext=bv.extensions?.EXT_meshopt_compression;let data;
 if(ext){data=Buffer.alloc(ext.count*ext.byteStride);MeshoptDecoder.decodeGltfBuffer(data,ext.count,ext.byteStride,bin.subarray(ext.byteOffset,ext.byteOffset+ext.byteLength),ext.mode,ext.filter);delete bv.extensions;}
 else data=bin.subarray(bv.byteOffset??0,(bv.byteOffset??0)+bv.byteLength);
 const pad=(4-offset%4)%4;if(pad){chunks.push(Buffer.alloc(pad));offset+=pad;}
 bv.buffer=0;bv.byteOffset=offset;bv.byteLength=data.length;chunks.push(data);offset+=data.length;
}
doc.buffers=[{byteLength:offset}];for(const key of ['extensionsRequired','extensionsUsed'])if(doc[key])doc[key]=doc[key].filter(x=>x!=='EXT_meshopt_compression');
const j=Buffer.from(JSON.stringify(doc)),jb=Buffer.concat([j,Buffer.alloc((4-j.length%4)%4,32)]),b=Buffer.concat(chunks),bb=Buffer.concat([b,Buffer.alloc((4-b.length%4)%4)]),head=Buffer.alloc(20),bh=Buffer.alloc(8);
head.write('glTF');head.writeUInt32LE(2,4);head.writeUInt32LE(28+jb.length+bb.length,8);head.writeUInt32LE(jb.length,12);head.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bb.length);bh.writeUInt32LE(0x004e4942,4);fs.writeFileSync(output,Buffer.concat([head,jb,bh,bb]));console.log(output);
