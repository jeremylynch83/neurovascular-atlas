// Authoring only: refresh caches after a proven fixed-boundary vein deformation.
// Usage: node tools/refresh-fixed-boundary-veins.mjs <old-venous.glb> <report.json>
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {flowGraphSource} from '../src/flowGeometry.ts';
const root=new URL('../',import.meta.url).pathname,base=root+'public/anatomy/';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const manifest=read(root+'anatomy/generated/complete_manifest.json'),surfaces=read(base+'dsa-surfaces.json'),flow=read(base+'dsa-flow.json');
const oldBytes=fs.readFileSync(process.argv[2]),newBytes=fs.readFileSync(base+'models/venous.glb');
const oldHash=hash(oldBytes),newHash=hash(newBytes);
assert.equal(flow.graphSource,flowGraphSource(manifest));assert.equal(flow.graphHash,hash(flow.graphSource));
assert.equal(flow.generatorHash,hash(fs.readFileSync(root+'tools/build-dsa-flow.mjs')+fs.readFileSync(root+'src/flowGeometry.ts')));
for(const cache of [surfaces,flow])for(const [file,sha] of Object.entries(cache.sourceHashes))assert.equal(sha,file==='models/venous.glb'?oldHash:hash(fs.readFileSync(base+file)));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function meshes(bytes){const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');const rows=new Map();gltf.scene.traverse(o=>{if(o.isMesh)rows.set(gltf.parser.json.nodes[gltf.parser.associations.get(o).nodes].name,o.geometry)});return rows}
const before=await meshes(oldBytes),after=await meshes(newBytes),changes=[];
assert.equal(before.size,after.size);
for(const [name,g] of after){
 const old=before.get(name);assert(old);assert.deepEqual(g.index.array,old.index.array);
 const p=g.attributes.position,op=old.attributes.position;assert.equal(p.count,op.count);
 const a=Array.from({length:p.count},(_,i)=>[p.getX(i),p.getY(i),p.getZ(i)]),b=Array.from({length:op.count},(_,i)=>[op.getX(i),op.getY(i),op.getZ(i)]);
 if(a.every((q,i)=>q.every((v,k)=>v===b[i][k])))continue;
 const s=manifest.structures.find(s=>s.asset?.file==='models/venous.glb'&&s.asset.node===name);assert(s);
 const edges=new Map(),index=g.index.array;
 for(let i=0;i<index.length;i+=3)for(let k=0;k<3;k++){const x=index[i+k],y=index[i+(k+1)%3],key=x<y?x+','+y:y+','+x;edges.set(key,(edges.get(key)??0)+1)}
 let fixed=0;for(const [key,n] of edges)if(n===1)for(const v of key.split(',').map(Number)){assert.deepEqual(a[v],b[v]);fixed++}
 const recipe=surfaces.entries[s.id];assert(recipe);assert.equal(recipe.vertexCount,p.count);
 const vertices=[...a,...recipe.extra],removed=new Set(recipe.removed),flips=new Set(recipe.flips),triangles=[];
 for(let i=0;i<index.length/3;i++)if(!removed.has(i)){const [x,y,z]=index.slice(i*3,i*3+3);triangles.push(recipe.reverse!==flips.has(i)?[x,z,y]:[x,y,z])}
 for(let i=0;i<recipe.caps.length;i+=3)triangles.push(recipe.caps.slice(i,i+3));assert.equal(triangles.length,recipe.faces);
 // Canonical coordinates weld native partition seams, as in the full validator.
 const canonical=new Map(),ids=vertices.map(v=>{const key=v.map(x=>Math.round(x*1e8)).join(',');if(!canonical.has(key))canonical.set(key,canonical.size);return canonical.get(key)}),balance=new Map();let volume=0;
 for(const t of triangles){const [u,v,w]=t.map(i=>vertices[i]);volume+=(u[0]*(v[1]*w[2]-v[2]*w[1])+u[1]*(v[2]*w[0]-v[0]*w[2])+u[2]*(v[0]*w[1]-v[1]*w[0]))/6;for(let k=0;k<3;k++){const x=ids[t[k]],y=ids[t[(k+1)%3]];if(x===y)continue;const key=x<y?x+','+y:y+','+x;balance.set(key,(balance.get(key)??0)+(x<y?1:-1))}}
 assert([...balance.values()].every(n=>n===0));assert(volume>0);recipe.volumeMm3=volume;
 flow.veinSites[s.id]=[0,1,2].map(k=>(Math.min(...a.map(p=>p[k]))+Math.max(...a.map(p=>p[k])))/2);
 changes.push({id:s.id,fixedBoundaryEndpointChecks:fixed,projectionFaces:triangles.length,volumeMm3:volume,veinSite:flow.veinSites[s.id]});
}
assert.deepEqual(changes.map(s=>s.id).sort(),(manifest.anatomicalBatch4Review?.correctedVessels??manifest.anatomicalBatch3Review.correctedStructures).slice().sort());
for(const cache of [surfaces,flow])cache.sourceHashes['models/venous.glb']=newHash;
surfaces.assetRevisions=manifest.assetRevisions;
fs.writeFileSync(base+'dsa-surfaces.json',JSON.stringify(surfaces));fs.writeFileSync(base+'dsa-flow.json',JSON.stringify(flow));
const report={oldHash,newHash,changes,arterialCoursesUnchanged:true,graphUnchanged:true,projectionTopologyUnchanged:true};fs.writeFileSync(process.argv[3],JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
