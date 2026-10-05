# Registered brain and dural context, v0.9.14

Built directly from the supplied **v0.9.13** application. The four existing skull and vascular GLBs and all pre-existing catalogue rows are unchanged. This release adds orientation anatomy and reproducible course guides for the next vessel-authoring stage.

## In the app

Open **Layers and anatomy → Brain and dura**. The tree contains cerebral hemispheres with lobes and cortical parcels, brainstem, cerebellum, deep structures, ventricles, falx/tentorium and vessel course landmarks. Each surface is selectable and has independent opaque, translucent and hidden states. Selecting a hidden brain structure or guide reveals it. The **Brain overview** and **Deep / posterior fossa** buttons show useful combinations with the existing veins.

Search includes alternate names, including *brachium conjunctivum*, *crus cerebri*, *Aqueduct of Sylvius* and *cerebellar tonsil*. The inspection panel displays **Alternate names** when present, for all anatomy, including existing vessels. Selected surface-guide markers have on-scene labels; all named surface meshes highlight and show their names in the inspection panel. Translucent brain and bone surfaces do not intercept vessel picks. Opaque brain surfaces remain selectable.

## Included anatomy

- 172 individually labelled source meshes, 363,132 triangles, with one geometry copy per structure.
- Both cerebral hemispheres, organised by lobes and source cortical regions.
- Paired midbrain, cerebral peduncles, superior/inferior colliculi, pons and medulla.
- 31 cerebellar parts, including hemispheric lobules, vermian lobules, tonsils, flocculi and superior cerebellar peduncles.
- Falx cerebri and both tentorial halves.
- Lateral, third and fourth ventricles and cerebral aqueduct.
- Thalami, hippocampi, corpus callosum, caudate nuclei, fornices, choroid plexuses, septum pellucidum and hypothalamus.
- 69 regionally selected points bound to exact surface triangles, plus two sparse illustrative course-guide sequences.

The source has no separately labelled middle or inferior cerebellar peduncles. Their labels have not been invented. Cerebellar lobules are simplified. Cortical parcel seams and brainstem cut surfaces come from the source model.

## Registration

The brain is not independently eyeballed into the skull. Seven corresponding cranial bones from the same Z-Anatomy FBX collection were registered to the actual retained v0.9.13 skull: frontal, occipital, sphenoid, both parietals and both temporals. A robust similarity ICP fit used per-bone nearest-vertex correspondences, an 85% trim and one shared rotation, translation and uniform scale. The transformation was then applied to every selected brain and dural part. No brain-specific warp or vessel-driven adjustment was applied.

Source FBX object transforms were baked, centimetres converted to millimetres, and [0, -1620, 0] mm subtracted for the source-orientation asset. That asset has +X anatomical left, +Y superior and +Z anterior. The committed matrix converts it to the application's **RAS millimetres**. Scale is **0.968998**. Full precision matrix, source hashes, axes and per-bone residuals are in `anatomy/source/brain/registration.json`.

Median nearest-vertex skull residuals are approximately 0.26–0.52 mm for the vault/occipital/sphenoid and 2.04–2.08 mm for the temporal bones; temporal 95th percentiles are approximately 5.4–5.5 mm. These are mesh-correspondence residuals, not an anatomical accuracy claim. Differences in source shapes and tessellation remain. The review image shows actual registered surfaces from anterior, superior, lateral-section and posterior-fossa views. Close surface approaches are recorded in the validation report; this is not a certified collision-free or patient-specific model.

## Semantic vessel placement

`public/anatomy/brain-landmarks.json` exposes the registered surfaces and guides independently of the UI. The main manifest carries the same bindings. Each guide has:

- Stable structure ID, readable name, side and aliases.
- `surfaceAnchor.structureId`, exact `triangleIndex`, three `barycentric` weights and RAS `position`.
- Registration ID and full registered-asset SHA-256, to reject stale bindings after a mesh change.
- `vesselGuide.vesselNames` for intended regional use, resolved `vesselIds` for existing veins, and `surfaceStructureIds`.
- `located_on` and `course_landmark` relationships. These are orientation relationships, not drainage or physical vascular junctions.

