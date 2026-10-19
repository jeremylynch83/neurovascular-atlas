// Incremental authoring rebuild, allowed only after exact per-node comparisons.
// Ordinary builds still use tools/build-dsa-flow.mjs and its global cache hashes.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {spawnSync} from 'node:child_process';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {flowGraphSource} from '../../src/flowGeometry.ts';import {authoredCourseSource} from '../dsa-course-guides.mjs';
const app=path.resolve(import.meta.dirname,'../..'),base=app+'/public/anatomy/',hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json')),surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json')),flow=JSON.parse(fs.readFileSync(base+'dsa-flow.json'));
const definition=fs.readFileSync(app+'/tools/build-dsa-flow.mjs')+fs.readFileSync(app+'/src/flowGeometry.ts')+fs.readFileSync(app+'/tools/dsa-course-guides.mjs');
const rows=manifest.structures.filter(s=>s.system==='artery'&&s.asset&&s.displayGroup!=='anastomoses'),signatures={};
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
for(const file of new Set(rows.map(s=>s.asset.file))){const b=fs.readFileSync(base+file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.traverse(o=>{if(!o.isMesh)return;const name=g.parser.json.nodes[g.parser.associations.get(o).nodes].name,s=rows.find(r=>r.asset.file===file&&r.asset.node===name);if(!s)return;const a=o.geometry.attributes.position,p=new Float32Array(a.count*3);for(let i=0;i<a.count;i++)for(let k=0;k<3;k++)p[i*3+k]=a.getComponent(i,k);const index=new Uint32Array(o.geometry.index.array);signatures[s.id]=hash(Buffer.concat([Buffer.from(p.buffer),Buffer.from(index.buffer)]))+':'+hash(JSON.stringify(s.flowCourseGuide??null))+':'+hash(JSON.stringify(surfaces.entries[s.id]??null));});}
const checkpoint=process.argv[3];
if(process.argv[2]==='--snapshot'){
 assert.equal(flow.generatorHash,hash(definition+authoredCourseSource(manifest)),'Snapshot requires current, fully verified flow data');
 for(const [file,h] of Object.entries(flow.sourceHashes))assert.equal(hash(fs.readFileSync(base+file)),h);
 fs.writeFileSync(checkpoint,JSON.stringify({signatures,definitionHash:hash(definition),graphHash:hash(flowGraphSource(manifest)),entries:Object.fromEntries(Object.entries(flow.entries).map(([id,r])=>[id,hash(JSON.stringify(r))]))}));console.log('Recorded exact DSA node signatures',Object.keys(signatures).length);
}else{
 const old=JSON.parse(fs.readFileSync(checkpoint));assert.equal(old.definitionHash,hash(definition));assert.equal(old.graphHash,hash(flowGraphSource(manifest)));assert.deepEqual(Object.keys(old.signatures).sort(),Object.keys(signatures).sort());
 const changed=Object.keys(signatures).filter(id=>old.signatures[id]!==signatures[id]);assert(changed.length>0);
 const run=spawnSync(process.execPath,[app+'/tools/build-dsa-flow.mjs','--force','--only',changed.join(',')],{cwd:app,stdio:'inherit'});assert.equal(run.status,0);
 const next=JSON.parse(fs.readFileSync(base+'dsa-flow.json'));for(const [id,h] of Object.entries(old.entries))if(!changed.includes(id))assert.equal(hash(JSON.stringify(next.entries[id])),h,'Unexpected unchanged course edit '+id);
 next.generatorHash=hash(definition+authoredCourseSource(manifest));next.incrementalVerification={changedCourses:changed,exactUnchangedCourses:Object.keys(old.entries).length-changed.filter(id=>old.entries[id]).length,method:'Exact decoded position/index, guide, surface-entry and graph comparison; unchanged flow entries retained byte-equivalently.'};fs.writeFileSync(base+'dsa-flow.json',JSON.stringify(next));console.log(next.incrementalVerification);
}
