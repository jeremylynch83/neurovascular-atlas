# ICA enclosure and medial cavernous bone fit, v0.9.12

The v0.9.11 reduction produced a narrow lateral receiving space, but it did not surround much of the retained cavernous ICA or reach the medial carotid sulcus. This release fits the venous envelope to those two structures while retaining a narrow, curved lateral compartment.

## Shape and fit

A thin receiving envelope follows the actual ICA surface, including the upper bend. The arterial lumen is excluded from the venous volume. Exclusion continues through the retained petrous and paraophthalmic ICA skin, preventing a false venous cap over either labelled cavernous exit. The lateral compartment is narrower and shifted medially relative to v0.9.11, with curved edges and rounded roof transitions. Nearby facing carotid-sulcus patches define the sphenoidal medial boundary. There are no planar side walls or added anterior bulb.

The sphenoidal medial wall follows bone. The sellar portion retains an inferred soft-tissue exclusion for the pituitary region. It is not pulled across the sella to reach a nonexistent bony side wall. Cranial nerves, pituitary, dural rings and venous septa are not added.

The SOV, ovale emissary, SMCV, lesser-wing and petrosal entries remain smoothly joined to the receiving space. Both sides retain direct basilar and intercavernous communication. The extra surface detail retained during decimation resolves the small junction boundaries without widening them.

The authoring offsets of 0.85 mm around the artery, 0.22 mm arterial exclusion and 0.18 mm bone clearance are numerical reconstruction settings. They are not measured venous thicknesses, histological wall thicknesses or population dimensions. The total transverse envelope necessarily includes the retained artery and its medial receiving space; the very small v0.9.11 lateral-label span did not represent an enclosing sinus.

## Independent mesh checks

| Side | Eligible ICA neighbours | Enclosed in v0.9.11 | Enclosed in v0.9.12 | Bone probes reaching sinus | Median bone surface gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| Right | 11,800 | 27.9% | 100% | 34 / 34 | 0.182 mm |
| Left | 12,003 | 27.2% | 100% | 45 / 45 | 0.179 mm |

Enclosure is tested on the actual exported watertight venous mesh using ray-based occupancy. Probe points are 0.45 mm along the retained ICA normals. Eligible points are above model z = 57 mm, more than 1.5 mm from labelled arterial ports, more than 0.4 mm outside sphenoid bone, outside the independently closed continuing-ICA mask and more than 0.35 mm from any continuing-ICA mask surface. Offsets that enter another part of the tight siphon or approach a temporary label cap cannot independently test venous enclosure. The report lists these overlapping exclusions explicitly.

Bone probes are selected independently from actual facing sphenoid triangle centroids, then traced towards the sinus surface. They do not reuse the authoring seeds. Every selected patch reaches the new surface, with 95th-percentile clearances below 0.20 mm on both sides. These are numerical apposition checks on the model, not patient morphometry.

All 18 intended direct interfaces have shared mesh edges. All 12 paired tributaries have continuous same-label paths to their retained peripheral courses, and both intercavernous channels connect the two sides. Exported normals match exactly across the tested tributary boundaries. The rebuilt cavernous and terminal entry surfaces have no detected triangle intersections with the tested ICA or resolved sphenoid/temporal bone, within the stated scopes.

The common venous skin is watertight, consistently wound and has positive volume. All 104 venous labels remain. All 196,494 exterior reference vertices are preserved exactly. The arterial, anastomotic and skull GLBs are byte-identical to v0.9.11. Historical arterial deformation measurements refer to the retained v0.9.7 correction.

Reports: [enclosure and bone apposition](validation/cavernous-ica-bone-fit-v0.9.12.json), [direct connections and dimensions](validation/cavernous-direct-connections-v0.9.12.json), [entry clearances](validation/cavernous-entry-clearances-v0.9.12.json), [geometry and surface intersections](validation/venous-morphology-v0.9.12.json), [authoring](validation/cavernous-local-build-v0.9.12.json), [viewer](validation/venous-viewer-v0.9.12.json), [interface](validation/venous-ui-v0.9.12.json), and [build](validation/venous-build-v0.9.12.json).

The comparison views use the same camera and scale for v0.9.11 and v0.9.12. Coronal sections show the old sinus in light grey, the new sinus in blue, the retained ICA in red and bone in dark grey. The review images use purple for SOV, orange for emissary veins and cyan for SMCV. App colours and interface behaviour are retained.

## Anatomical basis and limits

[Yasuda et al., The medial wall of the cavernous sinus: microsurgical anatomy](https://pubmed.ncbi.nlm.nih.gov/15214988/) distinguishes a sellar dural barrier against the pituitary fossa from sphenoidal dura lining the carotid sulcus. In their cadaveric study, venous spaces usually extended into the narrow interval between ICA and sulcus dura. The reported relationships varied substantially, including direct ICA contact with sellar dura and pituitary. This supports fitting the sphenoidal boundary to bone while keeping a separate sellar boundary; it does not prescribe a uniform venous sheath in every patient.

The proportions remain informed by the normal ICA-silhouette examples on [Neuroangio's cavernous sinus page](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/). Uncalibrated angiographic projections and separate-patient images cannot establish patient-specific dimensions or registration. CCF distension is not the size target.

The retained low petrous/lacerum ICA still intersects the incompletely resolved skull canal. That mismatch cannot be enclosed by a bone-clear venous space while retaining those artery and skull assets. It remains outside the successful enclosure test, and a universal full-course enclosure claim is not made. Matched CT, arterial and venous imaging is required to resolve this relationship reliably. Temporary caps are computational masks and are not anatomical dural boundaries.

Authoring scripts and sampled paths are included. Re-running the authoring comparisons also requires the extracted raw reference and baseline inputs used in the authoring workspace; these large intermediates are excluded from the install ZIP.
