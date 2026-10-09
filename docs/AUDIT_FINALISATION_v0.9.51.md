# Audit finalisation v0.9.51

The accepted v0.9.50 geometry is retained byte for byte. This is a validation and packaging release, with no further anatomical geometry changes. The infraorbital repair visible as pending in the screenshot was completed in v0.9.50 and is included here.

## Completed release work

- Independently checked the ten delivered alveolar, infraorbital, retinal, selected CPA auditory and regional vertebral venous additions against the actual composite atlas.
- Confirmed closed manifold edges, positive oriented volumes, one connected component per delivered addition, no degenerate faces and no non-adjacent self-intersections.
- Found no unintended arterial, brain or neighbouring venous contacts among these additions. Receiving venous attachments are intentional. Bone overlaps along unsegmented canals remain unresolved containment findings.
- Checked all five GLBs through the actual Three.js GLTFLoader and MeshoptDecoder. Every model byte and every loaded position and face index matches v0.9.50.
- Passed anatomy/course validation, TypeScript, the production build and precompression.

## Paired anterior middle meningeal veins

The original trial and subsequent alternative full companion reconstructions remain excluded. The alternatives failed neighbouring anatomy checks; none was accepted or exported into this release.

A separate check confirmed that the retained MMA trunk guide itself crosses temporal and adjacent brain reference surfaces on both sides. This explains part of the difficulty with fitting veins to the same guide. It is a geometric conflict in the atlas, not a claim about normal anatomy. A coordinated arterial/brain-reference and bony-corridor reconstruction is required; simply inserting paired tubes cannot close this finding.

Selected course anatomy is supported by San Millán Ruíz et al., AJNR 2004, PMID 14729539 (https://pubmed.ncbi.nlm.nih.gov/14729539/), and the paired dural-channel study, PMID 16944530 (https://pubmed.ncbi.nlm.nih.gov/16944530/). These sources do not validate the local atlas coordinates.

## Still open

The whole anatomical audit remains open. This package does not certify fine hypoglossal, acoustic, alveolar or infraorbital canal containment, independent supraorbital/ethmoidal/stylomastoid/Vidian guides, cervical bone fit, orbital nerves and globe anatomy, mastoid/posterior condylar routes, or medial petrosal free-outlet transitions. Existing atlas-wide surface issues outside the accepted corrections also remain open.

Separate new vessel surfaces overlap receiving venous volumes. Closed individual surfaces do not establish a continuous watertight atlas-wide lumen.

## Evidence and reproduction

See `docs/validation/final-release-v0.9.51.json`, the final contact, self-intersection, component and loader reports, `build-v0.9.51.json`, and `audit-register-v0.9.51.json`.

With the declared npm dependencies installed, decode `public/anatomy/models` using `tools/decode-posterior-baseline.mjs` into a fresh `WORK/decoded`. Run `prepare.py`, `validate.py`, `self_check.py` and `check_components.py` under `tools/final-audit-v0951/`, each with `WORK` as its argument. Run `npm run build`, then `node tools/check-final-release.mjs WORK/decoded WORK/loader.json`. The verification buffers and rejected candidate models are excluded from the install ZIP.
