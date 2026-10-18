# Lossless vessel index encoding - v0.9.119

This release reduces the three vessel files using smaller index-buffer encoding.
Every decoded coordinate, normal and triangle index remains exact, including
the original triangle order and the order of corners within each triangle.
There is no vessel smoothing, simplification, quantisation or vertex reordering.
Native junctions, small branches, calibre, curvature and repaired walls remain
geometrically identical to v0.9.118.

| Vessel file | Before bytes | After bytes |
| --- | ---: | ---: |
| Circulation | 55,566,816 | 47,308,232 |
| Veins | 17,595,168 | 17,093,288 |
| Anastomoses | 3,278,012 | 2,784,864 |
| Total | 76,439,996 | 67,186,384 |

The saving is 9,253,612 bytes (12.11%) in the vessel files. The gzip versions
reduce from 46,969,920 to 46,389,045 bytes, a saving of 580,875 bytes (1.24%).
The transfer saving therefore depends on whether the host serves gzip. The overall five-model set is
97,158,372 bytes, retaining the reduced brain candidate from v0.9.118. The
brain and bone GLBs are byte-identical to that release. The original v0.9.117
baseline remains available separately.

Meshopt has distinct index-sequence and triangle-list encodings. Triangle-list
encoding can cyclically rotate a triangle's corners. This release switches a
buffer only when a complete decode reproduces its original index sequence
byte-for-byte and the encoded result is smaller. All 372 rotation candidates
were rejected and their original compressed data retained. A total of 625 index
buffers passed. No new decoder, extension or browser dependency is introduced.

The authoring tool checks every decoded buffer view with the decoder bundled by
Three.js, including all filtered normals. Independent GLTFLoader checks compare
all 1,250 meshes against v0.9.118. Runtime worker checks use the unchanged
v0.9.118 expected-geometry hashes. Source nodes, materials, accessors and scene
transforms are preserved.

Current file hashes, byte sizes, vessel course bindings and DSA container hashes
are rebound. DSA projection recipes, coordinates, injection courses, safety
ranges and the branch graph remain exact. Existing brain anchors and the
anatomical issue register are unchanged.

The deferred-review registry carries forward the exact vessel geometry proofs,
cases and implementation checks. It deliberately retains the old brain asset
requirement: the earlier brain simplification still needs reassessment of any
spatial search exclusions that depended on the unsimplified brain. This vessel
encoding change does not add anatomical acceptance to that prior trial.

Run the compactor and compare an unpacked baseline with:

```sh
node tools/vessel-index-encoding/reencode.mjs INPUT.glb OUTPUT.glb
node tests/vessel-index-encoding/validate.mjs /path/to/inr-anatomy-atlas-v0.9.118
npm run build
```

Rebinding container hashes is required before publishing an isolated re-encoded
GLB. Per-buffer reports and exact source/output hashes are retained under
`anatomy/source/vessel-index-encoding-v0.9.119/`. The final size and validation
receipt is `docs/validation/vessel-index-encoding-v0.9.119.json`.

This reduces storage and transfer. Decoded mesh memory and triangle counts are
unchanged; device-specific rendering speed improvements are not established.
