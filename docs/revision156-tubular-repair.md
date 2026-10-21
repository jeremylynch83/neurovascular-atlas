# Revision156: ophthalmic and ICA tubular repair

The bilateral main ophthalmic and adjacent ICA surfaces are corrected in the source meshes and regenerated lossless loading packs. The earlier local fitting had compressed and stretched their walls.

Native pre-fitting walls were recovered by inverting the recorded revision146 deformation. A wider smooth displacement carries the ICA near the ophthalmic origin. The ophthalmic shaft follows its fitted course with rotated radial offsets, avoiding the former vertex-by-vertex shear. The proximal transition was adjusted until the rounded walls cleared the sphenoid.

Original triangle topology and the shared origin interfaces are retained. The ECA skull-base courses, anterior cavernous MMA branches and recurrent ophthalmic courses retain revision155 geometry, with local shared-cuff adjustments where required. Independent anastomosis cuffs follow the connected parent surfaces. The skull and application controls are unchanged.

## Verification

- Source atlas validation and production build.
- Actual source-mesh renders, with isolated vessels to expose the wall shape. Other branches and bone are omitted from these views; open branch ports remain visible.
- Bilateral cavernous ICA, paraophthalmic ICA and main ophthalmic triangle-contact checks: no new self-intersections, and no sphenoid intersections. The right ophthalmic mesh retains its pre-existing approximately 0.006mm local triangle overlap.
- Shared parent/child interface audit in `revision156-junctions.json`.
- Closed DSA projection surfaces, sampled interior guide stations, injection gates and split sections for the affected courses in `revision156-flow-validation.json`. Previously full safe ranges are required to remain full.
- Final recurrent ophthalmic and foramen rotundum checks in `revision156-local-clearance.json`.

The intermediate whole-network comparison found inherited submillimetre triangle overlaps outside the main repair. In the distal right ICA posterior-communicating segment, the maximum measured local overlap changed from approximately 0.011 to 0.019mm. This comparison is distinct from the zero-new-contact result for the six principal repaired meshes.

The sampled deformation bounds were authoring diagnostics, rather than direct lumen calibre measurements. Subsequent local-cuff passes supersede the earlier full-transport diagnostics for restored branches. This remains a reference-guided teaching reconstruction.

No pages, interaction controls, progressive-loading priorities, introductory text or progress-bar behaviour are changed.
