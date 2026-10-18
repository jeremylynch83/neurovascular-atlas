# Left A4 anterior shaft registration batch 16, v0.9.108

This bounded correction improves the left A4 anterior shaft fit. It moves 896 existing vertices by at most 2.692582 mm, affecting 1,856 physical triangles. All 8,445 original face indices and 4,382 vertices remain. All four native interfaces, totalling 323 shared coordinates, stay fixed. The previous right A4 fit and all 1,249 other named meshes remain exact.

This is partial progress on G05. Residual cortical embedding remains.

## Defined fit and paired measurements

A smooth quintic shear depends only on source Y. Support is Y -46 to -37 mm; the plateau is Y -43 to -40.5 mm. The plateau translates 2.5 mm medially and 1 mm inferiorly. Y stays fixed. Every analytical constant-Y cross-section translates rigidly and the analytical Jacobian determinant is one. The plateau bounds are defined before measurement.

| Matching source/candidate samples | Before | After |
| --- | ---: | ---: |
| Central plateau maximum depth | 1.226825 mm | 0 mm |
| Central plateau inside samples | 1,986 | 0 |
| Complete changed-region maximum depth | 2.522286 mm | 2.522286 mm |
| Complete changed-region inside samples | 10,574 | 5,377 |
| New inside samples | - | 0 |
| Maximum additional depth | - | 0 mm |

There are 12,992 matching samples: face corners, three edge midpoints and centroids of all changed triangles. Repeated shared coordinates are included; these are not independent anatomical observations or defect counts. Signed depth agrees with closed-volume parity above the 0.0001 mm disagreement threshold. Every nearby closed brain/bone target passes the no-new-entry and maximum 0.001 mm depth-regression gate. Nearby open targets pass conservative empty-ball separation.

No sampled embedding remains in the defined plateau. This does not prove continuous tissue clearance. The worst residual depth over the complete changed region remains 2.522286 mm in the transition/end region. Posterior left A4 and wider ACA/callosal registration remain open.

## Native geometry, normals and crossings

All 35,440 tested triangle pairs pass the no-new-crossing gate outside the known closed left middle-anterior cingulate embedding. There are no inherited non-neural crossings in this correction. The 152 closed cortical contact pairs are covered by the paired-depth gate and are not declared cleared.

All 323 source boundary edges and vertices remain fixed. The interfaces are left A3 (64 coordinates), left A5 (64), left paracentral (133) and left short callosal branch (62). Source and candidate bad-edge counts are zero. Coordinate-weld partitions and component counts stay unchanged. Every changed coordinate is checked against all 766 arterial labels to exclude new welds. No original face reverses; face area ratios are 0.989559 to 1.913075.

Flank normals use the inverse transpose of the analytical shear, quantised once to SNORM16. Fixed-vertex and plateau normals remain stored exactly. Independent replay reproduces positions, indices and normal integers byte for byte after integration.

## Export and application checks

GLTFLoader verifies all 599 circulation meshes, exact accepted buffers, every source face index and retained physical-face corner normal. The other 598 meshes in that asset and four other GLBs remain exact, including the previous right A4 repair.

The selected DSA recipe preserves sanitised source index lineage, flips/removals, cap vertices and cap connectivity. It remains closed, oriented and positive-volume. Its volume changes from 65.282745809 to 65.283082038 mm³ (0.000515035%). This small discrete mesh change is distinct from the exact unit-determinant analytical mapping. The 827 other proxy recipes remain exact.

One arterial course is refreshed. All 596 other course entries, selectability, directed connections, graph, vein sites, generator and unaffected edge distances remain exact. Only the selected A4-dependent distance changes.

Full build, all 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. Issue-register copies agree. No full-atlas render was performed.

## Excluded trials and remaining work

Broad and posterior-shifted support intervals deepen existing cortical embedding at their transition. Increasing uniform inferior displacement creates new entry or extra depth anteriorly. Varying inferior displacement still leaves a posterior regression. These trials are excluded. Passing anterior alternatives are recorded, but only the single specified fit is installed.

Wider bilateral A2, ACA/callosal/cortical registration, receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial triangles, the PICA vermian crossing and the separate ILT native interface remain open. No new independent imaging or target segmentation was introduced.

Evidence: anatomy/source/aca-shaft-v0.9.108. Replay tools: tools/aca-shaft-v0.9.108. Machine-readable report: docs/validation/aca-shaft-v0.9.108.json.
