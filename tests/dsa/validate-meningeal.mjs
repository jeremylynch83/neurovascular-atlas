// Use the real run builder with current catalogue/flow; no rendered proxy needed.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {createServer} from 'vite';
const root=path.resolve(import.meta.dirname,'../..'),manifest=JSON.parse(fs.readFileSync(root+'/public/anatomy/manifest.json')),flow=JSON.parse(fs.readFileSync(root+'/public/anatomy/dsa-flow.json'));
const server=await createServer({root,server:{middlewareMode:true},appType:'custom'});
try{
 const {makeDsaRun}=await server.ssrLoadModule('/src/dsa.ts');
 for(const side of ['left','right']){
  const suffix=side==='left'?'.left':'';const channels=['anterior','posterior'].map(p=>`vein.middle_meningeal.${p}.${side}`);
  for(const id of channels){const row=manifest.structures.find(s=>s.id===id);assert.equal(row.parent,`vein.sphenoparietal.${side}`);assert.equal(row.vesselCourse.attachments.outgoing[0].to,row.parent);assert(!manifest.deferredCourseSpecifications.includes(id));}
  const run=makeDsaRun(manifest,'mma',side,flow);const veins=new Map(run.vessels.filter(v=>v.vein).map(v=>[v.id,v]));
  for(const id of channels)assert(veins.has(id),id);assert(veins.has(`vein.sphenoparietal.${side}`));assert(veins.has(`vein.cavernous.${side}`));assert(!veins.has(`vein.pterygoid_plexus.${side}`));
  assert(veins.get(`vein.cavernous.${side}`).delay>veins.get(channels[0]).delay);
  const frontal=`artery.eca.maxillary.mma.frontal.right${suffix}`,row=flow.entries[frontal];const injection={id:frontal,distance:row.length*.4,point:row.points[Math.floor(row.points.length*.4)]};
  const selective=makeDsaRun(manifest,'mma',side,flow,injection);for(const id of channels)assert(selective.vessels.some(v=>v.id===id),`Frontal injection should include paired companion: ${id}`);
  const posterior=manifest.structures.filter(s=>s.system==='artery'&&s.side===side&&/posterior_convexity|petrosquamosal/.test(s.id)&&flow.entries[s.id]?.selectable);
  assert(posterior.length);
  for(const s of posterior){const r=flow.entries[s.id],run=makeDsaRun(manifest,'mma',side,flow,{id:s.id,distance:r.length*.5,point:r.points[Math.floor(r.points.length*.5)]});assert(!run.vessels.some(v=>channels.includes(v.id)),s.id);}
 }
 console.log('Both companion channels, declared lesser-wing drainage and downstream timing pass bilaterally. Selective frontal injections retain the pair; posterior-division injections do not reuse frontal channels.');
}finally{await server.close()}
