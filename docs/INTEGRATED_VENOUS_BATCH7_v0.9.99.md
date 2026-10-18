# Integrated venous junction batch 7, v0.9.99

The source scan covers all 231 venous meshes (1,035,509 vertices and 2,013,063 triangles in v0.9.98). It closes 39 small mixed-label native wall gaps across 14 meshes using 76 triangles and 45 appended copies of existing neighbouring coordinates/normals. Every original vertex position, normal integer and face remains exact. There are no new world coordinates or vessel displacements. Total added wall area is 0.073481 mm²; the largest patch spans 0.961801 mm.

Accepted junctions include retromandibular/superficial temporal, right maxillary/superficial temporal, basal ventricular/thalamic tributaries, pontotrigeminal/petrosal, inferior cerebellar/vermian, vermian/transverse, precentral/superior vermian, anterior medullary/spinal/pontomedullary, basilar/marginal, right lateral mesencephalic/posterior communicating and anterior intercavernous/sphenoparietal interfaces. Detailed per-interface counts are in the JSON report and source junction summary. These are small wall gaps, not 39 separate major anatomical defects.

The combined whole-venous boundary count falls from 15,601 to 15,447. All 4,594 pre-existing non-manifold/misoriented native edges retain their exact coordinates; none are introduced. All 841 potentially intersecting new-face triangle pairs pass. Every changed face passes the conservative local tissue-clearance gates. The final combined gate is reused only after proving the loop-owner-filtered candidate buffers byte exact to the originally checked candidate. Post-integration replay independently repeats the gate and reproduces the accepted buffers exactly.

The scan only considers bounded mixed-label loops up to 1 mm, away from all known bad-edge vertices. Ownership is checked for each individual loop, rather than inferred from its larger boundary component. Single-label loops and potential ports are retained. Tissue-embedded, crossing, topology-regressing, degenerate and unorderable candidates are excluded. Bounded alternative triangulations do not produce any additional accepted repair.

GLTFLoader verification checks all 231 venous meshes: 217 are unchanged and every original attribute/index prefix in the 14 edited meshes remains exact. All four other GLB assets are byte exact. DSA proxy recipes for the edited labels use retained source-face lineage and orientation constraints propagated from paired edges. Each proxy must remain closed, oriented and positive-volume. All 597 arterial course entries, arterial edges, graph and generator remain unchanged, and no vein-site data change. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures and relationships/asset bindings remain exact.

The build, all 19 repair tests, and DSA validation pass: 828 closed/oriented proxies, 8,971,462 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. Numerical checking is sufficient for these bounded append-only source-coordinate wall patches; no new full-atlas render is used.

## Remaining work

The larger Galenic/callosal/cortical, petrosal, dural and canal registration defects remain open. Existing remote topology defects, disconnected components and complete receiving lumens remain unaccepted. Earlier arterial/pericallosal findings and the separate ILT posteromedial native interface remain. This batch does not establish whole-atlas anatomical acceptance.

Source evidence: `anatomy/source/integrated-venous-v0.9.99`. Replay/export/proxy tools: `tools/integrated-venous-v0.9.99`. Report: `docs/validation/integrated-venous-v0.9.99.json`.
