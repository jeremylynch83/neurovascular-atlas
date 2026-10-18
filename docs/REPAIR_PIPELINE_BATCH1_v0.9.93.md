# Batch 1: reusable repair pipeline

The offline authoring pipeline is implemented in tools/repair. It replaces repeated per-vessel setup with cached decoded meshes, content-addressed collision indexes, bounded gap detection, explicit seam alignment, incremental validation and a persistent trial journal.

Production geometry, the 21 runtime source files, and both DSA datasets are byte-exact to v0.9.92. This batch provides authoring infrastructure. Six recorded native attachment failures and the wider anatomical register remain open.

## Replay benchmark

The fixture reconstructs the pre-v0.9.92 scene from the two stored tentorial baseline buffers and the otherwise unchanged production models. Both the historical scripts and the new pipeline produce the exact same seven added triangles across four native gaps. Every original coordinate and face is retained. The new detector uses generic mixed-label boundary rules, without hard-coded repair centres.

| Measurement | Time |
|---|---:|
| Historical preparation, repair and validation, median of 3 runs | 6.660 s |
| New pipeline with an empty authoring cache | 6.193 s |
| New pipeline with a warm cache, median of 3 runs | 1.163 s |

Warm runs are 5.73 times faster than the historical scripts, an 82.5% reduction in this measured authoring time. Every warm run repeats the new local checks; it does not simply return an earlier acceptance. Warm runs reuse five decoded assets, 25 collision indexes and two native boundary scans. The operating system's page cache was not controlled.

These timings exclude model export, DSA generation, release builds, human assessment and ZIP transfer. They are not a forecast for regional registration or reconstruction. Source preparation and repeated numerical work are the measured improvement.

See validation/repair-pipeline-v0.9.93/benchmark.json for all individual times, replay comparisons and source hashes. The full warm replay report is replay-validation.json. A scan of the delivered v0.9.92 geometry finds none of the four already repaired gaps; larger boundaries stay classified for regional review.

## Validation

Sixteen regressions pass. They cover transverse collisions, coplanar overlap, collisions sharing source vertices, legitimate shared edges, point tangency, BVH persistence and nearest-distance answers, automatic wall closure, intentional-port protection, obstacle rejection, enclosed target classification, bounded seam fitting, protected neighbouring attachments, source-content invalidation, unchanged-mesh index reuse, missing-cache recovery, accepted-file checksum checks and rejection reuse.

The replay validates all seven affected faces against the complete scene. It adds no crossings or inconsistent/non-manifold native edges. Closed targets use ray samples. Open or non-manifold reference surfaces use a conservative local clearance bound around existing source anchors, with their absolute volume membership left uncertified. This avoids treating incomplete source surfaces as reliable closed volumes.

The catalogue validation passes. All five model assets, both DSA files and all runtime source files match v0.9.92 exactly; production-retention.json records those checksums. Full runtime/DSA release tests remain for geometry-changing batches and the integrated release checkpoint.

Use tools/repair/README.md for commands, configuration, cache behaviour and staging limits. A staged numerical acceptance does not install geometry or establish anatomical acceptance.
