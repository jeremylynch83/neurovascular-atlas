# Distal right A5 fit batch 19, v0.9.111

This batch clears two recorded right A5/cortical contact pairs by fitting the terminal shaft up to 1 mm medially. It moves 408 existing vertices and affects 851 physical triangles. All 4,311 vertices and all 8,172 source triangles retain their original face indices. Every native attachment remains fixed, including five interfaces and 456 shared coordinates. Earlier A5 fit regions, both A4 fits, the left A5, falcine roots and all 1,249 other named meshes remain exact.

The specific cleared pairs are right A5 with the right posterior dorsal cingulate body and right posteroventral cingulate body. Other ACA/cortical embedding and wider G05/G06 remain open.

## Defined correction

A quintic ramp begins at source Y -96.7 mm and reaches full 1 mm medial translation at Y -97.7 mm. The terminal tail beyond that point translates rigidly. There is no Y or Z displacement. The generic compact-bump posterior bounds -120/-110 mm are beyond the whole source mesh, so no posterior fade acts on any source vertex. Y stays fixed; each analytical constant-Y section translates rigidly and the analytical Jacobian determinant is one.

All source positions and stored normals at Y >= -96.7 mm are independently checked exact. This includes all five native interfaces and the earlier mid-shaft fit. All 456 source boundary edges/vertices remain fixed, bad-edge counts remain zero, weld partitions and connected components remain unchanged, and changed coordinates are checked against all 766 arterial meshes. No original face reverses.

## Whole-label cortical clearance

| Complete A5 wall versus target | Maximum sampled depth before | After | Inside samples |
| --- | ---: | ---: | ---: |
| cingulate-gyrus-and-sulcus-posterior-dorsal-part.right | 0.254747 mm | 0 mm | 569 to 0 |
| cingulate-gyrus-posteroventral-part.right | 0.932321 mm | 0 mm | 2,741 to 0 |

Each complete-label comparison uses 57,204 matched face-corner, three-edge-midpoint and centroid samples. Repeated coordinates are included, so these are not independent anatomical observations or defect counts. The changed-region gate separately checks 5,957 matching source/candidate samples against every nearby brain/bone target, with no new inside samples, no additional depth, and signed-distance/enclosed-volume agreement.

Continuous separation of the whole A5 wall from both specified closed target surfaces is additionally proved using enclosing signed-distance balls over every physical triangle. The ball-centre signed distance minus its enclosing radius, including a numerical buffer, must exceed 0.00001 mm. Only inconclusive triangles are subdivided into four midpoint children. Every leaf must pass and leaf areas must cover the original wall area. Unresolved leaves or exhaustion of the limit fail. Original face-centroid signs are independently checked by enclosed-volume parity, with no disagreement above 0.0001 mm.

| Target | Balls evaluated | Certified leaf triangles | Maximum subdivision depth | Minimum certificate margin |
| --- | ---: | ---: | ---: | ---: |
| cingulate-gyrus-and-sulcus-posterior-dorsal-part.right | 8,640 | 8,523 | 2 | 0.000029615 mm |
| cingulate-gyrus-posteroventral-part.right | 8,832 | 8,667 | 2 | 0.000074226 mm |

Every one of the 8,172 source wall triangles is covered for each target. The candidate wall area is 100.137774595 mm², and the certified leaf areas agree within the recorded tolerance. These margins are conservative mathematical lower bounds, not measured physiological clearances. The proof concerns only these two closed targets and the represented vessel wall, not whole-atlas anatomy or lumen certification.

## Crossings, normals and shape

All 15,093 checked changed-face triangle pairs pass the crossing gate. There are no new non-neural crossings, inherited non-neural crossings or closed cortical contact pairs in the fitted region. Neighbouring PCA splenial, pericallosal-splenial and Galenic meshes remain unchanged.

Fixed-vertex and fully translated plateau normals retain their original SNORM16 values. Flank normals use the inverse transpose of the analytical shear and one SNORM16 encoding. The exporter adds no octahedral re-quantisation. Independent replay after integration reproduces positions, indices and normal integers byte for byte.

Source face-area ratios range from 0.527376 to 2.289546. DSA proxy volume changes from 19.664301831 to 19.664403499 mm³, a relative change of 0.000517016%. This small discrete mesh difference is distinct from the exact unit-determinant analytical mapping.

## Export and application checks

GLTFLoader verifies all 599 circulation meshes, exact accepted buffers, every source face index and retained physical-face corner normals. The 598 unselected circulation meshes and four other GLBs remain exact. All previous A4/A5 fit regions are independently retained.

The selected position-only DSA recipe keeps exact sanitised source index lineage, flips/removals, cap vertices and connectivity. All cap rims remain fixed. The proxy remains closed, oriented and positive-volume; all 827 other recipes match v0.9.110 exactly after the final build. Only one course is refreshed. All 596 other courses, selectability, directed connections, graph, vein sites, generator and unrelated edge distances remain exact. Only the selected A5-dependent distance changes.

The full build, 22 repair tests, three clearance tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. Issue-register copies agree. No full-atlas render was performed.

## Screened alternatives and remaining work

The broader medial fit starting at Y -95.3 mm clears the cortex but intersects splenial vessels. Other broad poses introduce vascular contacts, tissue regressions or reversed faces and are excluded. Later transition starts at -96.95 and -96.8 mm pass safety gates but retain cortical embedding. The chosen -96.7 to -97.7 mm transition clears both target pairs while avoiding the neighbouring vessels.

Right middle-posterior cingulate embedding, other bilateral ACA/callosal/cortical registration, full receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial triangles, PICA/ACom/native-wall issues and the separate ILT native interface remain open. No new independent imaging or target segmentation is introduced.

Evidence: anatomy/source/aca-tail-v0.9.111. Replay tools: tools/aca-tail-v0.9.111. Machine-readable report: docs/validation/aca-tail-v0.9.111.json.
