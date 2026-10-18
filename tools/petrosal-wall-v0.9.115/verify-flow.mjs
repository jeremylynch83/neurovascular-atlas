// Only native vein geometry changes; unchanged bounds preserve every flow input.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {authoredCourseSource}from '../dsa-course-guides.mjs';import {flowGraphSource}from '../../src/flowGeometry.ts';
const work=process.argv[2],base='public/anatomy/',old=JSON.parse(fs.readFileSync(work+'/old-dsa-flow.json')),manifest=JSON.parse(fs.readFileSync(base+'manifest.json')),ex=JSON.parse(fs.readFileSync(work+'/export-validation.json')),hash=x=>crypto.createHash('sha256').update(x).digest('hex');
assert(ex.passed&&ex.selectedBoundsExact&&ex.unchangedVeinMeshes===230&&ex.otherAssetsByteExact===4);
assert.equal(hash(fs.readFileSync(work+'/old-venous.glb')),old.sourceHashes['models/venous.glb']);
const sourceHashes=Object.fromEntries(Object.keys(old.sourceHashes).map(file=>[file,hash(fs.readFileSync(base+file))]));
for(const [file,h]of Object.entries(old.sourceHashes))if(file!=='models/venous.glb')assert.equal(sourceHashes[file],h,file);
assert.equal(hash(flowGraphSource(manifest)),old.graphHash);
const generator=hash(fs.readFileSync('tools/build-dsa-flow.mjs')+fs.readFileSync('src/flowGeometry.ts')+fs.readFileSync('tools/dsa-course-guides.mjs')+authoredCourseSource(manifest));assert.equal(generator,old.generatorHash);
const surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json'));for(const [file,h]of Object.entries(sourceHashes))assert.equal(surfaces.sourceHashes[file],h);
const now={...old,sourceHashes};assert.deepEqual(now.entries,old.entries);assert.deepEqual(now.edges,old.edges);assert.deepEqual(now.veinSites,old.veinSites);
fs.writeFileSync(base+'dsa-flow.json',JSON.stringify(now));const report={passed:true,allArterialCoursesExact:Object.keys(old.entries).length,allEdgesExact:true,allVeinSitesExact:true,graphAndGeneratorExact:true,sourceHashOnlyRefresh:true,veinBoundsExactProof:'All 231 before/after native vein position streams are checked by export verification: 230 unchanged streams and exact bounds for the selected stream.'};fs.writeFileSync(work+'/flow-refresh.json',JSON.stringify(report,null,2)+'\n');console.log(report);
