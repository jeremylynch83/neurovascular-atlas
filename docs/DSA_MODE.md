# DSA mode, v0.9.76

The detector/vessel icon beside bookmarks enters DSA without changing rotation,
pan or zoom. Until an injection is established, the existing arterial placement
view asks for an artery and then a point. Search selects the artery without
reframing the camera. Escape or Cancel before the first injection returns to
the previous 3D view. An established injection persists across mode switches.

Choose ICA, ECA, Vertebrobasilar, MMA or Maxillary artery in the existing
bookmark modal, with Left/Right/Both (left by default). Explicit bookmarks apply
their saved projection and use the existing proximal origin: cervical ICA,
proximal ECA, vertebral V1, MMA trunk or maxillary trunk respectively. Both uses
two origins. Switching into DSA after a bookmark retains that view and origin.
The first playback frame is 0.5 s, showing proximal arterial contrast. Mode entry,
bookmarks, new tips, reset and replay all start there. The zero-contrast baseline
remains internal; the phase slider starts at 0.5 s and exists only in DSA mode. Play, pause, replay and frame stepping
use a 0.5 s interval. Leaving DSA restores the previous camera, visibility,
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

Pause or choose **Injection point**. A temporary coloured arterial view appears.
Select a supported artery through search or a click, then click its surface to
place the tip on its verified course. The amber marker identifies the tip.
Playback resets to the first opacified frame at 0.5 s and remains paused until Play. Rotate, pan and zoom to
choose the position; a drag never places a tip. Escape or Cancel retains the
previous tip. Reset origin restores the selected preset origin at 0.5 s.
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
