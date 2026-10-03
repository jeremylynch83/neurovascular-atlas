# Structure descriptions and names, v0.8.2

The inspection panel displays a Description section immediately below Focus / Hide when the selected structure has text from the supplied notes. There are 717 descriptions and 1744 inline links. Other structures have no Description heading or placeholder.

Links select and focus their exact stable model ID through the existing selection handler. Left/right and explicit contralateral links retain their reviewed targets, including legacy left ECA IDs. Inspection titles, highlighting and focus follow the selected structure. Panel collapse state is preserved.

## Names

- STA-origin temporal branches: Posterior deep temporal artery, right and left.
- Maxillary-origin temporal branches: Middle deep temporal artery, right and left.
- Artery of the foramen rotundum, right and left: remove the duplicated artery wording.
- Inferior dental and posterior superior dental are searchable aliases for their equivalent alveolar entries.

Stable IDs and GLB node bindings are retained. Former display names remain search aliases. The three anatomy assets and their content hashes are unchanged from v0.8.1.

## Content and implementation

The authoritative source is the supplied nv(2).pdf. The reviewed content, source pages and anatomy amendment record are retained in STRUCTURE_DESCRIPTIONS.md. The geometry amendments in that record, including the medial palpebral supply and AICA branch-course mapping, remain for a separate model update. This release applies descriptions and display terminology.

The description renderer supports the catalogue’s paragraph and structure-link format. React renders the prose as text; no HTML is injected. Unknown link targets fall back to plain text. No Markdown dependency has been added.

The optional tools/import_structure_descriptions.py editing tool imports the reviewed document into anatomy/generated/complete_manifest.json. It is not an installation or startup step.

## Checks

- Production builds for the local root and GitHub Pages subpath.
- Actual App/Detail/Description component checks for selection and focus, same-side and contralateral targets, panel state, field omission and placement.
- All 1744 inline link handlers select a valid catalogue structure.
- New names and dental aliases resolve in search; text is escaped safely.
- Catalogue links, stable IDs, asset bindings and byte-identical anatomy assets checked before packaging.

The component interaction checks do not claim an end-to-end browser test.
