# Arterial native-port cleanup batch 13, v0.9.105

This batch removes 59 of the 69 guarded arterial exact-zero-area source triangles, across 29 labels. Every positive-area source triangle, position and stored normal remains exact. No new global boundary or local/global bad edge is introduced. Ten zero-area faces across seven labels remain open.

| Check | Before | After |
| --- | ---: | ---: |
| Exact-zero-area arterial source triangles | 69 | 10 |
| Bad native edges among 100 affected global coordinate edges | 85 | 11 |
| Boundary edges in that same affected set | 9 | 2 |
| Newly exposed per-label edges with verified native wall pairings | - | 36 |
| New global boundary edges | - | 0 |
| New local or global bad edges | - | 0 |

The 74 cleared bad coordinate edges and seven removed boundary artefacts are source topology improvements, not counts of major anatomical defects. All selected labels retain their original connected-component counts. No positive-area surface is added or reshaped.

## Exact subset search and native ports

The previous conservative guard retained all deletion contributors to a violating constraint. An exact search now groups candidates by shared coordinate edges: 35 independent groups, at most six faces per group. It enumerates every subset capable of improving the best deletion count. Nine triangles pass the original no-new-per-label-boundary rule.

The wider port rule permits a newly exposed per-label boundary only when two retained positive-area source wall triangles, from different artery labels, meet on that exact coordinate edge in opposite directions. All 36 newly exposed edges pass this proof. The 59-face result maximises deletion count under these explicit constraints. This is not an optimum over possible retessellation, regional refitting or new wall construction.

Each deletion is exactly zero-area using rational arithmetic on stored binary coordinates. Independent replay restores the v0.9.104 baseline buffers, retains all other indices in original order and recounts every affected edge against all 766 arterial meshes. It separately identifies both retained wall triangles at each exposed port edge and proves their positive area, opposite direction and distinct labels. Accepted and replayed buffers match byte for byte. No port is capped by the source repair.

## Export and application checks

Only complete-circulation.glb receives new compressed index accessors. Its original POSITION and NORMAL streams and accessor references remain intact. GLTFLoader checks all 599 meshes, every retained source index and every position/normal stream. The 570 unedited meshes in that asset and four other GLBs remain exact.

The 29 affected DSA recipes are refreshed using source-face lineage and rebuilt projection caps. Each proxy is closed, consistently oriented and positive-volume. Selected arterial courses are refreshed; all 568 unselected courses remain exact. Selectability, directed connections, graph, vein sites, generator and every edge-distance record remain unchanged.

The full build, all 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,504 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained. Issue-register copies agree and retain the one unresolved ILT native-interface record. No whole-atlas render was performed.

## Remaining work

A fresh scan finds ten zero-area triangles across seven labels: right ACom septal perforator, left AICA subarcuate branch, anterior communicating artery, right lacrimal artery, left PICA medullary perforator, left PICA vermian branch and right Wollschlaeger and Wollschlaeger artery. They cannot all be removed under this batch's deletion-only constraints; explicit local retessellation or wider native-junction review remains possible.

The existing Galenic, petrosal, dural, pericallosal/cortical and canal registration findings, remote topology defects, full receiving lumens and separate ILT interface remain open. Coordinate-edge pairing is a measured geometric relationship, not whole-atlas anatomical acceptance. Historical batch 12 guard records remain intact; this batch supplies their current partial resolution.

Evidence: anatomy/source/arterial-port-v0.9.105. Tools: tools/arterial-port-v0.9.105. Machine-readable report: docs/validation/arterial-port-v0.9.105.json.
