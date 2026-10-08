# Anterior cavernous sinus rim, v0.9.35

The v0.9.34 wall repair left an irregular anterior rim around the ICA opening. Its topological checks passed because the inner and outer walls were connected, but that did not establish an acceptable rim shape.

## Correction

The anterior chamber profile is adjusted locally to give a fuller wall around the fixed ICA. A smooth field intersection rounds the chamber/ICA-channel junction over a 0.9 mm blending band, avoiding a knife edge where the outer wall meets the channel. The posterior roof reduction remains in place. The corrected chamber is united with the retained venous network and remeshed as one connected surface, then repartitioned into selectable structures with shared normals and native remote collars.

Only the venous asset changes from v0.9.34. Arterial geometry, including the ophthalmic origins, remains exact. The original v0.9.33 authoring buffers are used with the v0.9.34 chamber reconstruction and an additional anterior correction, avoiding repeated resampling of remote veins.

## Checks and review

Each sinus is connected with no unmatched boundary edges or degenerate triangles. Main tributaries retain shared joins. The checked regional venous surfaces have zero detected non-adjacent intersections, and the sinus labels have no detected primary ICA or skull-base bone contacts. The production build and Three.js/Meshopt position/index/normal checks pass.

`review-renders/ICA_CS_rim_repair_depth.png` compares decoded v0.9.34 and final v0.9.35 assets with identical camera and scale. It uses depth-buffer rendering, including both sinus networks, to avoid the misleading surface-order artefacts of the previous plotted renders. It is a model render rather than an interactive app screenshot.

The remote browser could not reach the local development server, so live in-app verification was not completed. The exact marked view still needs review in the installed app. The ICA retains its entry and exit through the sinus boundary; these physiological openings are not intended to disappear. Dural boundaries remain estimates.

Authoring scripts: `tools/ica-cs-v0935`. Intermediate grids and decoded buffers are excluded from the ZIP. Use the v0.9.33 geometry authoring baseline and v0.9.34 GLB export baseline. Run repair, joined normals, topology/clearance/self-intersection checks, export, finalisation, build and loader checks, then decode the output and run `render_depth.py`. Detailed results are under `anatomy/source/ica-cs-v0935`.
