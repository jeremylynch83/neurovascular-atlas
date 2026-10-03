# Current release

v0.6.0 uses one combined bilateral scene. See [V0.6.0.md](V0.6.0.md) for current packaging, fitting and validation changes. The historical workflow below records how its retained source geometry was developed; older scene-installation steps are superseded.

# Reproducible neurovascular modelling workflow

Recorded 2 October 2026. Current reference: right ECA Draft 03, app v0.3.7.

## Purpose and scope

This record describes how the ECA model was created and refined, preserves the editable inputs, and defines checks for the next ICA/anterior and vertebral/posterior circulation models. Those next territories have not been built in this release.

The model is a composite teaching reconstruction. It is not a segmentation of one patient. Vessel calibre, transverse depth, soft-tissue relations and exact foraminal positions remain estimated unless separately documented. A visually smooth model is not evidence of anatomical accuracy.

## Source register

| Source | Use | Limits |
| --- | --- | --- |
| Existing BodyParts3D-derived skull, mandible and hyoid | Fixed bony context and geometric clearance checks | Original atlas resolution; several bones are open meshes. Not the TopBrain CT skull. Recorded CC BY-SA 2.1 Japan attribution applies. |
| Kiyosue, *External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment*, Springer, 2020, DOI 10.1007/978-981-15-4786-7 | Branching hierarchy; selected DSA curves; MPR relationships; skull-base routes | Different subjects and many pathological examples. Uncalibrated printed projections do not determine true diameter or 3D depth. |
| Borden, *3D Angiographic Atlas of Neurovascular Anatomy and Pathology*, 2006, cervical vasculature chapter, printed pp44–45 | Independent text cross-check of maxillary branching and the MMA skull-base/inner-table course | Cross-check, not an independent patient reconstruction. |
| Alvernia JE, Fraser K, Lanzino G. *The occipital artery: a microanatomical study*. Neurosurgery. 2006;58(1 Suppl):ONS114–22. DOI 10.1227/01.NEU.0000193519.00443.34. https://pubmed.ncbi.nlm.nih.gov/16543868/ | Occipital digastric, suboccipital and subgaleal segments; descending branches | Cadaveric anatomical reference. No coordinates or subject-specific registration transferred into this model. |

Kiyosue figures used: 4.3b (PDF p96, printed p93) for maxillary, basal MMA and STA; 5.8b (PDF p122) for frontal MMA; 5.9 MPRs for skull-base depth; 2.8/2.10 for facial/lingual; 3.3 for occipital; 3.13/3.16 for ascending pharyngeal; 4.1/4.2 for auricular branches. Manual pixel traces and source identifiers are retained. Copyrighted book pages and angiogram images are not included in the app.

## Coordinate contract

Use one anatomical coordinate system for modelling, collision checks and rendering.

- App and Draft 03 authoring data: RAS millimetres, +X anatomical right, +Y anterior, +Z superior.
- Earlier control-point JSON: legacy centimetres, −X anatomical right, +Y superior, +Z anterior.
- Convert legacy coordinates to app coordinates with `(-10*x, 10*z, 10*y)`.
- The standalone Draft 02 GLB used RAS metres. Multiply its positions by 1000 for the app.
- AP camera looks from anterior, with superior upwards and the patient's right on the left of the image. Right lateral looks from +X.

Check actual decoded world coordinates. The original legacy GLBs used compressed/quantised geometry: Three.js was used to decode and bake their world transforms before exporting the reference coordinates. Reading raw integer accessors as physical coordinates is incorrect.

The ECA tree belongs to the legacy skull used to construct it. Keep TopBrain in a separate scene until an explicit registration has been performed and checked.

## Stage 1: branch graph and initial curves

1. Define stable IDs, names, parents, side and source references before creating meshes.
2. Choose and document the represented anatomical variant. Keep uncommon anastomoses or variants separate from the default model.
3. Set control points using branch origins, anatomical landmarks, foraminal routes, territories and several reference projections.
4. Sample smooth cubic centreline curves by arc length. Attach child origins to their parent curve, with a local transition that avoids a kink.
5. Use estimated proximal and distal radii initially. Keep these estimates labelled.
6. Sweep circular sections with a transported local frame, avoiding frame flips along tortuous curves.

Draft 01 contained 81 named right ECA segments. The original authoring script and control-point JSON are retained in the reconstruction inputs.

## Stage 2: angiogram-guided refinement

The first model was too diagrammatic. Draft 02 revised 42 courses against the supplied angiograms.

