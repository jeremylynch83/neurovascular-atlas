# Petrous carotid and tympanic passages, batch 2, v0.9.135

This release reconstructs the bilateral carotid canals and fits the local tympanic arterial routes. It retains the batch 1 sphenoid repairs and the mandibular shading repair.

## Corrections

| Item | Correction |
|---|---|
| Carotid canal entrances | Removed the obstructing bone along the ascending ICA limbs. The generic carotid markers now identify the inferior apertures rather than the posterior genu. Entrance stations were fitted to the original inferior temporal surfaces. |
| Posterior genu and horizontal canal | Reconstructed continuous curved passages along the delivered ICA envelope. The main ICA course is preserved, with the original segment surfaces and shared seams unchanged. |
| ICA injection guides | Corrected both cervical-to-petrous transitions using the actual shared mesh interface. The earlier cervical guides wandered into unsafe terminal patches. |
| Petrous apex and lacerum relation | Fitted the superior carotid clearance and corrected the internal-opening guide. The ICA continues above the lacerum junction. No inferior-to-superior carotid bore was made through lacerum. |
| Caroticotympanic arteries | Replaced both defective native tubes. The old meshes had self-contacts and could not be selected as DSA injection targets. The new short, closed tubes run from within the posterior petrous ICA genu towards the middle-ear region. Their proximal ends overlap the parent lumen; their distal ends meet the existing potential tympanic connection geometry. |
| Caroticotympanic passages | Reconstructed small passages aligned with the new arterial courses. The chosen artery radius is 0.18 mm and the clearance-channel radius is 0.60 mm. These are teaching-model choices. |
| Inferior tympanic route | Fitted the connected arterial course and reconstructed its small passage through the inferior petrous region. The entrance marker is fitted to the original bone surface on the posterior side of the carotid entrance. |
| Other connected tympanic vessels | Applied one smooth spatial field to the anterior and superior tympanic branches, distal petrosal branches and their existing connection geometry. Reconstructed the local small arterial passages needed for clearance. The complete petrotympanic fissure outline remains partial. |

The carotid clearance radius is 3.20 mm, chosen to accommodate this atlas's delivered ICA surface and its broad segment interface. It is not a population measurement or a prescribed normal canal diameter. Small clearance channels use nominal radii of 0.45–0.60 mm, with short local flares of about 0.9 mm to clear the delivered branch collars. Native temporal surface openings are retained; the temporal meshes are not represented as entirely watertight bones. Temporary closures used for boolean operations were removed afterwards. Two negligible generated four-face fragments were discarded from the left temporal result.

## Geometry and DSA checks

See `foramina-batch2-validation.json` and `foramina-batch2-dsa-validation.json` for the final results. Checks cover source hashes, unchanged bones, regional vessel self-intersections, bone contacts within the stated passage windows, prior coincident interfaces, passage centrelines, injection selection, projection closure and split-surface closure. Batch 1 passage and DSA checks are repeated as a regression check.

The branch field uses smooth weighted velocity interpolation, 96 integration steps and a protected main ICA envelope. Long source facets and their DSA caps are subdivided together before fitting. IDs, hierarchy, original shared branch coordinates and potential-anastomosis semantics are retained. The caroticotympanic meshes are new reconstructions, with new geometry-bound injection guides. Their parent and receiving contacts are overlaps, not newly certified welded anatomical ostia. Normal app builds reuse the delivered meshes and add no dependencies.

## Remaining register

| Issue | Follow-up |
|---|---|
| Complete vidian canal, ECA continuation and their vessel/bone fit | Batch 5. The existing ICA contribution is retained. This release does not certify the full vidian route. |
| Internal acoustic, facial, jugular, hypoglossal and other posterior skull-base canals | Batch 3. Small arterial clearance channels in this release do not establish the full neural or labyrinthine canals. |
| B2-AT-01: proximal right anterior tympanic artery crosses the greater sphenoid wing below z=43 mm | Pre-existing approach defect, outside the corrected fissure window. Retained for batch 3, with the complete petrotympanic approach. It is not counted as anatomically cleared. |
| Full petrotympanic fissure outline | Still partial. Only its local arterial clearance is addressed here. |
| Lacerum fibrocartilage | Not separately segmented. The landmark remains partial; the artery-over-junction relationship is retained. |
| ICA colour stations | Historical stations from the earlier annotated classification are retained. The geometric canal entrance is now marked separately. A colour boundary is not proof of the anatomical canal entrance or a segmented ligament. |
| Mandibular condyles near the lower ICA | Mandibular surfaces are retained. Jaw-related contacts remain for the mandibular batch, separate from the corrected temporal/sphenoid passage windows. |

Coordinates in the reports are model RAS millimetres.

Six planned batches remain. This is a reference-guided teaching reconstruction with local geometric verification, not independent patient segmentation or anatomical certification.

## Anatomical references

- Tayebi Meybodi et al. Comprehensive microsurgical anatomy of the middle cranial fossa: Part II, neurovascular anatomy. Front Surg. 2023;10:1132784. https://doi.org/10.3389/fsurg.2023.1132784
- The enigmatic foramen lacerum. Primary anatomical investigation. https://pubmed.ncbi.nlm.nih.gov/9932893/
- High-resolution CT of the jugular foramen: anatomy and vascular variants and anomalies. Radiology. 1984. https://pubmed.ncbi.nlm.nih.gov/6320256/
- Kassam et al. Expanded endonasal approach: vidian canal as a landmark to the petrous internal carotid artery. J Neurosurg. 2008. https://pubmed.ncbi.nlm.nih.gov/18173330/

The optional `python3 tools/foramina/validate-petrous-geometry.py` check reads the delivered GLBs directly and uses NumPy, VTK and python-fcl. `node tools/foramina/validate-batch2.mjs` checks DSA and passage guides with the normal Node dependencies. The anterior tympanic clearance window starts at z=43 mm; the proximal B2-AT-01 defect is explicitly excluded and retained in the register.

Final checks: production build passed; 14 fully safe injection routes; 72 closed DSA split sections; six named passage guides clear; 14 regional bone-contact tests and 22 regional self-contact tests clear. All 14 previously coincident interfaces in 28 checked pairs are retained. Four new caroticotympanic parent/receiving overlaps are verified. The other 57 bone/teeth/hyoid meshes and all original ICA segment arrays are unchanged. B2-AT-01 remains explicitly deferred.
