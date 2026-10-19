# Skull foramina correction, batch 3

Release 0.9.136. This is a reference-guided teaching reconstruction fitted to the delivered atlas, not a patient CT segmentation or independent anatomical certification. Five planned audit batches remain.

## Implemented

| Region | Bone and catalogue changes | Associated vessel fit |
| --- | --- | --- |
| Internal acoustic meatus | Bilateral oblique porus-to-fundus passages with a bounded lumen and a blind fundal boundary. Separate fundus markers added. The facial route leaves the anterosuperior fundal region. | Labyrinthine, common cochlear and anterior vestibular arterial surfaces and guides fitted together; small vascular clearances retained at the fundus. |
| Facial canal and stylomastoid foramen | Labyrinthine segment, first genu/geniculate region, tympanic segment, second genu and descending mastoid segment connected to a separate inferior exit. | Native stylomastoid artery retained within its fitted passage; connected regional networks retained. |
| Jugular foramen | Native temporal-occipital cleft and venous outlet preserved, with separate intracranial and extracranial markers. Local posterolateral venous and anteromedial neural/petrosal passage shapes are connected without an invented complete bony septum. The pre-existing jugular-fossa marker remains separate. | Jugular meningeal arterial course fitted. Sigmoid sinus and internal jugular vein arrays remain unchanged. A small posterior petrous clearance follows the ascending arterial branch. |
| Hypoglossal canal | Oblique canal through the occipital region above the condyle, separate from foramen magnum and jugular passage. External opening receives its own marker. | Hypoglossal arterial branch fitted. Both anterior condylar veins are sheared through their respective canal courses; their delivered cross-sectional profiles are retained. |
| Petrotympanic fissure | Slit-shaped passage at the posterior mandibular-fossa/tympanic junction, with small adjacent vascular collar clearances distinguished from the fissure itself. | Both anterior tympanic approaches are fitted around the sphenoid margin. B2-AT-01 is corrected by rerouting the artery, rather than drilling an extra sphenoid passage. |
| Regional potential anastomoses | Two pre-existing folded subarcuate-to-APA auditory links replaced by short smooth overlapping capsules. | The links remain optional teaching representations. Overlap is not a certified welded anatomical ostium or evidence of normal conspicuous patency. |

The principal IAC cutter radius is 2.55 mm, facial canal radius 1.15 mm and hypoglossal canal radius 1.90 mm. Jugular shapes combine larger and smaller curved sweeps around the existing outlet; the petrotympanic sweep has a narrow vertical dimension. Small vascular passages use illustrative clearance radii of 0.45-0.70 mm. These are authoring dimensions fitted to this model, not population measurements or diagnostic cut-offs. The new short potential links use a 0.15 mm illustrative radius.

## How neighbouring anatomy is preserved

Compact smooth fields transport the coupled arterial surfaces, closing surfaces, source paths and injection guides. Main ICA, vertebral, AICA, PICA, maxillary and principal meningeal surfaces are protected. For the anterior tympanic arteries, protection is re-evaluated at every step of a 96-step stationary velocity integration, with finer local facet subdivision and dense transported injection guides. This avoids the folded facets and short unsupported DSA ranges found in the first candidate.

The anterior condylar correction is a shear along the transverse coordinate: y and z offsets vary with x. Its local Jacobian determinant is one, so the transformation does not compress the retained transverse slices. Left and right routes have separate fitting stations.

Native temporal surface openings remain open. Temporary closures used for boolean operations are removed afterwards. Negligible detached surface fragments are discarded. The other 57 bone/teeth/hyoid meshes are retained exactly, including sphenoid and mandible. The hypoglossal passage is kept separate from the foramen magnum. The unchanged major arterial arrays are checked separately from the changed asset-file hashes.

## Verification and reproducibility

Normal builds reuse the delivered GLBs and introduce no extra runtime dependencies. Source recipes are in `anatomy/source/foramina/posterior-*.json`.

- `node tools/foramina/validate-batch3.mjs`: geometry-bound injection courses, complete safe ranges, closed DSA projections and split sections, and passage centreline clearance.
- `python3 tools/foramina/validate-posterior-geometry.py`: decoded delivered mesh contacts against temporal, occipital and sphenoid bone, passage lines and bone topology. Requires NumPy, Trimesh, VTK and python-fcl for optional authoring QA only.
- `python3 tools/foramina/validate-posterior-self.py`: non-adjacent surface contacts in the corrected region. Material contacts are assessed at a 0.001 mm penetration-bound threshold; the report also retains smaller contacts.
- Batch 1 and batch 2 DSA tests are repeated as regressions. Production build, source contracts, asset hashes and ZIP contents are checked.

Detailed results are in the accompanying `foramina-batch3-*-validation.json` reports. Cross-section wall rays and a fundal stop are tested separately, so an unblocked line through free space is not presented as proof of a canal. Scope is regional; passing these tests does not certify every vessel or microscopic opening in the atlas.

## Remaining register

- Cochlear and vestibular aqueducts, mastoid canaliculus, the bony labyrinth, individual VII/VIII neural pathways and fundal neural microforamina remain unmodelled or unresolved. Small vascular clearances do not establish these structures.
- Posterior condylar and mastoid emissary variants remain optional and unlocated. No obligatory bilateral variant holes are introduced.
- Existing clival, descending odontoid and the right MMA-to-tentorial potential-link surface contacts remain in the broader atlas. Connected collars are transported to retain their interfaces; the complete clival courses are outside this passage batch and are not certified by its regional clearance report. The baseline comparison is retained in the validation metadata.
- Original caroticotympanic parent/receiving overlaps retain their teaching-model semantics; welded ostia are not claimed.
- The full vidian route, orbital/anterior-fossa, pterygopalatine/palatal and mandibular audit work remains in later batches as assigned in the original audit.

## Anatomical references

1. Katsuta T, Rhoton AL Jr, Matsushima T. The jugular foramen: microsurgical anatomy and operative approaches. Neurosurgery. 1997;41:149-201. https://pubmed.ncbi.nlm.nih.gov/9218307/
2. Weiglein AH. Postnatal development of the facial canal. An investigation based on cadaver dissections and computed tomography. Surg Radiol Anat. 1996;18:115-123. https://pubmed.ncbi.nlm.nih.gov/8782317/
3. Skrzat et al. Anatomy of the fundus of the internal acoustic meatus: micro-computed tomography study. https://pubmed.ncbi.nlm.nih.gov/26339817/
4. Merida Velasco et al. Anterior tympanic artery: course, ramification and relationship with the temporomandibular joint. https://pubmed.ncbi.nlm.nih.gov/9394959/
5. Deconstruction of the surgical approach to the jugular foramen region: anatomical study. https://pmc.ncbi.nlm.nih.gov/articles/PMC6748855/

Final checks: 48 regional vessel/bone tests and 12 passage centrelines clear; 22 complete safe injection routes and 96 closed DSA split sections; eight bounded cross-sections and two fundal stop rays; 62 major arterial arrays and 57 other bone/teeth/hyoid meshes unchanged; 20 original shared interfaces retained exactly; four potential-link endpoint overlaps checked. Five planned batches remain.
