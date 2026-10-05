# v0.9.14

- Register Z-Anatomy brain and dural surfaces to the retained v0.9.13 skull through seven corresponding cranial bones.
- Add 172 named surface meshes, 69 triangle-bound regional vessel guides and two sparse course-guide sequences.
- Add brain orientation views, group focus, searchable labels and visible alternate names.
- Make translucent brain surfaces pass clicks through to vessels.
- Preserve the original four skull and vascular assets byte-for-byte. Existing vessels are not refitted.
- Include source attribution, transformation/provenance, machine-readable guide data and validation reports.

# v0.9.13

- Remove the upper cavernous ICA sleeve and rebuild one slim cavity with curved walls and an independently defined roof.
- Lower the intracavernous ICA region smoothly by up to 0.9 mm, preserving shared coordinates across adjoining segments and branches.
- Fit the medial cavity to the carotid sulcus while retaining the skull and smooth SOV, emissary, SMCV, lesser-wing and petrosal connections.
- Check inferior ICA enclosure and absence of the upper sleeve separately. The arterial label is not an anatomical dural boundary.
- Include matched views and coronal sections. Dural roof position remains inferred from model bone landmarks.

# v0.9.12

- Fit the slim cavernous envelope around the retained ICA course and to the medial carotid-sulcus bone.
- Retain curved lateral contours, the sellar exclusion and the direct venous entries.
- Add independent checks of ICA enclosure and medial bone apposition on the exported meshes.
- Preserve the arterial, anastomotic and skull assets and document the unresolved low skull-canal relationship.

# v0.9.11

- Replace the broad box-like cavernous body with a narrower curved profile and rounded edges.
- Rebuild the SOV and ovale emissary attachments and fit the cerebral/petrosal terminal channels to the smaller receiving space.
- Preserve thin intercavernous channels and direct basilar connections.
- Add checks for every direct cavernous attachment and each tributary's continuous route to its retained course.
- Retain all 104 venous labels and the completed arterial, skull and interface assets.

# v0.9.10

- Rebuild slimmer cavernous cavities with concave lateral walls and roofs.
- Replace the anterior joining plate with smooth terminal lesser-wing and SMCV channels.
- Weld both entries into the common venous skin with identical exported normals across label boundaries.
- Retain all 104 vein labels and the completed arterial, skull and interface assets.
- Add matched before/after views and independent contour, junction and clearance checks.

# v0.9.9

- Replace the bulbous cavernous envelope with defined wall profiles and a flatter roof.
- Make the outer lateral wall straight to gently concave, and reduce the domed posterior contour.
- Remove the anterior rounded recess; retain the lesser-wing connection through a thin flat entry.
- Retain the completed ICA, anastomotic and skull assets and GUI.
- Preserve all 104 venous labels and verify continuity, topology and cavernous ICA clearance.

# v0.9.8

- Retain the completed v0.9.7 ICA correction and refine the local cavernous venous envelope.
- Correct temporary artery exclusion masks at open label boundaries, restoring posterosuperior venous space around the displayed ICA.
- Preserve the lesser-wing entry and all 104 named veins in one connected, watertight network.
- Check the actual displayed sinus/ICA surfaces for intersections on both sides, and preserve 196,494 exterior venous vertices exactly.
- Add the follow-up geometry review and record the unresolved low petrous/lacerum skull canal relationship.

# v0.9.7

- Move the lower cavernous ICA medially with smooth transitions; apply the same coordinate deformation to local branches and anastomoses.
- Rebuild broader parasellar cavernous sinuses and flatter anterior/posterior sellar cross-connections.
- Retain the skull and GUI, and document residual skull-canal uncertainty.

# v0.9.6

- Rework the basilar plexus into a shallow, irregular interconnected clival network.
- Fit the lesser-sphenoid-wing channels separately from superficial Sylvian venous drainage.
- Rework cavernous/intercavernous spaces around the retained cavernous ICA and sellar bone.
- Fit superior and inferior petrosal sinuses to the petrous crest and intracranial petroclival groove, with corrected cavernous and jugular junctions.
- Flatten bone-facing transverse/sigmoid walls and refine jugular bulb calibre.
- Fit the marginal sinus to the foramen-magnum rim, vary calibre and add selected condylar communications.
- Preserve existing UI and v0.9.5 translucent rendering behaviour.

# v0.9.5

- Use cached Lambert lighting and one pass for translucent context, retaining the existing meshes and full opaque shading.
- Lower movement resolution to 0.75 pixel ratio, restoring the original resolution when settled.
- Dispose both cached material variants when closing the renderer.

# v0.9.4

- Add software, BodyParts3D and anatomical reference credits to a bounded, keyboard-scrollable section in the information modal.
- Include Neurointervention (Lynch, Renowden and White, Oxford University Press, 2026).
- Omit historical Z-Anatomy and the separate supplied-notes credit from the modal.

# v0.9.3

