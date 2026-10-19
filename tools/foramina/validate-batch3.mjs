import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {downstreamFlow,decodeCoordinates,splitFlowSurface,closedSurfaceError,pointInsideSurface} from '../../src/flowGeometry.ts';
import {Vector3,Raycaster,DoubleSide} from 'three';
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
  meshes.set(row.id,{p,index:new Uint32Array(o.geometry.index.array)});if(['bone.sphenoid','bone.temporal.right','bone.temporal.left','bone.occipital'].includes(row.id)){o.material.side=DoubleSide;bones.push(o);}
  if(row.id==='bone.sphenoid'){sphenoid=o;sphenoid.material.side=DoubleSide;}
 });
}
function proxy(id){const orig=meshes.get(id),r=surfaces.entries[id],p=new Float32Array(orig.p.length+r.extra.length*3);p.set(orig.p);r.extra.forEach((v,i)=>p.set(v,orig.p.length+i*3));const f=[],removed=new Set(r.removed),flips=new Set(r.flips);for(let i=0;i<orig.index.length/3;i++)if(!removed.has(i)){const [a,b,c]=orig.index.subarray(i*3,i*3+3);f.push(...(r.reverse!==flips.has(i)?[a,c,b]:[a,b,c]));}f.push(...r.caps);return {p,index:new Uint32Array(f)};}
function welded(s){const map=new Map(),p=[],remap=[];for(let i=0;i<s.p.length;i+=3){const q=Array.from(s.p.subarray(i,i+3)),key=q.join(',');if(!map.has(key)){map.set(key,p.length/3);p.push(...q)}remap.push(map.get(key));}return {positions:new Float32Array(p),indices:new Uint32Array(Array.from(s.index,i=>remap[i]))};}
const report={release:manifest.release,passages:[],flows:[],closedSplitSections:0};
const ids=Object.keys(JSON.parse(fs.readFileSync(app+'/anatomy/source/foramina/posterior-changes.json'))).filter(id=>flow.entries[id]);
for(const id of ids){
 const r=flow.entries[id],surface=proxy(id);assert(r&&r.selectable,id+' not selectable');assert(r.safeRanges.length===1&&r.safeRanges[0][0]===0&&Math.abs(r.safeRanges[0][1]-r.length)<1e-5,id+' incomplete safe range');assert.equal(closedSurfaceError(welded(surface)),0,id+' projection not closed');assert(r.points.every(p=>pointInsideSurface(surface.p,surface.index,p)),id+' course outside vessel');
 for(const fraction of [0,.25,.75]){const sections=splitFlowSurface(surface.p,surface.index,decodeCoordinates(r,surface.p),r.length,r.length*fraction);assert(sections.length);for(const section of sections)assert.equal(closedSurfaceError(section),0,id+' open injection split');report.closedSplitSections+=sections.length;}
 if(id.includes('tympanic')||id.includes('petrosal')){const side=id.endsWith('left')||id.includes('_left')?'left':'right';assert(downstreamFlow(flow,[{id:`artery.anterior.internal_carotid_${side}.segment.petrous`,distance:0}],new Set(Object.keys(flow.entries))).has('artery.anterior.caroticotympanic_'+side),'caroticotympanic lacks ICA inflow');}
 report.flows.push({id,selectable:true,lengthMm:r.length});
}
const ray=new Raycaster();function clear(a,b){const aa=new Vector3(...a),bb=new Vector3(...b),d=bb.clone().sub(aa);if(d.length()<1e-6)return true;ray.set(aa,d.clone().normalize());ray.near=1e-5;ray.far=d.length()-1e-5;return ray.intersectObjects(bones,false).length===0;}
for(const side of ['right','left']){
 for(const family of ['internal-acoustic','facial-canal','stylomastoid','jugular-foramen','hypoglossal','petrotympanic']){const id=`landmark.${family}.${side}`,lm=rows.get(id).landmark;assert.equal(lm.status,'visible');for(let i=1;i<lm.course.length;i++)assert(clear(lm.course[i-1],lm.course[i]),id+' blocked centreline');report.passages.push({id,clear:true});}
}
for(const [file,hash] of Object.entries(flow.sourceHashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(base+file)).digest('hex'),hash,file+' stale DSA hash');
fs.writeFileSync(app+'/docs/foramina-batch3-dsa-validation.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
