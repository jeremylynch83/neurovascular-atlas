# Integrated venous native wall repair, v0.9.99

This batch scans all 231 venous meshes and installs 39 passing small mixed-label wall patches across 14 labels. See `docs/INTEGRATED_VENOUS_BATCH7_v0.9.99.md` for scope, metrics and exclusions. Every original position, normal and face remains exact. Single-label ports and wider defects remain open.

Use a copy of `anatomy/source/integrated-venous-v0.9.99` as WORK to preserve the packaged evidence. Run from the app root with absolute paths:

- `python3 tools/integrated-venous-v0.9.99/repair.py WORK CACHE` replays explicit accepted proposals against the retained baselines, verifies individual mixed-label boundary ownership and source-prefix retention, requires byte-exact equality, and repeats the combined whole-venous numerical gate. It never installs a GLB. NumPy and VTK are authoring dependencies. The unedited venous labels come from this complete release; decoded baselines are needed only for selected labels/neighbours.
- `node tools/integrated-venous-v0.9.99/export.mjs WORK SOURCE_GLB OUTPUT_GLB` requires passing `native-validation.json`. It preserves original normal integers and copies appended native coordinates/normals without requantisation. Historical SOURCE_GLB is the v0.9.98 venous asset, not duplicated here.
- `node tools/integrated-venous-v0.9.99/verify-export.mjs WORK [OUTPUT_GLB]` needs v0.9.98 `WORK/old-venous.glb` and checks every original selected position/normal/face, appended native attributes, all 217 other venous meshes and all four other assets.
- `python3 tools/integrated-venous-v0.9.99/projections.py WORK APP` refreshes selected DSA recipes from retained source-face lineage. A paired-edge constraint graph propagates historical sanitised DSA orientation to new faces, avoiding an exponential orientation search. Closed/oriented/positive-volume checks remain mandatory.
- Preserve v0.9.98 flow as `WORK/old-dsa-flow.json`, run `node tools/build-dsa-flow.mjs --only __no_arterial_changes__` and `node tools/integrated-venous-v0.9.99/verify-flow.mjs WORK`. All arterial entries, edges, graph and generator must match. Only selected vein sites may change; none changes in this release.

The retained source scan, boundary components, excluded triangulations, individual/fallback reports, accepted proposals and buffer checksums make the selection reviewable. The ordinary automatic repair scanner still refuses malformed source networks. This explicit reviewed batch isolates small components away from all known bad-edge vertices and retains every unchanged source defect.
