// Conservative, reversible authoring trial. Writes candidates, never the input.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {MeshoptDecoder, MeshoptEncoder, MeshoptSimplifier} from 'meshoptimizer';

await Promise.all([MeshoptDecoder.ready, MeshoptEncoder.ready, MeshoptSimplifier.ready]);
const [baseline, output] = process.argv.slice(2);
assert(baseline && output, 'Usage: node trial.mjs BASELINE_APP OUTPUT_DIRECTORY');
const gate=process.argv[4]?JSON.parse(fs.readFileSync(process.argv[4])):{};
const excluded=new Set(gate.excludedMeshes??[]);
fs.mkdirSync(output, {recursive: true});
const source = fs.readFileSync(path.join(baseline, 'public/anatomy/models/brain-context.glb'));
const jsonLength = source.readUInt32LE(12);
const original = JSON.parse(source.subarray(20, 20 + jsonLength));
const binary = source.subarray(28 + jsonLength);
const manifest = JSON.parse(fs.readFileSync(path.join(baseline, 'public/anatomy/manifest.json')));
const rows = manifest.structures.filter(s => s.asset?.file === 'models/brain-context.glb');
const rowByName = new Map(rows.map(s => [s.asset.node, s]));
const models = [], shared = new Map();
const key = (p, i) => `${p[i*3]},${p[i*3+1]},${p[i*3+2]}`;
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
function decode(accessor, filter = true) {
  const a = original.accessors[accessor], v = original.bufferViews[a.bufferView];
  const e = v.extensions.EXT_meshopt_compression, out = Buffer.alloc(v.byteLength);
  assert((a.byteOffset ?? 0) === 0);
  MeshoptDecoder.decodeGltfBuffer(out, e.count, e.byteStride, binary.subarray(e.byteOffset, e.byteOffset + e.byteLength), e.mode, filter ? e.filter : undefined);
  return out;
}
for (const node of original.nodes) {
  if (node.mesh === undefined) continue;
  const mesh = original.meshes[node.mesh]; assert.equal(mesh.primitives.length, 1);
  const primitive = mesh.primitives[0], row = rowByName.get(node.name); assert(row);
  assert.deepEqual(Object.keys(primitive.attributes).sort(), ['NORMAL', 'POSITION']);
  const pBytes = decode(primitive.attributes.POSITION), nBytes = decode(primitive.attributes.NORMAL), iBytes = decode(primitive.indices);
  const p = new Float32Array(pBytes.buffer, pBytes.byteOffset, pBytes.byteLength/4);
  const index = new Uint32Array(iBytes.buffer, iBytes.byteOffset, iBytes.byteLength/4);
  const normals = new Float32Array(p.length);
  for (let i=0;i<p.length/3;i++) for(let k=0;k<3;k++) normals[i*3+k] = Math.max(-1, nBytes.readInt16LE(i*8+k*2)/32767);
  const model = {id: row.id, name: node.name, mesh: node.mesh, category: row.anatomy.category, primitive,
    pBytes, nBytes, p, index, normals, locks: new Uint8Array(p.length/3), anchors: [],
    unfilteredNormals: decode(primitive.attributes.NORMAL, false)};
  const m = models.length;
  for(let i=0;i<p.length/3;i++) {const k=key(p,i), old=shared.get(k);if(old===undefined)shared.set(k,m);else if(old!==m)shared.set(k,-1);}
  models.push(model);
}
const byId = new Map(models.map(m => [m.id, m]));
for(const row of manifest.structures) for(const anchor of [row.surfaceAnchor, ...(row.secondarySurfaceAnchors ?? [])].filter(Boolean)) {
  const m = byId.get(anchor.structureId); assert(m);
  m.anchors.push({sourceId: row.id, triangleIndex: anchor.triangleIndex});
  for(let k=0;k<3;k++)m.locks[m.index[anchor.triangleIndex*3+k]]=1;
}
for(const m of models) {
  // Degenerate source triangles can confuse geometric topology after an edge
  // collapse. Keep their vertices and surrounding faces completely fixed.
  for(let i=0;i<m.index.length;i+=3) {
    const a=m.index[i]*3,b=m.index[i+1]*3,c=m.index[i+2]*3;
    const ux=m.p[b]-m.p[a],uy=m.p[b+1]-m.p[a+1],uz=m.p[b+2]-m.p[a+2];
    const vx=m.p[c]-m.p[a],vy=m.p[c+1]-m.p[a+1],vz=m.p[c+2]-m.p[a+2];
    const x=uy*vz-uz*vy,y=uz*vx-ux*vz,z=ux*vy-uy*vx;
    if(x*x+y*y+z*z<=1e-24)for(let k=0;k<3;k++)m.locks[m.index[i+k]]=1;
  }
  const seeds=m.locks.slice();
  for(let i=0;i<m.index.length;i+=3) if(seeds[m.index[i]]||seeds[m.index[i+1]]||seeds[m.index[i+2]])for(let k=0;k<3;k++)m.locks[m.index[i+k]]=1;
  for(let i=0;i<m.p.length/3;i++)if(shared.get(key(m.p,i))===-1)m.locks[i]=1;
}
shared.clear();
const dumpDir = path.join(output, 'baseline');fs.mkdirSync(dumpDir,{recursive:true});
for(const m of models) {
  fs.writeFileSync(path.join(dumpDir, m.name+'.positions.bin'), m.pBytes);
  fs.writeFileSync(path.join(dumpDir, m.name+'.indices.bin'), Buffer.from(m.index.buffer,m.index.byteOffset,m.index.byteLength));
}
const trials=[];
for(const error of gate.errors??[.01,.025,.05]) {
  const tag=String(error), target=path.join(output, tag);fs.mkdirSync(target,{recursive:true});
  const doc=structuredClone(original), changed=new Map(), results=[];
  for(const m of models) {
    const eligible=['cerebral_cortex','cerebellum'].includes(m.category) && m.index.length/3>=5000 && !m.name.includes('peduncle') && !excluded.has(m.name);
    let indices=m.index.slice(), achieved=0;
    if(eligible) [indices,achieved]=MeshoptSimplifier.simplifyWithAttributes(indices,m.p,3,m.normals,3,[.5,.5,.5],m.locks,
      Math.floor(m.index.length*.65/3)*3,error,['LockBorder','ErrorAbsolute','PreserveFolds']);
    const changedMesh=indices.length<m.index.length;
    const faceMap={};
    if(changedMesh) {
      const faces=new Map();
      for(let i=0;i<indices.length;i+=3)faces.set(`${indices[i]},${indices[i+1]},${indices[i+2]}`,i/3);
      for(const a of m.anchors) {
        const old=Array.from(m.index.subarray(a.triangleIndex*3,a.triangleIndex*3+3));let found;
        for(let rotate=0;rotate<3;rotate++) {const order=[old[rotate],old[(rotate+1)%3],old[(rotate+2)%3]],f=faces.get(order.join(','));if(f!==undefined){indices.set(old,f*3);found=f;break;}}
        assert(found!==undefined,`${m.name}: protected anchor face removed`);faceMap[a.triangleIndex]=found;
      }
      // Compact in original vertex order. Retained coordinates and encoded
      // normals are copied exactly, with no coordinate or shading update.
      const used=new Uint8Array(m.p.length/3);for(const i of indices)used[i]=1;
      const remap=new Uint32Array(used.length).fill(0xffffffff);let count=0;
      for(let i=0;i<used.length;i++)if(used[i])remap[i]=count++;
      const p=Buffer.alloc(count*12),n=Buffer.alloc(count*8),normalCheck=Buffer.alloc(count*8);
      for(let i=0;i<used.length;i++)if(used[i]) {
        m.pBytes.copy(p,remap[i]*12,i*12,i*12+12);
        m.unfilteredNormals.copy(n,remap[i]*8,i*8,i*8+8);
        m.nBytes.copy(normalCheck,remap[i]*8,i*8,i*8+8);
      }
      for(let i=0;i<indices.length;i++)indices[i]=remap[indices[i]];
      const iBytes=Buffer.from(indices.buffer,indices.byteOffset,indices.byteLength);
      for(const [accessor,bytes,vertexCount] of [[m.primitive.attributes.POSITION,p,count],[m.primitive.attributes.NORMAL,n,count],[m.primitive.indices,iBytes,indices.length]]) {
        const a=doc.accessors[accessor],v=doc.bufferViews[a.bufferView],e=v.extensions.EXT_meshopt_compression;
        const encoded=MeshoptEncoder.encodeGltfBuffer(bytes,vertexCount,e.byteStride,e.mode);
        const roundtrip=Buffer.alloc(bytes.length);MeshoptDecoder.decodeGltfBuffer(roundtrip,vertexCount,e.byteStride,encoded,e.mode,e.filter);
        assert.deepEqual(roundtrip,accessor===m.primitive.attributes.NORMAL?normalCheck:bytes,'Lossless retained attributes');
        changed.set(a.bufferView,{encoded,count:vertexCount,length:bytes.length});a.count=vertexCount;
        if(accessor===m.primitive.attributes.POSITION) {
          const positions=new Float32Array(p.buffer,p.byteOffset,p.length/4);a.min=[Infinity,Infinity,Infinity];a.max=[-Infinity,-Infinity,-Infinity];
          for(let i=0;i<positions.length;i++){const k=i%3;a.min[k]=Math.min(a.min[k],positions[i]);a.max[k]=Math.max(a.max[k],positions[i]);}
        }
      }
      fs.writeFileSync(path.join(target,m.name+'.positions.bin'),p);fs.writeFileSync(path.join(target,m.name+'.indices.bin'),iBytes);
    }
    results.push({id:m.id,name:m.name,category:m.category,eligible,changed:changedMesh,
      beforeVertices:m.p.length/3,afterVertices:changedMesh?doc.accessors[m.primitive.attributes.POSITION].count:m.p.length/3,
      beforeTriangles:m.index.length/3,afterTriangles:indices.length/3,approximateCombinedErrorMm:achieved,
      lockedVertices:m.locks.reduce((a,b)=>a+b,0),anchorTriangleMap:faceMap});
  }
  let physical=0,virtual=0;const chunks=[];
  for(let i=0;i<doc.bufferViews.length;i++) {
    const v=doc.bufferViews[i],e=v.extensions.EXT_meshopt_compression,patch=changed.get(i);
    const encoded=patch?.encoded??binary.subarray(e.byteOffset,e.byteOffset+e.byteLength);
    const pad=(-physical)&3;if(pad){chunks.push(Buffer.alloc(pad));physical+=pad;}
    e.byteOffset=physical;e.byteLength=encoded.length;if(patch){e.count=patch.count;v.byteLength=patch.length;}
    v.byteOffset=virtual;virtual+=v.byteLength;virtual=(virtual+3)&~3;
    chunks.push(encoded);physical+=encoded.length;
  }
  if(physical%4)chunks.push(Buffer.alloc(4-physical%4));
  const bin=Buffer.concat(chunks);doc.buffers[0].byteLength=bin.length;doc.buffers[1].byteLength=virtual;
  let js=Buffer.from(JSON.stringify(doc));if(js.length%4)js=Buffer.concat([js,Buffer.alloc(4-js.length%4,32)]);
  const header=Buffer.alloc(20),binHeader=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+js.length+bin.length,8);header.writeUInt32LE(js.length,12);header.writeUInt32LE(0x4e4f534a,16);binHeader.writeUInt32LE(bin.length);binHeader.writeUInt32LE(0x004e4942,4);
  const packed=Buffer.concat([header,js,binHeader,bin]);fs.writeFileSync(path.join(output,`brain-${tag}.glb`),packed);
  const result={errorBudgetMm:error,targetTriangleRatio:.65,beforeBytes:source.length,afterBytes:packed.length,
    beforeGzipBytes:zlib.gzipSync(source,{level:9}).length,afterGzipBytes:zlib.gzipSync(packed,{level:9}).length,
    beforeSha256:hash(source),afterSha256:hash(packed),beforeTriangles:results.reduce((n,m)=>n+m.beforeTriangles,0),
    afterTriangles:results.reduce((n,m)=>n+m.afterTriangles,0),changedMeshes:results.filter(m=>m.changed).length,meshes:results};
  fs.writeFileSync(path.join(output,`trial-${tag}.json`),JSON.stringify(result,null,2)+'\n');trials.push(result);
  console.log(JSON.stringify({...result,meshes:undefined}));
}
fs.writeFileSync(path.join(output,'trials.json'),JSON.stringify(trials.map(({meshes,...r})=>r),null,2)+'\n');
