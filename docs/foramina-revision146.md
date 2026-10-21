# Optic canal correction, v0.9.146

The previous narrow-section test did not validate the full canal. Revision145 had short superior walls and longer inferior walls. This revision reshapes the existing local lesser-wing surface to restore the expected wall-length relationship. Smooth axial deformation is blended into the surrounding bone, with modest variation of the oval bore along its axis. No independent sleeve, projecting ring or separate tube is added.

The local upper sphenoid envelope is intentionally reshaped. The older subtraction-only source-envelope requirement does not apply to this corrected patch. Large unrelated parts of the native bone are retained, and all other craniofacial meshes are preserved exactly as decoded. The short proximal ophthalmic arterial segments are fitted inferomedially into the canal entrances with a shared smooth map; nearby posterior orbitofrontal veins are lifted slightly above the roof. The map also moves any adjacent vertices at shared junctions. No subtractive vessel impressions are left in the bony mouths. Injection guides and projection-cap coordinates follow the same arterial map.

Final whole-canal measurements, local surface topology, self-contact checks, structure contact comparisons and preservation checks are recorded in revision146-optic-validation.json and revision146-geometry-validation.json. Wall lengths are model-space surface tracks, rather than clinical CT measurements. Rims are non-planar and their reported dimensions are approximate.

The optic nerves are not segmented, so this revision does not certify an optic-nerve-to-artery relationship. Existing source contacts elsewhere in the atlas are retained and compared against the baseline rather than described as absent. This release does not claim whole-skull anatomical acceptance.

Authoring sequence against revision145: revise146-optic.py, smooth146-normals.py, veins146.py, arteries146.py, followed by catalogue/surface hash binding and incremental DSA rebuild. Runtime builds use the delivered GLBs and require no additional scientific dependencies.

Anatomical references:
- Sthapak et al. Optic canal: a CT-based morphometric study. 2023. https://doi.org/10.1186/s41984-023-00220-1
- Radunovic et al. Morphometric characteristics of the optic canal and the optic nerve. 2019. https://pubmed.ncbi.nlm.nih.gov/30106467/
- Adanir et al. Evaluation of the cranial aperture of the optic canal. 2022. https://pubmed.ncbi.nlm.nih.gov/35175983/
