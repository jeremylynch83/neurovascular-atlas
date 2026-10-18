# Intersection classification audit, v0.9.101

Run from the app root with absolute output/cache paths:

`python3 tools/intersection-v0.9.101/audit.py WORK CACHE`

The audit reads the unchanged right A5 source geometry and the historical checker fixture in `anatomy/source/intersection-v0.9.101/previous-geometry.py`. It proves the reported face pair meets only at one shared vertex using independent exact plane-side determinants, compares old/new/exact predicates, and checks all 323 nearby candidate pairs against exact arithmetic. It writes predicate-audit.json only and never modifies a model. NumPy and VTK are authoring dependencies through the existing scene infrastructure.

The source fixture preserves the former checker for reproducibility; it is not used by current authoring tools. Current near-parallel checks use exact binary-coordinate rational signs, intervals and coplanar clipping, while ordinary pairs retain the fast numerical path. Default tolerance is unchanged. Tests retain true shallow-crossing rejection, shared-edge handling and arbitrarily thin positive coplanar overlap detection.

This clears only the single recorded right A5 false-positive flag. It does not certify the whole vessel, the pericallosal registration or full receiving lumens. Model assets and DSA flow/surface recipes remain byte exact to v0.9.100.
