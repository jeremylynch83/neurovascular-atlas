// Differential geometry checks and paired timings against the v0.9.79 splitter.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {CylinderGeometry} from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {decodeCoordinates,prepareFlowSurface,splitFlowSurface,closedSurfaceError} from '../../src/flowGeometry.ts';
import {splitFlowSurface as reference} from './reference-splitter.ts';

const root=path.resolve(import.meta.dirname,'../..'),base=root+'/public/anatomy/';
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json'));
const flow=JSON.parse(fs.readFileSync(base+'dsa-flow.json'));
const surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json'));
const only=process.argv.includes('--selected');
const bytes=a=>Buffer.from(a.buffer,a.byteOffset,a.byteLength);
let cases=0,sections=0,rejectedCases=0,closedSections=0;
const timings={referenceMs:0,optimisedMs:0,prepareMs:0};
const compare=(p,index,coordinate,length,inlet,prepared,id,step=18,checkClosed=true)=>{
  let original,current,oldMs,newMs,start,oldError,newError;
  const old=()=>{start=performance.now();try{original=reference(p,index,coordinate,length,inlet,step)}catch(e){oldError=e.message}oldMs=performance.now()-start};
  const next=()=>{start=performance.now();try{current=splitFlowSurface(p,index,coordinate,length,inlet,step,prepared)}catch(e){newError=e.message}newMs=performance.now()-start};
  if(cases%2){next();old()}else{old();next()}
  assert.equal(newError,oldError,`${id} @ ${inlet}`);
  if(oldError){assert(!checkClosed,`${id} @ ${inlet}: ${oldError}`);cases++;rejectedCases++;return {referenceMs:oldMs,optimisedMs:newMs}}
  assert.equal(current.length,original.length,id);
  current.forEach((s,i)=>{
    assert.equal(s.start,original[i].start,id);assert.equal(s.end,original[i].end,id);
    assert(bytes(s.positions).equals(bytes(original[i].positions)),`Positions differ: ${id} @ ${inlet}`);
    assert(bytes(s.indices).equals(bytes(original[i].indices)),`Indices differ: ${id} @ ${inlet}`);
    const closure=closedSurfaceError(s);assert.equal(closure,closedSurfaceError(original[i]),id);
    if(closure===0)closedSections++;
    if(checkClosed)assert.equal(closure,0,`Open section: ${id} @ ${inlet}`);
  });
  cases++;sections+=current.length;
  return {referenceMs:oldMs,optimisedMs:newMs};
};

// Coincident vertices, exact boundaries, fractional cuts, terminal cuts and
// triangles spanning multiple sections. Also exercise the uncached API.
const cylinder=new CylinderGeometry(1,1,72,8,4),position=new Float32Array(cylinder.attributes.position.array),index=new Uint32Array(cylinder.index.array);
for(let i=0;i<position.length;i++)if(Math.abs(position[i])<1e-6)position[i]=0;
const coordinate=Float32Array.from({length:position.length/3},(_,i)=>position[i*3+1]+36),prepared=prepareFlowSurface(position,index,coordinate);
for(const inlet of [0,1e-8,18,18-1e-7,18+1e-7,35.5,54,71.998,72])for(const step of [18,7.3,80])compare(position,index,coordinate,72,inlet,prepared,'boundary cylinder',step,false);
compare(position,index,coordinate,72,18,undefined,'uncached cylinder',18,false);
compare(position,index,coordinate,50,0,prepared,'coordinates past declared length',18,false);
cylinder.dispose();

const measurements=[],loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const selected=id=>/internal_carotid_left.segment.cervical|carotid.external.right.left|eca.maxillary.right.left$|posterior.pca_p[123](?:_p3)?_left/.test(id);
let vessels=0;
for(const file of Object.keys(flow.sourceHashes)){
  if(!manifest.structures.some(s=>s.asset?.file===file&&flow.entries[s.id]))continue;
  const data=fs.readFileSync(base+file),gltf=await loader.parseAsync(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),'');
  gltf.scene.traverse(o=>{
    if(!o.isMesh)return;
    const node=gltf.parser.json.nodes[gltf.parser.associations.get(o).nodes].name;
    const structure=manifest.structures.find(s=>s.asset?.file===file&&s.asset.node===node),id=structure?.id,row=flow.entries[id];
    if(!row?.selectable)return;
    if(only&&!selected(id))return;
    const recipe=surfaces.entries[id],original=o.geometry.attributes.position,p=new Float32Array((original.count+recipe.extra.length)*3);
    for(let i=0;i<original.count;i++)p.set([original.getX(i),original.getY(i),original.getZ(i)],i*3);
    recipe.extra.forEach((v,i)=>p.set(v,(original.count+i)*3));
    const removed=new Set(recipe.removed),flips=new Set(recipe.flips),source=o.geometry.index.array,faces=[];
    for(let i=0;i<source.length/3;i++)if(!removed.has(i)){const a=source[i*3],b=source[i*3+1],c=source[i*3+2];faces.push(...(recipe.reverse!==flips.has(i)?[a,c,b]:[a,b,c]))}
    faces.push(...recipe.caps);
    const index=new Uint32Array(faces),coordinate=decodeCoordinates(row,p),start=performance.now(),prepared=prepareFlowSurface(p,index,coordinate),prepareMs=performance.now()-start;
    timings.prepareMs+=prepareMs;
    for(const inlet of [0,row.length*.37]){
      const paired=compare(p,index,coordinate,row.length,inlet,prepared,id);
      timings.referenceMs+=paired.referenceMs;timings.optimisedMs+=paired.optimisedMs;
    }
    if(selected(id)){
      const cuts=[.01,.2,.5,.99].map(u=>row.length*u);
      for(const [a,b] of row.safeRanges)cuts.push(a,b);
      for(const inlet of cuts)compare(p,index,coordinate,row.length,inlet,prepared,id,18,false);
      measurements.push({id,prepareMs,triangles:index.length/3});
    }
    vessels++;
  });
  gltf.scene.traverse(o=>{if(o.isMesh)o.geometry.dispose()});
  console.log(`Checked ${file}: ${vessels} courses, ${cases} cases.`);
}
assert.equal(vessels,only?5:578);
const report={release:JSON.parse(fs.readFileSync(root+'/package.json')).version,vessels,cases,sections,byteIdentical:true,closedSections,rejectedCases,closureAndErrorBehaviourIdentical:true,timings,measurements,passed:true};
console.log(JSON.stringify(report));
if(process.env.DSA_SPLITTER_REPORT)fs.writeFileSync(process.env.DSA_SPLITTER_REPORT,JSON.stringify(report,null,2));
