# DSA mode, v0.9.82

The detector/vessel icon beside bookmarks enters DSA without changing rotation,
pan or zoom. Until an injection is established, the ordinary 3D scene immediately
shows all arteries opaque and asks for an artery and then a point. Opening this
selector needs no DSA data requests, renderer, targets, worker or section work. Search selects the artery without
reframing the camera. Escape or Cancel before the first injection returns to
the previous 3D view. An established injection persists across mode switches.

Choose ICA, ECA, Vertebrobasilar, MMA or Maxillary artery in the existing
bookmark modal, with Left/Right/Both (left by default). Explicit bookmarks apply
their saved projection and use the existing proximal origin: cervical ICA,
proximal ECA, vertebral V1, MMA trunk or maxillary trunk respectively. Both uses
two origins. Switching into DSA after a bookmark retains that view and origin.
The first playback frame is 0.5 s, showing proximal arterial contrast. Mode entry,
bookmarks and new tips all start there. The zero-contrast baseline
remains internal; the phase slider starts at 0.5 s and exists only in DSA mode. Separate play/pause icons and frame stepping
use a 0.5 s interval. Playback loops from the last frame to 0.5 s until paused. Leaving DSA restores the previous camera, visibility,
selection, Focus and section settings. Rotation, pan, zoom and orientation
buttons work in DSA.

## Implementation

- `dsaRenderer.ts` uses a closed-surface signed ray-length integral. It adds
  contrast concentration times vessel column length into a floating-point
  render target, then maps signal to greyscale on an RGB 176 background.
  Separate vessels overlap in projection without depth occlusion. Lighting,
  bone, solid brain and selection halos are outside the DSA rendering scene.
- `dsa-surfaces.json` stores only cap points and changes to existing index
  buffers. It carries source asset hashes, checked on loading. The ordinary
  anatomy assets are reused. No replacement arterial or venous geometry is
  shipped. Proxies close label boundaries and remove small non-manifold seam
  sheets; they are separate from the ordinary selectable atlas surfaces.
- `dsa.ts` evaluates a sustained contrast pulse directly from simulation time.
  Arterial transit delays shift both edges of the pulse, retaining proximal
  concentration while distal branches fill. All arteries in each preset have
  concentration 1 at 1.5, 2.0, 2.5 and 3.0 s. Peak distal concentration is not
  reduced by branch order; smaller column length makes small vessels lighter.
- `dsa-territories.json` defines tissue fields and venous starting points.
  Drainage follows `drains_to` plus explicit missing routes. Shared vessels
  render once. Left/right ICA avoids contralateral cortical venous seeds.
  A unilateral vertebral injection fills bilateral basilar descendants without
  automatically injecting the other cervical vertebral/PICA tree.
- Blush is a smooth 3D density field integrated along each viewing ray. ICA
  uses cerebral territories; posterior circulation uses occipital, cerebellar
  and brainstem fields; ECA/MMA/maxillary use extracranial or dural fields.
  This is an illustrative perfusion model: tissue fields and transit delays
  are approximations, not patient-specific haemodynamics. Closed sections up to 18 mm long use uniform concentration with a distance-based arrival delay. This does not solve patient-specific advection, pressure or collateral competition.
- Venous curves are broader, later and weaker. Sinuses and jugular veins may
  remain dark because their columns are thick. No capillary vessels are invented.
- Static geometry is cached. Movement and stationary images use the same
  resolution and modest supersampling, capped at 1,500 pixels on the longer side. Float32 accumulation is preferred; half-float
  accumulation is used where float blending is unavailable. Float render targets
  are required. There is no server-side renderer, new runtime dependency or
  cloud service. The default run is 12 s with overlapping phases.

## Validation

`npm run dsa:test` independently checks all 828 repaired surfaces for closed,
consistently oriented boundaries and matching source hashes. The production
build also runs the existing anatomy checks.

