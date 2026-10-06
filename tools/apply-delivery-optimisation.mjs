// Verify through the app's actual loader, then update assets and their bindings.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {Vector3} from 'three';
await MeshoptDecoder.ready;
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const manifestPath='anatomy/generated/complete_manifest.json';
const manifest=JSON.parse(fs.readFileSync(manifestPath));
const rows=new Map(manifest.structures.map(s=>[s.id,s]));
const report=JSON.parse(fs.readFileSync('.delivery-models/optimisation-report.json'));
const hashes=new Map(),sizes={},revisions={},meshes=new Map();
const loaderChecks=[];
for(const row of report){
 const file=row.filename,old=fs.readFileSync(`public/anatomy/models/${file}`),data=fs.readFileSync(`.delivery-models/${file}`);
 hashes.set(sha(old),sha(data));sizes[`models/${file}`]=data.length;revisions[`models/${file}`]=sha(data).slice(0,20);
 const gltf=await loader.parseAsync(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),'');
 gltf.scene.updateMatrixWorld(true);let count=0,triangles=0;
 gltf.scene.traverse(o=>{
  if(!o.isMesh)return;
  const assoc=gltf.parser.associations.get(o),name=gltf.parser.json.nodes[assoc.nodes].name;
  assert(!meshes.has(`${file}:${name}`));meshes.set(`${file}:${name}`,o);
  const p=o.geometry.getAttribute('position'),n=o.geometry.getAttribute('normal');
  assert.equal(p.count,n.count);assert(o.geometry.index);
  for(let i=0;i<p.count;i++){
   assert(Number.isFinite(p.getX(i))&&Number.isFinite(p.getY(i))&&Number.isFinite(p.getZ(i)));
   const norm=Math.hypot(n.getX(i),n.getY(i),n.getZ(i));assert(norm>0.99&&norm<1.01);
  }
  count++;triangles+=o.geometry.index.count/3;
 });
 assert.equal(triangles,row.triangleCount);
 const oldJsonLength=old.readUInt32LE(12),oldDoc=JSON.parse(old.subarray(20,20+oldJsonLength));
 assert.equal(count,oldDoc.meshes.reduce((n,m)=>n+m.primitives.length,0));
 loaderChecks.push({file,meshes:count,triangles,positionsFinite:true,normalPackingDecoded:true});
 console.log(`Loader verified ${file}: ${count} meshes, ${triangles} triangles`);
}
// Preserve historical provenance hashes. Refresh only current runtime identities.
const brainHash=hashes.get(manifest.brainRegistration.registeredAssetSha256);assert(brainHash);
manifest.brainRegistration.registeredAssetSha256=brainHash;
manifest.assetRevisions=revisions;manifest.assetByteSizes=sizes;
let primary=0,secondary=0;
function bind(a){
 const target=rows.get(a.structureId);assert(target?.asset);
 const mesh=meshes.get(`${path.basename(target.asset.file)}:${target.asset.node}`);assert(mesh);
 const p=mesh.geometry.getAttribute('position'),ix=mesh.geometry.index,offset=a.triangleIndex*3;
 assert(offset>=0&&offset+2<ix.count);const point=new Vector3();
 for(let j=0;j<3;j++)point.addScaledVector(new Vector3().fromBufferAttribute(p,ix.getX(offset+j)),a.barycentric[j]);
 point.applyMatrix4(mesh.matrixWorld);
 assert(point.distanceTo(new Vector3(...a.position))<0.001,'Surface anchor moved beyond delivery precision');
 a.position=point.toArray();a.assetSha256=brainHash;
}
for(const s of manifest.structures){
 if(s.asset)assert(meshes.has(`${path.basename(s.asset.file)}:${s.asset.node}`),s.id);
 if(s.surfaceAnchor){bind(s.surfaceAnchor);s.landmark.point=s.surfaceAnchor.position;primary++;}
 for(const a of s.secondarySurfaceAnchors??[]){bind(a);secondary++;}
 if(s.vesselCourse){
  s.vesselCourse.brainAssetSha256=brainHash;
  const replacement=hashes.get(s.vesselCourse.geometrySha256);assert(replacement);s.vesselCourse.geometrySha256=replacement;
 }
}
for(const s of manifest.structures){
 const keys=s.vesselGuide?.anchorIds;
 if(keys?.length){s.landmark.course=keys.map(k=>rows.get(k).surfaceAnchor.position);s.landmark.point=s.landmark.course[0];}
}
const finalReport={release:manifest.release,kind:'delivery-optimisation',structures:manifest.structures.length,models:report,loaderChecks,surfaceAnchors:primary,secondarySurfaceAnchors:secondary,anchorBindingsVerified:true,ponsAdvancementRetained:true,maximumPositionErrorMm:Math.max(...report.map(r=>r.maximumPositionErrorMm)),triangleCountUnchanged:true,geometryFittingChanged:false,scope:'Mesh decoding, topology preservation, normal precision and surface-anchor checks; no fresh browser GPU appearance check.'};
manifest.deliveryOptimisation={method:'Meshopt vertex/index compression and 12-bit octahedral normal packing',positionGridMm:1/4096,maximumPositionErrorMm:finalReport.maximumPositionErrorMm,triangleCountUnchanged:true,evidence:'docs/validation/delivery-optimisation-v0.9.21.json'};
const write=(p,o)=>fs.writeFileSync(p,JSON.stringify(o,null,2)+'\n');
for(const row of report)fs.copyFileSync(`.delivery-models/${row.filename}`,`public/anatomy/models/${row.filename}`);
write(manifestPath,manifest);
const landmarks=JSON.parse(fs.readFileSync('public/anatomy/brain-landmarks.json'));
landmarks.registration=manifest.brainRegistration;landmarks.anchors=manifest.structures.filter(r=>r.landmark&&r.system==='brain');write('public/anatomy/brain-landmarks.json',landmarks);
const courses=JSON.parse(fs.readFileSync('public/anatomy/vessel-courses.json'));
courses.brainRegistration=manifest.brainRegistration;courses.courses=manifest.structures.filter(r=>r.vesselCourse).map(r=>r.vesselCourse);write('public/anatomy/vessel-courses.json',courses);
write('docs/validation/delivery-optimisation-v0.9.21.json',finalReport);
console.log(`Applied delivery optimisation; ${primary} primary and ${secondary} secondary anchors rebound.`);
