# Galenic junction batch 5, v0.9.97

Eleven small native wall gaps are repaired around the Galenic and torcular tributary junctions. The changes use 61 triangles and 47 appended vertices copied from existing neighbouring atlas coordinates. Every original position, normal integer and triangle remains exact. No vessel course moves.

| Native interface region | Gaps closed | Added wall triangles |
| --- | ---: | ---: |
| Galen / precentral cerebellar | 3 | 38 |
| Galen / right posterior callosal | 1 | 1 |
| Confluence / left inferior vermian | 1 | 1 |
| Confluence / right inferior vermian | 2 | 14 |
| Confluence / occipital sinus | 1 | 4 |
| Left inferior vermian / occipital sinus | 3 | 3 |

The source network contains remote non-manifold/misoriented edges, so whole-network automatic acceptance is refused. Local components are reviewed only when their boundaries are mixed between known labels and do not touch those bad edges. Single-label ports and larger or malformed components remain untouched.

All added faces pass whole-scene intersection, degeneracy, native incidence and tissue-clearance checks. The 1,254 candidate triangle-pair checks find no crossings. Closed tissue volumes have no inside samples on new faces; open targets pass conservative surface-separation bounds. The combined 16-label source network's native boundary count decreases from 8,162 to 8,079, with the same 126 pre-existing bad edges and no new ones. Component counts remain unchanged: one for Galen and the left inferior vermian label, two for confluence.

The basal/Galen patch inside the registered corpus callosum is excluded. Local fan alternatives that cross existing surfaces and degenerate loops are excluded. Earlier broad Galenic shifts are not repeated. These results close bounded wall gaps only; they do not resolve the larger Galenic/callosal registration, residual tissue embedding, posterior arterial/sinus contacts, detached torcular component, remote topology defects, precise dural/canal fit or complete receiving lumens. G01 remains open. The separate arterial cohort retains its one ILT interface defect; bilateral pericallosal and other earlier issues remain open.

GLTFLoader export verifies exact retention of all original selected geometry and normals, all 228 other venous meshes and the four other assets. Three DSA proxies are refreshed. All 597 arterial courses, edges, graph, generator and vein sites are unchanged. The build, DSA checks and all 19 repair tests pass. Replay reproduces the accepted position/index buffers byte for byte. All 1,250 named meshes, 1,666 catalogue structures, relationships and 21 runtime source files are retained.

Detailed source inputs, accepted/excluded candidates, per-interface measurements and validation reports are in `anatomy/source/galenic-junctions-v0.9.97`. Replay/export instructions are in `tools/galenic-junctions-v0.9.97/README.md`.
