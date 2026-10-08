# ICA surface smoothing v0.9.39

Based on v0.9.38. Rebuilds the petrous/cavernous/paraophthalmic ICA surfaces and the adjoining ophthalmic, superior hypophyseal, inferolateral and meningohypophyseal branch junctions on both sides. The meningohypophyseal stem and its four proximal branch necks are reconstructed together. All 22 named surfaces remain selectable.

One continuous implicit surface is partitioned into the existing labels, then grafted onto the native distal surfaces. A local ring selection fixes the prior distant tentorial collar error. Consistent outward face orientation and shared surface normals remove shading seams; the normals blend into the retained native segments over 0.6 mm. The short petrous collars are locally rounded. Ophthalmic ostium centroids match the original positions to within 0.000001 mm after float32 export; their individual ostial vertices have been remeshed.

## Validation

- Each bilateral cohort is one connected surface, with zero non-manifold edges.
- All native outer boundary edges are preserved exactly.
- No ICA/cavernous sinus wall contacts in the checked region.
- No intersections involving changed triangles in the checked region.
- Existing lower petrous bone contacts are retained outside the rebuilt surface.
- The check also detects retained distal branch self-intersections: 177 on the right and 97 on the left. These occur in retained native branch triangles and are not closed by this local ICA junction repair. The entire atlas has not passed a global intersection or anatomical accuracy gate.

Positions and indices are checked against the actual Three.js GLTFLoader output. The production build validates the structure catalogue and course metadata. Bone, brain, venous geometry, vein/artery colours, startup vein visibility and author credits are retained from v0.9.38.

## Reproduction

The modelling scripts require NumPy, SciPy and VTK. Decode the v0.9.38 arterial baseline into `decoded` and retain its exact GLB in `baseline`, then run `repair.py`, `restore_origins.py`, `validate.py`, `selfcheck.py`, `decode_normals.mjs`, `orient_surfaces.py`, `export.mjs`, `finalise.py`, the production build and `check_export.mjs`. The input archive and large intermediate buffers are excluded from the release. The JSON evidence and matched lateral/oblique renders are included.

This is a reference model for expert anatomical review. No vessel course redesign or new anatomical claim is introduced.
