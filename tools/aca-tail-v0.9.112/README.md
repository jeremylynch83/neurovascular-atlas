# Bounded distal left A5 fit, v0.9.112

Copy anatomy/source/aca-tail-v0.9.112 to WORK before replay. Use absolute WORK and CACHE paths. The historical source GLB is recoverable from v0.9.111.

- reconstruct.py WORK CACHE replays spec.json from immutable decoded baseline buffers, checking fixed native interfaces/boundaries, normals, source face orientation, weld partitions and every arterial mesh. Accepted buffers must match byte for byte.
- validate_crossings.py WORK CACHE checks every changed face against the entire scene, including self/adjacent faces. Zero new non-neural crossings are allowed. One unique source self-contact pair (1156,1222) remains; acceptance also proves exact rigid translation and unchanged stored normals for all its vertices.
- validate_depth.py WORK CACHE checks matched samples against closed tissue volumes, with no new entry or depth increase over 0.001 mm. Open surfaces require enclosing-ball separation. Residual embedding is explicitly retained.
- validate_full_clearance.py WORK CACHE certifies only the distal 1,209-triangle section at source Y <= -95.1 mm outside the corpus callosum. Despite its inherited filename, it does not certify the whole A5 label. Area coverage and centroid parity are checked. Unresolved leaves fail.
- test_clearance.py checks separated, crossing and touching analytic cases.
- decode-normals.mjs SOURCE_GLB WORK/decoded extracts raw SNORM16 normals.
- export.mjs WORK SOURCE_GLB OUTPUT_GLB requires passing native-validation.json. verify-export.mjs WORK checks exact accepted buffers, all face indices, retained corner normals, 598 other circulation meshes and four other GLBs.
- projections.py WORK CACHE preserves source index lineage, caps and native rims while updating the selected proxy positions.
- Refresh only the ID in selected-course-ids.json. verify-flow.mjs WORK preserves all unselected courses and graph semantics; it requires old-dsa-flow.json.

See docs/ACA_TAIL_BATCH20_v0.9.112.md for scope, excluded trials and unresolved findings. No full-atlas render is required for this bounded correction.
