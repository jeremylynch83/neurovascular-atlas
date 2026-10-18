# Left inferior petrosal wall cleanup, v0.9.115

Copy anatomy/source/petrosal-wall-v0.9.115 to a fresh WORK directory. Use absolute WORK and CACHE paths. Tools require the Python/VTK repair environment and project Node dependencies. The decoded baseline buffers are immutable; the original source venous GLB is available in v0.9.114.

- reconstruct.py WORK CACHE replays spec.json and checks displacement, orientations, source indices, weld partitions, fixed boundaries and all three native interfaces. Accepted buffers must match exactly.
- validate_self.py WORK CACHE checks every selected face. Exactly the three recorded unchanged pairs may remain; new self contacts fail.
- validate_crossings.py WORK CACHE checks changed faces against all named scene surfaces.
- validate_depth.py WORK CACHE checks paired closed-volume samples and conservative open-surface separation. Regional fitting remains open.
- test_clearance.py verifies analytic separation, crossing and touching cases.
- export.mjs WORK SOURCE_GLB OUTPUT_GLB exports the passing candidate. Preserve the v0.9.114 source as WORK/old-venous.glb and the result as WORK/venous.glb for verify-export.mjs WORK. Verification checks all 231 veins, the other four assets, exact accepted buffers, all source face indices and all original stored normal components.
- projections.py WORK CACHE refreshes only the selected proxy volume and retains native cap rims and source index lineage.
- verify-flow.mjs WORK checks graph/generator hashes, all vein bounds and original flow data against WORK/old-dsa-flow.json, then refreshes the venous source hash only. Export validation is required first; install the verified candidate before the flow check.
- check_deferred.py [APP] checks the current 15-case exclusion registry. Source and validation implementation hashes must both match. These exclusions apply only to recorded search scopes; all anatomical findings remain open.

Run Python scripts with python3 and JavaScript scripts with node. See docs/PETROSAL_WALL_BATCH23_v0.9.115.md for accepted scope and remaining issues. No full-atlas render is required for this numerical cleanup.
