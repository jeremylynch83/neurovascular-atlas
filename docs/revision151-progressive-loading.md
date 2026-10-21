# v0.9.151: progressive geometry loading and build reuse

## Delivered behaviour

The viewer uses 13 generated arterial packs in a fixed sequence: starter circulation, main intracranial branches, smaller branches grouped by region and side, then anastomoses. The original skull, vein and brain assets follow in that order. Their existing visibility defaults remain unchanged: skull ghosted, arteries visible, veins and brain off.

The starter includes both common carotids, external carotid trunks, all 14 ICA segments, all eight vertebral segments, basilar, A1, M1, P1, anterior communicating and posterior communicating arteries. It becomes interactive after an actual successful scene draw. Only then do deferred downloads begin. Selection can wait for geometry, but never changes the download order.

The initial explanation, error fallback and retry remain outside React. Existing AP skull framing uses generated skull bounds instead of waiting for skull geometry. Later installation does not reframe the camera. Layers shows prepared geometry counts and existing per-structure loading/retry indicators, separately from visibility. DSA remains gated on vascular geometry and its existing metadata preparation.

## Reused implementation

- `StagedLoader`, the geometry worker, bounded preparation packets and interaction-aware installation slots are retained.
- Complete source GLBs, full anatomical catalogue and structure-to-source bindings remain authoritative. All source model files are byte-identical to v0.9.150.
- `build-loading-packs.py` copies existing meshopt payloads and accessor/node information. It performs no geometry simplification, quantisation or re-encoding. It rejects unsupported scene dependencies explicitly.
- Both a source-level cache and per-pack dependency hashes are used. Per-pack hashes ignore unrelated source buffer offsets and accessor numbering. Unchanged packs keep the same bytes and URLs after another branch changes.
- Generated packs and their index are included with the source release. Standard builds regenerate missing/stale packs automatically.
- Existing Three.js BatchedMesh code now appends across packets into bounded allocations, up to 250,000 vertices and 1,500,000 indices, with larger individual meshes accommodated. It retains individual picking/ghosting meshes and does not resize or repack existing batches. Per-instance visibility prevents a newly hidden vessel from hiding earlier vessels. Browsers without native multi-draw retain individual rendering.
- Gzip outputs are cached by content in `.build-cache/gzip`, outside Vite's cleaned distribution. The cache is disposable and excluded from releases. Compression level and output semantics are unchanged.

Packing does not alter the anatomical bindings used by DSA. Existing source hashes, flow graph checks and course/surface metadata remain authoritative; no projection or flow regeneration is necessary for a packaging-only change. The existing incremental authoring helper `tools/foramina/refresh-dsa.mjs` remains available. A pre-existing limitation remains: arbitrary new projection-surface regeneration refers to a `tools/build-dsa-surfaces.mjs` which is absent from this source release. This release does not add or claim a replacement surface-authoring algorithm.

## Validation and measurements

See the accompanying revision151 JSON reports for exact measurements and checks. Every one of the 774 packed arterial meshes has identical decoded attributes, triangle indices and world transforms. All 1,258 geometry structures have exactly one download-plan assignment. All 1,730 catalogue structures retain descriptions, aliases, landmarks, focus dependencies and relationships; all 15 preset/side DSA comparisons pass.

The actual loader was exercised for starter-only completion, fixed order despite selection, bounded installation, background completion, startup failure, background failure/retry and disposal. CPU scene fixtures exercise the actual engine material, clipping, picking and camera-preservation methods, plus append batching and cross-packet visibility. These fixtures do not replace a GPU test.

The initial required GLB payload falls from 94,615,132 to 6,452,632 bytes, a 93.2% reduction. With the generated gzip files, the comparison is 70,373,399 to 4,976,029 bytes. The complete packed arterial payload is 71,279,744 bytes versus 77,109,300 bytes of original arterial files, because unused source buffer data are omitted. Source GLBs remain included for editing and compatibility; the browser does not download those original arterial files during normal packed loading.

Decode timings are a single controlled Node run, without network, worker transfer or GPU uploads. Build benchmarks cover clean generated outputs, an unchanged rebuild and a temporary 0.01 mm translation of one illustrative anastomosis, followed by exact source restoration. The anastomosis is excluded from DSA, so this does not measure flow regeneration after editing an injection vessel.

A cloud-browser check confirmed that the explanation and retry remain available when WebGL cannot start. That browser does not support WebGL. Successful GPU rendering, first interactive browser timing, full browser loading time, frame rates and GPU memory were therefore **not measured**. Smaller startup payloads are not a demonstrated Core Web Vitals or SEO ranking result. Bounded batches trade additional draw submissions for bounded incremental uploads; measure the final scene on supported desktop/mobile GPUs.

## Build and edit

```sh
npm ci
npm run build
npm run web:loading
npm run web:validate
npm run web:startup
```

Continue editing the complete source models and their existing anatomical metadata. Do not edit generated packs. The normal build performs full source validation, pack generation, viewer catalogue generation, existing DSA dependency checks, TypeScript compilation, Vite and cached precompression.

Optional repeatable benchmark, which restores the exact source bytes before finishing:

```sh
python3 tools/benchmark-loading-builds.py
```

Browser performance entries include `atlas-startup` after the first successful scene draw, `atlas-full-loading` after all geometry has been installed, `atlas-download-decode` per asset and `atlas-geometry-install` per packet. The full-loading mark describes installed geometry, including hidden structures, rather than a GPU draw of every hidden structure.

No deployment was performed. Build output in `dist` is the deployment directory; this ZIP contains the source and generated packs.
