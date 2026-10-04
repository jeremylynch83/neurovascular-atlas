// Optional authoring tool; builds the separate, losslessly compressed venous asset.
import fs from 'node:fs';
import { MeshoptEncoder, MeshoptDecoder } from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const input=process.argv[2]??'.authoring/venous/venous-raw.glb';
const output=process.argv[3]??'public/anatomy/models/venous.glb';
const raw=fs.readFileSync(input),jlen=raw.readUInt32LE(12);
const doc=JSON.parse(raw.subarray(20,20+jlen));const bin=raw.subarray(28+jlen);
const chunks=[];let compressedOffset=0,decodedOffset=0;
const indexViews=new Set(doc.meshes.flatMap(m=>m.primitives.map(p=>doc.accessors[p.indices]?.bufferView)));
for(const [i,v] of doc.bufferViews.entries()){
  const accessor=doc.accessors.find(a=>a.bufferView===i);
  const components={SCALAR:1,VEC2:2,VEC3:3,VEC4:4}[accessor.type];
  const componentBytes={5121:1,5123:2,5125:4,5126:4}[accessor.componentType];
  const stride=v.byteStride??components*componentBytes, count=accessor.count;
  if((accessor.byteOffset??0)!==0||stride*count!==v.byteLength)throw Error(`Non-packed authoring view ${i}`);
  // INDICES mode preserves triangle ordering exactly (TRIANGLES may rotate indices).
  const mode=indexViews.has(i)?'INDICES':'ATTRIBUTES';
  const bytes=bin.subarray(v.byteOffset,v.byteOffset+v.byteLength);
  const encoded=MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,mode);
  const decoded=new Uint8Array(bytes.length);MeshoptDecoder.decodeGltfBuffer(decoded,count,stride,encoded,mode);
  if(!Buffer.from(decoded).equals(bytes))throw Error(`Roundtrip mismatch ${i}`);
  v.buffer=1;v.byteOffset=decodedOffset;decodedOffset+=v.byteLength;
  v.extensions={EXT_meshopt_compression:{buffer:0,byteOffset:compressedOffset,byteLength:encoded.length,byteStride:stride,count,mode}};
  const pad=(-encoded.length)&3;chunks.push(Buffer.from(encoded),Buffer.alloc(pad));compressedOffset+=encoded.length+pad;
}
doc.buffers=[{byteLength:compressedOffset},{byteLength:decodedOffset,extensions:{EXT_meshopt_compression:{fallback:true}}}];
doc.extensionsUsed=['EXT_meshopt_compression'];doc.extensionsRequired=['EXT_meshopt_compression'];
let j=Buffer.from(JSON.stringify(doc));j=Buffer.concat([j,Buffer.alloc((-j.length)&3,32)]);const b=Buffer.concat(chunks);
const h=Buffer.alloc(20);h.write('glTF');h.writeUInt32LE(2,4);h.writeUInt32LE(28+j.length+b.length,8);h.writeUInt32LE(j.length,12);h.writeUInt32LE(0x4e4f534a,16);
const bh=Buffer.alloc(8);bh.writeUInt32LE(b.length);bh.writeUInt32LE(0x004e4942,4);fs.writeFileSync(output,Buffer.concat([h,j,bh,b]));
console.log(JSON.stringify({inputBytes:raw.length,outputBytes:fs.statSync(output).size,buffersVerified:doc.bufferViews.length}));
