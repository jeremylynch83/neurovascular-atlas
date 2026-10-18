# Right A4 shaft registration batch 15, v0.9.107

This is a bounded regional course correction to the right A4 mid-shaft. It moves 1,647 existing vertices by at most 2.507987 mm and changes 3,359 physical triangles without adding or removing any source vertex or triangle. All 8,376 original face indices remain exact. The four native interfaces, totalling 324 shared coordinates, remain fixed.

The fit improves the represented cortical relationship but does not resolve G05 or establish complete anatomical acceptance.

## Defined support and measured outcome

A quintic bump depends only on source Y. Its support is Y -53.5 to -37 mm, with plateau Y -48.5 to -42 mm. The plateau moves 2.3 mm medially and 1 mm inferiorly. Y stays fixed, and every analytical cross-section at constant Y translates rigidly. The analytical Jacobian determinant is one. These bounds define the reported central section before measuring the result.

| Matching source/candidate samples | Before | After |
| --- | ---: | ---: |
| Maximum depth in the complete changed region | 1.715957 mm | 1.339721 mm |
| Maximum depth in the defined central plateau | 1.690410 mm | 0.168717 mm |
| Inside samples in the complete changed region | 14,747 | 4,818 |
| Inside samples in the defined central plateau | 4,538 | 464 |
| New inside samples | - | 0 |
| Maximum additional depth | - | 0 mm |

The 23,513 samples are matched face corners, three edge midpoints and centroids. They include repeated shared vertices and are not independent anatomical observations or counts of defects. Signed-distance results agree with closed-volume parity, with no disagreement above 0.0001 mm. Open nearby brain/bone surfaces pass conservative empty-ball separation. The paired gate permits at most 0.001 mm additional depth; the measured maximum is zero.

Residual embedding remains both centrally and in the transition regions. The whole changed-region maximum depth reduction is smaller than the central-section improvement. The left ACA and both A2 segments retain their previous findings.

## Geometry, normals and native interfaces

All 53,830 tested triangle pairs pass the no-new-crossing gate outside the known closed cortical embedding. There are no inherited non-neural crossing pairs in this accepted correction. The 216 cortical contact pairs are evaluated through the paired-depth gate and are not declared cleared.

Every source face has a positive old/new oriented normal dot product. Face area ratios range from 0.996553 to 1.371897. The DSA proxy volume changes from 64.574615618 to 64.574082773 mm³, a relative change of -0.000825161%. This small discrete mesh difference is distinct from the exact unit-determinant analytical mapping.

All 324 native boundary edges and vertices remain fixed, including interfaces with right A3, right A5, right paracentral and right short callosal branch. Source and candidate bad-edge counts are zero. Coordinate-weld partitions stay unchanged; all 766 arterial labels are checked to exclude new coordinate welds with the moved shaft. Connected-component counts remain unchanged.

Fixed vertex and plateau normals remain stored exactly. Sheared flank normals use the inverse transpose of the analytical Jacobian, followed by a single SNORM16 encoding. The exporter adds no octahedral re-quantisation. Independent replay reproduces positions, indices and normal integers byte for byte.

## Application and export checks

GLTFLoader verifies all 599 meshes in complete-circulation.glb. The accepted buffers, all source face indices and every retained physical-face corner normal are exact. The 598 other meshes in that asset and four other GLBs remain unchanged.

The selected DSA recipe retains exact source index lineage, sanitised flips/removals, projection cap coordinates and cap connectivity. It remains closed, oriented and positive-volume. All 827 other proxy recipes stay exact. One arterial course is refreshed; all 596 other entries, selectability, directed connections, graph, vein sites, generator and unaffected edge distances remain exact. The A4-dependent route distance is updated.

The full build, all 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. No full-atlas render was performed.

## Excluded wider trials and remaining work

Broad A2 movement clears the selected A2 samples but creates new tissue entry or extra depth in neighbouring branches, so it is excluded. A connected left A4-A5 fit improves its parent trunks but worsens attached branch depths. Shortening the branch taper folds the long and short callosal walls. Depth-projected branch points also fold and distort the walls. Those trial results are preserved without installing their geometry.

A bilateral shaft trial is excluded for left-sided extra depth, and the original 2.5 mm medial right trial enters the falx. The accepted 2.3 mm medial and 1 mm inferior right fit avoids those regressions.

Bilateral A2, left ACA, distal ACA/callosal fit, full receiving lumens, Galenic/petrosal/dural/canal findings, the PICA vermian crossing, seven zero-area arterial triangles and the separate ILT interface remain open. No new independent imaging or sulcal target segmentation is introduced. This numerical teaching-model fit is not anatomical certification.

Evidence: anatomy/source/aca-shaft-v0.9.107. Tools: tools/aca-shaft-v0.9.107. Machine-readable report: docs/validation/aca-shaft-v0.9.107.json.
