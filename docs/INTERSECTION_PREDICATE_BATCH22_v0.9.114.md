# Intersection predicate repair batch 22, v0.9.114

This batch fixes the authoring repair validator. Twelve previously reported wall crossings are tolerance artefacts. Exact binary-coordinate checks reject those reports and retain all 22 genuine petrosal cases in the regression cohort. No model geometry changes and no anatomical defect is claimed repaired.

| Reviewed source pair cohort | Previous reported pairs | Exact reported pairs | False reports corrected |
| --- | ---: | ---: | ---: |
| Inferior petrosal left | 17 | 12 | 5 |
| Inferior petrosal right | 16 | 10 | 6 |
| Left A5 source faces 1156/1222 | 1 | 0 | 1 |
| Total | 34 | 22 | 12 |

The bilateral petrosal scans check 76,606 potentially intersecting triangle pairs over the complete labels. The corrected scan retains exactly the known exact-positive pairs from the original reports and removes the 11 exact-negative pairs. Adjacent triangles are included: a shared vertex does not automatically excuse a genuine wall overlap. These pair counts are not counts of independent anatomical defects and do not use the older non-adjacent-only audit definition.

The left A5 pair reported as an inherited contact in batch 20 is also exact-negative. Its original report remains as historical evidence, with the current issue record explicitly superseding that classification. The vessel was not moved again. Residual left A5/corpus-callosum depth remains 0.195 mm, and wider ACA registration remains open.

## Root cause and correction

The previous floating-point plane-cut routine treated every triangle vertex within 0.0000001 mm of the opposite plane as lying on it. This can turn a point-sized or separated contact into an interval with positive overlap. Its existing exact fallback covered almost-parallel normals but missed other ill-conditioned point/plane cases.

The repaired predicate uses exact-coordinate bounding boxes and conservative floating-point separation filters. Distinct non-parallel triangles sharing an edge cannot overlap beyond that shared edge. A shared point can be rejected quickly only when the remaining vertices of a triangle are strictly on the same side of the other plane, beyond the uncertainty threshold. Ambiguous plane distances and every remaining potentially positive intersection use the exact binary-coordinate predicate. The floating-point cut no longer adds vertices merely because they are close to the plane.

The tolerance is now an uncertainty threshold for filtering. It does not thicken the represented triangles or discard a small genuine crossing. Degenerate triangles have no positive-area crossing and return without invalid normal division; separate topology/area gates still reject degenerate candidate faces. This does not permit degenerate repairs.

## Regression coverage

Immutable production-coordinate fixtures contain the 33 petrosal pairs and the retained left A5 pair. Expected classifications are fixed from exact binary-coordinate checks. False cases are checked under winding permutations and reversed argument order. Genuine petrosal cases are checked under argument reversal, power-of-two scaling and translation. Existing analytic tests retain transverse crossings, positive coplanar overlap, extremely thin genuine intersections, separated parallel triangles and valid shared-edge contacts. A deterministic 128-case differential check compares the conservative filters with the exact predicate for ordinary, nearly coplanar and shared-coordinate cases.

All 30 repair tests and three clearance tests pass. The standalone verify-fixtures.py also verifies all 34 production pairs. The single-pass fixture diagnostics record approximately 0.0063 seconds for the old 33-case routine and 0.0116 seconds for the corrected routine on this run. These are diagnostics, not a whole-atlas speed benchmark or a runtime-performance claim. The purpose is reliable authoring decisions and fewer wasted repair searches.

## Correct invalidation of prior exclusions

The batch 21 shortcut recorded geometry hashes only. A predicate change must invalidate earlier surface-search results even when the geometry is unchanged. check_deferred.py now requires five source asset hashes and four validation implementation hashes. Legacy records without implementation hashes require review and return exit code 2. A code-only hash mismatch also returns exit code 2. The matching current registry returns exit code 0. All three cases are verified without modifying the models.

The main authoring trial cache already includes the repair tool source hash in its signature. The changed geometry.py produces a different tool hash, so cached trials under the old predicate cannot be silently reused. Both hashes are retained in the evidence.

The 132 direct SCA/Wollschlaeger gap triangulations are rechecked under the corrected predicate and still fail retained-wall contacts. That case remains deferred. Thirteen fixed-rim tissue exclusions are retained because their boundary-point membership, source models and enclosed-volume implementation are unchanged. The new registry therefore covers 14 recorded cases. Eleven other legacy surface-search cases, including the earlier larger SCA local search, require review under the new predicate before their outcomes are reused. This is not a claim that those repairs will succeed.

Historical batch 21 replay scripts deliberately fail the updated implementation check when supplied with their geometry-only registry. Reproducing their original results requires the v0.9.113 implementation as well as its geometry. Current petrosal scan and fixture replay tools are supplied under tools/intersection-predicate-v0.9.114.

## Atlas retention and limits

All five GLBs, all 1,250 named meshes, every previous geometry repair, all 21 runtime source files, 1,666 catalogue structures, relationships, and the complete DSA surface and flow data are unchanged from v0.9.113. The full build and DSA checks pass: 828 closed/oriented proxies, 8,971,510 triangles, 579 selectable arterial courses and 2,353 closed sections. Issue-register copies agree and the original unresolved ILT interface is retained. No full-atlas render was performed.

Twenty-two exact petrosal contact pairs, residual vessel/cortex registration, full receiving lumens, SCA/native-wall reconstruction, Galenic/dural/canal findings, seven zero-area arterial triangles and the other recorded anatomical issues remain open. Exact predicate agreement is not anatomical or physiological approval. No independent imaging or segmentation was added.

Evidence: anatomy/source/intersection-predicate-v0.9.114. Report: docs/validation/intersection-predicate-v0.9.114.json.
