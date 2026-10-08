# Cavernous sinus surface repair, v0.9.34

v0.9.33 had conspicuous ragged windows and surface debris around the cavernous sinuses. A closed mesh and zero detected self-intersections were insufficient acceptance criteria. The preceding small-artery clearance subtraction carved a combined, capped branch network out of the venous volume and damaged the chamber wall.

## Repair

The compact chamber volume is restored and united with the existing tributaries. A separate primary ICA channel is retained. The joined wall is remeshed, faired and partitioned into selectable structures; native remote venous collars are grafted back. Shared surface normals are calculated on the welded network. Small label islands and numerical slivers are removed.

The repair does not subtract the combined capped small-branch network. Small arterial branches can meet or cross the wall at their exit points, rather than being surrounded by artificially widened clearance windows. These contact points need anatomical review; they are not treated as failed surface integrity.

Only the venous GLB changes. The ICA, ophthalmic origins, all arterial models, bone and brain retain their v0.9.33 geometry. The compact posterior chamber shape remains reduced, although local wall reconstruction changes its surface.

## Verification

- Each cavernous sinus label has one connected component.
- No unmatched edges on either sinus in the joined venous network.
- No degenerate sinus triangles.
- All twelve main tributary connections share mesh vertices with the corresponding sinus.
- No detected non-adjacent intersections in the checked regional venous network.
- No detected sinus contacts with the primary ICA wall or adjacent skull-base bone.
- Three.js GLTFLoader / MeshoptDecoder returns exactly the intended positions and indices, with unit normals.
- Production build and anatomy validation pass.

The opaque before/after images in `review-renders/ICA_CS_surface_repair_*.png` use decoded production geometry and identical cameras. They show lateral, oblique and AP views. No display-only repair is applied.

These are mesh integrity checks and model comparison renders, not anatomical certification or a claim of full interactive browser QA. Native lower petrous/canal geometry remains outside the repair. Historical v0.9.32/v0.9.33 checks are retained for provenance and do not certify this revision.

Authoring scripts are in `tools/ica-cs-v0934`. Decode the v0.9.33 assets into its `decoded` directory, then run `repair.py`, `join_normals.py`, `validate.py`, `clearance.py`, `check_venous.py`, `prepare_export.py`, `export.mjs`, `finalise.py`, the production build and `check_export.mjs`. Decode final assets into `exported` before running `render.py`. The intermediate grids and buffers are omitted from the release ZIP.
