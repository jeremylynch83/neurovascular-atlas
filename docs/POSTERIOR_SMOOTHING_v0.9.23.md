# Posterior arterial smoothing in v0.9.23

A conservative smoothing pass covers the bilateral PCA P1 and P2/P3 segments, the basilar artery and bilateral vertebral V1–V4 segments. Immediate branch collars share the same joined surface field. The full cohort has 82 labelled surfaces; distal branch movement tapers away from the main trunks.

The method combines windowed-sinc surface smoothing with correction of uniform shaft contraction, a continuous physical displacement field, fixed external junctions and local face-quality guards. Movement is capped at 0.8 mm and additionally limited to 35% of the source vertex's unsigned distance to unchanged brain, skull and venous surfaces. Near-pons basilar patches receive additional protection. Actual maximum movement is 0.7471 mm.

Validation against v0.9.22 finds no new triangle contact pairs across the changed arteries versus all decoded arteries, veins, brain and skull surfaces. The 315 pairs present in both versions remain recorded. Every exact shared arterial coordinate remains joined, with zero maximum seam gap. All 1,198,945 positive-area source faces retain orientation and positive area; source zero-area facets remain part of the retained topology.

Across 12 paired material sections per main label, equivalent section diameter ratios range from 0.9144 to 1.1167, within the 0.85–1.15 review bounds. These are convex-hull section measurements, not true lumen measurements; they do not prove circular calibre at every ostium. Source contours and branch attachment geometry constrain how much smoothing is accepted.

The exporter retains all labels, original indices and vertex order and updates course/container hashes. The actual Three.js loader checks every circulation position and index against the checked candidate or source, and checks finite unit normals on changed surfaces. Brain, skull, venous and anastomotic GLBs retain their v0.9.22 bytes.

This is an anatomical review build. The pass softens contours and shading but does not remove every large branch-junction bulge or establish correct vascular courses. Open tissue surfaces cannot establish solid containment. Browser GPU appearance has not been tested in this execution environment.

See the JSON evidence in `docs/validation/posterior-smoothing-*-v0.9.23.json`, the full-surface matched view in `docs/validation/posterior-smoothing-before-after-v0.9.23.png`, and the reproduction toolkit in `tools/posterior-smoothing-v0923/`.
