# Main venous anatomy, v0.9.0

This release adds 104 selectable venous structures, 98 descriptions adapted
closely from Jeremy Lynch's supplied neurovascular notes, and 127 drainage or
communication relationships. The three pre-existing artery, potential-connection
and craniofacial GLBs remain byte-for-byte identical to v0.8.12.

Enable **Veins** in Layers. Selecting a vein from search, the anatomy tree or a
description link also reveals the venous layer. The artery layer can be switched
off independently. Existing focus, highlighting, ghosting, clipping and subtree
checkboxes apply to veins. A description is omitted when no note text is supplied.
Incoming drainage is labelled **Receives from**, outgoing drainage **Drains to**;
bidirectional connections retain **Communicates with**. Display-tree grouping
does not imply flow direction. The relationship graph records drainage separately.

## Included anatomy

- Dural sinuses: superior and inferior sagittal, straight, confluence, occipital,
  marginal, paired transverse and sigmoid, cavernous, superior and inferior
  petrosal, sphenoparietal, and anterior/posterior intercavernous sinuses.
- Superficial cerebral veins: paired superficial middle cerebral, Trolard, Labbé,
  and representative frontal and parietal cortical collectors.
- Deep cerebral veins: Galen, paired internal cerebral and basal veins,
  thalamostriate, anterior septal, superior choroidal, anterior cerebral and deep
  middle cerebral veins; anterior and posterior communicating veins.
- Posterior fossa: superior petrosal veins, lateral mesencephalic and
  cerebellopontine fissure veins, inferior vermian and hemispheric veins,
  precentral cerebellar and superior vermian veins, the median anterior brainstem
  channel, transverse pontine and pontomedullary sulcal veins, and proximal
  anterior spinal vein.
- Extracranial routes: internal and external jugular, retromandibular, maxillary,
  facial, angular, deep facial, superficial temporal, posterior auricular,
  vertebral and deep cervical veins; representative pterygoid and suboccipital
  plexuses.
- Skull-base connections: superior and inferior ophthalmic veins, foramen ovale
  emissary veins, anterior and lateral condylar veins, and basilar/clival plexus.

## Sources and reconciliations

The authoritative source is `nv(2).pdf`, printed pp62-76 (physical PDF pp56-70),
including Figures 2.16-2.19. The illustrations and supplied angiogram were
visually reviewed. Descriptions and exact page mapping are retained in
`STRUCTURE_DESCRIPTIONS.md` and `anatomy/source/venous/courses.json`.
The PDF and its illustrations are not redistributed in the app.

The following original angiographic teaching resources were consulted for
spatial context and variation, without importing images or coordinates:

- https://neuroangio.org/venous-brain-anatomy/
- https://neuroangio.org/venous-brain-anatomy/venous-sinuses/
- https://neuroangio.org/venous-brain-anatomy/superficial-venous-system/
- https://neuroangio.org/venous-brain-anatomy/deep-venous-system/

The inferior sagittal sinus paragraph on printed p64 says it joins the internal
cerebral veins to form Galen. The more detailed Galen paragraph on p72 instead
states that Galen joins the inferior sagittal sinus to become the straight sinus.
This release follows p72 and the supplied diagrams. The p64 sentence is reconciled
in the description rather than reproduced as a contradictory drainage connection.
The spelling **Monro** is used for the interventricular foramen. **Posterior
anastomotic vein of Labbé** follows the notes; **inferior anastomotic vein** remains
a searchable alias.

## Represented pattern and limits

This is an editable teaching reconstruction in the existing RAS millimetre frame,
not a segmentation of one subject. Courses, calibres, depth and soft-tissue
boundaries are estimated. A bilateral template is fitted independently to each
side of the retained skull. It must not be interpreted as a measured symmetrical
venous anatomy or a haemodynamic simulation.

The model uses a communicating superficial pattern with Trolard, Labbé and the
superficial middle cerebral vein present on both sides; bilateral complete basal
veins draining to Galen; and modest right-sided transverse/jugular dominance.
The anterior communicating vein and occipital sinus are represented despite
their variability. The inferior ophthalmic route to the pterygoid plexus is one
represented route, not a claim that it is the only drainage pattern.

The jugular fossa, superior/inferior orbital fissures, foramen ovale, foramen
magnum, sella, clivus and petrous regions constrain the authoring. The superior
ophthalmic vein uses a local passage corridor within the observed superior
orbital fissure region. Cavernous spaces are bounded by the local sphenoid and
temporal surfaces and hollowed around the retained cavernous ICA.

The hypoglossal lumen is not resolved in the source skull. The anterior condylar
vein therefore follows the existing regional landmark and intersects unresolved
bone there. It is not a demonstrated canal fit. Posterior condylar, mastoid and
parietal emissary channels are deferred instead of inventing openings. Registered
brain, ventricular walls and cervical vertebrae are absent, so cortical, deep,
posterior-fossa and vertebral routes need anatomical review against future tissue
context. Small residual clearances against the dense existing meningeal/perforator
network are recorded in the authoring review, not silently treated as validated.

The neck veins are truncated at the current model's lower cervical field.
Subclavian, brachiocephalic and thoracic terminations are described where present
in the notes but are not modelled. Small medullary veins, complete cortical and
diploic networks, and the full spinal venous system are outside this first release.

## Geometry and performance

Manually authored curves are fitted to existing reference geometry. The final
surface is a joined implicit envelope with a 0.4 mm authoring grid, common-surface
smoothing and topology-preserving reduction. The grid is a meshing parameter,
not imaging evidence. The displayed sinus profiles are simplified rounded
envelopes; trabeculae, valves and arachnoid granulations are not modelled.

The complete venous skin is partitioned into named selectable meshes with shared
normals. Hiding a neighbour can expose its shared interface. Meshopt compression
is checked for an exact attribute/index round trip. `models/venous.glb` is separate
from the unchanged arterial and bone assets. Its byte size and revision hash are
included in the existing loading progress/cache mechanism.

On browsers with native multi-draw, opaque veins render in one independent batch.
Selected and ghosted veins use individual meshes, and per-structure proxies handle
picking and focus. The fallback path remains available without multi-draw.
No FPS improvement is claimed from these fixture tests.

## Checks and optional authoring tools

The standard app build still runs its existing catalogue/asset validation only.
No new anatomical fitting or collision audit runs when building or using the app.

One-off reports in `docs/validation/venous-*-v0.9.0.json` cover retained asset
hashes, the joined surface, note links, actual Three.js loading/raycast selection,
independent layers, selection/ghosting/clipping, subtree hiding and real React
event handlers. Geometry was visually inspected in lateral, frontal, oblique
and deep-system views using VTK. The UI checks use jsdom and a renderer fixture;
they are not a full browser/GPU or mobile-device benchmark. Root and GitHub Pages
subpath production builds are checked separately. Docker is not available in the
authoring environment.

Editable sparse courses, fitted paths and passage corridor coordinates are in
`anatomy/source/venous`. Optional Python authoring requires NumPy, SciPy, VTK and
Manifold3D; it is separate from normal installation. See that directory's README.
Optional interaction checks require `esbuild` and `jsdom` in `node_modules`, or
set `VENOUS_QA_MODULES` to a directory containing those packages. Run
`node tools/check-venous-viewer.mjs` and `node tools/check-venous-ui.mjs` from the
app root after building.
