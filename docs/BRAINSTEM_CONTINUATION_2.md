# Brainstem fitting continuation 2

The runnable app retains the five production model assets of v0.9.19 exactly. This continuation adds offline authoring experiments and stronger validation. It does not apply a newly fitted vascular or brain model.

## Finding that changes the acceptance checks

The anterior medullary vein has zero triangle contacts with the right medullary surface in the current app, but all 770 wall vertices lie inside that closed tissue mesh. Another 105 anterior pontine and 184 anterior spinal wall vertices are inside the same tissue label. Zero surface intersections therefore did not establish that these vessels were outside tissue.

`tools/brain/audit_closed_brainstem_containment.py` reproduces these results. The connected-vein acceptance tool now checks containment in every relevant closed tissue surface as well as triangle intersections. Closed primary brainstem surfaces must contain no fitted wall vertices. Open pons and midbrain surfaces still require explicit exposed-surface and cisternal-corridor checks.

This finding concerns the retained vessels. It does not contradict the earlier *triangle-contact* result for the clival plexus, or establish that the full v0.9.19 vascular registration was accepted. That build was already labelled a partial review build.

## New experiments

| Experiment | Outcome |
| --- | --- |
| Common posterior-fossa AP size map | Rejected. It changes 99 labels and creates skull, dural and retained-vein contacts. |
| Nine connected veins fitted to that size trial | The linear solver succeeds, source triangle indices and shared joins are preserved, and the closed-medullary wall containment check passes. Independent checks still reject hypothalamic contacts and section distortion. The associated brain adjustment is also rejected. |
| Directional posterior skull/dura bounds | Rejected. Independent checks find additional fixed-surface contacts. |
| Directional bounds including retained veins | The brain trial remains rejected and the associated section solver is infeasible. It has no current vein candidate. |

These experiments retain the earlier exact section-fitting work. They do not replace it with new procedural tubes. `docs/validation/resume-status.json` records current candidate hashes and results. Full trial evidence is in the authoring checkpoint.

The comparison image deliberately labels the new geometry as unaccepted. It shows why surface-vein fitting alone does not establish acceptance of the surrounding anatomy. It must not be used as a before/after image of an applied release.

## Validation completed

The app builds, its 1,118-part anatomy catalogue validates, and Chromium checks pass for model loading, search, target links, focus, visibility, orientation and sections. The five production GLB hashes match the original v0.9.19 ZIP. Modified Python tools compile. The matched comparison views were rendered and inspected.

Retained artery relationships and perforator entries have not been accepted for any new brain trial. No failed trial is copied to a production asset or assigned to refreshed production landmarks.

## Reproduction and continuation

Use this runnable app together with the original `brainstem-reconciliation-checkpoint-v0.9.19.zip` and the new `brainstem-continuation-2-checkpoint.zip`. The two checkpoints are authoring overlays. Extract them into the app folder in that order. The new checkpoint retains the later narrow rejected section trial, the new experiments, exact source/candidate buffers, checks and logs.

Python authoring requires NumPy, SciPy, trimesh and VTK. Normal app installation uses the existing dependencies.

```sh
python3 tools/brain/audit_closed_brainstem_containment.py
python3 tools/brain/test_coherent_fossa_resize.py
python3 tools/brain/verify_coherent_fossa_resize.py
python3 tools/brain/refit_brainstem_sections.py --brain-directory .authoring/coherent-fossa22 --output-directory .authoring/coherent-veins22 --preserve-xz
python3 tools/brain/verify_connected_brainstem_skin.py --section --directory .authoring/coherent-veins22
python3 tools/brain/test_bounded_fossa_resize.py --pin-retained-veins --output-directory .authoring/bounded-fossa24
python3 tools/brain/refit_brainstem_sections.py --brain-directory .authoring/bounded-fossa24 --output-directory .authoring/bounded-veins24 --preserve-xz
```

The acceptance commands intentionally reject these recorded candidates. A successful solver is not a publication approval. Clear old candidate files before a new run; a failed solve must never inherit a previous candidate name.

The next fitting pass needs a local anatomical reconstruction of the brainstem/peduncular and adjacent cerebellar interfaces, with fixed skull, dural and protected arterial landmarks. The broad AP maps are unsuitable. Then reconcile the upper communicating course and lateral collector transitions, check full vessel walls and closed-tissue containment, retain valid material sections and joins, and verify posterior arterial/perforator relationships before exporting a release.
