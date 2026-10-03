# Vertebral section correction, v0.8.9

The previous V3 station plan started too low on the ascending cervical limb
and ended too high on the cranial limb. Both V2/V3 and V3/V4 boundaries are
now placed against the red marks in the supplied
`image(20261003-204543).png`. V3 is confined to the shorter outer loop;
V2 continues to its lower start and V4 begins at its medial return.
The corresponding reference stations are applied to the left side.

These are diagram-guided stations on the retained model, not measured bone
or dural boundaries. Approximate projection/localisation is recorded in
`validation/vertebral-correction-v0.8.9.json`. Definitions and descriptions
remain those in the supplied notes. V1 and the existing C6-entry station are
unchanged, as are every ACA and ICA section.

For the right template, V3 previously occupied approximately 77 mm of
centreline arc. It now occupies approximately 29 mm, between the marked
upper-cervical exit and the end of the outer loop. These figures describe
the reference model, not patient measurements.

Only V2–V4 triangle ownership changes. No vessel is moved, resampled,
smoothed, capped or altered in calibre. Normals and positions are retained
exactly. Names and IDs are stable. Branch courses and ostia are unchanged;
their segment parents are updated to match the corrected partition.

## Checks

- Exact triangle-position/normal comparison across both vertebral surfaces.
- Every other circulation mesh, including V1 and ACA/ICA meshes, retains
  all original position, normal, colour and index bytes.
- Other model files and GUI sources are byte-identical to v0.8.8.
- Actual GLTFLoader and raycaster checks for every selectable section;
  retained whole-artery focus, highlighting, hiding and batching.
- Updated branch hierarchy and reviewed source-catalogue parent links.
- Production builds for the local root and GitHub Pages subpath.

Renderer and interaction checks use fixtures, not a full browser/GPU test.
The source diagram was visually checked against the projected centreline
and marked boundary locations.
