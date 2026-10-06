# Neurovascular Atlas v0.9.21 review build

Includes the ventral pons advancement of up to 3 mm, carried with the basilar artery and local pontine vessels. Cavernous sinuses retain their reviewed shape. The rejected PCA and deep venous fitting trials are excluded; those fitting tasks remain unfinished.

This compact installation package retains all 1,482 catalogue structures and all model triangles. Delivery assets use Meshopt compression, positions rounded on a 1/4096 mm grid (maximum displacement below 0.00022 mm), and high-precision packed shading normals. Surface anchors and asset hashes are updated and validated. Historical review images and authoring trial models are omitted from this installation package. See [delivery checks](docs/validation/delivery-optimisation-v0.9.21.json).

This build resumes posterior-fossa candidate 59 and applies candidate 61 to the full app. It brings the anterior veins closer to the brainstem, preserves circular tube sweeps and arterial overpasses, repairs the right P1/basilar and left SCA/proximal perforator joins, and places both posterior spinal arteries on the dorsal medulla and illustrative upper cervical cord from proximal PICA origins. Clival/basilar plexus geometry is omitted.

This remains an anatomical review build. The local posterior-fossa surface walls, closed-tissue containment, vein/artery crossings, sampled tube diameters and 151 source joins pass. Wider upper collecting-vein and cerebral parenchymal relationships are unfinished. The full scope and limitations are in [the fitting report](docs/POSTERIOR_FOSSA_v0.9.20.md).

Run `./docker.sh start` for local review, or use the existing installer with this v0.9.21 ZIP. The separate posterior-fossa authoring viewer is available in the review checkpoint.

The Docker launcher validates anatomy inside the build after installing npm dependencies. No host Node/npm installation is required for Docker startup.

## Bilateral central arterial family fit in v0.9.18

Applies both central arteries, their cortical branches and distal rami, and the adjoining MCA transitions. The complete eight-label family passes tissue, skull, vessel-neighbour, self-intersection, shared-join and wall-envelope checks. The build reproduces byte-for-byte from the supplied seed. Dural and brainstem groups remain deferred; brain, skull, venous and protected ICA/cavernous geometry are retained. See [fitting evidence and limits](docs/FITTING_v0.9.18.md).

## Fitting validation checkpoint in v0.9.17

Adds expanded cortical-family tissue checks, exact exported-buffer verification, dominant-axis branch refinement and a separate rejected eight-label trial for review. No fitting geometry is accepted. Every production geometry asset remains identical to v0.9.15. See [checkpoint findings and next work](docs/FITTING_v0.9.17.md). The first fitting batch remains incomplete.

## Previous anatomical targets and course rules in v0.9.15

Implements sections 1–2 of the vessel fitting plan on v0.9.14. Adds 16 missing sulcal/deep targets, ordered central sulcal and falcotentorial guides, 290 intracranial vessel course specifications and a measured baseline audit. Vessel panels link to their brain targets. The original skull, vascular assets and 172 brain meshes are preserved. See [release details](docs/VESSEL_TARGETS_v0.9.15.md) and [anatomical audit](docs/ANATOMICAL_AUDIT_v0.9.15.md). Vessel fitting itself is the next stage.

## Brain and dural orientation in v0.9.14

Based on v0.9.13. Adds skull-registered cerebral hemispheres, brainstem, cerebellum, falx, tentorium, ventricles and deep structures, with 172 named surfaces and 69 surface-bound vessel course landmarks. Open **Layers and anatomy** and choose **Brain overview** or **Deep / posterior fossa**. Alternate names are searchable and now appear in the inspection panel. See [registration, guide data and limits](docs/BRAIN_v0.9.14.md). Existing skull and vascular assets are unchanged; vessel refitting remains a separate authoring step.

## Cavernous roof and single cavity in v0.9.13

The previous upper ICA sleeve has been removed. One rounded cavity fits the carotid sulcus medially, with an independent roof constrained by the model's clinoid landmarks. The intracavernous ICA region is lowered smoothly by up to 0.9 mm, with the same coordinate adjustment applied to adjoining arterial segments and branches. See `docs/CAVERNOUS_v0.9.13.md` for the geometry checks, matched views and limits of the inferred dural boundary.

## Narrow cavernous spaces and restored connections in v0.9.11

The cavernous spaces have a much narrower curved profile with rounded edges. The SOV and emissary entries are rebuilt, with direct attachment and end-to-end continuity checks for the cavernous tributaries. See `docs/CAVERNOUS_v0.9.11.md` for the model measurements, comparisons and reference limits.

## Cavernous cavity and venous entries in v0.9.10

