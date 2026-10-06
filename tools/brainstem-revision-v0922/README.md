# Authoring inputs for the v0.9.22 revision

Production models are already included in this app. This optional toolkit reproduces the deformation from the exact delivered v0.9.21 baseline, not from v0.9.22.

Place a complete copy of the baseline in `app/` beside `work/`. The required baseline hashes are recorded in the export report. Install the app Node dependencies and Python NumPy, SciPy and VTK. From this directory run:

```sh
node decode-all.mjs app/public/anatomy/models decoded
python3 work/revise_cached.py --pons 1.7 --midbrain 0.8
python3 work/validate.py
```

Require `candidate/validation.json` to pass. From the baseline `app/` directory, run `node ../work/export-brainstem-revision.mjs ../candidate`, then build normally. The exporter is for one application to v0.9.21 and rebinds surface anchors and vessel course identities.

The movement field is constant across the relevant anterior vessel walls, tapers into fixed tissue and outlets, and preserves shared input coordinates. The clival plexus and distal cerebellar SCA branches remain stationary. Collision checks retain whole triangles that overlap a shared bounding box; this is a broad-phase speed optimisation, not mesh decimation. Existing baseline contacts, including V4/plexus contacts, remain recorded separately. The evidence assesses incremental changes, not complete anatomical correctness. Browser GPU appearance was not checked in this session; the production build and actual Three.js loader were checked.
