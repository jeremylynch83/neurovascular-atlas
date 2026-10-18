# Intersection classification batch 9, v0.9.101

This batch fixes the offline geometry checker and clears one incorrect defect flag. No anatomical geometry is changed. The reported residual right A5 self-intersection (faces 5129/5204) is a shared-vertex contact, not a positive crossing. The larger pericallosal/cortical and receiving-lumen findings remain open.

## Root cause and independent proof

The source face normals differ by a sine of approximately 3.18e-8. The previous checker treated vertices within 1e-7 mm of the opposing plane as lying on that plane. Plane separations of approximately 1.02e-8 mm then expanded the shared point into an artificial overlap interval. This is a numerical classification error, not a reason to reshape the vessel.

Every stored Float32 coordinate has an exact binary rational representation. Independently evaluated signed plane determinants are:

| Points tested | Exact signs | Non-zero determinant |
| --- | --- | --- |
| Triangle B against plane A | -1, 0, -1 | -4819217/18014398509481984 |
| Triangle A against plane B | 0, -1, 0 | -4819217/18014398509481984 |

Triangle B is on one side of plane A and touches it only at its shared vertex. The intersection therefore cannot contain a positive-length interval or positive area. An exact local audit covers 46 source faces and 323 candidate triangle pairs. Only the recorded pair changes classification; no exact positive crossing is found in that neighbourhood. This local result does not establish whole-course acceptance.

## Checker correction

When the sine of the angle between normals is below 1e-6, the checker uses exact rational plane-side signs, line intervals and coplanar positive-area clipping. It represents the supplied binary values exactly, without rounding decimal coordinates. The default 1e-7 spatial tolerance is not relaxed. Ordinary non-parallel pairs retain the fast numerical path. Genuine arbitrarily shallow crossings and thin positive coplanar overlaps remain rejected. Point/shared-edge contacts remain allowed. Existing authoring trial signatures hash geometry.py, so earlier cached decisions are invalidated automatically.

Three added regression methods cover the real A5 pair across winding/order symmetry and exact dyadic transforms, true near-parallel crossings, separated parallel triangles, shared-edge contacts and extremely thin coplanar overlap. All 22 repair tests pass. The 15 arterial and 39 venous wall repairs from the previous two batches replay byte for byte under the new checker, with 620 and 841 changed-face triangle pairs checked respectively. The arterial global gate still passes for all 121 affected coordinate edges.

## Retention and release checks

All five GLBs, all 1,250 named meshes, DSA flow and surface recipes, and all 21 runtime source files are byte exact to v0.9.100. Vessel-course data differ only in the release marker. All 1,666 catalogue structures, relationships and asset bindings remain unchanged. The full build and DSA checks pass: 828 closed/oriented proxies, 8,971,508 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. This is an offline authoring change; it adds no browser dependency or runtime work.

The issue ledger now reclassifies only the recorded residual right A5 pair. Historical v0.9.96 measurements remain preserved with their original method, while the current issue entry and this report explain the correction. Bilateral cortical/pericallosal registration, complete receiving lumens, regional Galenic/petrosal/dural/canal findings, remote topology defects and the separate ILT interface remain open.

Evidence: `anatomy/source/intersection-v0.9.101`. Portable audit: `tools/intersection-v0.9.101/audit.py WORK CACHE`. Detailed report: `docs/validation/intersection-v0.9.101.json`. No full-atlas render or physical mesh repair is performed.
