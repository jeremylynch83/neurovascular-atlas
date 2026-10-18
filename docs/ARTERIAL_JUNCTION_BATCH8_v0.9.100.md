# Arterial junction batch 8, v0.9.100

The scan covers all 766 arterial meshes: 599 in complete circulation and 167 in the communicating-branch asset, with 7,181,394 source triangles in v0.9.99. Fifteen passing mixed-label native wall gaps are closed across five meshes using 53 triangles and 23 appended copies of existing native coordinates/normals. Every original position, normal integer and face remains exact. No existing vertex moves and no new world coordinates are introduced. Total added wall area is 0.004119 mm²; the largest accepted patch spans 0.161852 mm. These small surface gaps are distinct from the larger unresolved anatomical defects.

| Native junction | Small gaps closed | Added triangles |
| --- | ---: | ---: |
| Left PCA P2-P3 / anterior inferior temporal | 4 | 8 |
| Left medial posterior choroidal / PCA P2-P3 | 8 | 32 |
| Right A2 / anterior communicating | 1 | 2 |
| Right V3 / V4 | 1 | 9 |
| Right A1 / terminal ICA perforator 1 | 1 | 2 |

The affected native neighbourhood boundary count falls from 5,277 to 5,194. Its eight pre-existing bad edges remain unchanged, with none added. All 620 potentially intersecting new-face triangle pairs pass, alongside the strict local tissue-clearance gates. Existing remote contacts are not counted as resolved.

## Global edge gate and scan efficiency

Each source mesh is scanned independently, and exact opposite boundary edges are cancelled across labels. This avoids concatenating all 7.18 million source faces. Each loop has its own boundary-label ownership, so a single-label port is not filled merely because it touches a mixed-label component. Known bad-edge vertices, large boundaries and unorderable loops are retained.

Boundary cancellation alone does not detect an additional internal edge in another label. A separate gate therefore measures actual source triangle incidence for every proposed coordinate edge against all 766 arterial meshes. Five of 48 triangulated proposals fail this check before local geometric validation. Every one of the 121 coordinate edges affected by the accepted patches ends with exactly two opposite incidences. Eighty-three native boundary edges are closed globally. No added edge touches a source bad edge or creates a third incidence. The same global gate passes after independent post-integration replay.

Of the 43 globally eligible proposals, 15 pass the local crossing/tissue/native-topology gates. Others, including tissue-embedded A1/M1 candidates and crossing PICA/SCA alternatives, are excluded. Non-simple/degenerate triangulations are deferred without repeating earlier fan searches. Larger pericallosal, skull-base and receiving-lumen reconstruction remains separate work.

## Export and app checks

GLTFLoader verifies all 599 meshes in the changed asset, including the 594 unchanged meshes and every original selected attribute/index prefix. All four other GLBs are byte exact, including all venous and communicating-branch geometry. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures and relationships/asset bindings are retained.

The five edited DSA proxy recipes use source-face lineage and paired-edge orientation propagation and remain closed, oriented and positive-volume. Five arterial courses are refreshed; 592 other course entries remain exact. Directed connections, catalogue graph, vein sites, generator and unaffected edge distances remain unchanged. Selected courses retain their original selectability. Only the five refreshed sources have changed edge-distance data.

The full build, 19 repair tests and DSA checks pass: 828 closed/oriented proxies with 8,971,508 triangles, 579 selectable arterial courses and 2,353 closed sections. Post-integration replay reproduces every accepted buffer byte for byte and reruns both local and global gates. No full-atlas render is used for these bounded append-only native wall patches.

## Remaining work

Whole-atlas anatomical acceptance remains false. Bilateral pericallosal/cortical registration, full receiving lumens, Galenic/petrosal/dural/canal fitting, remote topology defects and the separate ILT posteromedial native interface remain open. Right V3 still has its three original components. The local A2/communicating and A1/perforator wall closures do not resolve the wider G05/G06 defects.

Evidence: `anatomy/source/arterial-junctions-v0.9.100`. Tools: `tools/arterial-junctions-v0.9.100`. Report: `docs/validation/arterial-junctions-v0.9.100.json`.
