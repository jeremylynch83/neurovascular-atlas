# Optional deep-vein authoring replay

These scripts are not part of installation or the app build. They preserve the joined-skin authoring method without bundling intermediate buffers.

The exact final 70 course components and all selected receiver relations are in `anatomy/source/deep-veins-v0.9.27.json`. Copy that JSON to `candidate/courses.json` beside this README. Replaying requires the exact v0.9.26 model assets and decoded baseline mesh positions/indices in `decoded`, with a `meshes.json` containing name/file records. Copy the baseline venous GLB to `baseline/models/venous.glb`. Use the app Three.js loader/MeshoptDecoder to decode the baseline; keep atlas coordinates and exact node names. NumPy, SciPy, VTK and manifold3d are required for authoring only.

Run `work/build.py`, then `work/validate.py` and `work/check_courses.py`. Staged buffers can be applied with `tools/export-deep-veins.mjs`, explicitly supplying the baseline venous GLB as its third argument. The loader check requires the decoded baseline directory and candidate folder. Clinical anatomical review remains separate from these geometric checks. Original reference image pixels and large intermediate skins are omitted.