Browser verification covers all 15 preset/side combinations, the four-frame
arterial plateau, baseline and washout, delayed veins, blush timing, scrubbing,
playback, frame stepping, modal pauses, view restoration and notice removal.
Synthetic projection checks compare known 1, 2 and 3 mm columns, overlapping
vessels, camera distance changes and half-float rendering. Results are retained
in `dsa-validation.json`.

## Injection point placement

Choose **Choose injection point**. A temporary opaque red view of the complete arterial tree appears, with no veins.
All arteries remain visible after selecting a source. Only validated courses can
be injection sources; other arteries remain visible as context.
First select a supported artery through search or a click, then click its surface to
place the tip on its verified course. The amber marker identifies the tip.
Playback resets to the first opacified frame at 0.5 s and remains paused until Play. Rotate, pan and zoom to
choose the position; a drag never places a tip. Escape or Cancel retains the
previous tip. There is no reset-origin control.
Bookmarks replace a custom tip with their proximal preset origin. Both retains two preset origins; a custom tip
represents one injection and selects its vessel side.

The selected source is cut at the tip, so its upstream part stays unsubtracted.
Branches arising before the tip are excluded. Declared anatomical edges supply
downstream branches, including the bilateral basilar tree after the confluence.
Spatially adjacent vessels never become connected automatically. Blush and
venous seeds are restricted for selective injections but remain illustrative.

`dsa-flow.json` contains courses, branch attachments and normalised vertex
flow coordinates, not another anatomy model. Courses are inferred from mesh
surface geodesics, oriented using declared parents, and checked against closed
projection surfaces. Tiny unsafe intervals snap to an adjacent verified course
position. Every clicked tip also receives a direct containment check against the
closed vessel surface, with a nearest interior guide-point fallback. Compound or ambiguous courses remain visible downstream but cannot
be chosen as an injection source. The original atlas meshes remain unchanged.

`npm run build` hashes the actual artery and vein assets, the declared branch
graph and the generator. Matching data are reused. Changed geometry triggers
surface repair and course regeneration; graph edits trigger course regeneration.
This runs during authoring/build rather than app startup. Runtime loading checks
geometry revisions and the graph and rejects stale data. Ordinary builds need
no Python geometry packages; rebuilding projection repairs after geometry
changes uses the existing numpy/trimesh authoring dependencies.

`npm run dsa:test` also checks real flow sections, permitted tip positions,
required major courses, branch exclusion, ICA direction, basilar confluence,
shared-vessel deduplication and all geometry/generator hashes. Injection browser
checks are recorded in `dsa-injection-validation.json`.

The removed working-model notice remains absent. Anatomical issues are still
listed in the release's existing issue documents.

## Vessel inspection in DSA

Click or tap an opacified artery or vein to update the existing inspection panel
and pause playback. The panel uses the ordinary 3D layout and shares its open/closed
state: a vessel click never expands it automatically. It contains the name, alternate names, description and
relationships. Links navigate information without changing the injection,
camera, ordinary selection or visibility. Clicking background clears the DSA
selection. The panel can be collapsed through its existing title control.

Picking uses the nearest closed DSA section currently contributing contrast.
The same concentration threshold controls rendering and eligibility. Unfilled
sections and the source vessel upstream of the tip are excluded. Existing
anatomical IDs identify both arterial and venous sections. Rotate to separate
overlaps, as in the ordinary 3D view. The existing raycaster and pointer gesture
handling remain in use, including rejection of drags and multiple touches.

A small selection mask follows only the currently opacified sections. The
existing DSA display shader adds a narrow orange outline outside that mask,
leaving the vessel's interior shading unchanged. The mask is separate from the
contrast integral. Injection placement retains its own picking and view, with
inspection hidden temporarily. Exiting DSA restores the ordinary view state.

No model, projection recipe, course or flow graph is rebuilt for this feature.
The inspection checks are recorded in `dsa-inspection-validation.json`.

DSA entry, cancellation, bookmarked origins, persistent injections, search camera
preservation and movement resolution are checked in `dsa-entry-validation.json`.

The first opacified playback frame, shared inspection layout and collapsed/open
state are checked in `dsa-frame-panel-validation.json` on desktop and mobile.