- Preserve manual image-space samples rather than relying on memory of the images.
- Map lateral image samples into superior/anterior coordinates around a known origin and an explicit scale. The chosen DSA example was left-sided and was mirrored for the right-sided model.
- Infer transverse depth separately from MPRs, branching relationships and skull context. Record that depth is estimated.
- Fit reference curves to the actual skull in use. Different subjects cannot be overlaid without registration.
- Exclude tumour-directed terminals and pathological feeder enlargement. Do not copy a pathological calibre merely because its course is clearly visible.
- Preserve local bends and unequal branch lengths. Avoid mechanically regular sinusoids.
- Replace uniform taper with monotone piecewise radius profiles using PCHIP interpolation. Check daughter calibre against the local parent calibre.
- Fit selected meningeal courses to the inner cranial surface and scalp courses to the outer surface, then smooth the displacement field rather than erasing the original local tortuosity.

Draft 02 used 40 radial tube samples and approximately 0.22 mm longitudinal spacing. This is mesh sampling resolution, not evidence resolution.

## Stage 3: corrections prompted by expert review

### A. Branch junctions

Problem: each branch was an independently capped solid. Their overlapping surfaces left visible disks, shoulders and seams, especially at the ECA–STA–maxillary division.

Correction:

1. Recover the exact dense centreline samples and radii from the approved Draft 02 tube rings. The saved sparse control points alone do not reproduce its final skull-constrained surface.
2. Rebuild the branch solids and audit unintended branch contacts before joining them.
3. Form a boolean union with Manifold3D, retaining each source branch's face provenance.
4. Refine long boolean-cut/cap triangles to a target edge length of 0.32 mm.
5. Fair the surface locally at branch origins. The blend weight falls to zero beyond approximately 3.2 local parent radii, with a minimum zone of 0.65 mm. The terminal ECA division receives an additional local rounding pass.
6. Calculate normals on the whole joined surface before partitioning it into the 81 named display parts. Export those normals so lighting remains continuous across colour/selection boundaries.

The whole surface is closed. The named display parts share open interfaces where they join. They are no longer independently closed tubes. Hiding a neighbouring part can expose a cut interface, which is an expected display consequence.

Avoid joining every nearby vessel blindly. A boolean union can create an unintended anastomosis. The contact audit identified overlapping courses around the lingual/ascending pharyngeal region, a recurrent contact of an STA twig, and the deep temporal/MMA region. Small local depth edits and temporal surface corrections are explicit in the script. Closely adjacent maxillary origins remain within the local branching region; the buccal and posterior superior alveolar courses already shared one origin in Draft 02.

### B. Occipital trunk and bone relations

Problem: the earlier surface constraint only acted above legacy Y=6 cm, equivalent to RAS Z=60 mm. The lower occipital/suboccipital course could therefore pass through the occipital bone. Checking only a few control points also missed collisions between them.

Correction:

1. Check the complete dense occipital trunk, including its inferior course, against the solid occipital mesh.
2. Find the outer bony intersection along an anatomical outward ray from an approximate cranial centre.
3. Require clearance for the whole vessel radius, not just its centreline. The safety margin is a modelling allowance, not a measured tissue thickness.
4. Smooth the displacement along the course, then check the resulting surface again. Follow the parent displacement when updating child origins.
5. Apply the extracranial constraint to the lateral/medial scalp courses and descending muscular branch. Do not apply it indiscriminately to the mastoid branch, whose intended bone-entering route is retained.
6. Check the actual triangles of the final surface against bone, not just the pre-mesh centreline.

The occipital artery's initial course is deep in soft tissues; "outside bone" does not mean subcutaneous throughout. Its distal subgaleal course and its bone-entering branches require different constraints.

The same review also corrected selected superficial/posterior auricular and deep temporal relations. Temporal corrections use a smoothed upper envelope of the required displacement so a height boundary does not introduce a sharp step in the course. A deep temporal course and a superficial scalp course must not be forced onto the same surface offset.

The terminal ECA and proximal daughter courses were also moved behind the mandibular neck with a local posterior clearance rule. Restrict this rule to the proximal maxillary artery; applying it to its full course displaces the deep course incorrectly. For the lower deep temporal artery, use the first local lateral exit from temporal cortex, preserving its position deep to the zygomatic arch. An outermost cranial ray is inappropriate there.

After bone correction, smooth the ECA displacement field before updating child origins. A sharp local bend had produced a folded tube and an unintended handle when the daughter solids were joined. Smoothing the correction over 12 dense samples removed this defect while retaining bone clearance. A bounded junction kernel, 0.96 times the terminal parent radius, fills the central saddle; it is assigned to the ECA surface. Confirm the resulting surface topology rather than assuming that smoothing alone is sufficient.

### C. Checks added because of these failures

