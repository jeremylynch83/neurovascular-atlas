# Optional authoring replay

The app build and runtime do not require these scripts. They preserve the labelled-skin construction and checks without including large modelling buffers.

Copy work/ to a separate authoring folder. Supply the exact v0.9.27 models under baseline/models/, the current app under app/, and decoded v0.9.27 position/index arrays with meshes.json under decoded/. Copy anatomy/source/posterior-veins-v0.9.28.json to candidate/courses.json. Run build.py and validate.py, then export-posterior-veins.mjs from app/ against the supplied baseline venous.glb. check-posterior-veins.mjs verifies the actual loader output, supplying candidate/ and decoded/ as its arguments. The baseline SHA-256 guard is mandatory.

Python dependencies: NumPy, SciPy, VTK, manifold3d, Matplotlib. Node dependencies are provided by the normal app package. Detailed source fields, final courses, calibration limits and geometry reports are retained in the app.
