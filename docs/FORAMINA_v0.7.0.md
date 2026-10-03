# Skull passages and vessel course revision, v0.7.0

This release adds a searchable register of 64 opening/passage types, represented by 121 side-specific entries. There are 65 located regions. Selecting a located entry in **Skull → Foramina and passages** focuses the camera and displays a marker and any recorded course. Markers appear only while selected; a dashed line denotes a reference corridor, not a segmented canal. The detail panel records connected spaces, contents, associated vessels and mesh-resolution status.

## Geometry changes

- Both infraorbital courses now follow the inferior orbital fissure / orbital-floor corridor towards the visible anterior maxillary depression. The anterior superior alveolar origins follow their parent.
- Both MMA frontal courses and selected convexity branches are fitted to the inner cranial surface. The proximal intracranial MMA and petrosquamosal course are adjusted with them. Canal-directed orbital/petrosal branches retain their separate destination rules.
- Both petrous ICA bends are lowered and redirected towards the temporal carotid-canal region, with the superior lacerum relationship retained.
- Both proximal ophthalmic courses are redirected towards the estimated optic-canal region medial to the superior orbital fissure.
- Both arteries of foramen rotundum and accessory meningeal routes are redirected through the visible rotundum and ovale openings.
- Parent attachments are propagated to affected daughter branches. The 34 potential ECA connection curves retain their donor/recipient relationships and follow the moved endpoints.

The original joined vascular skin is transported along the edited centrelines, preserving its circular offsets and shared label vertices. Local seam fairing is performed on the complete skin, and normals are calculated before splitting it into named parts. The bone asset is unchanged. There is no drilling of invented canals and no change to the intended arterial graph.

## Limits that remain

**This is a regional correction, not certification of every artery passing through a fully modelled canal.** The current skull mesh does not reliably resolve a continuous optic, carotid, infraorbital or spinosum lumen. Its maxillae and temporal bones also contain open mesh boundaries. Those routes remain explicitly estimated or partially supported. In particular, the ophthalmic route is an anatomical region estimate, not a demonstrated optic-canal fit. Some intended intraosseous arterial surfaces therefore still overlap the coarse bone representation.

The register distinguishes:

- **Visible:** an opening is identifiable; the stored point is a manual anchor, not a segmented lumen.
- **Partial:** an opening/depression or part of a corridor is identifiable, but its complete lumen is not.
- **Regional:** adjacent bone supports a regional estimate; the named opening is not individually resolved.
- **Unresolved / variant unresolved:** no reliable point or assumed variant route is supplied.
- **Bone unavailable:** the registered cervical bone needed for the assessment is absent.

All entries remain unreviewed. Small foramina, variant emissary canals, sinus ostia and intraosseous dental routes are listed rather than silently omitted. Registered cervical vertebrae, optic nerves and brain/dural context are still needed for their respective detailed route constraints. The opening register does not imply that veins or nerves have been added to the rendered scene. Decimal coordinates are reproducible authoring values, not a claim of anatomical measurement precision. The left anchors use the skull's approximate symmetry plane where appropriate, with a separate maxillary adjustment; they are not independent patient measurements.

## Checks and when to repeat them

The geometry audit is a **one-off authoring operation**, not an additional app-build or installation stage. The app loads prebuilt assets. Ordinary UI edits do not rerun it. Revisit the saved regional audit only when its artery or bone geometry changes. Input/output SHA-256 hashes are recorded with the audit to identify the geometry reviewed.

- Actual exported mesh: finite vertices, positive volume, consistent winding, watertight joined skin and unchanged face incidence / intended genus 2.
- Actual MMA surface samples: first intersection with the inner skull surface, before and after. Sampling interval is 0.5 mm spatially; this is not an exhaustive triangle-intersection proof.
- Matched-view before/after renders, with opaque and translucent bone.
- Catalogue bindings, TypeScript/build, existing subtree hiding and potential ECA nesting, and landmark search/focus/visibility/disposal behaviour.
- Meshopt compression is lossless and checked by decoding every buffer view.

The final regional MMA check sampled 9,415 exported surface vertices across 12 bilateral convexity parts: 0 samples beyond the first inner-table intersection. Minimum recorded radial clearance was 0.237 mm. This result is specific to those parts and that sampling method.

Partial/unresolved canals deliberately receive no false canal-clearance pass. See the JSON reports and the review images under `docs/review/`. Historical v0.6.0 geometry reports refer to their original meshes, not this revision.

## Anatomical references

