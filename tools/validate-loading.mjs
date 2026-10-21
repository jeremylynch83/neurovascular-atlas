import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
import {createServer} from 'vite';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import * as THREE from 'three';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
const root=path.resolve(import.meta.dirname,'..'),base=root+'/public/anatomy/';
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const report={release:manifest.release,checks:[],measurements:{},limitations:['Node decoding excludes network, worker transfer, GPU upload and browser rendering. Browser timings must be measured on a WebGL-capable device.']};
const server=await createServer({root,server:{middlewareMode:true},appType:'custom'});
try {
 const {StagedLoader,loadingAssets}=await server.ssrLoadModule('/src/stagedLoading.ts');
 const assets=loadingAssets(manifest),critical=assets.filter(a=>a.critical);
 assert.equal(critical.length,1);
 assert(critical[0].structures.every(s=>s.system==='bone'));
 const firstArteries=assets.find(a=>a.order===1);
 assert(firstArteries.structures.some(s=>s.id==='artery.posterior.basilar'));
 assert.equal(assets[0].file,'models/craniofacial.glb');
 assert.equal(firstArteries.structures.filter(s=>/internal_carotid.*segment/.test(s.id)).length,14);
 assert.equal(firstArteries.structures.filter(s=>/vertebral.*segment/.test(s.id)).length,8);
 const all=assets.flatMap(a=>a.structures.map(s=>s.id));
 assert.equal(all.length,new Set(all).size);
 assert.equal(all.length,manifest.structures.filter(s=>s.asset).length);
 assert.deepEqual(assets.map(a=>a.order),assets.map(a=>a.order).sort((a,b)=>a-b));
 report.checks.push('Every geometry structure assigned exactly once; skull first, then complete bilateral ICA/vertebral segments and Circle of Willis; fixed skull, arterial, venous, brain order');
 const calls=[],slots=[],installed=new Set();let rejectOnce=null,loader;
 const source={async load(file){calls.push(file);if(file===rejectOnce){rejectOnce=null;throw Error('simulated download failure')}},async prepare(rows){return rows.slice(0,3).map(s=>({id:s.id}))},async release(){},dispose(){}};
 loader=new StagedLoader(manifest,source,async(meshes,background)=>{for(const m of meshes){assert(!installed.has(m.id));installed.add(m.id)}},async bg=>slots.push(bg),()=>{});
 await loader.loadCritical();
 assert.deepEqual(calls,critical.map(a=>a.file));assert.equal(installed.size,critical[0].structures.length);
 assert([...loader.states].some(([,s])=>s.status==='pending'));
 const last=assets.at(-1).structures.at(-1).id;
 let selectedReady=false;const selected=loader.ensure([last]).then(()=>selectedReady=true);
 // Requesting the last structure must not advance it in the download queue.
 rejectOnce=assets[2].file;loader.startBackground();
 await selected;
 assert(selectedReady);assert.deepEqual(calls,assets.map(a=>a.file));
 assert(slots.includes(false)&&slots.includes(true));
 const failed=assets[2].structures.map(s=>s.id);
 assert(failed.every(id=>loader.states.get(id).status==='error'));
 await loader.ensure(failed);
 assert(failed.every(id=>loader.states.get(id).status==='ready'));
 assert.equal(installed.size,all.length);loader.dispose();
 await assert.rejects(loader.ensure([last]),/closed/);
 const bad=new StagedLoader(manifest,{...source,async load(){throw Error('starter failed')}},async()=>{},async()=>{},()=>{});
 await assert.rejects(bad.loadCritical(),/starter failed/);bad.dispose();
 const stopped=new StagedLoader(manifest,source,async()=>{},async()=>{},()=>{});
 const pending=stopped.ensure([last]);stopped.dispose();await assert.rejects(pending,/closed/);
 report.checks.push('Actual loader: skull-only readiness; selection does not reorder; bounded packets; complete background loading; failure/retry; initial skull failure; disposal and pending waiters');
 const {AnatomyEngine,pickAnatomy}=await server.ssrLoadModule('/src/engine.ts');
 const engine=Object.create(AnatomyEngine.prototype);
 Object.assign(engine,{manifest,entries:new Map(),objectToId:new Map(),root:new THREE.Group(),bounds:new THREE.Box3(),primaryPrepared:true,vascularBatches:[],renderer:{extensions:{has:()=>false}},camera:new THREE.PerspectiveCamera(),controls:{target:new THREE.Vector3(2,3,4)},landmarkMarker:new THREE.Group(),selected:null,hidden:new Set(),visibility:new Map(),layers:{artery:'on',bone:'ghost',vein:'off',brain:'off'},focusedMembers:null,injectionPick:null,selectionHalo:{setMeshes(){},setFade(){},setClip(){}},reducedMotion:{matches:false},clipEnabled:true,clipPlane:new THREE.Plane(new THREE.Vector3(1,0,0),0),segmentMembers:new Map(),render(){}});
 const rows=['artery','bone','vein','brain'].map(system=>manifest.structures.find(s=>s.asset&&s.system===system));
 engine.visibility.set(rows[2].id,'on');
 engine.camera.position.set(8,9,10);const position=engine.camera.position.clone(),target=engine.controls.target.clone();
 const packets=rows.map(s=>({id:s.id,positions:new Float32Array([0,0,0,1,0,0,0,1,0]),normals:new Float32Array([0,0,1,0,0,1,0,0,1]),indices:new Uint32Array([0,1,2]),bounds:[[0,0,0],[1,1,0]],sphere:{centre:[.5,.5,0],radius:1}}));
 for(const packet of packets)engine.installMeshes([packet]);
 assert.deepEqual(engine.camera.position,position);assert.deepEqual(engine.controls.target,target);
 assert(rows.slice(0,3).every(s=>engine.entries.get(s.id).mesh.visible));
 assert.equal(engine.entries.get(rows[3].id).mesh.visible,false);
 assert(engine.entries.get(rows[1].id).mesh.material.opacity<1);
 assert(engine.entries.get(rows[0].id).mesh.material.clippingPlanes.includes(engine.clipPlane));
 engine.setVisibility(new Map([[rows[3].id,'on']]));assert(engine.entries.get(rows[3].id).mesh.visible);
 engine.setHiddenIds(new Set([rows[0].id]));assert.equal(engine.entries.get(rows[0].id).mesh.visible,false);
 engine.setHiddenIds(new Set());
 const entry=engine.entries.get(rows[0].id);engine.root.updateMatrixWorld(true);
 const ray=new THREE.Raycaster(new THREE.Vector3(.2,.2,1),new THREE.Vector3(0,0,-1));
 assert.equal(pickAnatomy(ray,[entry],engine.layers,null)?.object,entry.mesh);
 assert.equal(pickAnatomy(ray,[engine.entries.get(rows[1].id)],engine.layers,null),undefined);
 engine.installMeshes(packets);assert.equal(engine.entries.size,4);
 for(const e of engine.entries.values()){e.mesh.geometry.dispose();e.opaqueMaterial.dispose();e.ghostMaterial?.dispose()}
 // Cross-packet batching must retain visibility of earlier vessels.
 const arteryRows=manifest.structures.filter(s=>s.asset&&s.system==='artery').slice(0,3);
 Object.assign(engine,{entries:new Map(),objectToId:new Map(),root:new THREE.Group(),bounds:new THREE.Box3(),vascularBatches:[],selected:null,visibility:new Map(),hidden:new Set(),renderer:{extensions:{has:()=>true}}});
 const vascularPacket=(row)=>({...packets[0],id:row.id});
 engine.installMeshes([vascularPacket(arteryRows[0])]);
 const batch=engine.entries.get(arteryRows[0].id).batch.mesh;
 const vertexStorage=batch.geometry.getAttribute('position').array,indexStorage=batch.geometry.index.array;
 engine.setVisibility(new Map([[arteryRows[1].id,'off']]));
 engine.installMeshes([vascularPacket(arteryRows[1])]);
 assert.equal(engine.vascularBatches.length,1);assert(batch.visible,'New hidden vessel must not hide previous vessels');
 assert.equal(batch.geometry.getAttribute('position').array,vertexStorage);assert.equal(batch.geometry.index.array,indexStorage);
 engine.selected=arteryRows[0].id;engine.segmentMembers=new Map([[engine.selected,new Set([engine.selected])]]);engine.refreshMaterials();
 assert.equal(batch.visible,false);assert.equal(engine.entries.get(engine.selected).mesh.parent,engine.root);
 engine.setVisibility(new Map([[arteryRows[1].id,'on']]));assert(batch.visible);
 engine.selected=null;engine.refreshMaterials();
 engine.installMeshes([vascularPacket(arteryRows[2])]);assert.equal(engine.vascularBatches.length,1);
 assert.equal(batch.userData.visibleInstances.size,3);
 assert.deepEqual(engine.camera.position,position);assert.deepEqual(engine.controls.target,target);
 for(const e of engine.entries.values()){e.mesh.geometry.dispose();e.opaqueMaterial.dispose();e.ghostMaterial?.dispose()}
 batch.dispose();batch.material.dispose();
 report.checks.push('Actual BatchedMesh append path: multiple packets share fixed buffers; hidden arrival does not hide previous vessels; selection unbatches and restores correctly; camera remains unchanged');
 report.checks.push('Actual engine installation/material/picking methods: arrival leaves camera and target unchanged; existing layer defaults, preselected visibility, clipping, hiding, duplicate protection and ghost-bone picking preserved (CPU scene fixture, no GPU)');
 const decoder=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
 async function load(file){const b=fs.readFileSync(base+file);const start=performance.now();const g=await decoder.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);return {g,ms:performance.now()-start,bytes:b.length}}
 function geometries(g){const rows=new Map();g.scene.traverse(o=>{if(!o.isMesh)return;const association=g.parser.associations.get(o);const name=g.parser.json.nodes[association.nodes]?.name;rows.set(name,o)});return rows}
 function release(g){g.scene.traverse(o=>{o.geometry?.dispose();if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])m.dispose()})}
 const originals=new Map();let oldMs=0,oldInitialMs=0,oldInitialBytes=0,initialMs=0;
 for(const file of Object.keys(manifest.assetRevisions).filter(f=>f.startsWith('models/'))){
  const {g,ms,bytes}=await load(file);oldMs+=ms;if(critical.some(a=>a.file===file))initialMs+=ms;
  if(manifest.structures.some(s=>s.asset?.file===file&&['artery','bone'].includes(s.system))){oldInitialMs+=ms;oldInitialBytes+=bytes}
  if(file==='models/craniofacial.glb'){const box=new THREE.Box3();for(const [name,mesh] of geometries(g))if(name!=='bone.hyoid')box.expandByObject(mesh);assert.deepEqual(box.min.toArray(),manifest.startupBounds[0]);assert.deepEqual(box.max.toArray(),manifest.startupBounds[1]);}
  if(manifest.structures.some(s=>s.asset?.file===file&&s.system==='artery'))originals.set(file,{g,rows:geometries(g)});else release(g);
 }
 let compared=0,packMs=0,packBytes=0;
 for(const a of assets.filter(a=>a.file.startsWith('packs/'))){
  const {g,ms,bytes}=await load(a.file);packMs+=ms;packBytes+=bytes;
  assert.equal(hash(fs.readFileSync(base+a.file)).slice(0,20),manifest.assetRevisions[a.file]);
  const rows=geometries(g);assert.equal(rows.size,a.structures.length);
  for(const s of a.structures){
   const o=originals.get(s.asset.file).rows.get(s.asset.node),p=rows.get(s.asset.node);assert(o&&p,s.id);
   assert.deepEqual(o.matrixWorld.elements,p.matrixWorld.elements,s.id+' transform');
   assert.deepEqual(Object.keys(o.geometry.attributes).sort(),Object.keys(p.geometry.attributes).sort());
   for(const name of Object.keys(o.geometry.attributes)){
    const x=o.geometry.attributes[name],y=p.geometry.attributes[name];assert.equal(x.count,y.count,s.id);assert.equal(x.itemSize,y.itemSize,s.id);
    for(let i=0;i<x.count;i++)for(let k=0;k<x.itemSize;k++)assert.equal(x.getComponent(i,k),y.getComponent(i,k),s.id+' '+name);
   }
   assert.deepEqual(o.geometry.index?.array,p.geometry.index?.array,s.id+' triangles');compared++;
  }
  release(g);
 }
 for(const {g} of originals.values())release(g);
 report.checks.push(`Decoded positions, normals, all other attributes, triangles and world transforms exactly match for all ${compared} packed arterial meshes`);
 const sourceArteryBytes=[...originals.keys()].reduce((n,f)=>n+fs.statSync(base+f).size,0);
 report.measurements={singleControlledNodeRun:true,previousInitial:{bytes:oldInitialBytes,decodeMs:oldInitialMs},initialSkull:{bytes:critical.reduce((n,a)=>n+manifest.assetByteSizes[a.file],0),decodeMs:initialMs},previousAll:{decodeMs:oldMs},arteries:{sourceBytes:sourceArteryBytes,packBytes,packDecodeMs:packMs},structureCount:all.length,packCount:manifest.loadingPacks.length};
 fs.writeFileSync(root+'/docs/revision153-loading-validation.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}finally{await server.close()}
