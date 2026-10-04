import fs from 'node:fs';
import path from 'node:path';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'meshoptimizer';

const out = path.resolve(process.argv[2]??'../comparison-work');
fs.mkdirSync(out, {recursive:true});
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
await MeshoptDecoder.ready;
for (const [label,file] of [
  ['bones','public/anatomy/models/craniofacial.glb'],
  ['arteries','public/anatomy/models/complete-circulation.glb'],
  ['before',process.argv[3]??'../before/public/anatomy/models/venous.glb'],
  ['after','public/anatomy/models/venous.glb'],
]) {
  const bytes = fs.readFileSync(file);
  const gltf = await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  gltf.scene.updateMatrixWorld(true);
  const fd=fs.openSync(`${out}/${label}.bin`,'w');
  let offset=0; const records=[];
  gltf.scene.traverse(mesh=>{
    if(!mesh.isMesh)return;
    const assoc=gltf.parser.associations.get(mesh);
    const name=gltf.parser.json.nodes[assoc.nodes]?.name??mesh.name;
    const geometry=mesh.geometry.clone().applyMatrix4(mesh.matrixWorld);
    const a=geometry.getAttribute('position');
    const p=new Float32Array(a.count*3);
    for(let i=0;i<a.count;i++)p.set([a.getX(i),a.getY(i),a.getZ(i)],i*3);
    const ix=Uint32Array.from(geometry.index.array);
    records.push({name,positionOffset:offset,vertices:a.count,indexOffset:offset+p.byteLength,indices:ix.length});
    for(const arr of [p,ix]){const b=Buffer.from(arr.buffer);let k=0;while(k<b.length)k+=fs.writeSync(fd,b,k,Math.min(4*1024*1024,b.length-k));offset+=b.length;}
  });
  fs.closeSync(fd);
  fs.writeFileSync(`${out}/${label}.json`,JSON.stringify(records));
  console.log(`${label}: ${records.length} exported meshes`);
}
