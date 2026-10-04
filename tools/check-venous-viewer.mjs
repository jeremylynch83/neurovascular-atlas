// One-off interaction fixture; no browser/GPU performance claim.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'meshoptimizer';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const deps=process.env.VENOUS_QA_MODULES;
const {build}=await import(deps?pathToFileURL(path.resolve(deps,'esbuild/lib/main.js')).href:'esbuild');
for(const name of ['engine','catalogue'])await build({entryPoints:[`src/${name}.ts`],bundle:true,platform:'node',format:'esm',packages:'external',outfile:`tools/.qa/${name}.mjs`});
const {AnatomyEngine,pickAnatomy}=await import('./.qa/engine.mjs');
const {segmentGeometryMembers,geometrySubtrees,searchStructures}=await import('./.qa/catalogue.mjs');
const manifest=JSON.parse(fs.readFileSync('public/anatomy/manifest.json'));
const byId=new Map(manifest.structures.map(s=>[s.id,s]));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);await MeshoptDecoder.ready;
const entries=new Map();let triangles=0;
for(const file of new Set(manifest.structures.filter(s=>s.asset).map(s=>s.asset.file))){
 const bytes=fs.readFileSync(`public/anatomy/${file}`);const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.length),'');gltf.scene.updateMatrixWorld(true);
 const nodes=new Map();gltf.scene.traverse(o=>{if(o.isMesh){const a=gltf.parser.associations.get(o);nodes.set(gltf.parser.json.nodes[a.nodes].name,o)}});
 for(const s of manifest.structures.filter(s=>s.asset?.file===file)){
  const src=nodes.get(s.asset.node);assert(src,`Missing node ${s.id}`);
  const g=new THREE.BufferGeometry();
  for(const name of ['position','normal']){const a=src.geometry.getAttribute(name);assert(a,`${s.id} missing ${name}`);const arr=new Float32Array(a.count*3);for(let i=0;i<a.count;i++)arr.set([a.getX(i),a.getY(i),a.getZ(i)],i*3);assert(arr.every(Number.isFinite));g.setAttribute(name,new THREE.BufferAttribute(arr,3))}
  g.setIndex(src.geometry.index.clone());g.applyMatrix4(src.matrixWorld);g.computeBoundingBox();g.computeBoundingSphere();
  const mesh=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:s.color??'#888888',side:THREE.DoubleSide}));mesh.name=s.id;entries.set(s.id,{structure:s,mesh,baseOpacity:1});
  if(s.system==='vein')triangles+=g.index.count/3;
 }
}
const veins=[...entries.values()].filter(e=>e.structure.system==='vein');assert.equal(veins.length,104);
const stats=JSON.parse(fs.readFileSync(`docs/validation/venous-morphology-v${manifest.release}.json`));assert.equal(triangles,stats.triangles);
const fixture=(native)=>{const e=Object.create(AnatomyEngine.prototype);Object.assign(e,{manifest,entries,root:new THREE.Group(),vascularBatches:[],landmarkMarker:new THREE.Group(),hidden:new Set(),selected:null,segmentMembers:segmentGeometryMembers(manifest.structures),layers:{bone:'off',artery:'off',vein:'on',brain:'off'},clipEnabled:false,clipPlane:new THREE.Plane(),renderer:{extensions:{has:()=>native}},render:()=>{}});for(const x of entries.values())e.root.add(x.mesh);return e;};
const e=fixture(true);e.buildVascularBatches();assert.equal(e.vascularBatches.length,2);e.refreshMaterials();
e.bounds=new THREE.Box3();for(const x of entries.values())e.bounds.union(x.mesh.geometry.boundingBox);
const vb=e.vascularBatches.find(b=>b.userData.system==='vein'),ab=e.vascularBatches.find(b=>b.userData.system==='artery');assert(vb.visible&&!ab.visible);
assert(veins.every(x=>x.batch?.mesh===vb&&vb.getVisibleAt(x.batch.instanceId)));
const saved=veins.map(x=>[x.mesh.geometry.getAttribute('position').array.slice(),x.mesh.geometry.index.array.slice()]);
// Real scene ray tests, including the detached pick proxies used by batching.
let picked=0;const rc=new THREE.Raycaster();
for(const x of veins){
 const g=x.mesh.geometry,a=g.getAttribute('position'),ix=g.index.array;let ok=false;
 for(let j=0;j<ix.length&&!ok;j+=Math.max(3,Math.floor(ix.length/80/3)*3)){
  if(j+2>=ix.length)break;const pa=new THREE.Vector3().fromBufferAttribute(a,ix[j]),pb=new THREE.Vector3().fromBufferAttribute(a,ix[j+1]),pc=new THREE.Vector3().fromBufferAttribute(a,ix[j+2]);
  const n=pb.clone().sub(pa).cross(pc.clone().sub(pa)).normalize(),c=pa.add(pb).add(pc).divideScalar(3);
  rc.set(c.clone().addScaledVector(n,.08),n.negate());rc.far=.2;const hit=pickAnatomy(rc,[...entries.values()],e.layers,null);ok=hit?.object===x.mesh;
 }
 assert(ok,`Could not pick ${x.structure.id}`);picked++;
}
e.setSelected('vein.galen');const galen=entries.get('vein.galen');assert(galen.mesh.parent===e.root&&!vb.getVisibleAt(galen.batch.instanceId));assert.equal(galen.mesh.material.color.getHex(),0xf2b84b);
e.setLayers({bone:'off',artery:'on',vein:'off',brain:'off'});assert(!vb.visible&&ab.visible);assert(veins.every(x=>!x.mesh.visible));
e.setLayers({bone:'off',artery:'off',vein:'ghost',brain:'off'});assert(!vb.visible&&!ab.visible);assert(veins.every(x=>x.mesh.parent===e.root&&x.mesh.visible&&x.mesh.material.transparent));
e.setSelected(null);e.setLayers({bone:'off',artery:'off',vein:'on',brain:'off'});
const subtrees=geometrySubtrees(byId),hidden=new Set(subtrees.get('vein.galen'));assert(hidden.size>=15);e.setHiddenIds(hidden);assert([...hidden].every(id=>!entries.get(id).mesh.visible));assert(entries.get('vein.internal_jugular.right').mesh.visible);
e.setHiddenIds(new Set(subtrees.get('vein')));assert(veins.every(x=>!vb.getVisibleAt(x.batch.instanceId)));e.setHiddenIds(new Set());
e.setClip(true,'sagittal',0);assert(vb.material.clippingPlanes.length===1);e.setClip(false,'sagittal',0);assert(vb.material.clippingPlanes.length===0);
e.setLayers({bone:'ghost',artery:'on',vein:'on',brain:'off'});
const original=new Map([...entries].map(([id,x])=>[id,[x.mesh.material.opacity,x.mesh.visible]]));
e.setFocus('vein.galen');
for(const id of ['vein.galen','vein.internal_cerebral.right','vein.basal.left'])assert.equal(entries.get(id).mesh.material.opacity,1);
assert(entries.get('vein.thalamostriate.left').mesh.material.opacity<1);assert(entries.get('vein.internal_jugular.right').mesh.material.opacity<1);
e.setHiddenIds(new Set(['vein.basal.left']));assert(!entries.get('vein.basal.left').mesh.visible);e.setHiddenIds(new Set());
e.setFocus(null);for(const [id,x] of entries)assert.deepEqual([x.mesh.material.opacity,x.mesh.visible],original.get(id));
const eca=manifest.structures.find(s=>s.name==='External carotid artery left');e.setFocus(eca.id);
assert.equal(entries.get(eca.children[0]).mesh.material.opacity,1);
const facial=manifest.structures.find(s=>s.name==='Facial artery left');assert.equal(entries.get(facial.id).mesh.material.opacity,1);assert(entries.get(facial.children[0]).mesh.material.opacity<1);
e.setLayers({bone:'off',artery:'off',vein:'ghost',brain:'off'});e.setFocus('vein.galen');
const basal=entries.get('vein.basal.left');assert.equal(basal.mesh.material.opacity,1);assert(basal.mesh.parent===e.root&&basal.mesh.visible&&!vb.visible);
e.setFocus(null);e.setLayers({bone:'off',artery:'off',vein:'on',brain:'off'});
for(let i=0;i<veins.length;i++){assert.deepEqual(veins[i].mesh.geometry.getAttribute('position').array,saved[i][0]);assert.deepEqual(veins[i].mesh.geometry.index.array,saved[i][1]);}
for(const q of ['SSS','Galen','Labbe','IJV','SOV'])assert(searchStructures(manifest.structures,q).some(s=>s.system==='vein'),q);
// Per-structure states work even when the former system layer is off.
e.setLayers({bone:'ghost',artery:'off',vein:'off',brain:'off'});
const states=new Map(veins.map(x=>[x.structure.id,'on']));
states.set('vein.basal.left','ghost');states.set('vein.internal_jugular.right','off');
e.setVisibility(states);assert(vb.visible&&!ab.visible);
assert.equal(basal.mesh.material.opacity,.16);assert(!entries.get('vein.internal_jugular.right').mesh.visible);
e.setFocus('vein.galen');assert.equal(basal.mesh.material.opacity,1);assert(!entries.get('vein.internal_jugular.right').mesh.visible);
e.setFocus(null);assert.equal(basal.mesh.material.opacity,.16);
// Ghosted bone remains click-through; an individual opaque bone is selectable.
const bone=[...entries.values()].find(x=>x.structure.system==='bone');
const geometry=bone.mesh.geometry,index=geometry.index.array,attribute=geometry.getAttribute('position');
const pa=new THREE.Vector3().fromBufferAttribute(attribute,index[0]),pb=new THREE.Vector3().fromBufferAttribute(attribute,index[1]),pc=new THREE.Vector3().fromBufferAttribute(attribute,index[2]);
const normal=pb.clone().sub(pa).cross(pc.clone().sub(pa)).normalize(),centre=pa.add(pb).add(pc).divideScalar(3);
rc.set(centre.clone().addScaledVector(normal,.08),normal.negate());rc.far=.2;
states.set(bone.structure.id,'ghost');e.setVisibility(states);assert(!pickAnatomy(rc,[bone],e.layers,null,states));
states.set(bone.structure.id,'on');e.setVisibility(states);assert(pickAnatomy(rc,[bone],e.layers,null,states));
// Camera framing retains context and repeated automatic focus cannot stack zoom.
e.camera=new THREE.PerspectiveCamera(35,1,.01,10000);e.camera.position.set(0,-900,200);
e.controls={target:new THREE.Vector3(0,0,50),update(){}};
const startDistance=e.camera.position.distanceTo(e.controls.target);
e.focus('vein.superior_choroidal.right');const gentleDistance=e.camera.position.distanceTo(e.controls.target);
assert(gentleDistance>=startDistance*.8-1e-6);
e.focus('vein.superior_choroidal.right');assert(Math.abs(e.camera.position.distanceTo(e.controls.target)-gentleDistance)<1e-6);
e.focus('vein.anterior_septal.left');assert(e.camera.position.distanceTo(e.controls.target)>=gentleDistance-1e-6);
// Fallback uses the same proxies when native multi-draw is absent.
for(const x of entries.values())delete x.batch;
const fallback=fixture(false);fallback.buildVascularBatches();fallback.refreshMaterials();assert.equal(fallback.vascularBatches.length,0);assert(veins.every(x=>x.mesh.parent===fallback.root&&x.mesh.visible));
fallback.setFocus('vein.galen');assert.equal(entries.get('vein.basal.left').mesh.material.opacity,1);assert(entries.get('vein.internal_jugular.right').mesh.material.opacity<1);fallback.setFocus(null);
fallback.setVisibility(states);assert.equal(basal.mesh.material.opacity,.16);assert(!entries.get('vein.internal_jugular.right').mesh.visible);
// Lightweight translucency reuses geometry and restores the opaque material.
const originalGeometry=basal.mesh.geometry;
states.set(basal.structure.id,'ghost');fallback.setVisibility(states);
const ghostMaterial=basal.mesh.material;
assert(ghostMaterial.isMeshLambertMaterial&&ghostMaterial.forceSinglePass);
assert.equal(ghostMaterial.opacity,.16);
states.set(basal.structure.id,'on');fallback.setVisibility(states);
assert(basal.mesh.material.isMeshStandardMaterial);
assert.equal(basal.mesh.material,basal.opaqueMaterial);
states.set(basal.structure.id,'ghost');fallback.setVisibility(states);
assert.equal(basal.mesh.material,ghostMaterial);
assert.equal(basal.mesh.geometry,originalGeometry);
fallback.bounds=e.bounds;
fallback.setClip(true,'sagittal',0);assert.equal(ghostMaterial.clippingPlanes.length,1);
states.set(basal.structure.id,'on');fallback.setVisibility(states);
assert.equal(basal.mesh.material.clippingPlanes.length,1);
fallback.setClip(false,'sagittal',0);
// Movement resolution falls on standard-DPI screens and returns after settling.
let pixelRatio=1;
const resolutionFixture=Object.create(AnatomyEngine.prototype);
Object.assign(resolutionFixture,{renderer:{getPixelRatio:()=>pixelRatio,setPixelRatio:r=>{pixelRatio=r}},render(){},cameraInteracting:false});
globalThis.devicePixelRatio=1;
assert(resolutionFixture.useMotionResolution());assert.equal(pixelRatio,.75);
resolutionFixture.qualityRestoreAt=performance.now()-1;
resolutionFixture.restoreSettledResolution();assert.equal(pixelRatio,1);
globalThis.devicePixelRatio=2;
resolutionFixture.useMotionResolution();assert.equal(pixelRatio,.75);
resolutionFixture.qualityRestoreAt=performance.now()-1;
resolutionFixture.restoreSettledResolution();assert.equal(pixelRatio,2);
const report={release:manifest.release,loadedParts:entries.size,venousParts:veins.length,venousTriangles:triangles,realRaycastSelections:picked,nativeBatches:2,independentLayers:true,selectionGhostingClippingAndSubtreeHiding:true,geometryUnchangedByBatching:true,nativeAndFallback:true,scope:'Three.js loader/raycaster and engine-method fixtures; not browser/GPU benchmarking'};
report.lightweightGhostMaterialAndSinglePass=true;report.materialCacheAndOriginalGeometryReused=true;report.motionResolutionRestored=true;
report.focusRetainsImmediateBranchesAndRestoresLayers=true;
report.perStructureThreeStateVisibility=true;report.individualGhostBoneClickThrough=true;report.gentleFocusAndNoRepeatedZoom=true;
fs.writeFileSync(`docs/validation/venous-viewer-v${manifest.release}.json`,JSON.stringify(report,null,2)+'\n');console.log(report);
