# Bilateral anterior A4 shaft registration batch 18, v0.9.110

This batch improves the anterior A4 shafts between the short callosal roots and A3 junctions. It moves 1,623 existing vertices, affecting 3,377 physical triangles. All 8,730 source vertices and 16,821 original face indices remain. All eight native interfaces, totalling 647 shared coordinates, stay fixed. Earlier A4 fit regions at source Y <= -37 mm retain exact positions and stored normals. Both A5 fits, falcine roots and all 1,248 other named meshes remain exact.

Residual cortical embedding remains. This is partial progress on G05.

## Defined fit and paired measurements

Each quintic shear depends only on source Y, with support -35 to -27 mm and plateau -32.5 to -30 mm. The left plateau moves 2.3 mm medially and 1 mm inferiorly, with maximum displacement 2.507987 mm. The right moves 1.5 mm medially and 1 mm inferiorly, maximum 1.802776 mm. Y stays fixed. Every analytical constant-Y section translates rigidly and the analytical Jacobian determinant is one. Bounds are defined before measurement.

| Node | Plateau maximum sampled depth | Changed-region inside samples | Changed-region maximum depth |
| --- | ---: | ---: | ---: |
| ACA A4 left | 2.115695 to 0.546547 mm | 7,669 to 3,387 | 2.376648 to 2.376648 mm |
| ACA A4 right | 1.638385 to 0.091173 mm | 5,553 to 1,221 | 1.638385 to 1.132489 mm |

There are 11,802 matched samples left and 11,837 right: each changed-face corner, three edge midpoints and centroid. Shared coordinates repeat and are not independent observations or defect counts. Plateau inside samples fall from 3,526 to 1,028 left and 3,185 to 186 right. New inside samples and maximum extra depth are zero on both sides. Signed depth agrees with closed-volume parity above 0.0001 mm. The paired gate permits at most 0.001 mm additional depth.

Both plateaus retain sampled embedding. The left changed-region maximum depth remains unchanged; the right maximum improves. Native branch roots and remote course regions stay fixed, so this is not complete ACA/cortical registration or continuous closed-volume clearance certification.

## Open-surface clearance proof

The original first-corner enclosing balls are inconclusive near the superior frontal surfaces, with lower-bound margins -0.085902 mm left and -0.001584 mm right. A negative lower bound is not a measured penetration. Centring each enclosing ball on its triangle centroid gives conservative lower-bound margins 0.185838 mm left and 0.155061 mm right. Every changed triangle is certified, with complete area coverage and no subdivision required on these real-data cases.

The bound uses the fact that distance to a surface is 1-Lipschitz: distance from ball centre to the target minus a radius containing all triangle vertices bounds separation for the whole convex triangle. The radius includes a numerical buffer. Every certified margin must exceed 0.00001 mm. If a centred ball remains inconclusive, clearance.py subdivides only that triangle into four midpoint children. Unresolved leaves, contact or exhaustion of the limit fail. Certified leaf areas and unresolved areas must sum to original triangle area. This does not infer inside/outside membership for open surfaces.

Three analytic plane tests independently cover a near parallel triangle needing subdivision, a crossing triangle and a touching triangle. Only the separated case passes. All three tests pass.

## Native geometry, normals and shape

All 647 source boundary edges and vertices stay fixed. The four interfaces on each side are A3, A5, paracentral and short callosal. Source and candidate bad-edge counts remain zero; coordinate-weld partitions and component counts stay unchanged. Changed coordinates are checked against all 766 arterial labels, including both final candidates. No original face reverses.

| Node | Source face area ratio | DSA proxy volume, mm³ | Relative volume change |
| --- | ---: | ---: | ---: |
| ACA A4 left | 0.952937-2.169173 | 65.283082038 to 65.283141779 | 0.000091511% |
| ACA A4 right | 0.961697-1.761395 | 64.574082773 to 64.574211054 | 0.000198657% |

The small discrete volume differences are separate from the exact analytical unit-determinant mapping. Flank normals use the inverse transpose of the analytical shear and one SNORM16 encoding. Fixed-vertex and plateau normals remain exact. Independent replay after integration reproduces positions, indices and normal integers byte for byte.

All 51,812 tested triangle pairs pass the no-new-crossing gate outside known closed cortical embedding. There are no inherited non-neural crossings in this correction. The 251 residual cortical contact pairs involve the left and right middle-anterior cingulate bodies and are covered by the paired-depth gate; they are not declared cleared.

## Export and application checks

GLTFLoader verifies all 599 circulation meshes, both accepted buffer sets, every source face index and retained physical-face corner normals. The 597 unselected meshes and four other GLBs remain exact. This includes both A5 fits, falcine roots and all PICA/ACom meshes from the excluded trials.

The two selected DSA recipes retain sanitised source index lineage, flips/removals, cap coordinates and connectivity. Both remain closed, oriented and positive-volume. All 826 other recipes match v0.9.109 exactly after the final build. Two courses are refreshed; all 595 unselected courses, selectability, directed connections, graph, vein sites, generator and unrelated edge distances remain exact. Only the selected A4-dependent route distances change.

The full build, 22 repair tests, three clearance tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. Issue-register copies agree. No full-atlas render was performed.

## Excluded reconstruction trials and remaining work

PICA fixed-boundary retriangulation and coupled vermian/tonsillar wall trials fail strict crossing gates. Straightening a short shared seam by at most 0.001623 mm also fails because of neighbouring contacts. No PICA coordinate, normal or index change is installed. The recorded PICA vermian crossing remains open and requires a wider native-junction reconstruction.

All 132 bounded three-dimensional ACom port disk triangulations fail the crossing gate; neither that patch nor its proposed zero-face removals is installed. A right anterior A4 medial displacement of 2.3 mm enters the falx and is excluded. The accepted right displacement is 1.5 mm medially.

Wider bilateral A2, ACA/callosal/cortical registration, full receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial triangles and the separate ILT native interface remain open. No new independent imaging or target segmentation is introduced.

Evidence: anatomy/source/aca-shaft-v0.9.110. Replay tools: tools/aca-shaft-v0.9.110. Machine-readable report: docs/validation/aca-shaft-v0.9.110.json.
