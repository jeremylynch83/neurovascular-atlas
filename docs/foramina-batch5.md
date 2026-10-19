# Skull foramina batch 5, v0.9.138

This batch changes nine bone meshes and 35 arterial display parts, and adds two nasal incisive-aperture markers. It fits the pterygopalatine, nasal and palatal passages and their arterial routes to the existing teaching model. The repairs are reference-guided reconstructions, not patient-specific CT segmentation or clinical validation.

## Implemented

- Bilateral Vidian canals, directed posteriorly towards the lacerum region and kept separate from the superior/lateral rotundum passages.
- Bilateral palatovaginal (pharyngeal) passages fitted around the existing pterygovaginal arteries, with their maxillary origins and potential tubal connections retained.
- Vertically oval sphenopalatine gateways, with the sphenopalatine artery turning medially before its anterior nasal course.
- Descending palatine canals at the maxillary/palatine junction. The arterial approach passes anterior to the pterygoid plate. Greater palatine oral exits and separate smaller posterior lesser palatine passages are fitted independently on each side.
- A transversely oval common oral incisive aperture with paired superior nasal branches. The septal-palatal connections remain potential anastomoses.
- Posterior septal and lateral nasal arterial courses fitted to the delivered asymmetric vomer and nasal walls. The inferior conchae receive local medial-contour relief of at most 2.2 mm while their lateral attachments are retained. These contour edits provide the mucosal arterial corridors, rather than drilling fictitious neural canals through the conchae.
- Palatal arterial depth is fitted separately on each side. Both separate maxillary alveolar meshes are included wherever it overlaps a repaired canal. The native pterygomaxillary fissures and choanae are retained.
- Matching transport of connected display parts, source paths, potential links, closing surfaces and geometry-bound DSA guides. The release retains all existing structure identifiers.

## Verification and limits

The accompanying JSON reports record vessel/bone contacts, bone topology, exact unchanged arrays, arterial interfaces, DSA safe ranges and closed injection splits. The recorded deformation grid checks for local folding. The source model has small pre-existing surface folds in both maxillary trunks and descending palatine branches; the before/after surface report records these separately from newly introduced defects. This release does not claim whole-model freedom from surface intersections. Fine-scale surface contacts below 0.002 mm are treated as tessellation-scale contacts.

Aperture dimensions and conchal contours are fitted teaching-model estimates. Nerves and nasal mucosa are not segmented. The complete infraorbital canal, facial and mandibular repairs remain in batch 6; fine canals and variants remain in batch 7, followed by whole-model validation in batch 8.

## References

- Lupu et al. [The Pterygopalatine Ganglion, Palatine Nerves and Vessels: Dissection and Pathway](https://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0717-95022022000300601). International Journal of Morphology, 2022. Cadaveric regional relationships and palatine neurovascular course.
- [Osseous anatomy of the pterygopalatine fossa](https://www.ajnr.org/content/19/8/1423). AJNR, 1998. CT and dissection relationships of the named gateways.
- [A radioanatomical study of third-segment terminal branches of the maxillary artery in the pterygopalatine fossa](https://pmc.ncbi.nlm.nih.gov/articles/PMC9975186/). CT-based regional arterial relationships.
