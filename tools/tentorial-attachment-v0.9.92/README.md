# Optional tentorial attachment tools, v0.9.92

Use NumPy, SciPy and VTK 9.3 plus the existing tools/mma-v0958 triangle helper. Export uses the application's Meshoptimizer and Three.js dependencies. Ordinary application use adds no dependencies.

Start from the v0.9.91 full release and a fresh external WORK directory. Decode all five model files with tools/decode-posterior-baseline.mjs, writing WORK/decoded. Save the v0.9.91 arterial GLB as WORK/old-complete-circulation.glb. Do not run repair on already patched geometry.

Run repair.py WORK, then validate.py WORK. Repair selects only the explicitly bounded six-edge left gap and three triangular right gaps. It retains every source vertex and triangle and appends seven wall faces. Validation checks the additions against the entire delivered scene. It also measures restored native coordinates. Existing unrelated defects are not reclassified as resolved.

Run node tools/tentorial-attachment-v0.9.92/export.mjs WORK WORK/old-complete-circulation.glb WORK/complete-circulation.glb, then verify-export.mjs WORK. Source normal integers are copied, with no octahedral re-quantisation. The real app loader verifies exact source attributes and faces, exact candidate data, the unchanged other 597 arterial meshes and four assets.

Run projections.py WORK BASELINE_APP to stage two refreshed closed projection recipes. Install only after numerical checks pass, update current asset hashes and course bindings, and refresh the two affected flow entries with tools/build-dsa-flow.mjs --only. Verify all other entries, graph, sites and unchanged generator before restoring the existing generator hash. Run the ordinary production build and complete DSA checks.

The package includes the two baseline position/index buffers and candidate buffers. They permit numerical comparison without installing another model. Full re-export uses the v0.9.91 source asset identified by source-assets.json. Wider regional anatomy, right ACA and receiving lumens remain open.
