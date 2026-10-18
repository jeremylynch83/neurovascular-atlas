# Experimental brain simplification - v0.9.118

This is a separate comparison candidate based on v0.9.117. The previous release
remains available unchanged. No anatomical acceptance is implied by the trial.

The candidate reduces selected larger cerebral and cerebellar parcels rather
than smoothing or rounding coordinates. Every retained position and normal is
copied exactly from v0.9.117. All 193 brain parcels remain present: 29 have fewer
triangles and 164 retain their original decoded geometry. Brainstem, deep
structures, ventricles, dural surfaces, small parcels and cerebellar peduncles
remain unchanged. The four other GLBs are byte-identical, including all vessels,
their repaired junctions and bones.

| Brain model | v0.9.117 | Trial v0.9.118 |
| --- | ---: | ---: |
| File bytes | 29,070,264 | 26,304,940 |
| Triangles | 3,347,028 | 2,998,978 |

The brain file is 9.51% smaller, with 10.40% fewer triangles. These figures are
for the brain file, not the complete source archive. The final validation receipt
also includes actual production gzip sizes.

Protections include all landmark attachment faces and their one-ring neighbours,
shared parcel coordinates, mesh borders, and degenerate source triangles and
their one-ring neighbours. The simplifier uses retained source vertices, normal
attributes, locked borders and fold preservation. Its combined approximate error
budget is 0.01 mm. This algorithmic error estimate is not a maximum surface
distance guarantee.

Independent measurements sample both surfaces at every vertex, and at face
centres and edge midpoints with a stride of 16 faces. All sampled distances above
0.008 mm receive full triangle-BVH nearest-surface queries. Across 1,745,631
samples, the maximum measured distance is 0.018761 mm, the 99th percentile is
0.003158 mm and RMS distance is 0.000708 mm. The sampled acceptance limit is
0.02 mm. These measurements do not constitute a continuous Hausdorff bound and
cannot establish preservation of every anatomically important feature.

Initial reductions that altered topology were rejected. The selected candidate
preserves connected components, Euler characteristic and exact boundary edges,
with no increase in non-manifold edges or zero-area faces. Topology is evaluated
after excluding pre-existing exact zero-area source faces; those artefacts are
not treated as positive-area surface features. Area and signed volume changes
are limited to 0.1% per changed parcel. The 181 protected anchor triangles retain
their original ordered vertex coordinates and barycentric anchor positions;
their new face IDs and file hashes are rebound explicitly.

Four original-versus-candidate views cover the posterior and inferior cerebellum,
a detailed cerebellar parcel and the cerebral cortex. These comparisons showed
no obvious visible loss at the inspected views and scales. Functional loading
and DSA checks are recorded separately. Software WebGL does not establish
device-specific frame-rate improvements.

Changing brain surfaces invalidates spatial exclusions that depended on the old
brain asset. The previous deferred-review registry remains untouched and must
report the brain hash mismatch until those authoring search scopes are reviewed
again. Vessel meshes, DSA recipes, flow data, named anatomy, relationships and
the existing anatomical issue register remain unchanged.

Trial settings, excluded parcels and per-parcel measurements are retained under
`anatomy/source/brain-simplification-v0.9.118/`. Re-run authoring trials against an
unpacked v0.9.117 baseline with:

```sh
node tools/brain-simplification-v0.9.118/trial.mjs BASELINE_APP OUTPUT_DIRECTORY anatomy/source/brain-simplification-v0.9.118/gate.json
python tools/brain-simplification-v0.9.118/measure.py OUTPUT_DIRECTORY 0.01
node tests/brain-simplification/validate.mjs BASELINE_APP
```

The final release receipt is `docs/validation/brain-simplification-v0.9.118.json`.