- Open the anatomy tree directly and remove the Layers/Anatomy tabs and mesh labels.
- Cycle each tree visibility control through visible, translucent and absent; apply group changes to descendants and indicate mixed states.
- Fade the desktop orientation toolbar until hover or keyboard focus.
- Use gentler camera focus with a 25% zoom-in cap, surrounding context and no cumulative selection zoom.
- Retain all v0.9.2 anatomy assets exactly.

# v0.9.2

- Refine venous morphology against the curated Borden, Bradač and Neuroangio angiograms.
- Fit the superior sagittal, transverse and sigmoid sinuses against the retained inner skull with oriented triangular/oval profiles.
- Smooth transverse/sigmoid courses and their jugular transitions; vary collecting-sinus calibre and taper peripheral veins.
- Retain all 104 venous structures and the v0.9.1 interface; preserve arterial, connection and bone assets exactly.
- Include source notes, authoring changes and geometry/viewer validation.

# v0.9.1

- Start Anatomy and inspection panels collapsed on desktop and mobile.
- Dock desktop panels to the bottom screen edges, expanding upwards beside the orientation toolbar; fade until hovered or keyboard-focused.
- Move Focus and Hide to the left of the orientation toolbar.
- Focus dims other visible structures, retaining the selected structure, its segments and immediate branches/tributaries; clicking elsewhere restores opacity.
- Keep the mobile title on one line and move anatomy checkboxes after the label.

# v0.9.0

- Add the principal dural sinuses, cerebral veins, posterior fossa collectors, extracranial veins and skull-base connections.
- Add note-derived descriptions and clickable drainage relationships, with incoming drainage labelled Receives from.
- Preserve the existing arterial and bony assets exactly.
- Render opaque veins in a separate multi-draw batch; retain picking, highlighting, ghosting and subtree hiding.
- Reveal the venous layer when a vein is selected from search or a description link.

# v0.8.11

## v0.8.12

- Set bilateral V3 and V4 starts from the latest black-line annotation.
- Move the paired ASA origins to the red-marked V4 level, keeping the shared vertebral collars welded and the central ASA confluence fixed.
- Retain the vertebral courses, calibre, other branch origins, all other anatomy and GUI. Re-triangulate only the affected vertebral wall patches without adding triangles.
- Update posterior spinal and posterior meningeal branch parents to the revised V3 regions.


- Lower both inferior labial main courses into the lower lip below the visible lower teeth.
- Lower both superior labial main courses slightly above the visible upper teeth.
- Raise the submental loops to follow the mandibular inferior surface.
- Preserve welded facial origins and existing mesh topology; transport four linked potential labial routes.
- Retain bones, other arteries, ICA/vertebral/ACA sections, descriptions and GUI.

# v0.8.10

- Correct cervical/petrous and petrous/cavernous boundaries on both sides to the user’s annotated ICA diagram.
- Retain the continuous ICA surfaces, upper ICA sections, vertebral/ACA sections and GUI.
- Retain all branch origins, welded junctions, descriptions and relationships.

# v0.8.9

- Correct bilateral V2/V3 and V3/V4 boundaries to the user’s annotated diagram, confining V3 to the shorter outer atlas loop.
- Preserve every vessel triangle position and normal; retain V1, ACA/ICA boundaries and GUI behaviour.
- Update branch segment parents to match their unchanged attachment points.

# v0.8.8

- Start both panels collapsed on mobile, preserving user choices afterwards.
- Capitalise relationship labels, including Branches to and Has segment.

# v0.8.7

- Rename the interface to Neurovascular Atlas; replace reconstruction summaries with a brief introduction and Jeremy Lynch’s 2026 authorship.
- Show loading progress based on model downloads and scene preparation; hide FPS when rendering settles.
- Use compact panel headers, symmetric mobile margins and scrolling confined to panel bodies.
- Remove Fit, the Side row and planned counts/labels.
- Group relationships by type with deduplicated, clickable structure names.
- Preserve all anatomy assets, definitions and structure descriptions.

# v0.8.6

- Add bilateral selectable vertebral V1–V4 and ACA A1–A5 sections, following the supplied notes.
- Preserve all existing vessel surface positions, normals and triangles exactly.
- Add section descriptions, search aliases and branch hierarchy; retain existing description links.
- Preserve whole-artery focus/highlight and subtree visibility, including the distal pericallosal group.
- Document estimated section boundaries where cervical vertebrae, corpus callosum and coronal suture are not registered.

# v0.8.5

- Add a subtle white FPS readout, measuring actual rendered frames and indicating idle without extra draws.
- Remove the selection panel close button and coloured title dot.
- Shrink the mobile logo and prevent overlap with search controls.

# v0.8.4

- Coalesce rendering into one render per browser frame, preserving idle rendering and camera damping.
- Update material shader state only when transparency or clipping configuration changes.
- Apply layer state in one refresh and cache full-model bounds for clipping.
- Batch 754 opaque vascular meshes on browsers with native multi-draw, preserving all positions, normals and triangles exactly.
- Preserve per-structure picking, focus, selection highlighting, hiding and ghost transparency, with the original path on unsupported browsers.

