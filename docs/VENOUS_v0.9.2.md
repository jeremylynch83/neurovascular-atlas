# Venous morphology, v0.9.2

This revision addresses the round, bulky major sinuses, local transverse/sigmoid
kinks and blunt peripheral veins reported in v0.9.1. It keeps the 104 named
structures, 127 drainage/communication relationships and note-derived descriptions.

## Changes

- The superior sagittal sinus uses a rounded triangular cross-section oriented
  against the inner calvarium, with a finer anterior segment and gradual posterior
  enlargement. Transverse and sigmoid sinuses use bone-oriented oval profiles.
- Broad transverse/sigmoid courses are fitted independently to each side of the
  retained skull. Shared tangents at transverse/sigmoid and sigmoid/jugular joins
  remove an abrupt change of direction. Local avoidance of individual meningeal
  arterial branches no longer dictates the course of these large sinuses.
- Calibre varies along the transverse/sigmoid outflow rather than remaining
  constant. The selected modest right-sided dominance is retained. The lower
  sigmoid transitions through the retained skull's jugular outlet, with its
  jugular entry adjusted locally to remove an anterior displacement and return bend.
- Frontal/parietal cortical collectors, deep tributaries and selected cerebellar
  veins become finer towards their peripheral origins. Trolard, Labbé and other
  connections retain a lumen at both ends; a universal taper is not imposed.
- The final mesher retains the oriented sinus profiles, rather than replacing
  them with spherical envelopes. It uses a 0.28 mm authoring grid, common surface
  normals and topology-preserving reduction. Bone exclusion is applied before
  triangulation so sutures do not create folded surface triangles. This grid is
  not imaging resolution.

The current artery, connection and craniofacial assets are fixed references.
The v0.9.1 interface changes are retained. Scientific authoring tools remain
optional and are not part of the app's installation or browser runtime.

## Image review

The separate 40-asset venous reference pack contains the images and exact source
register. No book figures or website images are embedded in the app.

| Source | Reviewed figures | Use in this revision |
| --- | --- | --- |
| Neil M. Borden, *3D Angiographic Atlas of Neurovascular Anatomy and Pathology*, 2006 | 7.1a-c, 7.2a-b, printed pp227-229, PDF pp239-241 | Paired 3D courses, sinus outflow and relative collecting-vein calibre |
| Borden, same book | 7.3a-b, 7.4a-b, 7.5a-c/i, 7.6a-b, 7.7c-d | Smooth broad sinus contours, normal variation and finer cortical/deep/posterior-fossa tributaries |
| Gianni Boris Bradač, *Applied Cerebral Angiography*, 2017 | 9.5a, 9.6a-b, 9.14a-c, 9.17a-b; printed pp139-150 | Cortical entry angles, peripheral-to-collector hierarchy and sinus contours under different injections |
| Neuroangio, Venous Sinuses | Venous-3D-VR rotation; dural venous lake angiograms; separately labelled SSS/TS variants and CT/MR context | Three-dimensional course, profile variation and limits of a circular tube model |
| Neuroangio, Superficial Venous System | Trolard-Sylvian-Labbé network; balanced superficial system; basal/sylvian/Labbé collaterals | Collecting-vein calibre, continuity and peripheral taper |

Source pages:

- https://neuroangio.org/venous-brain-anatomy/venous-sinuses/
- https://neuroangio.org/venous-brain-anatomy/superficial-venous-system/

Faint opacification is not treated as proof of a small lumen. Fenestration,
stenosis, diverticulum and abnormal bone remodelling examples were excluded from
the default shape targets. Granular older 3D renderings were used for course and
depth rather than copying every surface irregularity.

## Validation and limits

The final joined surface is watertight, has one connected component and retains
all 104 selectable parts. Its 427,414 triangles are 4.9% fewer than v0.9.1.
All 122 specified main-path attachment endpoints agree within export rounding.
No major sinus faces invert during the final surface fitting.

In this model, the median nearest bone gap per 2 mm course bin is about 0.20 mm
for the SSS, 0.22–0.23 mm for the transverse sinuses and 0.21–0.24 mm for the
sampled sigmoid courses. The older values were about 0.91 mm, 0.92–0.99 mm and
1.77–2.18 mm respectively. These are mesh-space comparisons, not measured dural
thickness. Local sigmoid gaps remain around the skull-base transition, reaching
about 3.5 mm at the 90th percentile. The detailed report states the excluded
junction/end regions and limits of vertex/face-centroid sampling.

Production builds passed at both the root URL and a GitHub Pages subpath. The
actual browser loaded all four assets and passed venous layer, orientation,
search, Focus and Hide/Show checks in software WebGL2. Three.js ray tests picked
all 104 veins; React interaction checks retained the earlier panel behaviour.


`docs/validation/venous-morphology-v0.9.2.json` records the geometry and retained
asset checks, attachment continuity, local sinus turning and bone apposition.
Rendered review images cover both sides, frontal/posterior views, skull context
and the deep veins. Viewer and build reports use the v0.9.2 suffix.

This remains an editable reference reconstruction. The radii are authoring
choices informed by angiographic appearance, not measurements from calibrated
DICOM. Bone fitting uses the retained atlas skull, not the skull of any source
angiogram. Registered brain, dura, ventricles and cervical vertebrae are still
absent. Exact patient anatomy, dural thickness and sulcal relationships are not
established by this revision.

The pre-existing unresolved hypoglossal canal/anterior condylar relationship is
retained. Small artery/vein contact candidates are recorded in
`docs/validation/venous-contact-candidates-v0.9.2.json` for review; the major sinus
course is not distorted to route around an estimated meningeal twig. These
limitations should be read with the original `VENOUS_v0.9.0.md` scope notes.
