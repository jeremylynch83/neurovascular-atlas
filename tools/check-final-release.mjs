// Verify every delivered GLB through the actual application loader.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const baseline=path.resolve(process.argv[2]);
const out=path.resolve(process.argv[3]);
const expected=JSON.parse(fs.readFileSync(path.join(baseline,'source-assets.json')));
const selected=new Set(JSON.parse(fs.readFileSync('anatomy/source/audit-finish-v0950/revision.json')).newLabels);
const checks=[];
for(const [filename,hash] of Object.entries(expected)){
  const bytes=fs.readFileSync('public/anatomy/models/'+filename);
  const sha=crypto.createHash('sha256').update(bytes).digest('hex');
  assert.equal(sha,hash,'All accepted model assets must remain byte exact');
  const loader=new GLTFLoader();loader.setMeshoptDecoder(MeshoptDecoder);
  const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  let labels=0,triangles=0;
  gltf.scene.traverse(o=>{
    if(!o.isMesh)return;
    const a=gltf.parser.associations.get(o),name=gltf.parser.json.nodes[a.nodes].name;
    const p=fs.readFileSync(path.join(baseline,name+'.positions.bin'));
    const f=fs.readFileSync(path.join(baseline,name+'.indices.bin'));
    const g=o.geometry;
    assert.equal(p.length,g.attributes.position.count*12,name);
    assert.equal(f.length,g.index.count*4,name);
    for(let i=0;i<g.attributes.position.count;i++)for(let j=0;j<3;j++)assert.equal(g.attributes.position.getComponent(i,j),p.readFloatLE(i*12+j*4),name+' position');
    for(let i=0;i<g.index.count;i++)assert.equal(g.index.getX(i),f.readUInt32LE(i*4),name+' face');
    if(selected.has(name))for(let i=0;i<g.attributes.normal.count;i++)assert(Math.abs(Math.hypot(g.attributes.normal.getX(i),g.attributes.normal.getY(i),g.attributes.normal.getZ(i))-1)<.002,name+' normal');
    labels++;triangles+=g.index.count/3;
  });
  checks.push({file:filename,sha256:sha,labels,triangles,assetByteExact:true,exactLoadedPositionsAndIndices:true});
}
const manifest=JSON.parse(fs.readFileSync('public/anatomy/manifest.json'));
assert.equal(manifest.release,'0.9.51');
for(const s of manifest.structures){
  if(s.vesselCourse&&s.asset){
    const c=checks.find(c=>'models/'+c.file===s.asset.file);
    assert.equal(s.vesselCourse.geometrySha256,c.sha256,s.id+' geometry hash');
  }
}
const report={release:manifest.release,passed:true,checks,scope:'Actual Three.js GLTFLoader and MeshoptDecoder for all five models; complete byte, position and face equality to accepted v0.9.50.'};
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:true,assets:checks.length,labels:checks.reduce((a,c)=>a+c.labels,0)}));
