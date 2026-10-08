import fs from 'node:fs';
import path from 'node:path';
import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const root=path.resolve('tools/ica-smooth-v0939');
const raw=fs.readFileSync(root+'/baseline/complete-circulation.glb'),len=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+len)),bin=raw.subarray(28+len);
const changed=JSON.parse(fs.readFileSync(root+'/candidate/revision.json')).changed;
for(const row of changed){
 const node=doc.nodes.find(n=>n.name===row.node),prim=doc.meshes[node.mesh].primitives[0],a=doc.accessors[prim.attributes.NORMAL],v=doc.bufferViews[a.bufferView],e=v.extensions?.EXT_meshopt_compression,b=Buffer.alloc(v.byteLength);
 if(e)MeshoptDecoder.decodeGltfBuffer(b,e.count,e.byteStride,bin.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else bin.copy(b,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);
 const out=Buffer.alloc(a.count*12),stride=v.byteStride??(a.componentType===5126?12:6);
 for(let i=0;i<a.count;i++)for(let j=0;j<3;j++){const o=(a.byteOffset??0)+i*stride+j*(a.componentType===5126?4:2);out.writeFloatLE(a.componentType===5126?b.readFloatLE(o):Math.max(-1,b.readInt16LE(o)/32767),i*12+j*4);}
 fs.writeFileSync(root+'/decoded/'+row.node+'.normals.bin',out);
}
