# npm dependency maintenance, v0.9.30

Continues from the saved v0.9.29 anatomical correction build. This release updates the npm-managed build dependencies, rather than the system npm executable.

| Dependency | Previous version | Updated version |
| --- | --- | --- |
| Vite | 8.3.1 | 8.3.3 |
| Vite React plugin | 6.1.1 | 6.1.2 |

The package requirements and lockfile are updated together. The app release is 0.9.30 so the existing installer can recognise it as newer. The outdated README.txt has been corrected to describe the current anatomical content and remaining work.

## Verification

- A fresh `npm ci --no-audit --no-fund` succeeds using the updated lockfile.
- `npm run build` passes catalogue, course and brain validation, TypeScript compilation, Vite production bundling and gzip asset preparation.
- The existing eight course-segment regression tests pass.
- All five production model files are byte-identical to v0.9.29, verified by comparison with the baseline ZIP.
- The source catalogue is identical except for its top-level release number. It retains 1,648 structures, 1,395 relationships and 1,232 named mesh parts.

Build verification ran with Node 24.19.0 and npm 11.9.0. Docker and GitHub Pages remain configured for Node 22; their deployment builds were not run here. Both updated dependencies declare support for Node 22.12.0 and later.

Vite still reports a bundle-size warning for the main JavaScript chunk. This does not fail the build. No bundle-splitting or rendering changes are included in this maintenance release.

## Anatomical work still open

Seven audited posterior artery-vein crossing pairs, straight-sinus alignment, fine skull-base canal calibration and pericallosal fitting remain open. See [the v0.9.29 correction register](ANATOMICAL_CORRECTIONS_v0.9.29.md) for the exact pairs and supporting evidence. No new anatomical correction is claimed by this release.

## Installation

Place `inr-anatomy-atlas-v0.9.30.zip` beside the existing `inr-anatomy.sh` and run `./inr-anatomy.sh update` using the established workflow.
