# Orbital venous repair v0.9.120

Reference teaching reconstruction with posterior IOV-to-SOV drainage on each side. Pterygoid communication and every pre-existing inter-label attachment coordinate are retained. The new mid-branch radius is illustrative (0.60 mm). The left IOV dip receives a bounded, coherent displacement of approximately 0.8 mm.

`repair.py` requires an unpacked v0.9.119 baseline, Python NumPy/SciPy/VTK, and environment variables `ATLAS_BASELINE_ROOT` and `ATLAS_ORBITAL_WORK`. It writes candidates only. Run `check.py`, `selfcheck.py` and `projections.py` against that workspace. `normal-inputs.mjs BASELINE WORK` supplies original normals; `finalise.py` preserves remote corner normals and blends local collars; `projections.py export` refreshes the final DSA recipes.

`export.mjs EXPORT_DIR BASELINE_GLB OUTPUT_GLB` writes the four changed nodes losslessly. `verify.mjs BASELINE_APP` independently decodes and checks the installed model. `refresh-flow.mjs BASELINE_APP` reuses arterial flow only after proving its geometry, graph, guides and generator unchanged; it updates the four venous placement sites.

`install.py` is the release-specific metadata assembly record and contains the original authoring workspace paths. Do not run it as an app command. The model buffers, authored curves and final validation are retained under `anatomy/source/ophthalmic-v0.9.120`.

The build/runtime needs no Python geometry libraries. Clinical review is still required: orbital soft-tissue references are absent, branch calibre is illustrative and existing remote mesh defects remain outside this repair.
