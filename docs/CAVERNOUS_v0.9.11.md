# Narrow curved cavernous space, v0.9.11

Implements the user's review of v0.9.10: the cavernous cavity remained too wide and box-like, and the SOV and emissary attachments were unsatisfactory.

## Result

The cavernous body now has a narrow, curved profile with tapered, rounded ends. Its transverse thickness varies continuously, with a gentle inward lateral contour and rounded roof transitions. The planar anterior, posterior and medial wall constraints have been removed. A curved oval perimeter defines the body, rather than a solid with four clipped walls.

The terminal SOV and ovale emissary vein have been rebuilt to meet this smaller receiving space. Terminal SMCV, lesser-wing, superior petrosal and inferior petrosal courses have also been adjusted. Short posterior connections preserve communication with the basilar plexus. Thin curved anterior and posterior intercavernous channels connect both sides.

The right SOV previously had no direct common boundary with the cavernous sinus. The left had only a three-edge contact. The emissary vein still had shared edges, but its terminal form needed revision. The new checks therefore verify each intended direct attachment and trace the individual tributary back to its retained peripheral course. Being part of one connected whole-head network is insufficient to establish those local connections.

## Model measurements

| Measurement | v0.9.10 | v0.9.11 |
| --- | ---: | ---: |
| Right cavernous label volume, temporarily capped | 823.6 mm³ | 369.9 mm³ |
| Left cavernous label volume, temporarily capped | 824.1 mm³ | 372.5 mm³ |
| Right transverse span at y = −48, z = 58 mm | 6.44 mm | 2.91 mm |
| Left transverse span at y = −48, z = 58 mm | 6.47 mm | 2.90 mm |
| Right transverse span at y = −46, z = 61 mm | 6.71 mm | 1.65 mm |
| Left transverse span at y = −46, z = 61 mm | 6.78 mm | 1.76 mm |

The capped volume estimates are approximately 55% smaller. These are comparisons of the author's meshes, not normal population dimensions. Transverse spans are sampled at the same two core locations away from the anterior tributary mouths. Temporary closure of labelled ports influences volume estimates. Neither quantity measures wall thickness or establishes patient-specific accuracy.

## Verification

- All 18 expected direct cavernous interfaces are present: SOV, ovale emissary, SMCV, lesser-wing, superior petrosal, inferior petrosal, basilar plexus, anterior intercavernous and posterior intercavernous connections on each side.
- Each of the 12 paired tributaries has a continuous same-label surface path from the cavernous interface to its retained peripheral course. Both intercavernous channels have continuous paths between the two cavernous sinuses.
- The rebuilt terminal surfaces have no detected triangle intersections with the cavernous ICA or the retained sphenoid/temporal bones within the replacement interior. The retained overlap collar and peripheral courses are outside that terminal clearance test.
- Exported normals match exactly across the tested tributary/cavernous label boundaries.
- The common venous skin is watertight, consistently wound and has positive volume. All 104 vein labels remain, and all 196,494 exterior reference vertices are preserved exactly.
- The arterial, anastomotic and skull assets are byte-identical to v0.9.10.

Reports: [direct connections and dimensions](validation/cavernous-direct-connections-v0.9.11.json), [terminal clearances](validation/cavernous-entry-clearances-v0.9.11.json), [geometry and ICA clearance](validation/venous-morphology-v0.9.11.json), [authoring](validation/cavernous-local-build-v0.9.11.json), [viewer](validation/venous-viewer-v0.9.11.json), [interface](validation/venous-ui-v0.9.11.json), and [build](validation/venous-build-v0.9.11.json).

The companion review uses matched cameras for v0.9.10 and v0.9.11. Purple identifies the SOV, orange the ovale emissary vein, cyan the SMCV and blue the cavernous/lesser-wing spaces. These colours are used in the review images. The app's interface and colour behaviour are retained.

## Reference basis and limits

The proportions were reviewed against the normal cavernous sinus examples with ICA silhouettes on [Neuroangio's cavernous sinus page](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/), particularly the [normal carotid silhouette example](https://neuroangio.org/wp-content/uploads/Venous/V_cavernous_sinus_carotid_silhouette_1.png) and [vertebral venous-phase example](https://neuroangio.org/wp-content/uploads/Venous/V_cavernous_sinus_angiogram_VERT_2.png). CCF distension and pressurised venous injections were not used to set this release's cavity size.

The primary cadaveric study [Orbital venous drainage into the anterior cavernous sinus space: microanatomic relationships](https://pubmed.ncbi.nlm.nih.gov/9055293/) describes the anterior receiving compartment as slit-like. Its reported anteroposterior measurement concerns that anterior compartment, and has not been substituted for the width of the whole cavernous sinus.

This remains a reference-guided teaching reconstruction. No matched skull/arterial/venous patient dataset is available for registration. The known low petrous/lacerum skull canal relationship is unresolved. Cranial nerves, pituitary, dural rings and venous septa are not rendered. Historical ICA deformation measurements in the geometry report refer to the retained v0.9.7 correction.
