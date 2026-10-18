// Independent delivered-asset comparison with an unpacked v0.9.117 baseline.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {GLTFLoader}from'three/addons/loaders/GLTFLoader.js';import{MeshoptDecoder}from'meshoptimizer';
const root=path.resolve(import.meta.dirname,'../..'),baseline=path.resolve(process.argv[2]);
const read=p=>JSON.parse(fs.readFileSync(p)),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const manifest=read(root+'/public/anatomy/manifest.json'),prior=read(baseline+'/public/anatomy/manifest.json');
const trial=read(root+'/anatomy/source/brain-simplification-v0.9.118/trial.json'),results=new Map(trial.meshes.map(m=>[m.name,m]));
for(const file of Object.keys(manifest.assetRevisions)) {
 const a=fs.readFileSync(root+'/public/anatomy/'+file),b=fs.readFileSync(baseline+'/public/anatomy/'+file);
 assert.equal(hash(a).slice(0,20),manifest.assetRevisions[file]);assert.equal(a.length,manifest.assetByteSizes[file]);
 if(file!=='models/brain-context.glb')assert.deepEqual(a,b,file+' must remain byte-exact');
}
await MeshoptDecoder.ready;const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function load(file){const b=fs.readFileSync(file);return loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'')}
const before=await load(baseline+'/public/anatomy/models/brain-context.glb'),after=await load(root+'/public/anatomy/models/brain-context.glb');
for(const key of ['nodes','materials','scene','scenes'])assert.deepEqual(after.parser.json[key],before.parser.json[key],key);
const meshes=new Map();before.scene.traverse(o=>{if(o.isMesh)meshes.set(before.parser.json.nodes[before.parser.associations.get(o).nodes].name,o)});
let exact=0,changed=0,retainedVertices=0;
const vertex=(g,i)=>['position','normal'].flatMap(name=>{const a=g.getAttribute(name);return[a.getX(i),a.getY(i),a.getZ(i)]}).join(',');
after.scene.traverse(o=>{
 if(!o.isMesh)return;const name=after.parser.json.nodes[after.parser.associations.get(o).nodes].name,old=meshes.get(name),row=results.get(name);assert(old&&row);
 const p=o.geometry.getAttribute('position');assert.equal(p.count,row.afterVertices);assert.equal(o.geometry.index.count,row.afterTriangles*3);
 if(!row.changed){
  for(const name of ['position','normal']) {
   const a=o.geometry.getAttribute(name),b=old.geometry.getAttribute(name);assert.equal(a.count,b.count);
   for(let i=0;i<a.count;i++)for(let k=0;k<3;k++)assert.equal(a.getComponent(i,k),b.getComponent(i,k));
  }
  assert.deepEqual(o.geometry.index.array,old.geometry.index.array);exact++;
 }else{
  const originalVertices=new Set();for(let i=0;i<old.geometry.getAttribute('position').count;i++)originalVertices.add(vertex(old.geometry,i));
  for(let i=0;i<p.count;i++)assert(originalVertices.has(vertex(o.geometry,i)),name+' moved a vertex or changed a retained normal');
  retainedVertices+=p.count;changed++;
 }
});
assert.equal(exact+changed,193);assert.equal(changed,trial.changedMeshes);
function contract(m){
 const d=structuredClone(m);for(const k of ['release','assetRevisions','assetByteSizes','brainSimplificationTrial'])delete d[k];delete d.brainRegistration.registeredAssetSha256;
 for(const s of d.structures){if(s.vesselCourse)delete s.vesselCourse.brainAssetSha256;
  for(const a of[s.surfaceAnchor,...(s.secondarySurfaceAnchors??[])].filter(Boolean)){delete a.assetSha256;delete a.triangleIndex;}}
 return d;
}
assert.deepEqual(contract(manifest),contract(prior),'All catalogue semantics, anchor coordinates and barycentric weights must remain exact');
const oldRows=new Map(prior.structures.map(s=>[s.id,s])),newRows=new Map(manifest.structures.map(s=>[s.id,s]));
const currentMeshes=new Map();after.scene.traverse(o=>{if(o.isMesh)currentMeshes.set(after.parser.json.nodes[after.parser.associations.get(o).nodes].name,o)});
let anchors=0;
for(const s of manifest.structures){const previous=oldRows.get(s.id),oldAnchors=[previous.surfaceAnchor,...(previous.secondarySurfaceAnchors??[])].filter(Boolean),currentAnchors=[s.surfaceAnchor,...(s.secondarySurfaceAnchors??[])].filter(Boolean);
 for(let i=0;i<currentAnchors.length;i++){
  const a=currentAnchors[i],b=oldAnchors[i],name=newRows.get(a.structureId).asset.node;
  const g=currentMeshes.get(name).geometry,h=meshes.get(name).geometry;
  for(let k=0;k<3;k++){
   const p=g.getAttribute('position'),q=h.getAttribute('position'),vi=g.index.getX(a.triangleIndex*3+k),vj=h.index.getX(b.triangleIndex*3+k);
   for(let c=0;c<3;c++)assert.equal(p.getComponent(vi,c),q.getComponent(vj,c),'Protected anchor triangle vertex/order changed');
  }anchors++;
 }}
assert.equal(anchors,181);
assert.deepEqual(fs.readFileSync(root+'/public/anatomy/dsa-flow.json'),fs.readFileSync(baseline+'/public/anatomy/dsa-flow.json'));
const dsa=read(root+'/public/anatomy/dsa-surfaces.json'),oldDsa=read(baseline+'/public/anatomy/dsa-surfaces.json');delete dsa.assetRevisions;delete oldDsa.assetRevisions;assert.deepEqual(dsa,oldDsa);
for(const f of ['ANATOMICAL_ISSUES.json','ANATOMICAL_ISSUES.md'])assert.deepEqual(fs.readFileSync(root+'/'+f),fs.readFileSync(baseline+'/'+f));
const report={passed:true,release:manifest.release,brainMeshes:193,unchangedBrainMeshes:exact,changedBrainMeshes:changed,retainedVerticesCopiedExactly:retainedVertices,
 protectedAnchorTrianglesExact:anchors,otherGlbsByteExact:4,dsaRecipesAndFlowUnchanged:true,catalogueSemanticsAndAnchorPositionsExact:true};
fs.writeFileSync(root+'/docs/brain-simplification-geometry.json',JSON.stringify(report,null,2)+'\n');console.log(report);