# v0.8.3

- Cap rendering pixel ratio at 1 during camera navigation and damping.
- Restore full sharpness 180 ms after movement settles, retaining the existing idle cap of 2.
- Preserve the model assets, anatomy, descriptions and selection behaviour.

# v0.8.2

- Add 717 descriptions from the supplied notes below Focus / Hide, with 1744 structure selection links.
- Omit the Description section when the notes provide no text.
- Match bilateral temporal branch names to the notes, clean up foramen rotundum names, and preserve former names as search aliases.
- Keep selection links on the existing focus path and preserve panel collapse state.
- Bundle the reviewed source catalogue and an optional content-import editing tool.

# v0.8.0

## v0.8.1

- Move both ophthalmic origins just distal to the anterior genu, retaining a curved proximal departure.
- Start each selectable paraophthalmic segment 1 mm of centreline arc before its ophthalmic origin.
- Preserve the ICA centreline, PCom/AChA origins and distal ophthalmic course.
- Include installer 0.7.2 with clear diagnostics for incomplete release archives.

- Add 190 named arterial branch meshes and expand to 167 separate potential routes.
- Correct generic orbital/ILT overlay endpoints and add facial, tympanic, pharyngeal, clival, odontoid, choroidal and pial network representatives.
- Refit ophthalmic and PCom origins and proximal arcs; keep seven selectable ICA regions per side with explicit anatomical parents.
- Add provisional arterial segment ranges, selected cortical origin variants, aliases and calibre provenance.
- Preserve both panel states when selection changes or clears, including collapsed inspection titles.
- Keep new tissue, venous, arch/access and full spinal modules deferred.

# v0.7.6

- Restore gentle proximal ophthalmic and PCOM curves while retaining corrected origins.
- Blend the shared terminal ICA, A1 and M1 surface.
- Add fourteen selectable ICA regions using the Shapiro endovascular classification, with colour coding and branches nested under their region.
- Support whole-ICA focus/highlight and consistent subtree visibility from details.

# v0.7.5

- Rebuilt bilateral ICA–M1 bifurcations and proximal branch junctions as shared, smoothed surfaces.
- Raised PCOM and anterior choroidal origins; lowered ophthalmic origins slightly and smoothed proximal courses.
- Matched panel titles at 13 px, reduced padding and spacing, and removed passage information and notes from structure details.

# v0.7.4

- Stack Layers/Anatomy and structure details on the left, with collapsible title bars.
- Remove 3/4 and Face camera buttons.
- Show readable relationship names and remove internal IDs from details and search results.
- Remove reference-reconstruction, provenance, confidence and review fields from structure details.
- Retain v0.7.3 anatomical geometry unchanged.

# v0.7.3

- Fixed terminal ICA/M1 junction distortion and rebuilt smooth lateral M1 courses.
- Preserved both v0.7.2 A1 surfaces exactly.
- Lowered ophthalmic origins and moved cavernous bends medially/posteriorly.
- Routed inferior alveolar arteries within the mandible and mental branches out through the visible mental-foramen regions.
- Restricted junction deformation and fairing to avoid moving unrelated artery surfaces.

# v0.7.2

- Corrected bilateral skull-base ICA entry, petrous course and cavernous/clinoid sweep.
- Added 33 selectable ICA skull-base reference landmarks under Skull.
- Carotid canal records now use the corrected course and separate entry/bend/exit regions.
- Ophthalmic origins follow the corrected ICA while their orbital-apex targets are retained.
- Branch junctions and potential ECA connections follow the same surface deformation.
- Geometry review remains an authoring operation only.

# v0.7.1

- Git-backed installation at `~/Documents/GitHub/neurovascular-atlas` using the permanent installer.
- Commit/push and GitHub Pages Actions deployment with the correct project base path.
- Check the served release after local Docker startup and retain the previous image on failed health checks.
- Exclude review screenshots from the install ZIP.
- No artery, bone or other model geometry changes.

# 0.6.2

- Added anatomy-tree visibility checkboxes with recursive subtree hiding/restoring and mixed states.
- Shared visibility state with detail-panel Show/Hide.
- Anatomy tab opens with all rows collapsed, without changing the displayed model.
- Nested all 34 potential ECA connections under their recorded source branches; retained recipient relationships.
- Vessel and bone geometry unchanged.

# 0.6.1

- Removed the screenshot-identified UI text, source list, connection toggle and preset buttons.
- Potential ECA connections are enabled automatically with the artery layer.
- Vessel and bone geometry unchanged.

# 0.6.0

- One combined model: bilateral ECA plus anterior and posterior circulation.
- Restored maxillary and mandibular alveolar processes, condyles and 32 teeth.
- Fitted left ECA, refined craniofacial routes and smoothed joined surfaces.
- Separate bilateral potential anastomosis overlay.
- Click-through ghosted bone, clipping-aware picking and a Face view.
- Removed historical anatomy assets and model switching.
- Lossless mesh compression, gzip serving and content-revision caching.
