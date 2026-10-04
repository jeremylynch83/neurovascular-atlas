# Cavernous ICA and sinus refinement, v0.9.7

The v0.9.6 lower cavernous ICA sat too far lateral to the parasellar groove in the retained skull. The correction moves the lower course up to **3 mm medially and 1.4 mm superiorly** on each side, tapering at the petrous entry and upper exit. This is a skull-registered teaching reconstruction, not a measured patient segmentation.

## Changes

- The same continuous deformation follows local arterial branches and anastomotic surfaces, keeping their joins together. Most change is in the cavernous ICA, MHT, ILT and their cavernous connections. The adjacent petrous and paraophthalmic interfaces receive the tapered transition. Bone-defined landmarks stay fixed; inferred arterial dural-ring references follow the corrected course.
- Broad, smoothly united parasellar venous envelopes replace the three parallel rounded paths. Their medial walls exclude an inferred sellar soft-tissue space. Corrected ICA and retained sphenoid/temporal surfaces are excluded before meshing.
- Anterior and posterior intercavernous routes become flatter, smoother dural channels. Their calibre remains illustrative.
- Original tributary surfaces are retained through the regional replacement. A 0.64 mm gap at the right sphenoparietal collector is closed with a short bone- and ICA-constrained join. Isolated small envelope fragments are removed.
- **196,494 original venous vertices outside the replacement region are retained exactly.** Skull geometry, the UI and the drainage catalogue are retained.

At the matched coronal section y = -44 mm, the gap between the medial walls of the lower ICA sections falls from **26.57 mm to 20.57 mm**. These are model measurements at one section, not population targets. The maximum displacement vector is 3.31 mm.

## Evidence and limits

The retained carotid-sulcus, sellar-floor and clinoid landmarks provide the registration frame. Normal Neuroangio venous-phase angiography supports the sinus envelope around the carotid flow void. Cinematic DynaCT venous examples provide qualitative projection comparisons. These are different subjects with selective venous filling, without calibration or registration to the atlas.

References:

- [Anatomical study of cavernous ICA and sellar structures, 144 ICAs, 2013](https://pubmed.ncbi.nlm.nih.gov/23524760/). Examines ICA position relative to fixed sellar structures.
- [Basal cavernous sinuses, carotid arteries and pituitary relationships, 2008](https://pubmed.ncbi.nlm.nih.gov/18262607/). Describes intercarotid variability and differences between specimens and living imaging.
- [Cavernous venous-space dissection and morphology, Zhan et al., 2022](https://www.nature.com/articles/s41598-022-21254-9). Describes interconnected medial, lateral, anteroinferior and posterosuperior spaces around the ICA. These are not fabricated as separate labelled compartments here.
- [Neuroangio cavernous sinus angiography and 3D cases](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/). Cinematic images credited to Dr Matthew Young. Normal carotid silhouette and catheter venogram examples guide qualitative review.

The middle and upper corrected cavernous ICA vertices, above z = 56 mm, clear the sphenoid surface. The low petrous/lacerum transition still meets the unresolved canal region in the retained bone. Moving the artery alone cannot resolve that bone lumen. Its pre-existing negative bone distances are documented separately.

The named cavernous ICA ends are open interfaces with adjacent arterial parts. Signed distance is unreliable beyond these interfaces, so exact triangle-intersection checks are used independently. The pituitary, cranial nerves and dural rings are not segmented. The sellar soft-tissue exclusion is inferred. Detailed trabeculae and septa are not modelled. This release improves the broad relationships and remains subject to anatomical review.

## Validation

- One closed, consistently wound, positive-volume venous surface: **241,515 vertices, 483,334 triangles and all 104 named parts**.
- No triangle-intersection lines between either cavernous sinus and its corrected cavernous ICA.
- All 930 scene parts decode in Three.js. Real raycasts select all 104 venous structures. Focus, translucency, clipping, per-structure visibility and fallback rendering fixtures pass.
- React interaction checks, installer integration checks and production build pass. UI checks use jsdom and engine fixtures; they do not measure browser GPU performance.
- All compression buffers round-trip byte-for-byte. Very small boolean collar triangles remain in the closed mesh; their minimum area is recorded in the morphology report.

Reports are in `docs/validation`: `venous-morphology-v0.9.7.json`, `venous-viewer-v0.9.7.json`, `venous-ui-v0.9.7.json`, `ica-position-v0.9.7.json`, `ica-bone-v0.9.7.json` and `cavernous-local-build-v0.9.7.json`.

## Matched renders

Blue is the cavernous/intercavernous surface. Red is the named cavernous ICA. Grey includes skull context and short review stubs from connected veins. Clipped grey review stubs are not mesh breaks.

![Frontal before and after](validation/cavernous-v0.9.7/01-frontal.png)

![Six updated views](validation/cavernous-v0.9.7/00-six-view-overview.png)

![Skull-registered coronal audit](validation/cavernous-v0.9.7/10-coronal-ica-audit.png)

The same directory includes six matched before/after projections and three qualitative comparisons with published angiography and 3D imaging. Bone contours in the coronal audit remain fixed.

## Reproduce authoring

Requires Python NumPy, SciPy, VTK, trimesh and manifold3d, plus the app's Node dependencies. The production build does not run authoring or need these additional Python packages.

Decode the **v0.9.6** circulation, anastomotic and venous GLBs into `.authoring/circulation-raw.glb`, `.authoring/anastomoses-raw.glb` and `.authoring/venous-original.glb` with `tools/decode_glb.mjs`. Extract its bone/circulation references with `node tools/decode-reference.mjs`. Run `python3 tools/venous/refine_cavernous.py`, `python3 tools/venous/audit_cavernous_refinement.py` and the compressor for each refined asset. Remove `.authoring/venous/regional-replacement-v097.npz` when changing the volume recipe or baseline assets. It is an intermediate cache, not a production source.

For model renders, run `node tools/render-venous-comparison-decode.mjs ../comparison-v097 PATH_TO_V096_VENOUS PATH_TO_V096_CIRCULATION`, then `python3 tools/venous/render_refinement_views.py`. Supplied plates use the actual compressed delivered assets.
