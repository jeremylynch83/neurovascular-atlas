# Posterior-fossa fitting v0.9.20

This anatomical review build continues the recovered candidate 59. Candidate 60 reduces the anterior venous envelope smoothing weight from 20,000 to 2,000. Candidate 61 closes the right P1/basilar and left SCA/proximal perforator gaps with labelled Boolean joins.

Both PSAs arise from proximal PICAs and follow the dorsal medulla and the illustrative upper cervical cord. The former V3 origins are closed. The cord is constructed context, not an imported atlas structure. The recovered brainstem/cerebellar geometry is unchanged by the new vein and join work. Clival/basilar plexus is omitted from app rendering.

## Checks

- 109 local vessel/tissue rows checked; surface vessels have zero triangle intersections and zero wall vertices inside the checked closed tissue parts. Intentional perforator entry is reported separately.
- 21 rebuilt venous labels have zero triangle contacts and zero contained wall vertices in the closed local arterial solid.
- Sampled free tube sections preserve their minor diameter. Branch collars are excluded explicitly. The separate strict aspect-ratio check remains false because some curved sections widen; this is retained in the evidence.
- All 151 original seam pairs pass, including the two repaired arterial joins. PSA origin replacement is checked independently with shared PICA skin.
- Meshopt compression checks every buffer byte by an immediate decode. Review subsets match source positions and triangle indices exactly.
- Catalogue, brain-surface anchors, course hashes, TypeScript and production build checks pass. Both PSA selections, PICA links and illustrative cord load correctly in Chromium, with no unresolved model nodes, WebGL warnings or page errors.

## Surface apposition

The anterior medullary vein median sampled near-wall gap decreased from 0.69 to 0.32 mm. The anterior pontine vein decreased from 1.00 to 0.78 mm and the pontomesencephalic vein from 1.60 to 1.31 mm. These summaries include bridge and transition portions. They are improvements, not proof that every point contacts the pial surface. The near-wall measurements are in the checkpoint.

## Remaining work

The wider audit reports contacts of upper collecting veins, posterior arterial courses and cerebellar venous outlets with cerebral atlas structures outside the posterior-fossa test group. Existing baseline contacts are included. Different mesh densities make raw before/after contact counts unsuitable for judging deterioration; they identify regions for further review. These routes need anatomical reconciliation before this build can be described as fully fitted.

Open atlas surfaces permit triangle-intersection checks, not complete containment proof. The checks do not establish anatomical correctness by themselves. The local check passes must not be used as global anatomical acceptance.

Reports are in `docs/validation/posterior-*-v0.9.20.json`. Authoring geometry, fitted courses, reconstruction scripts and collision solids are preserved in the separate checkpoint.
