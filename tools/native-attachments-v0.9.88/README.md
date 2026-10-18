# Optional v0.9.88 attachment authoring tools

Run from the application root. Python authoring requires NumPy, SciPy, VTK and Matplotlib; these are not app runtime dependencies. Use an empty external work directory with a `decoded` subdirectory. Decode all five **v0.9.87** baseline models using `node tools/decode-posterior-baseline.mjs BASELINE_MODEL_DIRECTORY WORK/decoded`. This supplies the complete scene and `meshes.json`, not just the four stored snapshots.

`python3 tools/native-attachments-v0.9.88/mma_network.py WORK` builds and screens coupled routes. Then run `verify_network.py WORK` to compact candidate buffers and check shared edges, protected coordinates and components. `check_sinus.py WORK` uses the unchanged represented sinus and current proxy for the inclusion diagnostic. These scripts import the workspace from the first positional argument.

`render.py WORK APP_ROOT` creates the diagnostic projection. `projections.py WORK BASELINE_APP_ROOT` derives new closed recipes from the **unmodified v0.9.87** manifest and recipes. It writes workspace data without installing it. Do not use refreshed v0.9.88 recipes as the baseline. Do not install failed candidates.

Final candidate buffers, the accepted-corrections list and reports are stored under `anatomy/source/native-attachments-v0.9.88`. Copy that directory into a work directory for export. Copy the v0.9.87 arterial GLB as `WORK/old-complete-circulation.glb`, and put its `source-assets.json` under `WORK/decoded`. Run `node tools/patch-attachment-collars.mjs WORK WORK/old-complete-circulation.glb WORK/complete-circulation.glb` for lossless export. Run `node tools/verify-mma-falcine-export.mjs WORK` after installing the final model in an isolated app copy. The final report records all unchanged buffer and asset checks.

The two geometry-bound injection guides are stored in the generated manifest. Their node buffer hashes and point counts are recorded in `course-guide-summary.json`. `npm run dsa:flow` validates guide hashes and derives routes; `npm run dsa:test` validates source and geometry identity, injection selection and containment. Broader anatomical issues remain open.
