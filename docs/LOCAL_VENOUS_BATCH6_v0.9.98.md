# Local venous junction batch 6, v0.9.98

One mixed-label native wall gap at the left inferior petrosal sinus/basilar plexus interface is repaired with three triangles, total area 0.130700 mm² and maximum span 0.862051 mm. Only the basilar plexus mesh changes. One appended vertex copies an existing inferior petrosal coordinate and normal; all original positions, normal integers and faces remain exact. No vessel is repositioned.

The cached scan covers 20 local veins and 14 native neighbouring labels. It checks mixed-label directed boundary components up to 1 mm, away from vertices on existing bad edges. Single-label openings are retained as potential ports. The only other small mixed-label component is a 1.768 mm cavernous/sphenoparietal boundary, which touches existing bad edges and has inconsistent direction; it is excluded. This batch does not force a large sinus or canal refit through the local patch workflow.

The accepted new faces pass all 53 potentially intersecting triangle-pair checks against every nearby named surface. Fifteen unique corner/midpoint/centre samples are outside the closed occipital volume; conservative open-temporal-surface clearance has a minimum 0.164524 mm margin. The 34-label network boundary count falls from 2,724 to 2,719, with all 952 pre-existing non-manifold/misoriented edges retained and no new ones. At the repaired pair, shared native coordinates increase from 13 to 14 and opposite paired native edges from 12 to 14. The basilar plexus retains its three existing components.

The exported GLB is verified through GLTFLoader: all 231 venous meshes checked, 230 unchanged; every original selected position, normal and face exact; all four other GLBs byte exact. The basilar plexus DSA proxy is refreshed from retained source-face lineage. Its historical sanitised face orientation is matched independently of the display mesh, and the result must remain closed, oriented and positive-volume. All 597 arterial course entries, arterial edges, graph and generator remain unchanged. Runtime source, all 1,250 named meshes, all 1,666 catalogue structures and all relationships/asset bindings are retained.

The build, DSA validation and 19 repair tests pass. Explicit proposal replay reproduces the accepted buffers byte for byte after integration and reruns the local numerical gates.

## Remaining work

G08 remains open. The superior petrosal walls, disconnected components, old degenerate/bad-edge geometry and arterial/tissue contacts need coupled regional reconstruction. Inferior petrosal open walls, existing self-intersections and bone contacts remain. Closed local companion additions do not establish receiving-lumen continuity. Exact fine canal/nerve and cervical registration targets remain absent or unresolved. Earlier G01/G03/G04/G05/G06/G07 findings and the separate ILT interface remain open. These are local geometric repairs, not whole-atlas anatomical acceptance.

Source evidence: `anatomy/source/local-venous-junctions-v0.9.98`. Replay/export/proxy tools: `tools/local-venous-junctions-v0.9.98`. Detailed numerical report: `docs/validation/local-venous-junctions-v0.9.98.json`.