The cavernous cavities are slimmer, with inward-curving lateral walls and roofs. Rebuilt terminal SMCV and lesser-wing channels blend smoothly into the sinus through a shared surface. All 104 venous structures remain connected. See `docs/CAVERNOUS_v0.9.10.md` for the matched views, contour measurements, junction checks and limits.

## Rendering in v0.9.5

Translucent context uses cached Lambert materials and a single transparent pass. Full-detail opaque shading is restored when structures become opaque. The same model geometry is used throughout, with no new model downloads or preprocessing. During movement the 3D view uses a 0.75 pixel ratio, restoring its original resolution after the controls settle.

## Credits in v0.9.4

The information modal contains a compact, scrollable list of software, model and anatomical reference credits, including the Oxford Specialist Handbook Neurointervention.

## Interface in v0.9.3

The anatomy tree opens directly, with no Layers/Anatomy tabs or mesh labels.
Right-hand visibility controls cycle through fully visible, translucent and
absent. Group controls apply to descendants and show a mixed indicator when
children differ. Structure names select and centre anatomy; arrows expand it.
The desktop orientation toolbar fades like the side panels until hovered or
keyboard-focused. Mobile controls remain fully opaque. Automatic camera focus
uses a wider frame, caps zoom-in at 25% and avoids cumulative zoom on repeated
selections. Manual navigation resets that limit.

## Venous morphology in v0.9.2

Revises the major sinus courses and their fit against the retained skull, preserves bone-oriented sinus profiles, and gives selected peripheral veins finer taper. See `docs/VENOUS_v0.9.2.md` for sources, checks and modelling limits.

## Interface in v0.9.1

Both panels start collapsed on every device. On desktop, Anatomy sits at the
bottom-left edge and the selected structure panel at the bottom-right edge,
either side of the central orientation toolbar. Panels expand upwards and fade
until hovered or used with the keyboard. On mobile, the atlas title remains on
one line and the panels retain their compact stacked layout.

Focus and Hide are now on the left of the orientation toolbar. Focus keeps the
selected structure, its vessel segments and immediate named branches/tributaries
opaque while dimming other visible structures. Click elsewhere or press Focus
again to restore the previous opacity. Hidden structures remain hidden.
Anatomy visibility controls sit on the right of their labels, away from the expand arrows.

## Main venous anatomy in v0.9.0

Add 104 selectable venous structures with 98 note-derived descriptions and linked drainage relationships. Use the **Veins** tree visibility control, or select a vein through search to reveal veins. On supported browsers, veins use a separate multi-draw batch, so they remain independent of artery visibility. The existing artery, connection and bone models are byte-for-byte unchanged. See `docs/VENOUS_v0.9.0.md` for scope, sources and authoring limitations.

## Revised V3/V4 starts and ASA origins in v0.8.12

Set both vertebral V3 and V4 starts from the latest black-line annotation. Move the paired ASA origins to the red-marked V4 level while preserving their welded vertebral collars, central confluence and descending trunk. The vertebral courses and calibre, other branch origins, all other anatomy and GUI are retained. The affected vertebral wall patches are re-triangulated without adding triangles. See `docs/VA_ASA_v0.8.12.md`.

## Labial and submental courses in v0.8.11

Lower the bilateral inferior labial courses below the visible lower teeth, lower the superior labial courses slightly above the visible upper teeth, and raise the hanging submental loops to the inferior mandibular border. Preserve the facial arteries, shared root collars, vessel calibres, topology, IDs and descriptions. Carry four potential labial routes with their endpoints. Retain the corrected ICA/vertebral/ACA sections and GUI. See `docs/LABIAL_SUBMENTAL_v0.8.11.md`.

## ICA boundaries in v0.8.10

Correct the bilateral cervical/petrous and petrous/cavernous boundaries to the supplied annotated diagram, shortening the petrous section. The continuous ICA surfaces, upper ICA sections, vertebral/ACA sections and GUI are unchanged. All branch courses and welded junctions are retained. See `docs/ICA_v0.8.10.md`.

## Vertebral boundaries in v0.8.9

Correct the bilateral V2/V3 and V3/V4 boundaries to the supplied annotated diagram. V3 covers the short outer atlas loop; V2 ends at its lower start and V4 begins on its medial return. Vessel courses and surfaces are retained exactly. V1 and all ACA/ICA boundaries are unchanged. Branches remain attached to the same physical points, with their segment parents updated. See `docs/VERTEBRAL_v0.8.9.md`.

## Interface in v0.8.8

Both panels initially collapse at mobile widths up to 680px. The user’s expanded/collapsed choices persist during selection and resizing. Relationship labels start with capital letters, including Branches to and Has segment. Desktop defaults are retained.

## Interface in v0.8.7

