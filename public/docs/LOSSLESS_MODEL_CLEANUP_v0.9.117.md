# Lossless model cleanup - v0.9.117

This release removes unreachable accessors and their compressed buffer payloads
from three GLBs. It does not re-encode, quantise, simplify, reorder or reconstruct
any active geometry. The bone and anastomosis files remain byte-identical.

| Model set | v0.9.116 bytes | v0.9.117 bytes |
| --- | ---: | ---: |
| All five GLBs | 121,147,832 | 109,177,308 |
| Gzip downloads | 80,366,103 | 73,680,647 |

The saving is 11,970,524 bytes (9.88%) in the model files and 6,685,456 bytes
(8.32%) in their gzip representations. These figures describe anatomy assets,
not the entire source ZIP or total application transfer.

All 1,250 named meshes retain their decoded attributes, vertex IDs, triangle
indices and order, node bindings, materials and transforms. Accessor IDs and
physical compressed-buffer offsets change. Current file hashes, asset sizes,
vessel course bindings, brain anchor bindings and DSA source hashes are updated.
The DSA recipes and flow payloads themselves remain exact. Historical reports
retain their original hashes and conclusions. The current deferred-review
registry is carried forward with the same cases and implementation checks, with
an explicit reference to the geometry-equivalence proof.

The original v0.9.116 release remains the baseline. No canonical coordinates or
normals are lost in this cleanup. No anatomical review status is changed.
The staged loading and interaction code is unchanged from v0.9.116.

`tools/compact_glb.py INPUT.glb OUTPUT.glb` is a repeatable static-GLB compactor.
It fails on unsupported resource types and leaves already compact inputs
byte-identical. Repackaging alone changes asset hashes, so do not publish an
isolated repacked GLB without updating and validating its linked metadata.

To compare another unpacked v0.9.116 baseline against this release:

```sh
npm ci
node tests/model-cleanup/validate.mjs /path/to/inr-anatomy-atlas-v0.9.116
npm run build
npm run dsa:test
```

See `docs/validation/lossless-model-cleanup-v0.9.117.json` for the final validation
receipt, measured file sizes and exact source-to-output asset hashes. Browser
tests use software WebGL and establish functional compatibility; they do not
establish device-specific frame rates.
