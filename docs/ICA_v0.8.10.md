# ICA boundary correction, v0.8.10

The cervical/petrous and petrous/cavernous boundaries now follow the two
red lines in Jeremy Lynch’s supplied `image(20261003-205229).png`.
The cervical section extends closer to the lower bend. The petrous section
is shorter and the cavernous section begins lower on the ascending limb.
Corresponding stations are applied to the left reference template.

These are diagram-guided stations on the retained model. The screenshot
was approximately projected against existing colour transitions, bend
shoulders and the upper genu. The marks do not measure the carotid canal
entrance or petrolingual ligament. Localisation and station values are in
`validation/ica-boundary-correction-v0.8.10.json`.

The continuous ICA surface is unchanged: every original triangle position,
normal and vertex attribute is retained. Only ownership among the cervical,
petrous and cavernous sections changes. The paraophthalmic, posterior
communicating, anterior choroidal and terminus sections remain untouched,
as do the ophthalmic, PCom, AChA and A1/M1 origins and their courses.
The corrected vertebral sections from v0.8.9, ACA sections and GUI are retained.

## Retained branch junctions

All branch surfaces and origins remain unchanged, including the welded
caroticotympanic junctions. These small branches retain their note-derived
petrous parents. Their existing axis attachment stations lie approximately
2 mm below the new estimated cervical/petrous station. That small discrepancy
is recorded for anatomical review; it does not justify moving a welded
junction in this boundary-only correction. No tissue-derived carotid canal
entrance or petrolingual ligament is available to resolve that placement.

## One-off authoring checks

- Exact combined ICA triangle/attribute comparison before and after partition.
- Byte-exact attributes and indices for every other circulation mesh including every branch junction.
- Welded caroticotympanic seam vertices remain shared with the ICA.
- Other model assets, GUI sources, descriptions, IDs and relationships retained.
- Actual Three.js GLTFLoader and raycaster checks for all ICA, vertebral and
  ACA sections, including whole-artery focus, highlighting and hiding.
- Local-root and GitHub Pages subpath production builds.

Interaction and renderer checks use fixtures, not a full browser/GPU test.
The marked screenshot and projected ICA were visually inspected.
