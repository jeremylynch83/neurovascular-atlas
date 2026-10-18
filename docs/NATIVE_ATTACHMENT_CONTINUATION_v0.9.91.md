# Native attachment continuation, v0.9.91

This release repairs the left posterior cavernous MMA opening into the existing cavernous MMA parent. It is a local geometry correction. Wider anatomical acceptance remains false.

## Accepted geometry

The original native rim centres were separated by 3.929 mm. The parent outlet is lifted along its local axis by 0.15 mm with a 2 mm harmonic support and a constrained bone-depth refinement. Its two other native openings remain exact. The posterior branch proximal to Z=54 mm is reconstructed with an oblique cubic Hermite route and parallel-transported cross-sections, blending into the exact endpoint plane. Original distal geometry and the 148-coordinate distal native rim remain exact. The route clears the ovale emissary vein.

An exterior Boolean union removes internal overlapping walls at the new opening. It has 181 unique shared native boundary coordinates and 181 oppositely paired boundary edges. Both individual meshes and their combined native surface have zero self-intersections; no non-manifold edge remains. Temporary closure pieces exposed on the local union exterior become junction-wall triangles, while remote closure caps are discarded. Before Float32 cleanup, 49 such exterior pieces are retained. The tiny weld moves points by at most 0.000004265 mm. It does not merge distinct source coordinates.

The parent retains its 107- and 103-vertex remote rims, including the source duplicate seam. Every original coordinate shared with another label remains exact. Source per-corner normals on retained triangles are preserved, including duplicate-coordinate normal seams. The new interface has identical encoded normals on both labels. The real app loader verifies exact candidate positions and indices, 597 unchanged arterial meshes, and four other byte-exact assets. The app runtime source is unchanged.

## Scene and bone checks

Full-scene contact screening introduces no newly contacted object. The source incidental contact with Accessory meningeal left is removed; the declared distal ILT anastomosis is retained. Both final surfaces stay within the screened parent-plus-connector union to 0.000001568 mm at changed-face vertices, centres and edge midpoints.

The parent source already intersects the sphenoid. Signed-distance sampling of the changed parent region has no newly inside samples and zero increase in penetration depth. Maximum sampled depth remains 0.470843 mm and the adjusted port has minimum sampled clearance 0.031910 mm. Source bone contacts are not resolved by this local repair. Bone contact facet counts change from 217 to 223; these counts and other counts altered by retriangulation do not measure added penetration. Independent compartment support and wider bone/dural fit remain open.

## Data and scope

Only the two selected native meshes, projection recipes and injection courses are refreshed. Both remain selectable; the other 595 arterial courses, authored course guides, declared graph, generator and venous timing sites are unchanged. All earlier accepted corrections are retained.

Failed native-interface records in the deferred 12-segment cohort decrease from nine to eight. The remaining records concern bilateral tentorial marginal attachments to dorsal meningeal and meningohypophyseal branches, the left occipital mastoid parent opening, and three left ILT posterior-branch interfaces. The cohort remains under wider review. Right ACA native attachment and pericallosal/cortical registration (G05/G06), receiving-lumen continuity, and earlier G01/G03/G04/G07/G08 findings remain open.

## Validation and reproducibility

See validation/cavernous-v0.9.91.json and the included targeted before/after image. Optional scientific tools are in tools/cavernous-attachment-v0.9.91; baseline and candidate buffers, screened inputs, recipes and machine-readable provenance are in anatomy/source/cavernous-attachment-v0.9.91. Excluded displacement, collar and broad-route trials were not installed. Ordinary app use adds no dependency.

The full source ZIP includes all source files from v0.9.90 plus the new authoring tools, provenance and documentation. It excludes local dependencies and compiled output.

Release checks pass: production build; all 828 closed and oriented DSA proxies (8,968,916 triangles); 578 selectable courses; 2,350 closed injection sections; bilateral companion-channel timing and selective drainage; and 14 course unit tests. All 21 runtime source files are byte-exact to v0.9.90. All 1,250 named meshes and 1,666 catalogue structures are retained.