Use the Neurovascular Atlas name and a brief introduction with Jeremy Lynch’s 2026 authorship. Loading shows a percentage based on actual model downloads and scene preparation. FPS is hidden when rendering settles. Panels have compact title bars, equal mobile side margins and scrolling confined to their bodies. Remove Fit, the separate Side row and planned counts/labels; group relationships by type with clickable names. Anatomy assets, descriptions and definitions are unchanged.

## Vertebral and ACA sections in v0.8.6

Select vertebral V1–V4 and ACA A1–A5 sections on either side. Each has its note-derived description and linked structures. Whole-artery and distal pericallosal focus, highlighting and subtree hiding remain available. The existing vessel surfaces and courses are retained exactly; cervical, callosal and coronal-suture boundaries are reference estimates where tissue is not registered. See `docs/VERTEBRAL_ACA_v0.8.6.md`.

## Interface in v0.8.5

A small white FPS readout in the bottom-right corner counts actual rendered frames. It updates at most twice per second and shows `FPS · idle` when drawing stops, without forcing extra renders or rerendering the panels. The selection panel title omits the coloured dot and close button. The mobile logo uses a smaller font and a reserved area beside the responsive search box. Anatomy and rendering optimisations are retained.

## Rendering in v0.8.4

Changes share a single render per browser frame. Selection colours and clipping offsets no longer request unnecessary shader updates; layer changes refresh together and clipping reuses cached model bounds.

On browsers with native `WEBGL_multi_draw`, the 754 opaque vascular parts render in one batch. Their positions, normals, triangles, names and IDs are preserved. Selected vessels render individually to retain the existing highlight, and ghosted vessels keep their existing transparency rendering. The original per-structure meshes still handle picking and focus bounds. Browsers without native multi-draw keep the original rendering path to avoid adding batching overhead without reducing draw calls. Adaptive resolution from v0.8.3 is retained.

## Rendering in v0.8.3

Rotation, panning and zoom use a pixel ratio capped at 1. Full sharpness (device pixel ratio capped at 2) returns 180 ms after camera movement settles, including the damping glide. Anatomy, selection and descriptions are unchanged. Screens with a device pixel ratio of 1 or less keep their native resolution throughout.

## Descriptions and names in v0.8.2

Structures with text in the supplied notes show a **Description** section immediately below **Focus / Hide**. Click a linked structure name to select and focus it. Structures without note text have no Description section. Both panel collapse states continue to be preserved.

The STA temporal branch is named **Posterior deep temporal artery**, and the maxillary temporal branch is named **Middle deep temporal artery**, matching the notes on both sides. Previous names remain searchable aliases. Foramen rotundum artery names are cleaned up, and dental/alveolar terms are searchable synonyms. See `docs/DESCRIPTIONS_v0.8.2.md` and the reviewed catalogue in `docs/STRUCTURE_DESCRIPTIONS.md`.

## Corrections in v0.8.1

The ophthalmic origins are now just beyond the anterior ICA genu on both sides. The selectable paraophthalmic region starts 1 mm of centreline arc before each ophthalmic origin. The proximal ophthalmic curves are refitted while the ICA centreline, PCom/AChA origins and A1/M1 endpoints are retained. These are reference-model positions; the dural boundary remains estimated.

## Corrections in v0.8.0

Named arterial omissions and branch-specific potential routes from the discrepancy audit are implemented. Both panel states persist across selection changes and the inspection title updates while collapsed. See `docs/AMENDMENTS_v0.8.0.md` for the audit-item ledger, ICA changes, selected variants and remaining tissue-registration limits.

## Corrections in v0.7.6

Gentle proximal ophthalmic/PCOM curves are restored, and the terminal ICA–A1–M1 surface is blended into a continuous bifurcation. Each ICA has seven clickable, coloured endovascular regions, with branch hierarchy, focus and visibility controls. See `docs/SEGMENTS_v0.7.6.md`.

## Corrections in v0.7.5

The ICA–M1 junctions are rebuilt as joined surfaces. PCOM and anterior choroidal origins are higher, ophthalmic origins are slightly lower, and proximal ophthalmic/PCOM angulations are smoothed. Both panel titles use a matching smaller font with closer spacing. Passage information and notes are removed from the details panel. See `docs/JUNCTIONS_v0.7.5.md`.

## Panel changes in v0.7.4

Layers/Anatomy and structure details are stacked on the left. Click either title bar to collapse or expand it; the lower panel moves with the upper panel. The 3/4 and Face camera buttons are removed. Details and relationships show structure names without internal IDs, and the reconstruction/provenance/confidence/review fields are removed from the panel. Anatomy assets are unchanged from v0.7.3.

## Corrections in v0.7.3

