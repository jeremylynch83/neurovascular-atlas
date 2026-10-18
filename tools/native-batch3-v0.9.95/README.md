# Native attachment batch 3, v0.9.95

Authoring inputs, retained baseline buffers, accepted output buffers and local reports are in `anatomy/source/native-batch3-v0.9.95`. This release changes three arterial labels. It repairs three of four recorded native-interface failures. Wider anatomical review of the 12-segment cohort remains open.

The occipital mastoid source has a closed proximal cap. Clip it at the recorded plane, loft to the unchanged parent opening, then compute the exterior union to remove small local parent overlaps. Remote artificial union caps are discarded. The final native interface has 108 paired edges.

The ILT anterior branch and trunk expose a compound 131-coordinate root. Harmonic fitting uses a 1 mm support and 1 mm authoring limit; measured maximum movement is 0.5260267 mm. All remote native rims and other exact labelled attachments stay fixed. The 64/69 component interfaces include two common triple-junction coordinates.

`reconstruct.py WORK APP CACHE` replays both constructions from the shipped decoded source buffers and `occipital/screened.json`. It requires NumPy, SciPy, VTK and manifold3d 3.5.4. It stages output in `WORK/replayed` and never installs a GLB. Replay physical triangle sets match the accepted construction exactly; order is not required to match.

`preserve_normals.py WORK ilt-root` constructs export buffers in `WORK/candidate`: all retained source face corner SNORM16 values remain exact, duplicate normal seams are retained, and new fixed-root corners copy neighbouring native normals. New internal normals use area-weighted geometry. `validate.py WORK APP CACHE` checks the candidate arrays against the retained baseline and all current scene surfaces. It uses content-addressed caches from `tools/repair`.

`export.mjs WORK SOURCE_GLB OUTPUT_GLB` requires a passing `native-validation.json` and writes lossless compressed positions, indices and unfiltered SNORM16 normals. It does not overwrite the source. `verify-export.mjs WORK [OUTPUT_GLB]` uses GLTFLoader and the pre-export GLB at `WORK/old-complete-circulation.glb` to verify all candidate buffers, retained source corner normals, every other arterial mesh and the four other assets. The large old GLB is deliberately not duplicated in this release; use v0.9.94 for that comparison.

`projections.py WORK APP` refreshes only the three DSA proxy recipes. After integration, regenerate only their flow entries with `build-dsa-flow.mjs --only` and use `verify-flow.mjs WORK` to verify all 594 reused courses, graph, vein sites and generator identity before restoring a complete generator marker. It requires the pre-export flow JSON at `WORK/old-dsa-flow.json`, available in v0.9.94.

The posteromedial outlet is excluded. Wide snap trials overturn more than 1,500 faces. An initial loft trial also has orientation/collision failures. A corrected sidearm orientation fixes its own native topology, but the fixed distal 141-coordinate port lies entirely inside the current sphenoid mesh. A route to it cannot pass this repair's bone-clearance gate. This requires wider distal course and independent canal/bone registration, not a forced connector. The retained source defect remains explicitly recorded.

Closed, oriented target surfaces use compiled VTK point-in-volume samples, with triangle intersection checks in addition. Open/non-manifold tissue targets use conservative surface-separation bounds; absolute volume membership is not inferred. These are local numerical gates, not independent anatomical acceptance.
