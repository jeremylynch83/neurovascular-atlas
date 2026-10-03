# Labial and submental courses, v0.8.11

Apply the supplied facial-branch diagram and correction on both sides:

- Inferior labial: lower the main course into the lower-lip band below the
  visible lower dental crowns, approximately 9.5 mm lower distally.
- Superior labial: lower the main course by approximately 4 mm into the
  upper-lip band just above the visible upper crowns.
- Submental: raise the hanging loop, by up to approximately 11 mm, to follow
  the retained mandibular inferior surface. The reference axis is targeted
  about 2.2 mm below that surface more anteriorly, following a smooth
  transition from the retained root departure.

“Maxilla” in the initial request is interpreted as “mandible”, following
the supplied diagram and note-derived submental description. The reference
images are `image(20261003-224612).png` and `image(20261003-224632).png`.
Distances describe this reference model and are not patient measurements.

The bones and teeth remain unchanged. Crown/lip relationships are visual
reference positions; complete teeth include roots within the jaws.
Lip and mylohyoid soft-tissue planes are not registered. The inferior
mandibular surface is queried directly from the retained bone mesh.

## Surface handling

Preserve all six existing origins, shared facial seam vertices and root
collars. Smoothly transport each branch surface onto its corrected dense
path, retaining indices, triangles, colours and the illustrative radius profiles.
Recompute normals only on moved vertices; retained collars keep their
original position and normal bytes. The facial arteries are untouched.

Carry the two labial–septal routes and both cross-midline labial connections
with their corrected endpoints. Preserve their semantic relationships and
potential-connection display. Other vascular geometry, skull and dental
meshes, descriptions, selectable sections and GUI remain unchanged.

## One-off authoring review

Compare the actual surfaces before and after in front and oblique views
with the same retained teeth and jaw. Check that the six root seams are
still shared with the facial arteries, that moved surfaces remain finite
and non-degenerate, and that all unaffected attributes and indices remain
byte-identical. Check the main paths against the retained bone/dental
surfaces and check transported connection endpoints.

Use the actual Three.js loader and raycaster to exercise all corrected
arteries and existing selectable ICA, vertebral and ACA sections, together
with whole-artery focus, highlighting and hiding. Interaction checks use
fixtures, not a browser/GPU benchmark. Run local-root and GitHub Pages
subpath production builds. These are authoring checks, not a new runtime
anatomical validation step.
