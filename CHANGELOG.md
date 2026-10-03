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
