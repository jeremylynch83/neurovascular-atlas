# Brainstem reconciliation checkpoint

This is an unreleased authoring checkpoint against v0.9.18. No production anatomy, landmarks, vessel-course bindings or app version have changed. The existing five production assets match their original SHA-256 hashes, the app build passes and all 131 landmark bindings still resolve.

The trial moves the pons, medulla, midbrain, cerebral peduncle bases and neighbouring medial cerebellar surfaces posteriorly, with a maximum requested displacement of 8 mm. Actual displacement is limited near fixed tissue and the posterior skull. The skull and basilar venous plexus remain fixed. The anterior medullary, pontine and pontomesencephalic veins use a common anterior-surface translation; connected transverse veins and their immediate collector collars share the same field. Forty context labels and thirteen venous labels change in the staged assets. These labels are not declared anatomically fitted.

The clival plexus to brainstem triangle contacts fall from 2326 to zero using matched refined source surfaces. Both anterior medullary and pontomesencephalic trial walls have zero checked tissue and bone contacts. The pontine wall retains 50 contacts with the pons. This local improvement does not establish acceptance of the combined geometry.

## Why this trial is rejected

The complete check reports 59 failed comparisons. Six brainstem surface labels develop additional nonadjacent self-contacts. New crossings include midbrain to pons, optic tract and neighbouring upper brainstem structures, and cerebellar culmen to retained tentorial surfaces. Some venous outlet and spinal transition contacts increase. Closed cerebellar surface volumes also change substantially in some small labels; this is further evidence that the distance-capped deformation is unsuitable as a final correction. No failed geometry is applied to the app.

Counts compare the same refined triangles before and after displacement. The basilar plexus count differs from the earlier coarse-mesh count for this reason. Open atlas cut surfaces prevent reliable solid containment; a zero triangle contact count alone does not prove a vessel is outside tissue. Existing contacts and exact source-bound join collars are reported separately. Source refinement changes vertex and triangle counts while preserving the original facet surfaces before deformation.

## Files and reproduction

The checkpoint archive is an overlay for the existing v0.9.18 project. Extract it into that project directory. It contains the staged baseline, refined source, trial geometry, coordinate-map implementation, full checks, matched comparison image and source catalogue snapshots. It is not a new runnable release.

Python authoring requires numpy, scipy, trimesh, vtk and Pillow. From the project root:

```sh
python3 tools/brain/reconcile_brainstem.py --brain-only
python3 tools/brain/reconcile_brainstem.py --veins-only
python3 tools/brain/check_brainstem_context.py
python3 tools/brain/verify_brainstem_reconciliation.py
```

The final command returns exit status 1 for the rejected geometry. All outputs remain in `.authoring/brainstem19`; no command above writes production assets. The existing `npm run build` still builds v0.9.18.

Posterior arterial transport is an exploratory tool. Its earlier candidate is stale relative to the latest brain field and is deliberately excluded from this checkpoint's candidate comparison. A new brain correction must also pass posterior arterial relationship checks, shared-junction checks, wall-envelope checks, exported-buffer checks and refreshed landmark bindings before a release can be made.

## Required continuation

The next correction must reconcile the upper brainstem transition, cerebellar junctions and nearby dura as a connected anatomical region. The current nearest-surface displacement caps cause excessive local deformation. A constrained registration or reconstruction that retains tissue interfaces and shape is needed before fitting the complete anterior and lateral venous courses and their outlets. Changing the contact thresholds or accepting only the cleared clival region would conceal the remaining failures.

The anatomical targets use the basilar venous plexus as a clival dural structure and anterior pontomesencephalic veins as brainstem-surface structures:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC10714085/
- https://neuroangio.org/venous-brain-anatomy/anterior-pontomesencephalic-vein/
- https://neuroangio.org/venous-brain-anatomy/veins-posterior-fossa/

These references establish anatomical relationships; they do not validate this atlas trial.
