# Arterial exact-zero-area cleanup, v0.9.104

This removes 384 exact-zero-area source triangles across 86 arterial meshes. Positions, stored normals, positive-area source faces and connected-component counts remain exact. It clears 395 invalid native coordinate edges without creating a new boundary or bad edge. This is source topology cleanup; regional anatomical acceptance remains false.

Run from the app root using absolute WORK and CACHE paths. Copy anatomy/source/arterial-zero-area-v0.9.104 to WORK before replaying to preserve the recorded evidence.

- scan.py NEW_WORK CACHE scans all 766 arterial meshes. It filters candidate faces numerically, then proves zero area using exact rational arithmetic on the stored binary coordinates. NEW_WORK must be fresh.
- select.py WORK CACHE restores decoded source baselines and starts with all 453 source zero-area triangles. It conservatively retains every active deletion contributor to a local or global constraint that would introduce a boundary or bad edge, repeating until stable. The selected 384 deletions pass; 69 faces are guarded. This deterministic monotone procedure is not exhaustive and does not establish that alternative safe subsets or explicit repairs are impossible.
- cleanup.py WORK CACHE proves every selected deletion exactly zero-area, retains all other indices in source order, independently recounts all 596 affected edges against every arterial mesh, and writes replayed buffers. Existing accepted buffers must match byte for byte. It never installs a GLB.
- export.mjs WORK SOURCE_GLB OUTPUT_GLB appends compressed index accessors only. Original POSITION and NORMAL accessors are reused verbatim. The historical source is v0.9.103 complete-circulation.glb.
- verify-export.mjs WORK [OUTPUT_GLB] requires WORK/old-complete-circulation.glb. GLTFLoader checks all 599 meshes in that asset, exact retained indices, all position/normal streams, 513 unedited meshes and four other unchanged model assets.
- projections.py WORK APP refreshes only the 86 selected source-face recipes and rebuilds caps, requiring closed, consistently oriented positive-volume proxies.
- Preserve v0.9.103 dsa-flow.json as WORK/old-dsa-flow.json, regenerate only the IDs listed in selected-course-ids.json with tools/build-dsa-flow.mjs --only, then run verify-flow.mjs WORK. The 511 unselected arterial courses, selectable status, graph, vein sites, generator and directed connections must remain exact. Edge distances between unselected nodes must remain exact.

Historical GLBs are not duplicated in the evidence folder. NumPy and VTK use the existing authoring environment. Native edge checks use exact coordinate welding, preserving all stored vertices. Zero-area point/line artefacts are removed; every positive-area triangle remains. Existing disconnected components, registration issues, overlaps and receiving-lumen work remain on the issue register. No whole-atlas render was performed for this bounded cleanup.
