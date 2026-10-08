# ICA / cavernous sinus refinement, v0.9.33

Baseline: final v0.9.32 snapshot with local branch-clearance corrections. This is an anatomical review model.

## Changes

The posterior sinus roof is reduced while its anterior roof and fixed ophthalmic relationships remain close to the accepted baseline. The ICA is not lowered. Arterial surface fairing is limited to 0.055 mm per vertex, preserving calibre and the accepted course. Connected venous surfaces are faired together, with delicate native collars constrained. The venous deformation is damped to half the initial trial amplitude to retain a valid wall.

The roof displacement is intentionally non-uniform: bone apposition, arterial spaces and native connections constrain it. This avoids treating the sinus as a uniformly scaled object. All existing selectable labels and topology are retained.

| Posterior section | Mean upper-surface lowering, right | Left |
| --- | ---: | ---: |
| y=-54 mm | 1.71 mm | 1.74 mm |
| y=-50 mm | 2.02 mm | 1.86 mm |

These are atlas-coordinate measurements of the original upper decile of surface vertices in each section, not patient measurements. Some protected branch corridors remain at their original height.

## Verification

- Complete ophthalmic and superior hypophyseal meshes, their topology and incident parent-wall coordinates are unchanged.
- All 107 documented physical joins pass, including sinus tributaries and the affected arterial branch collars.
- Zero detected non-adjacent intersections on either corrected ICA wall and on the changed regional venous network.
- No detected contacts between the two corrected ICA regions or cavernous sinus labels and retained bone.
- All 30 recorded local arterial branch/sinus contact checks pass.
- Sampled parent-artery/sinus surface gaps are 0.267 mm right and 0.254 mm left.
- No degenerate output triangles; finite positions and unit normals.
- Production build and actual Three.js GLTFLoader/MeshoptDecoder checks pass. Unchanged mesh positions and indices remain exact.

## Review limits

Bone and brain geometry remain fixed. Dural boundaries are estimates, and native lower petrous/canal contacts remain outside this local refinement. Geometry checks are sampled or tolerance-limited and do not establish independent anatomical approval. Comparison renders come from decoded final production assets, with bone cut away for display only.

Detailed evidence is in `anatomy/source/ica-cs-v0933`. Reproduction instructions and the constrained authoring scripts are in `tools/ica-cs-v0933`.