`src/brainAnchors.ts` provides `resolveSurfaceAnchor(anchor, geometry, assetSha256)` and `vesselCourseGuides(manifest, vesselId)`. `AnatomyEngine.resolveBrainAnchor(id)` resolves a guide against the loaded geometry and checks the registration ID. The selected marker uses that resolved point. Both the normal build validator and geometry tests verify persisted positions against triangle weights.

Landmarks are **regional course guides**. Their triangle binding is exact on this model, but selecting the anatomical region is approximate. For example, a fourth-ventricular boundary is a spatial reference, not an attachment to a CSF lumen; a tentorial free-edge region is not a segmented venous sinus. Dashed lines connect sparse guide stations and are not fitted vessel centrelines. Future vessels should be fitted along the relevant surfaces/cisterns and connected to separately reviewed venous targets. Existing 9.13 vessel courses have not been refitted in this release.

## Reproduction and checks

Normal installation uses the committed geometry: `npm ci`, `npm test`, `npm run build`. No FBX conversion, registration, VTK or external dataset download occurs during a normal build. The existing Docker and installer workflow is retained. `./docker.sh` runs the extracted app locally; the existing `inr-anatomy.sh` supports its documented local and publishing modes.

Authoring only: `python3 tools/brain/build_brain.py` rebuilds the registered asset, labels and guides from the included source-orientation GLB and registration matrix. It requires NumPy, Trimesh and VTK. Source names are preserved in `source-manifest.json` and `label-map.json`. The optional `fit_registration_reference.py` accepts an independently extracted source-skull GLB, a decoded reference directory and an output path; it is not part of routine builds.

Checks cover all GLB node references, hierarchy, sided centroids, barycentric locations, stale-hash rejection, alternate-name search, group membership, vessel-guide lookup, ghost-brain click-through, existing venous ray picking and visibility/focus behaviour. Reports are under `docs/validation/brain-*` and `venous-*-v0.9.14.json`. Build and browser verification results are recorded in the release validation report.

## Sources and licences

- Z-Anatomy official PC-Version [NervousSystem100.fbx](https://github.com/LluisV/Z-Anatomy/blob/PC-Version/Resources/Models/FBX/NervousSystem100.fbx) and [SkeletalSystem100.fbx](https://github.com/LluisV/Z-Anatomy/blob/PC-Version/Resources/Models/FBX/SkeletalSystem100.fbx), retrieved 5 October 2026. The official download README notes that FBXs may not be the newest atlas release.
- [Original source licence](https://github.com/LluisV/Z-Anatomy/blob/PC-Version/Resources/Models/License.txt). Z-Anatomy CC BY-SA 4.0; original BodyParts3D credit retained. The selected subset excludes unrelated inner-ear and other mixed-licence assets. Adapted brain GLBs remain CC BY-SA 4.0, separate from the app-code licence. The original licence text is included in `public/anatomy/licenses/`.
- Regional venous context: Neuroangio [posterior fossa veins](https://neuroangio.org/venous-brain-anatomy/veins-posterior-fossa/), [precentral cerebellar vein](https://neuroangio.org/venous-brain-anatomy/precentral-cerebellar-vein/), [fourth ventricle and its veins](https://neuroangio.org/venous-brain-anatomy/4th-ventricle-and-its-veins/) , [internal cerebral vein](https://neuroangio.org/venous-brain-anatomy/internal-cerebral-vein/) and [deep venous system](https://neuroangio.org/venous-brain-anatomy/deep-venous-system/). No Neuroangio images are embedded in the application.

Validation outcome: catalogue validation and production build passed. Chromium 134 with software rendering loaded the production build with no page errors or unresolved mesh warnings. Orientation presets, alias lookup/panel, regional markers, focus, show/hide and section controls passed. This environment does not establish performance on a physical GPU. Vite reports its existing large-bundle advisory (about 935 kB); the build completes successfully.
