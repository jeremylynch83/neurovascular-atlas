import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {injectionOnPath,downstreamFlow,decodeCoordinates,splitFlowSurface,closedSurfaceError,pointInsideSurface} from '../../src/flowGeometry.ts';
import {Vector3,Triangle,Raycaster,DoubleSide} from 'three';
const app=path.resolve(import.meta.dirname,'../..'),base=app+'/public/anatomy/';
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json')),flow=JSON.parse(fs.readFileSync(base+'dsa-flow.json')),surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json'));
const rows=new Map(manifest.structures.map(s=>[s.id,s])),meshes=new Map();let sphenoid;
const bones=[];const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
for(const file of ['models/craniofacial.glb','models/complete-circulation.glb','models/complete-anastomoses.glb']){
 const b=fs.readFileSync(base+file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
 g.scene.updateMatrixWorld(true);
 g.scene.traverse(o=>{if(!o.isMesh)return;const name=g.parser.json.nodes[g.parser.associations.get(o).nodes].name;
  const row=manifest.structures.find(s=>s.asset?.file===file&&s.asset.node===name);if(!row)return;
  const a=o.geometry.attributes.position,p=new Float32Array(a.count*3);for(let i=0;i<a.count;i++)for(let k=0;k<3;k++)p[i*3+k]=a.getComponent(i,k);
  meshes.set(row.id,{p,index:new Uint32Array(o.geometry.index.array)});if(row.system==='bone'){o.material.side=DoubleSide;bones.push(o);}
  if(row.id==='bone.sphenoid'){sphenoid=o;sphenoid.material.side=DoubleSide;}
 });
}
function proxy(id){const orig=meshes.get(id),r=surfaces.entries[id],p=new Float32Array(orig.p.length+r.extra.length*3);p.set(orig.p);r.extra.forEach((v,i)=>p.set(v,orig.p.length+i*3));const f=[],removed=new Set(r.removed),flips=new Set(r.flips);for(let i=0;i<orig.index.length/3;i++)if(!removed.has(i)){const [a,b,c]=orig.index.subarray(i*3,i*3+3);f.push(...(r.reverse!==flips.has(i)?[a,c,b]:[a,b,c]));}f.push(...r.caps);return {p,index:new Uint32Array(f)};}
function welded(s){const map=new Map(),p=[],remap=[];for(let i=0;i<s.p.length;i+=3){const q=Array.from(s.p.subarray(i,i+3)),key=q.join(',');if(!map.has(key)){map.set(key,p.length/3);p.push(...q)}remap.push(map.get(key));}return {positions:new Float32Array(p),indices:new Uint32Array(Array.from(s.index,i=>remap[i]))};}
const report={release:manifest.release,flows:[],errors:[],closedSplitSections:0};
const selected=new Set(JSON.parse(fs.readFileSync(app+'/anatomy/source/foramina/revision158-flow-changes.json')));const baseline=JSON.parse(fs.readFileSync(app+'/anatomy/source/foramina/revision158-flow-status-baseline.json'));let count=0;
for(const [id,r]of Object.entries(flow.entries).filter(([id])=>selected.has(id))){
 const rec={id,selectable:r.selectable,lengthMm:r.length,safeRanges:r.safeRanges,fullSafe:r.safeRanges?.length===1&&r.safeRanges[0][0]===0&&Math.abs(r.safeRanges[0][1]-r.length)<1e-5};
 try{
  assert(!baseline[id]?.selectable||r.selectable,'Previously selectable course became unavailable');if(baseline[id]?.fullSafe)assert(rec.fullSafe,'Full safe range regressed');
  assert(meshes.has(id)&&surfaces.entries[id],id+' missing actual/proxy surface');const surface=proxy(id);rec.closedProjectionError=closedSurfaceError(welded(surface));assert.equal(rec.closedProjectionError,0,'projection not closed');
  if(r.selectable){
   assert(r.safeRanges.length>0,'selectable without safe range');const range=r.safeRanges.reduce((a,b)=>b[1]-b[0]>a[1]-a[0]?b:a);const distance=(range[0]+range[1])/2;const sections=splitFlowSurface(surface.p,surface.index,decodeCoordinates(r,surface.p),r.length,distance);assert(sections.length,'no split');rec.splitSections=sections.length;rec.openSplitSections=sections.filter(s=>closedSurfaceError(s)!==0).length;report.closedSplitSections+=sections.length-rec.openSplitSections;assert.equal(rec.openSplitSections,0,'open split');
   const indices=[...new Set(Array.from({length:17},(_,i)=>Math.round((r.points.length-1)*i/16)))];rec.sampledOutsideGuideIndices=indices.filter(i=>!pointInsideSurface(surface.p,surface.index,r.points[i]));rec.precisionOnlyEndpointIndices=[];rec.excludedUnsafeGuideIndices=rec.sampledOutsideGuideIndices.filter(i=>!r.safeRanges.some(([a,b])=>r.arc[i]>=a-1e-6&&r.arc[i]<=b+1e-6));
   for(const i of rec.sampledOutsideGuideIndices.filter(i=>!rec.excludedUnsafeGuideIndices.includes(i))){const point=new Vector3(...r.points[i]),tri=new Triangle(),closest=new Vector3();let distance=Infinity;for(let j=0;j<surface.index.length;j+=3){for(let k=0;k<3;k++)tri[['a','b','c'][k]].fromArray(surface.p,surface.index[j+k]*3);tri.closestPointToPoint(point,closest);distance=Math.min(distance,closest.distanceTo(point));}assert(distance<1e-5,'Endpoint outside beyond serialization tolerance');rec.precisionOnlyEndpointIndices.push(i);}
   rec.injectionGateChecked=true;for(const i of indices){const q=injectionOnPath(r,r.points[i]);assert(r.safeRanges.some(([a,b])=>q.distance>=a-1e-6&&q.distance<=b+1e-6),'injection outside declared safe ranges');}
   rec.additionalSections=[];for(const fraction of [.15,.85]){const sections=splitFlowSurface(surface.p,surface.index,decodeCoordinates(r,surface.p),r.length,range[0]+(range[1]-range[0])*fraction);assert(sections.length,'No split at '+fraction);assert(sections.every(s=>closedSurfaceError(s)===0),'Open split at '+fraction);report.closedSplitSections+=sections.length;rec.additionalSections.push({fraction,sections:sections.length});}

  }
 }catch(e){rec.error=String(e.message);report.errors.push({id,error:rec.error});}
 report.flows.push(rec);console.log('Checked',++count,id,rec.error??'passed');
}
fs.writeFileSync(app+'/docs/revision158-flow-validation.json',JSON.stringify(report,null,2));console.log('DSA summary',report.flows.length,'entries',report.errors.length,'structural errors');

assert.equal(report.errors.length,0,JSON.stringify(report.errors));
