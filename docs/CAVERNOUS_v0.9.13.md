# Single cavernous cavity and independent roof, v0.9.13

The v0.9.12 sinus incorrectly followed the upper ICA curve. Its whole-label enclosure check rewarded that extension even though an arterial label does not establish the dural boundary. This release removes that external sleeve and tests the inferior cavity and the upper arterial exit separately.

One slim cavity has rounded outer walls and a curved roof. Its outer shape is defined independently of arterial surface distance. The medial curve reaches towards the sphenoidal carotid sulcus without moving the lateral edge outwards. The actual continuing ICA is used only to exclude the arterial lumen from the venous volume. There is no separate external sleeve or added venous tube above the roof.

The roof is inferred from the inferior clinoid/optic-strut region in the retained sphenoid model. A modest increase from the first roof-bounded draft allows the lower course to fit beneath it. This is a model landmark approximation, not a segmented proximal dural ring. The upper arterial curve remains outside the cavity.

The intracavernous ICA region is lowered smoothly by up to 0.9 mm. The adjustment tapers to zero at the lower, anterior and upper ends. An identical coordinate field is applied across arterial segments and nearby branch attachments, so shared coordinates remain shared. Vertices outside the adjustment are unchanged. Jacobian and stable triangle orientation checks guard against folds. The skull is unchanged.

SOV, ovale emissary, SMCV, lesser-wing and both petrosal entries retain smooth direct attachment, with matching exported normals. The basilar and intercavernous connections remain. All 104 venous labels and the reference surface outside the local replacement region are preserved.

## Verification

The enclosure check uses the actual watertight exported venous mesh. Arterial neighbours are sampled 0.45 mm along surface normals in a fixed inferior model slab, z = 57 to 67.5 mm. Label ports, bone-adjacent samples, and normal offsets entering another part of the siphon are excluded explicitly. This test does not demand enclosure of the whole labelled arterial course.

A separate upper-course test uses a fixed arterial slab, z = 72.5 to 75 mm, and measures its neighbours against the actual cavernous surface. It verifies that the previous upper sleeve is absent. Medial apposition is checked independently using facing sphenoid triangles and ray intersections. These model coordinates and numerical offsets are reconstruction settings, not patient measurements or histological wall thicknesses.

The cavity and rebuilt terminal entry surfaces are checked against actual ICA and resolved sphenoid/temporal triangles. Direct shared edges and continuous same-label paths test all tributary junctions. Whole-network connectivity alone is insufficient. The common venous skin must be watertight, consistently wound and have positive volume. Matched cameras, opaque views and coronal sections provide a separate visual review of the geometry.

Reports: [inferior enclosure and medial apposition](validation/cavernous-ica-bone-fit-v0.9.13.json), [absence of upper sleeve](validation/cavernous-roof-v0.9.13.json), [direct connections and dimensions](validation/cavernous-direct-connections-v0.9.13.json), [entry clearances](validation/cavernous-entry-clearances-v0.9.13.json), [geometry](validation/venous-morphology-v0.9.13.json), [ICA adjustment](validation/cavernous-ica-lowering-v0.9.13.json), [authoring](validation/cavernous-local-build-v0.9.13.json), [viewer](validation/venous-viewer-v0.9.13.json), [interface](validation/venous-ui-v0.9.13.json), and [build](validation/venous-build-v0.9.13.json).

## Measured mesh checks

| Side | Inferior ICA neighbours enclosed | Bone probes reaching wall | Median bone gap | Upper-course minimum CS distance |
| --- | ---: | ---: | ---: | ---: |
| Right | 5,813 / 5,813 | 30 / 30 | 0.179 mm | 2.019 mm |
| Left | 5,869 / 5,869 | 43 / 43 | 0.178 mm | 1.927 mm |

The common skin has 490,236 triangles. All 196,494 exterior reference vertices remain at identical coordinates. Exact coordinate welding removes one coincident seam vertex and two collapsed edge triangles, leaving a watertight skin. No tested cavity/ICA or rebuilt cavity/bone triangle intersections are detected. All 18 direct junctions and 14 end-to-end venous paths pass. The upper-course probes have zero samples within 1 mm of the cavernous surface. Measurements apply only to this mesh and the stated test scopes.

## Anatomical basis and limits

[Seoane, Rhoton and de Oliveira, Microsurgical anatomy of the dural collar (carotid collar) and rings around the clinoid segment of the internal carotid artery](https://pubmed.ncbi.nlm.nih.gov/9574652/) describes the dural collar and the relationship between the rings and clinoidal ICA. A narrow venous interval within the collar does not justify the previous large external tube around the upper curve. This simplified cavity model omits a separate collar plexus.

The [Barrow anatomical review of the clinoidal ICA, carotid cave and paraclinoid space](https://www.barrowneuro.org/for-physicians-researchers/education/grand-rounds-publications-media/barrow-quarterly/volume-18-no-1-2002/microsurgical-anatomy-of-the-clinoidal-segment-of-the-internal-carotid-artery-carotid-cave-and-paraclinoid-space/) relates the lower dural boundary to the inferior anterior clinoid region and distinguishes it from the higher distal ring. These relationships guide the inferred roof. The exact ring position cannot be recovered from this coarse skull surface alone.

[Yasuda et al., The medial wall of the cavernous sinus: microsurgical anatomy](https://pubmed.ncbi.nlm.nih.gov/15214988/) distinguishes sphenoidal dura against the carotid sulcus from the sellar dural barrier. The sphenoidal wall is apposed to bone; the sellar boundary remains inferred against soft tissue. The model does not bridge the sella to find a nonexistent bony wall.

Normal angiographic proportions remain informed by [Neuroangio's cavernous sinus examples](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/). CCF distension is not the target. Uncalibrated 2D projections and separate-patient examples cannot establish exact dimensions or patient-specific registration. Cranial nerves, pituitary, dural rings and venous septa remain unmodelled.

The low petrous/lacerum ICA still overlaps the incompletely resolved skull canal. The new movement tapers out below z = 57 mm and does not resolve that separate mismatch. The successful inferior enclosure test excludes that region. The release therefore does not claim universal full-course enclosure or patient-validated anatomy. Matched CT and arterial/venous imaging would be needed to resolve the canal relationship reliably.

The app includes authoring scripts and sampled junction paths. Re-running the reconstruction requires the extracted raw reference and v0.9.12 baseline assets; these large intermediate inputs are excluded from the installation ZIP. Temporary arterial closure caps are computational exclusion masks, not anatomical dural boundaries.
