// Independent geometric invariants for the checked-in DSA projection recipes.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
const root=path.resolve(import.meta.dirname,'../..');
const manifest=JSON.parse(fs.readFileSync(root+'/public/anatomy/manifest.json'));
const data=JSON.parse(fs.readFileSync(root+'/public/anatomy/dsa-surfaces.json'));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);let meshes=0,faces=0;const invalid=[];
for(const file of new Set(manifest.structures.filter(s=>data.entries[s.id]).map(s=>s.asset.file))){
 const bytes=fs.readFileSync(root+'/public/anatomy/'+file);
 assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),data.sourceHashes[file]);
 const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 gltf.scene.traverse(o=>{
  if(!o.isMesh)return;
  const node=gltf.parser.json.nodes[gltf.parser.associations.get(o).nodes];
  const structure=manifest.structures.find(s=>s.asset?.file===file&&s.asset.node===node.name);
  const recipe=data.entries[structure?.id];if(!recipe)return;
  const p=o.geometry.attributes.position;assert.equal(p.count,recipe.vertexCount);
  const vertices=Array.from({length:p.count},(_,i)=>[p.getX(i),p.getY(i),p.getZ(i)]);
  vertices.push(...recipe.extra);
  const removed=new Set(recipe.removed),flips=new Set(recipe.flips),index=o.geometry.index.array,triangles=[];
  for(let i=0;i<index.length/3;i++)if(!removed.has(i)){
   const [a,b,c]=index.slice(i*3,i*3+3);triangles.push(recipe.reverse!==flips.has(i)?[a,c,b]:[a,b,c]);
  }
  for(let i=0;i<recipe.caps.length;i+=3)triangles.push(recipe.caps.slice(i,i+3));
  assert.equal(triangles.length,recipe.faces);assert(recipe.volumeMm3>0);
  const canonical=new Map(),ids=vertices.map(v=>{
   const k=v.map(x=>Math.round(x*1e8)).join(',');if(!canonical.has(k))canonical.set(k,canonical.size);return canonical.get(k);
  }),edges=new Map();
  for(const t of triangles)for(let k=0;k<3;k++){
   assert(t[k]<vertices.length);const a=ids[t[k]],b=ids[t[(k+1)%3]],key=a<b?a+','+b:b+','+a;
   if(a===b)continue; // A zero-length edge has no oriented boundary.
   const e=edges.get(key)??[0,0];e[0]++;e[1]+=a<b?1:-1;edges.set(key,e);
  }
  // Closed components can touch at a geometric edge. Every incidence must
  // still have its opposite partner, with zero oriented boundary.
  const bad=[...edges].filter(([key,e])=>e[0]<2||e[0]%2!==0||e[1]!==0);if(bad.length)invalid.push({id:structure.id,edges:bad.length,sample:bad.slice(0,2)});
  meshes++;faces+=triangles.length;
 });
 gltf.scene.traverse(o=>{if(o.isMesh)o.geometry.dispose()});
}
console.log('Invalid:',JSON.stringify(invalid));assert.equal(invalid.length,0);assert.equal(meshes,Object.keys(data.entries).length);assert.equal(meshes,828);
console.log('Closed and oriented DSA proxies:',meshes,'meshes,',faces,'triangles. Source hashes match.');
