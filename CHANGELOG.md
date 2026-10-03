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