M1 leaves the terminal ICA laterally with the folded junction corrected. Both A1 surfaces are preserved from v0.7.2. The ophthalmic origins are lower, the cavernous bends are more medial/posterior, and the inferior alveolar/mental routes now follow the mandibular body and visible mental-foramen regions. See `docs/REFINEMENT_v0.7.3.md`.

## ICA correction in v0.7.2

Both upper cervical/petrous entries now approach the carotid entry region anterior and lateral to the jugular fossa. The cavernous courses follow the parasellar corridor and ascend medial to the anterior clinoids. The prior overly medial entry and excessive lateral sweep are corrected. Under **Skull → ICA skull-base landmarks**, 33 entries identify the relevant bone surfaces, canal regions and estimated dural boundaries. Select a row to focus its marker; entries with a recorded course also show that course. The regular anatomy visibility controls and collapsed tree behaviour apply. See `docs/ICA_v0.7.2.md` for the method and remaining canal limitations.

## Included

- One combined anterior, posterior and bilateral ECA circulation.
- Revised infraorbital, meningeal, petrous ICA, ophthalmic, rotundum and ovale courses, with propagated branch attachments.
- 64 skull-opening types in a searchable, side-specific register under **Skull → Foramina and passages**. Selecting a located entry shows its regional marker and any saved course. Unresolved entries have no invented marker.
- Shared, smoothed vascular junctions and independently selectable vessel parts.
- Complete original skull context, both maxillae, mandible, condyles, alveolar processes and all 32 teeth.
- Potential ECA–ICA and ECA–vertebral connections on both sides, always enabled in gold with the artery layer.
- Simplified UI: removed the screenshot-identified banners, strapline, release subtitle, source list, About explanation, layer instructions, connection toggle and presets.
- Ghosted bone and teeth are click-through. Opaque bone remains selectable.

This is a reference-guided teaching reconstruction, not an individual patient segmentation. Vessel calibre, small canals, cervical vertebral and brain-surface relationships remain approximate. The left ECA uses the right template with independent bone fitting. It is not an independent angiographic reconstruction.

## Anatomy tree

Every row has a visibility checkbox. Unticking hides its geometry and all descendants, including collapsed branches. Ticking restores the subtree. A partial tick means some descendants are hidden. Detail-panel Show/Hide uses the same visibility state; global layer settings still apply. Landmark markers appear only while selected; their checkboxes enable or hide that selected marker. Unlocated entries have disabled checkboxes. The Anatomy tab starts fully collapsed each time it opens, independently of model visibility. Potential connections are nested under their recorded ECA source branches; their receiving arteries remain in the connection graph and detail panel.

## Download and serving

The release contains five anatomy assets. Meshopt compression of the vascular assets preserves the original floating-point positions, normals and index data exactly. The adjusted brain context uses additional material facets to represent the registration field. Model requests carry content hashes; nginx serves gzip and caches unchanged assets. The manifest is revalidated so a new release loads the new hashes.

## Development

`npm ci`, then `npm run dev`. `npm run build` validates the bundled catalogue and creates the production site. The normal installation needs Docker, not the Python modelling libraries. The modelling workflow and release-specific checks are in `docs/`. The one-off foraminal/compartment review is **not** part of `npm run build`, Docker, or the installer. Revisit it only after changing artery or bone geometry. See `docs/FORAMINA_v0.7.0.md` for the remaining canal limitations.

## Venous morphology in v0.9.6

All six skull-base regions are revised using angiographic appearances and local bone landmarks. See [the morphology review](docs/VENOUS_v0.9.6.md) for references, geometric checks and retained skull-mesh limits. The GUI and economical translucent renderer from v0.9.5 are retained.

## Cavernous refinement in v0.9.7

The lower cavernous ICA is moved medially with a smooth transition to the petrous and upper siphon segments. The cavernous sinuses are locally rebuilt as broad parasellar envelopes with flattened sellar cross-connections. Nearby arterial branches use the same coordinate deformation. See [the geometry review and matched renders](docs/CAVERNOUS_v0.9.7.md).

## Cavernous refinement in v0.9.8

Retain the completed v0.9.7 ICA correction and refine the venous exclusions around the displayed carotid, restoring posterosuperior space and preserving the lesser-wing entry. All 104 venous structures remain in one connected, watertight network. See [the follow-up review](docs/CAVERNOUS_v0.9.8.md) for checks and the unresolved low petrous/lacerum skull canal. The companion PDF provides matched views and qualitative angiographic comparisons.

## Cavernous wall correction in v0.9.9

Replace the rounded cavernous envelope with straight to gently concave lateral walls, a flatter roof and a sloping posterior contour. Remove the anterior rounded recess, retaining its lesser-wing connection through a thin flat entry. See [the wall correction review](docs/CAVERNOUS_v0.9.9.md).
