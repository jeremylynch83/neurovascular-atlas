// Independent Three.js GLTFLoader comparison against an unpacked v0.9.118.
import fs from'node:fs';import path from'node:path';import assert from'node:assert/strict';import crypto from'node:crypto';
import{GLTFLoader}from'three/addons/loaders/GLTFLoader.js';import{MeshoptDecoder}from'three/addons/libs/meshopt_decoder.module.js';
const root=path.resolve(import.meta.dirname,'../..'),baseline=path.resolve(process.argv[2]);
const read=p=>JSON.parse(fs.readFileSync(p)),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const old=read(baseline+'/public/anatomy/manifest.json'),now=read(root+'/public/anatomy/manifest.json');
await MeshoptDecoder.ready;const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function geometry(file){
 const b=fs.readFileSync(file),gltf=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),''),result=[];gltf.scene.updateMatrixWorld(true);
 gltf.scene.traverse(o=>{if(!o.isMesh)return;const attributes={};
  for(const[name,a]of Object.entries(o.geometry.attributes)){
   const v=new Float64Array(a.count*a.itemSize);for(let i=0;i<a.count;i++)for(let k=0;k<a.itemSize;k++)v[i*a.itemSize+k]=a.getComponent(i,k);
   attributes[name]={count:a.count,itemSize:a.itemSize,normalised:a.normalized,sha256:sha(Buffer.from(v.buffer))};
  }
  result.push({name:o.name,node:gltf.parser.associations.get(o)?.nodes,matrix:o.matrixWorld.toArray(),attributes,
   indices:sha(Buffer.from(Uint32Array.from(o.geometry.index.array).buffer)),indexCount:o.geometry.index.count,groups:o.geometry.groups});o.geometry.dispose();
 });return result;
}
let meshes=0,triangles=0;const assets=[];
for(const file of Object.keys(now.assetRevisions)){
 const before=await geometry(baseline+'/public/anatomy/'+file),after=await geometry(root+'/public/anatomy/'+file);assert.deepEqual(after,before,file);
 const b=fs.readFileSync(root+'/public/anatomy/'+file);assert.equal(sha(b).slice(0,20),now.assetRevisions[file]);assert.equal(b.length,now.assetByteSizes[file]);
 if(['models/brain-context.glb','models/craniofacial.glb'].includes(file))assert.deepEqual(b,fs.readFileSync(baseline+'/public/anatomy/'+file));
 meshes+=after.length;triangles+=after.reduce((n,g)=>n+g.indexCount/3,0);assets.push({file,meshes:after.length,allAttributesAndIndicesExact:true});console.log('Exact',file,after.length);
}
assert.equal(meshes,1250);
function contract(m){const d=structuredClone(m);for(const k of['release','assetRevisions','assetByteSizes','currentDeferredReviewRegistry','vesselLosslessIndexEncoding'])delete d[k];for(const s of d.structures)if(s.vesselCourse)delete s.vesselCourse.geometrySha256;return d}
assert.deepEqual(contract(now),contract(old),'No anatomical contract or brain-anchor changes');
for(const file of['dsa-surfaces.json','dsa-flow.json']){
 const before=read(baseline+'/public/anatomy/'+file),after=read(root+'/public/anatomy/'+file);
 for(const[asset,h]of Object.entries(after.sourceHashes))assert.equal(sha(fs.readFileSync(root+'/public/anatomy/'+asset)),h);
 for(const d of[before,after]){delete d.sourceHashes;delete d.assetRevisions;}assert.deepEqual(after,before,file+' payload');
}
for(const file of['ANATOMICAL_ISSUES.json','ANATOMICAL_ISSUES.md','public/anatomy/brain-landmarks.json','tests/staged-loading/expected-geometry.json'])assert.deepEqual(fs.readFileSync(root+'/'+file),fs.readFileSync(baseline+'/'+file),file);
const previous=read(baseline+'/'+old.currentDeferredReviewRegistry),current=read(root+'/'+now.currentDeferredReviewRegistry);
assert.deepEqual(current.cases,previous.cases);assert.deepEqual(current.requiredImplementationSha256,previous.requiredImplementationSha256);
assert.equal(current.requiredSourceAssetSha256['models/brain-context.glb'],previous.requiredSourceAssetSha256['models/brain-context.glb']);
for(const[file,h]of Object.entries(current.requiredSourceAssetSha256))if(file!=='models/brain-context.glb')assert.equal(sha(fs.readFileSync(root+'/public/anatomy/'+file)),h);
const report={passed:true,release:now.release,baseline:old.release,meshes,triangles,assets,
 allDecodedCoordinatesNormalsAndTriangleIndicesExact:true,allNativeJunctionsAndSmallBranchesExact:true,
 dsaRecipesAndFlowExactExceptContainerHashes:true,brainAndBoneAssetsByteExact:true,
 allBrainAnchorBindingsExact:true,anatomicalIssueRegisterExact:true,previousBrainSpatialReviewRequirementRetained:true};
fs.writeFileSync(root+'/docs/vessel-index-geometry.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
