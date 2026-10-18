# Bilateral A5 shaft registration batch 17, v0.9.109

This batch improves both A5 shafts between existing native branch junctions. It moves 2,069 existing vertices by at most 2.236068 mm, affecting 4,270 physical triangles. All 8,784 source vertices and 16,596 source triangles remain, with every face index exact. All ten native interfaces, totalling 980 shared coordinates, stay fixed. Both previous A4 fits, repaired falcine roots and all 1,248 other named meshes remain exact.

The fit provides partial progress on G05. Transition, proximal and distal cortical embedding remains.

## Defined fit and measurements

Each quintic shear depends only on source Y, with support -80 to -70 mm and plateau -76 to -73 mm. The plateau moves 1 mm medially and 2 mm inferiorly. Y stays fixed, every analytical constant-Y section translates rigidly, and the analytical Jacobian determinant is one. Bounds are defined before measurement.

| Node | Plateau maximum sampled depth | Changed-region inside samples | Changed-region maximum residual depth |
| --- | ---: | ---: | ---: |
| ACA A5 left | 0.244170 to 0 mm | 2,766 to 1,008 | 0.731382 mm |
| ACA A5 right | 0.405084 to 0 mm | 3,595 to 1,260 | 0.957889 mm |

There are 14,980 matched samples left and 14,910 right: every changed-face corner, three edge midpoints and centroid. Shared coordinates repeat and are not independent observations or defect counts. Both plateau inside-sample counts fall to zero (276 left and 574 right before fitting). New inside samples and maximum extra depth are zero on both sides. Signed depth agrees with closed-volume parity above 0.0001 mm; nearby open targets pass conservative empty-ball separation. The regression gate permits no more than 0.001 mm additional depth.

No sampled plateau embedding is not proof of continuous clearance. The changed-region maximum depth remains unchanged at the recorded values above because transition/end embedding remains. The proximal A4/A5 ports, long callosal roots, distal precuneal/falcine region and inferior parietal ports stay fixed. Wider ACA/cortical registration is unresolved.

## Native geometry and shape

All 980 source boundary edges and vertices stay fixed. Left interfaces are A4 (64), falcine branch (101), inferior internal parietal (142), long callosal (71) and precuneal (146). Right interfaces are A4 (64), falcine branch (32), inferior internal parietal (140), long callosal (72) and precuneal (148). Source/candidate bad-edge counts remain zero. Coordinate-weld partitions and connected-component counts are retained. Changed coordinates are checked against all 766 arterial labels, including both final candidates. No original face reverses.

| Node | Source face area ratio | DSA proxy volume, mm³ | Relative volume change |
| --- | ---: | ---: | ---: |
| ACA A5 left | 0.939509-1.844623 | 19.926735555 to 19.926798957 | 0.000318176% |
| ACA A5 right | 0.921471-1.877528 | 19.664384478 to 19.664301831 | -0.000420286% |

Discrete volume differences are distinguished from the exact analytical unit-determinant mapping. Flank normals use the inverse transpose of the analytical Jacobian and one SNORM16 encoding. Fixed-vertex and plateau normals stay stored exactly. Independent replay after integration reproduces positions, indices and normal integers byte for byte.

All 71,934 tested triangle pairs pass the no-new-crossing gate outside known closed cortical embedding. No inherited non-neural crossing pair is present. The 119 remaining cortical contact pairs involve the left and right middle-posterior cingulate bodies and are evaluated by the depth gate; they are not declared cleared.

## Export, application and retained work

GLTFLoader verifies all 599 circulation meshes, both accepted buffers, source face indices and retained physical-face corner normals. The 597 unselected circulation meshes and four other GLBs remain exact, including both A4 corrections and the falcine roots.

The two selected DSA recipes preserve sanitised index lineage, flips/removals, cap positions and connectivity. Both remain closed, oriented and positive-volume. All 826 other recipes match v0.9.108 exactly after the final build. Two courses are refreshed; all 595 unselected courses, selectability, directed connections, graph, vein sites, generator and unrelated edge distances remain exact. Only the selected A5-dependent route distances change.

The full build, 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. All issue-register copies agree. No full-atlas render was performed.

## Excluded trials and remaining work

Superior shifts cause new cortical entry or increased depth. Right medial shifts of 1.5 and 2 mm enter the falx. Those trials are excluded. Passing alternatives are retained as evidence; only the specified 1 mm medial and 2 mm inferior fit on each side is installed. Prior failed broad A2/A4-A5 experiments are not repeated.

Wider bilateral A2, ACA/callosal/cortical registration, receiving lumens, Galenic/petrosal/dural/canal findings, seven exact-zero-area arterial triangles, the PICA vermian crossing and the separate ILT native interface remain open. No new independent imaging or target segmentation is introduced.

Evidence: anatomy/source/aca-shaft-v0.9.109. Replay tools: tools/aca-shaft-v0.9.109. Machine-readable report: docs/validation/aca-shaft-v0.9.109.json.
