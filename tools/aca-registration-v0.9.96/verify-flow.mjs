import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {authoredCourseSource} from '../dsa-course-guides.mjs';
const work=process.argv[2],base='public/anatomy/',old=JSON.parse(fs.readFileSync(work+'/old-dsa-flow.json')),now=JSON.parse(fs.readFileSync(base+'dsa-flow.json')),manifest=JSON.parse(fs.readFileSync(base+'manifest.json'));
const selected=new Set(['artery.anterior.aca_pericallosal_right.segment.a5','artery.anterior.precuneal_right','artery.amendment.aca_falcine_branch.right']);let reused=0;
for(const [id,row]of Object.entries(old.entries))if(!selected.has(id)){assert.deepEqual(now.entries[id],row,id);reused++}
assert.deepEqual(now.graphHash,old.graphHash);assert.deepEqual(now.graphSource,old.graphSource);assert.deepEqual(now.veinSites,old.veinSites);
const hash=x=>crypto.createHash('sha256').update(x).digest('hex'),generator=hash(fs.readFileSync('tools/build-dsa-flow.mjs')+fs.readFileSync('src/flowGeometry.ts')+fs.readFileSync('tools/dsa-course-guides.mjs')+authoredCourseSource(manifest));assert.equal(generator,old.generatorHash);
const changedEdges=Object.keys(now.edges).filter(k=>JSON.stringify(now.edges[k])!==JSON.stringify(old.edges[k]));
for(const id of selected){assert(now.entries[id]);assert(now.entries[id].selectable,id+' selectable')}
now.generatorHash=generator;fs.writeFileSync(base+'dsa-flow.json',JSON.stringify(now));const report={passed:true,unchangedCoursesReused:reused,repairedCoursesSelectable:true,graphAndVeinSitesUnchanged:true,generatorUnchanged:true,changedEdgeSources:changedEdges};fs.writeFileSync(work+'/flow-refresh.json',JSON.stringify(report,null,2)+'\n');console.log(report)
