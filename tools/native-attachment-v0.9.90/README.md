# Optional native attachment tools, v0.9.90

The accepted correction is one native seam in MMA petrosquamosal left. Scientific checks require NumPy, SciPy, VTK 9.3, Matplotlib and the existing native triangle helper under `tools/mma-v0958`. The app has no new dependency.

Use a fresh external WORK directory. Decode all five **v0.9.89** baseline assets with `node tools/decode-posterior-baseline.mjs BASELINE_MODEL_DIRECTORY WORK/decoded`. Copy the stored two baseline normal buffers from `anatomy/source/native-attachment-v0.9.90/baseline` into WORK/decoded. Copy the full v0.9.89 `public/anatomy/dsa-surfaces.json` as WORK/old-dsa-surfaces.json. The small stored baseline-dsa-recipe.json is a provenance fixture, not a replacement for that complete dataset.

Run `python3 tools/native-attachment-v0.9.90/petro_local.py WORK`, then `prepare_export.py WORK`. The first script tests native rim alignment and all potentially changed intersection/contact pairs. A new intersection must involve a changed face, so the exact triangle test compares every affected triangle against the whole source mesh and parent; it does not repeat unchanged remote pairs. Full-scene contact screening uses the changed faces and all overlapping named structures. All native indices remain exact. The corrected harmonic boundary condition gives the other fixed rims zero total displacement.

`prepare_export.py` verifies paired boundary edges, keeps old normals outside the local change, copies exact parent normals at the new seam, and refreshes only the affected closed-proxy cap centre and volume. `render_petro.py WORK` makes the targeted before/after image.

For export only, copy the stored final candidate and accepted-corrections into WORK. Put the v0.9.89 arterial model at WORK/old-complete-circulation.glb and its source-assets.json under WORK/decoded. Run `node tools/patch-attachment-collars.mjs WORK WORK/old-complete-circulation.glb WORK/complete-circulation.glb`, then `node tools/verify-petrosquamosal-export.mjs WORK WORK/complete-circulation.glb`. These commands stage the export; they do not install it. Repeat the ordinary build and full numerical DSA checks after metadata and cache integration.

`probe_right.py` and `shorten_port.py` reproduce the right ACA feasibility diagnostics. Those outlet candidates are excluded. They are not part of the accepted correction and must not be installed. Their source A5 port is inside the registered cortex, and neighbouring native outlets limit local shortening. The wider registration issue remains open.
