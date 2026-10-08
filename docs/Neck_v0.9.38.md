# Upper cervical vessels, v0.9.38

The prominent folded upper right IJV in the supplied screenshot is replaced with a smooth tube. The left upper IJV is straightened consistently. The short rebuilt interval is z = −30 to +22 mm in atlas RAS coordinates. Native mesh above and below the interval is retained, including the sigmoid, inferior petrosal, anterior condylar and facial interfaces. Endpoint calibre is retained and interpolated along the rebuilt interval. The smooth course has a small posterior bow to remain clear of the carotid origin.

The proximal occipital artery crosses over the lateral surface of the IJV. A smooth local lateral displacement is 2.5 mm on the right and 0.5 mm on the left; origin and remote scalp course are preserved. Nearby labelled occipital branch and potential-connection surfaces receive the same field to retain their attachments. Carotid surfaces, skull, brain and the cavernous sinus repair are unchanged. The author attribution now reads “Jeremy Lynch, Sean McIlhone”.

## Validation

- Zero detected OA–IJV surface intersections, and zero IJV–cervical ICA/ECA contacts on both sides.
- Minimum sampled OA–IJV surface separation in the crossing: 0.377 mm right and 0.472 mm left. These are sampled values, not an exact continuous minimum.
- Zero detected bone contacts for these vessels within the checked cervical region.
- Zero non-adjacent self-intersections in either rebuilt IJV.
- All native shared vertices with the four checked venous neighbours retained. Boundary-edge totals remain 188 right and 199 left; these are the labelled interfaces, not newly opened defects.
- Three.js GLTFLoader and Meshopt decoding verify exact checked positions and indices, unit normals, and unchanged geometry for all other labels in the three exported assets.
- Production build and anatomy catalogue validation pass.

`review-renders/IJV_occipital_comparison.png` is a depth-buffer comparison of the retained baseline and the revised checked triangles, whose positions and indices match the delivered compressed assets. It uses the same camera and scale in both panels. It is an offline render, not a live app screenshot. The model remains a teaching reconstruction with illustrative calibre.

## Reproduction

Tools are under `tools/neck-v0938`. Populate `baseline` with the three named GLBs from v0.9.37 and decode that release into `decoded` with `tools/decode-posterior-baseline.mjs`. Run `repair.py`, `selfcheck.py`, export with `export.mjs`, update catalogue/course hashes, build, and check with `check_export.mjs`. Native baseline binaries and transient buffers are excluded from the archive. Validation reports are in `anatomy/source/neck-v0938`.

## Anatomical source

The usual superficial occipital artery crossing is described in the original anatomical imaging study [Aberrant courses of the occipital artery](https://pmc.ncbi.nlm.nih.gov/articles/PMC12043729/). The implementation follows the user’s requested usual relationship, without modelling the reported deep variants.
