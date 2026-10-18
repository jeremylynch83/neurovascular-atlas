# Tentorial native wall gaps, v0.9.92

This release closes four small native wall gaps in the bilateral tentorial marginal artery labels. Seven triangles are added. Every existing vertex coordinate, normal and triangle is retained exactly.

The left dorsal meningeal interface had a six-edge wall gap. Four triangles join its existing boundary, restoring the one missing parent coordinate. On the right, three triangular gaps are filled. Two restore the dorsal meningeal junction and the adjoining three-label corner; the third restores another meningohypophyseal interface coordinate. Patch spans are 0.117-0.178 mm. These dimensions are measurements of the illustrative mesh, not patient anatomy.

Both dorsal meningeal attachments now retain all recorded native coordinates: 16 on the left and 13 on the right. The right meningohypophyseal attachment increases from seven to nine matched coordinates; one remains missing. The left meningohypophyseal attachment is unchanged. Failed native-interface records in the 12-segment deferred group decrease from eight to six. Whole-network lumen closure is not established.

Only the two tentorial marginal meshes change. Their source faces and vertex attributes remain exact, including source duplicate-coordinate normal seams. Four appended vertices copy existing parent coordinates and normal integers. No additional coordinate or normal quantisation is used. All 597 other arterial meshes and the four other model files are unchanged. All 21 runtime source files, 1,250 named meshes, catalogue IDs and relationships are retained.

Every new disjoint triangle pair was screened against all 1,250 delivered named surfaces, including the unchanged parts of the edited meshes. No new crossing was found. The combined local native surfaces have no non-manifold or inconsistently oriented edge, and all 15 selected boundary edges acquire opposite partners. Signed-distance samples on the patches remain outside nearby represented bone and brain surfaces. These local checks preserve earlier unresolved source findings; they do not certify the wider anatomy.

The two affected DSA projection recipes and injection courses are refreshed. Their projections are closed and oriented, and both courses remain selectable. The other 595 arterial courses, graph, venous sites and authored course definitions remain unchanged.

Right ACA attachment and G05 pericallosal registration remain open. The remaining six deferred native-interface records concern bilateral meningohypophyseal attachments, the left occipital mastoid opening, and three left ILT posterior branch interfaces. Other bone/dural fit, receiving-network and earlier regional findings remain in ANATOMICAL_ISSUES.md.

Reproduction tools are in tools/tentorial-attachment-v0.9.92. Baseline and candidate buffers, source hashes and numerical evidence are in anatomy/source/tentorial-attachment-v0.9.92. The integrated report is docs/validation/tentorial-v0.9.92.json. These optional scientific tools add no application dependency.
