# Native arterial wall review, v0.9.113

This review installs no geometry. See docs/ARTERIAL_REVIEW_BATCH21_v0.9.113.md for results and limitations.

Run check_deferred.py [APP] to check the five source hashes. Exit 0 means the recorded exclusions can be reused within their exact search scopes. Exit 2 means baseline bytes changed or are missing and the shortcut is invalid. A different algorithm or region is not excluded by this registry.

To reproduce the searches, use a fresh absolute WORK path and CACHE path, with the v0.9.112 geometry also retained unchanged in v0.9.113. Run the following scripts from the app root in order, each with WORK CACHE arguments:

1. inspect-gap.py
2. gap-trials.py
3. local-retriangulation.py
4. remaining-gap-trials.py
5. remaining-gap-gates.py

common.py refuses a different source asset baseline before loading face IDs. Reports are written to WORK only. No script installs or exports a GLB. All original gap and receiving-wall coordinates remain fixed during these searches. Source wall overlap, degenerate faces, self-crossing or embedded rim points exclude a candidate. The bounded local retriangulation search has a 20,000-state ceiling; this baseline exhausts its discovered component at 4,620 states. Its result does not prove that larger reconstruction domains or other algorithms cannot succeed.

The registry and complete reports are in anatomy/source/arterial-review-v0.9.113. Their recorded exclusions are intentionally scoped and source-dependent.
