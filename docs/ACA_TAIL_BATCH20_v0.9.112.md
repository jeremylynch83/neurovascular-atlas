# Distal left A5 shaft fit batch 20, v0.9.112

This bounded fit reduces left A5/corpus-callosum overlap. It moves 463 existing vertices outward by 0.5 mm and superiorly by 0.5 mm at most, a maximum displacement of 0.707107 mm. All 4,473 vertices and 8,424 original face indices remain. The fit affects 998 physical faces. All five native interfaces and 524 shared coordinates remain fixed: left A4 (64), falcine branch (101), inferior internal parietal (142), long callosal (71) and precuneal (146). All 524 boundary edges/vertices remain fixed, with zero bad edges and unchanged weld partitions and connectivity.

The maximum sampled corpus-callosum depth over the changed region falls from 0.254732698 to 0.194552302 mm. Inside samples fall from 1,317 to 584. These are repeated face samples, not independent anatomical defect counts. Residual transition/attachment overlap remains. This is a partial correction, not whole-label clearance or anatomical acceptance.

## Defined correction and retained geometry

The quintic compact bump has source-Y support [-96.3, -94.3] mm and plateau [-95.7, -95.1] mm. The posterior transition width is 0.6 mm; the anterior width is 0.8 mm. Y stays fixed. Each analytical constant-Y section translates rigidly and the analytical Jacobian determinant is one. Every source face retains positive orientation relative to its original normal.

All 4,010 vertices outside the support retain positions and stored normals exactly. This includes the earlier mid-shaft fit and terminal tip. Both A4s, right A5 (including batch 19 clearance), branch roots and all 1,249 other named meshes remain exact. Changed coordinates are checked against all 766 arterial meshes; no coordinate weld is added. All 21 runtime source files, 1,250 meshes, 1,666 catalogue structures, relationships and asset bindings are retained.

## Tissue and crossing gates

The paired depth gate checks 6,986 matching changed-face corner, edge-midpoint and centroid samples against all nearby brain/bone targets. It finds no new sampled tissue entry, no extra depth and no signed-distance/enclosed-volume disagreement above 0.0001 mm. Open target surfaces require conservative enclosing-ball separation, including the left posteroventral cingulate surface. Its open topology does not support an absolute-inside claim.

The complete changed-face crossing check tests 19,786 triangle pairs and finds zero new non-neural crossings. The remaining 42 closed-target contact triangle pairs are the known residual corpus-callosum overlap and are covered by the paired depth gate.

One native self-contact pair, source faces 1156 and 1222, already exists. Both triangles lie entirely on the rigid plateau. Their positions undergo the same exact [-0.5, 0, +0.5] mm translation and their stored normals remain exact. The two directional records describe one unique pair. This native tessellation issue remains unresolved and is not counted as a new contact or a repaired defect.

## Continuous distal-section clearance

All 1,209 wall triangles whose original vertices have Y <= -95.1 mm are continuously certified outside the complete closed corpus-callosum surface. The section includes the posterior transition and fixed tip. Whole-label clearance is not claimed. In 8,463 matched section samples, inside samples fall from 231 to zero and sampled depth from 0.110128246 mm to zero. Original face-centroid signs agree with enclosed-volume parity.

The enclosing signed-distance ball proof evaluates 3,649 balls and certifies 3,039 leaf triangles, with maximum subdivision depth 5. Every leaf must have signed distance at its centre minus enclosing radius, including the numerical buffer, greater than 0.00001 mm. No unresolved leaf is permitted. Certified leaf area 12.739542256690 mm² covers the original section area 12.739542256690 mm² within the recorded tolerance. The minimum certified margin is 0.000120987796 mm. This is a conservative lower bound, not a measured anatomical clearance.

## Export, shape and application checks

Fixed and plateau normals retain source SNORM16 integers. Flank normals use the inverse transpose of the analytical shear followed by one SNORM16 encoding. Independent replay reproduces accepted positions, normals and indices byte for byte. GLTFLoader verifies all 599 circulation meshes, including 598 unchanged meshes, all accepted buffers and every original source face index. Four other GLBs remain byte-exact.

Physical face-area ratios range from 0.517494 to 2.238545. The DSA proxy volume changes from 19.926798957 to 19.926776156 mm³ (-0.000114423%). The discretised mesh measurement is distinct from the exact analytical unit-determinant mapping.

Only the selected position-only DSA recipe and course are refreshed. Source index lineage, sanitised flips/removals, cap positions/connectivity and native rims remain exact. The proxy remains closed, oriented and positive-volume. All 827 other recipes and 596 other courses remain exact after the final build. Selectability, directed connections, graph, vein sites, generator and unrelated edge distances remain exact.

The full build, 22 repair tests, three clearance tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 triangles, 579 selectable arterial courses and 2,353 closed sections. Issue-register copies agree. No full-atlas render was performed.

## Excluded trials and remaining work

Whole-tail medial/lateral/upward alternatives introduce vessel contacts, extra tissue depth, new entry or open cortical contacts. A narrower anterior transition reverses twelve faces. An earlier posterior support still introduces fifteen open cortical contacts. These are excluded. Keeping the terminal tip fixed removes those contacts while preserving the overlap reduction.

Residual left A5 attachment/transition overlap, one retained native self-contact pair, wider ACA/callosal/cortical registration, receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial triangles, PICA/ACom/native-wall issues and the separate ILT interface remain open. No independent imaging or segmentation was added.

Evidence: anatomy/source/aca-tail-v0.9.112. Replay tools: tools/aca-tail-v0.9.112. Report: docs/validation/aca-tail-v0.9.112.json.
