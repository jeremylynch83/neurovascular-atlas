// Verify the actual application loader, unchanged meshes and the repaired prefix.
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {MeshoptDecoder} from 'meshoptimizer';
const work=path.resolve(process.argv[2]);await MeshoptDecoder.ready;
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function load(file){const b=fs.readFileSync(file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');const out=new Map();g.scene.traverse(o=>{if(o.isMesh)out.set(g.parser.json.nodes[g.parser.associations.get(o).nodes].name,o.geometry)});return out;}
const before=await load(work+'/old-complete-circulation.glb'),after=await load('public/anatomy/models/complete-circulation.glb');assert.equal(before.size,after.size);
const changes=[];
const accepted=JSON.parse(fs.readFileSync(work+'/accepted-corrections.json')).accepted[0];
for(const [name,g]of after){const old=before.get(name);assert(old);const p=g.attributes.position,op=old.attributes.position;if(name!=='ACA falcine branch left'){assert.deepEqual(p.array,op.array,name+' positions');assert.deepEqual(g.index.array,old.index.array,name+' indices');assert.deepEqual(g.attributes.normal.array,old.attributes.normal.array,name+' normals');continue;}
const candidate=fs.readFileSync(work+'/candidate/'+name+'.positions.bin'),indices=fs.readFileSync(work+'/candidate/'+name+'.indices.bin');assert.equal(p.count*12,candidate.length);assert.equal(g.index.count*4,indices.length);
for(let i=0;i<p.count;i++)for(let k=0;k<3;k++)assert.equal(p.getComponent(i,k),candidate.readFloatLE(i*12+k*4));
for(let i=0;i<g.index.count;i++)assert.equal(g.index.getX(i),indices.readUInt32LE(i*4));
const key=(attr,i)=>[0,1,2].map(k=>attr.getComponent(i,k)).join(','),positions=new Set(Array.from({length:p.count},(_,i)=>key(p,i)));let fixed=0;
for(let i=0;i<op.count;i++)if(op.getZ(i)>=accepted.clipZ){assert(positions.has(key(op,i)));fixed++;}
const faceKey=(attr,idx,i)=>[0,1,2].map(k=>key(attr,idx.getX(i+k))).sort().join(';'),faces=new Set();for(let i=0;i<g.index.count;i+=3)faces.add(faceKey(p,g.index,i));let fixedFaces=0;
for(let i=0;i<old.index.count;i+=3)if([0,1,2].every(k=>op.getZ(old.index.getX(i+k))>=accepted.clipZ)){assert(faces.has(faceKey(op,old.index,i)));fixedFaces++;}
changes.push({node:name,originalDistalVerticesRetainedExactly:fixed,originalDistalTrianglesRetainedExactly:fixedFaces,collarCutZMm:accepted.clipZ,vertices:p.count,triangles:g.index.count/3,candidateRoundtripExact:true});}
assert.equal(changes.length,1);
const source=JSON.parse(fs.readFileSync(work+'/decoded/source-assets.json')),crypto=await import('node:crypto');let unaffectedAssets=0;
for(const [file,hash]of Object.entries(source))if(file!=='complete-circulation.glb'){const bytes=fs.readFileSync('public/anatomy/models/'+file);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),hash);unaffectedAssets++;}
const report={release:'0.9.87',passed:true,arterialMeshesChecked:after.size,otherAssetsByteExact:unaffectedAssets,changes};fs.writeFileSync(work+'/export-validation.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
