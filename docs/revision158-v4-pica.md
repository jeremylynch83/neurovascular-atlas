# Revision158: V4 course beside the PICA origins

The local rise and dip in each V4 segment has been replaced by a straighter tubular course. The distal V4 turn towards the basilar artery is retained. Native wall cross-sections were measured from the reviewed closed projection, with a smooth source-derived radius used for the revised shaft. A monotone height profile removes the local tent. The two transition bands are faired locally, with shared interface vertices fixed.

The PICA origins and anterior spinal root attachments follow the corrected parent walls through local cuff interpolation. Distal PICA courses are retained; the short adjoining left P2 cuff follows its P1 attachment. Seven source nodes change. The other 600 main arterial nodes are byte-equivalent in decoded positions and triangle arrays. Skull, brain, veins and independent anastomosis source files are unchanged.

## Verification

- Shared interface positions match exactly in the saved source meshes.
- Seven affected flow entries pass closed projection, safe-range, sampled interior-guide, injection-gate and split-section checks. Previously selectable/full-safe courses retain that status.
- No intersections with the regional occipital or temporal skull surfaces in any affected mesh.
- No PICA P1/P2 self-contacts. Existing tiny V4 triangle overlaps remain; their maximum depth and material-contact count did not increase.
- Production build, catalogue/DSA checks and progressive-loading validation pass. Loading-pack positions, normals and triangle arrays are verified against the authoring meshes.
- The before/after render uses actual saved source positions, with other branches and bone omitted to expose the wall shape.

The deformation-Jacobian bounds describe the continuous course/cuff map. The separate local surface-fairing record gives the additional vertex changes. Source-derived illustrative calibre is retained; these are teaching meshes rather than patient-specific measurements.

The authoring scripts are one-shot operations from revision157. The measured native-section file is retained as provenance. The installer ZIP uses the existing source-package format and includes the complete anatomy assets.
