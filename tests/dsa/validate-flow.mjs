// Geometry, branch ordering and partial-injection invariants against real assets.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {flowGraphSource,downstreamFlow,decodeCoordinates,splitFlowSurface,closedSurfaceError,pointInsideSurface,pathPoint,injectionOnPath} from '../../src/flowGeometry.ts';
import {authoredCourseSource} from '../../tools/dsa-course-guides.mjs';
const root=path.resolve(import.meta.dirname,'../..'),base=root+'/public/anatomy/';
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json'));
const flow=JSON.parse(fs.readFileSync(base+'dsa-flow.json'));
const surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json'));
const hash=v=>crypto.createHash('sha256').update(v).digest('hex');
assert.equal(flow.schema,1);assert.equal(flow.graphSource,flowGraphSource(manifest));assert.equal(flow.graphHash,hash(flow.graphSource));
assert.equal(flow.generatorHash,hash(fs.readFileSync(root+'/tools/build-dsa-flow.mjs')+fs.readFileSync(root+'/src/flowGeometry.ts')+fs.readFileSync(root+'/tools/dsa-course-guides.mjs')+authoredCourseSource(manifest)));
const allowed=new Set(Object.keys(flow.entries));let selectable=0,sections=0;
for(const [id,row] of Object.entries(flow.entries)) {
 assert(row.points.length===row.arc.length&&row.points.length>=2);assert.equal(row.arc[0],0);assert.equal(row.arc.at(-1),row.length);
 assert(row.arc.every((v,i)=>Number.isFinite(v)&&(!i||v>=row.arc[i-1])));assert(row.points.flat().every(Number.isFinite));
 assert.equal(Buffer.from(row.coordinates,'base64').length,row.vertexCount*2);
 for(const e of flow.edges[id]??[]){assert(allowed.has(e.to));assert(e.at>=0&&e.at<=row.length+1e-5);}
 if(row.selectable){selectable++;assert(row.safeRanges.length);assert(row.safeRanges.every(([a,b])=>a>=0&&b<=row.length&&b>a));}
}
for(const side of ['left','right']) {
 for(const stem of ['mma_paramedian','mma_falcine_terminal'])assert(flow.entries[`artery.amendment.${stem}.${side}`]?.selectable,'Repaired MMA injection course must remain selectable');
 const suffix=side==='left'?'.left':'';
 for(const id of [`artery.anterior.internal_carotid_${side}.segment.cervical`,`artery.carotid.external.right${suffix}`,`artery.eca.maxillary.right${suffix}`,`artery.eca.maxillary.mma.right${suffix}`,`artery.posterior.vertebral_${side}.segment.v1`])assert(flow.entries[id]?.selectable,'Required injection course: '+id);
 const max=`artery.eca.maxillary.right${suffix}`,mma=`artery.eca.maxillary.mma.right${suffix}`,branch=flow.edges[max].find(e=>e.to===mma);
 assert(branch&&branch.at>0&&branch.at<flow.entries[max].length);
 assert(downstreamFlow(flow,[{id:max,distance:branch.at-1}],allowed).has(mma));
 assert(!downstreamFlow(flow,[{id:max,distance:branch.at+1}],allowed).has(mma));
 const va=`artery.posterior.vertebral_${side}.segment.v4`,other=`artery.posterior.vertebral_${side==='left'?'right':'left'}.segment.v4`;
 const posterior=downstreamFlow(flow,[{id:va,distance:flow.entries[va].length*.5}],allowed);
 assert(posterior.has('artery.posterior.basilar'));assert(posterior.has('artery.posterior.pca_p1_left'));assert(posterior.has('artery.posterior.pca_p1_right'));assert(!posterior.has(other));
 const source=`artery.anterior.internal_carotid_${side}.segment.terminus`,cervical=`artery.anterior.internal_carotid_${side}.segment.cervical`;
 assert(!downstreamFlow(flow,[{id:source,distance:flow.entries[source].length*.25}],allowed).has(cervical));
}
const both=downstreamFlow(flow,['left','right'].map(side=>({id:`artery.posterior.vertebral_${side}.segment.v1`,distance:0})),allowed);
assert(both.has('artery.posterior.basilar'));assert.equal([...both.keys()].filter(id=>id==='artery.posterior.basilar').length,1);
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
for(const [file,expected] of Object.entries(flow.sourceHashes)) {
 const bytes=fs.readFileSync(base+file);assert.equal(hash(bytes),expected);assert.equal(surfaces.sourceHashes[file],expected);
 if(!manifest.structures.some(s=>s.asset?.file===file&&flow.entries[s.id]))continue;
 const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 gltf.scene.traverse(o=>{
  if(!o.isMesh)return;
  const name=gltf.parser.json.nodes[gltf.parser.associations.get(o).nodes].name;
  const structure=manifest.structures.find(s=>s.asset?.file===file&&s.asset.node===name),row=flow.entries[structure?.id];if(!row?.selectable)return;
  const recipe=surfaces.entries[structure.id],original=o.geometry.attributes.position;assert.equal(original.count,row.vertexCount);
  const p=new Float32Array((original.count+recipe.extra.length)*3);
  for(let i=0;i<original.count;i++)p.set([original.getX(i),original.getY(i),original.getZ(i)],i*3);
  recipe.extra.forEach((v,i)=>p.set(v,(original.count+i)*3));
  const removed=new Set(recipe.removed),flips=new Set(recipe.flips),source=o.geometry.index.array,faces=[];
  for(let i=0;i<source.length/3;i++)if(!removed.has(i)){const a=source[i*3],b=source[i*3+1],c=source[i*3+2];faces.push(...(recipe.reverse!==flips.has(i)?[a,c,b]:[a,b,c]));}
  faces.push(...recipe.caps);const index=new Uint32Array(faces),coordinates=decodeCoordinates(row,p);
  for(const inlet of [0,row.length*.37])for(const section of splitFlowSurface(p,index,coordinates,row.length,inlet)){assert.equal(closedSurfaceError(section),0,structure.id);sections++;}
  // Sample permitted course ranges, including points near either end.
  for(const [a,b] of row.safeRanges)for(const u of [.01,.5,.99])assert(pointInsideSurface(p,index,pathPoint(row,a+(b-a)*u)),`Catheter outside ${structure.id}`);
  for(let i=1;i<row.safeRanges.length;i++){
   const gap=(row.safeRanges[i-1][1]+row.safeRanges[i][0])/2,tip=injectionOnPath(row,pathPoint(row,gap));
   assert(row.safeRanges.some(([a,b])=>tip.distance>=a&&tip.distance<=b));assert(pointInsideSurface(p,index,tip.point));
  }
 });
 gltf.scene.traverse(o=>{if(o.isMesh)o.geometry.dispose()});
}
assert.equal(Object.keys(flow.entries).length,597);assert(selectable>500);
console.log(`Validated ${selectable} selectable arterial courses, ${sections} closed sections and directed injection routes. Geometry and generator hashes match.`);
