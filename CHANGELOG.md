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
