# Terminal ICA and mandibular corrections, v0.7.3

The v0.7.2 parent-junction deformation extended too far along M1. Its nearest-parent lookup could select a lower part of the returning ICA limb, pulling the M1 root down and folding the surface. This release restricts that collar to the junction and anchors terminal daughters to the terminal ICA attachment. M1 is rebuilt with a smooth lateral course on both sides. Both A1 triangle surfaces are retained exactly from v0.7.2, including their shared boundary vertices. The upper ICA blends into the retained terminal region.

The cavernous ICA controls move approximately 2–3 mm medially and 2–3 mm posteriorly around the bend. The ophthalmic origin is lowered approximately 3 mm towards the estimated distal dural-ring region, while retaining its orbital-apex destination. The dural rings are anatomical estimates, not segmented structures.

The inferior alveolar artery approaches the medial ramus, enters the mandibular-foramen region and follows an estimated intraosseous canal below the dental alveoli. It does not run beneath the mandibular body. The mental branch emerges outwards at the visible mental-foramen depression and continues towards the lower lip. The incisive and mylohyoid attachments follow the revised parent course. Mandibular-foramen, mental-foramen and canal catalogue records are updated on both sides. The complete canal lumen is not present in the source segmentation, so the course is fitted within the cortical envelope rather than certified against a segmented lumen.

Shared-vertex smoothing now leaves unaffected artery parts fixed. This avoids incidental changes to nearby branches when a different junction is adjusted. Potential connection endpoints use the same branch deformation and their donor/recipient relationships remain unchanged. Bones and app UI are unchanged.

## Authoring checks

- Actual exported surface: finite positions, watertight joined topology, consistent winding and unchanged face incidence.
- Both A1 surfaces: exact triangle-coordinate equality with v0.7.2.
- M1: strictly lateral centreline progression on each side; matched-camera review of the actual surface for the reported fold.
- Ophthalmic artery: lower measured origin on both sides.
- Mandibular body: sampled inferior alveolar centreline inside the cortical envelope, with outward mental branches near the reviewed exit regions.
- Cavernous/clinoid ICA: sampled exported surface vertices and face centres clear the sphenoid. The canal regions remain explicitly unresolved.
- Lossless mesh compression: exact decoded-buffer comparison.

See `validation/refinement-v0.7.3.json`, `validation/ica-v0.7.3.json` and the v0.7.3 compression reports. These are targeted authoring checks, not an exhaustive intersection proof or anatomical certification. They are not part of installation or normal application builds. The separate review PNG shows selected artery surfaces, so hidden daughter branches can leave apparent openings in the review image; the full exported circulation is joined.

## References

- Zhou C et al. Endoscopic cadaveric analysis of the origin of the ophthalmic artery. *Surgical and Radiologic Anatomy*, 2023. https://doi.org/10.1007/s00276-023-03234-4
- Kikuta S et al. The mental artery: anatomical study and literature review. *Journal of Anatomy*, 2020. https://pubmed.ncbi.nlm.nih.gov/31691967/
- The position and course of the mandibular canal. Cadaveric dissection study. https://pubmed.ncbi.nlm.nih.gov/1298823/

The skull-base references and source limitations in `ICA_v0.7.2.md` also apply.
