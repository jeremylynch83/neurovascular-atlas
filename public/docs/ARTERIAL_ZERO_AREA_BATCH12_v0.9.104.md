# Arterial exact-zero-area cleanup batch 12, v0.9.104

All 766 arterial source meshes were scanned. The scan found 453 exact-zero-area triangles across 100 labels. This release removes 384 of them across 86 labels without moving vertices, changing stored normals or deleting any positive-area source face. It is a source topology cleanup; whole-atlas anatomical acceptance remains false.

| Check | Before | After |
| --- | ---: | ---: |
| Exact-zero-area arterial source triangles | 453 | 69 |
| Bad native edges in the 596 affected global edges | 483 | 88 |
| Boundary edges in that same affected set | 107 | 9 |
| New boundary edges, per label or globally | - | 0 |
| New bad edges, per label or globally | - | 0 |

The 395 cleared bad edges and 98 removed boundary artefacts are coordinate-incidence improvements, not 395 large anatomical defects. Each deleted triangle has exactly zero cross-product under rational arithmetic on its stored binary coordinates. Every positive-area face remains in exact source order. Source point/line artefacts are removed without changing wall area. All selected labels retain their original connected-component counts.

## Selection and independent replay

The deterministic selection begins with all 453 zero-area candidates. If a proposed deletion introduces a local or global boundary or bad edge, every active deletion contributing to that constraint is retained. Repeating this guard propagation retains 47 then 22 faces and selects 384. This conservative procedure is not an optimiser; it does not prove the other 69 faces cannot be repaired by another safe subset, native-port review or explicit retessellation.

An independent replay restores decoded v0.9.103 baseline buffers, proves each deletion exactly zero-area, checks all retained indices and recounts all affected edges against every one of the 766 arterial meshes. Accepted and replayed buffers match byte for byte. A fresh post-integration scan confirms 69 zero-area triangles remain across 33 labels.

## Export and DSA

Only complete-circulation.glb receives new index accessors. Its original POSITION and NORMAL streams and accessor references remain intact. GLTFLoader checks all 599 meshes in the asset: retained source indices are exact and the 513 unedited meshes are unchanged. The four other model assets remain byte-exact.

The 86 affected DSA recipes are refreshed using retained source-face lineage and rebuilt caps. Every result is closed, consistently oriented and positive-volume. Selected arterial courses are refreshed; all 511 unselected courses remain exact. Selectability, directed connections, graph, vein sites and generator remain unchanged. No edge-distance record changes.

The full build, all 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,504 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. No full-atlas render was used for this bounded cleanup.

The historically stale public-root issue-register copies are synchronised with the current root and public/anatomy records, retaining the one unresolved ILT interface.

## Remaining work

The 69 guarded zero-area faces remain for focused review. Existing disconnected components, registration and tissue contacts, Galenic/petrosal/dural/canal findings, receiving lumens and the separate ILT native interface remain open. This release makes no claim that the atlas is anatomically accepted.

Evidence: anatomy/source/arterial-zero-area-v0.9.104. Tools: tools/arterial-zero-area-v0.9.104. Machine-readable report: docs/validation/arterial-zero-area-v0.9.104.json.
