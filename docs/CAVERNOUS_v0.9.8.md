# Cavernous sinus and ICA review, v0.9.8

4 October 2026. Continues the v0.9.6 skull-base venous work and preserves the completed v0.9.7 medial ICA correction. This follow-up corrects the solid exclusion mask at open arterial label boundaries and retains the posterosuperior venous space. The changes are reference-guided teaching geometry, not a segmentation or registration of a patient's angiogram.

## Comparison and changes

| Finding in v0.9.6 | Change | Evidence and limits |
|---|---|---|
| Lower cavernous ICA sits unnecessarily lateral to the parasellar sphenoid | Smooth medial correction, tapering into the petrous and upper exits; the same coordinate field is applied to local branches and optional anastomoses | Coronal sections in the retained skull, normal arterial-mask venous angiography and published sellar ICA morphometry. Displacement is an authoring choice, not a measurement taken from an uncalibrated figure. |
| Cavernous sinuses resemble rounded sleeves beside the artery | Broader connected parasellar spaces, with different inferior/posterior and superior/anterior extents; explicit artery and inferred sellar-space exclusions | Normal angiography shows venous spaces around the carotid silhouette. Selective sampling DynaCT demonstrates irregular connected envelopes. Cadaveric work describes posterosuperior, anteroinferior and medial venous spaces. Detailed septations and nerves are not reconstructed. |
| Sellar cross-connections are regular round tubes | Smaller, vertically flattened anterior and posterior connections following the sellar margins | Selective venography and anatomical studies support variable anterior/posterior dural channels. This is one illustrative bilateral pattern. |
| A refitted parasellar body can separate from the lesser-wing channel | An anterolateral entry recess is retained and checked for continuity | The original whole-network skin must remain connected. No venous structure is silently removed to obtain a passing check. |
| Low ICA still overlaps the retained skull at the petrous/lacerum transition | Record the residual intersection rather than forcing further medial movement or opening an invented canal | The supplied skull does not fully resolve this canal. A matched thin-section CTA/CTV or arterial and venous CBCT dataset is needed to determine whether to change the skull lumen, the low ICA course, or their registration. |

The medial displacement has a maximum of approximately 3 mm in the local coordinate field, with a smaller superior adjustment. It fades to zero outside the lower siphon. This preserves the upper paraophthalmic curve and existing arterial labels. Surfaces sharing an original coordinate receive the identical deformation, retaining local segment and branch joins. Segment arc distances in catalogue metadata remain original authoring-template stations; they are not remeasured post-deformation lengths.

The cavernous sinus is not flattened wholesale onto bone. Its parasellar envelope is constrained by the sphenoid and petrous surfaces, while the venous space extends around the ICA. The inferred central soft-tissue exclusion prevents the cross-connections filling the sellar compartment. No pituitary gland is added to the rendered catalogue.

## How the references were used

Normal arterial-phase and venous-phase mask examples are the principal check on the ICA silhouette and venous outline. Selective cavernous/IPS sampling-based 3D images are used to check connected venous spaces, inferior extension and skull-base relationships. They are not treated as an exact normal calibre template: injection pressure, flow, compartmental filling and individual anatomy alter the visible envelope. Fistula images help interpret possible connections, but are not used to set normal size. Different subjects and unknown projection calibration prevent quantitative image-to-mesh error measurements.

The side-by-side renders use the same camera and scale for the before/after model. Reference comparisons are explicitly qualitative, with different subjects and projections. The review includes frontal, lateral, superior, oblique, posterior and inferior views, together with six coronal sections.

## References

1. Maksim Shapiro, **Neuroangio: Cavernous Sinus**. Original catheter angiography, arterial-mask venous-phase examples, selective sampling venograms and DynaCT cinematic renders courtesy Dr Matthew Young. https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/
2. Maksim Shapiro, **Neuroangio: Internal Carotid Artery and Its Aneurysms**. Normal siphon geometries and angiographic segment-boundary limits. https://neuroangio.org/anatomy-and-variants/internal-carotid-artery-and-its-aneurysms/
3. Harris FS, Rhoton AL. **Anatomy of the cavernous sinus. A microsurgical study.** J Neurosurg. 1976;45:169-180. DOI: 10.3171/jns.1976.45.2.0169. https://pubmed.ncbi.nlm.nih.gov/939976/
4. Cheng Y et al. **Anatomical study of cavernous segment of the internal carotid artery and its relationship to the structures in sella region.** J Craniofac Surg. 2013;24:622-625. DOI: 10.1097/SCS.0b013e3182801f30. CTA morphometry and its spread support checking sellar relationships without imposing one universal ICA position. https://pubmed.ncbi.nlm.nih.gov/23524760/
5. **Venous Anatomy of the Cavernous Sinus and Relevant Veins.** Anatomical and angiographic review of venous wall relationships and drainage variation. https://pmc.ncbi.nlm.nih.gov/articles/PMC10370663/

The original curated venous atlas and previous skull-base reference register remain available in VENOUS_v0.9.6.md. Source images reproduced in the review retain their attribution. They are comparison material, not models bundled into the running app.

## Verification and outstanding anatomy

The geometry report records the full network's connectedness, watertight winding, all 104 named venous labels, preservation outside the local replacement region, consistency of the arterial coordinate field and sampled artery/sinus/skull clearances. The actual displayed cavernous sinus and ICA triangle surfaces have no detected intersection lines on either side. Minimum sampled unsigned surface gaps are approximately 0.245 mm on the right and 0.257 mm on the left. These gaps are mesh-authoring clearance, not measurements of real dural or venous wall thickness. Bone clearance uses vertex sampling and is not an exhaustive triangle-level canal check. Neither test establishes clinical anatomical validity. The delivered losslessly compressed assets are decoded and tested with the viewer's Three.js loader and raycaster. The production build and UI fixture are also checked.

The most useful next anatomical improvement is a matched skull/ICA/venous segmentation around the petrous apex, petrolingual entry, sphenoid carotid sulcus and anterior clinoid. The present canal intersection remains an explicit limitation. Cranial nerves, petrolingual ligament, dural rings, pituitary and patient-specific septa are not rendered; their boundaries remain inferred. Bilateral symmetry, calibres and connection count are illustrative.

The new meshes replace existing assets. There is no additional runtime model copy or preprocessing step.

### Delivered validation

- [Geometry and topology](validation/venous-morphology-v0.9.8.json): one closed network, consistent winding and positive volume; 104 labelled veins; 196,494 exterior vertices preserved exactly.
- [Viewer fixture](validation/venous-viewer-v0.9.8.json): all 104 venous structures selected by actual raycasts; native and fallback rendering, ghosting, visibility, clipping and camera behaviour passed. This fixture is not a browser GPU performance benchmark.
- [UI fixture](validation/venous-ui-v0.9.8.json): tree, selection and layer controls passed.
- [Production build](validation/venous-build-v0.9.8.json): completed successfully. The existing large-JavaScript-chunk advisory remains.
- Installer integration checks passed with real Git and simulated Docker/GitHub/HTTP services. No deployment was performed.

The companion `Cavernous_Sinus_and_ICA_Review_v0.9.8.pdf` contains the six baseline comparison views, four reference comparisons, coronal sections and two direct v0.9.7 to v0.9.8 comparisons. Review and source images are excluded from the install ZIP.
