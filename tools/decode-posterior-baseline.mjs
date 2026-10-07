import fs from 'node:fs';
import crypto from 'node:crypto';
import {MeshoptDecoder} from 'meshoptimizer';
import path from 'node:path';
await MeshoptDecoder.ready;
const inputDir=process.argv[2],output=process.argv[3];fs.mkdirSync(output,{recursive:true});
const selected={'brain-context.glb':null,'craniofacial.glb':null,'complete-circulation.glb':null,'venous.glb':null,'complete-anastomoses.glb':null};
const metadata=[],assetHashes={};
for(const [file,wanted] of Object.entries(selected)){
 const raw=fs.readFileSync(path.join(inputDir,file)),length=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+length)),binary=raw.subarray(28+length);
 assetHashes[file]=crypto.createHash('sha256').update(raw).digest('hex');
 const names=wanted??doc.nodes.filter(n=>'mesh' in n).map(n=>n.name);const cache=new Map();
 function access(id){const a=doc.accessors[id],v=doc.bufferViews[a.bufferView];let bytes=cache.get(a.bufferView);if(!bytes){const e=v.extensions?.EXT_meshopt_compression;bytes=Buffer.alloc(v.byteLength);if(e)MeshoptDecoder.decodeGltfBuffer(bytes,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(bytes,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);cache.set(a.bufferView,bytes);}const size={5123:2,5125:4,5126:4}[a.componentType],width={VEC3:3,SCALAR:1}[a.type],stride=v.byteStride??size*width,out=Buffer.alloc(a.count*width*4);for(let i=0;i<a.count;i++)for(let j=0;j<width;j++){const pos=(a.byteOffset??0)+i*stride+j*size;if(a.componentType===5126)out.writeFloatLE(bytes.readFloatLE(pos),(i*width+j)*4);else out.writeUInt32LE(a.componentType===5123?bytes.readUInt16LE(pos):bytes.readUInt32LE(pos),(i*width+j)*4);}return out;}
 for(const name of names){const node=doc.nodes.find(n=>n.name===name);if(!node)throw Error(`Missing ${name}`);const primitive=doc.meshes[node.mesh].primitives[0];const positions=access(primitive.attributes.POSITION),indices=access(primitive.indices);fs.writeFileSync(`${output}/${name}.positions.bin`,positions);fs.writeFileSync(`${output}/${name}.indices.bin`,indices);metadata.push({name,file,vertices:positions.length/12,triangles:indices.length/12});}
}
fs.writeFileSync(`${output}/source-assets.json`,JSON.stringify(assetHashes,null,2));
fs.writeFileSync(`${output}/meshes.json`,JSON.stringify(metadata,null,2));console.log(metadata);
