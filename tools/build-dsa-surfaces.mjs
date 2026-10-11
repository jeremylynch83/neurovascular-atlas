// Optional authoring tool. Python needs numpy/trimesh; normal app builds use
// the checked-in result and do not install those packages.
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
const root=path.resolve(import.meta.dirname,'..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-dsa-'));
const manifest=JSON.parse(fs.readFileSync(root+'/public/anatomy/manifest.json'));
const presets=JSON.parse(fs.readFileSync(root+'/src/presetVessels.json'));
const ids=new Set(Object.values(presets).flat());
const rows=manifest.structures.filter(s=>s.asset&&(ids.has(s.id)||s.system==='vein'));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
try{
 for(const file of new Set(rows.map(s=>s.asset.file))){
  const b=fs.readFileSync(root+'/public/anatomy/'+file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
  g.scene.updateMatrixWorld(true);
  g.scene.traverse(o=>{
   if(!o.isMesh)return;
   const node=g.parser.json.nodes[g.parser.associations.get(o).nodes],s=rows.find(s=>s.asset.file===file&&s.asset.node===node.name);if(!s)return;
   const p=o.geometry.attributes.position,vertices=new Float32Array(p.count*3);
   for(let i=0;i<p.count;i++)for(let k=0;k<3;k++)vertices[i*3+k]=p.getComponent(i,k);
   fs.writeFileSync(temp+'/'+s.id+'.vertices',Buffer.from(vertices.buffer));
   fs.writeFileSync(temp+'/'+s.id+'.indices',Buffer.from(new Uint32Array(o.geometry.index.array).buffer));
  });
  g.scene.traverse(o=>{if(o.isMesh)o.geometry.dispose()});
 }
 const repair=spawnSync('python3',[root+'/tools/close-dsa-surfaces.py',temp],{stdio:'inherit'});if(repair.status!==0)throw Error('DSA closure failed');
 const metadata=JSON.parse(fs.readFileSync(temp+'/surfaces.json'));
 metadata.assetRevisions=manifest.assetRevisions;
 metadata.sourceHashes=Object.fromEntries([...new Set(rows.map(s=>s.asset.file))].map(file=>[file,crypto.createHash('sha256').update(fs.readFileSync(root+'/public/anatomy/'+file)).digest('hex')]));
 fs.writeFileSync(root+'/public/anatomy/dsa-surfaces.json',JSON.stringify(metadata));
 console.log('DSA surfaces',Object.keys(metadata.entries).length,'closed projection recipes');
 fs.rmSync(temp,{recursive:true,force:true});
}catch(error){console.error('DSA authoring input retained at',temp);throw error}
