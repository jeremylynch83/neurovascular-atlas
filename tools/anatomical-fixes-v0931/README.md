# v0.9.31 authoring and checks

Production installation only requires the normal app build. These authoring tools operate on decoded full-resolution buffers and require NumPy, SciPy and VTK; matched renders additionally require Matplotlib. They are not runtime dependencies.

Inputs are the exact v0.9.30 assets and their decoded positions/indices, including the previous v0.9.29 corrections. Baseline asset hashes and all accepted placement parameters are recorded in `docs/validation/anatomical-mesh-authoring-v0.9.31.json`. Intermediate exploratory meshes are deliberately excluded from the release.

The tools use the shared v0.9.29 `geometry.py` and `extract_curves.py` helpers. Configure `fixes-work/baseline` and `audit-work/decoded` adjacent to the app as those helpers specify. Do not decode the already corrected v0.9.31 assets and then apply the adjustments again.

Accepted-candidate sequence, run from the app directory:

1. `python3 tools/anatomical-fixes-v0931/build_candidate.py --recorded`
2. `python3 tools/anatomical-fixes-v0931/check_candidate.py`
3. `python3 tools/anatomical-fixes-v0931/round_veins.py`
4. `python3 tools/anatomical-fixes-v0931/check_rounding.py`
5. `python3 tools/anatomical-fixes-v0931/prepare_final.py`
6. `python3 tools/anatomical-fixes-v0931/check_final.py`
7. `python3 tools/anatomical-fixes-v0931/check_recovered_walls.py`
8. `node tools/anatomical-fixes-v0931/export.mjs ../corrections-work/candidate-final ../fixes-work/baseline`
9. `python3 tools/anatomical-fixes-v0931/finalise_catalogue.py`
10. `npm run build`
11. `node tools/anatomical-fixes-v0931/check_export.mjs ../corrections-work/candidate-final ../audit-work/decoded`

Do not export unless the final geometry and recovered-wall reports pass. The exporter and catalogue finaliser enforce these gates. Back up the catalogue and use the original baseline before authoring; finalisation replaces the v0.9.31 regional-adjustment entry if rerun.

The search and trial scripts document exploratory attempts. Rejected dural and pericallosal buffers are never copied into production. See the release report for their results and the unresolved anatomical calibration work. The Jacobian check covers the placement field, while the recovered-wall check separately compares non-adjacent triangle contacts before and after wall recovery. Existing ostial folds are protected, not certified as repaired.
