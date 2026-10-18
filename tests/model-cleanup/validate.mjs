// Compare all decoded geometry and anatomical contracts with an unpacked release.
// Usage: node tests/model-cleanup/validate.mjs /path/to/unpacked/v0.9.116
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'meshoptimizer';

const baseline = path.resolve(process.argv[2]);
const root = path.resolve(import.meta.dirname, '../..');
const read = file => JSON.parse(fs.readFileSync(file));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
await MeshoptDecoder.ready;
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const original = read(path.join(baseline, 'public/anatomy/manifest.json'));
const current = read(path.join(root, 'public/anatomy/manifest.json'));
const files = [...new Set(current.structures.filter(s => s.asset).map(s => s.asset.file))];

async function geometry(file) {
  const b = fs.readFileSync(file);
  const gltf = await loader.parseAsync(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength), '');
  const result = [];
  gltf.scene.updateMatrixWorld(true);
  gltf.scene.traverse(o => {
    if (!o.isMesh) return;
    const g = o.geometry, attributes = {};
    for (const [name, a] of Object.entries(g.attributes)) {
      const values = new Float64Array(a.count * a.itemSize);
      for (let i = 0; i < a.count; i++) for (let k = 0; k < a.itemSize; k++) values[i * a.itemSize + k] = a.getComponent(i, k);
      attributes[name] = { count: a.count, itemSize: a.itemSize, normalised: a.normalized, sha256: sha(Buffer.from(values.buffer)) };
    }
    result.push({ name: o.name, node: gltf.parser.associations.get(o)?.nodes,
      matrix: o.matrixWorld.toArray(), attributes,
      indices: g.index ? sha(Buffer.from(Uint32Array.from(g.index.array).buffer)) : null,
      indexCount: g.index?.count ?? 0, groups: g.groups });
    g.dispose();
  });
  return result;
}

let meshes = 0, triangles = 0;
const assetChecks = [];
for (const file of files) {
  const before = await geometry(path.join(baseline, 'public/anatomy', file));
  const after = await geometry(path.join(root, 'public/anatomy', file));
  assert.deepEqual(after, before, file + ': decoded data, names, node bindings and transforms');
  meshes += after.length;
  triangles += after.reduce((n, g) => n + g.indexCount / 3, 0);
  const bytes = fs.readFileSync(path.join(root, 'public/anatomy', file));
  assert.equal(current.assetRevisions[file], sha(bytes).slice(0, 20));
  assert.equal(current.assetByteSizes[file], bytes.length);
  assetChecks.push({ file, meshes: after.length, allAttributesAndTriangleOrderExact: true });
  console.log('Exact decoded geometry:', file, after.length);
}
assert.equal(meshes, 1250);

function anatomicalContract(m) {
  const d = structuredClone(m);
  for (const k of ['release', 'assetRevisions', 'assetByteSizes', 'currentDeferredReviewRegistry', 'losslessContainerCleanup']) delete d[k];
  delete d.brainRegistration.registeredAssetSha256;
  for (const s of d.structures) {
    if (s.vesselCourse) { delete s.vesselCourse.geometrySha256; delete s.vesselCourse.brainAssetSha256; }
    if (s.surfaceAnchor) delete s.surfaceAnchor.assetSha256;
    for (const a of s.secondarySurfaceAnchors ?? []) delete a.assetSha256;
  }
  return d;
}
assert.deepEqual(anatomicalContract(current), anatomicalContract(original));
for (const name of ['dsa-surfaces.json', 'dsa-flow.json']) {
  const before = read(path.join(baseline, 'public/anatomy', name));
  const after = read(path.join(root, 'public/anatomy', name));
  for (const [file, h] of Object.entries(after.sourceHashes)) assert.equal(h, sha(fs.readFileSync(path.join(root, 'public/anatomy', file))));
  delete before.sourceHashes; delete after.sourceHashes;
  delete before.assetRevisions; delete after.assetRevisions;
  assert.deepEqual(after, before, name + ': full DSA recipes and flow unchanged');
}
for (const file of ['ANATOMICAL_ISSUES.json', 'ANATOMICAL_ISSUES.md']) {
  assert.deepEqual(fs.readFileSync(path.join(root, file)), fs.readFileSync(path.join(baseline, file)));
}
const previousRegistry = read(path.join(baseline, original.currentDeferredReviewRegistry));
const registry = read(path.join(root, current.currentDeferredReviewRegistry));
assert.deepEqual(registry.cases, previousRegistry.cases);
assert.deepEqual(registry.requiredImplementationSha256, previousRegistry.requiredImplementationSha256);
for (const [file, hash] of Object.entries(registry.requiredImplementationSha256)) assert.equal(sha(fs.readFileSync(path.join(root, file))), hash);
for (const [file, hash] of Object.entries(registry.requiredSourceAssetSha256)) assert.equal(sha(fs.readFileSync(path.join(root, 'public/anatomy', file))), hash);
const report = { passed: true, release: current.release, meshes, triangles, assetChecks,
  allDecodedAttributesAndTriangleOrderExact: true, anatomicalContractsExactExceptAssetHashes: true,
  dsaRecipesAndFlowExactExceptAssetHashes: true, anatomicalIssueRegisterByteExact: true,
  deferredCasesAndReviewImplementationExact: true };
fs.writeFileSync(path.join(root, 'docs/model-cleanup-geometry.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report));
