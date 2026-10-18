// Authoring check: actual app loader, changed buffers and exact new native joins.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {MeshoptDecoder} from 'meshoptimizer';
const work=path.resolve(process.argv[2]);await MeshoptDecoder.ready;const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function load(file){const b=fs.readFileSync(file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');const out=new Map();g.scene.traverse(o=>{if(o.isMesh)out.set(g.parser.json.nodes[g.parser.associations.get(o).nodes].name,o.geometry)});return out;}
const before=await load(work+'/old-complete-circulation.glb'),after=await load('public/anatomy/models/complete-circulation.glb');assert.equal(before.size,after.size);
const report=JSON.parse(fs.readFileSync(work+'/mma-network-trials.json')),selected=new Set(['MMA paramedian left','MMA falcine terminal left','MMA paramedian right','MMA falcine terminal right']),checks=[];
const key=(p,i)=>[0,1,2].map(k=>p.getComponent(i,k)).join(',');
for(const [name,g]of after){const old=before.get(name);assert(old);const p=g.attributes.position,op=old.attributes.position;
 if(!selected.has(name)){assert.deepEqual(p.array,op.array,name+' positions');assert.deepEqual(g.index.array,old.index.array,name+' indices');assert.deepEqual(g.attributes.normal.array,old.attributes.normal.array,name+' normals');continue;}
 const candidate=fs.readFileSync(work+'/candidate/'+name+'.positions.bin'),indices=fs.readFileSync(work+'/candidate/'+name+'.indices.bin');assert.equal(p.count*12,candidate.length);assert.equal(g.index.count*4,indices.length);
 for(let i=0;i<p.count;i++)for(let k=0;k<3;k++)assert.equal(p.getComponent(i,k),candidate.readFloatLE(i*12+k*4));for(let i=0;i<g.index.count;i++)assert.equal(g.index.getX(i),indices.readUInt32LE(i*4));
 const positions=new Set(Array.from({length:p.count},(_,i)=>key(p,i))),retained=report.retention.find(r=>r.node===name);let count=0;for(let i=0;i<op.count;i++)if(positions.has(key(op,i)))count++;assert.equal(count,retained.originalVerticesRetainedExactly);
 for(let i=0;i<g.attributes.normal.count;i++){const n=g.attributes.normal;assert(Math.abs(Math.hypot(n.getX(i),n.getY(i),n.getZ(i))-1)<.003);}
 checks.push({node:name,vertices:p.count,triangles:g.index.count/3,exactRetainedOriginalVertices:count,exactCandidateRoundtrip:true});
}
for(const row of report.accepted){const p=after.get('MMA paramedian '+row.side),c=after.get('MMA falcine terminal '+row.side);for(let k=0;k<row.sharedParentIndices.length;k++)for(const attr of ['position','normal'])for(let j=0;j<3;j++)assert.equal(p.attributes[attr].getComponent(row.sharedParentIndices[k],j),c.attributes[attr].getComponent(row.sharedChildIndices[k],j));}
const source=JSON.parse(fs.readFileSync(work+'/decoded/source-assets.json'));for(const [file,hash]of Object.entries(source))if(file!=='complete-circulation.glb')assert.equal(crypto.createHash('sha256').update(fs.readFileSync('public/anatomy/models/'+file)).digest('hex'),hash);
const result={release:'0.9.88',passed:true,arterialMeshesChecked:after.size,unchangedArterialMeshes:after.size-selected.size,otherAssetsByteExact:4,sharedCoordinatesAndNormalsExact:true,changes:checks};fs.writeFileSync(work+'/export-validation.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
