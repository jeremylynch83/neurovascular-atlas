# Pontine vessel quality, v0.9.48

Four connected veins have been rebuilt: median anterior pontine, transverse pontine left and right, and right prepontine bridging vein. The v0.9.47 model contained folded union facets, flattened walls and extra internal surfaces at their common junction. Adding triangle density did not resolve those defects.

The replacement uses smooth native centreline paths and bounded illustrative radius profiles to form circular tubes. Their branch connections merge into a single implicit solid, sampled at approximately 0.12 mm and smoothed mildly. The final exterior is partitioned into four disjoint patches for selection. Every exterior triangle appears once, and the shared label boundaries use identical positions and normals. There are no caps inside the four-vein junction.

## Scope of watertightness

The combined four-vein exterior wall is one connected closed manifold. The baseline combined meshes had 10,492 boundary edges, 1,160 non-manifold edges and 670 duplicate triangles; the rebuilt wall has zero of each. All four selectable patches are individually connected. It has zero boundary edges, zero non-manifold edges, consistent face orientation, no degenerate or duplicate triangles and no detected non-adjacent triangle intersections. Each selectable label is a patch of that common wall, with intentional open boundaries at label interfaces. It is not a separately capped printable object.

The eight connections into the retained neighbouring veins are verified as continuous solid-volume attachments at their original locations. Those neighbouring meshes remain unchanged and can overlap the rebuilt network at the endpoint collars. This release does not claim a manifold surface for the entire atlas or for those retained external collar overlaps.

## Placement and clearance

Local centreline adjustments of at most 0.96 mm clear the fixed pial and arterial surfaces. A small local radius allowance reconnects the right lateral tributary. The transverse midline crossing remains posterior to the basilar artery, between artery and pons; its sampled minimum posterior clearance is about 0.51 mm. No unexpected surface contacts with arteries, brain, skull or other veins are detected. Expected endpoint collar contacts are separately recorded.

All arteries, brain, skull and anastomosis assets retain their exact v0.9.47 hashes. The brain recess from v0.9.47 is retained. Other venous labels retain exact positions and indices. The interface, halo, selection and prior labial/ICA corrections are preserved.

The vein calibre is illustrative. The previous geodesic wall radius estimator was inflated around folded and bifurcating facets, so the new tube radii are smoothed and bounded, rather than reproducing those distorted outer walls. The source and resulting radius quantiles, local path changes and authoring grid are included in the evidence. Anatomical review status remains explicit.

## Verification and comparisons

[Machine-readable evidence](validation/brainstem-quality-v0.9.48.json) includes strict topology checks across the combined wall, exhaustive non-adjacent triangle checks, contacts, endpoint attachments, crossing depth, exact patch coverage, actual Three.js/MeshoptDecoder loading and production build verification. All 217 venous labels remain available. The rebuilt region uses approximately 86% fewer triangles.

[Anterior comparison](../review-renders/Brainstem_quality_anterior_v0.9.48.png) and [oblique comparison](../review-renders/Brainstem_quality_oblique_v0.9.48.png) use matched full-mesh views: v0.9.47 on the left, v0.9.48 on the right. Arteries are red, veins blue and pons grey.

## Reproduction

Decode the exact v0.9.47 assets with tools/decode-posterior-baseline.mjs. tools/brainstem-quality-v0948/measure.py extracts native geodesic paths, rebuild.py constructs the network, clearance.py adjusts local paths, validate.py checks the full combined exterior and neighbouring anatomy, attachments.py checks retained external connections and depth.py verifies the transverse crossing. Run export.mjs with candidate and exact baseline directories, catalogue.py, build-anatomy.sh, check_export.mjs and npm run build. evidence.py checks patch coverage and writes the evidence file. All Python authoring commands take the working directory as their first argument.
