// Lossless EXT_meshopt_compression. No quantisation, vertex reordering,
// decimation, triangle rotation or geometry changes. Retains mesh/node IDs.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { MeshoptEncoder, MeshoptDecoder } from 'meshoptimizer';
import { createHash } from 'node:crypto';
import { deflateSync } from 'node:zlib';
import path from 'node:path';
import assert from 'node:assert/strict';

await Promise.all([MeshoptEncoder.ready, MeshoptDecoder.ready]);
const source = process.argv[2], destination = process.argv[3];
assert(source && destination, 'Usage: node tools/compress_scene_lossless.mjs INPUT.glb OUTPUT.glb');
const input = await readFile(source);
assert.equal(input.readUInt32LE(0), 0x46546c67);
const jsonLength = input.readUInt32LE(12);
const document = JSON.parse(input.subarray(20, 20 + jsonLength).toString());
const binaryOffset = 20 + jsonLength + 8;
const binary = input.subarray(binaryOffset);
assert.equal(document.buffers.length, 1);
assert(!document.extensionsUsed?.includes('EXT_meshopt_compression'));
const chunks = [];
let compressedOffset = 0, verified = 0;
for (let index = 0; index < document.bufferViews.length; index++) {
  const view = document.bufferViews[index];
  const accessors = document.accessors.filter(a => a.bufferView === index);
  assert(accessors.length > 0, 'Every view must be an attribute/index buffer');
  assert(accessors.every(a => !a.sparse && !(a.byteOffset ?? 0)));
  const indices = accessors.every(a => a.type === 'SCALAR');
  const stride = view.byteStride ?? (indices ? (accessors[0].componentType === 5125 ? 4 : 2) : 12);
  const count = view.byteLength / stride;
  assert(Number.isInteger(count));
  const raw = new Uint8Array(binary.buffer, binary.byteOffset + (view.byteOffset ?? 0), view.byteLength);
  // INDICES retains index byte order, including barycentric triangle order.
  const mode = indices ? 'INDICES' : 'ATTRIBUTES';
  const encoded = MeshoptEncoder.encodeGltfBuffer(raw, count, stride, mode, 0);
  const decoded = new Uint8Array(view.byteLength);
  MeshoptDecoder.decodeGltfBuffer(decoded, count, stride, encoded, mode, 'NONE');
  assert(Buffer.from(decoded).equals(Buffer.from(raw)), 'Decoded bytes differ');
  verified++;
  const padding = (4 - encoded.byteLength % 4) % 4;
  chunks.push(Buffer.from(encoded), Buffer.alloc(padding));
  view.buffer = 1;
  view.extensions = { ...view.extensions, EXT_meshopt_compression: {
    buffer: 0, byteOffset: compressedOffset, byteLength: encoded.byteLength,
    byteStride: stride, count, mode, filter: 'NONE',
  } };
  compressedOffset += encoded.byteLength + padding;
}
const compressed = Buffer.concat(chunks);
document.buffers = [
  { byteLength: compressed.byteLength },
  { byteLength: document.buffers[0].byteLength, extensions: { EXT_meshopt_compression: { fallback: true } } },
];
document.extensionsUsed = [...(document.extensionsUsed ?? []), 'EXT_meshopt_compression'];
document.extensionsRequired = [...(document.extensionsRequired ?? []), 'EXT_meshopt_compression'];
let json = Buffer.from(JSON.stringify(document));
json = Buffer.concat([json, Buffer.alloc((4 - json.length % 4) % 4, 0x20)]);
const header = Buffer.alloc(20);
header.writeUInt32LE(0x46546c67, 0); header.writeUInt32LE(2, 4);
header.writeUInt32LE(12 + 8 + json.length + 8 + compressed.length, 8);
header.writeUInt32LE(json.length, 12); header.writeUInt32LE(0x4e4f534a, 16);
const binHeader = Buffer.alloc(8); binHeader.writeUInt32LE(compressed.length, 0); binHeader.writeUInt32LE(0x004e4942, 4);
const output = Buffer.concat([header, json, binHeader, compressed]);
await mkdir(path.dirname(destination), {recursive:true}); await writeFile(destination, output);
console.log(JSON.stringify({file:path.basename(source),originalBytes:input.length,compressedBytes:output.length,
  estimatedZipBytes:deflateSync(output,{level:6}).length,verifiedBuffers:verified,
  decodedBytesIdentical:true,nodeCount:document.nodes.length,
  originalSha256:createHash('sha256').update(input).digest('hex'),compressedSha256:createHash('sha256').update(output).digest('hex')}));
