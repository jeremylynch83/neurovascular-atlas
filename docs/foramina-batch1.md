# Sphenoid foramina, batch 1, v0.9.134

This release addresses the bilateral rotundum, ovale and spinosum items from the v0.9.133 skull foramina audit, including their local vessel paths.

- Native rotundum and ovale apertures are retained. Their markers and course guides are fitted separately to the two sides.
- Two 2.4 mm round oblique spinosum passages are reconstructed in the greater sphenoid wings, posterolateral to ovale. They are distinct from the lateral source seam. The sphenoid remains a single closed manifold, with exactly two additional through passages. Other bone meshes and the v0.9.133 mandibular shading repair are retained exactly.
- Both rotundum arteries are redirected through the existing canals rather than clipping the canal walls. MMA approaches pass through the reconstructed spinosum lumens. The accessory meningeal routes remain through ovale, with local shared-junction adjustments.
- The displaced left ovale emissary vein is moved into the native ovale. The right emissary and nearby middle meningeal venous surfaces receive coupled clearance corrections. Artery and vein surfaces are separated. Axial cross-sections move rigidly. Existing caudal capped middle meningeal vein ends are lifted onto the endocranial side; no new drainage connection is inferred. These capped ends and wider drainage anatomy remain explicitly unaccepted in their course records.
- Shared vascular coordinates and branch collars move together. The before/after attachment comparison verifies all 67 previously coincident interfaces in the checked 94 related pairs, including parent/child and existing receiving interfaces. Pre-existing unjoined catalogue relationships are not certified as new physical junctions.
- DSA projection cap vertices, geometry-bound injection guides, vessel-course exports and source path contracts are refreshed. Existing structure IDs, hierarchy and potential-anastomosis semantics are retained.

## Checks

See `foramina-batch1-validation.json` for the regional triangle intersection tests and shared-interface results. Triangle collision tests found zero bone contacts in the tested passage windows and zero artery-vein contacts for the tested AMA/MMA against the ovale emissary and middle meningeal veins on each side. This is regional geometric evidence, not certification of the whole atlas. Spine, optic, ethmoidal, petrous/carotid, posterior skull-base, palatal and other remaining audit items belong to later batches.

Ordinary builds require no new dependencies. `tools/foramina` and `anatomy/source/foramina` retain the authoring field definitions; authoring analysis used NumPy, SciPy, VTK, trimesh and manifold3d. Arterial route changes use small velocity-field steps. Venous walls use continuous section maps with positive axial derivatives. Native facets are split exactly at every affine-section boundary, preventing folds from interpolation across long facets. Two short rotundum patches receive less than 0.081 mm of local smoothing. The pre-existing ovale source triangle contacts are logged separately. The only additional numerical contact has a penetration bound below 0.000003 mm. No additional material folding was found at a 0.001 mm check tolerance. Bone correction used a local manifold boolean and retained the existing oval/rotundum surfaces. No universal literature diameter was imposed on the native openings.

## Anatomical basis

- Tayebi Meybodi et al. Comprehensive microsurgical anatomy of the middle cranial fossa, Part I. Front Surg. 2023;10:1132774. https://doi.org/10.3389/fsurg.2023.1132774
- Dilenge D, Geraud G. Accessory meningeal artery. Acta Radiol Suppl. 1976;347:63-69. https://pubmed.ncbi.nlm.nih.gov/207149/
- Bhattarai et al. Morphometric analysis of foramen ovale, foramen spinosum and foramen rotundum using CT. Ann Med Surg. 2023;85:1731-1736. https://pubmed.ncbi.nlm.nih.gov/37228912/

Spinosum is a chosen conventional teaching configuration. Optional foraminal and arterial variants have not been made obligatory. Calibres and source depth remain illustrative and require anatomical review.


Final validation: production build passed; six injection sources selectable; 36 closed DSA split sections; 67 prior coincident interfaces retained. The incremental final DSA refresh compared all node positions, indices, course guides and surface entries, retained 603 unchanged arterial courses and rebuilt only the two smoothed rotundum courses.
