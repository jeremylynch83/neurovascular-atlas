# Transverse pontine crossing, v0.9.47

The transverse pontine midline crossing now passes posterior to the basilar artery, between the artery and pons. Teksam et al. describe transverse midline venous anastomoses passing beneath the basilar artery ([AJNR 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC7974009/)). This correction does not impose a universal ordering on smaller pontine arterial branches.

The v0.9.46 crossing was anterior to the basilar artery. v0.9.47 moves the connected crossing and collars posteriorly using a common compact field. Four venous labels change: anterior pontine, transverse pontine left/right and prepontine bridge right. The existing pons geometry did not provide enough space behind the fixed artery, so both pontine labels receive a compact local groove recess, maximum 3.5 mm. This is a teaching-model context adjustment, not a patient-derived measurement. Arterial and skull assets are unchanged. The halo, selection, opacity and inspection-panel behaviour is retained.

Two levels of linear venous triangle subdivision preserve the original baseline surfaces while allowing the deformation to be represented accurately at coarse junction facets. Original labels and shared collars remain connected. The export uses exact float positions and indices with reconstructed normals, tested through the actual Three.js loader and MeshoptDecoder. All unchanged labels retain exact positions and indices.

## Validation

The evidence file records full moved-surface contact checks against overlapping anatomical labels, non-adjacent triangle checks, sampled posterior depth, shared-interface closure, deformation Jacobian, calibre estimates and actual loader verification. Production validation, TypeScript and Vite build pass.

At the transverse crossing, anterior-posterior rays through the actual basilar artery surface confirm the vein is posterior to it. Minimum sampled clearance is about 0.66 mm. Nearby small arterial crossings are checked individually.

The mesh contains legacy folded union facets. Raw self-contact pair identities change, including additional folded facet contacts at the transverse junctions (86 left and 4 right triangle pairs) beyond the recorded 0.15 mm existing-site tolerance. The self-intersection regression gate therefore remains failed for this union mesh. This is an explicit remaining mesh-quality limitation; the crossing depth and external artery/vein/brain clearance checks pass. Artificial medial pons label-closure facets are reported separately from the exterior pial surface. Existing pontine perforator tissue-entry relationships and fourth-ventricle internal context overlap remain recorded. This is not a watertight-mesh certificate or whole-model anatomical approval.

Calibre is illustrative. The section estimator is unreliable around bifurcations and records a substantial upper-tail radius change around the connected median junction. Median radius ratios remain 1.0. The crossing correction retains review status rather than claiming a quantitative lumen reconstruction.

## Comparisons

[Anterior comparison](../review-renders/Transverse_pontine_anterior_v0.9.47.png) and [oblique comparison](../review-renders/Transverse_pontine_oblique_v0.9.47.png) show matched views, v0.9.46 on the left and v0.9.47 on the right. The anterior view shows the basilar artery covering the transverse crossing after correction; the oblique view helps assess the space between artery and pons.

## Reproduction

Decode the exact v0.9.46 assets with tools/decode-posterior-baseline.mjs, retain venous.glb and brain-context.glb as exact export baselines, and use tools/brainstem-v0947/refine.py, model.py, audit.py, selfcheck.py, depth.py and calibre.py with the working directory argument. export.mjs takes candidate and baseline directories; catalogue.py refreshes persisted brain anchors and all course hashes. Run build-anatomy.sh, check_export.mjs and npm run build. See common.py for the complete placement fields.
