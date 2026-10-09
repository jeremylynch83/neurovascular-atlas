# Audit continuation v0.9.50

This release continues the v0.9.48 relationship audit on the validated v0.9.49 baseline. It is a reference teaching reconstruction. The complete audit is not closed.

## Implemented

- Constrained local petrosal shaft fitting, with every native shared collar coordinate fixed and nearby arterial courses protected.
- Bilateral selectable inferior alveolar, infraorbital, central retinal, selected CPA internal auditory and regional vertebral periarterial venous surfaces.
- Named drainage relationships, authored reference paths, source citations and explicit review status for every new label.
- Correction of the transverse sinus support screen: the original bone set omitted adjacent parietal bone. The existing lateral course is retained.

All new calibres are illustrative. The inferior alveolar representation stops before dental terminal branches. Retinal courses represent a selected superior ophthalmic drainage variant. The anterior meningeal trial was rejected for collisions and is not included. Internal auditory courses show a selected CPA route, not the entire intrabony labyrinthine venous system. The vertebral addition is a selected connected regional plexiform component, not a claim of complete microscopic anatomy.

## Still open

Fine orbital/skull-base guides need independent bony route definitions. Hypoglossal, internal acoustic, inferior alveolar and infraorbital canal containment cannot be certified by this coarse skull. Cervical vertebrae, exact foraminal levels, nerves and optic nerve/globe anatomy are absent. Mastoid emissary and posterior condylar routes need reliable aperture definitions and a selected variant. Medial petrosal free outlet transitions remain under anatomical review.

Existing baseline self-intersections and contacts are retained where outside the accepted corrections. Numerical checks do not establish clinical accuracy, lumen patency, exhaustive venous coverage or whole-atlas watertightness.

## Verification

The production build and actual Three.js/Meshopt loader are checked after export. Full reports are in `docs/validation/relationships-*-v0.9.50.json`. New surfaces are checked for closed manifold edges, degenerate faces and non-adjacent triangle intersections. Existing surfaces are compared against exact original face IDs, and native shared collars against original coordinates. Skull, brain and arterial assets are retained byte for byte.

Bone contacts along unsegmented canal corridors remain open findings, explicitly separated from intended venous receiver attachments. See `relationships-v0.9.50.json` and `audit-register-v0.9.50.json`.

The before-and-after PNG renders exact mesh triangles with matched cameras and scale. Vessels are isolated for inspection; the image does not prove bone containment.

## Audit register

| Item | Status |
| --- | --- |
| Incorrect left incisive and orbital MMA passage associations | resolved in v0.9.49; retained |
| Facial/deep facial and superficial temporal pairing | regional correction retained from v0.9.49; anatomical variants remain |
| Frontal MMA surface support | regional tubular rebuild retained from v0.9.49 |
| Lateral transverse sinus skull apposition | screen reconciled; no displacement needed |
| Superior and inferior petrosal shaft support | partially implemented |
| Inferior alveolar and infraorbital venous companions | selected bilateral proximal/reference courses implemented |
| Central retinal venous companion | selected bilateral ophthalmic drainage reference implemented |
| Paired anterior middle meningeal veins | open; trial rejected |
| Internal auditory veins | selected bilateral CPA drainage reference implemented |
| Vertebral venous system | regional plexiform component implemented; full fit open |
| Hypoglossal and internal acoustic canal containment | open; requires detailed canal segmentation |
| Supraorbital, ethmoidal, stylomastoid and Vidian guides | open; requires independent route/foramen definition |
| Mastoid emissary and posterior condylar veins | open; requires variant selection and reliable bony aperture definitions |

## Reproduction

Decode the exact v0.9.49 model assets using `tools/decode-posterior-baseline.mjs` into a work directory `decoded/`. Then run the scripts under `tools/audit-finish-v0950/` with that work directory as the first argument: `fit_sinuses.py`, `limit_deformation.py`, `extract_companions.py`, `add_veins.py`, `add_vertebral_plexus.py`, `add_retinal.py`, `repair_infraorbital.py`, `validate.py`, `self_check.py`, `check_components.py`, `export.mjs`, `catalogue.py`, production build, `check_export.mjs`, `report.py`, and `render_comparison.py`. Run from the app directory. Python scripts take the work directory as their first argument. The Node exporter takes `work/candidate` and the exact v0.9.49 GLB directory; the Node loader check takes `work/candidate` and `work/decoded`. Evidence and reference paths are included; transient decoded buffers are excluded from delivery.