The injection chooser, conditional Change artery action, standard playback icons,
separate play/pause controls and looping are checked in `dsa-controls-validation.json`.

## Injection preparation performance

Closed section splitting and boundary checks run in a module worker, reusing
`flowGeometry.ts`. Each worker caches decoded surface coordinates. Preparation starts
only after the injection point is confirmed, or an explicit bookmark supplies its
proximal origin. Selecting an artery only loads and validates course data. Uncut vessels
up to 18 mm reuse their already closed projection surface. Completed sections
are cached across runs. Original atlas buffers are never transferred or changed.
The previous view stays available during preparation; Cancel or Escape prevents
a pending result from replacing the existing injection.

Worker results match the original splitting functions byte for byte in ICA and
maxillary checks. Complete arterial placement, branch exclusion, source buffer
integrity and cancellation are checked in `dsa-preparation-validation.json`.
Cold preparation can still take several seconds on a slow CPU, but the long
synchronous main-thread preparation block is removed.

The selected injection artery is opaque orange. Placement picking respects the
nearest arterial surface, including context vessels that cannot be injected.
Rotate to separate overlaps. The selector uses the ordinary scene, arterial
batches, opaque materials and pick proxies. Visibility, focus, selection and
clipping are temporarily overridden without changing their saved values. Course
data load when an artery is chosen; projection recipes, renderer and worker are
created when a point is confirmed. An established injection or explicit bookmark
can enter DSA directly and waits for any uncached sections. Worker splitting
keeps geometry preparation off the UI thread.

Opaque material settings, selected colour, overlap picking and startup preparation
timings are checked in `dsa-opaque-placement-validation.json`.

## Splitter optimisation, v0.9.80

The existing worker prepares vertex positions, flow coordinates, position weld
keys and triangle coordinate ranges once per vessel. Each split assigns source
triangles only to the sections they intersect, retaining source order and
inclusive boundary handling. Interior triangles bypass clipping. Interpolation,
section spacing, cap construction and closure checks are unchanged. This adds
no persistent cache or background preparation.

`npm run dsa:splitter:test` compares positions and indices byte for byte against
the v0.9.79 reference across all 578 validated arterial courses. Boundary cases
and partial ICA, ECA, maxillary and PCA/P2-P3 cuts are included. The browser
checks real worker commits, repeated partial cuts, opaque arterial placement,
nearest-vessel overlaps and mobile placement.

In software-rendered Chromium, uncached ICA preparation fell from 9,762.5 ms
to 1,565.8 ms. These measure section preparation rather than complete button
click to displayed frame; device timings vary. See `dsa-splitter-validation.json`.

## Compact controls, v0.9.81

The vessel-name caption is removed. Time and contrast phase stay above the
slider, and Choose injection point shares the playback buttons row. At widths
up to 420 pixels the redundant 2 frames/s label is hidden so the controls fit.
Desktop, 390-pixel and 320-pixel placement-button and layout checks passed; see
`dsa-layout-validation.json`.

## Selector reuse, v0.9.82

The separate arterial placement scene, its meshes and materials, empty DSA run
and selection-time section prewarming have been removed. Normal 3D picking
chooses the nearest arterial surface, with context-only arteries still blocking
clicks through them. Source selection validates the course; the confirmed point
receives the existing closed-surface containment check before its DSA run is
built. Cancelled or replaced selections cannot commit stale asynchronous work.

The existing projection, ordinary view state, bookmark origins, DSA inspection,
contrast shading and anatomical geometry are retained. See
`dsa-selector-validation.json` for browser interaction and entry checks.

The matched software-rendered comparison at 1280 x 900 and DPR 1 measured
selector setup at 7.2 ms initially and 1.6 ms on repeat, versus 4.2 ms and
1.6 ms for ordinary arteries-only visibility changes. Both submitted one draw
call for 7,176,719 triangles. Full image completion still took approximately
6-8 seconds in this software-rendered environment. This is a graphics cost,
not DSA preparation; device timings vary.