The original Kiyosue and Borden source register remains in `MODELLING_WORKFLOW.md`. Additional checks used:

- [Anatomy of the infraorbital artery and its orbital branch](https://pmc.ncbi.nlm.nih.gov/articles/PMC12043843/).
- [Optic Canal: Microanatomic Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC1661800/).
- [ICA segments, anatomical study](https://pubmed.ncbi.nlm.nih.gov/15849455/).
- [MMA morphometric organisation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3699209/).

These establish anatomical relationships; no coordinates were transferred from another patient or publication.

## Opening inventory

| Region | Opening or passage | Mesh assessment |
| --- | --- | --- |
| Orbit | Optic canal | regional |
| Orbit | Superior orbital fissure | visible |
| Orbit | Inferior orbital fissure | visible |
| Orbit | Infraorbital groove and canal | partial |
| Orbit | Infraorbital foramen | partial |
| Orbit | Anterior ethmoidal canal | regional |
| Orbit | Posterior ethmoidal canal | regional |
| Orbit | Supraorbital notch or foramen | partial |
| Orbit | Frontal notch / supratrochlear exit | regional |
| Orbit | Zygomaticofacial foramen | unresolved |
| Orbit | Zygomaticotemporal foramen | unresolved |
| Orbit | Cranio-orbital / meningolacrimal canal | variant-unresolved |
| Orbit | Accessory optic canal | variant-unresolved |
| Orbit | Nasolacrimal canal | regional |
| Anterior base | Cribriform foramina | regional |
| Anterior base | Foramen caecum | unresolved |
| Middle base | Foramen rotundum | visible |
| Middle base | Foramen ovale | visible |
| Middle base | Foramen spinosum | regional |
| Middle base | Foramen lacerum | partial |
| Middle base | Sphenoidal emissary foramen (Vesalius) | variant-unresolved |
| Middle base | Greater petrosal nerve hiatus | unresolved |
| Middle base | Lesser petrosal nerve hiatus | unresolved |
| Temporal bone | Carotid canal | partial |
| Temporal bone | Caroticotympanic canaliculi | unresolved |
| Temporal bone | Internal acoustic meatus | regional |
| Temporal bone | Facial canal | unresolved |
| Temporal bone | Stylomastoid foramen | partial |
| Temporal bone | External acoustic meatus | partial |
| Temporal bone | Petrotympanic fissure | partial |
| Temporal bone | Tympanic canaliculus | unresolved |
| Temporal bone | Mastoid canaliculus | unresolved |
| Temporal bone | Cochlear aqueduct opening | unresolved |
| Temporal bone | Vestibular aqueduct opening | unresolved |
| Posterior base | Jugular foramen and fossa | partial |
| Posterior base | Hypoglossal canal | regional |
| Posterior base | Condylar canal | variant-unresolved |
| Posterior base | Mastoid foramen | variant-unresolved |
| Posterior base | Foramen magnum | visible |
| Pterygopalatine region | Pterygomaxillary fissure | visible |
| Pterygopalatine region | Sphenopalatine foramen | partial |
| Pterygopalatine region | Pterygoid (Vidian) canal | regional |
| Pterygopalatine region | Palatovaginal / pharyngeal canal | regional |
| Pterygopalatine region | Vomerovaginal canal | variant-unresolved |
| Palate and maxilla | Greater palatine canal | partial |
| Palate and maxilla | Greater palatine foramen | partial |
| Palate and maxilla | Lesser palatine foramina | unresolved |
| Palate and maxilla | Incisive canal and foramina | partial |
| Palate and maxilla | Posterior superior alveolar foramina | unresolved |
| Palate and maxilla | Canalis sinuosus | unresolved |
| Mandible | Mandibular foramen | regional |
| Mandible | Mandibular canal | unresolved |
| Mandible | Mental foramen | regional |
| Mandible | Mandibular incisive canal | unresolved |
| Mandible | Lingual and accessory mandibular foramina | variant-unresolved |
| Vault | Parietal emissary foramen | variant-unresolved |
| Vault | Occipital emissary foramina | variant-unresolved |
| Vault | Diploic channels and openings | unresolved |
| Nasal boundaries | Piriform aperture | visible |
| Nasal boundaries | Choana | visible |
| Nasal boundaries | Paranasal sinus ostia | unresolved |
| Upper cervical | Cervical transverse foramina | bone-unavailable |
| Upper cervical | Atlas vertebral artery groove | bone-unavailable |
| Upper cervical | Arcuate foramen (when present) | bone-unavailable |
