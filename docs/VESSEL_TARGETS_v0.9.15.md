# Anatomical targets and course rules v0.9.15

Implements sections 1 and 2 of the vessel fitting plan on the delivered v0.9.14 app, itself based on v0.9.13. This release establishes the baseline audit, adds missing target anatomy and stores explicit vessel course rules. Vessel fitting is the next modelling stage.

## In the app

- Search **Rolandic sulcus** or **Central sulcus** to select either newly imported central sulcus. Its alternate names appear in the panel.
- Search **Central sulcus course** for the nine ordered target stations on either side.
- Search **Falcotentorial attachment course** for the complete 25-station guide. Selecting it reveals both tentorial leaves and the falx. Galen references the anterior end; the straight sinus references the full line.
- Selecting an intracranial vessel shows **Anatomical course**, with clickable links to its brain targets. Existing course-landmark relationships link to the visible guides.
- Brain overview and Deep / posterior fossa retain their existing behaviour. Section controls now clear focus after processing the control change, so the first section click also works while a guide is focused.

## Added anatomy

16 original source meshes were added with the unchanged skull registration: bilateral central and parieto-occipital sulci, posterior lateral fissures, circular insular sulci, putamina, globi pallidi, optic tracts and optic chiasmal halves. The brain asset now contains 188 individually named surfaces and 391,136 triangles. Sulcal references and ventricular boundaries are distinguished from parenchymal and dural surfaces in metadata.

The original 172 registered brain meshes retain exactly the same vertex and triangle arrays. No brain deformation was needed for this preparation stage. Small local adjustments are permitted during later fitting, with constraints to preserve overall registration, shape, volume and neighbouring relationships, and mandatory regeneration of affected bindings.

## Falcotentorial and sulcal targets

The falcotentorial guide follows paired upper medial tentorial contours, sampled anterior to posterior within 2.5 mm of the registered source midline. Each point is bound to the left tentorial surface with independent right-tentorial and falcine triangle bindings. The maximum distance to the corresponding falcine witness is 1.03 mm; to the right tentorial witness, 1.27 mm. These are finite-thickness atlas surface agreement measurements, not dural thickness or a segmented sinus lumen.

Central sulcal guides sample the lateral lip of the original named reference surface from inferior to superior. They identify the sulcal target. The approach, tissue clearance, calibre and joins still need individual vessel fitting. Posterior Sylvian and parieto-occipital target guides provide additional regional stations.

## Course data and audit

All 870 vascular geometry labels have a version-bound course record. 290 have intracranial anatomical rules; the other 580 are retained baseline or potential-connection records. Modes distinguish surface, sulcal, cisternal, dural, bridging, subependymal, choroidal and penetrating phases. Each record carries its side, target IDs, station references, catalogue attachment graph, geometry hashes, radius-preservation policy and review state.

Mode order is an anatomical sequence, not an automatically invented geometric division of the existing tube. The fields explicitly require individual segment boundaries to be reviewed before fitting. Most targets are regional references; ordered triangle-bound sequences are provided where the present target geometry supports them. Missing perforator entry boundaries, choroidal fissure attachments and cervical spinal cord anatomy remain explicit dependencies.

The audit reads the actual decoded delivered GLB node geometry with world transforms. It records wall-to-target distances, minimum vertex-to-parent-surface attachment gaps and baseline asset identity. Unsigned sampled distances do not establish containment or patent junctions. The delivered vessel surfaces remain the authoritative calibre and shape baseline; older authoring centrelines are not substituted.

See `ANATOMICAL_AUDIT_v0.9.15.md`, the JSON/CSV reports in `docs/validation/`, and `anatomical-target-review-v0.9.15.png`.

## Reproduction

Normal installation remains `npm ci`, `npm test`, `npm run build` or the existing Docker/installer scripts. No FBX conversion, VTK or fitting process runs during normal build or viewing.

Authoring requires NumPy, Trimesh, SciPy and VTK. `import_targets.py` additionally requires ufbx and the exact original FBX/inventory passed by CLI. The extended source-orientation GLB is included, so ordinary target rebuilding does not need that FBX:

```sh
python3 tools/brain/build_brain.py
python3 tools/brain/build_targets.py
python3 tools/brain/build_courses.py
```

For the full baseline audit, losslessly decode the retained arterial/venous assets with `tools/decode_glb.mjs` to the filenames documented in `audit_baseline.py`, then pass the delivered v0.9.14 ZIP via `--baseline`. `render_targets.py` consumes these same decoded assets. Authoring dependencies and temporary decoded assets are excluded from the release ZIP.

Validation covers catalogue consistency, 131 primary surface bindings and secondary falcotentorial bindings, exact retained meshes, course references and stale-asset rejection, aliases, selection links, transparency, focus and section controls. Production build and browser results are recorded in `docs/validation/`. Source licences and attribution are retained.
