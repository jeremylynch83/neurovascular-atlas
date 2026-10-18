# Exact-zero-area source cleanup batch 10, v0.9.102

The scan covers all 231 venous meshes. It finds 24 exact-zero-area triangles across four labels, then removes 21 safe faces. Every deleted triangle is confirmed to have exactly zero cross product using rational arithmetic on the stored binary coordinates. No small-positive-area face is deleted under an epsilon rule.

| Mesh | Zero-area faces removed | Per-label bad edges | Per-label boundary edges |
| --- | ---: | ---: | ---: |
| vein.anterior_spinal | 11 | 14 -> 3 | 97 -> 86 |
| vein.inferior_ophthalmic.left | 2 | 3 -> 0 | 45 -> 45 |
| vein.pterygoid_plexus.left | 4 | 9 -> 6 | 181 -> 181 |
| vein.pterygoid_plexus.right | 4 | 7 -> 1 | 166 -> 166 |

Every vertex position, normal and retained source face index is exact. All positive-area triangles remain in their original order, with no movement, new face or surface-area loss. The exporter reuses original position/normal accessors verbatim and appends only compressed index accessors. GLTFLoader verifies all 231 venous meshes, including all attributes, exact retained faces and the 227 unedited meshes. All four other GLBs are byte exact.

## Native topology and guarded exclusions

The 40 affected coordinate edges are independently counted against actual triangles in every named venous source mesh. Affected global bad edges fall from 26 to 3, clearing 23 invalid edges. Eleven zero-area boundary artefacts disappear. No new boundary edge or bad edge is introduced, either within an edited label or globally. This is source-topology cleanup, not 23 separate anatomical defects or a new receiving-lumen reconstruction.

The recorded selection enumerates safe per-label subsets, keeps up to 32 leading options plus no-op, and checks 3,432 combinations against full venous incidence. It prioritises removal of global bad edges, per-label bad edges, exact-zero-area faces and boundary artefacts. This is a bounded explicit selection, not an exhaustive whole-atlas optimiser. Independent replay verifies the accepted deletion list rather than trusting the selection report alone.

Two anterior-spinal and one left-pterygoid exact-zero-area triangles remain. Removing them would expose new native boundaries. They need local retessellation, so they are retained explicitly. Other near-degenerate triangles with positive area are also retained. Existing source components do not merge: the left inferior ophthalmic and left pterygoid labels retain two and three components respectively.

Because no positive-area face moves or is added, this deletion cannot introduce new surface crossings or tissue penetration. Existing physical contacts and regional registration findings remain unresolved. All original exact attachment coordinates and normals remain present.

## Integration and verification

Four DSA recipes are refreshed from retained source-face lineage and remain closed, oriented and positive-volume. All 597 arterial course entries, arterial edges, catalogue graph, vein-site data and generator remain exact. The complete build, all 22 repair tests and DSA validation pass: 828 closed/oriented proxies with 8,971,506 triangles, 579 selectable arterial courses and 2,353 closed sections. Post-integration replay reproduces all four candidate meshes byte for byte and independently repeats the global edge counts.

All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. No browser/runtime dependency is added. No full-atlas render is used, since all visible positive-area surfaces and their attributes are exact.

Whole-atlas anatomical acceptance remains false. Regional cortical/pericallosal, Galenic, petrosal, dural and canal fitting, full receiving lumens, remote topology defects and the separate ILT posteromedial native interface remain open. The right A5 false-positive reclassification from v0.9.101 is retained.

Evidence: `anatomy/source/zero-area-v0.9.102`. Tools: `tools/zero-area-v0.9.102`. Report: `docs/validation/zero-area-v0.9.102.json`.
