// Decode one asset into a content-addressed, reusable authoring cache.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const [source,root,output]=process.argv.slice(2),raw=fs.readFileSync(source),jl=raw.readUInt32LE(12);
const doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl),cache=new Map();
if(raw.toString('ascii',0,4)!=='glTF'||raw.readUInt32LE(8)!==raw.length)throw Error('Invalid GLB');
for(const n of doc.nodes){if(n.translation?.some(x=>x!==0)||n.scale?.some(x=>x!==1)||n.rotation?.some((x,i)=>x!==[0,0,0,1][i])||n.matrix?.some((x,i)=>x!==[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1][i]))throw Error('Bake node transforms before native repair');}
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
function access(id){
 const a=doc.accessors[id],v=doc.bufferViews[a.bufferView];let bytes=cache.get(a.bufferView);
 if(!bytes){const e=v.extensions?.EXT_meshopt_compression;bytes=Buffer.alloc(v.byteLength);if(e)MeshoptDecoder.decodeGltfBuffer(bytes,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(bytes,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);cache.set(a.bufferView,bytes)}
 const width={VEC3:3,SCALAR:1}[a.type],size={5123:2,5125:4,5126:4}[a.componentType];if(!width||!size)throw Error('Unsupported accessor');
 const out=Buffer.alloc(a.count*width*4),stride=v.byteStride??size*width;
 for(let i=0;i<a.count;i++)for(let k=0;k<width;k++){const pos=(a.byteOffset??0)+i*stride+k*size;if(a.componentType===5126)out.writeFloatLE(bytes.readFloatLE(pos),(i*width+k)*4);else out.writeUInt32LE(size===2?bytes.readUInt16LE(pos):bytes.readUInt32LE(pos),(i*width+k)*4)}return out;
}
const rows=[];fs.mkdirSync(path.join(root,'geometry'),{recursive:true});
for(const n of doc.nodes.filter(n=>n.mesh!==undefined)){
 const p=doc.meshes[n.mesh].primitives[0],positions=access(p.attributes.POSITION),indices=access(p.indices);
 const key=hash(Buffer.concat([positions,indices])),dir=path.join(root,'geometry',key);fs.mkdirSync(dir,{recursive:true});
 for(const [name,bytes]of [['positions.bin',positions],['indices.bin',indices]]){const file=path.join(dir,name);if(!fs.existsSync(file)||fs.statSync(file).size!==bytes.length){const temp=file+'.'+process.pid+'.tmp';fs.writeFileSync(temp,bytes);fs.renameSync(temp,file)}}
 const bounds=[doc.accessors[p.attributes.POSITION].min,doc.accessors[p.attributes.POSITION].max];
 rows.push({name:n.name,key,vertices:positions.length/12,triangles:indices.length/12,bounds});
}
fs.writeFileSync(output,JSON.stringify({schema:1,sourceSha256:hash(raw),meshes:rows}));
