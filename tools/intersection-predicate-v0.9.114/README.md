# Intersection predicate repair, v0.9.114

The corrected authoring predicate is tools/repair/geometry.py. Model geometry and application runtime source are unchanged. See docs/INTERSECTION_PREDICATE_BATCH22_v0.9.114.md for scope and evidence.

- verify-fixtures.py [--output PATH] checks all 34 immutable production-coordinate cases. Expected results include 12 exact-negative reports and 22 genuine positive cases.
- scan-petrosal.py WORK CACHE scans the complete bilateral inferior petrosal labels using the current predicate. Use absolute, fresh WORK and CACHE paths. It writes WORK/petrosal-self-scan.json and never edits or exports a model.
- ../arterial-review-v0.9.113/check_deferred.py [APP] checks the new default registry. Source geometry and validation-code hashes must both match. Legacy geometry-only registries and implementation mismatches return exit code 2 and require review. The current matching registry returns 0.

Run the repair suite with python3 -m unittest discover -s tests/repair -v. The clearance suite remains tools/aca-tail-v0.9.112/test_clearance.py. Source fixtures, before/after predicate snapshots, full petrosal scans, corrected SCA recheck and cache-invalidation receipts are retained in anatomy/source/intersection-predicate-v0.9.114.

This code corrects validation reports. It does not repair anatomy, establish lumen continuity or certify physiological geometry. Historical fixed-face searches require the recorded implementation as well as source asset bytes.
