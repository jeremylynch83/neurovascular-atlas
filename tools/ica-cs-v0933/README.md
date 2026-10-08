# Posterior cavernous sinus refinement, v0.9.33

Baseline: final v0.9.32 production assets. This local refinement retains their topology and native ophthalmic and superior hypophyseal walls. The posterior sinus roof is reduced independently of the artery by integrating a constrained displacement field in 16 small steps. `constraints.json` keeps delicate native venous collar patches stable during smoothing after trial intersection checks. Arterial centreline displacement is not used. Bounded Taubin smoothing operates on the connected labelled networks, with native ostial parent faces and remote collars fixed. Bone remains fixed.

The Python scripts need NumPy, SciPy, VTK and Matplotlib. Decode v0.9.32 into this directory's `decoded` directory with `tools/decode-posterior-baseline.mjs`. Then run from the app root:

```
python3 tools/ica-cs-v0933/refine.py tools/ica-cs-v0933/decoded
python3 tools/ica-cs-v0933/damp_venous.py .5
python3 tools/ica-cs-v0933/selfcheck.py partitioned
python3 tools/ica-cs-v0933/check_venous.py
python3 tools/ica-cs-v0933/validate.py
node tools/ica-cs-v0933/export.mjs tools/ica-cs-v0933/candidate /path/to/v0.9.32/public/anatomy/models
python3 tools/ica-cs-v0933/finalise.py
npm run build
node tools/ica-cs-v0933/check_export.mjs tools/ica-cs-v0933/candidate tools/ica-cs-v0933/decoded
node tools/decode-posterior-baseline.mjs public/anatomy/models tools/ica-cs-v0933/exported
python3 tools/ica-cs-v0933/render.py --exported
```

The decoder output, candidate buffers and rendering work products are temporary and omitted from the release. The baseline v0.9.32 package must be retained separately to reproduce this refinement. The final assets, comparison images and measured checks are included.
