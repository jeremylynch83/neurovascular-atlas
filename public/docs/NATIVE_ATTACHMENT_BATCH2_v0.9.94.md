# Batch 2: remaining native attachments

All six recorded failures were assessed. Three small wall gaps at the bilateral tentorial/MHT attachments were repaired. The two corresponding failure records are cleared, leaving four records for collar or coupled regional reconstruction in batch 3. All 12 original segments remain under wider anatomical review.

## Accepted correction

The cached pipeline found two left triangular gaps and one right triangular gap within the explicitly selected compound native boundary networks. The reviewed configuration permits a larger boundary component while retaining the existing 0.25 mm per-gap span, area and planarity gates. The large loops and single-label ports remain open and are excluded from patching.

Three triangles and three existing parent coordinates are appended. Every source vertex position, source normal integer and source triangle is retained exactly. The left MHT interface increases from 11 to all 13 recorded native coordinates; the right increases from nine to all ten. The combined left network loses six unmatched boundary edges and the right loses three, with no new non-manifold or inconsistently oriented edge.

The pipeline stages and validates these patches in 1.664 seconds in this run, using the existing authoring cache. It checks all affected triangles against the scene, including adjacent triangles and coplanar overlap, and applies the existing local tissue/bone clearance gates. No new crossing is found. This is a local geometry gate, not whole-region anatomical acceptance. The earlier v0.9.92 dorsal meningeal patches and all other source surfaces are retained.

The existing lossless native exporter is reused. The actual app loader verifies 599 arterial meshes, including 597 unchanged arterial meshes, all original positions/normals/faces on the two edited labels, and four byte-exact other model assets. Appended coordinates and normals copy their MHT sources exactly. All 21 runtime source files, 1,250 named meshes, 1,666 catalogue IDs and anatomical relationships are retained.

## Excluded local operations

| Record | Finding and next work |
|---|---|
| Left occipital mastoid to occipital | The child has only a distal open boundary. Its proximal surface is closed, so it has no compatible open rim for a bounded snap. Reopen the proximal cap and reconstruct a native collar. The selected parent port centre is 0.474 mm from the child surface; the distant distal rim is not the physical gap. |
| Left ILT posterior to anterior branch | The root rims do not match. Rebuild this attachment together with the adjoining trunk and posterior collector. |
| Left ILT posterior to posteromedial ramus | The parent port is separated from the current child surface. The closest parent-rim vertex to child-vertex distances are 1.63-1.85 mm; a simple rim displacement is excluded. Review the regional route and attachment together. |
| Left ILT posterior to inferolateral trunk | The shared collector requires reconstruction alongside its anterior-branch attachment. The four-label source network has one non-manifold edge and one inconsistently oriented edge. |

All four explicit bounded seam probes return `registration-or-rim-reconstruction-required` and are recorded as rejected trials. Their geometry was not installed. Their disposition is reconstruction in batch 3, rather than repeated increases to the local snap bound. The full measurements, native boundary loops and source hashes are in the validation report and included provenance.

## Integration and reproduction

Only two DSA projection recipes and injection courses are refreshed. Both courses remain selectable; the other 595 arterial courses, graph, edge locations and venous sites are unchanged.

Run the reusable tool with `tools/repair/configs/batch2-tentorial.json` from the v0.9.93 baseline to reproduce the accepted candidate buffers. `batch2-bounded-seam-probes.json` reproduces the rejected bounded seam operations. Baseline/candidate buffers, the accepted pipeline report, proxy recipes, source hashes and rejected assessments are in `anatomy/source/native-batch2-v0.9.94`. The existing tools/tentorial-attachment-v0.9.92 exporter, loader verifier and projection refresh are reused with the included batch metadata. Do not apply the accepted patches again to the already repaired v0.9.94 geometry.

The production build, all 828 closed DSA proxy checks, 578 selectable course checks, 2,350 closed injection sections, bilateral meningeal drainage checks and all 16 repair regressions pass. The integrated evidence is docs/validation/native-batch2-v0.9.94.json. Right ACA/pericallosal registration, regional bone/dural fit and whole receiving lumens remain open.
