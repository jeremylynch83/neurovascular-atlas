# v0.9.160: proximal IMA and distal ECA wall correction

The native proximal maxillary wall had irregular, flattened sections and local
triangle overlaps. The distal ECA/IMA/ST attachment also had an elongated,
creased collar. The defect was in the source geometry; v0.9.159 packaging had
preserved that geometry byte for byte.

The proximal IMA wall is reconstructed on both sides using a reviewed native
course and an illustrative 1.05 mm tube radius. The 17 original boundary loops
are retained. Seven proximal side-port loops are rebuilt; the wall is then fitted
back to the original small-branch rings. All small branches keep their original
positions, normals and triangles. The distal IMA geometry beyond the oblique
section station -47.6 is retained. That station uses s = -0.6|x| + 0.8y in RAS mm.
Final local wall fairing fixes every port vertex and every retained distal vertex.

The adjoining ECA/ST collar is adjusted and its shared coordinates reconciled.
Only six main arterial nodes change: the ECA, IMA and ST on each side. The other
601 main nodes, including ICA/ophthalmic and V4/PICA corrections, retain their
original decoded geometry. No independent connection mesh, bone, vein or brain
asset changes. Branch graph, identifiers, presets and viewer behaviour are retained.

Validation records include the saved-model interface audit, lossless loading-pack
checks, catalogue checks, DSA checks, build/gzip checks and exact source restoration.
The final shared-interface gap is 0.0 mm. The regional skull collision check finds
no intersections in the corrected walls. All 24 affected/restored DSA courses are
checked, with the two IMA courses rechecked after final wall fairing. Previously
selectable/full-safe status is retained.

This is a local educational wall reconstruction, not a measured patient lumen.
It is not a claim that the entire source network is free of triangle self-contact.
The right IMA has 154 material contacts versus 587 before, with maximum measured
depth 0.0664 mm versus 0.1102 mm. The left has 184 versus 590, with maximum depth
0.1199 mm versus 0.1129 mm. These include small residual seam/collar contacts and
retained distal source geometry. The reconstructed display wall remains open at
its branch ports; DSA uses separately closed projection surfaces.

The authoring helpers in tools/foramina are one-shot provenance tools requiring
NumPy, SciPy and VTK. They are not runtime/build dependencies and must not be run
on an already-corrected model. Ordinary builds reuse delivered geometry, restore
the large source byte for byte from packs/fragments, and retain the v0.9.159 GitHub
file-size handling. No model file over GitHub's limit is included in the source ZIP.
