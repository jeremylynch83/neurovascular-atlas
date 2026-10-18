# Arterial native wall repair batch 14, v0.9.106

Two bounded native-junction repairs remove three of the ten remaining arterial exact-zero-area source faces. All original positions and stored normals remain exact. One existing posterior-spinal coordinate and its exact stored normal are copied into the PICA label. Whole-atlas anatomical acceptance remains false.

## Right lacrimal/palpebral subdivision

The right lacrimal wall used a single long edge where its lateral superior palpebral neighbour used two subedges. A collinear zero-area facet bridged that mismatch. The adjacent wall triangle is split at its existing middle vertex, exactly 1134/2267 along the edge. Rational arithmetic on stored binary coordinates proves the two new oriented cross products are positive fractions summing exactly to the original. Their union is precisely the original 0.00024595238151195 mm² wall patch, with no wall-shape or area change.

Both new native subedges finish with exactly two opposite positive-area wall incidences, one from each artery. No vertex is moved or introduced. Every stored normal remains exact; activating the existing middle vertex can change shading interpolation locally. All other positive-area source indices remain exact and in source order.

## Left PICA medullary/posterior spinal wall gap

Removing the two collapsed line facets exposes a bounded mixed-label native wall gap. Seven triangles close its nine-edge boundary. The patch spans 0.00725268559 mm and has area 3.55458461e-06 mm². It adds one copy of an existing posterior-spinal coordinate and stored normal, with no existing vertex movement or new world coordinate.

Every patch boundary edge is independently shown to border one retained positive-area source wall after zero-face removal, with opposite patch direction. The loop includes both native artery labels. All nine edges finish with exactly two opposite incidences. The three newly exposed per-label edges pair with retained positive-area neighbouring artery walls. This measured local closure does not certify a complete receiving lumen.

## Validation and retention

All 22 affected coordinate edges are independently recounted in both source and candidate geometry against all 766 arterial meshes. Affected bad edges fall from three to zero; affected global boundary edges fall from seven to zero. No new global boundary or local/global bad edge is permitted. Both selected labels retain their original connected-component counts.

The unchanged strict changed-face gate checks 143 triangle pairs and all nearby brain/bone targets, with no crossing or tissue-clearance failure. Post-integration replay repeats the exact partition, source-attachment, global-incidence and strict geometric checks and reproduces accepted buffers byte for byte.

GLTFLoader verifies all 599 meshes in complete-circulation.glb. Every original position, stored SNORM16 normal component, retained source face and copied native coordinate/normal is exact. The 597 unedited meshes and four other model assets remain unchanged. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue structures, relationships and asset bindings are retained.

Two DSA recipes and selected arterial courses are refreshed. Both proxies are closed, oriented and positive-volume. All 595 unselected courses remain exact, and selectability, directed connections, graph, vein sites, generator and every edge-distance record remain unchanged. The full build, all 22 repair tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. No full-atlas render was performed.

## Excluded trials and remaining work

The left PICA vermian subdivision trial fails the strict crossing gate. Independent exact arithmetic confirms a genuine pre-existing positive crossing between its unchanged source faces 7390 and 7392. The trial preserves that crossing and is excluded; the original production mesh is retained. The crossing is recorded as open in the issue register.

The ACom gap fails projected-polygon triangulation for all tested owners and is excluded. Single-label collapsed ports are retained without capping. A fresh scan confirms seven zero-area triangles across five labels: right ACom septal perforator, left AICA subarcuate branch, anterior communicating artery, left PICA vermian branch and right Wollschlaeger and Wollschlaeger artery.

Wider Galenic, petrosal, dural, pericallosal/cortical and canal registration findings, remote topology defects, full receiving lumens and the separate ILT native interface remain open. Counts here describe small source topology artefacts, not counts of major anatomical defects.

The hypothetical all-zero-deletion scan is trial evidence only and is labelled accordingly. The accepted spec and final scan describe installed geometry. Historical guard records and rejected trial reports remain preserved.

Evidence: anatomy/source/arterial-wall-v0.9.106. Tools: tools/arterial-wall-v0.9.106. Machine-readable report: docs/validation/arterial-wall-v0.9.106.json.
