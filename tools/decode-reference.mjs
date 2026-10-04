// One-off authoring reference extraction. Never runs during app build/load.
import fs from 'node:fs';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'meshoptimizer';
const out = process.argv[2] ?? '.authoring/venous';
fs.mkdirSync(out,{recursive:true});
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
await MeshoptDecoder.ready;
const fd=fs.openSync(`${out}/reference.bin`,'w');
let offset=0;const records=[];
for(const file of ['craniofacial','complete-circulation']) {
  const bytes=fs.readFileSync(`public/anatomy/models/${file}.glb`);
  const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  gltf.scene.updateMatrixWorld(true);
  gltf.scene.traverse(o=>{
    if(!o.isMesh)return;
    const assoc=gltf.parser.associations.get(o);
    const name=gltf.parser.json.nodes[assoc.nodes]?.name??o.name;
    const g=o.geometry.clone().applyMatrix4(o.matrixWorld);
    const a=g.getAttribute('position'),p=new Float32Array(a.count*3);
    for(let i=0;i<a.count;i++)p.set([a.getX(i),a.getY(i),a.getZ(i)],i*3);
    const ix=g.index?Uint32Array.from(g.index.array):Uint32Array.from({length:a.count},(_,i)=>i);
    g.computeBoundingBox();
    const rec={name,file,positionOffset:offset,vertices:a.count,indexOffset:offset+p.byteLength,indices:ix.length,bounds:[g.boundingBox.min.toArray(),g.boundingBox.max.toArray()]};
    for(const arr of [p,ix]){const b=Buffer.from(arr.buffer);let k=0;while(k<b.length)k+=fs.writeSync(fd,b,k,Math.min(4*1024*1024,b.length-k));offset+=b.length;}
    records.push(rec);
  });
}
fs.closeSync(fd);fs.writeFileSync(`${out}/reference.json`,JSON.stringify(records));
console.log(JSON.stringify({parts:records.length,bytes:offset}));
