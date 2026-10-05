# v0.9.16 implementation checkpoint

The offline shared-skin fitter and exported-geometry validation are implemented. **No trial geometry is applied. The first fitting batch remains incomplete.** Every skull, brain and vascular asset in the runnable app is byte-for-byte identical to v0.9.15. Course information records the failed trial groups as blocked.

## What was implemented

The authoring tools use decoded delivered GLBs, shared coordinate fields at labelled joins, bounded surface/corridor targets, actual-wall refinement and recomputed shared normals. They retain vessel IDs, labels and original triangle indices. Registration and bound targets remain versioned. Fitting runs offline; normal installation and viewing require no new Python dependencies.

The checks cover label boundaries, protected position/normal/index buffers, named tissue contacts, skull contacts, retained arterial neighbours, matched cross-section envelopes and local context displacement/volume. Publication rejects stale validation hashes and new contacts in the edited cortical family. These checks are scoped geometric tests, not proof of lumen patency or full anatomical accuracy. Parent transitions below z = 120 mm still require their own regional review before any cortical fit can be considered complete.

## Why the geometry was withheld

| Trial | Result | Required next work |
| --- | --- | --- |
| Left central arterial family | Main artery cleared its banks, skull and retained arterial neighbours in the checked sulcal phase. Its adjoining cortical branch and distal ramus introduced 254 and 351 postcentral contacts, both from zero. | Establish branch-specific courses and reconstruct the joined regional skin coherently. |
| Right central arterial family | Terminal join refinement failed to converge. The last rejected trial had 38 precentral and 188 postcentral contacts. | Review the terminal corridor and rebuild its joined skin with fixed external collars. |
| Straight sinus and Galenic/inferior sagittal joins | The guide-based trial introduced 91 declive, 45 culmen and 95 callosal contacts in relationships that had zero baseline contacts. | Reconcile the complete dural attachment and neighbouring tissue corridor before moving the junction. |
| Brainstem surface veins | Exposed-surface projection met the clivus. A 6 mm context shear cleared skull contacts but introduced 206 left and 207 right medulla–tonsil contacts, from zero; pons–tonsil contacts increased from 36 to 115 per side. | Reconcile brainstem, fourth ventricular, tonsillar and clival relationships together. |

A separate anterior compression trial was rejected because it reduced the closed medulla mesh volume by about 22%. The connected shear changed exported medulla volume by about 0.5%, but failed the neighbour constraint. A dural context adjustment bounded at 7.55 mm also remains rejected. Overall registration and every brain mesh are retained.

A clear primary vessel does not establish a clear adjoining family. For that reason the left primary fit is also withheld. No cavernous or ICA correction is undone, and no failed trial is presented as a completed anatomical correction.

## Evidence

The four `*-trial-v0.9.16.json` reports contain the failure evidence. `left-central-trial-v0.9.16.json` includes per-label displacement, calibre envelopes, primary checks and the subsequent family check that rejected the fit. Its four changed mesh labels are supplied separately as `anatomy/source/brain/trials/left-central-v0.9.16.glb`, for review only. This file is not loaded by the app.

`validation/trial-central-comparison-v0.9.16.png` compares the retained baseline with the rejected left trial at matched cameras and scale, including translucent and opaque banks. Red identifies the left family; grey is the retained right family; green is the sulcal reference. The trial panel is explicitly labelled rejected.

The live `fitting-geometry`, `fitting-context` and `fitting-surrounding-tissue` reports describe the retained checkpoint geometry, not a passing fit. Baseline tissue contacts remain unresolved. `release-validation-v0.9.16.json` records build, browser, installer and preservation checks.

## Reproduce and inspect

Use the delivered v0.9.15 ZIP as baseline. Create `.authoring/`, decode `public/anatomy/models/complete-circulation.glb` and `venous.glb` with `tools/decode_glb.mjs` as `arteries-baseline.glb` and `veins-baseline.glb`. Preserve the brain GLB and generated manifest as `brain-baseline.glb` and `manifest-baseline.json`. Decode `craniofacial.glb` as `bones-baseline.glb`. Old centrelines do not replace delivered skins.

Authoring requires NumPy, SciPy, trimesh, VTK and Pillow, plus the app's Node dependencies. The default fitter retains geometry while all groups are blocked. Trial flags are for disposable authoring copies:

```sh
python3 tools/brain/fit_vessels.py --include-left-central-experiment
python3 tools/brain/verify_fitting.py
python3 tools/brain/verify_context.py
python3 tools/brain/verify_surrounding_tissue.py
python3 tools/brain/verify_arterial_neighbours.py
python3 tools/brain/verify_calibre.py
```

The surrounding-tissue report exposes the adjoining branch failures. `publish_fitting.py` must reject this trial. Right central, dural and brainstem modes have separate `--include-*-experiment` flags. `fit_dura.py` enables context trials only with explicit experiment flags. Store rejected candidate geometry as `.authoring/arteries-rejected.glb` to reproduce the review image with `render_fitting.py --rejected-trial`.

Shared label gaps must be below 0.0002 mm. Triangle indices must remain exact, geometry finite and non-degenerate, and validation hashes current. Zero contacts in one primary phase cannot override a failed family, skull or context check. Matched-plane skin-envelope areas depend on vessel inclination and are not internal lumen diameter measurements.

Anatomical references: [Neuroangio posterior fossa veins](https://neuroangio.org/venous-brain-anatomy/veins-posterior-fossa/), [venous sinuses](https://neuroangio.org/venous-brain-anatomy/venous-sinuses/), [MCA anatomy and variants](https://neuroangio.org/anatomy-and-variants/middle-cerebral-artery/). Source atlas attribution and licences remain in the app.
