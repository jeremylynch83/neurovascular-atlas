# Native arterial wall review batch 21, v0.9.113

No additional geometry repair passes all acceptance gates in this batch. This is a review checkpoint: every model is byte-identical to v0.9.112, and no anatomical finding is claimed resolved. All prior repairs are preserved.

## Findings

| Search scope | Examined | Result |
| --- | ---: | --- |
| Original eight-point right SCA/Wollschlaeger gap | 132 boundary triangulations | Every option contacts retained wall. |
| Same gap plus three adjacent source SCA faces | 4,620 local retriangulation states | No examined state is clear of retained wall. |
| 23 other surviving mixed-label native gaps | 637 boundary triangulations | None passes all surface and tissue gates. |

The original SCA gap spans approximately 0.0525 mm. The local reconstruction domain includes the original eight gap points plus one existing SCA point and source faces 23440, 23558 and 23559. The nine-point, nine-face disk retains a seven-edge external boundary. All 4,620 discovered states were examined, with a ceiling of 20,000 states that was not reached. At least one retained-wall contact remains in every examined state. This describes the recorded local search component, not every possible reconstruction algorithm or larger domain. A preliminary attempt to form a simple polygon after removing only two faces produced a repeated boundary vertex and was excluded.

The other-gap cohort is selected from surviving loops in the earlier native-wall scan: mixed-label ownership, no recorded bad-edge contact, at most eight boundary vertices and maximum span 0.3 mm. Every current global rim edge is rechecked to have exactly one source incidence with consistent orientation. Triangles use existing source coordinates only. All enumerated boundary triangulations are checked for positive area, retained-surface contacts and self-crossings. Their 5,608 potentially intersecting source triangle pairs are screened.

Thirteen loops have surface-clear candidates, but their fixed native rim vertices are inside closed registered tissue: the bilateral olfactory-sulcus bodies or left gyrus rectus. Because every boundary-only option retains those inside rim points, changing its diagonals cannot satisfy the tissue gate. These attempts are excluded. The ten other loops have no non-degenerate, surface-clear boundary triangulation in the recorded search. This does not establish that a different method or larger reconstruction cannot succeed.

## Reusable exclusions

The machine-readable deferred-repairs.json records 25 search cases covering 24 small gap locations. Each case states its method scope, result and next requirement. These are deferred cases, not completed repairs or newly discovered major anatomical defects.

check_deferred.py hashes all five source GLBs. While every hash matches this reviewed baseline, later batches can reuse the recorded exclusions for these exact searches. If any source bytes change or an asset is missing, it returns status baseline-changed-review-required and exit code 2. This conservatively invalidates the shortcut; a different repair method or region is outside the recorded exclusion scope. The guard is verified with both matching source assets and an intentionally mismatched expected hash, without editing the models.

The replay scripts require this exact geometry baseline before applying recorded face IDs. Copy the evidence to a fresh working directory when replaying. They do not install a GLB or alter the atlas.

## Next work

The SCA case needs review of a wider receiving-wall region and its opposing wall, rather than another fill of the same small boundary. The 13 tissue-embedded rims require coordinated vessel/cortex registration before wall closure. Other anatomical groups remain available for separate work. The fixed-rim, boundary-only searches recorded here should not be repeated against unchanged source geometry merely by choosing another diagonal.

The remaining ACA/callosal/cortical registration, receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial faces, PICA/native-wall issues and separate ILT native interface remain open. No independent anatomical imaging or target segmentation was introduced.

## Retention and checks

All five source GLBs, all 1,250 named meshes, all 21 runtime source files, all 1,666 catalogue structures and relationships, and the complete DSA surface and flow data match v0.9.112. The left A5 residual depth of 0.195 mm and existing native wall contact from batch 20 remain unresolved. Previous right A5 clearance is preserved because its geometry and targets are unchanged.

The full build, 22 repair tests, three clearance tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 proxy triangles, 579 selectable arterial courses and 2,353 closed sections. No full-atlas render was performed. The original unresolved ILT interface and all prior issue records are retained, and the issue-register copies agree.

Evidence: anatomy/source/arterial-review-v0.9.113. Replay tools: tools/arterial-review-v0.9.113. Report: docs/validation/arterial-review-v0.9.113.json.
