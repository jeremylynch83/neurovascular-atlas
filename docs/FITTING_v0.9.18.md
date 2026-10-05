# v0.9.18: bilateral central arterial family fit

This release applies the left and right central arteries, their cortical branches and distal rami, and the adjoining MCA superior-division transitions. Eight arterial labels change. All 591 other arterial labels retain their position, normal and index buffers exactly. All 104 venous labels, all 188 brain surfaces, the skull and the anastomosis asset remain unchanged. The v0.9.13 ICA and cavernous corrections are preserved.

The dural and brainstem groups remain deferred for the tissue-corridor problems documented in the [v0.9.16 findings](FITTING_v0.9.16.md). Their original geometry is retained. This is a regional atlas fitting release, not completion of the remaining vessel fitting programme.

## What changed

The main arteries follow the registered central sulcal region. Each attached branch has an independent cortical course rather than inheriting the main artery's displacement. A finite regional search checks named cortical surfaces, skull clearance and separation from the main vessel outside the intended join. Original branch wall sections are transported with rotation-minimising frames. Source-bound collars and short ramus take-off sections retain the joined skin; cortical end caps are transported rigidly.

The right main artery's folded terminal trial is replaced by ordered whole sections. A short join-bearing interval is adjusted 1.2 mm medially and 0.6 mm posteriorly, with smooth stationary end collars, to provide room for the branch outlets. The left ramus retains a 2.5 mm source-bound take-off section and the right a 2.0 mm section. No brain deformation is applied. Original vessel IDs, vertex counts and triangle indices are retained, and shared normals are recomputed for the changed labels.

The normal viewer loads the corrected production circulation asset. Experimental fitting runs only in the offline authoring tools. The compact primary seed is provenance, not a viewer asset or an accepted standalone vessel fit.

## Acceptance evidence

The complete eight-label family passes these checks on its final skin:

- No new or increased whole-wall contacts with named tissue or skull surfaces. The central arteries and all four attached branches have zero checked tissue contacts. The two distal rami's baseline parietal contacts, 92 left and 122 right, become zero.
- Zero nonadjacent skin self-intersections for every changed label. Earlier candidates that cleared neighbouring tissue but folded their own walls were rejected.
- Zero arterial contacts outside the original anatomical join collars, including all edited labels against every retained artery and each other.
- Exact original triangle indices and coincident labelled joins. The maximum measured shared-coordinate gap is 0.000009 mm, below the 0.0002 mm gate.
- Exact decoded exported position, normal and index buffers; asset bindings and course hashes match the delivered files.
- Byte-identical reproduction of the complete authoring asset from the supplied compact seed, in an isolated directory.
- Eleven invalid publication fixtures rejected, covering stale hashes, incomplete families, opened joins, self-intersections, new tissue/skull/arterial contacts and failed wall-envelope checks.

The MCA parent labels retain their pre-existing opercular tissue contacts: 225 left and 243 right. Their contact counts do not increase. Those proximal relationships still need their own regional anatomical review; the whole MCA course is not declared fitted.

## Wall-envelope measurements and limits

Material correspondence follows the same original wall intersections through the deformed triangle edges. Each contour is projected onto its own best-fit plane. This avoids comparing a moved oblique branch with unrelated fixed world planes. These are outer skin-envelope measurements, not internal lumen segmentations or proof of patency.

| Label | Minimum area ratio | Median area ratio | Maximum area ratio |
| --- | ---: | ---: | ---: |
| Central left | 0.569 | 1.139 | 1.562 |
| Central right | 0.548 | 1.095 | 1.648 |
| Cortical branch left | 1.000 | 1.000 | 1.000 |
| Cortical branch right | 1.000 | 1.000 | 1.000 |
| Distal ramus left | 0.767 | 1.000 | 1.002 |
| Distal ramus right | 0.792 | 0.999 | 1.000 |

These ratios include changed inclination, section distortion and blended joins. They must not be described as unchanged transverse calibre or direct lumen diameter ratios. The minimum gates are 0.5 for primary material envelopes and 0.55 for branch envelopes. These are modelling rejection thresholds, not anatomical acceptance criteria. The main profiles and branch take-offs remain subject to anatomical review.

Open cortical atlas surfaces do not support reliable solid containment. Triangle contact tests include their actual surfaces, but a passing atlas skin test does not establish full anatomical accuracy. Sulcal/fissural guide sheets, dura and ventricular references are excluded from the solid-tissue contact audit. Existing unedited relationships remain outside this regional correction.

## Files and reproduction

- `validation/central-rebuilt-acceptance-v0.9.18.json`: final whole-family, skull, tissue, self-intersection, arterial-neighbour and material-section audit, bound to the exact authoring hash.
- `validation/central-rebuilt-trial-v0.9.18.json`: source/destination courses, search routes, branch wall contacts and correspondence.
- `validation/central-publication-guards-v0.9.18.json`: invalid-fixture rejection checks.
- `validation/central-reproduction-v0.9.18.json`: isolated byte-identical reconstruction proof.
- `validation/fitting-export-v0.9.18.json`: exact delivered buffer and course-binding verification.
- `validation/central-rebuilt-comparison-v0.9.18.png`: matched baseline/applied views with translucent and opaque context.
- `../anatomy/source/brain/central-courses-v0.9.18.json`: applied regional branch courses and delivered asset hashes.
- `../anatomy/source/brain/trials/central-primary-seed-v0.9.18.glb`: four exact primary/parent seed labels, separate from the viewer assets.

Prepare the delivered v0.9.15 baseline as described in the preceding checkpoint report. Use its ZIP, rather than v0.9.18's corrected circulation, as the baseline. Authoring requires NumPy, SciPy, trimesh, VTK, Pillow and the app's Node dependencies. Normal installation needs no new dependencies.

```sh
node tools/decode_glb.mjs anatomy/source/brain/trials/central-primary-seed-v0.9.18.glb .authoring/central-primary-seed.glb
python3 tools/brain/rebuild_central_branches.py --experimental --primary-checkpoint .authoring/central-primary-seed.glb
python3 tools/brain/verify_central_rebuild.py
python3 tools/brain/check_central_reproduction.py
python3 tools/brain/check_central_guard.py
node tools/compress-venous.mjs .authoring/central-rebuilt-trial.glb .authoring/central-rebuilt-export.glb
node tools/decode_glb.mjs .authoring/central-rebuilt-export.glb .authoring/central-rebuilt-export-decoded.glb
python3 tools/brain/publish_central_rebuild.py
npm run build
python3 tools/brain/verify_release_export.py --release 0.9.18 --arteries-authoring .authoring/central-rebuilt-trial.glb --arteries-exported .authoring/central-rebuilt-export-decoded.glb
```

The reconstruction tool requires `--experimental`, writes authoring-only outputs and never publishes geometry. The dedicated publisher checks current hashes, the complete family, exact staged export buffers and the four retained production assets before changing the app. The older v0.9.17 publisher is a historical checkpoint tool and must not publish this release.

The production build and Chromium browser checks cover model loading, search, course links, guide selections, focus, visibility and sections. Installer logic is unchanged from the previously tested checkpoint. No remote deployment was performed during this implementation.