- Evaluate dense paths and final surfaces. A control-point-only check is insufficient.
- Audit centreline sampling after a constraint: large jumps between consecutive samples reveal a new kink.
- Compute actual bone/artery triangle contacts and signed distance where the bone is closed.
- Treat signs from an open bone mesh cautiously. An open mandible or maxilla can produce misleading negative signed distances far from the bone; review actual contact and the relevant anatomical compartment.
- Check branch count, positive volume, finite vertices, consistent winding, connected components and topology.
- The current ECA tree should have one component and no loops: Euler characteristic 2/genus 0. This rule is specific to this represented tree, not to every arterial territory.
- Inspect matched-view, matched-scale before/after renders (centre the junction on its updated location), including an opaque-bone view and a monochrome close-up of the main junction. Transparent bone and family colours can conceal errors.

## Rebuilding the current model

The installable archive includes `anatomy-source/eca/authoring/` with dense Draft 02 inputs, original control points, manual trace metadata, skull reference geometry and the refinement scripts. Patient data and reference page images are not needed to rebuild Draft 03 from these recorded inputs.

From that directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python draft03/refine03.py
python draft03/validate03.py
```

The outputs are `draft03/ECA_Right_Draft03_mm.glb`, the joined surface, dense centreline JSON, geometry checks and validation results. This authoring environment is separate from the ordinary app installation. The normal installer uses prebuilt GLBs and does not need these modelling packages.

The historical `build.py` and `refine.py` document Stages 1 and 2. They write their own stage outputs. The shipped Draft 02 dense input is the preserved baseline for Stage 3 and should not be replaced without an intentional new review.

Pinned authoring versions are recorded in `requirements.txt`. The app's deterministic anatomy validation also checks its structure IDs, source references, hierarchy and GLB node bindings.

## Updating the application

1. Copy the new RAS-mm vessel GLB to `public/anatomy/models/eca-reference.glb`.
2. Preserve stable structure IDs and update the ECA manifest's title, geometry notes and source references.
3. Refresh model hashes and build the browser manifests with `./build-anatomy.sh`.
4. Run `npm run build` and load the production viewer in a real browser.
5. Check the default model, all 81 vessel parts, shared normals/colours, AP orientation, search/selection, layer controls and switching to CT and back.
6. Package the app with its prebuilt assets and process record. Verify the extracted ZIP's anatomy setup and reuse of the retained TopBrain reference.
7. Preserve the previous release and provide the new ZIP for the existing permanent `inr-anatomy.sh` installer.

## Next time: ICA/anterior and vertebral/posterior circulation

Begin with a new source and branch register using this same coordinate frame. Review the intended variant and landmarks before drawing dense paths.

For the ICA/anterior circulation, explicitly anchor the carotid canal, petrous course, cavernous course, clinoid/dural transitions and intracranial branches. Add appropriate brain and dural context to constrain cisternal and cortical courses. A skull surface alone does not define those courses.

For the vertebral/posterior circulation, anchor the cervical transverse foramina, atlas groove/V3, dural entry and foramen magnum, then relate the intracranial vertebral, basilar and cerebellar branches to the brainstem and cerebellum. Do not estimate these territories only by projecting onto the skull.

Assign each segment a compartment: extracranial soft tissue, bone canal/foramen, dural, cisternal or pial. Record allowed bone entry/exit landmarks and choose inner/outer surface rules per segment. Avoid a universal bone-repulsion rule.

Retain source images privately where authorised, record reference views and uncertainty, and generate small regional review renders before adding distal detail. Use a calibre source appropriate to each territory; carry no ECA radius assumptions into the intracranial model.

Set the expected graph topology deliberately. The circle of Willis contains intended connections and may contain loops; the ECA genus-zero rule must not be applied to it unchanged. Do not create an anastomosis from a geometric collision or silently choose a hypoplastic/aplastic variant.

Finish each territory with expert review of course, branching, calibre, bone/brain relations and allowed variants. Numerical checks support that review and do not replace it.

## ICA/anterior extension

The first bilateral anterior circulation draft is now recorded in [ANTERIOR_MODELLING.md](ANTERIOR_MODELLING.md). It adds an explicit compartment rule, a separate potential-anastomosis graph/overlay, smooth skull-base displacement fitting, and validation against the existing ECA as well as the skull. The posterior extension is recorded below.

## Posterior extension and shared junction rule

See [POSTERIOR_MODELLING.md](POSTERIOR_MODELLING.md). Build one graph across circulation boundaries. A continuous parent-to-daughter loft must precede union where separately capped tubes produce shoulders. Include every actual endpoint connection in the junction smoothing list, calculate normals on the complete skin and only then split labels. Inspect junctions with connected neighbours visible, and validate the deliberately chosen graph cycles. Record missing tissue constraints instead of treating the skull as a substitute brain surface.
