# Optional upstream MMA authoring, v0.9.89

These scientific tools require NumPy, SciPy, VTK 9.3, Matplotlib and `manifold3d==3.5.4`, plus the existing native triangle helper under `tools/mma-v0958`. They add no browser or ordinary build dependency.

Use a fresh external work directory. Decode the full **v0.9.88** five-model baseline with `node tools/decode-posterior-baseline.mjs BASELINE_MODEL_DIRECTORY WORK/decoded`. Copy the stored `baseline-surface-recipes.json` from `anatomy/source/upstream-mma-v0.9.89` to WORK. Copy the four stored baseline normal buffers into WORK/decoded. Do not substitute the updated v0.9.89 recipes for this fixture.

Run these scripts from the app root, passing WORK as their first argument, in order: `manifold_bounded.py`, `final_weld.py`, `verify_native.py`, `validate_envelope.py`, `accept_checks.py`, then `prepare_normals.py`. The last numerical acceptance step requires the envelope check because facet counts can change when the same exterior is retriangulated. `render_joint.py WORK` makes the targeted diagnostic view. `projections.py WORK BASELINE_APP_ROOT` rebuilds the four closed DSA recipes using the unmodified v0.9.88 app as its second argument.

`manifold_bounded.py` writes a pre-weld report named `manifold-union.json`. It is not the final acceptance report. A right-side Float32 near-duplicate is resolved by `final_weld.py`, preserving original coordinates. The final `native-validation.json` and `export-validation.json` are authoritative. The ordinary VTK trial entry points in imported helper files were rejected and are not the accepted pipeline.

Final baseline/candidate buffers, accepted-corrections and validation reports are stored under `anatomy/source/upstream-mma-v0.9.89`. Copy them to WORK to repeat only the export stage. Copy the v0.9.88 arterial GLB as WORK/old-complete-circulation.glb and place source-assets.json under WORK/decoded. Run `node tools/patch-attachment-collars.mjs WORK WORK/old-complete-circulation.glb WORK/complete-circulation.glb`, then `node tools/verify-upstream-mma.mjs WORK WORK/complete-circulation.glb`. These commands write staging files and reports. They do not install a new app release.

The full release also updates manifest bounds/hashes and attachment review metadata, refreshes four injection entries and their directed attachment distances, and verifies reuse of the remaining 593 course entries. Run the production build, DSA suite and course tests after integration. Whole-atlas anatomical acceptance remains false.
