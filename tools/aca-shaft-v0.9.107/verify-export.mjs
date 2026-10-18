import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;const work=path.resolve(process.argv[2]),candidate=process.argv[3]??work+'/complete-circulation.glb';
async function load(file){const b=fs.readFileSync(file),g=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');const out=new Map();g.scene.traverse(o=>{if(o.isMesh)out.set(g.parser.json.nodes[g.parser.associations.get(o).nodes].name,o.geometry)});return out}
const before=await load(work+'/old-complete-circulation.glb'),after=await load(candidate),rows=JSON.parse(fs.readFileSync(work+'/normal-provenance.json')),selected=new Set(rows.map(x=>x.node));assert.equal(before.size,after.size);
for(const [n,g]of after){const old=before.get(n);assert(old);if(!selected.has(n)){for(const a of ['position','normal'])assert.deepEqual(g.attributes[a].array,old.attributes[a].array,n+' '+a);assert.deepEqual(g.index.array,old.index.array,n+' indices');continue}
 const p=g.attributes.position,op=old.attributes.position,b=fs.readFileSync(work+'/candidate/'+n+'.positions.bin'),idx=fs.readFileSync(work+'/candidate/'+n+'.indices.bin');assert.equal(p.count*12,b.length);assert.equal(g.index.count*4,idx.length);
 for(let i=0;i<p.count;i++)for(let k=0;k<3;k++)assert.equal(p.getComponent(i,k),b.readFloatLE(i*12+k*4));
 for(let i=0;i<g.index.count;i++){assert.equal(g.index.getX(i),idx.readUInt32LE(i*4));assert.equal(g.index.getX(i),old.index.getX(i),n+' all source indices');}
 const nb=fs.readFileSync(work+'/candidate/'+n+'.normal-snorm16.bin');assert.deepEqual(Buffer.from(g.attributes.normal.array.buffer,g.attributes.normal.array.byteOffset,g.attributes.normal.array.byteLength),nb,n+' SNORM16 exact');
 let retained=0;
 for(let i=0;i<g.index.count;i+=3){let unchanged=true;for(let j=0;j<3;j++){const vi=g.index.getX(i+j);for(let k=0;k<3;k++)if(g.attributes.position.getComponent(vi,k)!==old.attributes.position.getComponent(vi,k))unchanged=false;}if(unchanged){retained++;for(let j=0;j<3;j++){const vi=g.index.getX(i+j);for(let k=0;k<3;k++)assert.equal(g.attributes.normal.getComponent(vi,k),old.attributes.normal.getComponent(vi,k),n+' fixed source corner normal');}}}
 assert.equal(retained,rows.find(x=>x.node===n).retainedSourceTrianglesWithExactCornerNormals);


}
const source=JSON.parse(fs.readFileSync(work+'/decoded/source-assets.json'));for(const [file,hash]of Object.entries(source))if(file!=='complete-circulation.glb')assert.equal(crypto.createHash('sha256').update(fs.readFileSync('public/anatomy/models/'+file)).digest('hex'),hash);
const report={release:'0.9.107',passed:true,arterialMeshesChecked:after.size,unchangedArterialMeshes:after.size-selected.size,otherAssetsByteExact:4,candidateBuffersExact:true,allSourceFaceIndicesExact:true,retainedSourceCornerNormalsExact:true};fs.writeFileSync(work+'/export-validation.json',JSON.stringify(report,null,2)+'\n');console.log(report);
