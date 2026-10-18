# Local venous native wall repair, v0.9.98

This appends three wall triangles to the basilar plexus with one existing native coordinate/normal copied from the left inferior petrosal sinus. All original source data remain exact. See `docs/LOCAL_VENOUS_BATCH6_v0.9.98.md` for scope and exclusions.

Use a copy of `anatomy/source/local-venous-junctions-v0.9.98` as WORK to preserve packaged evidence. Run from the application root with absolute paths:

- `python3 tools/local-venous-junctions-v0.9.98/repair.py WORK CACHE` replays accepted proposals against retained baselines, verifies byte-exact equality and the combined regional gate; never installs an asset. Authoring dependencies are NumPy and VTK.
- `node tools/local-venous-junctions-v0.9.98/export.mjs WORK SOURCE_GLB OUTPUT_GLB` requires the passing numerical gate, copies original normal integers and exports lossless positions/indices. Historical SOURCE_GLB is the v0.9.97 venous asset, not duplicated in this package.
- `node tools/local-venous-junctions-v0.9.98/verify-export.mjs WORK [OUTPUT_GLB]` needs `WORK/old-venous.glb` from v0.9.97 and checks selected prefixes, native appended data, every other venous mesh and four other assets.
- `python3 tools/local-venous-junctions-v0.9.98/projections.py WORK APP` derives the single refreshed proxy from the retained face lineage. New face orientation is matched to historical DSA sanitisation with a bounded search (at most 12 new faces), then closed/oriented/positive-volume gates apply.
- Preserve v0.9.97 flow as `WORK/old-dsa-flow.json`, run `node tools/build-dsa-flow.mjs --only __no_arterial_changes__` and `node tools/local-venous-junctions-v0.9.98/verify-flow.mjs WORK`. All arterial entries, edges, graph and generator must match. Only the edited vein site is permitted to change; none changes here.

Unchanged remote defects and full anatomical/receiving-lumen acceptance remain open. The retained small-boundary scan records why the other mixed-label component is excluded. Single-label boundaries are never assumed to be wall defects.
