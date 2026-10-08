# Modelling and evidence

Run from this directory with Python 3, NumPy, SciPy, VTK and Matplotlib installed. The app npm dependencies provide the source GLB decoder/exporter.

1. `python3 prepare.py`
2. `python3 fit.py`
3. `python3 anchors.py`
4. `python3 build_geometry.py rebuild cavity partition`
5. `python3 venous.py prepare network`
6. `python3 basilar_join.py`
7. `python3 catalogue_joins.py`
8. `python3 build_geometry.py revision`
9. `python3 selfcheck.py partitioned`
10. `python3 validate.py`
11. `python3 extra_checks.py`
12. `python3 check_basilar_collar.py`

Export only after all recorded gates pass. From the app root run:

```
node tools/ica-cs-v0932/export.mjs tools/ica-cs-v0932/candidate tools/ica-cs-v0932/baseline
python3 tools/ica-cs-v0932/finalize_release.py
npm run build
node tools/ica-cs-v0932/check_export.mjs tools/ica-cs-v0932/candidate tools/ica-cs-v0932/decoded
node tools/decode-posterior-baseline.mjs public/anatomy/models tools/ica-cs-v0932/exported
python3 tools/ica-cs-v0932/render.py --exported
```

`candidate` is a work directory created by the scripts. The baseline vascular assets are v0.9.31, checked by SHA-256. The unchanged skull and brain are linked from production by `prepare.py`. Source-derived centreline arrays are provided. Do not substitute a previous rejected trial.

The main-shaft radius check excludes centreline-end estimates from the source's open cut surfaces: those endpoints are handled by the retained native wall collars. It reports its measured scope and raw endpoint-inclusive ratios. Geometry grids and temporary decoded buffers are not distributed. Delete `artery-network-sdf.npy` before rerunning the venous volume after any arterial mesh change; cached distance grids are valid only for the geometry that generated them. `--reuse` reuses branch volumes and is only appropriate when their routes and ports are unchanged.

The exact accepted export, loader, local geometry and physical-join evidence is in `../../anatomy/source/ica-cs-v0932` from the app root. This is an anatomical review build, with estimated dural boundaries and unresolved lower canal contacts.
