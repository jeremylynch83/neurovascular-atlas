# Neurovascular atlas: structure descriptions from the notes

Content catalogue for descriptions in the app.

**Model:** neurovascular-atlas, release 0.8.2.  
**Source:** Jeremy Lynch, *Neurovascular anatomy*, supplied `nv(2).pdf` (86 PDF pages, printed pages 7–92).

**Implementation decision, 3 October 2026:** Treat the supplied notes as the authoritative source for this project. Where the model conflicts with their names, origins, branching relationships, ICA segment membership, arterial course or bony passages, update the model to match the notes in the next implementation batch. Do not rewrite a description merely to accommodate the current model. Preserve stable structure IDs when changing display names or anatomy, and update the linked descriptions alongside the model.

Where the notes explicitly allow an anatomical variant, an existing model configuration that matches that variant can be retained and identified as such. A different term for the same vessel does not by itself require a geometric change.

The catalogue includes every current model entry. Description text is drawn from the notes, with light edits to punctuation, extraction artefacts and wording that depended on a preceding paragraph. Shared left/right descriptions and descriptions of representative branch families are repeated where appropriate. Procedural instructions have generally been left out of these anatomical excerpts.

Only the text beneath **Description** is displayed in the panel section below **Focus / Hide**. Entries without that block should have no Description field in the app. Model IDs, source references and editorial mapping notes are for this document and the later import, not the inspection panel.

Links display a structure name and target `#structure-` followed by its exact model ID. They navigate to the corresponding catalogue entry here. In the app, these links select and focus the exact model ID. Same-side links are used in left/right entries; explicit contralateral references select the other side. Generic bilateral references in midline descriptions remain plain unless an unambiguous midline target exists.

Page references give both the PDF page number and the page printed in the notes. They sit outside the Description block.

## Contents

- [Carotid arteries and branches, right](#carotid-right)
- [Carotid arteries and branches, left](#carotid-left)
- [Vertebrobasilar arteries and branches, right](#vertebrobasilar-right)
- [Vertebrobasilar arteries and branches, left](#vertebrobasilar-left)
- [Midline arteries](#midline-arteries)
- [Potential arterial connections, right](#connections-right)
- [Potential arterial connections, left](#connections-left)
- [Potential arterial connections, midline](#connections-midline)
- [Vascular landmarks](#vascular-landmarks)
- [Bony foramina, passages and regions](#bone-landmarks)
- [Bones and teeth](#bones)
- [Catalogue groups](#groups)
- [Model amendments required by the notes](#notes-authority-amendments)
- [Editorial mapping notes](#editorial-mapping-notes)

**Catalogue:** 994 model entries; 717 entries with note-derived descriptions.

<a id="carotid-right"></a>

## Carotid arteries and branches, right

<a id="structure-artery.anterior.common_carotid_right"></a>

### Common carotid right

**Model ID:** `artery.anterior.common_carotid_right`

**Description**

The right CCA arises from the brachiocephalic trunk behind the sternoclavicular joint. It ascends in the carotid space adjacent to the internal jugular vein (IJV) and vagus nerve and bifurcates into its internal and external branches usually at the upper border of the thyroid cartilage at C4.

At the bifurcation, the vessel dilates into the carotid sinus (or bulb), which is a baroreceptor, sensitive to pressure changes in arterial blood pressure (BP). Stimulation (particularly during balloon angioplasty) may result in pronounced bradycardia and peripheral vasodilatation.

On the posterior edge of the bifurcation is the carotid body, a chemoreceptor which is mainly responsive to changes in the arterial respiratory gases O2, CO2, and pH.

Usually, no branches arise from the CCA itself; however, occasionally the [superior thyroid](#structure-artery.eca.superior_thyroid.right), [ascending pharyngeal](#structure-artery.eca.apa.right), or [occipital arteries](#structure-artery.eca.occipital.right) may do so.

**Source:** `nv(2).pdf`, PDF pages 3–4; printed pages 9–10.

**Parent:** [Arteries](#structure-artery)

<a id="structure-artery.carotid.external.right"></a>

### External carotid artery right

**Model ID:** `artery.carotid.external.right`

**Description**

The ECA arises from the [CCA](#structure-artery.anterior.common_carotid_right), typically at the level of the C4 vertebra (varying from C2 to T2). In 75%, the [internal carotid artery](#structure-artery.anterior.internal_carotid_right) ([ICA](#structure-artery.anterior.internal_carotid_right)) lies posterolateral to the ECA.

It supplies structures of the head, neck, and face, including muscles, skin, and bones, as well as the pharynx, oral cavity, larynx, thyroid gland, cranial nerves (CNs), and dura mater.

Near its origin, the inferiorly directed [superior thyroid artery](#structure-artery.eca.superior_thyroid.right) arises.

The ECA then runs superiorly towards the parotid gland, giving off the lingual and facial arteries anteriorly, and the occipital, [ascending pharyngeal](#structure-artery.eca.apa.right), and [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries posterosuperiorly.

It bifurcates into the [superficial temporal artery](#structure-artery.eca.superficial_temporal.right) ([STA](#structure-artery.eca.superficial_temporal.right)) and [internal maxillary artery](#structure-artery.eca.maxillary.right) ([IMA](#structure-artery.eca.maxillary.right)) after piercing the parotid gland, behind the neck of the mandible.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [Common carotid right](#structure-artery.anterior.common_carotid_right)

<a id="structure-artery.eca.superior_thyroid.right"></a>

### Superior thyroid artery right

**Model ID:** `artery.eca.superior_thyroid.right`

**Description**

Supply: upper thyroid gland, infrahyoid, sternocleidomastoid, and cricothyroid muscles, superior larynx, and the parathyroids. It has rich anastomoses with the inferior thyroid branch of the thyrocervical trunk.

Origin: anteriorly at the origin of the [ECA](#structure-artery.carotid.external.right). Occasionally it originates from the [CCA](#structure-artery.anterior.common_carotid_right) and rarely from a common origin with the [lingual artery](#structure-artery.eca.lingual.right).

Course: it is directed acutely downward and continues lateral to the larynx before reaching the thyroid gland.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.superior_laryngeal.right"></a>

### Superior laryngeal artery right

**Model ID:** `artery.eca.superior_laryngeal.right`

**Parent:** [Superior thyroid artery right](#structure-artery.eca.superior_thyroid.right)

<a id="structure-artery.eca.infrahyoid.right"></a>

### Infrahyoid artery right

**Model ID:** `artery.eca.infrahyoid.right`

**Parent:** [Superior thyroid artery right](#structure-artery.eca.superior_thyroid.right)

<a id="structure-artery.amendment.superior_thyroid_scm_branch.right"></a>

### Superior thyroid SCM branch right

**Model ID:** `artery.amendment.superior_thyroid_scm_branch.right`

**Parent:** [Superior thyroid artery right](#structure-artery.eca.superior_thyroid.right)

<a id="structure-artery.amendment.cricothyroid.right"></a>

### Cricothyroid right

**Model ID:** `artery.amendment.cricothyroid.right`

**Parent:** [Superior thyroid artery right](#structure-artery.eca.superior_thyroid.right)

<a id="structure-artery.eca.lingual.right"></a>

### Lingual artery right

**Model ID:** `artery.eca.lingual.right`

**Description**

Supply: ipsilateral tongue and buccal and oral mucosa. It can also supply the submandibular and sublingual salivary glands.

Origin: the lingual artery originates anteriorly from the [ECA](#structure-artery.carotid.external.right) just below the [facial artery](#structure-artery.eca.facial.right), although it occasionally shares a common origin. Rarely, it can share a common origin with the [superior thyroid](#structure-artery.eca.superior_thyroid.right).

Course: initially, anterosuperior to the greater horn of the hyoid, it then turns inferiorly and then anteriorly, crossed by the hypoglossal nerve. It then runs horizontally along the hyoid before diving under the hyoglossus.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.deep_lingual.right"></a>

### Deep lingual artery right

**Model ID:** `artery.eca.deep_lingual.right`

**Parent:** [Lingual artery right](#structure-artery.eca.lingual.right)

<a id="structure-artery.eca.dorsal_lingual.right"></a>

### Dorsal lingual artery right

**Model ID:** `artery.eca.dorsal_lingual.right`

**Parent:** [Lingual artery right](#structure-artery.eca.lingual.right)

<a id="structure-artery.eca.sublingual.right"></a>

### Sublingual artery right

**Model ID:** `artery.eca.sublingual.right`

**Parent:** [Lingual artery right](#structure-artery.eca.lingual.right)

<a id="structure-artery.eca.facial.right"></a>

### Facial artery right

**Model ID:** `artery.eca.facial.right`

**Description**

Supply: the submandibular gland, musculocutaneous tissue of the face, and the mandible.

Origin: the facial artery usually arises just above the [lingual artery](#structure-artery.eca.lingual.right), although sometimes it shares a common origin.

Course: initially anterosuperiorly directed it turns inferiorly and descends in the parapharyngeal space to reach the submandibular gland. It runs anterolaterally, crossing the deep aspect of the gland and giving off the [submental artery](#structure-artery.eca.submental.right) before crossing the mandible in front of the masseter. The artery terminates at the level of the ala of the nose in about 50% and gives rise to the [superior labial artery](#structure-artery.eca.superior_labial.right) and alar branches. Alternatively, it becomes the [angular artery](#structure-artery.eca.angular.right), running in the nasolabial fold to reach the angle of the eye.

**Source:** `nv(2).pdf`, PDF pages 6, 8; printed pages 12, 14.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.angular.right"></a>

### Angular artery right

**Model ID:** `artery.eca.angular.right`

**Description**

Angular artery: if present, this is the terminal branch of the [facial artery](#structure-artery.eca.facial.right). It may also originate from the ophthalmic or [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right). The vessel courses in the nasojugal fold giving off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery ([lacrimal artery](#structure-artery.anterior.lacrimal_right)) to form the palpebral arcade. There are anastomoses with the ophthalmic, [lateral nasal](#structure-artery.eca.lateral_nasal.right), and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right) in addition to its counterpart across the midline.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.ascending_palatine.right"></a>

### Ascending palatine artery right

**Model ID:** `artery.eca.ascending_palatine.right`

**Description**

Ascending palatine artery: this originates most frequently from the apex of the proximal segment of the [facial artery](#structure-artery.eca.facial.right) or from the [ascending pharyngeal](#structure-artery.eca.apa.right) or lingual arteries. It ascends superiorly between the styloglossus and stylopharyngeus, giving off tonsillar branches. The artery reaches and supplies the soft palate and the Eustachian tube superiorly. It anastomoses with the pharyngeal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right), and [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right) arteries. Damage to this vessel is often implicated in post-tonsillectomy haemorrhage.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.tonsillar.right"></a>

### Tonsillar artery right

**Model ID:** `artery.eca.tonsillar.right`

**Description**

Tonsillar branch: this arises from the proximal descending part and ascends between the internal pterygoid muscle and styloglossus. It courses anteromedially to supply the palatine tonsil and tongue. It can also be injured during tonsillectomy.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.submental.right"></a>

### Submental artery right

**Model ID:** `artery.eca.submental.right`

**Description**

Submental artery: this originates at the submandibular segment of the artery and courses anteriorly on mylohyoid, delivering branches to the submandibular gland and regional musculocutaneous tissue and the mandible.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.inferior_labial.right"></a>

### Inferior labial artery right

**Model ID:** `artery.eca.inferior_labial.right`

**Description**

The inferior labial artery runs along the lower lip. The labial arteries supply the labial glands, mucous membranes, and regional musculature.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.superior_labial.right"></a>

### Superior labial artery right

**Model ID:** `artery.eca.superior_labial.right`

**Description**

The superior labial artery follows the upper lip. The labial arteries supply the labial glands, mucous membranes, and regional musculature. The superior labial artery also delivers branches to the nasal septum and ala and can anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right) (the terminal branch of the [IMA](#structure-artery.eca.maxillary.right)).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.lateral_nasal.right"></a>

### Lateral nasal artery right

**Model ID:** `artery.eca.lateral_nasal.right`

**Description**

Lateral nasal artery: this originates distal to the [superior labial](#structure-artery.eca.superior_labial.right) branch (or from the [superior labial artery](#structure-artery.eca.superior_labial.right)) and runs superiorly along the side of the nose. Occasionally, it is the terminal branch of the [facial artery](#structure-artery.eca.facial.right).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.amendment.facial_submandibular_gland_branch.right"></a>

### Facial submandibular gland branch right

**Model ID:** `artery.amendment.facial_submandibular_gland_branch.right`

**Description**

Submandibular gland branches originate inferiorly from the submandibular and submental segments of the [facial artery](#structure-artery.eca.facial.right).

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.amendment.facial_masseteric_branch.right"></a>

### Facial masseteric branch right

**Model ID:** `artery.amendment.facial_masseteric_branch.right`

**Description**

Masseteric muscular and buccal mucosal branches: these originate superiorly from the [facial artery](#structure-artery.eca.facial.right).

Anastomoses: masseteric branches of the [facial artery](#structure-artery.eca.facial.right) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right).

**Source:** `nv(2).pdf`, PDF pages 9, 20; printed pages 15, 26.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.amendment.facial_buccal_branch.right"></a>

### Facial buccal branch right

**Model ID:** `artery.amendment.facial_buccal_branch.right`

**Description**

Masseteric muscular and buccal mucosal branches: these originate superiorly from the [facial artery](#structure-artery.eca.facial.right).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.eca.occipital.right"></a>

### Occipital artery right

**Model ID:** `artery.eca.occipital.right`

**Description**

Supply: musculocutaneous tissue and bone, dura mater of the posterior cranial fossa, and CNs.

Origin: posterosuperiorly from the proximal [ECA](#structure-artery.carotid.external.right) usually just above or below the [ascending pharyngeal artery](#structure-artery.eca.apa.right) (occasionally they share a common trunk). In some cases, it arises from the internal carotid, vertebral, deep cervical, or [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries.

First segment: runs posterosuperiorly to reach the occipital groove of the temporal bone.

Second segment: horizontal to the superior nuchal line (a bony ridge sweeping laterally from the external occipital protuberance).

Third segment: ascends the distal occiput.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.occipital_lateral_scalp.right"></a>

### Occipital lateral scalp artery right

**Model ID:** `artery.eca.occipital_lateral_scalp.right`

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

<a id="structure-artery.eca.occipital_medial_scalp.right"></a>

### Occipital medial scalp artery right

**Model ID:** `artery.eca.occipital_medial_scalp.right`

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

<a id="structure-artery.eca.occipital_descending.right"></a>

### Occipital descending artery right

**Model ID:** `artery.eca.occipital_descending.right`

**Description**

Descending muscular branches: there are superficial and deep muscular branches arising from the second segment that run inferiorly to supply the back muscles, such as the splenius and trapezius. Importantly, the deep branch anastomoses with the [vertebral artery](#structure-artery.posterior.vertebral_right) and branches of the costocervical trunk at the C1-C2 level and the cervical arteries at C3-C4.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

<a id="structure-artery.eca.occipital_mastoid.right"></a>

### Occipital mastoid artery right

**Model ID:** `artery.eca.occipital_mastoid.right`

**Description**

Mastoid branches: these arise from the second segment and supply the mastoid bone and skin. A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

<a id="structure-artery.amendment.occipital_mastoid_dural_branch.right"></a>

### Occipital mastoid dural branch right

**Model ID:** `artery.amendment.occipital_mastoid_dural_branch.right`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid artery right](#structure-artery.eca.occipital_mastoid.right)

<a id="structure-artery.amendment.occipital_scm_branch.right"></a>

### Occipital SCM branch right

**Model ID:** `artery.amendment.occipital_scm_branch.right`

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

<a id="structure-artery.eca.posterior_auricular.right"></a>

### Posterior auricular artery right

**Model ID:** `artery.eca.posterior_auricular.right`

**Description**

Supply: musculocutaneous tissue of the face, scalp, pinna, and parotid gland. It is in haemodynamic balance with the [occipital artery](#structure-artery.eca.occipital.right) and [STA](#structure-artery.eca.superficial_temporal.right). There are anastomoses with the anterior auricular artery (a branch of the [STA](#structure-artery.eca.superficial_temporal.right)) above the ear.

Origin: the vessel arises from the distal [ECA](#structure-artery.carotid.external.right) posteriorly at the level of the inferior parotid gland. Alternatively, it may share a common trunk with the [occipital artery](#structure-artery.eca.occipital.right).

Course: the artery is directed posterosuperiorly beneath the parotid gland and runs on the superior surface of the posterior belly of the digastric muscle. It turns superficially at the mastoid process and courses posterosuperiorly in the posterior auricular sulcus, between the mastoid process and the pinna.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.occipital.stylomastoid.right"></a>

### Stylomastoid artery right

**Model ID:** `artery.eca.occipital.stylomastoid.right`

**Description**

Stylomastoid artery: this arises from the first segment of the [occipital artery](#structure-artery.eca.occipital.right) or the [posterior auricular artery](#structure-artery.eca.posterior_auricular.right). It enters the [stylomastoid foramen](#structure-landmark.stylomastoid.right) with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the middle meningeal artery](#structure-artery.eca.maxillary.mma.petrosal.right) ([MMA](#structure-artery.eca.maxillary.mma.right)). It enters the tympanic cavity and anastomoses with the [superior tympanic artery](#structure-artery.amendment.superior_tympanic.right) from the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right) branch of the [IMA](#structure-artery.eca.maxillary.right), the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right), the [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) branch of the [ICA](#structure-artery.anterior.internal_carotid_right), and the arcuate branch of the [anterior inferior cerebellar artery](#structure-artery.posterior.aica_right) ([AICA](#structure-artery.posterior.aica_right)). It also supplies the tympanic antrum, mastoid bone, and semicircular canal.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Posterior auricular artery right](#structure-artery.eca.posterior_auricular.right)

<a id="structure-artery.amendment.posterior_auricular_parotid_branch.right"></a>

### Posterior auricular parotid branch right

**Model ID:** `artery.amendment.posterior_auricular_parotid_branch.right`

**Parent:** [Posterior auricular artery right](#structure-artery.eca.posterior_auricular.right)

<a id="structure-artery.amendment.posterior_auricular_auricular_branch.right"></a>

### Posterior auricular auricular branch right

**Model ID:** `artery.amendment.posterior_auricular_auricular_branch.right`

**Parent:** [Posterior auricular artery right](#structure-artery.eca.posterior_auricular.right)

<a id="structure-artery.eca.superficial_temporal.right"></a>

### Superficial temporal artery right

**Model ID:** `artery.eca.superficial_temporal.right`

**Description**

Supply: the lateral aspect of the scalp and face.

Origin: this is one of the two terminal divisions of the [ECA](#structure-artery.carotid.external.right) (the other being the [IMA](#structure-artery.eca.maxillary.right)).

Course: the artery originates behind the neck of the mandible in the parotid gland. It ascends laterally along the superficial surface of the temporalis muscle, over the posterior aspect of the condylar process, and passes superficially over the zygomatic process of the temporal bone. After a few centimetres it divides into its frontal and parietal terminal branches.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.superficial_temporal.frontal.right"></a>

### STA frontal artery right

**Model ID:** `artery.eca.superficial_temporal.frontal.right`

**Description**

The frontal and parietal terminal divisions of the [STA](#structure-artery.eca.superficial_temporal.right) arise a couple of centimetres above the superior margin of the zygomatic arch, supplying muscle, skin, and bone. The frontal division curves anterosuperiorly towards the superior orbital rim. It anastomoses with the supraorbital and frontal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.eca.sta_frontal_anterior_twig.right"></a>

### STA frontal anterior twig artery right

**Model ID:** `artery.eca.sta_frontal_anterior_twig.right`

**Parent:** [STA frontal artery right](#structure-artery.eca.superficial_temporal.frontal.right)

<a id="structure-artery.eca.superficial_temporal.parietal.right"></a>

### STA parietal artery right

**Model ID:** `artery.eca.superficial_temporal.parietal.right`

**Description**

The frontal and parietal terminal divisions of the [STA](#structure-artery.eca.superficial_temporal.right) arise a couple of centimetres above the superior margin of the zygomatic arch, supplying muscle, skin, and bone. The parietal division runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right), and [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.eca.sta_parietal_anterior_twig.right"></a>

### STA parietal anterior twig artery right

**Model ID:** `artery.eca.sta_parietal_anterior_twig.right`

**Parent:** [STA parietal artery right](#structure-artery.eca.superficial_temporal.parietal.right)

<a id="structure-artery.eca.superficial_temporal.transverse_facial.right"></a>

### Transverse facial artery right

**Model ID:** `artery.eca.superficial_temporal.transverse_facial.right`

**Description**

Transverse facial artery: this arises within the parotid gland near the origin of the [STA](#structure-artery.eca.superficial_temporal.right) and divides into superior and inferior branches. The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), zygomaticomalar, inferior palpebral, buccal, and facial arteries. The inferior trunk also supplies the parotid gland and runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.amendment.transverse_facial_superior_division.right"></a>

### Transverse facial superior division right

**Model ID:** `artery.amendment.transverse_facial_superior_division.right`

**Description**

The superior division of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right) passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery right](#structure-artery.eca.superficial_temporal.transverse_facial.right)

<a id="structure-artery.amendment.transverse_facial_inferior_division.right"></a>

### Transverse facial inferior division right

**Model ID:** `artery.amendment.transverse_facial_inferior_division.right`

**Description**

The inferior trunk of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right) also supplies the parotid gland and runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery right](#structure-artery.eca.superficial_temporal.transverse_facial.right)

<a id="structure-artery.amendment.transverse_facial_masseteric_branch.right"></a>

### Transverse facial masseteric branch right

**Model ID:** `artery.amendment.transverse_facial_masseteric_branch.right`

**Description**

The inferior trunk of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right) runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial inferior division right](#structure-artery.amendment.transverse_facial_inferior_division.right)

<a id="structure-artery.amendment.transverse_facial_parotid_branch.right"></a>

### Transverse facial parotid branch right

**Model ID:** `artery.amendment.transverse_facial_parotid_branch.right`

**Description**

Both divisions of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right) supply the parotid gland.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery right](#structure-artery.eca.superficial_temporal.transverse_facial.right)

<a id="structure-artery.eca.middle_temporal.right"></a>

### Middle deep temporal artery right

**Model ID:** `artery.eca.middle_temporal.right`

**Description**

Posterior deep temporal artery: this arises at the level of the zygoma and is directed posteroinferiorly. Rarely it originates from the [IMA](#structure-artery.eca.maxillary.right) or from a common trunk with the zygomatico-orbital arteries. It supplies the temporalis muscle and anastomoses with the middle and anterior temporal arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.amendment.sta_anterior_auricular.right"></a>

### STA anterior auricular right

**Model ID:** `artery.amendment.sta_anterior_auricular.right`

**Description**

Anterior auricular branches: superior, middle, and inferior branches supply the external ear.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.amendment.zygomatico_orbital.right"></a>

### Zygomatico-orbital right

**Model ID:** `artery.amendment.zygomatico_orbital.right`

**Description**

Zygomatico-orbital artery: this arises just proximal to the bifurcation and is directed anteriorly along the upper border of the zygomatic arch towards the lateral angle of the orbit. The artery supplies the anterior temporal and malar region and orbicularis orbis.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery right](#structure-artery.eca.superficial_temporal.right)

<a id="structure-artery.eca.maxillary.right"></a>

### Maxillary artery right

**Model ID:** `artery.eca.maxillary.right`

**Description**

The internal maxillary artery (IMA) and [STA](#structure-artery.eca.superficial_temporal.right) are the terminal divisions of the [ECA](#structure-artery.carotid.external.right). The IMA can be referred to as simply the maxillary artery.

IMA branches supply the organs and muscles of the head and neck, mouth, paranasal sinuses, dura, and CNs.

Origin: the IMA originates within the parotid gland behind the neck of the mandible.

The first (mandibular) segment runs deep to the neck of the mandible and runs anterior just lateral to the inferior alveolar nerve towards the border of the lateral pterygoid muscle. It gives off the [deep auricular](#structure-artery.eca.maxillary.deep_auricular.right), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right), middle meningeal, [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right), and [inferior alveolar (dental)](#structure-artery.eca.maxillary.inferior_alveolar.right) arteries.

The second (zygomatic or pterygoid) segment curves anteromedially, either superficial or deep to the pterygoid muscles, to reach the pterygopalatine fossa. It gives off [middle deep temporal](#structure-artery.eca.posterior_deep_temporal.right), pterygoid, masseteric, buccal, and [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right) branches.

The third (pterygopalatine) segment runs medially in the pterygopalatine fossa giving off the [posterior superior dental](#structure-artery.eca.maxillary.posterior_superior_alveolar.right), [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right), and pharyngeal arteries and the arteries of the [foramen rotundum](#structure-landmark.rotundum.right), [pterygoid canal](#structure-landmark.pterygoid-canal.right) (vidian artery), and [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right). It terminates as the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right) at the medial border of the fossa, in the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.right).

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.maxillary.deep_auricular.right"></a>

### Deep auricular artery right

**Model ID:** `artery.eca.maxillary.deep_auricular.right`

**Description**

Origin: this tiny artery is the first maxillary branch. It may share a common origin with the [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right).

Course: it ascends within the parotid behind the temporomandibular joint. It passes through the wall of the external acoustic meatus to supply the skin of the canal and the outer surface of the tympanic membrane.

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.anterior_tympanic.right"></a>

### Anterior tympanic artery right

**Model ID:** `artery.eca.maxillary.anterior_tympanic.right`

**Description**

Origin: another small vessel, sometimes shares a common origin with the [deep auricular artery](#structure-artery.eca.maxillary.deep_auricular.right). It also occasionally arises from the [STA](#structure-artery.eca.superficial_temporal.right), the distal [ECA](#structure-artery.carotid.external.right), or other proximal maxillary arteries such as the inferior dental or middle meningeal.

Course: the artery ascends behind the temporomandibular joint and bifurcates into anterior and posterior branches. The anterior branch supplies the temporomandibular joint, and the posterior branch enters the tympanic cavity through the [petrotympanic fissure](#structure-landmark.petrotympanic.right) to supply the mucosa of the tympanic cavity and the tympanic membrane.

Anastomoses: [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right), the [artery of the pterygoid canal](#structure-artery.eca.maxillary.pterygoid_canal.right) (vidian artery), and anastomoses within the tympanic cavity including the [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) branch of the [ICA](#structure-artery.anterior.internal_carotid_right).

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.inferior_alveolar.right"></a>

### Inferior alveolar artery right

**Model ID:** `artery.eca.maxillary.inferior_alveolar.right`

**Description**

Origin: inferiorly from the first segment of the [IMA](#structure-artery.eca.maxillary.right). Occasionally arises from a common trunk with the [middle deep temporal artery](#structure-artery.eca.posterior_deep_temporal.right).

The vessel supplies the roots of the lower teeth.

Course: it runs inferiorly accompanying the inferior alveolar nerve and vein. It enters the [mandibular canal](#structure-landmark.mandibular-canal.right) through an opening on the medial surface of the mandibular ramus and then courses anteroinferiorly and medially towards the [mental foramen](#structure-landmark.mental-foramen.right) on the anterior surface of the mandible, anastomosing with mental branches of the [facial artery](#structure-artery.eca.facial.right).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.mental.right"></a>

### Mental artery right

**Model ID:** `artery.eca.mental.right`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right) divides into incisor and mental terminal branches opposite the first premolar tooth. The mental branch supplies the lower lip and chin.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery right](#structure-artery.eca.maxillary.inferior_alveolar.right)

<a id="structure-artery.eca.incisive.right"></a>

### Incisive artery right

**Model ID:** `artery.eca.incisive.right`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right) divides into incisor and mental terminal branches opposite the first premolar tooth. The incisor branch supplies the pulp of the teeth.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery right](#structure-artery.eca.maxillary.inferior_alveolar.right)

<a id="structure-artery.eca.mylohyoid.right"></a>

### Mylohyoid artery right

**Model ID:** `artery.eca.mylohyoid.right`

**Description**

Extramandibular branches of the [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right) supply the pterygoid and mylohyoid muscles and the lingual nerve.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery right](#structure-artery.eca.maxillary.inferior_alveolar.right)

<a id="structure-artery.eca.posterior_deep_temporal.right"></a>

### Middle deep temporal artery right

**Model ID:** `artery.eca.posterior_deep_temporal.right`

**Description**

Origin: this is from the proximal aspect of the second maxillary segment. It may share a common origin with the [inferior dental artery](#structure-artery.eca.maxillary.inferior_alveolar.right).

Course: superiorly on the temporal bone giving off small branches to bone and the temporalis muscle.

Anastomoses: [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right) and [superficial temporal arteries](#structure-artery.eca.superficial_temporal.right). There are transosseous anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) and distal lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.anterior_deep_temporal.right"></a>

### Anterior deep temporal artery right

**Model ID:** `artery.eca.anterior_deep_temporal.right`

**Description**

Origin: the anterior deep temporal artery takes its origin from the distal aspect of the second segment. It may share a common origin with the [buccal artery](#structure-artery.eca.maxillary.buccal.right).

Course: anterosuperiorly along the temporalis muscle which it supplies. It contributes an important branch to the lateral orbit which it reaches either via the zygomatic temporal fissure or [inferior orbital fissure](#structure-landmark.inferior-orbital-fissure.right).

Anastomoses: middle deep and [superficial temporal arteries](#structure-artery.eca.superficial_temporal.right) and also distal lacrimal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF pages 20–21; printed pages 26–27.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.masseteric.right"></a>

### Masseteric artery right

**Model ID:** `artery.eca.maxillary.masseteric.right`

**Description**

Origin: proximal part of the second maxillary segment.

Course: inferiorly through the mandibular notch, between the coronoid and condyloid processes, to supply the masseter muscle.

Anastomoses: masseteric branches of the [facial artery](#structure-artery.eca.facial.right) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right).

**Source:** `nv(2).pdf`, PDF pages 15, 20; printed pages 21, 26.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.buccal.right"></a>

### Buccal artery right

**Model ID:** `artery.eca.maxillary.buccal.right`

**Description**

Origin: distal part of the second maxillary segment.

Course: inferiorly to supply buccal mucosa, buccinator, the parotid duct, and skin.

Anastomoses: ascending branch of the [facial artery](#structure-artery.eca.facial.right) and the superior masseteric branch of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right). It is an important route for [facial artery](#structure-artery.eca.facial.right) reconstitution after proximal [facial artery](#structure-artery.eca.facial.right) ligation.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.pterygoid_muscular.right"></a>

### Pterygoid muscular artery right

**Model ID:** `artery.eca.pterygoid_muscular.right`

**Description**

Origin: inferiorly from the second maxillary segment.

The artery supplies the medial and lateral pterygoid muscles.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.posterior_superior_alveolar.right"></a>

### Posterior superior alveolar artery right

**Model ID:** `artery.eca.maxillary.posterior_superior_alveolar.right`

**Description**

Origin: this artery takes its origin from the proximal part of the third maxillary segment, just inside the pterygopalatine fossa. It often shares a common trunk with the [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right).

Course: anteroinferiorly on the lateral surface of the maxilla, giving off osseous branches, supplying the mucosa of the maxillary sinus and buccal cavity, and buccinator. The vessel then enters the superior alveolar canal in the maxilla running towards the incisor foramen.

Anastomoses: [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right), and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right) arteries.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.psa_anterior_division.right"></a>

### PSA anterior division right

**Model ID:** `artery.eca.psa_anterior_division.right`

**Parent:** [Posterior superior alveolar artery right](#structure-artery.eca.maxillary.posterior_superior_alveolar.right)

<a id="structure-artery.eca.maxillary.infraorbital.right"></a>

### Infraorbital artery right

**Model ID:** `artery.eca.maxillary.infraorbital.right`

**Description**

Origin: this terminal branch of the [IMA](#structure-artery.eca.maxillary.right) arises anteroinferiorly from the proximal part of the third maxillary segment. It may share a common origin with the [posterior superior dental artery](#structure-artery.eca.maxillary.posterior_superior_alveolar.right). It supplies the inferior rectus and inferior oblique muscles and lacrimal sac.

Course: laterally, it looks like an upturned boat hull. It ascends on the posterior wall of the maxillary sinus and then traverses the [inferior orbital fissure](#structure-landmark.inferior-orbital-fissure.right) to enter the orbit. The vessel runs forward on the orbital floor in the [infraorbital groove](#structure-landmark.infraorbital-groove.right) (together with the infraorbital nerve and vein), giving off osseous and muscular branches and anastomosing with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right). It then exits through the [infraorbital foramen](#structure-landmark.infraorbital-foramen.right) (again with the infraorbital nerve and vein) to supply the lateral aspect of the nose, upper lip, and the lower eyelid.

Anastomoses: the terminal branches anastomose with the superficial temporal, ophthalmic, facial, and [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right) arteries.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.anterior_superior_alveolar.right"></a>

### Anterior superior alveolar artery right

**Model ID:** `artery.eca.anterior_superior_alveolar.right`

**Parent:** [Infraorbital artery right](#structure-artery.eca.maxillary.infraorbital.right)

<a id="structure-artery.amendment.infraorbital_muscular_branch.right"></a>

### Infraorbital muscular branch right

**Model ID:** `artery.amendment.infraorbital_muscular_branch.right`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) supplies the inferior rectus and inferior oblique muscles and lacrimal sac. On the orbital floor it gives off osseous and muscular branches and anastomoses with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Infraorbital artery right](#structure-artery.eca.maxillary.infraorbital.right)

<a id="structure-artery.eca.maxillary.descending_palatine.right"></a>

### Descending palatine artery right

**Model ID:** `artery.eca.maxillary.descending_palatine.right`

**Description**

Origin: inferiorly from the third maxillary segment. It may share a common origin with the [posterior lateral nasal branch](#structure-artery.eca.posterior_lateral_nasal.right) of the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right).

Course: it descends and enters the [greater palatine (pterygopalatine) canal](#structure-landmark.greater-palatine-canal.right) accompanied by the great palatine nerve. Within the canal it gives off the [lesser palatine artery](#structure-artery.eca.lesser_palatine.right) which supplies the soft palate. The artery becomes the [greater palatine artery](#structure-artery.eca.greater_palatine.right) as it exits the canal through the [greater palatine foramen](#structure-landmark.greater-palatine-foramen.right). It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

Anastomoses: [posterior septal arteries](#structure-artery.eca.posterior_septal.right) (from the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right)) and the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.greater_palatine.right"></a>

### Greater palatine artery right

**Model ID:** `artery.eca.greater_palatine.right`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) becomes the greater palatine artery as it exits the canal through the [greater palatine foramen](#structure-landmark.greater-palatine-foramen.right). It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

Anastomoses: [posterior septal arteries](#structure-artery.eca.posterior_septal.right) (from the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right)) and the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Descending palatine artery right](#structure-artery.eca.maxillary.descending_palatine.right)

<a id="structure-artery.eca.lesser_palatine.right"></a>

### Lesser palatine artery right

**Model ID:** `artery.eca.lesser_palatine.right`

**Description**

Within the [greater palatine canal](#structure-landmark.greater-palatine-canal.right), the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) gives off the lesser palatine artery, which supplies the soft palate.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Descending palatine artery right](#structure-artery.eca.maxillary.descending_palatine.right)

<a id="structure-artery.eca.maxillary.sphenopalatine.right"></a>

### Sphenopalatine artery right

**Model ID:** `artery.eca.maxillary.sphenopalatine.right`

**Description**

Origin: the sphenopalatine is a terminal branch of the [maxillary artery](#structure-artery.eca.maxillary.right).

Course: medially through the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.right) to enter the nasal cavity, which it supplies in addition to the paranasal sinuses. It is best seen on the anteroposterior projection angiographically due to its medial course.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.posterior_septal.right"></a>

### Posterior septal artery right

**Model ID:** `artery.eca.posterior_septal.right`

**Description**

Posterior septal (or medial [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right)) artery: this vessel is medially directed towards the superior turbinate and gives off a branch to the sphenoid ostium. It divides into superior and inferior branches. The superior branch supplies the superior turbinate before coursing medially to the nasal septum where it curves anteriorly. It anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right) and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right) and contributes to Kiesselbach’s plexus. This plexus is located on the anterior inferior quadrant of the nasal septum (‘Little’s area’) and is a common site for epistaxis. It is supplied by five vessels: the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right), [superior labial](#structure-artery.eca.superior_labial.right), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_right), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_right) arteries.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Sphenopalatine artery right](#structure-artery.eca.maxillary.sphenopalatine.right)

<a id="structure-artery.amendment.superior_septal_subdivision.right"></a>

### Superior septal subdivision right

**Model ID:** `artery.amendment.superior_septal_subdivision.right`

**Description**

The [posterior septal artery](#structure-artery.eca.posterior_septal.right) divides into superior and inferior branches. The superior branch supplies the superior turbinate before coursing medially to the nasal septum where it curves anteriorly. It anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right) and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right) and contributes to Kiesselbach’s plexus.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Posterior septal artery right](#structure-artery.eca.posterior_septal.right)

<a id="structure-artery.amendment.inferior_septal_subdivision.right"></a>

### Inferior septal subdivision right

**Model ID:** `artery.amendment.inferior_septal_subdivision.right`

**Parent:** [Posterior septal artery right](#structure-artery.eca.posterior_septal.right)

<a id="structure-artery.eca.posterior_lateral_nasal.right"></a>

### Posterior lateral nasal artery right

**Model ID:** `artery.eca.posterior_lateral_nasal.right`

**Description**

Posterior lateral nasal artery (or lateral [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right)): this vessel sometimes originates from the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right). It supplies the middle and inferior turbinates and maxillary and ethmoidal sinuses. It may anastomose with branches of the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right), nasal branches of the [facial artery](#structure-artery.eca.facial.right), and ethmoidal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Sphenopalatine artery right](#structure-artery.eca.maxillary.sphenopalatine.right)

<a id="structure-artery.eca.pterygovaginal.right"></a>

### Pterygovaginal artery right

**Model ID:** `artery.eca.pterygovaginal.right`

**Description**

Origin: third maxillary segment proximal to the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.right). It sometimes shares a common trunk with the artery of the pterygoid/[vidian canal](#structure-landmark.pterygoid-canal.right) or the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right).

Course: posteromedially and inferiorly through the pharyngeal (pterygovaginal) canal to supply the roof of pharynx and pharyngeal end of the Eustachian tube.

Anastomoses: branches of the [ascending pharyngeal artery](#structure-artery.eca.apa.right), vidian artery, and [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) (pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.pterygoid_canal.right"></a>

### Vidian artery right

**Model ID:** `artery.eca.maxillary.pterygoid_canal.right`

**Description**

Origin: posterosuperiorly from the third maxillary segment. It may share a common origin with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right) or the pharyngeal artery.

It supplies the mucosa of the pterygopalatine fossa and nasopharyngeal cavity.

Course: the vessel has a horizontal course, running posterolaterally through the [vidian canal](#structure-landmark.pterygoid-canal.right) accompanied by the vidian nerve to reach the [foramen lacerum](#structure-landmark.foramen-lacerum.right) where it anastomoses with the other vidian artery arising from the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous). Along its course it gives off mucosal branches to the nasal and oropharyngeal cavities and osseous branches within the [pterygoid canal](#structure-landmark.pterygoid-canal.right) and Eustachian tube.

Anastomoses: [vidian artery of the ICA](#structure-artery.anterior.vidian_ica_contribution_right), [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right), mandibular artery, [ascending pharyngeal](#structure-artery.eca.apa.right) ([superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right)), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right), and [ascending palatine](#structure-artery.eca.ascending_palatine.right) arteries (the pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.foramen_rotundum.right"></a>

### Artery of the foramen rotundum right

**Model ID:** `artery.eca.maxillary.foramen_rotundum.right`

**Description**

Origin: posterosuperiorly from the third maxillary segment. It courses posteriorly accompanied by the maxillary nerve, which it supplies, and enters the cranium through the [foramen rotundum](#structure-landmark.rotundum.right) to supply dura mater. It has a characteristic corkscrew appearance.

Anastomoses: there is an important anastomosis with the [anterolateral branch of the ILT](#structure-artery.amendment.ilt_anterolateral_ramus.right) (from the [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous)).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.accessory_meningeal.right"></a>

### Accessory meningeal artery right

**Model ID:** `artery.eca.maxillary.accessory_meningeal.right`

**Description**

Origin: this artery has an oblique anterior and medial slant, arising anterosuperiorly from the first segment of the [IMA](#structure-artery.eca.maxillary.right) or from the extracranial [MMA](#structure-artery.eca.maxillary.mma.right). It supplies the CNs, the pharynx, the Eustachian tube, meninges and has several important anastomoses.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.amendment.accessory_meningeal_anterior_tubal.right"></a>

### Accessory meningeal anterior tubal right

**Model ID:** `artery.amendment.accessory_meningeal_anterior_tubal.right`

**Description**

Anterior branch: courses along the Eustachian tube reaching the torus tubaris, supplying regional mucosa, bone, and the tensor veli palatini muscle. There are anastomoses with the vidian artery, mandibular artery, the artery of the pterygoid and pharyngeal canals, and the pharyngeal branch of the [ascending pharyngeal](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Accessory meningeal artery right](#structure-artery.eca.maxillary.accessory_meningeal.right)

<a id="structure-artery.amendment.accessory_meningeal_posterior_intracranial.right"></a>

### Accessory meningeal posterior intracranial right

**Model ID:** `artery.amendment.accessory_meningeal_posterior_intracranial.right`

**Description**

Posterior branch: ascends superiorly and enters the skull through the [foramen ovale](#structure-landmark.ovale.right) or [foramen vesalius](#structure-landmark.vesalius.right). The vessel supplies the mandibular division of the trigeminal nerve, trigeminal ganglion and dura mater of Meckel’s cave and the middle cranial fossa. There are anastomoses with inferolateral and MHTs of the [ICA](#structure-artery.anterior.internal_carotid_right), recurrent meningeal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right), cavernous branches of the [MMA](#structure-artery.eca.maxillary.mma.right), the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right), and the [subarcuate artery](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Accessory meningeal artery right](#structure-artery.eca.maxillary.accessory_meningeal.right)

<a id="structure-artery.eca.maxillary.mma.right"></a>

### Middle meningeal artery right

**Model ID:** `artery.eca.maxillary.mma.right`

**Description**

The middle meningeal artery supplies more than two-thirds of the cranial dura.

Origin: the MMA arises from the superomedial surface of the first segment of the [IMA](#structure-artery.eca.maxillary.right). Often it shares a common trunk with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right). The MMA may also rarely originate from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) (the ‘recurrent meningeal artery’), the [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous) via the [ILT](#structure-artery.anterior.inferolateral_trunk_right), the [petrosal ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) via the persistent stapedial or vidian arteries, the [cervical ICA](#structure-artery.anterior.internal_carotid_right.segment.cervical), the [basilar artery](#structure-artery.posterior.basilar) (usually distal third), or the [occipital artery](#structure-artery.eca.occipital.right).

Extracranial segment: the artery passes superiorly and medially and enters the cranial cavity via the [foramen spinosum](#structure-landmark.foramen-spinosum.right).

Horizontal segment: it then turns abruptly laterally and runs horizontally giving off wispy petrosal and cavernous sinus branches. The vessel continues to reach the petrosquamous suture, delivering a [petrosquamosal branch](#structure-artery.eca.maxillary.mma.petrosquamosal.right).

Temporal segment: it then courses anteriorly on the greater wing of the sphenoid to reach the pterion (the convergence of the frontal, parietal, temporal, and sphenoid bones).

Pterional segment: this segment curves around the pterion.

Coronal segment: this segment runs superomedially along the coronal suture towards the midline, becoming the paramedian artery supplying the superior sagittal sinus.

**Source:** `nv(2).pdf`, PDF pages 15, 18; printed pages 21, 24.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.maxillary.mma.frontal.right"></a>

### MMA frontal artery right

**Model ID:** `artery.eca.maxillary.mma.frontal.right`

**Description**

Anterior convexity branches: these originate from the temporal, pterional, and coronal segments and course medially along the lesser wing of the sphenoid bone. There are important anastomoses with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right). The [MMA](#structure-artery.eca.maxillary.mma.right) may be the sole supply of the orbit (the ‘meningo-ophthalmic artery’) or supply the lacrimal gland and lateral orbit via a recurrent branch traversing the [foramen of Hyrtl](#structure-landmark.cranio-orbital.right) (found in the spheno-orbital foramen, in the orbital roof). This latter branch usually also has [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) anastomoses. Anterior branches from the coronal segment anastomose with the [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_right) branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.eca.mma_frontal_anterior_division.right"></a>

### MMA frontal anterior division right

**Model ID:** `artery.eca.mma_frontal_anterior_division.right`

**Parent:** [MMA frontal artery right](#structure-artery.eca.maxillary.mma.frontal.right)

<a id="structure-artery.eca.mma_frontal_posterior_division.right"></a>

### MMA frontal posterior division right

**Model ID:** `artery.eca.mma_frontal_posterior_division.right`

**Parent:** [MMA frontal artery right](#structure-artery.eca.maxillary.mma.frontal.right)

<a id="structure-artery.amendment.mma_paramedian.right"></a>

### MMA paramedian right

**Model ID:** `artery.amendment.mma_paramedian.right`

**Description**

Paramedian arteries: these are the terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right). They are directed anteriorly or posteriorly along the superior sagittal sinus and anastomose with the anterior (from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right)) or posterior (from the [ascending pharyngeal](#structure-artery.eca.apa.right)) falcine arteries. They deliver small branches to the superior sagittal sinus and falx cerebri. They also anastomose with dural branches of the posterior cerebral artery (PCA; Davidoff and Schechter) and the [superior cerebellar artery](#structure-artery.posterior.sca_right) ([SCA](#structure-artery.posterior.sca_right); [artery of Wollschlaeger and Wollschlaeger](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.right)).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [MMA frontal artery right](#structure-artery.eca.maxillary.mma.frontal.right)

<a id="structure-artery.amendment.mma_falcine_terminal.right"></a>

### MMA falcine terminal right

**Model ID:** `artery.amendment.mma_falcine_terminal.right`

**Description**

The paramedian terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right) deliver small branches to the superior sagittal sinus and falx cerebri. They anastomose with the anterior and posterior falcine arteries, and with dural branches of the PCA and [SCA](#structure-artery.posterior.sca_right).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [MMA paramedian right](#structure-artery.amendment.mma_paramedian.right)

<a id="structure-artery.eca.maxillary.mma.posterior_convexity.right"></a>

### MMA posterior convexity artery right

**Model ID:** `artery.eca.maxillary.mma.posterior_convexity.right`

**Description**

Posterior convexity branches: a variable number of posterior branches arise from the temporal and coronal segments, and the petrosquamosal branches, supplying a large region of convexity dura mater. Note that all peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right) and [occipital artery](#structure-artery.eca.occipital.right) via transosseous branches, which become evident under pathological conditions, in particular, dural arteriovenous fistulas. There are also potential anastomoses with dural branches of cortical arteries.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.eca.mma_parietal_ascending.right"></a>

### MMA parietal ascending artery right

**Model ID:** `artery.eca.mma_parietal_ascending.right`

**Parent:** [MMA posterior convexity artery right](#structure-artery.eca.maxillary.mma.posterior_convexity.right)

<a id="structure-artery.eca.mma_posterior_terminal.right"></a>

### MMA posterior terminal artery right

**Model ID:** `artery.eca.mma_posterior_terminal.right`

**Parent:** [MMA posterior convexity artery right](#structure-artery.eca.maxillary.mma.posterior_convexity.right)

<a id="structure-artery.eca.maxillary.mma.petrosquamosal.right"></a>

### MMA petrosquamosal artery right

**Model ID:** `artery.eca.maxillary.mma.petrosquamosal.right`

**Description**

Petrosquamosal branch: this arises from the horizontal segment slightly more distally than the petrosal branches. On the lateral view it can be difficult to distinguish from the petrosal branches, but this is easy on anteroposterior (AP) views as the petrosquamosal is directed laterally (and is usually more prominent) whereas the petrosal branches course medially and are wispy.

**Source:** `nv(2).pdf`, PDF pages 18–19; printed pages 24–25.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.eca.maxillary.mma.petrosal.right"></a>

### MMA petrosal artery right

**Model ID:** `artery.eca.maxillary.mma.petrosal.right`

**Description**

Petrosal branches: these arise posteriorly at the level of the [foramen spinosum](#structure-landmark.foramen-spinosum.right) from the proximal horizontal segment. The branches should be protected during embolisation particularly because the superficial petrosal branch passes through the facial nerve canal contributing to the facial arcade to supply the facial nerve. They run medially to supply regional dura mater. The proximal petrosal branch, immediately distal to the [foramen spinosum](#structure-landmark.foramen-spinosum.right), supplies the cavernous sinus, trigeminal nerve, and Gasserian ganglion and anastomoses with the [ILT](#structure-artery.anterior.inferolateral_trunk_right). This artery also supplies the [superior tympanic](#structure-artery.amendment.superior_tympanic.right) cavity and anastomoses in the tympanic cavity with the [caroticotympanic](#structure-artery.anterior.caroticotympanic_right), [superior tympanic](#structure-artery.amendment.superior_tympanic.right) (another petrosal branch supplying the tensor tympani muscle and superior part of the tympanic cavity), [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right), subarcuate (anterior inferior cerebellar branch) arteries, and the tubal branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right). There are also numerous important anastomoses including with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right), tentorial arteries from the inferolateral or MHTs of the [ICA](#structure-artery.anterior.internal_carotid_right), dural branches from the [AICA](#structure-artery.posterior.aica_right) and [ascending pharyngeal artery](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.amendment.superior_tympanic.right"></a>

### Superior tympanic right

**Model ID:** `artery.amendment.superior_tympanic.right`

**Description**

The superior tympanic artery is a [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right) supplying the tensor tympani muscle and superior part of the tympanic cavity.

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right) anastomoses in the tympanic cavity with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right), superior tympanic, and [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) arteries.

**Source:** `nv(2).pdf`, PDF pages 10, 18; printed pages 16, 24.

**Parent:** [MMA petrosal artery right](#structure-artery.eca.maxillary.mma.petrosal.right)

<a id="structure-artery.eca.mma_cavernous.right"></a>

### MMA cavernous artery right

**Model ID:** `artery.eca.mma_cavernous.right`

**Description**

Cavernous sinus branches: anterior and posterior branches originate from the horizontal segment to supply the lateral wall of the cavernous sinus. The anterior branch runs anteromedially to supply the anterior cavernous sinus and anastomoses with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right). The posterior branch is directed posteromedially to supply the posterior cavernous sinus and anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.amendment.mma_anterior_cavernous.right"></a>

### MMA anterior cavernous right

**Model ID:** `artery.amendment.mma_anterior_cavernous.right`

**Description**

The anterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right) arises from its horizontal segment. It runs anteromedially to supply the anterior cavernous sinus and anastomoses with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [MMA cavernous artery right](#structure-artery.eca.mma_cavernous.right)

<a id="structure-artery.amendment.mma_posterior_cavernous.right"></a>

### MMA posterior cavernous right

**Model ID:** `artery.amendment.mma_posterior_cavernous.right`

**Description**

The posterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right) arises from its horizontal segment. It is directed posteromedially to supply the posterior cavernous sinus and anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [MMA cavernous artery right](#structure-artery.eca.mma_cavernous.right)

<a id="structure-artery.eca.mma_orbital.right"></a>

### MMA orbital artery right

**Model ID:** `artery.eca.mma_orbital.right`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right) may be the sole supply of the orbit (the meningo-ophthalmic artery) or supply the lacrimal gland and lateral orbit via a recurrent branch traversing the [foramen of Hyrtl](#structure-landmark.cranio-orbital.right). This latter branch usually also has [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) anastomoses.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery right](#structure-artery.eca.maxillary.mma.right)

<a id="structure-artery.amendment.artery_of_superior_orbital_fissure.right"></a>

### Artery of superior orbital fissure right

**Model ID:** `artery.amendment.artery_of_superior_orbital_fissure.right`

**Description**

Origin: superomedially from the third maxillary segment. It may share a common trunk with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right).

Course: superiorly through the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.right) towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right).

Anastomoses: anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery right](#structure-artery.eca.maxillary.right)

<a id="structure-artery.eca.apa.right"></a>

### Ascending pharyngeal artery right

**Model ID:** `artery.eca.apa.right`

**Description**

Supply: nasopharynx, Eustachian tube, middle ear, oropharynx, soft palate, abducens, glossopharyngeal, vagus, accessory, and hypoglossal nerves.

Origin: this long needle-thin artery arises posteromedially from the proximal [ECA](#structure-artery.carotid.external.right), close to the [occipital artery](#structure-artery.eca.occipital.right) origin, sometimes sharing an origin. It can also arise from a common trunk with the lingual and facial arteries, the carotid bifurcation, internal carotid, or ascending cervical artery. There are numerous potential anastomoses with the vertebrobasilar artery and [ICA](#structure-artery.anterior.internal_carotid_right).

Course: it runs straight up medial to the [ICA](#structure-artery.anterior.internal_carotid_right), giving off small muscular branches before dividing into anterior pharyngeal and posterior neuromeningeal trunks.

**Source:** `nv(2).pdf`, PDF page 12; printed page 18.

**Parent:** [External carotid artery right](#structure-artery.carotid.external.right)

<a id="structure-artery.eca.apa.pharyngeal_trunk.right"></a>

### Pharyngeal trunk right

**Model ID:** `artery.eca.apa.pharyngeal_trunk.right`

**Description**

Superior, middle, and inferior pharyngeal branches: these branches supply the pharyngeal submucosal spaces and contribute to a rich anastomotic network with the contralateral [ascending pharyngeal artery](#structure-artery.eca.apa.right.left) and [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Ascending pharyngeal artery right](#structure-artery.eca.apa.right)

<a id="structure-artery.eca.inferior_pharyngeal.right"></a>

### Inferior pharyngeal artery right

**Model ID:** `artery.eca.inferior_pharyngeal.right`

**Description**

The inferior branch, also of importance in post-tonsillectomy haemorrhage, courses anteroinferiorly and supplies the oropharynx. It may anastomose with the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk right](#structure-artery.eca.apa.pharyngeal_trunk.right)

<a id="structure-artery.eca.middle_pharyngeal.right"></a>

### Middle pharyngeal artery right

**Model ID:** `artery.eca.middle_pharyngeal.right`

**Description**

The middle branch is directed anteromedially and supplies the nasopharynx and soft palate. It is an important source of bleeding in refractory epistaxis and post-tonsillectomy haemorrhage. It may anastomose with the [pterygovaginal](#structure-artery.eca.pterygovaginal.right), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right), and descending and greater palatine arteries.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk right](#structure-artery.eca.apa.pharyngeal_trunk.right)

<a id="structure-artery.eca.superior_pharyngeal.right"></a>

### Superior pharyngeal artery right

**Model ID:** `artery.eca.superior_pharyngeal.right`

**Description**

The superior branch is directed upwards and supplies the nasopharynx and soft palate. It anastomoses with the [artery of the pterygoid canal](#structure-artery.eca.maxillary.pterygoid_canal.right) and middle meningeal and [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right) arteries (from the [IMA](#structure-artery.eca.maxillary.right)), and the vidian and mandibular arteries ([ICA](#structure-artery.anterior.internal_carotid_right) cavernous segment). The superior branch gives off Eustachian tube and carotid branches. The former supplies the Eustachian tube and submucosa of the fossa of Rosenmüller while the latter traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.right) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right) ([inferolateral trunk](#structure-artery.anterior.inferolateral_trunk_right) ([ILT](#structure-artery.anterior.inferolateral_trunk_right)) of the [ICA](#structure-artery.anterior.internal_carotid_right), both ipsilateral and contralateral).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk right](#structure-artery.eca.apa.pharyngeal_trunk.right)

<a id="structure-artery.amendment.superior_pharyngeal_tubal_branch.right"></a>

### Superior pharyngeal tubal branch right

**Model ID:** `artery.amendment.superior_pharyngeal_tubal_branch.right`

**Description**

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) gives off an Eustachian tube branch, which supplies the Eustachian tube and submucosa of the fossa of Rosenmüller.

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [pharyngeal trunk](#structure-artery.eca.apa.pharyngeal_trunk.right) contributes to the Eustachian tube anastomotic circle. It is connected to the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous)’s mandibular and vidian arteries and forms connections with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) and [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right) (distal [IMA](#structure-artery.eca.maxillary.right)). It also sends a branch through the [foramen lacerum](#structure-landmark.foramen-lacerum.right) to the cavernous sinus, joining the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right) and the [ILT](#structure-artery.anterior.inferolateral_trunk_right) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous).

**Source:** `nv(2).pdf`, PDF pages 13, 52; printed pages 19, 58.

**Parent:** [Superior pharyngeal artery right](#structure-artery.eca.superior_pharyngeal.right)

<a id="structure-artery.amendment.superior_pharyngeal_carotid_branch.right"></a>

### Superior pharyngeal carotid branch right

**Model ID:** `artery.amendment.superior_pharyngeal_carotid_branch.right`

**Description**

The carotid branch of the superior pharyngeal artery traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.right) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right) from the [ILT](#structure-artery.anterior.inferolateral_trunk_right) of the [ICA](#structure-artery.anterior.internal_carotid_right), both ipsilateral and contralateral.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Superior pharyngeal artery right](#structure-artery.eca.superior_pharyngeal.right)

<a id="structure-artery.eca.apa.neuromeningeal_trunk.right"></a>

### Neuromeningeal trunk right

**Model ID:** `artery.eca.apa.neuromeningeal_trunk.right`

**Description**

The neuromeningeal trunk is important because of its supply of cranial nerves. It may also arise from the occipital or [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries. The trunk bifurcates into jugular and hypoglossal branches.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Ascending pharyngeal artery right](#structure-artery.eca.apa.right)

<a id="structure-artery.eca.apa.hypoglossal.right"></a>

### Hypoglossal branch right

**Model ID:** `artery.eca.apa.hypoglossal.right`

**Description**

The hypoglossal branch is more posterior, inferior, and medial and enters the cranium through the [hypoglossal canal](#structure-landmark.hypoglossal.right) to supply the hypoglossal nerve and meninges. A medial branch runs over the medial clivus and anastomoses with the [medial clival artery (MHT of the ICA)](#structure-artery.amendment.medial_clival_mht_branch.right). A descending branch anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries. Posterior branches course inferomedially along the floor of the posterior fossa, medially as the [artery of the falx cerebelli](#structure-artery.amendment.falx_cerebelli_artery.right) and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_right). Rarely, the [posterior inferior cerebellar artery](#structure-artery.posterior.pica_right) ([PICA](#structure-artery.posterior.pica_right)) may arise from the hypoglossal artery.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Neuromeningeal trunk right](#structure-artery.eca.apa.neuromeningeal_trunk.right)

<a id="structure-artery.eca.medial_clival.right"></a>

### Medial clival artery right

**Model ID:** `artery.eca.medial_clival.right`

**Description**

A medial branch of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right) runs over the medial clivus and anastomoses with the [medial clival artery from the MHT](#structure-artery.amendment.medial_clival_mht_branch.right) of the [ICA](#structure-artery.anterior.internal_carotid_right).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch right](#structure-artery.eca.apa.hypoglossal.right)

<a id="structure-artery.eca.apa.descending_odontoid.right"></a>

### Odontoid descending artery right

**Model ID:** `artery.eca.apa.descending_odontoid.right`

**Description**

A descending branch of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right) anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch right](#structure-artery.eca.apa.hypoglossal.right)

<a id="structure-artery.eca.apa.posterior_meningeal.right"></a>

### Hypoglossal posterior meningeal artery right

**Model ID:** `artery.eca.apa.posterior_meningeal.right`

**Description**

Posterior branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right) course inferomedially along the floor of the posterior fossa, medially as the [artery of the falx cerebelli](#structure-artery.amendment.falx_cerebelli_artery.right) and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch right](#structure-artery.eca.apa.hypoglossal.right)

<a id="structure-artery.amendment.falx_cerebelli_artery.right"></a>

### Falx cerebelli artery right

**Model ID:** `artery.amendment.falx_cerebelli_artery.right`

**Description**

Posterior branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right) course inferomedially along the floor of the posterior fossa, medially as the artery of the falx cerebelli and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal posterior meningeal artery right](#structure-artery.eca.apa.posterior_meningeal.right)

<a id="structure-artery.eca.apa.jugular.right"></a>

### Jugular branch right

**Model ID:** `artery.eca.apa.jugular.right`

**Description**

The jugular branch is the more superior and lateral division of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right) and enters the cranium through the [jugular foramen](#structure-landmark.jugular-foramen.right).

It supplies the glossopharyngeal, vagus, and accessory nerves in addition to meninges. It has an ascending medial branch that accompanies the inferior petrosal sinus and anastomoses with the [lateral clival artery (meningohypophyseal trunk (MHT))](#structure-artery.amendment.lateral_clival_mht_branch.right). Clival branches also anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_right) and can supply the abducens nerve in Dorello’s canal. A sigmoid branch accompanies the sigmoid and transverse sinuses and anastomoses with the middle meningeal and [occipital arteries](#structure-artery.eca.occipital.right). An additional ascending branch supplies dura mater of the internal auditory canal and may anastomose with the [AICA](#structure-artery.posterior.aica_right). The posterior meningeal artery may originate from the jugular branch.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Neuromeningeal trunk right](#structure-artery.eca.apa.neuromeningeal_trunk.right)

<a id="structure-artery.eca.lateral_clival.right"></a>

### Lateral clival artery right

**Model ID:** `artery.eca.lateral_clival.right`

**Description**

An ascending medial branch of the [jugular artery](#structure-artery.eca.apa.jugular.right) accompanies the inferior petrosal sinus and anastomoses with the [lateral clival artery from the MHT](#structure-artery.amendment.lateral_clival_mht_branch.right). Clival branches also anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_right) and can supply the abducens nerve in Dorello’s canal.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch right](#structure-artery.eca.apa.jugular.right)

<a id="structure-artery.eca.apa.sigmoid_sinus_branch.right"></a>

### Jugular sigmoid branch right

**Model ID:** `artery.eca.apa.sigmoid_sinus_branch.right`

**Description**

A sigmoid branch of the [jugular artery](#structure-artery.eca.apa.jugular.right) accompanies the sigmoid and transverse sinuses and anastomoses with the middle meningeal and [occipital arteries](#structure-artery.eca.occipital.right).

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch right](#structure-artery.eca.apa.jugular.right)

<a id="structure-artery.amendment.jugular_ascending_iac_branch.right"></a>

### Jugular ascending IAC branch right

**Model ID:** `artery.amendment.jugular_ascending_iac_branch.right`

**Description**

An ascending branch of the [jugular artery](#structure-artery.eca.apa.jugular.right) supplies dura mater of the internal auditory canal and may anastomose with the [AICA](#structure-artery.posterior.aica_right).

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch right](#structure-artery.eca.apa.jugular.right)

<a id="structure-artery.eca.apa.inferior_tympanic.right"></a>

### Inferior tympanic artery right

**Model ID:** `artery.eca.apa.inferior_tympanic.right`

**Description**

The inferior tympanic artery branch of the [ascending pharyngeal artery](#structure-artery.eca.apa.right) travels with Jacobson’s nerve through the inferior tympanic foramen, anastomosing with other tympanic ([anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right), [superior tympanic](#structure-artery.amendment.superior_tympanic.right)) and surrounding arteries within the middle ear including the [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_right), a [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) branch.

The [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_right) is normally a tiny branch of the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) but may enlarge and form the anatomical variant of the ‘aberrant [ICA](#structure-artery.anterior.internal_carotid_right)’ in the absence of normal [cervical ICA](#structure-artery.anterior.internal_carotid_right.segment.cervical) development.

**Source:** `nv(2).pdf`, PDF pages 13, 52; printed pages 19, 58.

**Parent:** [Ascending pharyngeal artery right](#structure-artery.eca.apa.right)

<a id="structure-artery.amendment.apa_musculospinal.right"></a>

### APA musculospinal right

**Model ID:** `artery.amendment.apa_musculospinal.right`

**Description**

Musculospinal branch: this passes posteroinferiorly at the C3 level. It supplies the spinal accessory nerve and the superior sympathetic ganglion. Important anastomoses connect with the ascending and deep cervical arteries and [vertebral artery](#structure-artery.posterior.vertebral_right).

The musculospinal branch laterally anastomoses with the C3 radicular anastomotic artery from the [vertebral artery](#structure-artery.posterior.vertebral_right).

**Source:** `nv(2).pdf`, PDF pages 13, 54; printed pages 19, 60.

**Parent:** [Ascending pharyngeal artery right](#structure-artery.eca.apa.right)

<a id="structure-artery.amendment.apa_prevertebral_branch.right"></a>

### APA prevertebral branch right

**Model ID:** `artery.amendment.apa_prevertebral_branch.right`

**Description**

The prevertebral branch, running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_right) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Ascending pharyngeal artery right](#structure-artery.eca.apa.right)

<a id="structure-artery.anterior.internal_carotid_right"></a>

### Internal carotid right

**Model ID:** `artery.anterior.internal_carotid_right`

**Description**

The ICA originates at the bifurcation of the [CCA](#structure-artery.anterior.common_carotid_right). This is usually at C4 but may be as low as T2.

The New York University segmental classification divides the ICA into cervical, petrosal, cavernous, paraophthalmic, communicating, choroidal, and terminal segments.

**Source:** `nv(2).pdf`, PDF page 24; printed page 30.

**Parent:** [Common carotid right](#structure-artery.anterior.common_carotid_right)

<a id="structure-artery.anterior.internal_carotid_right.segment.cervical"></a>

### ICA cervical right

**Model ID:** `artery.anterior.internal_carotid_right.segment.cervical`

**Description**

This begins at the bifurcation of the [CCA](#structure-artery.anterior.common_carotid_right) and ends as the artery enters the [carotid canal](#structure-landmark.carotid-canal.right).

Course: the [ICA](#structure-artery.anterior.internal_carotid_right) is contained within the carotid sheath, anteromedial to the IJV. The [ECA](#structure-artery.carotid.external.right) is also usually anteromedial initially, before it veers laterally. The vagus nerve and the cranial root of the accessory nerve are located posteriorly.

**Source:** `nv(2).pdf`, PDF page 24; printed page 30.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.internal_carotid_right.segment.petrous"></a>

### ICA petrous right

**Model ID:** `artery.anterior.internal_carotid_right.segment.petrous`

**Description**

From the [carotid canal](#structure-landmark.carotid-canal.right) to the petrolingual ligament (approximately the anterior aspect of the petrous ridge).

Course: the segment starts vertically in the [carotid canal](#structure-landmark.carotid-canal.right) before turning anteromedially and running over the cartilage covering the [foramen lacerum](#structure-landmark.foramen-lacerum.right). It is accompanied by sympathetic fibres from the stellate ganglion and a venous plexus.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.caroticotympanic_right"></a>

### Caroticotympanic right

**Model ID:** `artery.anterior.caroticotympanic_right`

**Description**

Caroticotympanic: this small branch (the vestigial remnant of the hyoid artery) enters the middle ear cavity and anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right), the [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right) and [superior tympanic](#structure-artery.amendment.superior_tympanic.right) arteries, and a branch of the [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right). It forms the cranial part of the ‘aberrant [ICA](#structure-artery.anterior.internal_carotid_right)’.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous right](#structure-artery.anterior.internal_carotid_right.segment.petrous)

<a id="structure-artery.anterior.vidian_ica_contribution_right"></a>

### Vidian ICA contribution right

**Model ID:** `artery.anterior.vidian_ica_contribution_right`

**Description**

Mandibulovidian artery: this artery has vidian and mandibular branches, both of which may arise separately from the [ICA](#structure-artery.anterior.internal_carotid_right).

The vidian branch, horizontally orientated, passes anteriorly through the [vidian canal](#structure-landmark.pterygoid-canal.right) and then into the pterygopalatine fossa to meet its counterpart [vidian branch of the IMA](#structure-artery.eca.maxillary.pterygoid_canal.right). The branch is not always visible angiographically but may enlarge in certain situations, e.g., when supplying a juvenile nasopharyngeal angiofibroma.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous right](#structure-artery.anterior.internal_carotid_right.segment.petrous)

<a id="structure-artery.amendment.mandibular_ica_branch.right"></a>

### Mandibular ICA branch right

**Model ID:** `artery.amendment.mandibular_ica_branch.right`

**Description**

The mandibular branch runs anteroinferiorly exiting the temporal bone to supply regional soft tissues and contributes to pharyngeal vascular anastomoses.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous right](#structure-artery.anterior.internal_carotid_right.segment.petrous)

<a id="structure-artery.anterior.internal_carotid_right.segment.cavernous"></a>

### ICA cavernous right

**Model ID:** `artery.anterior.internal_carotid_right.segment.cavernous`

**Description**

From the petrolingual ligament to the proximal dural ring.

Course: the vessel runs superiorly along the [posterior clinoid process](#structure-landmark.ica.posterior-clinoid.right) to the [anterior clinoid process](#structure-landmark.ica.anterior-clinoid.right) before passing through the dural ring. Within the cavernous sinus it lies superomedially to the abducens nerve, and medial to CN III, CN IV, and the ophthalmic and maxillary divisions of CN V and the trigeminal (Gasserian) ganglion.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.meningohypophyseal_trunk_right"></a>

### Meningohypophyseal trunk right

**Model ID:** `artery.anterior.meningohypophyseal_trunk_right`

**Description**

The meningohypophyseal trunk (MHT): this projects posteriorly and laterally from the proximal [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous) to supply the posterior pituitary, clivus, CNs III-VI, the trigeminal ganglion, the tentorium cerebelli, and other adjacent dura mater. It may exist as a single trunk or as multiple branches directly from the [ICA](#structure-artery.anterior.internal_carotid_right) (or, indeed, the [ILT](#structure-artery.anterior.inferolateral_trunk_right)).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [ICA cavernous right](#structure-artery.anterior.internal_carotid_right.segment.cavernous)

<a id="structure-artery.anterior.tentorial_marginal_right"></a>

### Tentorial marginal right

**Model ID:** `artery.anterior.tentorial_marginal_right`

**Description**

The marginal tentorial artery of Bernasconi and Cassinari is a dural vessel that traverses the medial, free, edge of the tentorial leaf towards the torcular.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Meningohypophyseal trunk right](#structure-artery.anterior.meningohypophyseal_trunk_right)

<a id="structure-artery.anterior.dorsal_meningeal_right"></a>

### Dorsal meningeal right

**Model ID:** `artery.anterior.dorsal_meningeal_right`

**Parent:** [Meningohypophyseal trunk right](#structure-artery.anterior.meningohypophyseal_trunk_right)

<a id="structure-artery.amendment.medial_clival_mht_branch.right"></a>

### Medial clival MHT branch right

**Model ID:** `artery.amendment.medial_clival_mht_branch.right`

**Description**

The [posterior inferior hypophyseal artery](#structure-artery.anterior.inferior_hypophyseal_right) gives off an inferior clival artery that anastomoses with clival branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right). The [posterior inferior hypophyseal](#structure-artery.anterior.inferior_hypophyseal_right) and medial clival arteries are remnants of the primitive [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Dorsal meningeal right](#structure-artery.anterior.dorsal_meningeal_right)

<a id="structure-artery.amendment.lateral_clival_mht_branch.right"></a>

### Lateral clival MHT branch right

**Model ID:** `artery.amendment.lateral_clival_mht_branch.right`

**Description**

The lateral clival artery supplies the dura of the clivus. It has lateral and inferolateral branches which follow, respectively, the superior and inferior petrosal sinuses. There are anastomoses with its contralateral counterpart, the [jugular branch](#structure-artery.eca.apa.jugular.right) of the [ascending pharyngeal](#structure-artery.eca.apa.right), and the [MMA](#structure-artery.eca.maxillary.mma.right).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Dorsal meningeal right](#structure-artery.anterior.dorsal_meningeal_right)

<a id="structure-artery.anterior.inferior_hypophyseal_right"></a>

### Inferior hypophyseal right

**Model ID:** `artery.anterior.inferior_hypophyseal_right`

**Description**

The posterior inferior hypophyseal artery: anastomoses with its contralateral counterpart and supplies the posterior (and sometimes part of the anterior) lobe of the pituitary. It gives off an inferior clival artery that anastomoses with clival branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right). The posterior inferior hypophyseal and medial clival arteries are remnants of the primitive [IMA](#structure-artery.eca.maxillary.right) which can persist and enlarge in agenesis of the [cervical ICA](#structure-artery.anterior.internal_carotid_right.segment.cervical), so reconstituting the intracranial carotid circulation.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Meningohypophyseal trunk right](#structure-artery.anterior.meningohypophyseal_trunk_right)

<a id="structure-artery.amendment.basal_tentorial_mht_branch.right"></a>

### Basal tentorial MHT branch right

**Model ID:** `artery.amendment.basal_tentorial_mht_branch.right`

**Description**

The basal (or lateral) tentorial artery, also a dural vessel, courses more laterally and inferiorly along the lateral edge of the tentorium cerebelli and sigmoid sinus and anastomoses with branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), occipital, and [middle meningeal arteries](#structure-artery.eca.maxillary.mma.right).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Meningohypophyseal trunk right](#structure-artery.anterior.meningohypophyseal_trunk_right)

<a id="structure-artery.anterior.inferolateral_trunk_right"></a>

### Inferolateral trunk right

**Model ID:** `artery.anterior.inferolateral_trunk_right`

**Description**

Inferolateral trunk (ILT): originates on the lateral part of the mid-horizontal [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous) and is directed inferiorly. It is an important vascular network connecting the middle meningeal, [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right), internal carotid, ophthalmic, and [ascending pharyngeal](#structure-artery.eca.apa.right) arteries.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [ICA cavernous right](#structure-artery.anterior.internal_carotid_right.segment.cavernous)

<a id="structure-artery.anterior.ilt_anterior_branch_right"></a>

### ILT anteromedial ramus right

**Model ID:** `artery.anterior.ilt_anterior_branch_right`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) as the [deep recurrent ophthalmic artery](#structure-artery.amendment.deep_recurrent_ophthalmic.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk right](#structure-artery.anterior.inferolateral_trunk_right)

<a id="structure-artery.anterior.ilt_posterior_branch_right"></a>

### ILT posterior division (posterolateral continuation) right

**Model ID:** `artery.anterior.ilt_posterior_branch_right`

**Description**

The posterolateral branch supplies the trigeminal ganglion and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) at the [foramen spinosum](#structure-landmark.foramen-spinosum.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk right](#structure-artery.anterior.inferolateral_trunk_right)

<a id="structure-artery.amendment.ilt_posteromedial_ramus.right"></a>

### ILT posteromedial ramus right

**Model ID:** `artery.amendment.ilt_posteromedial_ramus.right`

**Description**

The posteromedial ramus is directed towards the [foramen ovale](#structure-landmark.ovale.right) and anastomoses with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) to supply the abducens nerve, the trigeminal ganglion, and the motor root of CN V.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [ILT posterior division (posterolateral continuation) right](#structure-artery.anterior.ilt_posterior_branch_right)

<a id="structure-artery.amendment.ilt_superior_ramus.right"></a>

### ILT superior ramus right

**Model ID:** `artery.amendment.ilt_superior_ramus.right`

**Description**

The superior branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) veers medially to supply CNs III, IV, and V1 (the ophthalmic division of the trigeminal nerve) in the cavernous sinus.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk right](#structure-artery.anterior.inferolateral_trunk_right)

<a id="structure-artery.amendment.ilt_anterolateral_ramus.right"></a>

### ILT anterolateral ramus right

**Model ID:** `artery.amendment.ilt_anterolateral_ramus.right`

**Description**

The anterolateral ramus, directed laterally over the trochlear nerve and under the ophthalmic division of the trigeminal nerve, enters the [foramen rotundum](#structure-landmark.rotundum.right) to anastomose with the [IMA](#structure-artery.eca.maxillary.right) via the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk right](#structure-artery.anterior.inferolateral_trunk_right)

<a id="structure-artery.amendment.ilt_recurrent_lacerum_ramus.right"></a>

### ILT recurrent lacerum ramus right

**Model ID:** `artery.amendment.ilt_recurrent_lacerum_ramus.right`

**Description**

The recurrent artery of the foramen lacerum, which forms an anastomosis in the [foramen lacerum](#structure-landmark.foramen-lacerum.right) with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk right](#structure-artery.anterior.inferolateral_trunk_right)

<a id="structure-artery.anterior.internal_carotid_right.segment.paraophthalmic"></a>

### ICA paraophthalmic right

**Model ID:** `artery.anterior.internal_carotid_right.segment.paraophthalmic`

**Description**

From the estimated distal border of the cavernous segment, just proximal to the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) ostium, to the ostium of the [PCOM](#structure-artery.anterior.posterior_communicating_right).

This segment incorporates the proximal and distal dural rings (the clinoid [ICA](#structure-artery.anterior.internal_carotid_right) segment); however, the dural anatomy in the anterior clinoid region is complex, variable, and impossible to reliably define on imaging, making it difficult to differentiate intradural and extradural aneurysms in this region.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.ophthalmic_right"></a>

### Ophthalmic right

**Model ID:** `artery.anterior.ophthalmic_right`

**Description**

Ophthalmic artery: originates anteriorly from the [ICA](#structure-artery.anterior.internal_carotid_right) and traverses the orbital canal initially inferolateral and then arching superomedially over the optic nerve, adopting an American Civil War bayonet shape at the origin of the [central artery of the retina](#structure-artery.anterior.central_retinal_right) and posterior choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA paraophthalmic right](#structure-artery.anterior.internal_carotid_right.segment.paraophthalmic)

<a id="structure-artery.anterior.lacrimal_right"></a>

### Lacrimal right

**Model ID:** `artery.anterior.lacrimal_right`

**Description**

Lacrimal artery: laterally placed, supplies the lacrimal gland, eyelids, and conjunctiva. The recurrent meningeal branch courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right). Other anastomoses include branches of the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right) and deep temporal arteries.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.superficial_recurrent_meningeal.right"></a>

### Superficial recurrent meningeal right

**Model ID:** `artery.amendment.superficial_recurrent_meningeal.right`

**Description**

The recurrent meningeal branch of the lacrimal artery courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.amendment.lacrimal_inferior_branch.right"></a>

### Lacrimal inferior branch right

**Model ID:** `artery.amendment.lacrimal_inferior_branch.right`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right) has anastomoses with the inferior branch of the lacrimal artery via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.amendment.lateral_superior_palpebral.right"></a>

### Lateral superior palpebral right

**Model ID:** `artery.amendment.lateral_superior_palpebral.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.amendment.lateral_inferior_palpebral.right"></a>

### Lateral inferior palpebral right

**Model ID:** `artery.amendment.lateral_inferior_palpebral.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.anterior.central_retinal_right"></a>

### Central retinal right

**Model ID:** `artery.anterior.central_retinal_right`

**Description**

The central retinal artery: this, the most important branch, arises within the [optic canal](#structure-landmark.optic-canal.right) and travels alongside the optic nerve to supply the retina. It is a terminal branch without anastomoses and occlusion may result in permanent and severe visual loss.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.posterior_ciliary_medial_right"></a>

### Posterior ciliary medial right

**Model ID:** `artery.anterior.posterior_ciliary_medial_right`

**Description**

The posterior ciliary arteries arise from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) just proximal to the [central retinal artery](#structure-artery.anterior.central_retinal_right). They are responsible for the choroidal blush.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.posterior_ciliary_lateral_right"></a>

### Posterior ciliary lateral right

**Model ID:** `artery.anterior.posterior_ciliary_lateral_right`

**Description**

The posterior ciliary arteries arise from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) just proximal to the [central retinal artery](#structure-artery.anterior.central_retinal_right). They are responsible for the choroidal blush.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.supraorbital_right"></a>

### Supraorbital right

**Model ID:** `artery.anterior.supraorbital_right`

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.supratrochlear_right"></a>

### Supratrochlear right

**Model ID:** `artery.anterior.supratrochlear_right`

**Description**

Supratrochlear artery: supplies the skin of the forehead/scalp, and underlying pericranium and frontalis.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.dorsal_nasal_right"></a>

### Dorsal nasal right

**Model ID:** `artery.anterior.dorsal_nasal_right`

**Description**

Dorsal nasal artery: supplies the lacrimal sac, face, and nose.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.anterior_ethmoidal_right"></a>

### Anterior ethmoidal right

**Model ID:** `artery.anterior.anterior_ethmoidal_right`

**Description**

The anterior ethmoidal artery distributes to the superior nasal septum and into the anterior meningeal branches (the artery of the falx cerebri). The ethmoidal arteries anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.anterior_falcine.right"></a>

### Anterior falcine right

**Model ID:** `artery.amendment.anterior_falcine.right`

**Description**

The anterior falcine artery is a meningeal branch arising from the ethmoidal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

The paramedian terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right) anastomose with the anterior falcine artery from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right).

**Source:** `nv(2).pdf`, PDF pages 19, 53; printed pages 25, 59.

**Parent:** [Anterior ethmoidal right](#structure-artery.anterior.anterior_ethmoidal_right)

<a id="structure-artery.anterior.posterior_ethmoidal_right"></a>

### Posterior ethmoidal right

**Model ID:** `artery.anterior.posterior_ethmoidal_right`

**Description**

The posterior ethmoidal artery distributes to the posterosuperior nasal septum. The ethmoidal arteries anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.ophthalmic_inferior_muscular_branch.right"></a>

### Ophthalmic inferior muscular branch right

**Model ID:** `artery.amendment.ophthalmic_inferior_muscular_branch.right`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) gives off osseous and muscular branches on the orbital floor and anastomoses with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.ophthalmic_superior_muscular_branch.right"></a>

### Ophthalmic superior muscular branch right

**Model ID:** `artery.amendment.ophthalmic_superior_muscular_branch.right`

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.deep_recurrent_ophthalmic.right"></a>

### Deep recurrent ophthalmic right

**Model ID:** `artery.amendment.deep_recurrent_ophthalmic.right`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) as the deep recurrent ophthalmic artery.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.medial_superior_palpebral.right"></a>

### Medial superior palpebral right

**Model ID:** `artery.amendment.medial_superior_palpebral.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.amendment.medial_inferior_palpebral.right"></a>

### Medial inferior palpebral right

**Model ID:** `artery.amendment.medial_inferior_palpebral.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Ophthalmic right](#structure-artery.anterior.ophthalmic_right)

<a id="structure-artery.anterior.superior_hypophyseal_right"></a>

### Superior hypophyseal right

**Model ID:** `artery.anterior.superior_hypophyseal_right`

**Description**

Superior hypophyseal arteries: these small vessels typically arise medially along the [paraophthalmic ICA segment](#structure-artery.anterior.internal_carotid_right.segment.paraophthalmic) and supply the pituitary gland, optic chiasm, and optic nerve and some may supply the hypothalamus. There are anastomoses with their contralateral counterparts and ipsilateral [PCOM](#structure-artery.anterior.posterior_communicating_right).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA paraophthalmic right](#structure-artery.anterior.internal_carotid_right.segment.paraophthalmic)

<a id="structure-artery.anterior.internal_carotid_right.segment.posterior-communicating"></a>

### ICA posterior communicating right

**Model ID:** `artery.anterior.internal_carotid_right.segment.posterior-communicating`

**Description**

From the [PCOM](#structure-artery.anterior.posterior_communicating_right) ostium to the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) ostium.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.posterior_communicating_right"></a>

### Posterior communicating right

**Model ID:** `artery.anterior.posterior_communicating_right`

**Description**

The PCOM insertion defines the PCA P1-P2 segments. Embryonically, the PCOM represents the caudal division of the [ICA](#structure-artery.anterior.internal_carotid_right) (contrasting with the adult description of the [ICA](#structure-artery.anterior.internal_carotid_right) division into the middle cerebral artery (MCA) and anterior cerebral artery (ACA)).

A ‘fetal type’ PCOM, seen in approximately 25%, means the vessel is larger than the P1, or that it supplies most of the flow to the PCA territory. Complete absence of the PCOM is very rare; however, a very hypoplastic vessel may not be appreciated angiographically.

Branches: the PCOM gives off numerous small perforators to the ventral thalamus. These may be present even if the vessel is hypoplastic.

In embryonic development the PCOM is the caudal division of the [ICA](#structure-artery.anterior.internal_carotid_right). As the vertebrobasilar system develops and gives rise to the PCA, the PCOM regresses to a variable degree.

**Source:** `nv(2).pdf`, PDF pages 30, 48; printed pages 36, 54.

**Parent:** [ICA posterior communicating right](#structure-artery.anterior.internal_carotid_right.segment.posterior-communicating)

<a id="structure-artery.amendment.tuberothalamic_artery.right"></a>

### Tuberothalamic artery right

**Model ID:** `artery.amendment.tuberothalamic_artery.right`

**Description**

The tuberothalamic artery is a particularly prominent anterior thalamoperforating artery from the superolateral aspect of the [PCOM](#structure-artery.anterior.posterior_communicating_right). It supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating right](#structure-artery.anterior.posterior_communicating_right)

<a id="structure-artery.amendment.anterior_thalamoperforating_branch.right"></a>

### Anterior thalamoperforating branch right

**Model ID:** `artery.amendment.anterior_thalamoperforating_branch.right`

**Description**

The anterior thalamoperforators of the [PCOM](#structure-artery.anterior.posterior_communicating_right) arise from the superolateral aspect and a particularly prominent one is the [tuberothalamic artery](#structure-artery.amendment.tuberothalamic_artery.right), which supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract. The anterior thalamoperforating group also supply the posterior optic chiasm, proximal optic radiations, posterior hypothalamus, and cerebral peduncle. They anastomose with choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating right](#structure-artery.anterior.posterior_communicating_right)

<a id="structure-artery.anterior.internal_carotid_right.segment.anterior-choroidal"></a>

### ICA anterior choroidal right

**Model ID:** `artery.anterior.internal_carotid_right.segment.anterior-choroidal`

**Description**

From the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) ostium and immediately adjacent.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.anterior_choroidal_right"></a>

### Anterior choroidal right

**Model ID:** `artery.anterior.anterior_choroidal_right`

**Description**

The anterior choroidal artery supplies highly eloquent tissue. It is rarely absent. It usually arises posterolaterally from the [ICA](#structure-artery.anterior.internal_carotid_right), 2-4 mm distal to the origin of the [PCOM](#structure-artery.anterior.posterior_communicating_right). It may uncommonly arise from the MCA, a joint origin with the [PCOM](#structure-artery.anterior.posterior_communicating_right), or the [PCOM](#structure-artery.anterior.posterior_communicating_right) itself. It may also be larger than the [PCOM](#structure-artery.anterior.posterior_communicating_right), and thus occasionally mistaken for this vessel.

The anterior choroidal artery runs posteriorly beneath the optic tract and then around the cerebral peduncle in the carotid, crural, and ambient cisterns before again crossing the optic tract from medial to lateral at the level of the lateral geniculate body. It then enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. Occasionally, it may sweep around the pulvinar to reach the foramen of Monro. It anastomoses with the posterior choroidal artery via its intraventricular terminal branches and also with the middle and posterior cerebral arteries.

The crucial branches are cisternal. They supply the optic tract, cerebral peduncle (corticospinal tracts, red nucleus, subthalamus), the posterior limb of the internal capsule, the optic radiation, the lateral geniculate body, proximal optic radiations, the hippocampus, the amygdala, the uncus, dentate gyrus, piriform cortex, globus pallidus, and the ventral thalamic nuclei. Although a small artery, its occlusion may cause significant neurological deficit, including contralateral hemiplegia, contralateral hemisensory loss, contralateral homonymous hemianopia, hemineglect, and aphasia.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [ICA anterior choroidal right](#structure-artery.anterior.internal_carotid_right.segment.anterior-choroidal)

<a id="structure-artery.amendment.acha_optic_tract_branch.right"></a>

### AChA optic tract branch right

**Model ID:** `artery.amendment.acha_optic_tract_branch.right`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) supply the optic tract, optic radiation, and lateral geniculate body.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.amendment.acha_capsular_branch.right"></a>

### AChA capsular branch right

**Model ID:** `artery.amendment.acha_capsular_branch.right`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) supply the posterior limb of the internal capsule.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.amendment.acha_peduncular_branch.right"></a>

### AChA peduncular branch right

**Model ID:** `artery.amendment.acha_peduncular_branch.right`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) supply the cerebral peduncle, including the corticospinal tracts, red nucleus, and subthalamus.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.amendment.acha_temporal_branch.right"></a>

### AChA temporal branch right

**Model ID:** `artery.amendment.acha_temporal_branch.right`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) supply the hippocampus, amygdala, uncus, dentate gyrus, and piriform cortex.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.amendment.anterior_choroidal_plexal_representative.right"></a>

### Anterior choroidal plexal representative right

**Model ID:** `artery.amendment.anterior_choroidal_plexal_representative.right`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. Occasionally, it may sweep around the pulvinar to reach the foramen of Monro. It anastomoses with the posterior choroidal artery via its intraventricular terminal branches.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.anterior.internal_carotid_right.segment.terminus"></a>

### ICA terminus right

**Model ID:** `artery.anterior.internal_carotid_right.segment.terminus`

**Description**

From just distal to the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) to the [ICA](#structure-artery.anterior.internal_carotid_right) bifurcation.

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [Internal carotid right](#structure-artery.anterior.internal_carotid_right)

<a id="structure-artery.anterior.aca_a1_right"></a>

### ACA A1 right

**Model ID:** `artery.anterior.aca_a1_right`

**Description**

The A1 segment is directed forwards and medially above the optic nerve and chiasm towards the anterior interhemispheric fissure.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [ICA terminus right](#structure-artery.anterior.internal_carotid_right.segment.terminus)

<a id="structure-artery.anterior.aca_pericallosal_right"></a>

### ACA pericallosal right

**Model ID:** `artery.anterior.aca_pericallosal_right`

**Description**

The A2 segment arises distal to the [ACOM](#structure-artery.anterior.anterior_communicating) and extends to the junction of the rostrum and genu of the corpus callosum.

The A3 segment extends around the genu of the corpus callosum.

Segments inclusive of and distal to the A3 are generally called the pericallosal artery, although sometimes the A2 segment is also referred to as such. Small perforating branches supply the corpus callosum and the callosal arteries, and these traverse the corpus callosum to supply the septum, anterior pillars of the fornix, and anterior commissure. Distally, there are anastomoses with the [posterior pericallosal branch of the PCA](#structure-artery.posterior.pca_splenial_right) via perisplenial branches.

The A4 segment originates at the body of the corpus callosum and the A5 segment is the continuation of the vessel posterior to the coronal suture.

**Source:** `nv(2).pdf`, PDF pages 36–37; printed pages 42–43.

**Parent:** [ACA A1 right](#structure-artery.anterior.aca_a1_right)

<a id="structure-artery.anterior.recurrent_artery_of_heubner_right"></a>

### Recurrent artery of Heubner right

**Model ID:** `artery.anterior.recurrent_artery_of_heubner_right`

**Description**

The recurrent artery of Heubner: the largest laterally projecting perforating branch arising from the A1 or proximal A2 segment, travelling above the A1 and M1 segments, supplies the anterior hypothalamus, anteroinferior caudate head, anterior lentiform nucleus, and the anterior limb of the internal capsule. It is optimally demonstrated angiographically by a contralateral carotid injection. It is in haemodynamic balance with the [medial lenticulostriates](#structure-artery.anterior.medial_lenticulostriate_right).

**Source:** `nv(2).pdf`, PDF pages 34–35; printed pages 40–41.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.aca_orbitofrontal_right"></a>

### ACA orbitofrontal right

**Model ID:** `artery.anterior.aca_orbitofrontal_right`

**Description**

The orbitofrontal artery: arising proximally and coursing anteriorly in the interhemispheric fissure to supply the gyrus rectus, olfactory bulb, and inferior frontal lobe.

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.aca_frontopolar_right"></a>

### ACA frontopolar right

**Model ID:** `artery.anterior.aca_frontopolar_right`

**Description**

The frontopolar artery: this arises just proximal to the genu of the corpus callosum to supply the frontal cortex.

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.callosomarginal_right"></a>

### Callosomarginal right

**Model ID:** `artery.anterior.callosomarginal_right`

**Description**

The callosomarginal artery is the major branch of the A3 segment and runs parallel to the vessel inside the cingulate sulcus. It may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right). It gives off four arteries that supply the medial frontal lobe: the anterior, middle, and posterior internal frontal arteries, and the [paracentral artery](#structure-artery.anterior.paracentral_right).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.anterior_internal_frontal_right"></a>

### Anterior internal frontal right

**Model ID:** `artery.anterior.anterior_internal_frontal_right`

**Description**

The anterior internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal right](#structure-artery.anterior.callosomarginal_right)

<a id="structure-artery.anterior.middle_internal_frontal_right"></a>

### Middle internal frontal right

**Model ID:** `artery.anterior.middle_internal_frontal_right`

**Description**

The middle internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal right](#structure-artery.anterior.callosomarginal_right)

<a id="structure-artery.anterior.posterior_internal_frontal_right"></a>

### Posterior internal frontal right

**Model ID:** `artery.anterior.posterior_internal_frontal_right`

**Description**

The posterior internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal right](#structure-artery.anterior.callosomarginal_right)

<a id="structure-artery.anterior.paracentral_right"></a>

### Paracentral right

**Model ID:** `artery.anterior.paracentral_right`

**Description**

The paracentral artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_right) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.precuneal_right"></a>

### Precuneal right

**Model ID:** `artery.anterior.precuneal_right`

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.inferior_internal_parietal_right"></a>

### Inferior internal parietal right

**Model ID:** `artery.anterior.inferior_internal_parietal_right`

**Description**

Parietal branches of the A4 and A5 segments supply the medial parietal lobe. There may be distinct superior and inferior branches.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.amendment.short_callosal_branch.right"></a>

### Short callosal branch right

**Model ID:** `artery.amendment.short_callosal_branch.right`

**Description**

Short callosal perforating arteries: supplying the pillars of the fornix and the anterior commissure.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.amendment.long_callosal_branch.right"></a>

### Long callosal branch right

**Model ID:** `artery.amendment.long_callosal_branch.right`

**Description**

Long callosal arteries: supplying adjacent cortex.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.amendment.aca_falcine_branch.right"></a>

### ACA falcine branch right

**Model ID:** `artery.amendment.aca_falcine_branch.right`

**Description**

Dural branches: supplying the falx.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

<a id="structure-artery.anterior.medial_lenticulostriate_right"></a>

### Medial lenticulostriate right

**Model ID:** `artery.anterior.medial_lenticulostriate_right`

**Description**

Medial lenticulostriate arteries: superior branches supply the anterior basal ganglia, anterior commissure, and anterior limb of the internal capsule. Medial branches supply the anterior aspect of the lateral wall of the third ventricle, hypothalamus, and septum pellucidum. Inferior branches infiltrate the optic nerves and chiasm. They vary in size and number.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [ACA A1 right](#structure-artery.anterior.aca_a1_right)

<a id="structure-artery.amendment.medial_lenticulostriate_superior_representative.right"></a>

### Medial lenticulostriate superior representative right

**Model ID:** `artery.amendment.medial_lenticulostriate_superior_representative.right`

**Description**

The superior branches of the [medial lenticulostriate arteries](#structure-artery.anterior.medial_lenticulostriate_right) supply the anterior basal ganglia, anterior commissure, and anterior limb of the internal capsule.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [Medial lenticulostriate right](#structure-artery.anterior.medial_lenticulostriate_right)

<a id="structure-artery.amendment.acom_hypothalamic_perforator.right"></a>

### ACom hypothalamic perforator right

**Model ID:** `artery.amendment.acom_hypothalamic_perforator.right`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the hypothalamus.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.amendment.acom_septal_perforator.right"></a>

### ACom septal perforator right

**Model ID:** `artery.amendment.acom_septal_perforator.right`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the septum pellucidum.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.amendment.acom_chiasmatic_perforator.right"></a>

### ACom chiasmatic perforator right

**Model ID:** `artery.amendment.acom_chiasmatic_perforator.right`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the optic chiasm.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.anterior.mca_m1_right"></a>

### MCA M1 right

**Model ID:** `artery.anterior.mca_m1_right`

**Description**

The M1 segment runs horizontally from the termination of the [ICA](#structure-artery.anterior.internal_carotid_right) to the limen insulae (the anteroinferior insular and lateral limit of the anterior perforated substance), along the sphenoid wing.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [ICA terminus right](#structure-artery.anterior.internal_carotid_right.segment.terminus)

<a id="structure-artery.anterior.mca_superior_division_right"></a>

### MCA superior division right

**Model ID:** `artery.anterior.mca_superior_division_right`

**Description**

The artery usually divides into two trunks, although a single trunk, trifurcation, or quadrifurcation are all possible. Superior and inferior divisions are usually referred to. It is slightly more common for the inferior division to be dominant, covering the temporal and parietal lobes while the superior division tends to supply the frontal lobe. With superior dominance, its territory may extend to the angular gyrus and temporo-occipital regions.

The branches angulate superiorly and course in the Sylvian fissure lateral to the insular cortex.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.anterior.mca_orbitofrontal_right"></a>

### MCA orbitofrontal right

**Model ID:** `artery.anterior.mca_orbitofrontal_right`

**Description**

The orbitofrontal artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division right](#structure-artery.anterior.mca_superior_division_right)

<a id="structure-artery.anterior.prefrontal_right"></a>

### Prefrontal right

**Model ID:** `artery.anterior.prefrontal_right`

**Parent:** [MCA superior division right](#structure-artery.anterior.mca_superior_division_right)

<a id="structure-artery.anterior.prefrontal_cortical_branch_right"></a>

### Prefrontal cortical branch right

**Model ID:** `artery.anterior.prefrontal_cortical_branch_right`

**Parent:** [Prefrontal right](#structure-artery.anterior.prefrontal_right)

<a id="structure-artery.amendment.prefrontal_distal_ramus.right"></a>

### Prefrontal distal ramus right

**Model ID:** `artery.amendment.prefrontal_distal_ramus.right`

**Parent:** [Prefrontal right](#structure-artery.anterior.prefrontal_right)

<a id="structure-artery.anterior.precentral_right"></a>

### Precentral right

**Model ID:** `artery.anterior.precentral_right`

**Description**

The precentral artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division right](#structure-artery.anterior.mca_superior_division_right)

<a id="structure-artery.anterior.precentral_cortical_branch_right"></a>

### Precentral cortical branch right

**Model ID:** `artery.anterior.precentral_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The precentral artery is one of the frontal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Precentral right](#structure-artery.anterior.precentral_right)

<a id="structure-artery.amendment.precentral_distal_ramus.right"></a>

### Precentral distal ramus right

**Model ID:** `artery.amendment.precentral_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The precentral artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Precentral right](#structure-artery.anterior.precentral_right)

<a id="structure-artery.anterior.central_right"></a>

### Central right

**Model ID:** `artery.anterior.central_right`

**Description**

The central artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division right](#structure-artery.anterior.mca_superior_division_right)

<a id="structure-artery.anterior.central_cortical_branch_right"></a>

### Central cortical branch right

**Model ID:** `artery.anterior.central_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The central artery is one of the frontal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Central right](#structure-artery.anterior.central_right)

<a id="structure-artery.amendment.central_distal_ramus.right"></a>

### Central distal ramus right

**Model ID:** `artery.amendment.central_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The central artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Central right](#structure-artery.anterior.central_right)

<a id="structure-artery.anterior.mca_inferior_division_right"></a>

### MCA inferior division right

**Model ID:** `artery.anterior.mca_inferior_division_right`

**Description**

The artery usually divides into two trunks, although a single trunk, trifurcation, or quadrifurcation are all possible. Superior and inferior divisions are usually referred to. It is slightly more common for the inferior division to be dominant, covering the temporal and parietal lobes while the superior division tends to supply the frontal lobe. With superior dominance, its territory may extend to the angular gyrus and temporo-occipital regions.

The branches angulate superiorly and course in the Sylvian fissure lateral to the insular cortex.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.anterior.anterior_parietal_right"></a>

### Anterior parietal right

**Model ID:** `artery.anterior.anterior_parietal_right`

**Description**

The anterior parietal artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.anterior_parietal_cortical_branch_right"></a>

### Anterior parietal cortical branch right

**Model ID:** `artery.anterior.anterior_parietal_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The anterior parietal artery is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Anterior parietal right](#structure-artery.anterior.anterior_parietal_right)

<a id="structure-artery.amendment.anterior_parietal_distal_ramus.right"></a>

### Anterior parietal distal ramus right

**Model ID:** `artery.amendment.anterior_parietal_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The anterior parietal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Anterior parietal right](#structure-artery.anterior.anterior_parietal_right)

<a id="structure-artery.anterior.posterior_parietal_right"></a>

### Posterior parietal right

**Model ID:** `artery.anterior.posterior_parietal_right`

**Description**

The posterior parietal artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.posterior_parietal_cortical_branch_right"></a>

### Posterior parietal cortical branch right

**Model ID:** `artery.anterior.posterior_parietal_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior parietal artery is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior parietal right](#structure-artery.anterior.posterior_parietal_right)

<a id="structure-artery.amendment.posterior_parietal_distal_ramus.right"></a>

### Posterior parietal distal ramus right

**Model ID:** `artery.amendment.posterior_parietal_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior parietal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior parietal right](#structure-artery.anterior.posterior_parietal_right)

<a id="structure-artery.anterior.angular_right"></a>

### Angular right

**Model ID:** `artery.anterior.angular_right`

**Description**

The angular artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.angular_cortical_branch_right"></a>

### Angular cortical branch right

**Model ID:** `artery.anterior.angular_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The [angular artery](#structure-artery.anterior.angular_right) is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Angular right](#structure-artery.anterior.angular_right)

<a id="structure-artery.amendment.angular_distal_ramus.right"></a>

### Angular distal ramus right

**Model ID:** `artery.amendment.angular_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The [angular artery](#structure-artery.anterior.angular_right) is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Angular right](#structure-artery.anterior.angular_right)

<a id="structure-artery.anterior.temporo_occipital_right"></a>

### Temporo-occipital right

**Model ID:** `artery.anterior.temporo_occipital_right`

**Description**

The temporo [occipital artery](#structure-artery.eca.occipital.right) is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.middle_temporal_right"></a>

### Middle temporal right

**Model ID:** `artery.anterior.middle_temporal_right`

**Description**

The middle temporal artery is one of the temporal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.middle_temporal_cortical_branch_right"></a>

### Middle temporal cortical branch right

**Model ID:** `artery.anterior.middle_temporal_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The middle temporal artery is one of the temporal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Middle temporal right](#structure-artery.anterior.middle_temporal_right)

<a id="structure-artery.amendment.middle_temporal_distal_ramus.right"></a>

### Middle temporal distal ramus right

**Model ID:** `artery.amendment.middle_temporal_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The middle temporal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Middle temporal right](#structure-artery.anterior.middle_temporal_right)

<a id="structure-artery.anterior.posterior_temporal_right"></a>

### Posterior temporal right

**Model ID:** `artery.anterior.posterior_temporal_right`

**Description**

The posterior temporal artery is one of the temporal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.posterior_temporal_cortical_branch_right"></a>

### Posterior temporal cortical branch right

**Model ID:** `artery.anterior.posterior_temporal_cortical_branch_right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior temporal artery is one of the temporal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior temporal right](#structure-artery.anterior.posterior_temporal_right)

<a id="structure-artery.amendment.posterior_temporal_distal_ramus.right"></a>

### Posterior temporal distal ramus right

**Model ID:** `artery.amendment.posterior_temporal_distal_ramus.right`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior temporal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior temporal right](#structure-artery.anterior.posterior_temporal_right)

<a id="structure-artery.amendment.polar_temporal.right"></a>

### Polar temporal right

**Model ID:** `artery.amendment.polar_temporal.right`

**Description**

The polar temporal artery is one of the temporal cortical branches of the MCA. These branches are named after the regions they supply.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division right](#structure-artery.anterior.mca_inferior_division_right)

<a id="structure-artery.anterior.anterior_temporal_right"></a>

### Anterior temporal right

**Model ID:** `artery.anterior.anterior_temporal_right`

**Description**

Anterior temporal artery: this usually arises inferiorly from the middle of the M1 and supplies the anterior third of the superior, middle, and inferior temporal gyri.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.anterior.lateral_lenticulostriate_1_right"></a>

### Lateral lenticulostriate 1 right

**Model ID:** `artery.anterior.lateral_lenticulostriate_1_right`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.amendment.lateral_lenticulostriate_anterior_representative.right"></a>

### Lateral lenticulostriate anterior representative right

**Model ID:** `artery.amendment.lateral_lenticulostriate_anterior_representative.right`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [Lateral lenticulostriate 1 right](#structure-artery.anterior.lateral_lenticulostriate_1_right)

<a id="structure-artery.anterior.lateral_lenticulostriate_2_right"></a>

### Lateral lenticulostriate 2 right

**Model ID:** `artery.anterior.lateral_lenticulostriate_2_right`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.anterior.lateral_lenticulostriate_3_right"></a>

### Lateral lenticulostriate 3 right

**Model ID:** `artery.anterior.lateral_lenticulostriate_3_right`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 right](#structure-artery.anterior.mca_m1_right)

<a id="structure-artery.amendment.terminal_ica_perforator_1.right"></a>

### Terminal ICA perforator 1 right

**Model ID:** `artery.amendment.terminal_ica_perforator_1.right`

**Description**

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [ICA terminus right](#structure-artery.anterior.internal_carotid_right.segment.terminus)

<a id="structure-artery.amendment.terminal_ica_perforator_2.right"></a>

### Terminal ICA perforator 2 right

**Model ID:** `artery.amendment.terminal_ica_perforator_2.right`

**Description**

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [ICA terminus right](#structure-artery.anterior.internal_carotid_right.segment.terminus)

<a id="carotid-left"></a>

## Carotid arteries and branches, left

<a id="structure-artery.amendment.acom_hypothalamic_perforator.left"></a>

### ACom hypothalamic perforator left

**Model ID:** `artery.amendment.acom_hypothalamic_perforator.left`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the hypothalamus.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.amendment.acom_septal_perforator.left"></a>

### ACom septal perforator left

**Model ID:** `artery.amendment.acom_septal_perforator.left`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the septum pellucidum.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.amendment.acom_chiasmatic_perforator.left"></a>

### ACom chiasmatic perforator left

**Model ID:** `artery.amendment.acom_chiasmatic_perforator.left`

**Description**

Multiple small perforating branches arise from the [ACOM](#structure-artery.anterior.anterior_communicating). Their supply includes the optic chiasm.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.anterior.common_carotid_left"></a>

### Common carotid left

**Model ID:** `artery.anterior.common_carotid_left`

**Description**

The left CCA arises just distal to the brachiocephalic artery from the aortic arch. It ascends posteriorly and laterally before bifurcating into its internal and external branches.

**Source:** `nv(2).pdf`, PDF page 4; printed page 10.

**Parent:** [Arteries](#structure-artery)

<a id="structure-artery.anterior.internal_carotid_left"></a>

### Internal carotid left

**Model ID:** `artery.anterior.internal_carotid_left`

**Description**

The ICA originates at the bifurcation of the [CCA](#structure-artery.anterior.common_carotid_left). This is usually at C4 but may be as low as T2.

The New York University segmental classification divides the ICA into cervical, petrosal, cavernous, paraophthalmic, communicating, choroidal, and terminal segments.

**Source:** `nv(2).pdf`, PDF page 24; printed page 30.

**Parent:** [Common carotid left](#structure-artery.anterior.common_carotid_left)

<a id="structure-artery.anterior.internal_carotid_left.segment.cervical"></a>

### ICA cervical left

**Model ID:** `artery.anterior.internal_carotid_left.segment.cervical`

**Description**

This begins at the bifurcation of the [CCA](#structure-artery.anterior.common_carotid_left) and ends as the artery enters the [carotid canal](#structure-landmark.carotid-canal.left).

Course: the [ICA](#structure-artery.anterior.internal_carotid_left) is contained within the carotid sheath, anteromedial to the IJV. The [ECA](#structure-artery.carotid.external.right.left) is also usually anteromedial initially, before it veers laterally. The vagus nerve and the cranial root of the accessory nerve are located posteriorly.

**Source:** `nv(2).pdf`, PDF page 24; printed page 30.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.internal_carotid_left.segment.petrous"></a>

### ICA petrous left

**Model ID:** `artery.anterior.internal_carotid_left.segment.petrous`

**Description**

From the [carotid canal](#structure-landmark.carotid-canal.left) to the petrolingual ligament (approximately the anterior aspect of the petrous ridge).

Course: the segment starts vertically in the [carotid canal](#structure-landmark.carotid-canal.left) before turning anteromedially and running over the cartilage covering the [foramen lacerum](#structure-landmark.foramen-lacerum.left). It is accompanied by sympathetic fibres from the stellate ganglion and a venous plexus.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.caroticotympanic_left"></a>

### Caroticotympanic left

**Model ID:** `artery.anterior.caroticotympanic_left`

**Description**

Caroticotympanic: this small branch (the vestigial remnant of the hyoid artery) enters the middle ear cavity and anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), the [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left) and [superior tympanic](#structure-artery.amendment.superior_tympanic.left) arteries, and a branch of the [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right.left). It forms the cranial part of the ‘aberrant [ICA](#structure-artery.anterior.internal_carotid_left)’.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous left](#structure-artery.anterior.internal_carotid_left.segment.petrous)

<a id="structure-artery.anterior.vidian_ica_contribution_left"></a>

### Vidian ICA contribution left

**Model ID:** `artery.anterior.vidian_ica_contribution_left`

**Description**

Mandibulovidian artery: this artery has vidian and mandibular branches, both of which may arise separately from the [ICA](#structure-artery.anterior.internal_carotid_left).

The vidian branch, horizontally orientated, passes anteriorly through the [vidian canal](#structure-landmark.pterygoid-canal.left) and then into the pterygopalatine fossa to meet its counterpart [vidian branch of the IMA](#structure-artery.eca.maxillary.pterygoid_canal.right.left). The branch is not always visible angiographically but may enlarge in certain situations, e.g., when supplying a juvenile nasopharyngeal angiofibroma.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous left](#structure-artery.anterior.internal_carotid_left.segment.petrous)

<a id="structure-artery.amendment.mandibular_ica_branch.left"></a>

### Mandibular ICA branch left

**Model ID:** `artery.amendment.mandibular_ica_branch.left`

**Description**

The mandibular branch runs anteroinferiorly exiting the temporal bone to supply regional soft tissues and contributes to pharyngeal vascular anastomoses.

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [ICA petrous left](#structure-artery.anterior.internal_carotid_left.segment.petrous)

<a id="structure-artery.anterior.internal_carotid_left.segment.cavernous"></a>

### ICA cavernous left

**Model ID:** `artery.anterior.internal_carotid_left.segment.cavernous`

**Description**

From the petrolingual ligament to the proximal dural ring.

Course: the vessel runs superiorly along the [posterior clinoid process](#structure-landmark.ica.posterior-clinoid.left) to the [anterior clinoid process](#structure-landmark.ica.anterior-clinoid.left) before passing through the dural ring. Within the cavernous sinus it lies superomedially to the abducens nerve, and medial to CN III, CN IV, and the ophthalmic and maxillary divisions of CN V and the trigeminal (Gasserian) ganglion.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.meningohypophyseal_trunk_left"></a>

### Meningohypophyseal trunk left

**Model ID:** `artery.anterior.meningohypophyseal_trunk_left`

**Description**

The meningohypophyseal trunk (MHT): this projects posteriorly and laterally from the proximal [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous) to supply the posterior pituitary, clivus, CNs III-VI, the trigeminal ganglion, the tentorium cerebelli, and other adjacent dura mater. It may exist as a single trunk or as multiple branches directly from the [ICA](#structure-artery.anterior.internal_carotid_left) (or, indeed, the [ILT](#structure-artery.anterior.inferolateral_trunk_left)).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [ICA cavernous left](#structure-artery.anterior.internal_carotid_left.segment.cavernous)

<a id="structure-artery.anterior.tentorial_marginal_left"></a>

### Tentorial marginal left

**Model ID:** `artery.anterior.tentorial_marginal_left`

**Description**

The marginal tentorial artery of Bernasconi and Cassinari is a dural vessel that traverses the medial, free, edge of the tentorial leaf towards the torcular.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Meningohypophyseal trunk left](#structure-artery.anterior.meningohypophyseal_trunk_left)

<a id="structure-artery.anterior.dorsal_meningeal_left"></a>

### Dorsal meningeal left

**Model ID:** `artery.anterior.dorsal_meningeal_left`

**Parent:** [Meningohypophyseal trunk left](#structure-artery.anterior.meningohypophyseal_trunk_left)

<a id="structure-artery.amendment.medial_clival_mht_branch.left"></a>

### Medial clival MHT branch left

**Model ID:** `artery.amendment.medial_clival_mht_branch.left`

**Description**

The [posterior inferior hypophyseal artery](#structure-artery.anterior.inferior_hypophyseal_left) gives off an inferior clival artery that anastomoses with clival branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left). The [posterior inferior hypophyseal](#structure-artery.anterior.inferior_hypophyseal_left) and medial clival arteries are remnants of the primitive [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Dorsal meningeal left](#structure-artery.anterior.dorsal_meningeal_left)

<a id="structure-artery.amendment.lateral_clival_mht_branch.left"></a>

### Lateral clival MHT branch left

**Model ID:** `artery.amendment.lateral_clival_mht_branch.left`

**Description**

The lateral clival artery supplies the dura of the clivus. It has lateral and inferolateral branches which follow, respectively, the superior and inferior petrosal sinuses. There are anastomoses with its contralateral counterpart, the [jugular branch](#structure-artery.eca.apa.jugular.right.left) of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), and the [MMA](#structure-artery.eca.maxillary.mma.right.left).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Dorsal meningeal left](#structure-artery.anterior.dorsal_meningeal_left)

<a id="structure-artery.anterior.inferior_hypophyseal_left"></a>

### Inferior hypophyseal left

**Model ID:** `artery.anterior.inferior_hypophyseal_left`

**Description**

The posterior inferior hypophyseal artery: anastomoses with its contralateral counterpart and supplies the posterior (and sometimes part of the anterior) lobe of the pituitary. It gives off an inferior clival artery that anastomoses with clival branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left). The posterior inferior hypophyseal and medial clival arteries are remnants of the primitive [IMA](#structure-artery.eca.maxillary.right.left) which can persist and enlarge in agenesis of the [cervical ICA](#structure-artery.anterior.internal_carotid_left.segment.cervical), so reconstituting the intracranial carotid circulation.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Meningohypophyseal trunk left](#structure-artery.anterior.meningohypophyseal_trunk_left)

<a id="structure-artery.amendment.basal_tentorial_mht_branch.left"></a>

### Basal tentorial MHT branch left

**Model ID:** `artery.amendment.basal_tentorial_mht_branch.left`

**Description**

The basal (or lateral) tentorial artery, also a dural vessel, courses more laterally and inferiorly along the lateral edge of the tentorium cerebelli and sigmoid sinus and anastomoses with branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), occipital, and [middle meningeal arteries](#structure-artery.eca.maxillary.mma.right.left).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Meningohypophyseal trunk left](#structure-artery.anterior.meningohypophyseal_trunk_left)

<a id="structure-artery.anterior.inferolateral_trunk_left"></a>

### Inferolateral trunk left

**Model ID:** `artery.anterior.inferolateral_trunk_left`

**Description**

Inferolateral trunk (ILT): originates on the lateral part of the mid-horizontal [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous) and is directed inferiorly. It is an important vascular network connecting the middle meningeal, [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left), internal carotid, ophthalmic, and [ascending pharyngeal](#structure-artery.eca.apa.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [ICA cavernous left](#structure-artery.anterior.internal_carotid_left.segment.cavernous)

<a id="structure-artery.anterior.ilt_anterior_branch_left"></a>

### ILT anteromedial ramus left

**Model ID:** `artery.anterior.ilt_anterior_branch_left`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) as the [deep recurrent ophthalmic artery](#structure-artery.amendment.deep_recurrent_ophthalmic.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk left](#structure-artery.anterior.inferolateral_trunk_left)

<a id="structure-artery.anterior.ilt_posterior_branch_left"></a>

### ILT posterior division (posterolateral continuation) left

**Model ID:** `artery.anterior.ilt_posterior_branch_left`

**Description**

The posterolateral branch supplies the trigeminal ganglion and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) at the [foramen spinosum](#structure-landmark.foramen-spinosum.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk left](#structure-artery.anterior.inferolateral_trunk_left)

<a id="structure-artery.amendment.ilt_posteromedial_ramus.left"></a>

### ILT posteromedial ramus left

**Model ID:** `artery.amendment.ilt_posteromedial_ramus.left`

**Description**

The posteromedial ramus is directed towards the [foramen ovale](#structure-landmark.ovale.left) and anastomoses with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) to supply the abducens nerve, the trigeminal ganglion, and the motor root of CN V.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [ILT posterior division (posterolateral continuation) left](#structure-artery.anterior.ilt_posterior_branch_left)

<a id="structure-artery.amendment.ilt_superior_ramus.left"></a>

### ILT superior ramus left

**Model ID:** `artery.amendment.ilt_superior_ramus.left`

**Description**

The superior branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) veers medially to supply CNs III, IV, and V1 (the ophthalmic division of the trigeminal nerve) in the cavernous sinus.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk left](#structure-artery.anterior.inferolateral_trunk_left)

<a id="structure-artery.amendment.ilt_anterolateral_ramus.left"></a>

### ILT anterolateral ramus left

**Model ID:** `artery.amendment.ilt_anterolateral_ramus.left`

**Description**

The anterolateral ramus, directed laterally over the trochlear nerve and under the ophthalmic division of the trigeminal nerve, enters the [foramen rotundum](#structure-landmark.rotundum.left) to anastomose with the [IMA](#structure-artery.eca.maxillary.right.left) via the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk left](#structure-artery.anterior.inferolateral_trunk_left)

<a id="structure-artery.amendment.ilt_recurrent_lacerum_ramus.left"></a>

### ILT recurrent lacerum ramus left

**Model ID:** `artery.amendment.ilt_recurrent_lacerum_ramus.left`

**Description**

The recurrent artery of the foramen lacerum, which forms an anastomosis in the [foramen lacerum](#structure-landmark.foramen-lacerum.left) with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Inferolateral trunk left](#structure-artery.anterior.inferolateral_trunk_left)

<a id="structure-artery.anterior.internal_carotid_left.segment.paraophthalmic"></a>

### ICA paraophthalmic left

**Model ID:** `artery.anterior.internal_carotid_left.segment.paraophthalmic`

**Description**

From the estimated distal border of the cavernous segment, just proximal to the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) ostium, to the ostium of the [PCOM](#structure-artery.anterior.posterior_communicating_left).

This segment incorporates the proximal and distal dural rings (the clinoid [ICA](#structure-artery.anterior.internal_carotid_left) segment); however, the dural anatomy in the anterior clinoid region is complex, variable, and impossible to reliably define on imaging, making it difficult to differentiate intradural and extradural aneurysms in this region.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.ophthalmic_left"></a>

### Ophthalmic left

**Model ID:** `artery.anterior.ophthalmic_left`

**Description**

Ophthalmic artery: originates anteriorly from the [ICA](#structure-artery.anterior.internal_carotid_left) and traverses the orbital canal initially inferolateral and then arching superomedially over the optic nerve, adopting an American Civil War bayonet shape at the origin of the [central artery of the retina](#structure-artery.anterior.central_retinal_left) and posterior choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA paraophthalmic left](#structure-artery.anterior.internal_carotid_left.segment.paraophthalmic)

<a id="structure-artery.anterior.lacrimal_left"></a>

### Lacrimal left

**Model ID:** `artery.anterior.lacrimal_left`

**Description**

Lacrimal artery: laterally placed, supplies the lacrimal gland, eyelids, and conjunctiva. The recurrent meningeal branch courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right.left). Other anastomoses include branches of the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left) and deep temporal arteries.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.superficial_recurrent_meningeal.left"></a>

### Superficial recurrent meningeal left

**Model ID:** `artery.amendment.superficial_recurrent_meningeal.left`

**Description**

The recurrent meningeal branch of the lacrimal artery courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right.left).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.amendment.lacrimal_inferior_branch.left"></a>

### Lacrimal inferior branch left

**Model ID:** `artery.amendment.lacrimal_inferior_branch.left`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right.left) has anastomoses with the inferior branch of the lacrimal artery via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right.left) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.amendment.lateral_superior_palpebral.left"></a>

### Lateral superior palpebral left

**Model ID:** `artery.amendment.lateral_superior_palpebral.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.amendment.lateral_inferior_palpebral.left"></a>

### Lateral inferior palpebral left

**Model ID:** `artery.amendment.lateral_inferior_palpebral.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.anterior.central_retinal_left"></a>

### Central retinal left

**Model ID:** `artery.anterior.central_retinal_left`

**Description**

The central retinal artery: this, the most important branch, arises within the [optic canal](#structure-landmark.optic-canal.left) and travels alongside the optic nerve to supply the retina. It is a terminal branch without anastomoses and occlusion may result in permanent and severe visual loss.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.posterior_ciliary_medial_left"></a>

### Posterior ciliary medial left

**Model ID:** `artery.anterior.posterior_ciliary_medial_left`

**Description**

The posterior ciliary arteries arise from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) just proximal to the [central retinal artery](#structure-artery.anterior.central_retinal_left). They are responsible for the choroidal blush.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.posterior_ciliary_lateral_left"></a>

### Posterior ciliary lateral left

**Model ID:** `artery.anterior.posterior_ciliary_lateral_left`

**Description**

The posterior ciliary arteries arise from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) just proximal to the [central retinal artery](#structure-artery.anterior.central_retinal_left). They are responsible for the choroidal blush.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.supraorbital_left"></a>

### Supraorbital left

**Model ID:** `artery.anterior.supraorbital_left`

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.supratrochlear_left"></a>

### Supratrochlear left

**Model ID:** `artery.anterior.supratrochlear_left`

**Description**

Supratrochlear artery: supplies the skin of the forehead/scalp, and underlying pericranium and frontalis.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.dorsal_nasal_left"></a>

### Dorsal nasal left

**Model ID:** `artery.anterior.dorsal_nasal_left`

**Description**

Dorsal nasal artery: supplies the lacrimal sac, face, and nose.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.anterior_ethmoidal_left"></a>

### Anterior ethmoidal left

**Model ID:** `artery.anterior.anterior_ethmoidal_left`

**Description**

The anterior ethmoidal artery distributes to the superior nasal septum and into the anterior meningeal branches (the artery of the falx cerebri). The ethmoidal arteries anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.anterior_falcine.left"></a>

### Anterior falcine left

**Model ID:** `artery.amendment.anterior_falcine.left`

**Description**

The anterior falcine artery is a meningeal branch arising from the ethmoidal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

The paramedian terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left) anastomose with the anterior falcine artery from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left).

**Source:** `nv(2).pdf`, PDF pages 19, 53; printed pages 25, 59.

**Parent:** [Anterior ethmoidal left](#structure-artery.anterior.anterior_ethmoidal_left)

<a id="structure-artery.anterior.posterior_ethmoidal_left"></a>

### Posterior ethmoidal left

**Model ID:** `artery.anterior.posterior_ethmoidal_left`

**Description**

The posterior ethmoidal artery distributes to the posterosuperior nasal septum. The ethmoidal arteries anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.ophthalmic_inferior_muscular_branch.left"></a>

### Ophthalmic inferior muscular branch left

**Model ID:** `artery.amendment.ophthalmic_inferior_muscular_branch.left`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) gives off osseous and muscular branches on the orbital floor and anastomoses with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.ophthalmic_superior_muscular_branch.left"></a>

### Ophthalmic superior muscular branch left

**Model ID:** `artery.amendment.ophthalmic_superior_muscular_branch.left`

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.deep_recurrent_ophthalmic.left"></a>

### Deep recurrent ophthalmic left

**Model ID:** `artery.amendment.deep_recurrent_ophthalmic.left`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) as the deep recurrent ophthalmic artery.

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.medial_superior_palpebral.left"></a>

### Medial superior palpebral left

**Model ID:** `artery.amendment.medial_superior_palpebral.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.amendment.medial_inferior_palpebral.left"></a>

### Medial inferior palpebral left

**Model ID:** `artery.amendment.medial_inferior_palpebral.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Ophthalmic left](#structure-artery.anterior.ophthalmic_left)

<a id="structure-artery.anterior.superior_hypophyseal_left"></a>

### Superior hypophyseal left

**Model ID:** `artery.anterior.superior_hypophyseal_left`

**Description**

Superior hypophyseal arteries: these small vessels typically arise medially along the [paraophthalmic ICA segment](#structure-artery.anterior.internal_carotid_left.segment.paraophthalmic) and supply the pituitary gland, optic chiasm, and optic nerve and some may supply the hypothalamus. There are anastomoses with their contralateral counterparts and ipsilateral [PCOM](#structure-artery.anterior.posterior_communicating_left).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA paraophthalmic left](#structure-artery.anterior.internal_carotid_left.segment.paraophthalmic)

<a id="structure-artery.anterior.internal_carotid_left.segment.posterior-communicating"></a>

### ICA posterior communicating left

**Model ID:** `artery.anterior.internal_carotid_left.segment.posterior-communicating`

**Description**

From the [PCOM](#structure-artery.anterior.posterior_communicating_left) ostium to the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) ostium.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.posterior_communicating_left"></a>

### Posterior communicating left

**Model ID:** `artery.anterior.posterior_communicating_left`

**Description**

The PCOM insertion defines the PCA P1-P2 segments. Embryonically, the PCOM represents the caudal division of the [ICA](#structure-artery.anterior.internal_carotid_left) (contrasting with the adult description of the [ICA](#structure-artery.anterior.internal_carotid_left) division into the middle cerebral artery (MCA) and anterior cerebral artery (ACA)).

A ‘fetal type’ PCOM, seen in approximately 25%, means the vessel is larger than the P1, or that it supplies most of the flow to the PCA territory. Complete absence of the PCOM is very rare; however, a very hypoplastic vessel may not be appreciated angiographically.

Branches: the PCOM gives off numerous small perforators to the ventral thalamus. These may be present even if the vessel is hypoplastic.

In embryonic development the PCOM is the caudal division of the [ICA](#structure-artery.anterior.internal_carotid_left). As the vertebrobasilar system develops and gives rise to the PCA, the PCOM regresses to a variable degree.

**Source:** `nv(2).pdf`, PDF pages 30, 48; printed pages 36, 54.

**Parent:** [ICA posterior communicating left](#structure-artery.anterior.internal_carotid_left.segment.posterior-communicating)

<a id="structure-artery.amendment.tuberothalamic_artery.left"></a>

### Tuberothalamic artery left

**Model ID:** `artery.amendment.tuberothalamic_artery.left`

**Description**

The tuberothalamic artery is a particularly prominent anterior thalamoperforating artery from the superolateral aspect of the [PCOM](#structure-artery.anterior.posterior_communicating_left). It supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating left](#structure-artery.anterior.posterior_communicating_left)

<a id="structure-artery.amendment.anterior_thalamoperforating_branch.left"></a>

### Anterior thalamoperforating branch left

**Model ID:** `artery.amendment.anterior_thalamoperforating_branch.left`

**Description**

The anterior thalamoperforators of the [PCOM](#structure-artery.anterior.posterior_communicating_left) arise from the superolateral aspect and a particularly prominent one is the [tuberothalamic artery](#structure-artery.amendment.tuberothalamic_artery.left), which supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract. The anterior thalamoperforating group also supply the posterior optic chiasm, proximal optic radiations, posterior hypothalamus, and cerebral peduncle. They anastomose with choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating left](#structure-artery.anterior.posterior_communicating_left)

<a id="structure-artery.anterior.internal_carotid_left.segment.anterior-choroidal"></a>

### ICA anterior choroidal left

**Model ID:** `artery.anterior.internal_carotid_left.segment.anterior-choroidal`

**Description**

From the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) ostium and immediately adjacent.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.anterior_choroidal_left"></a>

### Anterior choroidal left

**Model ID:** `artery.anterior.anterior_choroidal_left`

**Description**

The anterior choroidal artery supplies highly eloquent tissue. It is rarely absent. It usually arises posterolaterally from the [ICA](#structure-artery.anterior.internal_carotid_left), 2-4 mm distal to the origin of the [PCOM](#structure-artery.anterior.posterior_communicating_left). It may uncommonly arise from the MCA, a joint origin with the [PCOM](#structure-artery.anterior.posterior_communicating_left), or the [PCOM](#structure-artery.anterior.posterior_communicating_left) itself. It may also be larger than the [PCOM](#structure-artery.anterior.posterior_communicating_left), and thus occasionally mistaken for this vessel.

The anterior choroidal artery runs posteriorly beneath the optic tract and then around the cerebral peduncle in the carotid, crural, and ambient cisterns before again crossing the optic tract from medial to lateral at the level of the lateral geniculate body. It then enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. Occasionally, it may sweep around the pulvinar to reach the foramen of Monro. It anastomoses with the posterior choroidal artery via its intraventricular terminal branches and also with the middle and posterior cerebral arteries.

The crucial branches are cisternal. They supply the optic tract, cerebral peduncle (corticospinal tracts, red nucleus, subthalamus), the posterior limb of the internal capsule, the optic radiation, the lateral geniculate body, proximal optic radiations, the hippocampus, the amygdala, the uncus, dentate gyrus, piriform cortex, globus pallidus, and the ventral thalamic nuclei. Although a small artery, its occlusion may cause significant neurological deficit, including contralateral hemiplegia, contralateral hemisensory loss, contralateral homonymous hemianopia, hemineglect, and aphasia.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [ICA anterior choroidal left](#structure-artery.anterior.internal_carotid_left.segment.anterior-choroidal)

<a id="structure-artery.amendment.acha_optic_tract_branch.left"></a>

### AChA optic tract branch left

**Model ID:** `artery.amendment.acha_optic_tract_branch.left`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) supply the optic tract, optic radiation, and lateral geniculate body.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.amendment.acha_capsular_branch.left"></a>

### AChA capsular branch left

**Model ID:** `artery.amendment.acha_capsular_branch.left`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) supply the posterior limb of the internal capsule.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.amendment.acha_peduncular_branch.left"></a>

### AChA peduncular branch left

**Model ID:** `artery.amendment.acha_peduncular_branch.left`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) supply the cerebral peduncle, including the corticospinal tracts, red nucleus, and subthalamus.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.amendment.acha_temporal_branch.left"></a>

### AChA temporal branch left

**Model ID:** `artery.amendment.acha_temporal_branch.left`

**Description**

The cisternal branches of the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) supply the hippocampus, amygdala, uncus, dentate gyrus, and piriform cortex.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.amendment.anterior_choroidal_plexal_representative.left"></a>

### Anterior choroidal plexal representative left

**Model ID:** `artery.amendment.anterior_choroidal_plexal_representative.left`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. Occasionally, it may sweep around the pulvinar to reach the foramen of Monro. It anastomoses with the posterior choroidal artery via its intraventricular terminal branches.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.anterior.internal_carotid_left.segment.terminus"></a>

### ICA terminus left

**Model ID:** `artery.anterior.internal_carotid_left.segment.terminus`

**Description**

From just distal to the [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) to the [ICA](#structure-artery.anterior.internal_carotid_left) bifurcation.

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [Internal carotid left](#structure-artery.anterior.internal_carotid_left)

<a id="structure-artery.anterior.aca_a1_left"></a>

### ACA A1 left

**Model ID:** `artery.anterior.aca_a1_left`

**Description**

The A1 segment is directed forwards and medially above the optic nerve and chiasm towards the anterior interhemispheric fissure.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [ICA terminus left](#structure-artery.anterior.internal_carotid_left.segment.terminus)

<a id="structure-artery.anterior.aca_pericallosal_left"></a>

### ACA pericallosal left

**Model ID:** `artery.anterior.aca_pericallosal_left`

**Description**

The A2 segment arises distal to the [ACOM](#structure-artery.anterior.anterior_communicating) and extends to the junction of the rostrum and genu of the corpus callosum.

The A3 segment extends around the genu of the corpus callosum.

Segments inclusive of and distal to the A3 are generally called the pericallosal artery, although sometimes the A2 segment is also referred to as such. Small perforating branches supply the corpus callosum and the callosal arteries, and these traverse the corpus callosum to supply the septum, anterior pillars of the fornix, and anterior commissure. Distally, there are anastomoses with the [posterior pericallosal branch of the PCA](#structure-artery.posterior.pca_splenial_left) via perisplenial branches.

The A4 segment originates at the body of the corpus callosum and the A5 segment is the continuation of the vessel posterior to the coronal suture.

**Source:** `nv(2).pdf`, PDF pages 36–37; printed pages 42–43.

**Parent:** [ACA A1 left](#structure-artery.anterior.aca_a1_left)

<a id="structure-artery.anterior.recurrent_artery_of_heubner_left"></a>

### Recurrent artery of Heubner left

**Model ID:** `artery.anterior.recurrent_artery_of_heubner_left`

**Description**

The recurrent artery of Heubner: the largest laterally projecting perforating branch arising from the A1 or proximal A2 segment, travelling above the A1 and M1 segments, supplies the anterior hypothalamus, anteroinferior caudate head, anterior lentiform nucleus, and the anterior limb of the internal capsule. It is optimally demonstrated angiographically by a contralateral carotid injection. It is in haemodynamic balance with the [medial lenticulostriates](#structure-artery.anterior.medial_lenticulostriate_left).

**Source:** `nv(2).pdf`, PDF pages 34–35; printed pages 40–41.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.aca_orbitofrontal_left"></a>

### ACA orbitofrontal left

**Model ID:** `artery.anterior.aca_orbitofrontal_left`

**Description**

The orbitofrontal artery: arising proximally and coursing anteriorly in the interhemispheric fissure to supply the gyrus rectus, olfactory bulb, and inferior frontal lobe.

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.aca_frontopolar_left"></a>

### ACA frontopolar left

**Model ID:** `artery.anterior.aca_frontopolar_left`

**Description**

The frontopolar artery: this arises just proximal to the genu of the corpus callosum to supply the frontal cortex.

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.callosomarginal_left"></a>

### Callosomarginal left

**Model ID:** `artery.anterior.callosomarginal_left`

**Description**

The callosomarginal artery is the major branch of the A3 segment and runs parallel to the vessel inside the cingulate sulcus. It may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left). It gives off four arteries that supply the medial frontal lobe: the anterior, middle, and posterior internal frontal arteries, and the [paracentral artery](#structure-artery.anterior.paracentral_left).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.anterior_internal_frontal_left"></a>

### Anterior internal frontal left

**Model ID:** `artery.anterior.anterior_internal_frontal_left`

**Description**

The anterior internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal left](#structure-artery.anterior.callosomarginal_left)

<a id="structure-artery.anterior.middle_internal_frontal_left"></a>

### Middle internal frontal left

**Model ID:** `artery.anterior.middle_internal_frontal_left`

**Description**

The middle internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal left](#structure-artery.anterior.callosomarginal_left)

<a id="structure-artery.anterior.posterior_internal_frontal_left"></a>

### Posterior internal frontal left

**Model ID:** `artery.anterior.posterior_internal_frontal_left`

**Description**

The posterior internal frontal artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [Callosomarginal left](#structure-artery.anterior.callosomarginal_left)

<a id="structure-artery.anterior.paracentral_left"></a>

### Paracentral left

**Model ID:** `artery.anterior.paracentral_left`

**Description**

The paracentral artery is one of four branches of the [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) supplying the medial frontal lobe. The [callosomarginal artery](#structure-artery.anterior.callosomarginal_left) may be absent, with its branches arising directly from the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 36; printed page 42.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.precuneal_left"></a>

### Precuneal left

**Model ID:** `artery.anterior.precuneal_left`

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.inferior_internal_parietal_left"></a>

### Inferior internal parietal left

**Model ID:** `artery.anterior.inferior_internal_parietal_left`

**Description**

Parietal branches of the A4 and A5 segments supply the medial parietal lobe. There may be distinct superior and inferior branches.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.amendment.short_callosal_branch.left"></a>

### Short callosal branch left

**Model ID:** `artery.amendment.short_callosal_branch.left`

**Description**

Short callosal perforating arteries: supplying the pillars of the fornix and the anterior commissure.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.amendment.long_callosal_branch.left"></a>

### Long callosal branch left

**Model ID:** `artery.amendment.long_callosal_branch.left`

**Description**

Long callosal arteries: supplying adjacent cortex.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.amendment.aca_falcine_branch.left"></a>

### ACA falcine branch left

**Model ID:** `artery.amendment.aca_falcine_branch.left`

**Description**

Dural branches: supplying the falx.

**Source:** `nv(2).pdf`, PDF page 37; printed page 43.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

<a id="structure-artery.anterior.medial_lenticulostriate_left"></a>

### Medial lenticulostriate left

**Model ID:** `artery.anterior.medial_lenticulostriate_left`

**Description**

Medial lenticulostriate arteries: superior branches supply the anterior basal ganglia, anterior commissure, and anterior limb of the internal capsule. Medial branches supply the anterior aspect of the lateral wall of the third ventricle, hypothalamus, and septum pellucidum. Inferior branches infiltrate the optic nerves and chiasm. They vary in size and number.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [ACA A1 left](#structure-artery.anterior.aca_a1_left)

<a id="structure-artery.amendment.medial_lenticulostriate_superior_representative.left"></a>

### Medial lenticulostriate superior representative left

**Model ID:** `artery.amendment.medial_lenticulostriate_superior_representative.left`

**Description**

The superior branches of the [medial lenticulostriate arteries](#structure-artery.anterior.medial_lenticulostriate_left) supply the anterior basal ganglia, anterior commissure, and anterior limb of the internal capsule.

**Source:** `nv(2).pdf`, PDF page 34; printed page 40.

**Parent:** [Medial lenticulostriate left](#structure-artery.anterior.medial_lenticulostriate_left)

<a id="structure-artery.anterior.mca_m1_left"></a>

### MCA M1 left

**Model ID:** `artery.anterior.mca_m1_left`

**Description**

The M1 segment runs horizontally from the termination of the [ICA](#structure-artery.anterior.internal_carotid_left) to the limen insulae (the anteroinferior insular and lateral limit of the anterior perforated substance), along the sphenoid wing.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [ICA terminus left](#structure-artery.anterior.internal_carotid_left.segment.terminus)

<a id="structure-artery.anterior.mca_superior_division_left"></a>

### MCA superior division left

**Model ID:** `artery.anterior.mca_superior_division_left`

**Description**

The artery usually divides into two trunks, although a single trunk, trifurcation, or quadrifurcation are all possible. Superior and inferior divisions are usually referred to. It is slightly more common for the inferior division to be dominant, covering the temporal and parietal lobes while the superior division tends to supply the frontal lobe. With superior dominance, its territory may extend to the angular gyrus and temporo-occipital regions.

The branches angulate superiorly and course in the Sylvian fissure lateral to the insular cortex.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.anterior.mca_orbitofrontal_left"></a>

### MCA orbitofrontal left

**Model ID:** `artery.anterior.mca_orbitofrontal_left`

**Description**

The orbitofrontal artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division left](#structure-artery.anterior.mca_superior_division_left)

<a id="structure-artery.anterior.prefrontal_left"></a>

### Prefrontal left

**Model ID:** `artery.anterior.prefrontal_left`

**Parent:** [MCA superior division left](#structure-artery.anterior.mca_superior_division_left)

<a id="structure-artery.anterior.prefrontal_cortical_branch_left"></a>

### Prefrontal cortical branch left

**Model ID:** `artery.anterior.prefrontal_cortical_branch_left`

**Parent:** [Prefrontal left](#structure-artery.anterior.prefrontal_left)

<a id="structure-artery.amendment.prefrontal_distal_ramus.left"></a>

### Prefrontal distal ramus left

**Model ID:** `artery.amendment.prefrontal_distal_ramus.left`

**Parent:** [Prefrontal left](#structure-artery.anterior.prefrontal_left)

<a id="structure-artery.anterior.precentral_left"></a>

### Precentral left

**Model ID:** `artery.anterior.precentral_left`

**Description**

The precentral artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division left](#structure-artery.anterior.mca_superior_division_left)

<a id="structure-artery.anterior.precentral_cortical_branch_left"></a>

### Precentral cortical branch left

**Model ID:** `artery.anterior.precentral_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The precentral artery is one of the frontal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Precentral left](#structure-artery.anterior.precentral_left)

<a id="structure-artery.amendment.precentral_distal_ramus.left"></a>

### Precentral distal ramus left

**Model ID:** `artery.amendment.precentral_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The precentral artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Precentral left](#structure-artery.anterior.precentral_left)

<a id="structure-artery.anterior.central_left"></a>

### Central left

**Model ID:** `artery.anterior.central_left`

**Description**

The central artery is one of the frontal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA superior division left](#structure-artery.anterior.mca_superior_division_left)

<a id="structure-artery.anterior.central_cortical_branch_left"></a>

### Central cortical branch left

**Model ID:** `artery.anterior.central_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The central artery is one of the frontal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Central left](#structure-artery.anterior.central_left)

<a id="structure-artery.amendment.central_distal_ramus.left"></a>

### Central distal ramus left

**Model ID:** `artery.amendment.central_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The central artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Central left](#structure-artery.anterior.central_left)

<a id="structure-artery.anterior.mca_inferior_division_left"></a>

### MCA inferior division left

**Model ID:** `artery.anterior.mca_inferior_division_left`

**Description**

The artery usually divides into two trunks, although a single trunk, trifurcation, or quadrifurcation are all possible. Superior and inferior divisions are usually referred to. It is slightly more common for the inferior division to be dominant, covering the temporal and parietal lobes while the superior division tends to supply the frontal lobe. With superior dominance, its territory may extend to the angular gyrus and temporo-occipital regions.

The branches angulate superiorly and course in the Sylvian fissure lateral to the insular cortex.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.anterior.anterior_parietal_left"></a>

### Anterior parietal left

**Model ID:** `artery.anterior.anterior_parietal_left`

**Description**

The anterior parietal artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.anterior_parietal_cortical_branch_left"></a>

### Anterior parietal cortical branch left

**Model ID:** `artery.anterior.anterior_parietal_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The anterior parietal artery is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Anterior parietal left](#structure-artery.anterior.anterior_parietal_left)

<a id="structure-artery.amendment.anterior_parietal_distal_ramus.left"></a>

### Anterior parietal distal ramus left

**Model ID:** `artery.amendment.anterior_parietal_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The anterior parietal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Anterior parietal left](#structure-artery.anterior.anterior_parietal_left)

<a id="structure-artery.anterior.posterior_parietal_left"></a>

### Posterior parietal left

**Model ID:** `artery.anterior.posterior_parietal_left`

**Description**

The posterior parietal artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.posterior_parietal_cortical_branch_left"></a>

### Posterior parietal cortical branch left

**Model ID:** `artery.anterior.posterior_parietal_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior parietal artery is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior parietal left](#structure-artery.anterior.posterior_parietal_left)

<a id="structure-artery.amendment.posterior_parietal_distal_ramus.left"></a>

### Posterior parietal distal ramus left

**Model ID:** `artery.amendment.posterior_parietal_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior parietal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior parietal left](#structure-artery.anterior.posterior_parietal_left)

<a id="structure-artery.anterior.angular_left"></a>

### Angular left

**Model ID:** `artery.anterior.angular_left`

**Description**

The angular artery is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.angular_cortical_branch_left"></a>

### Angular cortical branch left

**Model ID:** `artery.anterior.angular_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The [angular artery](#structure-artery.anterior.angular_left) is one of the parieto-occipital branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Angular left](#structure-artery.anterior.angular_left)

<a id="structure-artery.amendment.angular_distal_ramus.left"></a>

### Angular distal ramus left

**Model ID:** `artery.amendment.angular_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The [angular artery](#structure-artery.anterior.angular_left) is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Angular left](#structure-artery.anterior.angular_left)

<a id="structure-artery.anterior.temporo_occipital_left"></a>

### Temporo-occipital left

**Model ID:** `artery.anterior.temporo_occipital_left`

**Description**

The temporo [occipital artery](#structure-artery.eca.occipital.right.left) is one of the parieto-occipital branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.middle_temporal_left"></a>

### Middle temporal left

**Model ID:** `artery.anterior.middle_temporal_left`

**Description**

The middle temporal artery is one of the temporal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.middle_temporal_cortical_branch_left"></a>

### Middle temporal cortical branch left

**Model ID:** `artery.anterior.middle_temporal_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The middle temporal artery is one of the temporal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Middle temporal left](#structure-artery.anterior.middle_temporal_left)

<a id="structure-artery.amendment.middle_temporal_distal_ramus.left"></a>

### Middle temporal distal ramus left

**Model ID:** `artery.amendment.middle_temporal_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The middle temporal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Middle temporal left](#structure-artery.anterior.middle_temporal_left)

<a id="structure-artery.anterior.posterior_temporal_left"></a>

### Posterior temporal left

**Model ID:** `artery.anterior.posterior_temporal_left`

**Description**

The posterior temporal artery is one of the temporal branches of the MCA. The cortical branches are named after the regions they supply.

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.posterior_temporal_cortical_branch_left"></a>

### Posterior temporal cortical branch left

**Model ID:** `artery.anterior.posterior_temporal_cortical_branch_left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior temporal artery is one of the temporal branches, named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior temporal left](#structure-artery.anterior.posterior_temporal_left)

<a id="structure-artery.amendment.posterior_temporal_distal_ramus.left"></a>

### Posterior temporal distal ramus left

**Model ID:** `artery.amendment.posterior_temporal_distal_ramus.left`

**Description**

The M4 (cortical) segments commence at the opercular turn and run on the surface of the cerebral convexity. The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex.

The posterior temporal artery is named after the region it supplies.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [Posterior temporal left](#structure-artery.anterior.posterior_temporal_left)

<a id="structure-artery.amendment.polar_temporal.left"></a>

### Polar temporal left

**Model ID:** `artery.amendment.polar_temporal.left`

**Description**

The polar temporal artery is one of the temporal cortical branches of the MCA. These branches are named after the regions they supply.

**Source:** `nv(2).pdf`, PDF page 40; printed page 46.

**Parent:** [MCA inferior division left](#structure-artery.anterior.mca_inferior_division_left)

<a id="structure-artery.anterior.anterior_temporal_left"></a>

### Anterior temporal left

**Model ID:** `artery.anterior.anterior_temporal_left`

**Description**

Anterior temporal artery: this usually arises inferiorly from the middle of the M1 and supplies the anterior third of the superior, middle, and inferior temporal gyri.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.anterior.lateral_lenticulostriate_1_left"></a>

### Lateral lenticulostriate 1 left

**Model ID:** `artery.anterior.lateral_lenticulostriate_1_left`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.amendment.lateral_lenticulostriate_anterior_representative.left"></a>

### Lateral lenticulostriate anterior representative left

**Model ID:** `artery.amendment.lateral_lenticulostriate_anterior_representative.left`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [Lateral lenticulostriate 1 left](#structure-artery.anterior.lateral_lenticulostriate_1_left)

<a id="structure-artery.anterior.lateral_lenticulostriate_2_left"></a>

### Lateral lenticulostriate 2 left

**Model ID:** `artery.anterior.lateral_lenticulostriate_2_left`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.anterior.lateral_lenticulostriate_3_left"></a>

### Lateral lenticulostriate 3 left

**Model ID:** `artery.anterior.lateral_lenticulostriate_3_left`

**Description**

Lenticulostriate arteries (between 1 and 20, average 10) arise from the superior surface of this segment and perforate the anterior perforated substance. The medial group supplies the globus pallidus and lentiform nucleus. The lateral group supplies the anterior commissure, internal capsule, and upper head and body of the caudate nucleus, putamen, globus pallidus, and substantia innominata. They have an S-shape configuration on the right, and reverse S-shape on the left. The medial group may also arise from the A1 and the latter group may arise from the M2 segments.

**Source:** `nv(2).pdf`, PDF page 38; printed page 44.

**Parent:** [MCA M1 left](#structure-artery.anterior.mca_m1_left)

<a id="structure-artery.amendment.terminal_ica_perforator_1.left"></a>

### Terminal ICA perforator 1 left

**Model ID:** `artery.amendment.terminal_ica_perforator_1.left`

**Description**

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [ICA terminus left](#structure-artery.anterior.internal_carotid_left.segment.terminus)

<a id="structure-artery.amendment.terminal_ica_perforator_2.left"></a>

### Terminal ICA perforator 2 left

**Model ID:** `artery.amendment.terminal_ica_perforator_2.left`

**Description**

This segment contains a variable number of perforating arteries to the anterior perforating substance, which contribute to the collateral reconstitution in Moyamoya disease. Anastomoses are found with the posterior choroidal arteries and ACA.

**Source:** `nv(2).pdf`, PDF page 31; printed page 37.

**Parent:** [ICA terminus left](#structure-artery.anterior.internal_carotid_left.segment.terminus)

<a id="structure-artery.carotid.external.right.left"></a>

### External carotid artery left

**Model ID:** `artery.carotid.external.right.left`

**Description**

The ECA arises from the [CCA](#structure-artery.anterior.common_carotid_left), typically at the level of the C4 vertebra (varying from C2 to T2). In 75%, the [internal carotid artery](#structure-artery.anterior.internal_carotid_left) ([ICA](#structure-artery.anterior.internal_carotid_left)) lies posterolateral to the ECA.

It supplies structures of the head, neck, and face, including muscles, skin, and bones, as well as the pharynx, oral cavity, larynx, thyroid gland, cranial nerves (CNs), and dura mater.

Near its origin, the inferiorly directed [superior thyroid artery](#structure-artery.eca.superior_thyroid.right.left) arises.

The ECA then runs superiorly towards the parotid gland, giving off the lingual and facial arteries anteriorly, and the occipital, [ascending pharyngeal](#structure-artery.eca.apa.right.left), and [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries posterosuperiorly.

It bifurcates into the [superficial temporal artery](#structure-artery.eca.superficial_temporal.right.left) ([STA](#structure-artery.eca.superficial_temporal.right.left)) and [internal maxillary artery](#structure-artery.eca.maxillary.right.left) ([IMA](#structure-artery.eca.maxillary.right.left)) after piercing the parotid gland, behind the neck of the mandible.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [Common carotid left](#structure-artery.anterior.common_carotid_left)

<a id="structure-artery.eca.superior_thyroid.right.left"></a>

### Superior thyroid artery left

**Model ID:** `artery.eca.superior_thyroid.right.left`

**Description**

Supply: upper thyroid gland, infrahyoid, sternocleidomastoid, and cricothyroid muscles, superior larynx, and the parathyroids. It has rich anastomoses with the inferior thyroid branch of the thyrocervical trunk.

Origin: anteriorly at the origin of the [ECA](#structure-artery.carotid.external.right.left). Occasionally it originates from the [CCA](#structure-artery.anterior.common_carotid_left) and rarely from a common origin with the [lingual artery](#structure-artery.eca.lingual.right.left).

Course: it is directed acutely downward and continues lateral to the larynx before reaching the thyroid gland.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.superior_laryngeal.right.left"></a>

### Superior laryngeal artery left

**Model ID:** `artery.eca.superior_laryngeal.right.left`

**Parent:** [Superior thyroid artery left](#structure-artery.eca.superior_thyroid.right.left)

<a id="structure-artery.eca.infrahyoid.right.left"></a>

### Infrahyoid artery left

**Model ID:** `artery.eca.infrahyoid.right.left`

**Parent:** [Superior thyroid artery left](#structure-artery.eca.superior_thyroid.right.left)

<a id="structure-artery.amendment.superior_thyroid_scm_branch.left"></a>

### Superior thyroid SCM branch left

**Model ID:** `artery.amendment.superior_thyroid_scm_branch.left`

**Parent:** [Superior thyroid artery left](#structure-artery.eca.superior_thyroid.right.left)

<a id="structure-artery.amendment.cricothyroid.left"></a>

### Cricothyroid left

**Model ID:** `artery.amendment.cricothyroid.left`

**Parent:** [Superior thyroid artery left](#structure-artery.eca.superior_thyroid.right.left)

<a id="structure-artery.eca.lingual.right.left"></a>

### Lingual artery left

**Model ID:** `artery.eca.lingual.right.left`

**Description**

Supply: ipsilateral tongue and buccal and oral mucosa. It can also supply the submandibular and sublingual salivary glands.

Origin: the lingual artery originates anteriorly from the [ECA](#structure-artery.carotid.external.right.left) just below the [facial artery](#structure-artery.eca.facial.right.left), although it occasionally shares a common origin. Rarely, it can share a common origin with the [superior thyroid](#structure-artery.eca.superior_thyroid.right.left).

Course: initially, anterosuperior to the greater horn of the hyoid, it then turns inferiorly and then anteriorly, crossed by the hypoglossal nerve. It then runs horizontally along the hyoid before diving under the hyoglossus.

**Source:** `nv(2).pdf`, PDF page 6; printed page 12.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.deep_lingual.right.left"></a>

### Deep lingual artery left

**Model ID:** `artery.eca.deep_lingual.right.left`

**Parent:** [Lingual artery left](#structure-artery.eca.lingual.right.left)

<a id="structure-artery.eca.dorsal_lingual.right.left"></a>

### Dorsal lingual artery left

**Model ID:** `artery.eca.dorsal_lingual.right.left`

**Parent:** [Lingual artery left](#structure-artery.eca.lingual.right.left)

<a id="structure-artery.eca.sublingual.right.left"></a>

### Sublingual artery left

**Model ID:** `artery.eca.sublingual.right.left`

**Parent:** [Lingual artery left](#structure-artery.eca.lingual.right.left)

<a id="structure-artery.eca.facial.right.left"></a>

### Facial artery left

**Model ID:** `artery.eca.facial.right.left`

**Description**

Supply: the submandibular gland, musculocutaneous tissue of the face, and the mandible.

Origin: the facial artery usually arises just above the [lingual artery](#structure-artery.eca.lingual.right.left), although sometimes it shares a common origin.

Course: initially anterosuperiorly directed it turns inferiorly and descends in the parapharyngeal space to reach the submandibular gland. It runs anterolaterally, crossing the deep aspect of the gland and giving off the [submental artery](#structure-artery.eca.submental.right.left) before crossing the mandible in front of the masseter. The artery terminates at the level of the ala of the nose in about 50% and gives rise to the [superior labial artery](#structure-artery.eca.superior_labial.right.left) and alar branches. Alternatively, it becomes the [angular artery](#structure-artery.eca.angular.right.left), running in the nasolabial fold to reach the angle of the eye.

**Source:** `nv(2).pdf`, PDF pages 6, 8; printed pages 12, 14.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.angular.right.left"></a>

### Angular artery left

**Model ID:** `artery.eca.angular.right.left`

**Description**

Angular artery: if present, this is the terminal branch of the [facial artery](#structure-artery.eca.facial.right.left). It may also originate from the ophthalmic or [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left). The vessel courses in the nasojugal fold giving off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery ([lacrimal artery](#structure-artery.anterior.lacrimal_left)) to form the palpebral arcade. There are anastomoses with the ophthalmic, [lateral nasal](#structure-artery.eca.lateral_nasal.right.left), and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left) in addition to its counterpart across the midline.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.ascending_palatine.right.left"></a>

### Ascending palatine artery left

**Model ID:** `artery.eca.ascending_palatine.right.left`

**Description**

Ascending palatine artery: this originates most frequently from the apex of the proximal segment of the [facial artery](#structure-artery.eca.facial.right.left) or from the [ascending pharyngeal](#structure-artery.eca.apa.right.left) or lingual arteries. It ascends superiorly between the styloglossus and stylopharyngeus, giving off tonsillar branches. The artery reaches and supplies the soft palate and the Eustachian tube superiorly. It anastomoses with the pharyngeal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right.left), and [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left) arteries. Damage to this vessel is often implicated in post-tonsillectomy haemorrhage.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.tonsillar.right.left"></a>

### Tonsillar artery left

**Model ID:** `artery.eca.tonsillar.right.left`

**Description**

Tonsillar branch: this arises from the proximal descending part and ascends between the internal pterygoid muscle and styloglossus. It courses anteromedially to supply the palatine tonsil and tongue. It can also be injured during tonsillectomy.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.submental.right.left"></a>

### Submental artery left

**Model ID:** `artery.eca.submental.right.left`

**Description**

Submental artery: this originates at the submandibular segment of the artery and courses anteriorly on mylohyoid, delivering branches to the submandibular gland and regional musculocutaneous tissue and the mandible.

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.inferior_labial.right.left"></a>

### Inferior labial artery left

**Model ID:** `artery.eca.inferior_labial.right.left`

**Description**

The inferior labial artery runs along the lower lip. The labial arteries supply the labial glands, mucous membranes, and regional musculature.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.superior_labial.right.left"></a>

### Superior labial artery left

**Model ID:** `artery.eca.superior_labial.right.left`

**Description**

The superior labial artery follows the upper lip. The labial arteries supply the labial glands, mucous membranes, and regional musculature. The superior labial artery also delivers branches to the nasal septum and ala and can anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left) (the terminal branch of the [IMA](#structure-artery.eca.maxillary.right.left)).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.lateral_nasal.right.left"></a>

### Lateral nasal artery left

**Model ID:** `artery.eca.lateral_nasal.right.left`

**Description**

Lateral nasal artery: this originates distal to the [superior labial](#structure-artery.eca.superior_labial.right.left) branch (or from the [superior labial artery](#structure-artery.eca.superior_labial.right.left)) and runs superiorly along the side of the nose. Occasionally, it is the terminal branch of the [facial artery](#structure-artery.eca.facial.right.left).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.amendment.facial_submandibular_gland_branch.left"></a>

### Facial submandibular gland branch left

**Model ID:** `artery.amendment.facial_submandibular_gland_branch.left`

**Description**

Submandibular gland branches originate inferiorly from the submandibular and submental segments of the [facial artery](#structure-artery.eca.facial.right.left).

**Source:** `nv(2).pdf`, PDF page 8; printed page 14.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.amendment.facial_masseteric_branch.left"></a>

### Facial masseteric branch left

**Model ID:** `artery.amendment.facial_masseteric_branch.left`

**Description**

Masseteric muscular and buccal mucosal branches: these originate superiorly from the [facial artery](#structure-artery.eca.facial.right.left).

Anastomoses: masseteric branches of the [facial artery](#structure-artery.eca.facial.right.left) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left).

**Source:** `nv(2).pdf`, PDF pages 9, 20; printed pages 15, 26.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.amendment.facial_buccal_branch.left"></a>

### Facial buccal branch left

**Model ID:** `artery.amendment.facial_buccal_branch.left`

**Description**

Masseteric muscular and buccal mucosal branches: these originate superiorly from the [facial artery](#structure-artery.eca.facial.right.left).

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.eca.occipital.right.left"></a>

### Occipital artery left

**Model ID:** `artery.eca.occipital.right.left`

**Description**

Supply: musculocutaneous tissue and bone, dura mater of the posterior cranial fossa, and CNs.

Origin: posterosuperiorly from the proximal [ECA](#structure-artery.carotid.external.right.left) usually just above or below the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left) (occasionally they share a common trunk). In some cases, it arises from the internal carotid, vertebral, deep cervical, or [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries.

First segment: runs posterosuperiorly to reach the occipital groove of the temporal bone.

Second segment: horizontal to the superior nuchal line (a bony ridge sweeping laterally from the external occipital protuberance).

Third segment: ascends the distal occiput.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.occipital_lateral_scalp.right.left"></a>

### Occipital lateral scalp artery left

**Model ID:** `artery.eca.occipital_lateral_scalp.right.left`

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

<a id="structure-artery.eca.occipital_medial_scalp.right.left"></a>

### Occipital medial scalp artery left

**Model ID:** `artery.eca.occipital_medial_scalp.right.left`

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

<a id="structure-artery.eca.occipital_descending.right.left"></a>

### Occipital descending artery left

**Model ID:** `artery.eca.occipital_descending.right.left`

**Description**

Descending muscular branches: there are superficial and deep muscular branches arising from the second segment that run inferiorly to supply the back muscles, such as the splenius and trapezius. Importantly, the deep branch anastomoses with the [vertebral artery](#structure-artery.posterior.vertebral_left) and branches of the costocervical trunk at the C1-C2 level and the cervical arteries at C3-C4.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

<a id="structure-artery.eca.occipital_mastoid.right.left"></a>

### Occipital mastoid artery left

**Model ID:** `artery.eca.occipital_mastoid.right.left`

**Description**

Mastoid branches: these arise from the second segment and supply the mastoid bone and skin. A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

<a id="structure-artery.amendment.occipital_mastoid_dural_branch.left"></a>

### Occipital mastoid dural branch left

**Model ID:** `artery.amendment.occipital_mastoid_dural_branch.left`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid artery left](#structure-artery.eca.occipital_mastoid.right.left)

<a id="structure-artery.amendment.occipital_scm_branch.left"></a>

### Occipital SCM branch left

**Model ID:** `artery.amendment.occipital_scm_branch.left`

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

<a id="structure-artery.eca.posterior_auricular.right.left"></a>

### Posterior auricular artery left

**Model ID:** `artery.eca.posterior_auricular.right.left`

**Description**

Supply: musculocutaneous tissue of the face, scalp, pinna, and parotid gland. It is in haemodynamic balance with the [occipital artery](#structure-artery.eca.occipital.right.left) and [STA](#structure-artery.eca.superficial_temporal.right.left). There are anastomoses with the anterior auricular artery (a branch of the [STA](#structure-artery.eca.superficial_temporal.right.left)) above the ear.

Origin: the vessel arises from the distal [ECA](#structure-artery.carotid.external.right.left) posteriorly at the level of the inferior parotid gland. Alternatively, it may share a common trunk with the [occipital artery](#structure-artery.eca.occipital.right.left).

Course: the artery is directed posterosuperiorly beneath the parotid gland and runs on the superior surface of the posterior belly of the digastric muscle. It turns superficially at the mastoid process and courses posterosuperiorly in the posterior auricular sulcus, between the mastoid process and the pinna.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.occipital.stylomastoid.right.left"></a>

### Stylomastoid artery left

**Model ID:** `artery.eca.occipital.stylomastoid.right.left`

**Description**

Stylomastoid artery: this arises from the first segment of the [occipital artery](#structure-artery.eca.occipital.right.left) or the [posterior auricular artery](#structure-artery.eca.posterior_auricular.right.left). It enters the [stylomastoid foramen](#structure-landmark.stylomastoid.left) with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the middle meningeal artery](#structure-artery.eca.maxillary.mma.petrosal.right.left) ([MMA](#structure-artery.eca.maxillary.mma.right.left)). It enters the tympanic cavity and anastomoses with the [superior tympanic artery](#structure-artery.amendment.superior_tympanic.left) from the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right.left), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left) branch of the [IMA](#structure-artery.eca.maxillary.right.left), the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), the [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) branch of the [ICA](#structure-artery.anterior.internal_carotid_left), and the arcuate branch of the [anterior inferior cerebellar artery](#structure-artery.posterior.aica_left) ([AICA](#structure-artery.posterior.aica_left)). It also supplies the tympanic antrum, mastoid bone, and semicircular canal.

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Posterior auricular artery left](#structure-artery.eca.posterior_auricular.right.left)

<a id="structure-artery.amendment.posterior_auricular_parotid_branch.left"></a>

### Posterior auricular parotid branch left

**Model ID:** `artery.amendment.posterior_auricular_parotid_branch.left`

**Parent:** [Posterior auricular artery left](#structure-artery.eca.posterior_auricular.right.left)

<a id="structure-artery.amendment.posterior_auricular_auricular_branch.left"></a>

### Posterior auricular auricular branch left

**Model ID:** `artery.amendment.posterior_auricular_auricular_branch.left`

**Parent:** [Posterior auricular artery left](#structure-artery.eca.posterior_auricular.right.left)

<a id="structure-artery.eca.superficial_temporal.right.left"></a>

### Superficial temporal artery left

**Model ID:** `artery.eca.superficial_temporal.right.left`

**Description**

Supply: the lateral aspect of the scalp and face.

Origin: this is one of the two terminal divisions of the [ECA](#structure-artery.carotid.external.right.left) (the other being the [IMA](#structure-artery.eca.maxillary.right.left)).

Course: the artery originates behind the neck of the mandible in the parotid gland. It ascends laterally along the superficial surface of the temporalis muscle, over the posterior aspect of the condylar process, and passes superficially over the zygomatic process of the temporal bone. After a few centimetres it divides into its frontal and parietal terminal branches.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.superficial_temporal.frontal.right.left"></a>

### STA frontal artery left

**Model ID:** `artery.eca.superficial_temporal.frontal.right.left`

**Description**

The frontal and parietal terminal divisions of the [STA](#structure-artery.eca.superficial_temporal.right.left) arise a couple of centimetres above the superior margin of the zygomatic arch, supplying muscle, skin, and bone. The frontal division curves anterosuperiorly towards the superior orbital rim. It anastomoses with the supraorbital and frontal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.eca.sta_frontal_anterior_twig.right.left"></a>

### STA frontal anterior twig artery left

**Model ID:** `artery.eca.sta_frontal_anterior_twig.right.left`

**Parent:** [STA frontal artery left](#structure-artery.eca.superficial_temporal.frontal.right.left)

<a id="structure-artery.eca.superficial_temporal.parietal.right.left"></a>

### STA parietal artery left

**Model ID:** `artery.eca.superficial_temporal.parietal.right.left`

**Description**

The frontal and parietal terminal divisions of the [STA](#structure-artery.eca.superficial_temporal.right.left) arise a couple of centimetres above the superior margin of the zygomatic arch, supplying muscle, skin, and bone. The parietal division runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right.left), and [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.eca.sta_parietal_anterior_twig.right.left"></a>

### STA parietal anterior twig artery left

**Model ID:** `artery.eca.sta_parietal_anterior_twig.right.left`

**Parent:** [STA parietal artery left](#structure-artery.eca.superficial_temporal.parietal.right.left)

<a id="structure-artery.eca.superficial_temporal.transverse_facial.right.left"></a>

### Transverse facial artery left

**Model ID:** `artery.eca.superficial_temporal.transverse_facial.right.left`

**Description**

Transverse facial artery: this arises within the parotid gland near the origin of the [STA](#structure-artery.eca.superficial_temporal.right.left) and divides into superior and inferior branches. The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), zygomaticomalar, inferior palpebral, buccal, and facial arteries. The inferior trunk also supplies the parotid gland and runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.amendment.transverse_facial_superior_division.left"></a>

### Transverse facial superior division left

**Model ID:** `artery.amendment.transverse_facial_superior_division.left`

**Description**

The superior division of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery left](#structure-artery.eca.superficial_temporal.transverse_facial.right.left)

<a id="structure-artery.amendment.transverse_facial_inferior_division.left"></a>

### Transverse facial inferior division left

**Model ID:** `artery.amendment.transverse_facial_inferior_division.left`

**Description**

The inferior trunk of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) also supplies the parotid gland and runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery left](#structure-artery.eca.superficial_temporal.transverse_facial.right.left)

<a id="structure-artery.amendment.transverse_facial_masseteric_branch.left"></a>

### Transverse facial masseteric branch left

**Model ID:** `artery.amendment.transverse_facial_masseteric_branch.left`

**Description**

The inferior trunk of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) runs superficially over the masseter, which it supplies. It anastomoses with branches of the [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial inferior division left](#structure-artery.amendment.transverse_facial_inferior_division.left)

<a id="structure-artery.amendment.transverse_facial_parotid_branch.left"></a>

### Transverse facial parotid branch left

**Model ID:** `artery.amendment.transverse_facial_parotid_branch.left`

**Description**

Both divisions of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) supply the parotid gland.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial artery left](#structure-artery.eca.superficial_temporal.transverse_facial.right.left)

<a id="structure-artery.eca.middle_temporal.right.left"></a>

### Middle deep temporal artery left

**Model ID:** `artery.eca.middle_temporal.right.left`

**Description**

Posterior deep temporal artery: this arises at the level of the zygoma and is directed posteroinferiorly. Rarely it originates from the [IMA](#structure-artery.eca.maxillary.right.left) or from a common trunk with the zygomatico-orbital arteries. It supplies the temporalis muscle and anastomoses with the middle and anterior temporal arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.amendment.sta_anterior_auricular.left"></a>

### STA anterior auricular left

**Model ID:** `artery.amendment.sta_anterior_auricular.left`

**Description**

Anterior auricular branches: superior, middle, and inferior branches supply the external ear.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.amendment.zygomatico_orbital.left"></a>

### Zygomatico-orbital left

**Model ID:** `artery.amendment.zygomatico_orbital.left`

**Description**

Zygomatico-orbital artery: this arises just proximal to the bifurcation and is directed anteriorly along the upper border of the zygomatic arch towards the lateral angle of the orbit. The artery supplies the anterior temporal and malar region and orbicularis orbis.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superficial temporal artery left](#structure-artery.eca.superficial_temporal.right.left)

<a id="structure-artery.eca.maxillary.right.left"></a>

### Maxillary artery left

**Model ID:** `artery.eca.maxillary.right.left`

**Description**

The internal maxillary artery (IMA) and [STA](#structure-artery.eca.superficial_temporal.right.left) are the terminal divisions of the [ECA](#structure-artery.carotid.external.right.left). The IMA can be referred to as simply the maxillary artery.

IMA branches supply the organs and muscles of the head and neck, mouth, paranasal sinuses, dura, and CNs.

Origin: the IMA originates within the parotid gland behind the neck of the mandible.

The first (mandibular) segment runs deep to the neck of the mandible and runs anterior just lateral to the inferior alveolar nerve towards the border of the lateral pterygoid muscle. It gives off the [deep auricular](#structure-artery.eca.maxillary.deep_auricular.right.left), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left), middle meningeal, [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left), and [inferior alveolar (dental)](#structure-artery.eca.maxillary.inferior_alveolar.right.left) arteries.

The second (zygomatic or pterygoid) segment curves anteromedially, either superficial or deep to the pterygoid muscles, to reach the pterygopalatine fossa. It gives off [middle deep temporal](#structure-artery.eca.posterior_deep_temporal.right.left), pterygoid, masseteric, buccal, and [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right.left) branches.

The third (pterygopalatine) segment runs medially in the pterygopalatine fossa giving off the [posterior superior dental](#structure-artery.eca.maxillary.posterior_superior_alveolar.right.left), [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right.left), and pharyngeal arteries and the arteries of the [foramen rotundum](#structure-landmark.rotundum.left), [pterygoid canal](#structure-landmark.pterygoid-canal.left) (vidian artery), and [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left). It terminates as the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left) at the medial border of the fossa, in the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.left).

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.maxillary.deep_auricular.right.left"></a>

### Deep auricular artery left

**Model ID:** `artery.eca.maxillary.deep_auricular.right.left`

**Description**

Origin: this tiny artery is the first maxillary branch. It may share a common origin with the [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right.left).

Course: it ascends within the parotid behind the temporomandibular joint. It passes through the wall of the external acoustic meatus to supply the skin of the canal and the outer surface of the tympanic membrane.

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.anterior_tympanic.right.left"></a>

### Anterior tympanic artery left

**Model ID:** `artery.eca.maxillary.anterior_tympanic.right.left`

**Description**

Origin: another small vessel, sometimes shares a common origin with the [deep auricular artery](#structure-artery.eca.maxillary.deep_auricular.right.left). It also occasionally arises from the [STA](#structure-artery.eca.superficial_temporal.right.left), the distal [ECA](#structure-artery.carotid.external.right.left), or other proximal maxillary arteries such as the inferior dental or middle meningeal.

Course: the artery ascends behind the temporomandibular joint and bifurcates into anterior and posterior branches. The anterior branch supplies the temporomandibular joint, and the posterior branch enters the tympanic cavity through the [petrotympanic fissure](#structure-landmark.petrotympanic.left) to supply the mucosa of the tympanic cavity and the tympanic membrane.

Anastomoses: [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right.left), the [artery of the pterygoid canal](#structure-artery.eca.maxillary.pterygoid_canal.right.left) (vidian artery), and anastomoses within the tympanic cavity including the [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) branch of the [ICA](#structure-artery.anterior.internal_carotid_left).

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.inferior_alveolar.right.left"></a>

### Inferior alveolar artery left

**Model ID:** `artery.eca.maxillary.inferior_alveolar.right.left`

**Description**

Origin: inferiorly from the first segment of the [IMA](#structure-artery.eca.maxillary.right.left). Occasionally arises from a common trunk with the [middle deep temporal artery](#structure-artery.eca.posterior_deep_temporal.right.left).

The vessel supplies the roots of the lower teeth.

Course: it runs inferiorly accompanying the inferior alveolar nerve and vein. It enters the [mandibular canal](#structure-landmark.mandibular-canal.left) through an opening on the medial surface of the mandibular ramus and then courses anteroinferiorly and medially towards the [mental foramen](#structure-landmark.mental-foramen.left) on the anterior surface of the mandible, anastomosing with mental branches of the [facial artery](#structure-artery.eca.facial.right.left).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.mental.right.left"></a>

### Mental artery left

**Model ID:** `artery.eca.mental.right.left`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right.left) divides into incisor and mental terminal branches opposite the first premolar tooth. The mental branch supplies the lower lip and chin.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery left](#structure-artery.eca.maxillary.inferior_alveolar.right.left)

<a id="structure-artery.eca.incisive.right.left"></a>

### Incisive artery left

**Model ID:** `artery.eca.incisive.right.left`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right.left) divides into incisor and mental terminal branches opposite the first premolar tooth. The incisor branch supplies the pulp of the teeth.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery left](#structure-artery.eca.maxillary.inferior_alveolar.right.left)

<a id="structure-artery.eca.mylohyoid.right.left"></a>

### Mylohyoid artery left

**Model ID:** `artery.eca.mylohyoid.right.left`

**Description**

Extramandibular branches of the [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right.left) supply the pterygoid and mylohyoid muscles and the lingual nerve.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Inferior alveolar artery left](#structure-artery.eca.maxillary.inferior_alveolar.right.left)

<a id="structure-artery.eca.posterior_deep_temporal.right.left"></a>

### Middle deep temporal artery left

**Model ID:** `artery.eca.posterior_deep_temporal.right.left`

**Description**

Origin: this is from the proximal aspect of the second maxillary segment. It may share a common origin with the [inferior dental artery](#structure-artery.eca.maxillary.inferior_alveolar.right.left).

Course: superiorly on the temporal bone giving off small branches to bone and the temporalis muscle.

Anastomoses: [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right.left) and [superficial temporal arteries](#structure-artery.eca.superficial_temporal.right.left). There are transosseous anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) and distal lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.anterior_deep_temporal.right.left"></a>

### Anterior deep temporal artery left

**Model ID:** `artery.eca.anterior_deep_temporal.right.left`

**Description**

Origin: the anterior deep temporal artery takes its origin from the distal aspect of the second segment. It may share a common origin with the [buccal artery](#structure-artery.eca.maxillary.buccal.right.left).

Course: anterosuperiorly along the temporalis muscle which it supplies. It contributes an important branch to the lateral orbit which it reaches either via the zygomatic temporal fissure or [inferior orbital fissure](#structure-landmark.inferior-orbital-fissure.left).

Anastomoses: middle deep and [superficial temporal arteries](#structure-artery.eca.superficial_temporal.right.left) and also distal lacrimal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF pages 20–21; printed pages 26–27.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.masseteric.right.left"></a>

### Masseteric artery left

**Model ID:** `artery.eca.maxillary.masseteric.right.left`

**Description**

Origin: proximal part of the second maxillary segment.

Course: inferiorly through the mandibular notch, between the coronoid and condyloid processes, to supply the masseter muscle.

Anastomoses: masseteric branches of the [facial artery](#structure-artery.eca.facial.right.left) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left).

**Source:** `nv(2).pdf`, PDF pages 15, 20; printed pages 21, 26.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.buccal.right.left"></a>

### Buccal artery left

**Model ID:** `artery.eca.maxillary.buccal.right.left`

**Description**

Origin: distal part of the second maxillary segment.

Course: inferiorly to supply buccal mucosa, buccinator, the parotid duct, and skin.

Anastomoses: ascending branch of the [facial artery](#structure-artery.eca.facial.right.left) and the superior masseteric branch of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left). It is an important route for [facial artery](#structure-artery.eca.facial.right.left) reconstitution after proximal [facial artery](#structure-artery.eca.facial.right.left) ligation.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.pterygoid_muscular.right.left"></a>

### Pterygoid muscular artery left

**Model ID:** `artery.eca.pterygoid_muscular.right.left`

**Description**

Origin: inferiorly from the second maxillary segment.

The artery supplies the medial and lateral pterygoid muscles.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.posterior_superior_alveolar.right.left"></a>

### Posterior superior alveolar artery left

**Model ID:** `artery.eca.maxillary.posterior_superior_alveolar.right.left`

**Description**

Origin: this artery takes its origin from the proximal part of the third maxillary segment, just inside the pterygopalatine fossa. It often shares a common trunk with the [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left).

Course: anteroinferiorly on the lateral surface of the maxilla, giving off osseous branches, supplying the mucosa of the maxillary sinus and buccal cavity, and buccinator. The vessel then enters the superior alveolar canal in the maxilla running towards the incisor foramen.

Anastomoses: [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right.left), and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.psa_anterior_division.right.left"></a>

### PSA anterior division left

**Model ID:** `artery.eca.psa_anterior_division.right.left`

**Parent:** [Posterior superior alveolar artery left](#structure-artery.eca.maxillary.posterior_superior_alveolar.right.left)

<a id="structure-artery.eca.maxillary.infraorbital.right.left"></a>

### Infraorbital artery left

**Model ID:** `artery.eca.maxillary.infraorbital.right.left`

**Description**

Origin: this terminal branch of the [IMA](#structure-artery.eca.maxillary.right.left) arises anteroinferiorly from the proximal part of the third maxillary segment. It may share a common origin with the [posterior superior dental artery](#structure-artery.eca.maxillary.posterior_superior_alveolar.right.left). It supplies the inferior rectus and inferior oblique muscles and lacrimal sac.

Course: laterally, it looks like an upturned boat hull. It ascends on the posterior wall of the maxillary sinus and then traverses the [inferior orbital fissure](#structure-landmark.inferior-orbital-fissure.left) to enter the orbit. The vessel runs forward on the orbital floor in the [infraorbital groove](#structure-landmark.infraorbital-groove.left) (together with the infraorbital nerve and vein), giving off osseous and muscular branches and anastomosing with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left). It then exits through the [infraorbital foramen](#structure-landmark.infraorbital-foramen.left) (again with the infraorbital nerve and vein) to supply the lateral aspect of the nose, upper lip, and the lower eyelid.

Anastomoses: the terminal branches anastomose with the superficial temporal, ophthalmic, facial, and [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.anterior_superior_alveolar.right.left"></a>

### Anterior superior alveolar artery left

**Model ID:** `artery.eca.anterior_superior_alveolar.right.left`

**Parent:** [Infraorbital artery left](#structure-artery.eca.maxillary.infraorbital.right.left)

<a id="structure-artery.amendment.infraorbital_muscular_branch.left"></a>

### Infraorbital muscular branch left

**Model ID:** `artery.amendment.infraorbital_muscular_branch.left`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) supplies the inferior rectus and inferior oblique muscles and lacrimal sac. On the orbital floor it gives off osseous and muscular branches and anastomoses with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Infraorbital artery left](#structure-artery.eca.maxillary.infraorbital.right.left)

<a id="structure-artery.eca.maxillary.descending_palatine.right.left"></a>

### Descending palatine artery left

**Model ID:** `artery.eca.maxillary.descending_palatine.right.left`

**Description**

Origin: inferiorly from the third maxillary segment. It may share a common origin with the [posterior lateral nasal branch](#structure-artery.eca.posterior_lateral_nasal.right.left) of the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left).

Course: it descends and enters the [greater palatine (pterygopalatine) canal](#structure-landmark.greater-palatine-canal.left) accompanied by the great palatine nerve. Within the canal it gives off the [lesser palatine artery](#structure-artery.eca.lesser_palatine.right.left) which supplies the soft palate. The artery becomes the [greater palatine artery](#structure-artery.eca.greater_palatine.right.left) as it exits the canal through the [greater palatine foramen](#structure-landmark.greater-palatine-foramen.left). It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

Anastomoses: [posterior septal arteries](#structure-artery.eca.posterior_septal.right.left) (from the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left)) and the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right.left).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.greater_palatine.right.left"></a>

### Greater palatine artery left

**Model ID:** `artery.eca.greater_palatine.right.left`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) becomes the greater palatine artery as it exits the canal through the [greater palatine foramen](#structure-landmark.greater-palatine-foramen.left). It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

Anastomoses: [posterior septal arteries](#structure-artery.eca.posterior_septal.right.left) (from the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left)) and the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right.left).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Descending palatine artery left](#structure-artery.eca.maxillary.descending_palatine.right.left)

<a id="structure-artery.eca.lesser_palatine.right.left"></a>

### Lesser palatine artery left

**Model ID:** `artery.eca.lesser_palatine.right.left`

**Description**

Within the [greater palatine canal](#structure-landmark.greater-palatine-canal.left), the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) gives off the lesser palatine artery, which supplies the soft palate.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Descending palatine artery left](#structure-artery.eca.maxillary.descending_palatine.right.left)

<a id="structure-artery.eca.maxillary.sphenopalatine.right.left"></a>

### Sphenopalatine artery left

**Model ID:** `artery.eca.maxillary.sphenopalatine.right.left`

**Description**

Origin: the sphenopalatine is a terminal branch of the [maxillary artery](#structure-artery.eca.maxillary.right.left).

Course: medially through the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.left) to enter the nasal cavity, which it supplies in addition to the paranasal sinuses. It is best seen on the anteroposterior projection angiographically due to its medial course.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.posterior_septal.right.left"></a>

### Posterior septal artery left

**Model ID:** `artery.eca.posterior_septal.right.left`

**Description**

Posterior septal (or medial [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left)) artery: this vessel is medially directed towards the superior turbinate and gives off a branch to the sphenoid ostium. It divides into superior and inferior branches. The superior branch supplies the superior turbinate before coursing medially to the nasal septum where it curves anteriorly. It anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left) and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right.left) and contributes to Kiesselbach’s plexus. This plexus is located on the anterior inferior quadrant of the nasal septum (‘Little’s area’) and is a common site for epistaxis. It is supplied by five vessels: the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left), [superior labial](#structure-artery.eca.superior_labial.right.left), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_left), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_left) arteries.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Sphenopalatine artery left](#structure-artery.eca.maxillary.sphenopalatine.right.left)

<a id="structure-artery.amendment.superior_septal_subdivision.left"></a>

### Superior septal subdivision left

**Model ID:** `artery.amendment.superior_septal_subdivision.left`

**Description**

The [posterior septal artery](#structure-artery.eca.posterior_septal.right.left) divides into superior and inferior branches. The superior branch supplies the superior turbinate before coursing medially to the nasal septum where it curves anteriorly. It anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left) and [descending palatine](#structure-artery.eca.maxillary.descending_palatine.right.left) and contributes to Kiesselbach’s plexus.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Posterior septal artery left](#structure-artery.eca.posterior_septal.right.left)

<a id="structure-artery.amendment.inferior_septal_subdivision.left"></a>

### Inferior septal subdivision left

**Model ID:** `artery.amendment.inferior_septal_subdivision.left`

**Parent:** [Posterior septal artery left](#structure-artery.eca.posterior_septal.right.left)

<a id="structure-artery.eca.posterior_lateral_nasal.right.left"></a>

### Posterior lateral nasal artery left

**Model ID:** `artery.eca.posterior_lateral_nasal.right.left`

**Description**

Posterior lateral nasal artery (or lateral [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left)): this vessel sometimes originates from the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left). It supplies the middle and inferior turbinates and maxillary and ethmoidal sinuses. It may anastomose with branches of the [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left), nasal branches of the [facial artery](#structure-artery.eca.facial.right.left), and ethmoidal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Sphenopalatine artery left](#structure-artery.eca.maxillary.sphenopalatine.right.left)

<a id="structure-artery.eca.pterygovaginal.right.left"></a>

### Pterygovaginal artery left

**Model ID:** `artery.eca.pterygovaginal.right.left`

**Description**

Origin: third maxillary segment proximal to the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.left). It sometimes shares a common trunk with the artery of the pterygoid/[vidian canal](#structure-landmark.pterygoid-canal.left) or the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left).

Course: posteromedially and inferiorly through the pharyngeal (pterygovaginal) canal to supply the roof of pharynx and pharyngeal end of the Eustachian tube.

Anastomoses: branches of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left), vidian artery, and [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) (pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.pterygoid_canal.right.left"></a>

### Vidian artery left

**Model ID:** `artery.eca.maxillary.pterygoid_canal.right.left`

**Description**

Origin: posterosuperiorly from the third maxillary segment. It may share a common origin with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left) or the pharyngeal artery.

It supplies the mucosa of the pterygopalatine fossa and nasopharyngeal cavity.

Course: the vessel has a horizontal course, running posterolaterally through the [vidian canal](#structure-landmark.pterygoid-canal.left) accompanied by the vidian nerve to reach the [foramen lacerum](#structure-landmark.foramen-lacerum.left) where it anastomoses with the other vidian artery arising from the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous). Along its course it gives off mucosal branches to the nasal and oropharyngeal cavities and osseous branches within the [pterygoid canal](#structure-landmark.pterygoid-canal.left) and Eustachian tube.

Anastomoses: [vidian artery of the ICA](#structure-artery.anterior.vidian_ica_contribution_left), [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left), mandibular artery, [ascending pharyngeal](#structure-artery.eca.apa.right.left) ([superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left)), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left), and [ascending palatine](#structure-artery.eca.ascending_palatine.right.left) arteries (the pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.foramen_rotundum.right.left"></a>

### Artery of the foramen rotundum left

**Model ID:** `artery.eca.maxillary.foramen_rotundum.right.left`

**Description**

Origin: posterosuperiorly from the third maxillary segment. It courses posteriorly accompanied by the maxillary nerve, which it supplies, and enters the cranium through the [foramen rotundum](#structure-landmark.rotundum.left) to supply dura mater. It has a characteristic corkscrew appearance.

Anastomoses: there is an important anastomosis with the [anterolateral branch of the ILT](#structure-artery.amendment.ilt_anterolateral_ramus.left) (from the [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous)).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.accessory_meningeal.right.left"></a>

### Accessory meningeal artery left

**Model ID:** `artery.eca.maxillary.accessory_meningeal.right.left`

**Description**

Origin: this artery has an oblique anterior and medial slant, arising anterosuperiorly from the first segment of the [IMA](#structure-artery.eca.maxillary.right.left) or from the extracranial [MMA](#structure-artery.eca.maxillary.mma.right.left). It supplies the CNs, the pharynx, the Eustachian tube, meninges and has several important anastomoses.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.amendment.accessory_meningeal_anterior_tubal.left"></a>

### Accessory meningeal anterior tubal left

**Model ID:** `artery.amendment.accessory_meningeal_anterior_tubal.left`

**Description**

Anterior branch: courses along the Eustachian tube reaching the torus tubaris, supplying regional mucosa, bone, and the tensor veli palatini muscle. There are anastomoses with the vidian artery, mandibular artery, the artery of the pterygoid and pharyngeal canals, and the pharyngeal branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Accessory meningeal artery left](#structure-artery.eca.maxillary.accessory_meningeal.right.left)

<a id="structure-artery.amendment.accessory_meningeal_posterior_intracranial.left"></a>

### Accessory meningeal posterior intracranial left

**Model ID:** `artery.amendment.accessory_meningeal_posterior_intracranial.left`

**Description**

Posterior branch: ascends superiorly and enters the skull through the [foramen ovale](#structure-landmark.ovale.left) or [foramen vesalius](#structure-landmark.vesalius.left). The vessel supplies the mandibular division of the trigeminal nerve, trigeminal ganglion and dura mater of Meckel’s cave and the middle cranial fossa. There are anastomoses with inferolateral and MHTs of the [ICA](#structure-artery.anterior.internal_carotid_left), recurrent meningeal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left), cavernous branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left), the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left), and the [subarcuate artery](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Accessory meningeal artery left](#structure-artery.eca.maxillary.accessory_meningeal.right.left)

<a id="structure-artery.eca.maxillary.mma.right.left"></a>

### Middle meningeal artery left

**Model ID:** `artery.eca.maxillary.mma.right.left`

**Description**

The middle meningeal artery supplies more than two-thirds of the cranial dura.

Origin: the MMA arises from the superomedial surface of the first segment of the [IMA](#structure-artery.eca.maxillary.right.left). Often it shares a common trunk with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left). The MMA may also rarely originate from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) (the ‘recurrent meningeal artery’), the [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous) via the [ILT](#structure-artery.anterior.inferolateral_trunk_left), the [petrosal ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) via the persistent stapedial or vidian arteries, the [cervical ICA](#structure-artery.anterior.internal_carotid_left.segment.cervical), the [basilar artery](#structure-artery.posterior.basilar) (usually distal third), or the [occipital artery](#structure-artery.eca.occipital.right.left).

Extracranial segment: the artery passes superiorly and medially and enters the cranial cavity via the [foramen spinosum](#structure-landmark.foramen-spinosum.left).

Horizontal segment: it then turns abruptly laterally and runs horizontally giving off wispy petrosal and cavernous sinus branches. The vessel continues to reach the petrosquamous suture, delivering a [petrosquamosal branch](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left).

Temporal segment: it then courses anteriorly on the greater wing of the sphenoid to reach the pterion (the convergence of the frontal, parietal, temporal, and sphenoid bones).

Pterional segment: this segment curves around the pterion.

Coronal segment: this segment runs superomedially along the coronal suture towards the midline, becoming the paramedian artery supplying the superior sagittal sinus.

**Source:** `nv(2).pdf`, PDF pages 15, 18; printed pages 21, 24.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.maxillary.mma.frontal.right.left"></a>

### MMA frontal artery left

**Model ID:** `artery.eca.maxillary.mma.frontal.right.left`

**Description**

Anterior convexity branches: these originate from the temporal, pterional, and coronal segments and course medially along the lesser wing of the sphenoid bone. There are important anastomoses with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left). The [MMA](#structure-artery.eca.maxillary.mma.right.left) may be the sole supply of the orbit (the ‘meningo-ophthalmic artery’) or supply the lacrimal gland and lateral orbit via a recurrent branch traversing the [foramen of Hyrtl](#structure-landmark.cranio-orbital.left) (found in the spheno-orbital foramen, in the orbital roof). This latter branch usually also has [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) anastomoses. Anterior branches from the coronal segment anastomose with the [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_left) branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.eca.mma_frontal_anterior_division.right.left"></a>

### MMA frontal anterior division left

**Model ID:** `artery.eca.mma_frontal_anterior_division.right.left`

**Parent:** [MMA frontal artery left](#structure-artery.eca.maxillary.mma.frontal.right.left)

<a id="structure-artery.eca.mma_frontal_posterior_division.right.left"></a>

### MMA frontal posterior division left

**Model ID:** `artery.eca.mma_frontal_posterior_division.right.left`

**Parent:** [MMA frontal artery left](#structure-artery.eca.maxillary.mma.frontal.right.left)

<a id="structure-artery.amendment.mma_paramedian.left"></a>

### MMA paramedian left

**Model ID:** `artery.amendment.mma_paramedian.left`

**Description**

Paramedian arteries: these are the terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left). They are directed anteriorly or posteriorly along the superior sagittal sinus and anastomose with the anterior (from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left)) or posterior (from the [ascending pharyngeal](#structure-artery.eca.apa.right.left)) falcine arteries. They deliver small branches to the superior sagittal sinus and falx cerebri. They also anastomose with dural branches of the posterior cerebral artery (PCA; Davidoff and Schechter) and the [superior cerebellar artery](#structure-artery.posterior.sca_left) ([SCA](#structure-artery.posterior.sca_left); [artery of Wollschlaeger and Wollschlaeger](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.left)).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [MMA frontal artery left](#structure-artery.eca.maxillary.mma.frontal.right.left)

<a id="structure-artery.amendment.mma_falcine_terminal.left"></a>

### MMA falcine terminal left

**Model ID:** `artery.amendment.mma_falcine_terminal.left`

**Description**

The paramedian terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left) deliver small branches to the superior sagittal sinus and falx cerebri. They anastomose with the anterior and posterior falcine arteries, and with dural branches of the PCA and [SCA](#structure-artery.posterior.sca_left).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [MMA paramedian left](#structure-artery.amendment.mma_paramedian.left)

<a id="structure-artery.eca.maxillary.mma.posterior_convexity.right.left"></a>

### MMA posterior convexity artery left

**Model ID:** `artery.eca.maxillary.mma.posterior_convexity.right.left`

**Description**

Posterior convexity branches: a variable number of posterior branches arise from the temporal and coronal segments, and the petrosquamosal branches, supplying a large region of convexity dura mater. Note that all peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right.left) and [occipital artery](#structure-artery.eca.occipital.right.left) via transosseous branches, which become evident under pathological conditions, in particular, dural arteriovenous fistulas. There are also potential anastomoses with dural branches of cortical arteries.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.eca.mma_parietal_ascending.right.left"></a>

### MMA parietal ascending artery left

**Model ID:** `artery.eca.mma_parietal_ascending.right.left`

**Parent:** [MMA posterior convexity artery left](#structure-artery.eca.maxillary.mma.posterior_convexity.right.left)

<a id="structure-artery.eca.mma_posterior_terminal.right.left"></a>

### MMA posterior terminal artery left

**Model ID:** `artery.eca.mma_posterior_terminal.right.left`

**Parent:** [MMA posterior convexity artery left](#structure-artery.eca.maxillary.mma.posterior_convexity.right.left)

<a id="structure-artery.eca.maxillary.mma.petrosquamosal.right.left"></a>

### MMA petrosquamosal artery left

**Model ID:** `artery.eca.maxillary.mma.petrosquamosal.right.left`

**Description**

Petrosquamosal branch: this arises from the horizontal segment slightly more distally than the petrosal branches. On the lateral view it can be difficult to distinguish from the petrosal branches, but this is easy on anteroposterior (AP) views as the petrosquamosal is directed laterally (and is usually more prominent) whereas the petrosal branches course medially and are wispy.

**Source:** `nv(2).pdf`, PDF pages 18–19; printed pages 24–25.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.eca.maxillary.mma.petrosal.right.left"></a>

### MMA petrosal artery left

**Model ID:** `artery.eca.maxillary.mma.petrosal.right.left`

**Description**

Petrosal branches: these arise posteriorly at the level of the [foramen spinosum](#structure-landmark.foramen-spinosum.left) from the proximal horizontal segment. The branches should be protected during embolisation particularly because the superficial petrosal branch passes through the facial nerve canal contributing to the facial arcade to supply the facial nerve. They run medially to supply regional dura mater. The proximal petrosal branch, immediately distal to the [foramen spinosum](#structure-landmark.foramen-spinosum.left), supplies the cavernous sinus, trigeminal nerve, and Gasserian ganglion and anastomoses with the [ILT](#structure-artery.anterior.inferolateral_trunk_left). This artery also supplies the [superior tympanic](#structure-artery.amendment.superior_tympanic.left) cavity and anastomoses in the tympanic cavity with the [caroticotympanic](#structure-artery.anterior.caroticotympanic_left), [superior tympanic](#structure-artery.amendment.superior_tympanic.left) (another petrosal branch supplying the tensor tympani muscle and superior part of the tympanic cavity), [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left), subarcuate (anterior inferior cerebellar branch) arteries, and the tubal branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left). There are also numerous important anastomoses including with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left), tentorial arteries from the inferolateral or MHTs of the [ICA](#structure-artery.anterior.internal_carotid_left), dural branches from the [AICA](#structure-artery.posterior.aica_left) and [ascending pharyngeal artery](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.amendment.superior_tympanic.left"></a>

### Superior tympanic left

**Model ID:** `artery.amendment.superior_tympanic.left`

**Description**

The superior tympanic artery is a [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right.left) supplying the tensor tympani muscle and superior part of the tympanic cavity.

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right.left) anastomoses in the tympanic cavity with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left), superior tympanic, and [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) arteries.

**Source:** `nv(2).pdf`, PDF pages 10, 18; printed pages 16, 24.

**Parent:** [MMA petrosal artery left](#structure-artery.eca.maxillary.mma.petrosal.right.left)

<a id="structure-artery.eca.mma_cavernous.right.left"></a>

### MMA cavernous artery left

**Model ID:** `artery.eca.mma_cavernous.right.left`

**Description**

Cavernous sinus branches: anterior and posterior branches originate from the horizontal segment to supply the lateral wall of the cavernous sinus. The anterior branch runs anteromedially to supply the anterior cavernous sinus and anastomoses with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left). The posterior branch is directed posteromedially to supply the posterior cavernous sinus and anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.amendment.mma_anterior_cavernous.left"></a>

### MMA anterior cavernous left

**Model ID:** `artery.amendment.mma_anterior_cavernous.left`

**Description**

The anterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right.left) arises from its horizontal segment. It runs anteromedially to supply the anterior cavernous sinus and anastomoses with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [MMA cavernous artery left](#structure-artery.eca.mma_cavernous.right.left)

<a id="structure-artery.amendment.mma_posterior_cavernous.left"></a>

### MMA posterior cavernous left

**Model ID:** `artery.amendment.mma_posterior_cavernous.left`

**Description**

The posterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right.left) arises from its horizontal segment. It is directed posteromedially to supply the posterior cavernous sinus and anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [MMA cavernous artery left](#structure-artery.eca.mma_cavernous.right.left)

<a id="structure-artery.eca.mma_orbital.right.left"></a>

### MMA orbital artery left

**Model ID:** `artery.eca.mma_orbital.right.left`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right.left) may be the sole supply of the orbit (the meningo-ophthalmic artery) or supply the lacrimal gland and lateral orbit via a recurrent branch traversing the [foramen of Hyrtl](#structure-landmark.cranio-orbital.left). This latter branch usually also has [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) anastomoses.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle meningeal artery left](#structure-artery.eca.maxillary.mma.right.left)

<a id="structure-artery.amendment.artery_of_superior_orbital_fissure.left"></a>

### Artery of superior orbital fissure left

**Model ID:** `artery.amendment.artery_of_superior_orbital_fissure.left`

**Description**

Origin: superomedially from the third maxillary segment. It may share a common trunk with the [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left).

Course: superiorly through the [sphenopalatine foramen](#structure-landmark.sphenopalatine-foramen.left) towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left).

Anastomoses: anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Maxillary artery left](#structure-artery.eca.maxillary.right.left)

<a id="structure-artery.eca.apa.right.left"></a>

### Ascending pharyngeal artery left

**Model ID:** `artery.eca.apa.right.left`

**Description**

Supply: nasopharynx, Eustachian tube, middle ear, oropharynx, soft palate, abducens, glossopharyngeal, vagus, accessory, and hypoglossal nerves.

Origin: this long needle-thin artery arises posteromedially from the proximal [ECA](#structure-artery.carotid.external.right.left), close to the [occipital artery](#structure-artery.eca.occipital.right.left) origin, sometimes sharing an origin. It can also arise from a common trunk with the lingual and facial arteries, the carotid bifurcation, internal carotid, or ascending cervical artery. There are numerous potential anastomoses with the vertebrobasilar artery and [ICA](#structure-artery.anterior.internal_carotid_left).

Course: it runs straight up medial to the [ICA](#structure-artery.anterior.internal_carotid_left), giving off small muscular branches before dividing into anterior pharyngeal and posterior neuromeningeal trunks.

**Source:** `nv(2).pdf`, PDF page 12; printed page 18.

**Parent:** [External carotid artery left](#structure-artery.carotid.external.right.left)

<a id="structure-artery.eca.apa.pharyngeal_trunk.right.left"></a>

### Pharyngeal trunk left

**Model ID:** `artery.eca.apa.pharyngeal_trunk.right.left`

**Description**

Superior, middle, and inferior pharyngeal branches: these branches supply the pharyngeal submucosal spaces and contribute to a rich anastomotic network with the contralateral [ascending pharyngeal artery](#structure-artery.eca.apa.right) and [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Ascending pharyngeal artery left](#structure-artery.eca.apa.right.left)

<a id="structure-artery.eca.inferior_pharyngeal.right.left"></a>

### Inferior pharyngeal artery left

**Model ID:** `artery.eca.inferior_pharyngeal.right.left`

**Description**

The inferior branch, also of importance in post-tonsillectomy haemorrhage, courses anteroinferiorly and supplies the oropharynx. It may anastomose with the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right.left).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk left](#structure-artery.eca.apa.pharyngeal_trunk.right.left)

<a id="structure-artery.eca.middle_pharyngeal.right.left"></a>

### Middle pharyngeal artery left

**Model ID:** `artery.eca.middle_pharyngeal.right.left`

**Description**

The middle branch is directed anteromedially and supplies the nasopharynx and soft palate. It is an important source of bleeding in refractory epistaxis and post-tonsillectomy haemorrhage. It may anastomose with the [pterygovaginal](#structure-artery.eca.pterygovaginal.right.left), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left), and descending and greater palatine arteries.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk left](#structure-artery.eca.apa.pharyngeal_trunk.right.left)

<a id="structure-artery.eca.superior_pharyngeal.right.left"></a>

### Superior pharyngeal artery left

**Model ID:** `artery.eca.superior_pharyngeal.right.left`

**Description**

The superior branch is directed upwards and supplies the nasopharynx and soft palate. It anastomoses with the [artery of the pterygoid canal](#structure-artery.eca.maxillary.pterygoid_canal.right.left) and middle meningeal and [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left) arteries (from the [IMA](#structure-artery.eca.maxillary.right.left)), and the vidian and mandibular arteries ([ICA](#structure-artery.anterior.internal_carotid_left) cavernous segment). The superior branch gives off Eustachian tube and carotid branches. The former supplies the Eustachian tube and submucosa of the fossa of Rosenmüller while the latter traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.left) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left) ([inferolateral trunk](#structure-artery.anterior.inferolateral_trunk_left) ([ILT](#structure-artery.anterior.inferolateral_trunk_left)) of the [ICA](#structure-artery.anterior.internal_carotid_left), both ipsilateral and contralateral).

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Pharyngeal trunk left](#structure-artery.eca.apa.pharyngeal_trunk.right.left)

<a id="structure-artery.amendment.superior_pharyngeal_tubal_branch.left"></a>

### Superior pharyngeal tubal branch left

**Model ID:** `artery.amendment.superior_pharyngeal_tubal_branch.left`

**Description**

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) gives off an Eustachian tube branch, which supplies the Eustachian tube and submucosa of the fossa of Rosenmüller.

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [pharyngeal trunk](#structure-artery.eca.apa.pharyngeal_trunk.right.left) contributes to the Eustachian tube anastomotic circle. It is connected to the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous)’s mandibular and vidian arteries and forms connections with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) and [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left) (distal [IMA](#structure-artery.eca.maxillary.right.left)). It also sends a branch through the [foramen lacerum](#structure-landmark.foramen-lacerum.left) to the cavernous sinus, joining the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left) and the [ILT](#structure-artery.anterior.inferolateral_trunk_left) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous).

**Source:** `nv(2).pdf`, PDF pages 13, 52; printed pages 19, 58.

**Parent:** [Superior pharyngeal artery left](#structure-artery.eca.superior_pharyngeal.right.left)

<a id="structure-artery.amendment.superior_pharyngeal_carotid_branch.left"></a>

### Superior pharyngeal carotid branch left

**Model ID:** `artery.amendment.superior_pharyngeal_carotid_branch.left`

**Description**

The carotid branch of the superior pharyngeal artery traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.left) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left) from the [ILT](#structure-artery.anterior.inferolateral_trunk_left) of the [ICA](#structure-artery.anterior.internal_carotid_left), both ipsilateral and contralateral.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Superior pharyngeal artery left](#structure-artery.eca.superior_pharyngeal.right.left)

<a id="structure-artery.eca.apa.neuromeningeal_trunk.right.left"></a>

### Neuromeningeal trunk left

**Model ID:** `artery.eca.apa.neuromeningeal_trunk.right.left`

**Description**

The neuromeningeal trunk is important because of its supply of cranial nerves. It may also arise from the occipital or [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries. The trunk bifurcates into jugular and hypoglossal branches.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Ascending pharyngeal artery left](#structure-artery.eca.apa.right.left)

<a id="structure-artery.eca.apa.hypoglossal.right.left"></a>

### Hypoglossal branch left

**Model ID:** `artery.eca.apa.hypoglossal.right.left`

**Description**

The hypoglossal branch is more posterior, inferior, and medial and enters the cranium through the [hypoglossal canal](#structure-landmark.hypoglossal.left) to supply the hypoglossal nerve and meninges. A medial branch runs over the medial clivus and anastomoses with the [medial clival artery (MHT of the ICA)](#structure-artery.amendment.medial_clival_mht_branch.left). A descending branch anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries. Posterior branches course inferomedially along the floor of the posterior fossa, medially as the [artery of the falx cerebelli](#structure-artery.amendment.falx_cerebelli_artery.left) and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_left). Rarely, the [posterior inferior cerebellar artery](#structure-artery.posterior.pica_left) ([PICA](#structure-artery.posterior.pica_left)) may arise from the hypoglossal artery.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Neuromeningeal trunk left](#structure-artery.eca.apa.neuromeningeal_trunk.right.left)

<a id="structure-artery.eca.medial_clival.right.left"></a>

### Medial clival artery left

**Model ID:** `artery.eca.medial_clival.right.left`

**Description**

A medial branch of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left) runs over the medial clivus and anastomoses with the [medial clival artery from the MHT](#structure-artery.amendment.medial_clival_mht_branch.left) of the [ICA](#structure-artery.anterior.internal_carotid_left).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch left](#structure-artery.eca.apa.hypoglossal.right.left)

<a id="structure-artery.eca.apa.descending_odontoid.right.left"></a>

### Odontoid descending artery left

**Model ID:** `artery.eca.apa.descending_odontoid.right.left`

**Description**

A descending branch of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left) anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch left](#structure-artery.eca.apa.hypoglossal.right.left)

<a id="structure-artery.eca.apa.posterior_meningeal.right.left"></a>

### Hypoglossal posterior meningeal artery left

**Model ID:** `artery.eca.apa.posterior_meningeal.right.left`

**Description**

Posterior branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left) course inferomedially along the floor of the posterior fossa, medially as the [artery of the falx cerebelli](#structure-artery.amendment.falx_cerebelli_artery.left) and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal branch left](#structure-artery.eca.apa.hypoglossal.right.left)

<a id="structure-artery.amendment.falx_cerebelli_artery.left"></a>

### Falx cerebelli artery left

**Model ID:** `artery.amendment.falx_cerebelli_artery.left`

**Description**

Posterior branches of the [hypoglossal artery](#structure-artery.eca.apa.hypoglossal.right.left) course inferomedially along the floor of the posterior fossa, medially as the artery of the falx cerebelli and laterally as the posterior meningeal artery. Both of these may also arise from the vertebral or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Hypoglossal posterior meningeal artery left](#structure-artery.eca.apa.posterior_meningeal.right.left)

<a id="structure-artery.eca.apa.jugular.right.left"></a>

### Jugular branch left

**Model ID:** `artery.eca.apa.jugular.right.left`

**Description**

The jugular branch is the more superior and lateral division of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left) and enters the cranium through the [jugular foramen](#structure-landmark.jugular-foramen.left).

It supplies the glossopharyngeal, vagus, and accessory nerves in addition to meninges. It has an ascending medial branch that accompanies the inferior petrosal sinus and anastomoses with the [lateral clival artery (meningohypophyseal trunk (MHT))](#structure-artery.amendment.lateral_clival_mht_branch.left). Clival branches also anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_left) and can supply the abducens nerve in Dorello’s canal. A sigmoid branch accompanies the sigmoid and transverse sinuses and anastomoses with the middle meningeal and [occipital arteries](#structure-artery.eca.occipital.right.left). An additional ascending branch supplies dura mater of the internal auditory canal and may anastomose with the [AICA](#structure-artery.posterior.aica_left). The posterior meningeal artery may originate from the jugular branch.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Neuromeningeal trunk left](#structure-artery.eca.apa.neuromeningeal_trunk.right.left)

<a id="structure-artery.eca.lateral_clival.right.left"></a>

### Lateral clival artery left

**Model ID:** `artery.eca.lateral_clival.right.left`

**Description**

An ascending medial branch of the [jugular artery](#structure-artery.eca.apa.jugular.right.left) accompanies the inferior petrosal sinus and anastomoses with the [lateral clival artery from the MHT](#structure-artery.amendment.lateral_clival_mht_branch.left). Clival branches also anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_left) and can supply the abducens nerve in Dorello’s canal.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch left](#structure-artery.eca.apa.jugular.right.left)

<a id="structure-artery.eca.apa.sigmoid_sinus_branch.right.left"></a>

### Jugular sigmoid branch left

**Model ID:** `artery.eca.apa.sigmoid_sinus_branch.right.left`

**Description**

A sigmoid branch of the [jugular artery](#structure-artery.eca.apa.jugular.right.left) accompanies the sigmoid and transverse sinuses and anastomoses with the middle meningeal and [occipital arteries](#structure-artery.eca.occipital.right.left).

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch left](#structure-artery.eca.apa.jugular.right.left)

<a id="structure-artery.amendment.jugular_ascending_iac_branch.left"></a>

### Jugular ascending IAC branch left

**Model ID:** `artery.amendment.jugular_ascending_iac_branch.left`

**Description**

An ascending branch of the [jugular artery](#structure-artery.eca.apa.jugular.right.left) supplies dura mater of the internal auditory canal and may anastomose with the [AICA](#structure-artery.posterior.aica_left).

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Jugular branch left](#structure-artery.eca.apa.jugular.right.left)

<a id="structure-artery.eca.apa.inferior_tympanic.right.left"></a>

### Inferior tympanic artery left

**Model ID:** `artery.eca.apa.inferior_tympanic.right.left`

**Description**

The inferior tympanic artery branch of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left) travels with Jacobson’s nerve through the inferior tympanic foramen, anastomosing with other tympanic ([anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left), [superior tympanic](#structure-artery.amendment.superior_tympanic.left)) and surrounding arteries within the middle ear including the [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_left), a [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) branch.

The [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_left) is normally a tiny branch of the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) but may enlarge and form the anatomical variant of the ‘aberrant [ICA](#structure-artery.anterior.internal_carotid_left)’ in the absence of normal [cervical ICA](#structure-artery.anterior.internal_carotid_left.segment.cervical) development.

**Source:** `nv(2).pdf`, PDF pages 13, 52; printed pages 19, 58.

**Parent:** [Ascending pharyngeal artery left](#structure-artery.eca.apa.right.left)

<a id="structure-artery.amendment.apa_musculospinal.left"></a>

### APA musculospinal left

**Model ID:** `artery.amendment.apa_musculospinal.left`

**Description**

Musculospinal branch: this passes posteroinferiorly at the C3 level. It supplies the spinal accessory nerve and the superior sympathetic ganglion. Important anastomoses connect with the ascending and deep cervical arteries and [vertebral artery](#structure-artery.posterior.vertebral_left).

The musculospinal branch laterally anastomoses with the C3 radicular anastomotic artery from the [vertebral artery](#structure-artery.posterior.vertebral_left).

**Source:** `nv(2).pdf`, PDF pages 13, 54; printed pages 19, 60.

**Parent:** [Ascending pharyngeal artery left](#structure-artery.eca.apa.right.left)

<a id="structure-artery.amendment.apa_prevertebral_branch.left"></a>

### APA prevertebral branch left

**Model ID:** `artery.amendment.apa_prevertebral_branch.left`

**Description**

The prevertebral branch, running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_left) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Ascending pharyngeal artery left](#structure-artery.eca.apa.right.left)

<a id="vertebrobasilar-right"></a>

## Vertebrobasilar arteries and branches, right

<a id="structure-artery.posterior.pcom_perforator_right"></a>

### PCom perforator right

**Model ID:** `artery.posterior.pcom_perforator_right`

**Description**

The anterior thalamoperforators of the [PCOM](#structure-artery.anterior.posterior_communicating_right) arise from the superolateral aspect and a particularly prominent one is the [tuberothalamic artery](#structure-artery.amendment.tuberothalamic_artery.right), which supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract. The anterior thalamoperforating group also supply the posterior optic chiasm, proximal optic radiations, posterior hypothalamus, and cerebral peduncle. They anastomose with choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating right](#structure-artery.anterior.posterior_communicating_right)

<a id="structure-artery.posterior.vertebral_right"></a>

### Vertebral right

**Model ID:** `artery.posterior.vertebral_right`

**Description**

The vertebral artery can be divided into four segments .

This segment extends until the artery enters the foramen in the transverse process, typically at the C6 level (C4 if the vertebral artery arises from the aortic arch).

The artery continues vertically upwards to the C2 transverse foramina, surrounded by the vertebral venous plexus.

Starts at the foramen transversarium of the axis (C2). The artery turns laterally and ascends, passing through the transverse foramen of the atlas (C1). It then curves medially and is directed towards the [foramen magnum](#structure-landmark.foramen-magnum.midline). It imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the [arcuate foramen](#structure-landmark.arcuate-foramen.right) (a possible risk factor for paediatric ischaemic stroke).

This segment pierces the atlanto-occipital membrane to become intradural (where it is focally smoothly narrowed), entering the cranial cavity via the [foramen magnum](#structure-landmark.foramen-magnum.midline). It continues medially until it joins its counterpart to form the [basilar artery](#structure-artery.posterior.basilar) at the upper edge of the medulla oblongata.

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Arteries](#structure-artery)

<a id="structure-artery.posterior.pca_p1_right"></a>

### PCA P1 right

**Model ID:** `artery.posterior.pca_p1_right`

**Description**

Originating at the basilar bifurcation, the P1 segment runs within the interpeduncular cistern and terminates at the [PCOM](#structure-artery.anterior.posterior_communicating_right) insertion.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pca_p2_p3_right"></a>

### PCA P2-P3 right

**Model ID:** `artery.posterior.pca_p2_p3_right`

**Description**

P2 courses around the midbrain, under the thalamus, running in the crural and ambient cisterns. Branches supply the thalamus, cerebral peduncle, and quadrigeminal plate.

The P3 segment runs posteromedially in the quadrigeminal cistern.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P1 right](#structure-artery.posterior.pca_p1_right)

<a id="structure-artery.posterior.pca_calcarine_right"></a>

### PCA calcarine right

**Model ID:** `artery.posterior.pca_calcarine_right`

**Description**

Calcarine: this runs initially inferior and lateral to the [parieto-occipital artery](#structure-artery.posterior.pca_parieto_occipital_right) within the calcarine fissure to supply the visual cortex, cuneus, and lingual gyrus. It occasionally originates from the parieto-occipital or posterior temporal arteries.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.calcarine_superior_cortical_right"></a>

### Calcarine superior cortical right

**Model ID:** `artery.posterior.calcarine_superior_cortical_right`

**Parent:** [PCA calcarine right](#structure-artery.posterior.pca_calcarine_right)

<a id="structure-artery.posterior.calcarine_inferior_cortical_right"></a>

### Calcarine inferior cortical right

**Model ID:** `artery.posterior.calcarine_inferior_cortical_right`

**Parent:** [PCA calcarine right](#structure-artery.posterior.pca_calcarine_right)

<a id="structure-artery.posterior.pca_parieto_occipital_right"></a>

### PCA parieto-occipital right

**Model ID:** `artery.posterior.pca_parieto_occipital_right`

**Description**

Parieto-occipital: usually the largest of the terminal branches, it runs initially superior and medial to the [calcarine artery](#structure-artery.posterior.pca_calcarine_right) in the parieto-occipital fissure. The artery supplies the cuneus, precuneus, and superior occipital gyrus of the occipital lobe. It may also give branches to the precentral gyrus, superior parietal lobule, and an accessory calcarine branch to the visual cortex.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.parieto_occipital_cuneal_right"></a>

### Parieto-occipital cuneal right

**Model ID:** `artery.posterior.parieto_occipital_cuneal_right`

**Parent:** [PCA parieto-occipital right](#structure-artery.posterior.pca_parieto_occipital_right)

<a id="structure-artery.posterior.pca_anterior_inferior_temporal_right"></a>

### PCA anterior inferior temporal right

**Model ID:** `artery.posterior.pca_anterior_inferior_temporal_right`

**Description**

The anterior temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.pca_middle_inferior_temporal_right"></a>

### PCA middle inferior temporal right

**Model ID:** `artery.posterior.pca_middle_inferior_temporal_right`

**Description**

The middle temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.pca_posterior_inferior_temporal_right"></a>

### PCA posterior inferior temporal right

**Model ID:** `artery.posterior.pca_posterior_inferior_temporal_right`

**Description**

The posterior temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.pca_lateral_occipital_right"></a>

### PCA lateral occipital right

**Model ID:** `artery.posterior.pca_lateral_occipital_right`

**Parent:** [PCA posterior inferior temporal right](#structure-artery.posterior.pca_posterior_inferior_temporal_right)

<a id="structure-artery.posterior.pca_splenial_right"></a>

### PCA splenial right

**Model ID:** `artery.posterior.pca_splenial_right`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.pca_hippocampal_right"></a>

### PCA hippocampal right

**Model ID:** `artery.posterior.pca_hippocampal_right`

**Description**

Hippocampal: supplying the hippocampus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.medial_posterior_choroidal_right"></a>

### Medial posterior choroidal right

**Model ID:** `artery.posterior.medial_posterior_choroidal_right`

**Description**

Medial posterior choroidal artery: this vessel usually arises from the medial P2 segment but may arise from the parieto-occipital, calcarine, or posterior pericallosal (splenial) branches. It runs medially and supplies the adjacent tectum, pineal gland, habenula and medial geniculate body, and posterior thalamus. It then enters the roof of the third ventricle within the velum interpositum (the small membrane just above and anterior to the pineal gland) to supply the choroid plexus. As it arches over the quadrigeminal plate, it adopts a characteristic ‘3’ shape on a lateral angiographic projection. It runs inferior to the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_right). Terminal branches anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_right) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.amendment.medial_posterior_choroidal_plexal_representative.right"></a>

### Medial posterior choroidal plexal representative right

**Model ID:** `artery.amendment.medial_posterior_choroidal_plexal_representative.right`

**Description**

The [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) enters the roof of the third ventricle within the velum interpositum to supply the choroid plexus. Terminal branches anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_right) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal right](#structure-artery.posterior.medial_posterior_choroidal_right)

<a id="structure-artery.posterior.lateral_posterior_choroidal_right"></a>

### Lateral posterior choroidal right

**Model ID:** `artery.posterior.lateral_posterior_choroidal_right`

**Description**

Lateral posterior choroidal artery: this artery usually arises distal to the [medial posterior choroidal](#structure-artery.posterior.medial_posterior_choroidal_right) but can arise from hippocampal, temporal, and parieto-occipital arteries. It runs superoanterior in the ambient cistern, sending branches to the cerebral peduncle, pineal gland, splenium of the corpus callosum, posterior commissure, tail of the caudate nucleus, lateral geniculate body, and dorsomedial and pulvinar of the thalamus. It then enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.right"></a>

### Lateral posterior choroidal plexal representative right

**Model ID:** `artery.amendment.lateral_posterior_choroidal_plexal_representative.right`

**Description**

The [lateral posterior choroidal artery](#structure-artery.posterior.lateral_posterior_choroidal_right) enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Lateral posterior choroidal right](#structure-artery.posterior.lateral_posterior_choroidal_right)

<a id="structure-artery.posterior.thalamogeniculate_right"></a>

### Thalamogeniculate right

**Model ID:** `artery.posterior.thalamogeniculate_right`

**Description**

Thalamogeniculate perforators (up to 12): these supply the optic tract, medial and lateral geniculate bodies, the lateral and inferior thalamus, and the posterior internal capsule.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.peduncular_perforator_right"></a>

### Peduncular perforator right

**Model ID:** `artery.posterior.peduncular_perforator_right`

**Description**

Peduncular perforating branches: perforators arise from the P1 or P2 segment to supply the cerebral peduncles.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.amendment.davidoff_and_schechter_artery.right"></a>

### Davidoff and Schechter artery right

**Model ID:** `artery.amendment.davidoff_and_schechter_artery.right`

**Description**

Meningeal branch of Davidoff and Schechter: this eponymous branch is named after the mentors of those who first described it. It is a dural artery arising from the PCA near the falcotentorial junction to supply the falx cerebri. Often too small to be seen angiographically, it is more frequently seen in dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [PCA P2-P3 right](#structure-artery.posterior.pca_p2_p3_right)

<a id="structure-artery.posterior.thalamoperforator_1_right"></a>

### Thalamoperforator 1 right

**Model ID:** `artery.posterior.thalamoperforator_1_right`

**Description**

Posterior thalamoperforators (up to eight): these enter the posterior perforated substance, the interpeduncular cistern, and medial cerebral peduncles, and supply the posterior part of the thalamus, posterior part of the optic chiasm and tracts, posterior limb of the internal capsule, hypothalamus, subthalamus, substantia nigra, red nucleus, oculomotor and trochlear nuclei, rostral mesencephalon, and cerebral peduncles. The peduncular supply includes the corticospinal and corticobulbar tracts.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 right](#structure-artery.posterior.pca_p1_right)

<a id="structure-artery.posterior.thalamoperforator_2_right"></a>

### Thalamoperforator 2 right

**Model ID:** `artery.posterior.thalamoperforator_2_right`

**Description**

Posterior thalamoperforators (up to eight): these enter the posterior perforated substance, the interpeduncular cistern, and medial cerebral peduncles, and supply the posterior part of the thalamus, posterior part of the optic chiasm and tracts, posterior limb of the internal capsule, hypothalamus, subthalamus, substantia nigra, red nucleus, oculomotor and trochlear nuclei, rostral mesencephalon, and cerebral peduncles. The peduncular supply includes the corticospinal and corticobulbar tracts.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 right](#structure-artery.posterior.pca_p1_right)

<a id="structure-artery.amendment.pca_short_circumflex.right"></a>

### PCA short circumflex right

**Model ID:** `artery.amendment.pca_short_circumflex.right`

**Description**

Long and short circumflex arteries: these may arise from the P1 or P2 segments and supply the geniculate bodies, peduncle, and tegmentum.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 right](#structure-artery.posterior.pca_p1_right)

<a id="structure-artery.amendment.pca_long_circumflex.right"></a>

### PCA long circumflex right

**Model ID:** `artery.amendment.pca_long_circumflex.right`

**Description**

Long and short circumflex arteries: these may arise from the P1 or P2 segments and supply the geniculate bodies, peduncle, and tegmentum. The long circumflex extends to the colliculi and additionally supplies the tectum.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 right](#structure-artery.posterior.pca_p1_right)

<a id="structure-artery.amendment.pca_collicular.right"></a>

### PCA collicular right

**Model ID:** `artery.amendment.pca_collicular.right`

**Description**

Collicular arteries sometimes arise distinctly from the [P1 segment](#structure-artery.posterior.pca_p1_right) (running medial to P2) or P2 segment. They curve around and send branches to the cerebral peduncle, terminating at the collicular (quadrigeminal) plate. An anastomosis between the PCA and [SCA](#structure-artery.posterior.sca_right) can occur at this location.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA long circumflex right](#structure-artery.amendment.pca_long_circumflex.right)

<a id="structure-artery.posterior.sca_right"></a>

### SCA right

**Model ID:** `artery.posterior.sca_right`

**Description**

The SCA arises near the termination of the [basilar artery](#structure-artery.posterior.basilar) and initially runs parallel and inferior to the PCA, separated by the oculomotor nerve. It deviates laterally in the ambient cistern, running over the middle cerebellar peduncle under the trochlear nerve, before continuing into the quadrigeminal cistern and veering towards the midline.

It supplies the lower midbrain, upper pons, superior vermis, and superior cerebellar hemispheres.

The artery may share a common origin with the PCA or arise from the [P1 segment](#structure-artery.posterior.pca_p1_right), more common in caudal fusion types. It may be duplicated (in up to 28%), and this will correspond to separate origins of the medial and lateral divisions.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.sca_vermian_right"></a>

### SCA vermian right

**Model ID:** `artery.posterior.sca_vermian_right`

**Description**

Superior vermian branch: the terminal branch supplying the vermis and anastomosing with the [AICA](#structure-artery.posterior.aica_right) and [PICA](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.posterior.sca_medial_hemispheric_right"></a>

### SCA medial hemispheric right

**Model ID:** `artery.posterior.sca_medial_hemispheric_right`

**Description**

The medial (rostral) division of the [SCA](#structure-artery.posterior.sca_right) subdivides at the lateral pontomesencephalic level. A lateral branch supplies the superomedial cerebellar hemisphere and superior vermis.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.posterior.sca_rostral_hemispheric_right"></a>

### SCA rostral hemispheric right

**Model ID:** `artery.posterior.sca_rostral_hemispheric_right`

**Description**

The medial (rostral) division of the [SCA](#structure-artery.posterior.sca_right) subdivides at the lateral pontomesencephalic level. A lateral branch supplies the superomedial cerebellar hemisphere and superior vermis.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA medial hemispheric right](#structure-artery.posterior.sca_medial_hemispheric_right)

<a id="structure-artery.posterior.sca_lateral_hemispheric_right"></a>

### SCA lateral hemispheric right

**Model ID:** `artery.posterior.sca_lateral_hemispheric_right`

**Description**

Lateral (caudal marginal) division: this is usually the larger division and supplies the deep nuclei of the cerebellum including the dentate nucleus, and the superolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.posterior.sca_caudal_hemispheric_right"></a>

### SCA caudal hemispheric right

**Model ID:** `artery.posterior.sca_caudal_hemispheric_right`

**Description**

Lateral (caudal marginal) division: this is usually the larger division and supplies the deep nuclei of the cerebellum including the dentate nucleus, and the superolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA lateral hemispheric right](#structure-artery.posterior.sca_lateral_hemispheric_right)

<a id="structure-artery.amendment.sca_proximal_perforator.right"></a>

### SCA proximal perforator right

**Model ID:** `artery.amendment.sca_proximal_perforator.right`

**Description**

Perforators from the proximal [SCA](#structure-artery.posterior.sca_right) to the pons, midbrain, and inferior colliculus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.amendment.sca_tectal_branch.right"></a>

### SCA tectal branch right

**Model ID:** `artery.amendment.sca_tectal_branch.right`

**Description**

A medial branch of the rostral division of the [SCA](#structure-artery.posterior.sca_right) supplies the tectal anastomotic network that supplies the colliculi, occasionally anastomosing with collicular branches of the PCA, and the superior cerebellar peduncle.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.right"></a>

### Wollschlaeger and Wollschlaeger artery right

**Model ID:** `artery.amendment.wollschlaeger_and_wollschlaeger_artery.right`

**Description**

The artery of Wollschlaeger and Wollschlaeger: this dural branch arises from the lateral pontomesencephalic segment of the [SCA](#structure-artery.posterior.sca_right). It runs through the ambient cistern to supply the medial tentorium.

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [SCA right](#structure-artery.posterior.sca_right)

<a id="structure-artery.posterior.aica_right"></a>

### AICA right

**Model ID:** `artery.posterior.aica_right`

**Description**

The AICA arises from the lower or mid-third of the [basilar artery](#structure-artery.posterior.basilar) and runs over the anterolateral surface of the pons. It supplies the inferior and middle cerebellar peduncles, the inferior flocculus, the choroid plexus of the fourth ventricle, and the cerebellar hemisphere.

It may be duplicated or arise from a common trunk with the [PICA](#structure-artery.posterior.pica_right) (AICA-PICA trunk).

There are anastomoses with branches of the [PICA](#structure-artery.posterior.pica_right) and [SCA](#structure-artery.posterior.sca_right).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.labyrinthine_right"></a>

### Labyrinthine right

**Model ID:** `artery.posterior.labyrinthine_right`

**Description**

The internal auditory (labyrinthine) artery arises from the [AICA](#structure-artery.posterior.aica_right) or, less commonly, directly from the [basilar artery](#structure-artery.posterior.basilar). It divides into cochlear and anterior vestibular branches which are the main supply of the cochlea and vestibular apparatus. The internal auditory artery also supplies the facial nerve in the internal auditory canal.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA right](#structure-artery.posterior.aica_right)

<a id="structure-artery.amendment.common_cochlear.right"></a>

### Common cochlear right

**Model ID:** `artery.amendment.common_cochlear.right`

**Description**

The [internal auditory (labyrinthine) artery](#structure-artery.posterior.labyrinthine_right) divides into cochlear and anterior vestibular branches, which are the main supply of the cochlea and vestibular apparatus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Labyrinthine right](#structure-artery.posterior.labyrinthine_right)

<a id="structure-artery.amendment.anterior_vestibular.right"></a>

### Anterior vestibular right

**Model ID:** `artery.amendment.anterior_vestibular.right`

**Description**

The [internal auditory (labyrinthine) artery](#structure-artery.posterior.labyrinthine_right) divides into cochlear and anterior vestibular branches, which are the main supply of the cochlea and vestibular apparatus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Labyrinthine right](#structure-artery.posterior.labyrinthine_right)

<a id="structure-artery.posterior.aica_rostral_branch_right"></a>

### AICA rostral branch right

**Model ID:** `artery.posterior.aica_rostral_branch_right`

**Parent:** [AICA right](#structure-artery.posterior.aica_right)

<a id="structure-artery.amendment.aica_fourth_ventricular_choroidal.right"></a>

### AICA fourth ventricular choroidal right

**Model ID:** `artery.amendment.aica_fourth_ventricular_choroidal.right`

**Description**

The [AICA](#structure-artery.posterior.aica_right) supplies the choroid plexus of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA rostral branch right](#structure-artery.posterior.aica_rostral_branch_right)

<a id="structure-artery.posterior.aica_caudal_branch_right"></a>

### AICA caudal branch right

**Model ID:** `artery.posterior.aica_caudal_branch_right`

**Parent:** [AICA right](#structure-artery.posterior.aica_right)

<a id="structure-artery.amendment.aica_subarcuate.right"></a>

### AICA subarcuate right

**Model ID:** `artery.amendment.aica_subarcuate.right`

**Description**

The subarcuate branch is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA right](#structure-artery.posterior.aica_right)

<a id="structure-artery.posterior.pontine_paramedian_1_right"></a>

### Pontine paramedian 1 right

**Model ID:** `artery.posterior.pontine_paramedian_1_right`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_paramedian_2_right"></a>

### Pontine paramedian 2 right

**Model ID:** `artery.posterior.pontine_paramedian_2_right`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_paramedian_3_right"></a>

### Pontine paramedian 3 right

**Model ID:** `artery.posterior.pontine_paramedian_3_right`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_circumferential_right"></a>

### Pontine circumferential right

**Model ID:** `artery.posterior.pontine_circumferential_right`

**Description**

Short circumflex branches partially encircle the pons.

Long circumflex branches fully encircle it and generally have fewer terminal branches.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.amendment.pontine_short_circumflex.right"></a>

### Pontine short circumflex right

**Model ID:** `artery.amendment.pontine_short_circumflex.right`

**Description**

Short circumflex branches partially encircle the pons.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.amendment.pontine_long_circumflex.right"></a>

### Pontine long circumflex right

**Model ID:** `artery.amendment.pontine_long_circumflex.right`

**Description**

Long circumflex branches fully encircle the pons and generally have fewer terminal branches.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pica_right"></a>

### PICA right

**Model ID:** `artery.posterior.pica_right`

**Description**

The artery most commonly originates from the intradural [vertebral artery](#structure-artery.posterior.vertebral_right), however, its origin is variable. It may arise from the [basilar artery](#structure-artery.posterior.basilar), a joint AICA-PICA trunk, the extradural [vertebral artery](#structure-artery.posterior.vertebral_right) as low as C2, or the ascending cervical, occipital, and [ascending pharyngeal](#structure-artery.eca.apa.right) arteries, or as a remnant of the trigeminal artery.

It may be duplicated or unilaterally or bilaterally absent, in which case its territory is served by another artery, usually the [AICA](#structure-artery.posterior.aica_right).

It supplies the lower medulla, tonsils, vermis, and inferolateral cerebellar hemisphere.

The artery can be anatomically segmented into the following: anterior medullary (anterior to the apex of the inferior olive), lateral medullary (extends from the inferior olive), tonsillomedullary, telovelotonsillar, and cortical.

The first three segments emit perforators to the lateral medulla and anterior and lateral spinal arteries. The perforators may anastomose with those from the vertebral and [basilar artery](#structure-artery.posterior.basilar).

In addition to pial vessels, the posterior meningeal artery may arise from the PICA.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.pica_vermian_right"></a>

### PICA vermian right

**Model ID:** `artery.posterior.pica_vermian_right`

**Description**

The [PICA](#structure-artery.posterior.pica_right) supplies the vermis. Vermian branches may occasionally cross the midline and establish a bilateral supply.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.pica_hemispheric_right"></a>

### PICA hemispheric right

**Model ID:** `artery.posterior.pica_hemispheric_right`

**Description**

The [PICA](#structure-artery.posterior.pica_right) supplies the inferolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.pica_lateral_hemispheric_right"></a>

### PICA lateral hemispheric right

**Model ID:** `artery.posterior.pica_lateral_hemispheric_right`

**Description**

The [PICA](#structure-artery.posterior.pica_right) supplies the inferolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA hemispheric right](#structure-artery.posterior.pica_hemispheric_right)

<a id="structure-artery.posterior.pica_tonsillar_right"></a>

### PICA tonsillar right

**Model ID:** `artery.posterior.pica_tonsillar_right`

**Description**

The [PICA](#structure-artery.posterior.pica_right) supplies the cerebellar tonsils.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.pica_choroidal_right"></a>

### PICA choroidal right

**Model ID:** `artery.posterior.pica_choroidal_right`

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.pica_medullary_perforator_right"></a>

### PICA medullary perforator right

**Model ID:** `artery.posterior.pica_medullary_perforator_right`

**Description**

The first three [PICA](#structure-artery.posterior.pica_right) segments emit perforators to the lateral medulla and anterior and lateral spinal arteries. The perforators may anastomose with those from the vertebral and [basilar artery](#structure-artery.posterior.basilar).

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.anterior_spinal_root_right"></a>

### Anterior spinal root right

**Model ID:** `artery.posterior.anterior_spinal_root_right`

**Description**

[Anterior spinal artery](#structure-artery.posterior.anterior_spinal) ([ASA](#structure-artery.posterior.anterior_spinal)): the [anterior spinal axis](#structure-artery.posterior.anterior_spinal) originates from the [vertebral artery](#structure-artery.posterior.vertebral_right) usually on the side with the dominant [PICA](#structure-artery.posterior.pica_right), typically at the vertebrobasilar junction. Where there is no dominant [PICA](#structure-artery.posterior.pica_right), it may arise symmetrically from both vertebral arteries, uniting to form a single vessel at C2-C4. There are anastomoses in the midline with other radiculomedullary arteries, particularly the artery of the cervical enlargement.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.posterior_spinal_right"></a>

### Posterior spinal right

**Model ID:** `artery.posterior.posterior_spinal_right`

**Description**

The PSAs are positioned off midline, and hence identifiable on carefully performed true AP spinal angiography. They are sometimes visible arising from the intradural vertebral arteries or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_right), particularly in the presence of cervical AVMs. In the non-pathological state, they are small and measure <0.5 mm.

The PSAs and contributing radiculopial arteries create a network to supply the circumference of the periphery of the cord in a centripetal manner. In this instance, the network is analogous to the M2 perforators as they pass into the insular cortex from the Sylvian fissure.

The PSAs principally supply the posterior third of the cord, including the dorsal columns, dorsal grey matter, and dorsal aspects of the lateral columns.

**Source:** `nv(2).pdf`, PDF pages 74–75; printed pages 80–81.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.va_muscular_c1_right"></a>

### VA muscular C1 right

**Model ID:** `artery.posterior.va_muscular_c1_right`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_right) gives muscular branches to paraspinal arteries. There are extensive anastomoses with other arteries in the neck, particularly the ascending cervical, deep cervical, [ascending pharyngeal](#structure-artery.eca.apa.right), contralateral vertebral, and [occipital arteries](#structure-artery.eca.occipital.right).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.va_muscular_c2_right"></a>

### VA muscular C2 right

**Model ID:** `artery.posterior.va_muscular_c2_right`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_right) gives muscular branches to paraspinal arteries. There are extensive anastomoses with other arteries in the neck, particularly the ascending cervical, deep cervical, [ascending pharyngeal](#structure-artery.eca.apa.right), contralateral vertebral, and [occipital arteries](#structure-artery.eca.occipital.right).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.va_odontoid_contribution_right"></a>

### VA odontoid contribution right

**Model ID:** `artery.posterior.va_odontoid_contribution_right`

**Description**

The C3 radicular spinal arteries participate in the odontoid arterial arcade (also formed from branches of the [ascending pharyngeal](#structure-artery.eca.apa.right) and [occipital arteries](#structure-artery.eca.occipital.right)).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.posterior.posterior_meningeal_va_right"></a>

### Posterior meningeal VA right

**Model ID:** `artery.posterior.posterior_meningeal_va_right`

**Description**

Posterior meningeal artery: the posterior meningeal artery supplies the tentorium cerebelli and may originate from the extracranial [vertebral artery](#structure-artery.posterior.vertebral_right), the [occipital artery](#structure-artery.eca.occipital.right), the [ascending pharyngeal artery](#structure-artery.eca.apa.right), or the [PICA](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.amendment.va_anterior_meningeal.right"></a>

### VA anterior meningeal right

**Model ID:** `artery.amendment.va_anterior_meningeal.right`

**Description**

Anterior meningeal branch of the [vertebral artery](#structure-artery.posterior.vertebral_right): this is a small branch of the distal [vertebral artery](#structure-artery.posterior.vertebral_right) that contributes to the dura of the anterior [foramen magnum](#structure-landmark.foramen-magnum.midline).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.amendment.va_medullary_perforator_1.right"></a>

### VA medullary perforator 1 right

**Model ID:** `artery.amendment.va_medullary_perforator_1.right`

**Description**

Perforators supplying the medulla and pyramids traverse the foramen caecum on the anterior medulla at the pontomedullary junction and penetrates all the way back to the tegmentum and floor of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.amendment.va_medullary_perforator_2.right"></a>

### VA medullary perforator 2 right

**Model ID:** `artery.amendment.va_medullary_perforator_2.right`

**Description**

Perforators supplying the medulla and pyramids traverse the foramen caecum on the anterior medulla at the pontomedullary junction and penetrates all the way back to the tegmentum and floor of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="vertebrobasilar-left"></a>

## Vertebrobasilar arteries and branches, left

<a id="structure-artery.posterior.pcom_perforator_left"></a>

### PCom perforator left

**Model ID:** `artery.posterior.pcom_perforator_left`

**Description**

The anterior thalamoperforators of the [PCOM](#structure-artery.anterior.posterior_communicating_left) arise from the superolateral aspect and a particularly prominent one is the [tuberothalamic artery](#structure-artery.amendment.tuberothalamic_artery.left), which supplies the anterior thalamus, reticular nucleus, and mammillothalamic tract. The anterior thalamoperforating group also supply the posterior optic chiasm, proximal optic radiations, posterior hypothalamus, and cerebral peduncle. They anastomose with choroidal arteries.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Posterior communicating left](#structure-artery.anterior.posterior_communicating_left)

<a id="structure-artery.posterior.pca_p1_left"></a>

### PCA P1 left

**Model ID:** `artery.posterior.pca_p1_left`

**Description**

Originating at the basilar bifurcation, the P1 segment runs within the interpeduncular cistern and terminates at the [PCOM](#structure-artery.anterior.posterior_communicating_left) insertion.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pca_p2_p3_left"></a>

### PCA P2-P3 left

**Model ID:** `artery.posterior.pca_p2_p3_left`

**Description**

P2 courses around the midbrain, under the thalamus, running in the crural and ambient cisterns. Branches supply the thalamus, cerebral peduncle, and quadrigeminal plate.

The P3 segment runs posteromedially in the quadrigeminal cistern.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P1 left](#structure-artery.posterior.pca_p1_left)

<a id="structure-artery.posterior.pca_calcarine_left"></a>

### PCA calcarine left

**Model ID:** `artery.posterior.pca_calcarine_left`

**Description**

Calcarine: this runs initially inferior and lateral to the [parieto-occipital artery](#structure-artery.posterior.pca_parieto_occipital_left) within the calcarine fissure to supply the visual cortex, cuneus, and lingual gyrus. It occasionally originates from the parieto-occipital or posterior temporal arteries.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.calcarine_superior_cortical_left"></a>

### Calcarine superior cortical left

**Model ID:** `artery.posterior.calcarine_superior_cortical_left`

**Parent:** [PCA calcarine left](#structure-artery.posterior.pca_calcarine_left)

<a id="structure-artery.posterior.calcarine_inferior_cortical_left"></a>

### Calcarine inferior cortical left

**Model ID:** `artery.posterior.calcarine_inferior_cortical_left`

**Parent:** [PCA calcarine left](#structure-artery.posterior.pca_calcarine_left)

<a id="structure-artery.posterior.pca_parieto_occipital_left"></a>

### PCA parieto-occipital left

**Model ID:** `artery.posterior.pca_parieto_occipital_left`

**Description**

Parieto-occipital: usually the largest of the terminal branches, it runs initially superior and medial to the [calcarine artery](#structure-artery.posterior.pca_calcarine_left) in the parieto-occipital fissure. The artery supplies the cuneus, precuneus, and superior occipital gyrus of the occipital lobe. It may also give branches to the precentral gyrus, superior parietal lobule, and an accessory calcarine branch to the visual cortex.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.parieto_occipital_cuneal_left"></a>

### Parieto-occipital cuneal left

**Model ID:** `artery.posterior.parieto_occipital_cuneal_left`

**Parent:** [PCA parieto-occipital left](#structure-artery.posterior.pca_parieto_occipital_left)

<a id="structure-artery.posterior.pca_anterior_inferior_temporal_left"></a>

### PCA anterior inferior temporal left

**Model ID:** `artery.posterior.pca_anterior_inferior_temporal_left`

**Description**

The anterior temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.pca_middle_inferior_temporal_left"></a>

### PCA middle inferior temporal left

**Model ID:** `artery.posterior.pca_middle_inferior_temporal_left`

**Description**

The middle temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.pca_posterior_inferior_temporal_left"></a>

### PCA posterior inferior temporal left

**Model ID:** `artery.posterior.pca_posterior_inferior_temporal_left`

**Description**

The posterior temporal artery is a cortical branch of the PCA supplying the corresponding part of the temporal lobe.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.pca_lateral_occipital_left"></a>

### PCA lateral occipital left

**Model ID:** `artery.posterior.pca_lateral_occipital_left`

**Parent:** [PCA posterior inferior temporal left](#structure-artery.posterior.pca_posterior_inferior_temporal_left)

<a id="structure-artery.posterior.pca_splenial_left"></a>

### PCA splenial left

**Model ID:** `artery.posterior.pca_splenial_left`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.pca_hippocampal_left"></a>

### PCA hippocampal left

**Model ID:** `artery.posterior.pca_hippocampal_left`

**Description**

Hippocampal: supplying the hippocampus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.medial_posterior_choroidal_left"></a>

### Medial posterior choroidal left

**Model ID:** `artery.posterior.medial_posterior_choroidal_left`

**Description**

Medial posterior choroidal artery: this vessel usually arises from the medial P2 segment but may arise from the parieto-occipital, calcarine, or posterior pericallosal (splenial) branches. It runs medially and supplies the adjacent tectum, pineal gland, habenula and medial geniculate body, and posterior thalamus. It then enters the roof of the third ventricle within the velum interpositum (the small membrane just above and anterior to the pineal gland) to supply the choroid plexus. As it arches over the quadrigeminal plate, it adopts a characteristic ‘3’ shape on a lateral angiographic projection. It runs inferior to the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_left). Terminal branches anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_left) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.amendment.medial_posterior_choroidal_plexal_representative.left"></a>

### Medial posterior choroidal plexal representative left

**Model ID:** `artery.amendment.medial_posterior_choroidal_plexal_representative.left`

**Description**

The [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) enters the roof of the third ventricle within the velum interpositum to supply the choroid plexus. Terminal branches anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_left) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal left](#structure-artery.posterior.medial_posterior_choroidal_left)

<a id="structure-artery.posterior.lateral_posterior_choroidal_left"></a>

### Lateral posterior choroidal left

**Model ID:** `artery.posterior.lateral_posterior_choroidal_left`

**Description**

Lateral posterior choroidal artery: this artery usually arises distal to the [medial posterior choroidal](#structure-artery.posterior.medial_posterior_choroidal_left) but can arise from hippocampal, temporal, and parieto-occipital arteries. It runs superoanterior in the ambient cistern, sending branches to the cerebral peduncle, pineal gland, splenium of the corpus callosum, posterior commissure, tail of the caudate nucleus, lateral geniculate body, and dorsomedial and pulvinar of the thalamus. It then enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.left"></a>

### Lateral posterior choroidal plexal representative left

**Model ID:** `artery.amendment.lateral_posterior_choroidal_plexal_representative.left`

**Description**

The [lateral posterior choroidal artery](#structure-artery.posterior.lateral_posterior_choroidal_left) enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Lateral posterior choroidal left](#structure-artery.posterior.lateral_posterior_choroidal_left)

<a id="structure-artery.posterior.thalamogeniculate_left"></a>

### Thalamogeniculate left

**Model ID:** `artery.posterior.thalamogeniculate_left`

**Description**

Thalamogeniculate perforators (up to 12): these supply the optic tract, medial and lateral geniculate bodies, the lateral and inferior thalamus, and the posterior internal capsule.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.peduncular_perforator_left"></a>

### Peduncular perforator left

**Model ID:** `artery.posterior.peduncular_perforator_left`

**Description**

Peduncular perforating branches: perforators arise from the P1 or P2 segment to supply the cerebral peduncles.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.amendment.davidoff_and_schechter_artery.left"></a>

### Davidoff and Schechter artery left

**Model ID:** `artery.amendment.davidoff_and_schechter_artery.left`

**Description**

Meningeal branch of Davidoff and Schechter: this eponymous branch is named after the mentors of those who first described it. It is a dural artery arising from the PCA near the falcotentorial junction to supply the falx cerebri. Often too small to be seen angiographically, it is more frequently seen in dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [PCA P2-P3 left](#structure-artery.posterior.pca_p2_p3_left)

<a id="structure-artery.posterior.thalamoperforator_1_left"></a>

### Thalamoperforator 1 left

**Model ID:** `artery.posterior.thalamoperforator_1_left`

**Description**

Posterior thalamoperforators (up to eight): these enter the posterior perforated substance, the interpeduncular cistern, and medial cerebral peduncles, and supply the posterior part of the thalamus, posterior part of the optic chiasm and tracts, posterior limb of the internal capsule, hypothalamus, subthalamus, substantia nigra, red nucleus, oculomotor and trochlear nuclei, rostral mesencephalon, and cerebral peduncles. The peduncular supply includes the corticospinal and corticobulbar tracts.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 left](#structure-artery.posterior.pca_p1_left)

<a id="structure-artery.posterior.thalamoperforator_2_left"></a>

### Thalamoperforator 2 left

**Model ID:** `artery.posterior.thalamoperforator_2_left`

**Description**

Posterior thalamoperforators (up to eight): these enter the posterior perforated substance, the interpeduncular cistern, and medial cerebral peduncles, and supply the posterior part of the thalamus, posterior part of the optic chiasm and tracts, posterior limb of the internal capsule, hypothalamus, subthalamus, substantia nigra, red nucleus, oculomotor and trochlear nuclei, rostral mesencephalon, and cerebral peduncles. The peduncular supply includes the corticospinal and corticobulbar tracts.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 left](#structure-artery.posterior.pca_p1_left)

<a id="structure-artery.amendment.pca_short_circumflex.left"></a>

### PCA short circumflex left

**Model ID:** `artery.amendment.pca_short_circumflex.left`

**Description**

Long and short circumflex arteries: these may arise from the P1 or P2 segments and supply the geniculate bodies, peduncle, and tegmentum.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 left](#structure-artery.posterior.pca_p1_left)

<a id="structure-artery.amendment.pca_long_circumflex.left"></a>

### PCA long circumflex left

**Model ID:** `artery.amendment.pca_long_circumflex.left`

**Description**

Long and short circumflex arteries: these may arise from the P1 or P2 segments and supply the geniculate bodies, peduncle, and tegmentum. The long circumflex extends to the colliculi and additionally supplies the tectum.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA P1 left](#structure-artery.posterior.pca_p1_left)

<a id="structure-artery.amendment.pca_collicular.left"></a>

### PCA collicular left

**Model ID:** `artery.amendment.pca_collicular.left`

**Description**

Collicular arteries sometimes arise distinctly from the [P1 segment](#structure-artery.posterior.pca_p1_left) (running medial to P2) or P2 segment. They curve around and send branches to the cerebral peduncle, terminating at the collicular (quadrigeminal) plate. An anastomosis between the PCA and [SCA](#structure-artery.posterior.sca_left) can occur at this location.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA long circumflex left](#structure-artery.amendment.pca_long_circumflex.left)

<a id="structure-artery.posterior.sca_left"></a>

### SCA left

**Model ID:** `artery.posterior.sca_left`

**Description**

The SCA arises near the termination of the [basilar artery](#structure-artery.posterior.basilar) and initially runs parallel and inferior to the PCA, separated by the oculomotor nerve. It deviates laterally in the ambient cistern, running over the middle cerebellar peduncle under the trochlear nerve, before continuing into the quadrigeminal cistern and veering towards the midline.

It supplies the lower midbrain, upper pons, superior vermis, and superior cerebellar hemispheres.

The artery may share a common origin with the PCA or arise from the [P1 segment](#structure-artery.posterior.pca_p1_left), more common in caudal fusion types. It may be duplicated (in up to 28%), and this will correspond to separate origins of the medial and lateral divisions.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.sca_vermian_left"></a>

### SCA vermian left

**Model ID:** `artery.posterior.sca_vermian_left`

**Description**

Superior vermian branch: the terminal branch supplying the vermis and anastomosing with the [AICA](#structure-artery.posterior.aica_left) and [PICA](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.posterior.sca_medial_hemispheric_left"></a>

### SCA medial hemispheric left

**Model ID:** `artery.posterior.sca_medial_hemispheric_left`

**Description**

The medial (rostral) division of the [SCA](#structure-artery.posterior.sca_left) subdivides at the lateral pontomesencephalic level. A lateral branch supplies the superomedial cerebellar hemisphere and superior vermis.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.posterior.sca_rostral_hemispheric_left"></a>

### SCA rostral hemispheric left

**Model ID:** `artery.posterior.sca_rostral_hemispheric_left`

**Description**

The medial (rostral) division of the [SCA](#structure-artery.posterior.sca_left) subdivides at the lateral pontomesencephalic level. A lateral branch supplies the superomedial cerebellar hemisphere and superior vermis.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA medial hemispheric left](#structure-artery.posterior.sca_medial_hemispheric_left)

<a id="structure-artery.posterior.sca_lateral_hemispheric_left"></a>

### SCA lateral hemispheric left

**Model ID:** `artery.posterior.sca_lateral_hemispheric_left`

**Description**

Lateral (caudal marginal) division: this is usually the larger division and supplies the deep nuclei of the cerebellum including the dentate nucleus, and the superolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.posterior.sca_caudal_hemispheric_left"></a>

### SCA caudal hemispheric left

**Model ID:** `artery.posterior.sca_caudal_hemispheric_left`

**Description**

Lateral (caudal marginal) division: this is usually the larger division and supplies the deep nuclei of the cerebellum including the dentate nucleus, and the superolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA lateral hemispheric left](#structure-artery.posterior.sca_lateral_hemispheric_left)

<a id="structure-artery.amendment.sca_proximal_perforator.left"></a>

### SCA proximal perforator left

**Model ID:** `artery.amendment.sca_proximal_perforator.left`

**Description**

Perforators from the proximal [SCA](#structure-artery.posterior.sca_left) to the pons, midbrain, and inferior colliculus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.amendment.sca_tectal_branch.left"></a>

### SCA tectal branch left

**Model ID:** `artery.amendment.sca_tectal_branch.left`

**Description**

A medial branch of the rostral division of the [SCA](#structure-artery.posterior.sca_left) supplies the tectal anastomotic network that supplies the colliculi, occasionally anastomosing with collicular branches of the PCA, and the superior cerebellar peduncle.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.left"></a>

### Wollschlaeger and Wollschlaeger artery left

**Model ID:** `artery.amendment.wollschlaeger_and_wollschlaeger_artery.left`

**Description**

The artery of Wollschlaeger and Wollschlaeger: this dural branch arises from the lateral pontomesencephalic segment of the [SCA](#structure-artery.posterior.sca_left). It runs through the ambient cistern to supply the medial tentorium.

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [SCA left](#structure-artery.posterior.sca_left)

<a id="structure-artery.posterior.aica_left"></a>

### AICA left

**Model ID:** `artery.posterior.aica_left`

**Description**

The AICA arises from the lower or mid-third of the [basilar artery](#structure-artery.posterior.basilar) and runs over the anterolateral surface of the pons. It supplies the inferior and middle cerebellar peduncles, the inferior flocculus, the choroid plexus of the fourth ventricle, and the cerebellar hemisphere.

It may be duplicated or arise from a common trunk with the [PICA](#structure-artery.posterior.pica_left) (AICA-PICA trunk).

There are anastomoses with branches of the [PICA](#structure-artery.posterior.pica_left) and [SCA](#structure-artery.posterior.sca_left).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.labyrinthine_left"></a>

### Labyrinthine left

**Model ID:** `artery.posterior.labyrinthine_left`

**Description**

The internal auditory (labyrinthine) artery arises from the [AICA](#structure-artery.posterior.aica_left) or, less commonly, directly from the [basilar artery](#structure-artery.posterior.basilar). It divides into cochlear and anterior vestibular branches which are the main supply of the cochlea and vestibular apparatus. The internal auditory artery also supplies the facial nerve in the internal auditory canal.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA left](#structure-artery.posterior.aica_left)

<a id="structure-artery.amendment.common_cochlear.left"></a>

### Common cochlear left

**Model ID:** `artery.amendment.common_cochlear.left`

**Description**

The [internal auditory (labyrinthine) artery](#structure-artery.posterior.labyrinthine_left) divides into cochlear and anterior vestibular branches, which are the main supply of the cochlea and vestibular apparatus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Labyrinthine left](#structure-artery.posterior.labyrinthine_left)

<a id="structure-artery.amendment.anterior_vestibular.left"></a>

### Anterior vestibular left

**Model ID:** `artery.amendment.anterior_vestibular.left`

**Description**

The [internal auditory (labyrinthine) artery](#structure-artery.posterior.labyrinthine_left) divides into cochlear and anterior vestibular branches, which are the main supply of the cochlea and vestibular apparatus.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [Labyrinthine left](#structure-artery.posterior.labyrinthine_left)

<a id="structure-artery.posterior.aica_rostral_branch_left"></a>

### AICA rostral branch left

**Model ID:** `artery.posterior.aica_rostral_branch_left`

**Parent:** [AICA left](#structure-artery.posterior.aica_left)

<a id="structure-artery.amendment.aica_fourth_ventricular_choroidal.left"></a>

### AICA fourth ventricular choroidal left

**Model ID:** `artery.amendment.aica_fourth_ventricular_choroidal.left`

**Description**

The [AICA](#structure-artery.posterior.aica_left) supplies the choroid plexus of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA rostral branch left](#structure-artery.posterior.aica_rostral_branch_left)

<a id="structure-artery.posterior.aica_caudal_branch_left"></a>

### AICA caudal branch left

**Model ID:** `artery.posterior.aica_caudal_branch_left`

**Parent:** [AICA left](#structure-artery.posterior.aica_left)

<a id="structure-artery.amendment.aica_subarcuate.left"></a>

### AICA subarcuate left

**Model ID:** `artery.amendment.aica_subarcuate.left`

**Description**

The subarcuate branch is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right.left) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA left](#structure-artery.posterior.aica_left)

<a id="structure-artery.posterior.pontine_paramedian_1_left"></a>

### Pontine paramedian 1 left

**Model ID:** `artery.posterior.pontine_paramedian_1_left`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_paramedian_2_left"></a>

### Pontine paramedian 2 left

**Model ID:** `artery.posterior.pontine_paramedian_2_left`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_paramedian_3_left"></a>

### Pontine paramedian 3 left

**Model ID:** `artery.posterior.pontine_paramedian_3_left`

**Description**

Paramedian branches enter the pons off-centre.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.pontine_circumferential_left"></a>

### Pontine circumferential left

**Model ID:** `artery.posterior.pontine_circumferential_left`

**Description**

Short circumflex branches partially encircle the pons.

Long circumflex branches fully encircle it and generally have fewer terminal branches.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.amendment.pontine_short_circumflex.left"></a>

### Pontine short circumflex left

**Model ID:** `artery.amendment.pontine_short_circumflex.left`

**Description**

Short circumflex branches partially encircle the pons.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.amendment.pontine_long_circumflex.left"></a>

### Pontine long circumflex left

**Model ID:** `artery.amendment.pontine_long_circumflex.left`

**Description**

Long circumflex branches fully encircle the pons and generally have fewer terminal branches.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.vertebral_left"></a>

### Vertebral left

**Model ID:** `artery.posterior.vertebral_left`

**Description**

The vertebral artery can be divided into four segments .

This segment extends until the artery enters the foramen in the transverse process, typically at the C6 level (C4 if the vertebral artery arises from the aortic arch).

The artery continues vertically upwards to the C2 transverse foramina, surrounded by the vertebral venous plexus.

Starts at the foramen transversarium of the axis (C2). The artery turns laterally and ascends, passing through the transverse foramen of the atlas (C1). It then curves medially and is directed towards the [foramen magnum](#structure-landmark.foramen-magnum.midline). It imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the [arcuate foramen](#structure-landmark.arcuate-foramen.left) (a possible risk factor for paediatric ischaemic stroke).

This segment pierces the atlanto-occipital membrane to become intradural (where it is focally smoothly narrowed), entering the cranial cavity via the [foramen magnum](#structure-landmark.foramen-magnum.midline). It continues medially until it joins its counterpart to form the [basilar artery](#structure-artery.posterior.basilar) at the upper edge of the medulla oblongata.

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Arteries](#structure-artery)

<a id="structure-artery.posterior.pica_left"></a>

### PICA left

**Model ID:** `artery.posterior.pica_left`

**Description**

The artery most commonly originates from the intradural [vertebral artery](#structure-artery.posterior.vertebral_left), however, its origin is variable. It may arise from the [basilar artery](#structure-artery.posterior.basilar), a joint AICA-PICA trunk, the extradural [vertebral artery](#structure-artery.posterior.vertebral_left) as low as C2, or the ascending cervical, occipital, and [ascending pharyngeal](#structure-artery.eca.apa.right.left) arteries, or as a remnant of the trigeminal artery.

It may be duplicated or unilaterally or bilaterally absent, in which case its territory is served by another artery, usually the [AICA](#structure-artery.posterior.aica_left).

It supplies the lower medulla, tonsils, vermis, and inferolateral cerebellar hemisphere.

The artery can be anatomically segmented into the following: anterior medullary (anterior to the apex of the inferior olive), lateral medullary (extends from the inferior olive), tonsillomedullary, telovelotonsillar, and cortical.

The first three segments emit perforators to the lateral medulla and anterior and lateral spinal arteries. The perforators may anastomose with those from the vertebral and [basilar artery](#structure-artery.posterior.basilar).

In addition to pial vessels, the posterior meningeal artery may arise from the PICA.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.pica_vermian_left"></a>

### PICA vermian left

**Model ID:** `artery.posterior.pica_vermian_left`

**Description**

The [PICA](#structure-artery.posterior.pica_left) supplies the vermis. Vermian branches may occasionally cross the midline and establish a bilateral supply.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="structure-artery.posterior.pica_hemispheric_left"></a>

### PICA hemispheric left

**Model ID:** `artery.posterior.pica_hemispheric_left`

**Description**

The [PICA](#structure-artery.posterior.pica_left) supplies the inferolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="structure-artery.posterior.pica_lateral_hemispheric_left"></a>

### PICA lateral hemispheric left

**Model ID:** `artery.posterior.pica_lateral_hemispheric_left`

**Description**

The [PICA](#structure-artery.posterior.pica_left) supplies the inferolateral cerebellar hemisphere.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA hemispheric left](#structure-artery.posterior.pica_hemispheric_left)

<a id="structure-artery.posterior.pica_tonsillar_left"></a>

### PICA tonsillar left

**Model ID:** `artery.posterior.pica_tonsillar_left`

**Description**

The [PICA](#structure-artery.posterior.pica_left) supplies the cerebellar tonsils.

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="structure-artery.posterior.pica_choroidal_left"></a>

### PICA choroidal left

**Model ID:** `artery.posterior.pica_choroidal_left`

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="structure-artery.posterior.pica_medullary_perforator_left"></a>

### PICA medullary perforator left

**Model ID:** `artery.posterior.pica_medullary_perforator_left`

**Description**

The first three [PICA](#structure-artery.posterior.pica_left) segments emit perforators to the lateral medulla and anterior and lateral spinal arteries. The perforators may anastomose with those from the vertebral and [basilar artery](#structure-artery.posterior.basilar).

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="structure-artery.posterior.anterior_spinal_root_left"></a>

### Anterior spinal root left

**Model ID:** `artery.posterior.anterior_spinal_root_left`

**Description**

[Anterior spinal artery](#structure-artery.posterior.anterior_spinal) ([ASA](#structure-artery.posterior.anterior_spinal)): the [anterior spinal axis](#structure-artery.posterior.anterior_spinal) originates from the [vertebral artery](#structure-artery.posterior.vertebral_left) usually on the side with the dominant [PICA](#structure-artery.posterior.pica_left), typically at the vertebrobasilar junction. Where there is no dominant [PICA](#structure-artery.posterior.pica_left), it may arise symmetrically from both vertebral arteries, uniting to form a single vessel at C2-C4. There are anastomoses in the midline with other radiculomedullary arteries, particularly the artery of the cervical enlargement.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.posterior_spinal_left"></a>

### Posterior spinal left

**Model ID:** `artery.posterior.posterior_spinal_left`

**Description**

The PSAs are positioned off midline, and hence identifiable on carefully performed true AP spinal angiography. They are sometimes visible arising from the intradural vertebral arteries or [posterior inferior cerebellar arteries](#structure-artery.posterior.pica_left), particularly in the presence of cervical AVMs. In the non-pathological state, they are small and measure <0.5 mm.

The PSAs and contributing radiculopial arteries create a network to supply the circumference of the periphery of the cord in a centripetal manner. In this instance, the network is analogous to the M2 perforators as they pass into the insular cortex from the Sylvian fissure.

The PSAs principally supply the posterior third of the cord, including the dorsal columns, dorsal grey matter, and dorsal aspects of the lateral columns.

**Source:** `nv(2).pdf`, PDF pages 74–75; printed pages 80–81.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.va_muscular_c1_left"></a>

### VA muscular C1 left

**Model ID:** `artery.posterior.va_muscular_c1_left`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_left) gives muscular branches to paraspinal arteries. There are extensive anastomoses with other arteries in the neck, particularly the ascending cervical, deep cervical, [ascending pharyngeal](#structure-artery.eca.apa.right.left), contralateral vertebral, and [occipital arteries](#structure-artery.eca.occipital.right.left).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.va_muscular_c2_left"></a>

### VA muscular C2 left

**Model ID:** `artery.posterior.va_muscular_c2_left`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_left) gives muscular branches to paraspinal arteries. There are extensive anastomoses with other arteries in the neck, particularly the ascending cervical, deep cervical, [ascending pharyngeal](#structure-artery.eca.apa.right.left), contralateral vertebral, and [occipital arteries](#structure-artery.eca.occipital.right.left).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.va_odontoid_contribution_left"></a>

### VA odontoid contribution left

**Model ID:** `artery.posterior.va_odontoid_contribution_left`

**Description**

The C3 radicular spinal arteries participate in the odontoid arterial arcade (also formed from branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left) and [occipital arteries](#structure-artery.eca.occipital.right.left)).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.posterior.posterior_meningeal_va_left"></a>

### Posterior meningeal VA left

**Model ID:** `artery.posterior.posterior_meningeal_va_left`

**Description**

Posterior meningeal artery: the posterior meningeal artery supplies the tentorium cerebelli and may originate from the extracranial [vertebral artery](#structure-artery.posterior.vertebral_left), the [occipital artery](#structure-artery.eca.occipital.right.left), the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left), or the [PICA](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.amendment.va_anterior_meningeal.left"></a>

### VA anterior meningeal left

**Model ID:** `artery.amendment.va_anterior_meningeal.left`

**Description**

Anterior meningeal branch of the [vertebral artery](#structure-artery.posterior.vertebral_left): this is a small branch of the distal [vertebral artery](#structure-artery.posterior.vertebral_left) that contributes to the dura of the anterior [foramen magnum](#structure-landmark.foramen-magnum.midline).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.amendment.va_medullary_perforator_1.left"></a>

### VA medullary perforator 1 left

**Model ID:** `artery.amendment.va_medullary_perforator_1.left`

**Description**

Perforators supplying the medulla and pyramids traverse the foramen caecum on the anterior medulla at the pontomedullary junction and penetrates all the way back to the tegmentum and floor of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="structure-artery.amendment.va_medullary_perforator_2.left"></a>

### VA medullary perforator 2 left

**Model ID:** `artery.amendment.va_medullary_perforator_2.left`

**Description**

Perforators supplying the medulla and pyramids traverse the foramen caecum on the anterior medulla at the pontomedullary junction and penetrates all the way back to the tegmentum and floor of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 42; printed page 48.

**Parent:** [Vertebral left](#structure-artery.posterior.vertebral_left)

<a id="midline-arteries"></a>

## Midline arteries

<a id="structure-artery.anterior.anterior_communicating"></a>

### Anterior communicating

**Model ID:** `artery.anterior.anterior_communicating`

**Description**

The ACOM varies in size and multiplicity and joins the A1 segments across the midline in the chiasmatic cistern above the optic chiasm. Usually, multiple small perforating branches arise from it supplying the septum pellucidum, corpus callosum, lamina terminalis, optic chiasm, and hypothalamus. The [subcallosal artery](#structure-artery.amendment.subcallosal_artery.midline), which supplies the rostrum and genu of the corpus callosum, is usually the largest single such branch.

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [ACA A1 right](#structure-artery.anterior.aca_a1_right)

<a id="structure-artery.amendment.subcallosal_artery.midline"></a>

### Subcallosal artery

**Model ID:** `artery.amendment.subcallosal_artery.midline`

**Description**

The subcallosal artery, which supplies the rostrum and genu of the corpus callosum, is usually the largest single perforating branch of the [ACOM](#structure-artery.anterior.anterior_communicating).

**Source:** `nv(2).pdf`, PDF pages 35–36; printed pages 41–42.

**Parent:** [Anterior communicating](#structure-artery.anterior.anterior_communicating)

<a id="structure-artery.posterior.basilar"></a>

### Basilar

**Model ID:** `artery.posterior.basilar`

**Description**

The basilar artery arises at the pontomedullary junction. It runs over the surface of the pons and divides into the PCAs approximately at the level of the superior surface of the dorsum sella.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Vertebral right](#structure-artery.posterior.vertebral_right)

<a id="structure-artery.amendment.pontine_median_perforator.midline"></a>

### Pontine median perforator

**Model ID:** `artery.amendment.pontine_median_perforator.midline`

**Description**

Median branches penetrate the pons directly in the midline and are visible only when the [basilar artery](#structure-artery.posterior.basilar) is retracted. They penetrate to the floor of the fourth ventricle.

**Source:** `nv(2).pdf`, PDF page 45; printed page 51.

**Parent:** [Basilar](#structure-artery.posterior.basilar)

<a id="structure-artery.posterior.anterior_spinal"></a>

### Anterior spinal

**Model ID:** `artery.posterior.anterior_spinal`

**Description**

Anterior spinal artery (ASA): the anterior spinal axis originates from the vertebral artery usually on the side with the dominant PICA, typically at the vertebrobasilar junction. Where there is no dominant PICA, it may arise symmetrically from both vertebral arteries, uniting to form a single vessel at C2-C4. There are anastomoses in the midline with other radiculomedullary arteries, particularly the artery of the cervical enlargement.

The ASA measures up to 0.8 mm in size, and receives contributions from 2-5 cervical sources, where it is richly vascularised.

The ASA terminates at the conus in a basket of arteries which anastomose with the posterior spinal arteries (PSAs). Occasionally, a small filum terminalis artery can persist, passing inferiorly.

**Source:** `nv(2).pdf`, PDF pages 42, 74; printed pages 48, 80.

**Parent:** [Anterior spinal root right](#structure-artery.posterior.anterior_spinal_root_right)

<a id="connections-right"></a>

## Potential arterial connections, right

<a id="structure-artery.connection.angular_dorsal_nasal.right"></a>

### Angular–dorsal nasal right

**Model ID:** `artery.connection.angular_dorsal_nasal.right`

**Description**

Anastomoses to the distal [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) include the distal [facial artery](#structure-artery.eca.facial.right) via the [dorsal nasal artery](#structure-artery.anterior.dorsal_nasal_right).

[Angular artery](#structure-artery.eca.angular.right): if present, this is the terminal branch of the [facial artery](#structure-artery.eca.facial.right). It may also originate from the ophthalmic or [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right). The vessel courses in the nasojugal fold giving off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery ([lacrimal artery](#structure-artery.anterior.lacrimal_right)) to form the palpebral arcade. There are anastomoses with the ophthalmic, [lateral nasal](#structure-artery.eca.lateral_nasal.right), and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right) in addition to its counterpart across the midline.

**Source:** `nv(2).pdf`, PDF pages 9, 54; printed pages 15, 60.

**Parent:** [Angular artery right](#structure-artery.eca.angular.right)

**Connection endpoints:** [Angular artery right](#structure-artery.eca.angular.right); [Dorsal nasal right](#structure-artery.anterior.dorsal_nasal_right)

<a id="structure-artery.connection.labial_septal_plexus.right"></a>

### Labial–septal plexus right

**Model ID:** `artery.connection.labial_septal_plexus.right`

**Description**

The [superior labial artery](#structure-artery.eca.superior_labial.right) delivers branches to the nasal septum and ala and can anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right).

Kiesselbach’s plexus is supplied by the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right), [superior labial](#structure-artery.eca.superior_labial.right), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_right), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_right) arteries.

**Source:** `nv(2).pdf`, PDF pages 9, 23; printed pages 15, 29.

**Parent:** [Superior labial artery right](#structure-artery.eca.superior_labial.right)

**Connection endpoints:** [Superior labial artery right](#structure-artery.eca.superior_labial.right); [Inferior septal subdivision right](#structure-artery.amendment.inferior_septal_subdivision.right)

<a id="structure-artery.connection.facial_maxillary_masseteric.right"></a>

### Facial–maxillary masseteric right

**Model ID:** `artery.connection.facial_maxillary_masseteric.right`

**Description**

The [masseteric artery](#structure-artery.eca.maxillary.masseteric.right) anastomoses with masseteric branches of the [facial artery](#structure-artery.eca.facial.right) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Facial masseteric branch right](#structure-artery.amendment.facial_masseteric_branch.right)

**Connection endpoints:** [Facial masseteric branch right](#structure-artery.amendment.facial_masseteric_branch.right); [Masseteric artery right](#structure-artery.eca.maxillary.masseteric.right)

<a id="structure-artery.connection.facial_maxillary_buccal.right"></a>

### Facial–maxillary buccal right

**Model ID:** `artery.connection.facial_maxillary_buccal.right`

**Description**

Anastomoses: ascending branch of the [facial artery](#structure-artery.eca.facial.right) and the superior masseteric branch of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right). It is an important route for [facial artery](#structure-artery.eca.facial.right) reconstitution after proximal [facial artery](#structure-artery.eca.facial.right) ligation.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Facial buccal branch right](#structure-artery.amendment.facial_buccal_branch.right)

**Connection endpoints:** [Facial buccal branch right](#structure-artery.amendment.facial_buccal_branch.right); [Buccal artery right](#structure-artery.eca.maxillary.buccal.right)

<a id="structure-artery.connection.occipital_posterior_auricular_scalp.right"></a>

### Occipital–posterior auricular scalp right

**Model ID:** `artery.connection.occipital_posterior_auricular_scalp.right`

**Parent:** [Occipital lateral scalp artery right](#structure-artery.eca.occipital_lateral_scalp.right)

**Connection endpoints:** [Occipital lateral scalp artery right](#structure-artery.eca.occipital_lateral_scalp.right); [Posterior auricular artery right](#structure-artery.eca.posterior_auricular.right)

<a id="structure-artery.connection.occipital_mma_transosseous_potential.right"></a>

### Occipital–MMA transosseous potential right

**Model ID:** `artery.connection.occipital_mma_transosseous_potential.right`

**Description**

All peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right) and [occipital artery](#structure-artery.eca.occipital.right) via transosseous branches, which become evident under pathological conditions, in particular dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Occipital lateral scalp artery right](#structure-artery.eca.occipital_lateral_scalp.right)

**Connection endpoints:** [Occipital lateral scalp artery right](#structure-artery.eca.occipital_lateral_scalp.right); [MMA posterior convexity artery right](#structure-artery.eca.maxillary.mma.posterior_convexity.right)

<a id="structure-artery.connection.occipital_descending_vertebral_c2.right"></a>

### Occipital descending–vertebral C2 right

**Model ID:** `artery.connection.occipital_descending_vertebral_c2.right`

**Description**

The [occipital artery](#structure-artery.eca.occipital.right), derived from embryological type I and II proatlantal arteries (C1 and C2 segmental arteries), maintains anastomotic pathways from the [ECA](#structure-artery.carotid.external.right) to the [vertebral artery](#structure-artery.posterior.vertebral_right) via posterior radicular branches at the C1 and C2 levels. These connections serve as major collateral pathways from the [vertebral artery](#structure-artery.posterior.vertebral_right) to the carotid system, particularly visible in cases where the common carotid is ligated or occluded.

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Occipital descending artery right](#structure-artery.eca.occipital_descending.right)

**Connection endpoints:** [Occipital descending artery right](#structure-artery.eca.occipital_descending.right); [VA muscular C2 right](#structure-artery.posterior.va_muscular_c2_right)

<a id="structure-artery.connection.occipital_mastoid_apa_sigmoid.right"></a>

### Occipital mastoid–APA sigmoid right

**Model ID:** `artery.connection.occipital_mastoid_apa_sigmoid.right`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right)

**Connection endpoints:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right); [Jugular sigmoid branch right](#structure-artery.eca.apa.sigmoid_sinus_branch.right)

<a id="structure-artery.connection.occipital_mastoid_mma_petrosquamosal.right"></a>

### Occipital mastoid–MMA petrosquamosal right

**Model ID:** `artery.connection.occipital_mastoid_mma_petrosquamosal.right`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right)

**Connection endpoints:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right); [MMA petrosquamosal artery right](#structure-artery.eca.maxillary.mma.petrosquamosal.right)

<a id="structure-artery.connection.occipital_mastoid_apa_jugular.right"></a>

### Occipital mastoid–APA jugular right

**Model ID:** `artery.connection.occipital_mastoid_apa_jugular.right`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right)

**Connection endpoints:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right); [Jugular branch right](#structure-artery.eca.apa.jugular.right)

<a id="structure-artery.connection.occipital_mastoid_hypoglossal_meningeal.right"></a>

### Occipital mastoid–hypoglossal meningeal right

**Model ID:** `artery.connection.occipital_mastoid_hypoglossal_meningeal.right`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.right) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) of the [AICA](#structure-artery.posterior.aica_right). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_right).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right)

**Connection endpoints:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right); [Hypoglossal posterior meningeal artery right](#structure-artery.eca.apa.posterior_meningeal.right)

<a id="structure-artery.connection.occipital_tentorial_pca_dural.right"></a>

### Occipital tentorial–PCA dural right

**Model ID:** `artery.connection.occipital_tentorial_pca_dural.right`

**Parent:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right)

**Connection endpoints:** [Occipital mastoid dural branch right](#structure-artery.amendment.occipital_mastoid_dural_branch.right); [Davidoff and Schechter artery right](#structure-artery.amendment.davidoff_and_schechter_artery.right)

<a id="structure-artery.connection.occipital_vertebral_c1.right"></a>

### Occipital–vertebral C1 right

**Model ID:** `artery.connection.occipital_vertebral_c1.right`

**Description**

The [occipital artery](#structure-artery.eca.occipital.right), derived from embryological type I and II proatlantal arteries (C1 and C2 segmental arteries), maintains anastomotic pathways from the [ECA](#structure-artery.carotid.external.right) to the [vertebral artery](#structure-artery.posterior.vertebral_right) via posterior radicular branches at the C1 and C2 levels. These connections serve as major collateral pathways from the [vertebral artery](#structure-artery.posterior.vertebral_right) to the carotid system, particularly visible in cases where the common carotid is ligated or occluded.

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Occipital artery right](#structure-artery.eca.occipital.right)

**Connection endpoints:** [Occipital artery right](#structure-artery.eca.occipital.right); [VA muscular C1 right](#structure-artery.posterior.va_muscular_c1_right)

<a id="structure-artery.connection.stylomastoid_inferior_tympanic.right"></a>

### Stylomastoid–inferior tympanic right

**Model ID:** `artery.connection.stylomastoid_inferior_tympanic.right`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right) enters the tympanic cavity and anastomoses with the [superior tympanic artery](#structure-artery.amendment.superior_tympanic.right) from the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right) branch of the [IMA](#structure-artery.eca.maxillary.right), the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right), the [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) branch of the [ICA](#structure-artery.anterior.internal_carotid_right), and the arcuate branch of the [anterior inferior cerebellar artery](#structure-artery.posterior.aica_right) ([AICA](#structure-artery.posterior.aica_right)).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Stylomastoid artery right](#structure-artery.eca.occipital.stylomastoid.right)

**Connection endpoints:** [Stylomastoid artery right](#structure-artery.eca.occipital.stylomastoid.right); [Inferior tympanic artery right](#structure-artery.eca.apa.inferior_tympanic.right)

<a id="structure-artery.connection.sta_supratrochlear_scalp.right"></a>

### STA–supratrochlear scalp right

**Model ID:** `artery.connection.sta_supratrochlear_scalp.right`

**Parent:** [STA frontal anterior twig artery right](#structure-artery.eca.sta_frontal_anterior_twig.right)

**Connection endpoints:** [STA frontal anterior twig artery right](#structure-artery.eca.sta_frontal_anterior_twig.right); [Supratrochlear right](#structure-artery.anterior.supratrochlear_right)

<a id="structure-artery.connection.sta_supraorbital.right"></a>

### STA–supraorbital right

**Model ID:** `artery.connection.sta_supraorbital.right`

**Description**

The [frontal division of the STA](#structure-artery.eca.superficial_temporal.frontal.right) anastomoses with the supraorbital and frontal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA frontal artery right](#structure-artery.eca.superficial_temporal.frontal.right)

**Connection endpoints:** [STA frontal artery right](#structure-artery.eca.superficial_temporal.frontal.right); [Supraorbital right](#structure-artery.anterior.supraorbital_right)

<a id="structure-artery.connection.sta_occipital_scalp.right"></a>

### STA–occipital scalp right

**Model ID:** `artery.connection.sta_occipital_scalp.right`

**Description**

The [parietal division of the STA](#structure-artery.eca.superficial_temporal.parietal.right) runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right), and [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA parietal artery right](#structure-artery.eca.superficial_temporal.parietal.right)

**Connection endpoints:** [STA parietal artery right](#structure-artery.eca.superficial_temporal.parietal.right); [Occipital lateral scalp artery right](#structure-artery.eca.occipital_lateral_scalp.right)

<a id="structure-artery.connection.sta_mma_transosseous_potential.right"></a>

### STA–MMA transosseous potential right

**Model ID:** `artery.connection.sta_mma_transosseous_potential.right`

**Description**

All peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right) and [occipital artery](#structure-artery.eca.occipital.right) via transosseous branches, which become evident under pathological conditions, in particular dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [STA parietal artery right](#structure-artery.eca.superficial_temporal.parietal.right)

**Connection endpoints:** [STA parietal artery right](#structure-artery.eca.superficial_temporal.parietal.right); [MMA parietal ascending artery right](#structure-artery.eca.mma_parietal_ascending.right)

<a id="structure-artery.connection.transverse_facial_infraorbital.right"></a>

### Transverse facial–infraorbital right

**Model ID:** `artery.connection.transverse_facial_infraorbital.right`

**Description**

The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial superior division right](#structure-artery.amendment.transverse_facial_superior_division.right)

**Connection endpoints:** [Transverse facial superior division right](#structure-artery.amendment.transverse_facial_superior_division.right); [Infraorbital artery right](#structure-artery.eca.maxillary.infraorbital.right)

<a id="structure-artery.connection.transverse_facial_facial.right"></a>

### Transverse facial–facial right

**Model ID:** `artery.connection.transverse_facial_facial.right`

**Description**

The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial inferior division right](#structure-artery.amendment.transverse_facial_inferior_division.right)

**Connection endpoints:** [Transverse facial inferior division right](#structure-artery.amendment.transverse_facial_inferior_division.right); [Facial artery right](#structure-artery.eca.facial.right)

<a id="structure-artery.connection.sta_posterior_auricular_scalp.right"></a>

### STA–posterior auricular scalp right

**Model ID:** `artery.connection.sta_posterior_auricular_scalp.right`

**Description**

The [parietal division of the STA](#structure-artery.eca.superficial_temporal.parietal.right) runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right), and [posterior auricular](#structure-artery.eca.posterior_auricular.right) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA anterior auricular right](#structure-artery.amendment.sta_anterior_auricular.right)

**Connection endpoints:** [STA anterior auricular right](#structure-artery.amendment.sta_anterior_auricular.right); [Posterior auricular auricular branch right](#structure-artery.amendment.posterior_auricular_auricular_branch.right)

<a id="structure-artery.connection.zygomatico_orbital_lacrimal.right"></a>

### Zygomatico-orbital–lacrimal right

**Model ID:** `artery.connection.zygomatico_orbital_lacrimal.right`

**Parent:** [Zygomatico-orbital right](#structure-artery.amendment.zygomatico_orbital.right)

**Connection endpoints:** [Zygomatico-orbital right](#structure-artery.amendment.zygomatico_orbital.right); [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.connection.deep_temporal_lacrimal.right"></a>

### Deep temporal–lacrimal right

**Model ID:** `artery.connection.deep_temporal_lacrimal.right`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right) has anastomoses with the [inferior branch of the lacrimal artery](#structure-artery.amendment.lacrimal_inferior_branch.right) via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Anterior deep temporal artery right](#structure-artery.eca.anterior_deep_temporal.right)

**Connection endpoints:** [Anterior deep temporal artery right](#structure-artery.eca.anterior_deep_temporal.right); [Lacrimal inferior branch right](#structure-artery.amendment.lacrimal_inferior_branch.right)

<a id="structure-artery.connection.infraorbital_ophthalmic.right"></a>

### Infraorbital–ophthalmic right

**Model ID:** `artery.connection.infraorbital_ophthalmic.right`

**Description**

Anastomoses: the terminal branches anastomose with the superficial temporal, ophthalmic, facial, and [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right) arteries.

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) gives off osseous and muscular branches on the orbital floor, anastomosing with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Infraorbital muscular branch right](#structure-artery.amendment.infraorbital_muscular_branch.right)

**Connection endpoints:** [Infraorbital muscular branch right](#structure-artery.amendment.infraorbital_muscular_branch.right); [Ophthalmic inferior muscular branch right](#structure-artery.amendment.ophthalmic_inferior_muscular_branch.right)

<a id="structure-artery.connection.inferior_lacrimal_infraorbital_muscular.right"></a>

### Inferior lacrimal–infraorbital muscular right

**Model ID:** `artery.connection.inferior_lacrimal_infraorbital_muscular.right`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right) has anastomoses with the [inferior branch of the lacrimal artery](#structure-artery.amendment.lacrimal_inferior_branch.right) via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Infraorbital muscular branch right](#structure-artery.amendment.infraorbital_muscular_branch.right)

**Connection endpoints:** [Infraorbital muscular branch right](#structure-artery.amendment.infraorbital_muscular_branch.right); [Lacrimal inferior branch right](#structure-artery.amendment.lacrimal_inferior_branch.right)

<a id="structure-artery.connection.septal_anterior_ethmoidal.right"></a>

### Septal–anterior ethmoidal right

**Model ID:** `artery.connection.septal_anterior_ethmoidal.right`

**Description**

The [posterior septal artery](#structure-artery.eca.posterior_septal.right) anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right) and [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) and contributes to Kiesselbach’s plexus.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Posterior septal artery right](#structure-artery.eca.posterior_septal.right)

**Connection endpoints:** [Posterior septal artery right](#structure-artery.eca.posterior_septal.right); [Anterior ethmoidal right](#structure-artery.anterior.anterior_ethmoidal_right)

<a id="structure-artery.connection.posterior_septal_posterior_ethmoidal.right"></a>

### Posterior septal–posterior ethmoidal right

**Model ID:** `artery.connection.posterior_septal_posterior_ethmoidal.right`

**Description**

Kiesselbach’s plexus is located on the anterior inferior quadrant of the nasal septum (Little’s area). It is supplied by five vessels: the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right), [superior labial](#structure-artery.eca.superior_labial.right), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_right), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_right) arteries.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Superior septal subdivision right](#structure-artery.amendment.superior_septal_subdivision.right)

**Connection endpoints:** [Superior septal subdivision right](#structure-artery.amendment.superior_septal_subdivision.right); [Posterior ethmoidal right](#structure-artery.anterior.posterior_ethmoidal_right)

<a id="structure-artery.connection.septal_palatine_network.right"></a>

### Septal–palatine network right

**Model ID:** `artery.connection.septal_palatine_network.right`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) anastomoses with the [posterior septal arteries](#structure-artery.eca.posterior_septal.right) from the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right) and with the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Inferior septal subdivision right](#structure-artery.amendment.inferior_septal_subdivision.right)

**Connection endpoints:** [Inferior septal subdivision right](#structure-artery.amendment.inferior_septal_subdivision.right); [Greater palatine artery right](#structure-artery.eca.greater_palatine.right)

<a id="structure-artery.connection.vidian_eca_ica.right"></a>

### Vidian ECA–ICA right

**Model ID:** `artery.connection.vidian_eca_ica.right`

**Description**

The vidian artery, running horizontally, arises from the distal [IMA](#structure-artery.eca.maxillary.right) and runs through the [vidian canal](#structure-landmark.pterygoid-canal.right) to the [foramen lacerum](#structure-landmark.foramen-lacerum.right), where it meets the [vidian branch of the mandibulovidian artery](#structure-artery.anterior.vidian_ica_contribution_right) from the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Vidian artery right](#structure-artery.eca.maxillary.pterygoid_canal.right)

**Connection endpoints:** [Vidian artery right](#structure-artery.eca.maxillary.pterygoid_canal.right); [Vidian ICA contribution right](#structure-artery.anterior.vidian_ica_contribution_right)

<a id="structure-artery.connection.foramen_rotundum_ilt.right"></a>

### Foramen rotundum–ILT right

**Model ID:** `artery.connection.foramen_rotundum_ilt.right`

**Description**

The [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right) from the [IMA](#structure-artery.eca.maxillary.right) connects to the [anterolateral branch of the ILT](#structure-artery.amendment.ilt_anterolateral_ramus.right) and, in rare instances, with the lateral clival artery.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Artery of the foramen rotundum right](#structure-artery.eca.maxillary.foramen_rotundum.right)

**Connection endpoints:** [Artery of the foramen rotundum right](#structure-artery.eca.maxillary.foramen_rotundum.right); [ILT anterolateral ramus right](#structure-artery.amendment.ilt_anterolateral_ramus.right)

<a id="structure-artery.connection.accessory_meningeal_ilt.right"></a>

### Accessory meningeal–ILT right

**Model ID:** `artery.connection.accessory_meningeal_ilt.right`

**Description**

The superior division of the [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right) enters the cavernous sinus through the [foramen ovale](#structure-landmark.ovale.right) to connect with the [posteromedial branch of the ILT](#structure-artery.amendment.ilt_posteromedial_ramus.right), which runs beneath the trigeminal ganglion and along the second branch of the trigeminal nerve (CN V2).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Accessory meningeal posterior intracranial right](#structure-artery.amendment.accessory_meningeal_posterior_intracranial.right)

**Connection endpoints:** [Accessory meningeal posterior intracranial right](#structure-artery.amendment.accessory_meningeal_posterior_intracranial.right); [ILT posteromedial ramus right](#structure-artery.amendment.ilt_posteromedial_ramus.right)

<a id="structure-artery.connection.mma_tentorial_marginal.right"></a>

### MMA–tentorial marginal right

**Model ID:** `artery.connection.mma_tentorial_marginal.right`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right)’s petrosquamous or posterior branch also anastomoses with the [marginal tentorial artery](#structure-artery.anterior.tentorial_marginal_right), which may originate from the [ILT](#structure-artery.anterior.inferolateral_trunk_right), [ophthalmic artery](#structure-artery.anterior.ophthalmic_right), or the [MHT](#structure-artery.anterior.meningohypophyseal_trunk_right) of the [ICA](#structure-artery.anterior.internal_carotid_right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [MMA petrosquamosal artery right](#structure-artery.eca.maxillary.mma.petrosquamosal.right)

**Connection endpoints:** [MMA petrosquamosal artery right](#structure-artery.eca.maxillary.mma.petrosquamosal.right); [Tentorial marginal right](#structure-artery.anterior.tentorial_marginal_right)

<a id="structure-artery.connection.mma_tentorial_pca_dural.right"></a>

### MMA tentorial–PCA dural right

**Model ID:** `artery.connection.mma_tentorial_pca_dural.right`

**Parent:** [MMA petrosquamosal artery right](#structure-artery.eca.maxillary.mma.petrosquamosal.right)

**Connection endpoints:** [MMA petrosquamosal artery right](#structure-artery.eca.maxillary.mma.petrosquamosal.right); [Davidoff and Schechter artery right](#structure-artery.amendment.davidoff_and_schechter_artery.right)

<a id="structure-artery.connection.superior_anterior_tympanic.right"></a>

### Superior–anterior tympanic right

**Model ID:** `artery.connection.superior_anterior_tympanic.right`

**Description**

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right) supplies the mandibular joint and the tympanic cavity, where it anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right), [superior tympanic](#structure-artery.amendment.superior_tympanic.right), and [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superior tympanic right](#structure-artery.amendment.superior_tympanic.right)

**Connection endpoints:** [Superior tympanic right](#structure-artery.amendment.superior_tympanic.right); [Anterior tympanic artery right](#structure-artery.eca.maxillary.anterior_tympanic.right)

<a id="structure-artery.connection.superior_inferior_tympanic.right"></a>

### Superior–inferior tympanic right

**Model ID:** `artery.connection.superior_inferior_tympanic.right`

**Description**

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right) supplies the mandibular joint and the tympanic cavity, where it anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right), [superior tympanic](#structure-artery.amendment.superior_tympanic.right), and [caroticotympanic](#structure-artery.anterior.caroticotympanic_right) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superior tympanic right](#structure-artery.amendment.superior_tympanic.right)

**Connection endpoints:** [Superior tympanic right](#structure-artery.amendment.superior_tympanic.right); [Inferior tympanic artery right](#structure-artery.eca.apa.inferior_tympanic.right)

<a id="structure-artery.connection.facial_nerve_arcade.right"></a>

### Facial nerve arcade right

**Model ID:** `artery.connection.facial_nerve_arcade.right`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right) enters the [stylomastoid foramen](#structure-landmark.stylomastoid.right) with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [MMA petrosal artery right](#structure-artery.eca.maxillary.mma.petrosal.right)

**Connection endpoints:** [MMA petrosal artery right](#structure-artery.eca.maxillary.mma.petrosal.right); [Stylomastoid artery right](#structure-artery.eca.occipital.stylomastoid.right)

<a id="structure-artery.connection.mma_cavernous_ilt.right"></a>

### MMA cavernous–ILT right

**Model ID:** `artery.connection.mma_cavernous_ilt.right`

**Description**

After entering the [foramen spinosum](#structure-landmark.foramen-spinosum.right), the [MMA](#structure-artery.eca.maxillary.mma.right) has cavernous branches that connect with the superior or tentorial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right), and orbital branches that anastomose within the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right) with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right).

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [MMA anterior cavernous right](#structure-artery.amendment.mma_anterior_cavernous.right)

**Connection endpoints:** [MMA anterior cavernous right](#structure-artery.amendment.mma_anterior_cavernous.right); [ILT superior ramus right](#structure-artery.amendment.ilt_superior_ramus.right)

<a id="structure-artery.connection.posterior_cavernous_mma_posterolateral_ilt.right"></a>

### Posterior cavernous MMA–posterolateral ILT right

**Model ID:** `artery.connection.posterior_cavernous_mma_posterolateral_ilt.right`

**Description**

The posterolateral branch supplies the trigeminal ganglion and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) at the [foramen spinosum](#structure-landmark.foramen-spinosum.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [MMA posterior cavernous right](#structure-artery.amendment.mma_posterior_cavernous.right)

**Connection endpoints:** [MMA posterior cavernous right](#structure-artery.amendment.mma_posterior_cavernous.right); [ILT posterior division (posterolateral continuation) right](#structure-artery.anterior.ilt_posterior_branch_right)

<a id="structure-artery.connection.mma_lacrimal__meningolacrimal.right"></a>

### MMA–lacrimal (meningolacrimal) right

**Model ID:** `artery.connection.mma_lacrimal__meningolacrimal.right`

**Description**

Meningolacrimal artery: partial supply only of the lacrimal gland from the [MMA](#structure-artery.eca.maxillary.mma.right) via the [foramen of Hyrtl](#structure-landmark.cranio-orbital.right).

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [MMA orbital artery right](#structure-artery.eca.mma_orbital.right)

**Connection endpoints:** [MMA orbital artery right](#structure-artery.eca.mma_orbital.right); [Lacrimal right](#structure-artery.anterior.lacrimal_right)

<a id="structure-artery.connection.mma_ophthalmic__recurrent_meningeal.right"></a>

### MMA–ophthalmic (recurrent meningeal) right

**Model ID:** `artery.connection.mma_ophthalmic__recurrent_meningeal.right`

**Description**

The [recurrent meningeal branch of the lacrimal artery](#structure-artery.amendment.superficial_recurrent_meningeal.right) courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [MMA orbital artery right](#structure-artery.eca.mma_orbital.right)

**Connection endpoints:** [MMA orbital artery right](#structure-artery.eca.mma_orbital.right); [Superficial recurrent meningeal right](#structure-artery.amendment.superficial_recurrent_meningeal.right)

<a id="structure-artery.connection.sof_artery_anteromedial_ilt.right"></a>

### SOF artery–anteromedial ILT right

**Model ID:** `artery.connection.sof_artery_anteromedial_ilt.right`

**Description**

The [artery of the superior orbital fissure](#structure-artery.amendment.artery_of_superior_orbital_fissure.right) anastomoses with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and the recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Artery of superior orbital fissure right](#structure-artery.amendment.artery_of_superior_orbital_fissure.right)

**Connection endpoints:** [Artery of superior orbital fissure right](#structure-artery.amendment.artery_of_superior_orbital_fissure.right); [ILT anteromedial ramus right](#structure-artery.anterior.ilt_anterior_branch_right)

<a id="structure-artery.connection.sof_artery_recurrent_meningeal.right"></a>

### SOF artery–recurrent meningeal right

**Model ID:** `artery.connection.sof_artery_recurrent_meningeal.right`

**Description**

The [artery of the superior orbital fissure](#structure-artery.amendment.artery_of_superior_orbital_fissure.right) anastomoses with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and the recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Artery of superior orbital fissure right](#structure-artery.amendment.artery_of_superior_orbital_fissure.right)

**Connection endpoints:** [Artery of superior orbital fissure right](#structure-artery.amendment.artery_of_superior_orbital_fissure.right); [Superficial recurrent meningeal right](#structure-artery.amendment.superficial_recurrent_meningeal.right)

<a id="structure-artery.connection.tubal_accessory_meningeal_circle.right"></a>

### Tubal–accessory meningeal circle right

**Model ID:** `artery.connection.tubal_accessory_meningeal_circle.right`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.right), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right) from the distal [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right)

**Connection endpoints:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right); [Accessory meningeal anterior tubal right](#structure-artery.amendment.accessory_meningeal_anterior_tubal.right)

<a id="structure-artery.connection.tubal_mandibular_ica_circle.right"></a>

### Tubal–mandibular ICA circle right

**Model ID:** `artery.connection.tubal_mandibular_ica_circle.right`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.right), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right) from the distal [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right)

**Connection endpoints:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right); [Mandibular ICA branch right](#structure-artery.amendment.mandibular_ica_branch.right)

<a id="structure-artery.connection.tubal_pterygovaginal_circle.right"></a>

### Tubal–pterygovaginal circle right

**Model ID:** `artery.connection.tubal_pterygovaginal_circle.right`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.right), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right) from the distal [IMA](#structure-artery.eca.maxillary.right).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right)

**Connection endpoints:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right); [Pterygovaginal artery right](#structure-artery.eca.pterygovaginal.right)

<a id="structure-artery.connection.tubal_maxillary_vidian_circle.right"></a>

### Tubal–maxillary vidian circle right

**Model ID:** `artery.connection.tubal_maxillary_vidian_circle.right`

**Description**

Anastomoses: [vidian artery of the ICA](#structure-artery.anterior.vidian_ica_contribution_right), [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right), mandibular artery, [ascending pharyngeal](#structure-artery.eca.apa.right) ([superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right)), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right), and [ascending palatine](#structure-artery.eca.ascending_palatine.right) arteries (the pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right)

**Connection endpoints:** [Superior pharyngeal tubal branch right](#structure-artery.amendment.superior_pharyngeal_tubal_branch.right); [Vidian artery right](#structure-artery.eca.maxillary.pterygoid_canal.right)

<a id="structure-artery.connection.pharyngeal_carotid_recurrent_lacerum.right"></a>

### Pharyngeal carotid–recurrent lacerum right

**Model ID:** `artery.connection.pharyngeal_carotid_recurrent_lacerum.right`

**Description**

The [carotid branch of the superior pharyngeal artery](#structure-artery.amendment.superior_pharyngeal_carotid_branch.right) traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.right) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right) from the [ILT](#structure-artery.anterior.inferolateral_trunk_right) of the [ICA](#structure-artery.anterior.internal_carotid_right), both ipsilateral and contralateral.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Superior pharyngeal carotid branch right](#structure-artery.amendment.superior_pharyngeal_carotid_branch.right)

**Connection endpoints:** [Superior pharyngeal carotid branch right](#structure-artery.amendment.superior_pharyngeal_carotid_branch.right); [ILT recurrent lacerum ramus right](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right)

<a id="structure-artery.connection.apha_clival_mht.right"></a>

### APhA clival–MHT right

**Model ID:** `artery.connection.apha_clival_mht.right`

**Description**

The [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right) divides into jugular and hypoglossal branches, each giving off medial and lateral clival branches which anastomose with clival branches from the [MHT](#structure-artery.anterior.meningohypophyseal_trunk_right) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous): important in the vascular supply to meningiomas.

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Medial clival artery right](#structure-artery.eca.medial_clival.right)

**Connection endpoints:** [Medial clival artery right](#structure-artery.eca.medial_clival.right); [Medial clival MHT branch right](#structure-artery.amendment.medial_clival_mht_branch.right)

<a id="structure-artery.connection.apha_odontoid_vertebral.right"></a>

### APhA odontoid–vertebral right

**Model ID:** `artery.connection.apha_odontoid_vertebral.right`

**Description**

The [prevertebral branch](#structure-artery.amendment.apa_prevertebral_branch.right), running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_right) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Odontoid descending artery right](#structure-artery.eca.apa.descending_odontoid.right)

**Connection endpoints:** [Odontoid descending artery right](#structure-artery.eca.apa.descending_odontoid.right); [VA odontoid contribution right](#structure-artery.posterior.va_odontoid_contribution_right)

<a id="structure-artery.connection.falx_cerebelli_va_posterior_meningeal.right"></a>

### Falx cerebelli–VA posterior meningeal right

**Model ID:** `artery.connection.falx_cerebelli_va_posterior_meningeal.right`

**Parent:** [Falx cerebelli artery right](#structure-artery.amendment.falx_cerebelli_artery.right)

**Connection endpoints:** [Falx cerebelli artery right](#structure-artery.amendment.falx_cerebelli_artery.right); [Posterior meningeal VA right](#structure-artery.posterior.posterior_meningeal_va_right)

<a id="structure-artery.connection.apa_tentorial_sca_dural.right"></a>

### APA tentorial–SCA dural right

**Model ID:** `artery.connection.apa_tentorial_sca_dural.right`

**Parent:** [Hypoglossal posterior meningeal artery right](#structure-artery.eca.apa.posterior_meningeal.right)

**Connection endpoints:** [Hypoglossal posterior meningeal artery right](#structure-artery.eca.apa.posterior_meningeal.right); [Wollschlaeger and Wollschlaeger artery right](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.right)

<a id="structure-artery.connection.lateral_clival_apa_mht.right"></a>

### Lateral clival APA–MHT right

**Model ID:** `artery.connection.lateral_clival_apa_mht.right`

**Description**

The lateral clival artery supplies the dura of the clivus. It has lateral and inferolateral branches which follow, respectively, the superior and inferior petrosal sinuses. There are anastomoses with its contralateral counterpart, the [jugular branch](#structure-artery.eca.apa.jugular.right) of the [ascending pharyngeal](#structure-artery.eca.apa.right), and the [MMA](#structure-artery.eca.maxillary.mma.right).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Lateral clival artery right](#structure-artery.eca.lateral_clival.right)

**Connection endpoints:** [Lateral clival artery right](#structure-artery.eca.lateral_clival.right); [Lateral clival MHT branch right](#structure-artery.amendment.lateral_clival_mht_branch.right)

<a id="structure-artery.connection.lateral_clival_recurrent_ilt.right"></a>

### Lateral clival–recurrent ILT right

**Model ID:** `artery.connection.lateral_clival_recurrent_ilt.right`

**Description**

Clival branches of the [jugular artery](#structure-artery.eca.apa.jugular.right) anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_right) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_right) and can supply the abducens nerve in Dorello’s canal.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Lateral clival artery right](#structure-artery.eca.lateral_clival.right)

**Connection endpoints:** [Lateral clival artery right](#structure-artery.eca.lateral_clival.right); [ILT recurrent lacerum ramus right](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right)

<a id="structure-artery.connection.inferior_tympanic_caroticotympanic.right"></a>

### Inferior tympanic–caroticotympanic right

**Model ID:** `artery.connection.inferior_tympanic_caroticotympanic.right`

**Description**

The [inferior tympanic artery](#structure-artery.eca.apa.inferior_tympanic.right) branch of the [ascending pharyngeal artery](#structure-artery.eca.apa.right) travels with Jacobson’s nerve through the inferior tympanic foramen, anastomosing with other tympanic ([anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right), [superior tympanic](#structure-artery.amendment.superior_tympanic.right)) and surrounding arteries within the middle ear including the [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_right), a [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) branch.

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Inferior tympanic artery right](#structure-artery.eca.apa.inferior_tympanic.right)

**Connection endpoints:** [Inferior tympanic artery right](#structure-artery.eca.apa.inferior_tympanic.right); [Caroticotympanic right](#structure-artery.anterior.caroticotympanic_right)

<a id="structure-artery.connection.apa_musculospinal_va.right"></a>

### APA musculospinal–VA right

**Model ID:** `artery.connection.apa_musculospinal_va.right`

**Description**

The [musculospinal branch](#structure-artery.amendment.apa_musculospinal.right) laterally anastomoses with the C3 radicular anastomotic artery from the [vertebral artery](#structure-artery.posterior.vertebral_right).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [APA musculospinal right](#structure-artery.amendment.apa_musculospinal.right)

**Connection endpoints:** [APA musculospinal right](#structure-artery.amendment.apa_musculospinal.right); [VA muscular C2 right](#structure-artery.posterior.va_muscular_c2_right)

<a id="structure-artery.connection.apa_prevertebral_odontoid.right"></a>

### APA prevertebral–odontoid right

**Model ID:** `artery.connection.apa_prevertebral_odontoid.right`

**Description**

The [prevertebral branch](#structure-artery.amendment.apa_prevertebral_branch.right), running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_right) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [APA prevertebral branch right](#structure-artery.amendment.apa_prevertebral_branch.right)

**Connection endpoints:** [APA prevertebral branch right](#structure-artery.amendment.apa_prevertebral_branch.right); [Odontoid descending artery right](#structure-artery.eca.apa.descending_odontoid.right)

<a id="structure-artery.connection.mandibular_vidian_circle.right"></a>

### Mandibular–vidian circle right

**Model ID:** `artery.connection.mandibular_vidian_circle.right`

**Description**

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [pharyngeal trunk](#structure-artery.eca.apa.pharyngeal_trunk.right) contributes to the Eustachian tube anastomotic circle. It is connected to the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous)’s mandibular and vidian arteries and forms connections with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) and [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right) (distal [IMA](#structure-artery.eca.maxillary.right)). It also sends a branch through the [foramen lacerum](#structure-landmark.foramen-lacerum.right) to the cavernous sinus, joining the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.right) and the [ILT](#structure-artery.anterior.inferolateral_trunk_right) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_right.segment.cavernous).

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Mandibular ICA branch right](#structure-artery.amendment.mandibular_ica_branch.right)

**Connection endpoints:** [Mandibular ICA branch right](#structure-artery.amendment.mandibular_ica_branch.right); [Vidian ICA contribution right](#structure-artery.anterior.vidian_ica_contribution_right)

<a id="structure-artery.connection.clival_posterior_cavernous_mma.right"></a>

### Clival–posterior cavernous MMA right

**Model ID:** `artery.connection.clival_posterior_cavernous_mma.right`

**Description**

The posterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right) anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Lateral clival MHT branch right](#structure-artery.amendment.lateral_clival_mht_branch.right)

**Connection endpoints:** [Lateral clival MHT branch right](#structure-artery.amendment.lateral_clival_mht_branch.right); [MMA posterior cavernous right](#structure-artery.amendment.mma_posterior_cavernous.right)

<a id="structure-artery.connection.basal_tentorial_sca_dural.right"></a>

### Basal tentorial–SCA dural right

**Model ID:** `artery.connection.basal_tentorial_sca_dural.right`

**Parent:** [Basal tentorial MHT branch right](#structure-artery.amendment.basal_tentorial_mht_branch.right)

**Connection endpoints:** [Basal tentorial MHT branch right](#structure-artery.amendment.basal_tentorial_mht_branch.right); [Wollschlaeger and Wollschlaeger artery right](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.right)

<a id="structure-artery.connection.anterior_falcine_mma_paramedian.right"></a>

### Anterior falcine–MMA paramedian right

**Model ID:** `artery.connection.anterior_falcine_mma_paramedian.right`

**Description**

Paramedian arteries: these are the terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right). They are directed anteriorly or posteriorly along the superior sagittal sinus and anastomose with the anterior (from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_right)) or posterior (from the [ascending pharyngeal](#structure-artery.eca.apa.right)) falcine arteries. They deliver small branches to the superior sagittal sinus and falx cerebri. They also anastomose with dural branches of the posterior cerebral artery (PCA; Davidoff and Schechter) and the [superior cerebellar artery](#structure-artery.posterior.sca_right) ([SCA](#structure-artery.posterior.sca_right); [artery of Wollschlaeger and Wollschlaeger](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.right)).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Anterior falcine right](#structure-artery.amendment.anterior_falcine.right)

**Connection endpoints:** [Anterior falcine right](#structure-artery.amendment.anterior_falcine.right); [MMA paramedian right](#structure-artery.amendment.mma_paramedian.right)

<a id="structure-artery.connection.deep_recurrent_ophthalmic_ilt.right"></a>

### Deep recurrent ophthalmic–ILT right

**Model ID:** `artery.connection.deep_recurrent_ophthalmic_ilt.right`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.right), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_right) as the [deep recurrent ophthalmic artery](#structure-artery.amendment.deep_recurrent_ophthalmic.right).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Deep recurrent ophthalmic right](#structure-artery.amendment.deep_recurrent_ophthalmic.right)

**Connection endpoints:** [Deep recurrent ophthalmic right](#structure-artery.amendment.deep_recurrent_ophthalmic.right); [ILT anteromedial ramus right](#structure-artery.anterior.ilt_anterior_branch_right)

<a id="structure-artery.connection.superior_palpebral_arcade.right"></a>

### Superior palpebral arcade right

**Model ID:** `artery.connection.superior_palpebral_arcade.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Medial superior palpebral right](#structure-artery.amendment.medial_superior_palpebral.right)

**Connection endpoints:** [Medial superior palpebral right](#structure-artery.amendment.medial_superior_palpebral.right); [Lateral superior palpebral right](#structure-artery.amendment.lateral_superior_palpebral.right)

<a id="structure-artery.connection.inferior_palpebral_arcade.right"></a>

### Inferior palpebral arcade right

**Model ID:** `artery.connection.inferior_palpebral_arcade.right`

**Description**

The [angular artery](#structure-artery.eca.angular.right) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_right) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Medial inferior palpebral right](#structure-artery.amendment.medial_inferior_palpebral.right)

**Connection endpoints:** [Medial inferior palpebral right](#structure-artery.amendment.medial_inferior_palpebral.right); [Lateral inferior palpebral right](#structure-artery.amendment.lateral_inferior_palpebral.right)

<a id="structure-artery.connection.anterior_lateral_posterior_choroidal.right"></a>

### Anterior–lateral posterior choroidal right

**Model ID:** `artery.connection.anterior_lateral_posterior_choroidal.right`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) anastomoses with the posterior choroidal artery via its intraventricular terminal branches.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal plexal representative right](#structure-artery.amendment.anterior_choroidal_plexal_representative.right)

**Connection endpoints:** [Anterior choroidal plexal representative right](#structure-artery.amendment.anterior_choroidal_plexal_representative.right); [Lateral posterior choroidal plexal representative right](#structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.right)

<a id="structure-artery.connection.aca_mca_frontal_border_zone.right"></a>

### ACA–MCA frontal border zone right

**Model ID:** `artery.connection.aca_mca_frontal_border_zone.right`

**Parent:** [Anterior internal frontal right](#structure-artery.anterior.anterior_internal_frontal_right)

**Connection endpoints:** [Anterior internal frontal right](#structure-artery.anterior.anterior_internal_frontal_right); [Prefrontal cortical branch right](#structure-artery.anterior.prefrontal_cortical_branch_right)

<a id="structure-artery.connection.aca_mca_parietal_border_zone.right"></a>

### ACA–MCA parietal border zone right

**Model ID:** `artery.connection.aca_mca_parietal_border_zone.right`

**Parent:** [Paracentral right](#structure-artery.anterior.paracentral_right)

**Connection endpoints:** [Paracentral right](#structure-artery.anterior.paracentral_right); [Anterior parietal cortical branch right](#structure-artery.anterior.anterior_parietal_cortical_branch_right)

<a id="structure-artery.connection.aca_falcine_mma_falcine.right"></a>

### ACA falcine–MMA falcine right

**Model ID:** `artery.connection.aca_falcine_mma_falcine.right`

**Parent:** [ACA falcine branch right](#structure-artery.amendment.aca_falcine_branch.right)

**Connection endpoints:** [ACA falcine branch right](#structure-artery.amendment.aca_falcine_branch.right); [MMA falcine terminal right](#structure-artery.amendment.mma_falcine_terminal.right)

<a id="structure-artery.connection.pericallosal_splenial.right"></a>

### Pericallosal–splenial right

**Model ID:** `artery.connection.pericallosal_splenial.right`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right)

**Connection endpoints:** [ACA pericallosal right](#structure-artery.anterior.aca_pericallosal_right); [PCA splenial right](#structure-artery.posterior.pca_splenial_right)

<a id="structure-artery.connection.mca_pca_occipital_border_zone.right"></a>

### MCA–PCA occipital border zone right

**Model ID:** `artery.connection.mca_pca_occipital_border_zone.right`

**Parent:** [Angular cortical branch right](#structure-artery.anterior.angular_cortical_branch_right)

**Connection endpoints:** [Angular cortical branch right](#structure-artery.anterior.angular_cortical_branch_right); [PCA parieto-occipital right](#structure-artery.posterior.pca_parieto_occipital_right)

<a id="structure-artery.connection.mca_pca_temporal_border_zone.right"></a>

### MCA–PCA temporal border zone right

**Model ID:** `artery.connection.mca_pca_temporal_border_zone.right`

**Parent:** [Posterior temporal cortical branch right](#structure-artery.anterior.posterior_temporal_cortical_branch_right)

**Connection endpoints:** [Posterior temporal cortical branch right](#structure-artery.anterior.posterior_temporal_cortical_branch_right); [PCA posterior inferior temporal right](#structure-artery.posterior.pca_posterior_inferior_temporal_right)

<a id="structure-artery.connection.medial_lateral_posterior_choroidal.right"></a>

### Medial–lateral posterior choroidal right

**Model ID:** `artery.connection.medial_lateral_posterior_choroidal.right`

**Description**

Terminal branches of the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_right) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal plexal representative right](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.right)

**Connection endpoints:** [Medial posterior choroidal plexal representative right](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.right); [Lateral posterior choroidal plexal representative right](#structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.right)

<a id="structure-artery.connection.posterior_choroidal_splenial.right"></a>

### Posterior choroidal–splenial right

**Model ID:** `artery.connection.posterior_choroidal_splenial.right`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_right).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [Medial posterior choroidal plexal representative right](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.right)

**Connection endpoints:** [Medial posterior choroidal plexal representative right](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.right); [PCA splenial right](#structure-artery.posterior.pca_splenial_right)

<a id="structure-artery.connection.pca_sca_tectal_network.right"></a>

### PCA–SCA tectal network right

**Model ID:** `artery.connection.pca_sca_tectal_network.right`

**Description**

Collicular arteries sometimes arise distinctly from the [P1 segment](#structure-artery.posterior.pca_p1_right) (running medial to P2) or P2 segment. They curve around and send branches to the cerebral peduncle, terminating at the collicular (quadrigeminal) plate. An anastomosis between the PCA and [SCA](#structure-artery.posterior.sca_right) can occur at this location.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA collicular right](#structure-artery.amendment.pca_collicular.right)

**Connection endpoints:** [PCA collicular right](#structure-artery.amendment.pca_collicular.right); [SCA tectal branch right](#structure-artery.amendment.sca_tectal_branch.right)

<a id="structure-artery.connection.aica_sca_pial_border_zone.right"></a>

### AICA–SCA pial border zone right

**Model ID:** `artery.connection.aica_sca_pial_border_zone.right`

**Description**

The [AICA](#structure-artery.posterior.aica_right) has anastomoses with branches of the [PICA](#structure-artery.posterior.pica_right) and [SCA](#structure-artery.posterior.sca_right).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA rostral branch right](#structure-artery.posterior.aica_rostral_branch_right)

**Connection endpoints:** [AICA rostral branch right](#structure-artery.posterior.aica_rostral_branch_right); [SCA caudal hemispheric right](#structure-artery.posterior.sca_caudal_hemispheric_right)

<a id="structure-artery.connection.subarcuate_petrosal_mma.right"></a>

### Subarcuate–petrosal MMA right

**Model ID:** `artery.connection.subarcuate_petrosal_mma.right`

**Description**

The [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right)

**Connection endpoints:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right); [MMA petrosal artery right](#structure-artery.eca.maxillary.mma.petrosal.right)

<a id="structure-artery.connection.subarcuate_stylomastoid.right"></a>

### Subarcuate–stylomastoid right

**Model ID:** `artery.connection.subarcuate_stylomastoid.right`

**Description**

The [subarcuate branch](#structure-artery.amendment.aica_subarcuate.right) is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right)

**Connection endpoints:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right); [Stylomastoid artery right](#structure-artery.eca.occipital.stylomastoid.right)

<a id="structure-artery.connection.subarcuate_apa_auditory.right"></a>

### Subarcuate–APA auditory right

**Model ID:** `artery.connection.subarcuate_apa_auditory.right`

**Parent:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right)

**Connection endpoints:** [AICA subarcuate right](#structure-artery.amendment.aica_subarcuate.right); [Jugular ascending IAC branch right](#structure-artery.amendment.jugular_ascending_iac_branch.right)

<a id="structure-artery.connection.pica_sca_vermian_border_zone.right"></a>

### PICA–SCA vermian border zone right

**Model ID:** `artery.connection.pica_sca_vermian_border_zone.right`

**Description**

The superior vermian terminal branch of the [SCA](#structure-artery.posterior.sca_right) supplies the vermis and anastomoses with the [AICA](#structure-artery.posterior.aica_right) and [PICA](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [PICA vermian right](#structure-artery.posterior.pica_vermian_right)

**Connection endpoints:** [PICA vermian right](#structure-artery.posterior.pica_vermian_right); [SCA vermian right](#structure-artery.posterior.sca_vermian_right)

<a id="structure-artery.connection.pica_aica_pial_border_zone.right"></a>

### PICA–AICA pial border zone right

**Model ID:** `artery.connection.pica_aica_pial_border_zone.right`

**Description**

The [AICA](#structure-artery.posterior.aica_right) has anastomoses with branches of the [PICA](#structure-artery.posterior.pica_right) and [SCA](#structure-artery.posterior.sca_right).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [PICA hemispheric right](#structure-artery.posterior.pica_hemispheric_right)

**Connection endpoints:** [PICA hemispheric right](#structure-artery.posterior.pica_hemispheric_right); [AICA caudal branch right](#structure-artery.posterior.aica_caudal_branch_right)

<a id="connections-left"></a>

## Potential arterial connections, left

<a id="structure-artery.connection.mandibular_vidian_circle.left"></a>

### Mandibular–vidian circle left

**Model ID:** `artery.connection.mandibular_vidian_circle.left`

**Description**

The [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [pharyngeal trunk](#structure-artery.eca.apa.pharyngeal_trunk.right.left) contributes to the Eustachian tube anastomotic circle. It is connected to the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous)’s mandibular and vidian arteries and forms connections with the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) and [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left) (distal [IMA](#structure-artery.eca.maxillary.right.left)). It also sends a branch through the [foramen lacerum](#structure-landmark.foramen-lacerum.left) to the cavernous sinus, joining the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left) and the [ILT](#structure-artery.anterior.inferolateral_trunk_left) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous).

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Mandibular ICA branch left](#structure-artery.amendment.mandibular_ica_branch.left)

**Connection endpoints:** [Mandibular ICA branch left](#structure-artery.amendment.mandibular_ica_branch.left); [Vidian ICA contribution left](#structure-artery.anterior.vidian_ica_contribution_left)

<a id="structure-artery.connection.clival_posterior_cavernous_mma.left"></a>

### Clival–posterior cavernous MMA left

**Model ID:** `artery.connection.clival_posterior_cavernous_mma.left`

**Description**

The posterior cavernous branch of the [MMA](#structure-artery.eca.maxillary.mma.right.left) anastomoses with the medial clival artery and the carotid branch of the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left).

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Lateral clival MHT branch left](#structure-artery.amendment.lateral_clival_mht_branch.left)

**Connection endpoints:** [Lateral clival MHT branch left](#structure-artery.amendment.lateral_clival_mht_branch.left); [MMA posterior cavernous left](#structure-artery.amendment.mma_posterior_cavernous.left)

<a id="structure-artery.connection.basal_tentorial_sca_dural.left"></a>

### Basal tentorial–SCA dural left

**Model ID:** `artery.connection.basal_tentorial_sca_dural.left`

**Parent:** [Basal tentorial MHT branch left](#structure-artery.amendment.basal_tentorial_mht_branch.left)

**Connection endpoints:** [Basal tentorial MHT branch left](#structure-artery.amendment.basal_tentorial_mht_branch.left); [Wollschlaeger and Wollschlaeger artery left](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.left)

<a id="structure-artery.connection.anterior_falcine_mma_paramedian.left"></a>

### Anterior falcine–MMA paramedian left

**Model ID:** `artery.connection.anterior_falcine_mma_paramedian.left`

**Description**

Paramedian arteries: these are the terminal branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left). They are directed anteriorly or posteriorly along the superior sagittal sinus and anastomose with the anterior (from the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left)) or posterior (from the [ascending pharyngeal](#structure-artery.eca.apa.right.left)) falcine arteries. They deliver small branches to the superior sagittal sinus and falx cerebri. They also anastomose with dural branches of the posterior cerebral artery (PCA; Davidoff and Schechter) and the [superior cerebellar artery](#structure-artery.posterior.sca_left) ([SCA](#structure-artery.posterior.sca_left); [artery of Wollschlaeger and Wollschlaeger](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.left)).

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Anterior falcine left](#structure-artery.amendment.anterior_falcine.left)

**Connection endpoints:** [Anterior falcine left](#structure-artery.amendment.anterior_falcine.left); [MMA paramedian left](#structure-artery.amendment.mma_paramedian.left)

<a id="structure-artery.connection.deep_recurrent_ophthalmic_ilt.left"></a>

### Deep recurrent ophthalmic–ILT left

**Model ID:** `artery.connection.deep_recurrent_ophthalmic_ilt.left`

**Description**

The anteromedial ramus is directed towards the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left), supplying CNs III, IV, V1, and the abducens nerve (CN VI), and forming an anastomosis with the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) as the [deep recurrent ophthalmic artery](#structure-artery.amendment.deep_recurrent_ophthalmic.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [Deep recurrent ophthalmic left](#structure-artery.amendment.deep_recurrent_ophthalmic.left)

**Connection endpoints:** [Deep recurrent ophthalmic left](#structure-artery.amendment.deep_recurrent_ophthalmic.left); [ILT anteromedial ramus left](#structure-artery.anterior.ilt_anterior_branch_left)

<a id="structure-artery.connection.superior_palpebral_arcade.left"></a>

### Superior palpebral arcade left

**Model ID:** `artery.connection.superior_palpebral_arcade.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Medial superior palpebral left](#structure-artery.amendment.medial_superior_palpebral.left)

**Connection endpoints:** [Medial superior palpebral left](#structure-artery.amendment.medial_superior_palpebral.left); [Lateral superior palpebral left](#structure-artery.amendment.lateral_superior_palpebral.left)

<a id="structure-artery.connection.inferior_palpebral_arcade.left"></a>

### Inferior palpebral arcade left

**Model ID:** `artery.connection.inferior_palpebral_arcade.left`

**Description**

The [angular artery](#structure-artery.eca.angular.right.left) gives off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery from the [lacrimal artery](#structure-artery.anterior.lacrimal_left) to form the palpebral arcade.

**Source:** `nv(2).pdf`, PDF page 9; printed page 15.

**Parent:** [Medial inferior palpebral left](#structure-artery.amendment.medial_inferior_palpebral.left)

**Connection endpoints:** [Medial inferior palpebral left](#structure-artery.amendment.medial_inferior_palpebral.left); [Lateral inferior palpebral left](#structure-artery.amendment.lateral_inferior_palpebral.left)

<a id="structure-artery.connection.anterior_lateral_posterior_choroidal.left"></a>

### Anterior–lateral posterior choroidal left

**Model ID:** `artery.connection.anterior_lateral_posterior_choroidal.left`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) anastomoses with the posterior choroidal artery via its intraventricular terminal branches.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Anterior choroidal plexal representative left](#structure-artery.amendment.anterior_choroidal_plexal_representative.left)

**Connection endpoints:** [Anterior choroidal plexal representative left](#structure-artery.amendment.anterior_choroidal_plexal_representative.left); [Lateral posterior choroidal plexal representative left](#structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.left)

<a id="structure-artery.connection.aca_mca_frontal_border_zone.left"></a>

### ACA–MCA frontal border zone left

**Model ID:** `artery.connection.aca_mca_frontal_border_zone.left`

**Parent:** [Anterior internal frontal left](#structure-artery.anterior.anterior_internal_frontal_left)

**Connection endpoints:** [Anterior internal frontal left](#structure-artery.anterior.anterior_internal_frontal_left); [Prefrontal cortical branch left](#structure-artery.anterior.prefrontal_cortical_branch_left)

<a id="structure-artery.connection.aca_mca_parietal_border_zone.left"></a>

### ACA–MCA parietal border zone left

**Model ID:** `artery.connection.aca_mca_parietal_border_zone.left`

**Parent:** [Paracentral left](#structure-artery.anterior.paracentral_left)

**Connection endpoints:** [Paracentral left](#structure-artery.anterior.paracentral_left); [Anterior parietal cortical branch left](#structure-artery.anterior.anterior_parietal_cortical_branch_left)

<a id="structure-artery.connection.aca_falcine_mma_falcine.left"></a>

### ACA falcine–MMA falcine left

**Model ID:** `artery.connection.aca_falcine_mma_falcine.left`

**Parent:** [ACA falcine branch left](#structure-artery.amendment.aca_falcine_branch.left)

**Connection endpoints:** [ACA falcine branch left](#structure-artery.amendment.aca_falcine_branch.left); [MMA falcine terminal left](#structure-artery.amendment.mma_falcine_terminal.left)

<a id="structure-artery.connection.pericallosal_splenial.left"></a>

### Pericallosal–splenial left

**Model ID:** `artery.connection.pericallosal_splenial.left`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left)

**Connection endpoints:** [ACA pericallosal left](#structure-artery.anterior.aca_pericallosal_left); [PCA splenial left](#structure-artery.posterior.pca_splenial_left)

<a id="structure-artery.connection.mca_pca_occipital_border_zone.left"></a>

### MCA–PCA occipital border zone left

**Model ID:** `artery.connection.mca_pca_occipital_border_zone.left`

**Parent:** [Angular cortical branch left](#structure-artery.anterior.angular_cortical_branch_left)

**Connection endpoints:** [Angular cortical branch left](#structure-artery.anterior.angular_cortical_branch_left); [PCA parieto-occipital left](#structure-artery.posterior.pca_parieto_occipital_left)

<a id="structure-artery.connection.mca_pca_temporal_border_zone.left"></a>

### MCA–PCA temporal border zone left

**Model ID:** `artery.connection.mca_pca_temporal_border_zone.left`

**Parent:** [Posterior temporal cortical branch left](#structure-artery.anterior.posterior_temporal_cortical_branch_left)

**Connection endpoints:** [Posterior temporal cortical branch left](#structure-artery.anterior.posterior_temporal_cortical_branch_left); [PCA posterior inferior temporal left](#structure-artery.posterior.pca_posterior_inferior_temporal_left)

<a id="structure-artery.connection.angular_dorsal_nasal.left"></a>

### Angular–dorsal nasal left

**Model ID:** `artery.connection.angular_dorsal_nasal.left`

**Description**

Anastomoses to the distal [ophthalmic artery](#structure-artery.anterior.ophthalmic_left) include the distal [facial artery](#structure-artery.eca.facial.right.left) via the [dorsal nasal artery](#structure-artery.anterior.dorsal_nasal_left).

[Angular artery](#structure-artery.eca.angular.right.left): if present, this is the terminal branch of the [facial artery](#structure-artery.eca.facial.right.left). It may also originate from the ophthalmic or [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left). The vessel courses in the nasojugal fold giving off the medial palpebral artery supplying the eyelids, and anastomoses with the lateral palpebral artery ([lacrimal artery](#structure-artery.anterior.lacrimal_left)) to form the palpebral arcade. There are anastomoses with the ophthalmic, [lateral nasal](#structure-artery.eca.lateral_nasal.right.left), and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left) in addition to its counterpart across the midline.

**Source:** `nv(2).pdf`, PDF pages 9, 54; printed pages 15, 60.

**Parent:** [Angular artery left](#structure-artery.eca.angular.right.left)

**Connection endpoints:** [Angular artery left](#structure-artery.eca.angular.right.left); [Dorsal nasal left](#structure-artery.anterior.dorsal_nasal_left)

<a id="structure-artery.connection.labial_septal_plexus.left"></a>

### Labial–septal plexus left

**Model ID:** `artery.connection.labial_septal_plexus.left`

**Description**

The [superior labial artery](#structure-artery.eca.superior_labial.right.left) delivers branches to the nasal septum and ala and can anastomose with the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left).

Kiesselbach’s plexus is supplied by the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left), [superior labial](#structure-artery.eca.superior_labial.right.left), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_left), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_left) arteries.

**Source:** `nv(2).pdf`, PDF pages 9, 23; printed pages 15, 29.

**Parent:** [Superior labial artery left](#structure-artery.eca.superior_labial.right.left)

**Connection endpoints:** [Superior labial artery left](#structure-artery.eca.superior_labial.right.left); [Inferior septal subdivision left](#structure-artery.amendment.inferior_septal_subdivision.left)

<a id="structure-artery.connection.facial_maxillary_masseteric.left"></a>

### Facial–maxillary masseteric left

**Model ID:** `artery.connection.facial_maxillary_masseteric.left`

**Description**

The [masseteric artery](#structure-artery.eca.maxillary.masseteric.right.left) anastomoses with masseteric branches of the [facial artery](#structure-artery.eca.facial.right.left) and [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left).

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Facial masseteric branch left](#structure-artery.amendment.facial_masseteric_branch.left)

**Connection endpoints:** [Facial masseteric branch left](#structure-artery.amendment.facial_masseteric_branch.left); [Masseteric artery left](#structure-artery.eca.maxillary.masseteric.right.left)

<a id="structure-artery.connection.facial_maxillary_buccal.left"></a>

### Facial–maxillary buccal left

**Model ID:** `artery.connection.facial_maxillary_buccal.left`

**Description**

Anastomoses: ascending branch of the [facial artery](#structure-artery.eca.facial.right.left) and the superior masseteric branch of the [transverse facial artery](#structure-artery.eca.superficial_temporal.transverse_facial.right.left). It is an important route for [facial artery](#structure-artery.eca.facial.right.left) reconstitution after proximal [facial artery](#structure-artery.eca.facial.right.left) ligation.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Facial buccal branch left](#structure-artery.amendment.facial_buccal_branch.left)

**Connection endpoints:** [Facial buccal branch left](#structure-artery.amendment.facial_buccal_branch.left); [Buccal artery left](#structure-artery.eca.maxillary.buccal.right.left)

<a id="structure-artery.connection.occipital_posterior_auricular_scalp.left"></a>

### Occipital–posterior auricular scalp left

**Model ID:** `artery.connection.occipital_posterior_auricular_scalp.left`

**Parent:** [Occipital lateral scalp artery left](#structure-artery.eca.occipital_lateral_scalp.right.left)

**Connection endpoints:** [Occipital lateral scalp artery left](#structure-artery.eca.occipital_lateral_scalp.right.left); [Posterior auricular artery left](#structure-artery.eca.posterior_auricular.right.left)

<a id="structure-artery.connection.occipital_mma_transosseous_potential.left"></a>

### Occipital–MMA transosseous potential left

**Model ID:** `artery.connection.occipital_mma_transosseous_potential.left`

**Description**

All peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right.left) and [occipital artery](#structure-artery.eca.occipital.right.left) via transosseous branches, which become evident under pathological conditions, in particular dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Occipital lateral scalp artery left](#structure-artery.eca.occipital_lateral_scalp.right.left)

**Connection endpoints:** [Occipital lateral scalp artery left](#structure-artery.eca.occipital_lateral_scalp.right.left); [MMA posterior convexity artery left](#structure-artery.eca.maxillary.mma.posterior_convexity.right.left)

<a id="structure-artery.connection.occipital_descending_vertebral_c2.left"></a>

### Occipital descending–vertebral C2 left

**Model ID:** `artery.connection.occipital_descending_vertebral_c2.left`

**Description**

The [occipital artery](#structure-artery.eca.occipital.right.left), derived from embryological type I and II proatlantal arteries (C1 and C2 segmental arteries), maintains anastomotic pathways from the [ECA](#structure-artery.carotid.external.right.left) to the [vertebral artery](#structure-artery.posterior.vertebral_left) via posterior radicular branches at the C1 and C2 levels. These connections serve as major collateral pathways from the [vertebral artery](#structure-artery.posterior.vertebral_left) to the carotid system, particularly visible in cases where the common carotid is ligated or occluded.

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Occipital descending artery left](#structure-artery.eca.occipital_descending.right.left)

**Connection endpoints:** [Occipital descending artery left](#structure-artery.eca.occipital_descending.right.left); [VA muscular C2 left](#structure-artery.posterior.va_muscular_c2_left)

<a id="structure-artery.connection.occipital_mastoid_apa_sigmoid.left"></a>

### Occipital mastoid–APA sigmoid left

**Model ID:** `artery.connection.occipital_mastoid_apa_sigmoid.left`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left)

**Connection endpoints:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left); [Jugular sigmoid branch left](#structure-artery.eca.apa.sigmoid_sinus_branch.right.left)

<a id="structure-artery.connection.occipital_mastoid_mma_petrosquamosal.left"></a>

### Occipital mastoid–MMA petrosquamosal left

**Model ID:** `artery.connection.occipital_mastoid_mma_petrosquamosal.left`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left)

**Connection endpoints:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left); [MMA petrosquamosal artery left](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left)

<a id="structure-artery.connection.occipital_mastoid_apa_jugular.left"></a>

### Occipital mastoid–APA jugular left

**Model ID:** `artery.connection.occipital_mastoid_apa_jugular.left`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left)

**Connection endpoints:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left); [Jugular branch left](#structure-artery.eca.apa.jugular.right.left)

<a id="structure-artery.connection.occipital_mastoid_hypoglossal_meningeal.left"></a>

### Occipital mastoid–hypoglossal meningeal left

**Model ID:** `artery.connection.occipital_mastoid_hypoglossal_meningeal.left`

**Description**

A large mastoid branch often continues superiorly and then enters the cranium through the [mastoid foramen](#structure-landmark.mastoid-foramen.left) to supply the posterior fossa dura mater: the posterior meningeal artery. It divides into descending, ascending, and posteromedial branches. The descending branch courses along the sigmoid sinus and anastomoses with the sigmoid sinus branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left). The ascending branch runs posterosuperiorly along the sigmoid sinus before anastomosing with the [petrosquamous branch of the MMA](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left) and sometimes the [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) of the [AICA](#structure-artery.posterior.aica_left). The posteromedial branch courses inferomedially and anastomoses with the hypoglossal, jugular, and musculospinal branches of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), or the jugular branch of the [posterior meningeal artery from the vertebral artery](#structure-artery.posterior.posterior_meningeal_va_left).

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left)

**Connection endpoints:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left); [Hypoglossal posterior meningeal artery left](#structure-artery.eca.apa.posterior_meningeal.right.left)

<a id="structure-artery.connection.occipital_tentorial_pca_dural.left"></a>

### Occipital tentorial–PCA dural left

**Model ID:** `artery.connection.occipital_tentorial_pca_dural.left`

**Parent:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left)

**Connection endpoints:** [Occipital mastoid dural branch left](#structure-artery.amendment.occipital_mastoid_dural_branch.left); [Davidoff and Schechter artery left](#structure-artery.amendment.davidoff_and_schechter_artery.left)

<a id="structure-artery.connection.occipital_vertebral_c1.left"></a>

### Occipital–vertebral C1 left

**Model ID:** `artery.connection.occipital_vertebral_c1.left`

**Description**

The [occipital artery](#structure-artery.eca.occipital.right.left), derived from embryological type I and II proatlantal arteries (C1 and C2 segmental arteries), maintains anastomotic pathways from the [ECA](#structure-artery.carotid.external.right.left) to the [vertebral artery](#structure-artery.posterior.vertebral_left) via posterior radicular branches at the C1 and C2 levels. These connections serve as major collateral pathways from the [vertebral artery](#structure-artery.posterior.vertebral_left) to the carotid system, particularly visible in cases where the common carotid is ligated or occluded.

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Occipital artery left](#structure-artery.eca.occipital.right.left)

**Connection endpoints:** [Occipital artery left](#structure-artery.eca.occipital.right.left); [VA muscular C1 left](#structure-artery.posterior.va_muscular_c1_left)

<a id="structure-artery.connection.stylomastoid_inferior_tympanic.left"></a>

### Stylomastoid–inferior tympanic left

**Model ID:** `artery.connection.stylomastoid_inferior_tympanic.left`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right.left) enters the tympanic cavity and anastomoses with the [superior tympanic artery](#structure-artery.amendment.superior_tympanic.left) from the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right.left), [anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left) branch of the [IMA](#structure-artery.eca.maxillary.right.left), the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left) branch of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), the [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) branch of the [ICA](#structure-artery.anterior.internal_carotid_left), and the arcuate branch of the [anterior inferior cerebellar artery](#structure-artery.posterior.aica_left) ([AICA](#structure-artery.posterior.aica_left)).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Stylomastoid artery left](#structure-artery.eca.occipital.stylomastoid.right.left)

**Connection endpoints:** [Stylomastoid artery left](#structure-artery.eca.occipital.stylomastoid.right.left); [Inferior tympanic artery left](#structure-artery.eca.apa.inferior_tympanic.right.left)

<a id="structure-artery.connection.sta_supratrochlear_scalp.left"></a>

### STA–supratrochlear scalp left

**Model ID:** `artery.connection.sta_supratrochlear_scalp.left`

**Parent:** [STA frontal anterior twig artery left](#structure-artery.eca.sta_frontal_anterior_twig.right.left)

**Connection endpoints:** [STA frontal anterior twig artery left](#structure-artery.eca.sta_frontal_anterior_twig.right.left); [Supratrochlear left](#structure-artery.anterior.supratrochlear_left)

<a id="structure-artery.connection.sta_supraorbital.left"></a>

### STA–supraorbital left

**Model ID:** `artery.connection.sta_supraorbital.left`

**Description**

The [frontal division of the STA](#structure-artery.eca.superficial_temporal.frontal.right.left) anastomoses with the supraorbital and frontal branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA frontal artery left](#structure-artery.eca.superficial_temporal.frontal.right.left)

**Connection endpoints:** [STA frontal artery left](#structure-artery.eca.superficial_temporal.frontal.right.left); [Supraorbital left](#structure-artery.anterior.supraorbital_left)

<a id="structure-artery.connection.sta_occipital_scalp.left"></a>

### STA–occipital scalp left

**Model ID:** `artery.connection.sta_occipital_scalp.left`

**Description**

The [parietal division of the STA](#structure-artery.eca.superficial_temporal.parietal.right.left) runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right.left), and [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA parietal artery left](#structure-artery.eca.superficial_temporal.parietal.right.left)

**Connection endpoints:** [STA parietal artery left](#structure-artery.eca.superficial_temporal.parietal.right.left); [Occipital lateral scalp artery left](#structure-artery.eca.occipital_lateral_scalp.right.left)

<a id="structure-artery.connection.sta_mma_transosseous_potential.left"></a>

### STA–MMA transosseous potential left

**Model ID:** `artery.connection.sta_mma_transosseous_potential.left`

**Description**

All peripheral branches of the [MMA](#structure-artery.eca.maxillary.mma.right.left) have potential anastomoses with more superficial arteries such as the [STA](#structure-artery.eca.superficial_temporal.right.left) and [occipital artery](#structure-artery.eca.occipital.right.left) via transosseous branches, which become evident under pathological conditions, in particular dural arteriovenous fistulas.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [STA parietal artery left](#structure-artery.eca.superficial_temporal.parietal.right.left)

**Connection endpoints:** [STA parietal artery left](#structure-artery.eca.superficial_temporal.parietal.right.left); [MMA parietal ascending artery left](#structure-artery.eca.mma_parietal_ascending.right.left)

<a id="structure-artery.connection.transverse_facial_infraorbital.left"></a>

### Transverse facial–infraorbital left

**Model ID:** `artery.connection.transverse_facial_infraorbital.left`

**Description**

The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial superior division left](#structure-artery.amendment.transverse_facial_superior_division.left)

**Connection endpoints:** [Transverse facial superior division left](#structure-artery.amendment.transverse_facial_superior_division.left); [Infraorbital artery left](#structure-artery.eca.maxillary.infraorbital.right.left)

<a id="structure-artery.connection.transverse_facial_facial.left"></a>

### Transverse facial–facial left

**Model ID:** `artery.connection.transverse_facial_facial.left`

**Description**

The superior division passes through and supplies the parotid gland before running anteriorly and supplying the face, parotid duct, regional musculature, and the facial nerve. It anastomoses with the [infraorbital](#structure-artery.eca.maxillary.infraorbital.right.left), zygomaticomalar, inferior palpebral, buccal, and facial arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Transverse facial inferior division left](#structure-artery.amendment.transverse_facial_inferior_division.left)

**Connection endpoints:** [Transverse facial inferior division left](#structure-artery.amendment.transverse_facial_inferior_division.left); [Facial artery left](#structure-artery.eca.facial.right.left)

<a id="structure-artery.connection.sta_posterior_auricular_scalp.left"></a>

### STA–posterior auricular scalp left

**Model ID:** `artery.connection.sta_posterior_auricular_scalp.left`

**Description**

The [parietal division of the STA](#structure-artery.eca.superficial_temporal.parietal.right.left) runs posterosuperiorly and anastomoses with the occipital, [deep middle temporal](#structure-artery.eca.middle_temporal.right.left), and [posterior auricular](#structure-artery.eca.posterior_auricular.right.left) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [STA anterior auricular left](#structure-artery.amendment.sta_anterior_auricular.left)

**Connection endpoints:** [STA anterior auricular left](#structure-artery.amendment.sta_anterior_auricular.left); [Posterior auricular auricular branch left](#structure-artery.amendment.posterior_auricular_auricular_branch.left)

<a id="structure-artery.connection.zygomatico_orbital_lacrimal.left"></a>

### Zygomatico-orbital–lacrimal left

**Model ID:** `artery.connection.zygomatico_orbital_lacrimal.left`

**Parent:** [Zygomatico-orbital left](#structure-artery.amendment.zygomatico_orbital.left)

**Connection endpoints:** [Zygomatico-orbital left](#structure-artery.amendment.zygomatico_orbital.left); [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.connection.deep_temporal_lacrimal.left"></a>

### Deep temporal–lacrimal left

**Model ID:** `artery.connection.deep_temporal_lacrimal.left`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right.left) has anastomoses with the [inferior branch of the lacrimal artery](#structure-artery.amendment.lacrimal_inferior_branch.left) via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right.left) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Anterior deep temporal artery left](#structure-artery.eca.anterior_deep_temporal.right.left)

**Connection endpoints:** [Anterior deep temporal artery left](#structure-artery.eca.anterior_deep_temporal.right.left); [Lacrimal inferior branch left](#structure-artery.amendment.lacrimal_inferior_branch.left)

<a id="structure-artery.connection.infraorbital_ophthalmic.left"></a>

### Infraorbital–ophthalmic left

**Model ID:** `artery.connection.infraorbital_ophthalmic.left`

**Description**

Anastomoses: the terminal branches anastomose with the superficial temporal, ophthalmic, facial, and [transverse facial](#structure-artery.eca.superficial_temporal.transverse_facial.right.left) arteries.

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) gives off osseous and muscular branches on the orbital floor, anastomosing with the inferior muscular branches of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Infraorbital muscular branch left](#structure-artery.amendment.infraorbital_muscular_branch.left)

**Connection endpoints:** [Infraorbital muscular branch left](#structure-artery.amendment.infraorbital_muscular_branch.left); [Ophthalmic inferior muscular branch left](#structure-artery.amendment.ophthalmic_inferior_muscular_branch.left)

<a id="structure-artery.connection.inferior_lacrimal_infraorbital_muscular.left"></a>

### Inferior lacrimal–infraorbital muscular left

**Model ID:** `artery.connection.inferior_lacrimal_infraorbital_muscular.left`

**Description**

The distal [IMA](#structure-artery.eca.maxillary.right.left) has anastomoses with the [inferior branch of the lacrimal artery](#structure-artery.amendment.lacrimal_inferior_branch.left) via the [anterior deep temporal](#structure-artery.eca.anterior_deep_temporal.right.left) and [infraorbital arteries](#structure-artery.eca.maxillary.infraorbital.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Infraorbital muscular branch left](#structure-artery.amendment.infraorbital_muscular_branch.left)

**Connection endpoints:** [Infraorbital muscular branch left](#structure-artery.amendment.infraorbital_muscular_branch.left); [Lacrimal inferior branch left](#structure-artery.amendment.lacrimal_inferior_branch.left)

<a id="structure-artery.connection.septal_anterior_ethmoidal.left"></a>

### Septal–anterior ethmoidal left

**Model ID:** `artery.connection.septal_anterior_ethmoidal.left`

**Description**

The [posterior septal artery](#structure-artery.eca.posterior_septal.right.left) anastomoses with branches of the [anterior ethmoidal artery](#structure-artery.anterior.anterior_ethmoidal_left) and [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) and contributes to Kiesselbach’s plexus.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Posterior septal artery left](#structure-artery.eca.posterior_septal.right.left)

**Connection endpoints:** [Posterior septal artery left](#structure-artery.eca.posterior_septal.right.left); [Anterior ethmoidal left](#structure-artery.anterior.anterior_ethmoidal_left)

<a id="structure-artery.connection.posterior_septal_posterior_ethmoidal.left"></a>

### Posterior septal–posterior ethmoidal left

**Model ID:** `artery.connection.posterior_septal_posterior_ethmoidal.left`

**Description**

Kiesselbach’s plexus is located on the anterior inferior quadrant of the nasal septum (Little’s area). It is supplied by five vessels: the [sphenopalatine](#structure-artery.eca.maxillary.sphenopalatine.right.left), [superior labial](#structure-artery.eca.superior_labial.right.left), greater palatine, [anterior ethmoidal](#structure-artery.anterior.anterior_ethmoidal_left), and [posterior ethmoidal](#structure-artery.anterior.posterior_ethmoidal_left) arteries.

**Source:** `nv(2).pdf`, PDF page 23; printed page 29.

**Parent:** [Superior septal subdivision left](#structure-artery.amendment.superior_septal_subdivision.left)

**Connection endpoints:** [Superior septal subdivision left](#structure-artery.amendment.superior_septal_subdivision.left); [Posterior ethmoidal left](#structure-artery.anterior.posterior_ethmoidal_left)

<a id="structure-artery.connection.septal_palatine_network.left"></a>

### Septal–palatine network left

**Model ID:** `artery.connection.septal_palatine_network.left`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) anastomoses with the [posterior septal arteries](#structure-artery.eca.posterior_septal.right.left) from the [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left) and with the [ascending palatine artery](#structure-artery.eca.ascending_palatine.right.left).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Inferior septal subdivision left](#structure-artery.amendment.inferior_septal_subdivision.left)

**Connection endpoints:** [Inferior septal subdivision left](#structure-artery.amendment.inferior_septal_subdivision.left); [Greater palatine artery left](#structure-artery.eca.greater_palatine.right.left)

<a id="structure-artery.connection.vidian_eca_ica.left"></a>

### Vidian ECA–ICA left

**Model ID:** `artery.connection.vidian_eca_ica.left`

**Description**

The vidian artery, running horizontally, arises from the distal [IMA](#structure-artery.eca.maxillary.right.left) and runs through the [vidian canal](#structure-landmark.pterygoid-canal.left) to the [foramen lacerum](#structure-landmark.foramen-lacerum.left), where it meets the [vidian branch of the mandibulovidian artery](#structure-artery.anterior.vidian_ica_contribution_left) from the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Vidian artery left](#structure-artery.eca.maxillary.pterygoid_canal.right.left)

**Connection endpoints:** [Vidian artery left](#structure-artery.eca.maxillary.pterygoid_canal.right.left); [Vidian ICA contribution left](#structure-artery.anterior.vidian_ica_contribution_left)

<a id="structure-artery.connection.foramen_rotundum_ilt.left"></a>

### Foramen rotundum–ILT left

**Model ID:** `artery.connection.foramen_rotundum_ilt.left`

**Description**

The [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left) from the [IMA](#structure-artery.eca.maxillary.right.left) connects to the [anterolateral branch of the ILT](#structure-artery.amendment.ilt_anterolateral_ramus.left) and, in rare instances, with the lateral clival artery.

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Artery of the foramen rotundum left](#structure-artery.eca.maxillary.foramen_rotundum.right.left)

**Connection endpoints:** [Artery of the foramen rotundum left](#structure-artery.eca.maxillary.foramen_rotundum.right.left); [ILT anterolateral ramus left](#structure-artery.amendment.ilt_anterolateral_ramus.left)

<a id="structure-artery.connection.accessory_meningeal_ilt.left"></a>

### Accessory meningeal–ILT left

**Model ID:** `artery.connection.accessory_meningeal_ilt.left`

**Description**

The superior division of the [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right.left) enters the cavernous sinus through the [foramen ovale](#structure-landmark.ovale.left) to connect with the [posteromedial branch of the ILT](#structure-artery.amendment.ilt_posteromedial_ramus.left), which runs beneath the trigeminal ganglion and along the second branch of the trigeminal nerve (CN V2).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Accessory meningeal posterior intracranial left](#structure-artery.amendment.accessory_meningeal_posterior_intracranial.left)

**Connection endpoints:** [Accessory meningeal posterior intracranial left](#structure-artery.amendment.accessory_meningeal_posterior_intracranial.left); [ILT posteromedial ramus left](#structure-artery.amendment.ilt_posteromedial_ramus.left)

<a id="structure-artery.connection.mma_tentorial_marginal.left"></a>

### MMA–tentorial marginal left

**Model ID:** `artery.connection.mma_tentorial_marginal.left`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right.left)’s petrosquamous or posterior branch also anastomoses with the [marginal tentorial artery](#structure-artery.anterior.tentorial_marginal_left), which may originate from the [ILT](#structure-artery.anterior.inferolateral_trunk_left), [ophthalmic artery](#structure-artery.anterior.ophthalmic_left), or the [MHT](#structure-artery.anterior.meningohypophyseal_trunk_left) of the [ICA](#structure-artery.anterior.internal_carotid_left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [MMA petrosquamosal artery left](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left)

**Connection endpoints:** [MMA petrosquamosal artery left](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left); [Tentorial marginal left](#structure-artery.anterior.tentorial_marginal_left)

<a id="structure-artery.connection.mma_tentorial_pca_dural.left"></a>

### MMA tentorial–PCA dural left

**Model ID:** `artery.connection.mma_tentorial_pca_dural.left`

**Parent:** [MMA petrosquamosal artery left](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left)

**Connection endpoints:** [MMA petrosquamosal artery left](#structure-artery.eca.maxillary.mma.petrosquamosal.right.left); [Davidoff and Schechter artery left](#structure-artery.amendment.davidoff_and_schechter_artery.left)

<a id="structure-artery.connection.superior_anterior_tympanic.left"></a>

### Superior–anterior tympanic left

**Model ID:** `artery.connection.superior_anterior_tympanic.left`

**Description**

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right.left) supplies the mandibular joint and the tympanic cavity, where it anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left), [superior tympanic](#structure-artery.amendment.superior_tympanic.left), and [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superior tympanic left](#structure-artery.amendment.superior_tympanic.left)

**Connection endpoints:** [Superior tympanic left](#structure-artery.amendment.superior_tympanic.left); [Anterior tympanic artery left](#structure-artery.eca.maxillary.anterior_tympanic.right.left)

<a id="structure-artery.connection.superior_inferior_tympanic.left"></a>

### Superior–inferior tympanic left

**Model ID:** `artery.connection.superior_inferior_tympanic.left`

**Description**

The [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right.left) supplies the mandibular joint and the tympanic cavity, where it anastomoses with the [inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left), [superior tympanic](#structure-artery.amendment.superior_tympanic.left), and [caroticotympanic](#structure-artery.anterior.caroticotympanic_left) arteries.

**Source:** `nv(2).pdf`, PDF page 10; printed page 16.

**Parent:** [Superior tympanic left](#structure-artery.amendment.superior_tympanic.left)

**Connection endpoints:** [Superior tympanic left](#structure-artery.amendment.superior_tympanic.left); [Inferior tympanic artery left](#structure-artery.eca.apa.inferior_tympanic.right.left)

<a id="structure-artery.connection.facial_nerve_arcade.left"></a>

### Facial nerve arcade left

**Model ID:** `artery.connection.facial_nerve_arcade.left`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right.left) enters the [stylomastoid foramen](#structure-landmark.stylomastoid.left) with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right.left).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [MMA petrosal artery left](#structure-artery.eca.maxillary.mma.petrosal.right.left)

**Connection endpoints:** [MMA petrosal artery left](#structure-artery.eca.maxillary.mma.petrosal.right.left); [Stylomastoid artery left](#structure-artery.eca.occipital.stylomastoid.right.left)

<a id="structure-artery.connection.mma_cavernous_ilt.left"></a>

### MMA cavernous–ILT left

**Model ID:** `artery.connection.mma_cavernous_ilt.left`

**Description**

After entering the [foramen spinosum](#structure-landmark.foramen-spinosum.left), the [MMA](#structure-artery.eca.maxillary.mma.right.left) has cavernous branches that connect with the superior or tentorial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left), and orbital branches that anastomose within the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left) with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left).

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [MMA anterior cavernous left](#structure-artery.amendment.mma_anterior_cavernous.left)

**Connection endpoints:** [MMA anterior cavernous left](#structure-artery.amendment.mma_anterior_cavernous.left); [ILT superior ramus left](#structure-artery.amendment.ilt_superior_ramus.left)

<a id="structure-artery.connection.posterior_cavernous_mma_posterolateral_ilt.left"></a>

### Posterior cavernous MMA–posterolateral ILT left

**Model ID:** `artery.connection.posterior_cavernous_mma_posterolateral_ilt.left`

**Description**

The posterolateral branch supplies the trigeminal ganglion and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) at the [foramen spinosum](#structure-landmark.foramen-spinosum.left).

**Source:** `nv(2).pdf`, PDF page 28; printed page 34.

**Parent:** [MMA posterior cavernous left](#structure-artery.amendment.mma_posterior_cavernous.left)

**Connection endpoints:** [MMA posterior cavernous left](#structure-artery.amendment.mma_posterior_cavernous.left); [ILT posterior division (posterolateral continuation) left](#structure-artery.anterior.ilt_posterior_branch_left)

<a id="structure-artery.connection.mma_lacrimal__meningolacrimal.left"></a>

### MMA–lacrimal (meningolacrimal) left

**Model ID:** `artery.connection.mma_lacrimal__meningolacrimal.left`

**Description**

Meningolacrimal artery: partial supply only of the lacrimal gland from the [MMA](#structure-artery.eca.maxillary.mma.right.left) via the [foramen of Hyrtl](#structure-landmark.cranio-orbital.left).

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [MMA orbital artery left](#structure-artery.eca.mma_orbital.right.left)

**Connection endpoints:** [MMA orbital artery left](#structure-artery.eca.mma_orbital.right.left); [Lacrimal left](#structure-artery.anterior.lacrimal_left)

<a id="structure-artery.connection.mma_ophthalmic__recurrent_meningeal.left"></a>

### MMA–ophthalmic (recurrent meningeal) left

**Model ID:** `artery.connection.mma_ophthalmic__recurrent_meningeal.left`

**Description**

The [recurrent meningeal branch of the lacrimal artery](#structure-artery.amendment.superficial_recurrent_meningeal.left) courses through the [superior orbital fissure](#structure-landmark.superior-orbital-fissure.left) to connect with the [MMA](#structure-artery.eca.maxillary.mma.right.left).

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [MMA orbital artery left](#structure-artery.eca.mma_orbital.right.left)

**Connection endpoints:** [MMA orbital artery left](#structure-artery.eca.mma_orbital.right.left); [Superficial recurrent meningeal left](#structure-artery.amendment.superficial_recurrent_meningeal.left)

<a id="structure-artery.connection.sof_artery_anteromedial_ilt.left"></a>

### SOF artery–anteromedial ILT left

**Model ID:** `artery.connection.sof_artery_anteromedial_ilt.left`

**Description**

The [artery of the superior orbital fissure](#structure-artery.amendment.artery_of_superior_orbital_fissure.left) anastomoses with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and the recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Artery of superior orbital fissure left](#structure-artery.amendment.artery_of_superior_orbital_fissure.left)

**Connection endpoints:** [Artery of superior orbital fissure left](#structure-artery.amendment.artery_of_superior_orbital_fissure.left); [ILT anteromedial ramus left](#structure-artery.anterior.ilt_anterior_branch_left)

<a id="structure-artery.connection.sof_artery_recurrent_meningeal.left"></a>

### SOF artery–recurrent meningeal left

**Model ID:** `artery.connection.sof_artery_recurrent_meningeal.left`

**Description**

The [artery of the superior orbital fissure](#structure-artery.amendment.artery_of_superior_orbital_fissure.left) anastomoses with the anteromedial branch of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and the recurrent meningeal branch of the lacrimal branch of the [ophthalmic artery](#structure-artery.anterior.ophthalmic_left).

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Artery of superior orbital fissure left](#structure-artery.amendment.artery_of_superior_orbital_fissure.left)

**Connection endpoints:** [Artery of superior orbital fissure left](#structure-artery.amendment.artery_of_superior_orbital_fissure.left); [Superficial recurrent meningeal left](#structure-artery.amendment.superficial_recurrent_meningeal.left)

<a id="structure-artery.connection.tubal_accessory_meningeal_circle.left"></a>

### Tubal–accessory meningeal circle left

**Model ID:** `artery.connection.tubal_accessory_meningeal_circle.left`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right.left) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.left), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left) from the distal [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left)

**Connection endpoints:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left); [Accessory meningeal anterior tubal left](#structure-artery.amendment.accessory_meningeal_anterior_tubal.left)

<a id="structure-artery.connection.tubal_mandibular_ica_circle.left"></a>

### Tubal–mandibular ICA circle left

**Model ID:** `artery.connection.tubal_mandibular_ica_circle.left`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right.left) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.left), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left) from the distal [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left)

**Connection endpoints:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left); [Mandibular ICA branch left](#structure-artery.amendment.mandibular_ica_branch.left)

<a id="structure-artery.connection.tubal_pterygovaginal_circle.left"></a>

### Tubal–pterygovaginal circle left

**Model ID:** `artery.connection.tubal_pterygovaginal_circle.left`

**Description**

The [AMA](#structure-artery.eca.maxillary.accessory_meningeal.right.left) forms smaller anastomotic connections around the Eustachian tube with the [superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left) of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left), the [mandibular branch of the petrous ICA](#structure-artery.amendment.mandibular_ica_branch.left), and the [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left) from the distal [IMA](#structure-artery.eca.maxillary.right.left).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left)

**Connection endpoints:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left); [Pterygovaginal artery left](#structure-artery.eca.pterygovaginal.right.left)

<a id="structure-artery.connection.tubal_maxillary_vidian_circle.left"></a>

### Tubal–maxillary vidian circle left

**Model ID:** `artery.connection.tubal_maxillary_vidian_circle.left`

**Description**

Anastomoses: [vidian artery of the ICA](#structure-artery.anterior.vidian_ica_contribution_left), [pterygovaginal artery](#structure-artery.eca.pterygovaginal.right.left), mandibular artery, [ascending pharyngeal](#structure-artery.eca.apa.right.left) ([superior pharyngeal branch](#structure-artery.eca.superior_pharyngeal.right.left)), [accessory meningeal](#structure-artery.eca.maxillary.accessory_meningeal.right.left), and [ascending palatine](#structure-artery.eca.ascending_palatine.right.left) arteries (the pharyngeal/Eustachian tube anastomosis).

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left)

**Connection endpoints:** [Superior pharyngeal tubal branch left](#structure-artery.amendment.superior_pharyngeal_tubal_branch.left); [Vidian artery left](#structure-artery.eca.maxillary.pterygoid_canal.right.left)

<a id="structure-artery.connection.pharyngeal_carotid_recurrent_lacerum.left"></a>

### Pharyngeal carotid–recurrent lacerum left

**Model ID:** `artery.connection.pharyngeal_carotid_recurrent_lacerum.left`

**Description**

The [carotid branch of the superior pharyngeal artery](#structure-artery.amendment.superior_pharyngeal_carotid_branch.left) traverses the [foramen lacerum](#structure-landmark.foramen-lacerum.left) to anastomose with the [recurrent artery of the foramen lacerum](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left) from the [ILT](#structure-artery.anterior.inferolateral_trunk_left) of the [ICA](#structure-artery.anterior.internal_carotid_left), both ipsilateral and contralateral.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Superior pharyngeal carotid branch left](#structure-artery.amendment.superior_pharyngeal_carotid_branch.left)

**Connection endpoints:** [Superior pharyngeal carotid branch left](#structure-artery.amendment.superior_pharyngeal_carotid_branch.left); [ILT recurrent lacerum ramus left](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left)

<a id="structure-artery.connection.apha_clival_mht.left"></a>

### APhA clival–MHT left

**Model ID:** `artery.connection.apha_clival_mht.left`

**Description**

The [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left) divides into jugular and hypoglossal branches, each giving off medial and lateral clival branches which anastomose with clival branches from the [MHT](#structure-artery.anterior.meningohypophyseal_trunk_left) from the [cavernous ICA](#structure-artery.anterior.internal_carotid_left.segment.cavernous): important in the vascular supply to meningiomas.

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Medial clival artery left](#structure-artery.eca.medial_clival.right.left)

**Connection endpoints:** [Medial clival artery left](#structure-artery.eca.medial_clival.right.left); [Medial clival MHT branch left](#structure-artery.amendment.medial_clival_mht_branch.left)

<a id="structure-artery.connection.apha_odontoid_vertebral.left"></a>

### APhA odontoid–vertebral left

**Model ID:** `artery.connection.apha_odontoid_vertebral.left`

**Description**

The [prevertebral branch](#structure-artery.amendment.apa_prevertebral_branch.left), running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_left) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [Odontoid descending artery left](#structure-artery.eca.apa.descending_odontoid.right.left)

**Connection endpoints:** [Odontoid descending artery left](#structure-artery.eca.apa.descending_odontoid.right.left); [VA odontoid contribution left](#structure-artery.posterior.va_odontoid_contribution_left)

<a id="structure-artery.connection.falx_cerebelli_va_posterior_meningeal.left"></a>

### Falx cerebelli–VA posterior meningeal left

**Model ID:** `artery.connection.falx_cerebelli_va_posterior_meningeal.left`

**Parent:** [Falx cerebelli artery left](#structure-artery.amendment.falx_cerebelli_artery.left)

**Connection endpoints:** [Falx cerebelli artery left](#structure-artery.amendment.falx_cerebelli_artery.left); [Posterior meningeal VA left](#structure-artery.posterior.posterior_meningeal_va_left)

<a id="structure-artery.connection.apa_tentorial_sca_dural.left"></a>

### APA tentorial–SCA dural left

**Model ID:** `artery.connection.apa_tentorial_sca_dural.left`

**Parent:** [Hypoglossal posterior meningeal artery left](#structure-artery.eca.apa.posterior_meningeal.right.left)

**Connection endpoints:** [Hypoglossal posterior meningeal artery left](#structure-artery.eca.apa.posterior_meningeal.right.left); [Wollschlaeger and Wollschlaeger artery left](#structure-artery.amendment.wollschlaeger_and_wollschlaeger_artery.left)

<a id="structure-artery.connection.lateral_clival_apa_mht.left"></a>

### Lateral clival APA–MHT left

**Model ID:** `artery.connection.lateral_clival_apa_mht.left`

**Description**

The lateral clival artery supplies the dura of the clivus. It has lateral and inferolateral branches which follow, respectively, the superior and inferior petrosal sinuses. There are anastomoses with its contralateral counterpart, the [jugular branch](#structure-artery.eca.apa.jugular.right.left) of the [ascending pharyngeal](#structure-artery.eca.apa.right.left), and the [MMA](#structure-artery.eca.maxillary.mma.right.left).

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Lateral clival artery left](#structure-artery.eca.lateral_clival.right.left)

**Connection endpoints:** [Lateral clival artery left](#structure-artery.eca.lateral_clival.right.left); [Lateral clival MHT branch left](#structure-artery.amendment.lateral_clival_mht_branch.left)

<a id="structure-artery.connection.lateral_clival_recurrent_ilt.left"></a>

### Lateral clival–recurrent ILT left

**Model ID:** `artery.connection.lateral_clival_recurrent_ilt.left`

**Description**

Clival branches of the [jugular artery](#structure-artery.eca.apa.jugular.right.left) anastomose with branches of the [ILT](#structure-artery.anterior.inferolateral_trunk_left) and other clival branches of the [meningohypophyseal artery](#structure-artery.anterior.meningohypophyseal_trunk_left) and can supply the abducens nerve in Dorello’s canal.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Lateral clival artery left](#structure-artery.eca.lateral_clival.right.left)

**Connection endpoints:** [Lateral clival artery left](#structure-artery.eca.lateral_clival.right.left); [ILT recurrent lacerum ramus left](#structure-artery.amendment.ilt_recurrent_lacerum_ramus.left)

<a id="structure-artery.connection.inferior_tympanic_caroticotympanic.left"></a>

### Inferior tympanic–caroticotympanic left

**Model ID:** `artery.connection.inferior_tympanic_caroticotympanic.left`

**Description**

The [inferior tympanic artery](#structure-artery.eca.apa.inferior_tympanic.right.left) branch of the [ascending pharyngeal artery](#structure-artery.eca.apa.right.left) travels with Jacobson’s nerve through the inferior tympanic foramen, anastomosing with other tympanic ([anterior tympanic](#structure-artery.eca.maxillary.anterior_tympanic.right.left), [superior tympanic](#structure-artery.amendment.superior_tympanic.left)) and surrounding arteries within the middle ear including the [caroticotympanic artery](#structure-artery.anterior.caroticotympanic_left), a [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) branch.

**Source:** `nv(2).pdf`, PDF page 52; printed page 58.

**Parent:** [Inferior tympanic artery left](#structure-artery.eca.apa.inferior_tympanic.right.left)

**Connection endpoints:** [Inferior tympanic artery left](#structure-artery.eca.apa.inferior_tympanic.right.left); [Caroticotympanic left](#structure-artery.anterior.caroticotympanic_left)

<a id="structure-artery.connection.apa_musculospinal_va.left"></a>

### APA musculospinal–VA left

**Model ID:** `artery.connection.apa_musculospinal_va.left`

**Description**

The [musculospinal branch](#structure-artery.amendment.apa_musculospinal.left) laterally anastomoses with the C3 radicular anastomotic artery from the [vertebral artery](#structure-artery.posterior.vertebral_left).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [APA musculospinal left](#structure-artery.amendment.apa_musculospinal.left)

**Connection endpoints:** [APA musculospinal left](#structure-artery.amendment.apa_musculospinal.left); [VA muscular C2 left](#structure-artery.posterior.va_muscular_c2_left)

<a id="structure-artery.connection.apa_prevertebral_odontoid.left"></a>

### APA prevertebral–odontoid left

**Model ID:** `artery.connection.apa_prevertebral_odontoid.left`

**Description**

The [prevertebral branch](#structure-artery.amendment.apa_prevertebral_branch.left), running along the ventral surface of the C1-C2 vertebrae and typically emerging from the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left), forms a U-shaped curve and anastomoses medially with C3 [vertebral artery](#structure-artery.posterior.vertebral_left) radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF page 54; printed page 60.

**Parent:** [APA prevertebral branch left](#structure-artery.amendment.apa_prevertebral_branch.left)

**Connection endpoints:** [APA prevertebral branch left](#structure-artery.amendment.apa_prevertebral_branch.left); [Odontoid descending artery left](#structure-artery.eca.apa.descending_odontoid.right.left)

<a id="structure-artery.connection.medial_lateral_posterior_choroidal.left"></a>

### Medial–lateral posterior choroidal left

**Model ID:** `artery.connection.medial_lateral_posterior_choroidal.left`

**Description**

Terminal branches of the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) anastomose with the [lateral posterior choroidal arteries](#structure-artery.posterior.lateral_posterior_choroidal_left) at the foramen of Monro.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal plexal representative left](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.left)

**Connection endpoints:** [Medial posterior choroidal plexal representative left](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.left); [Lateral posterior choroidal plexal representative left](#structure-artery.amendment.lateral_posterior_choroidal_plexal_representative.left)

<a id="structure-artery.connection.posterior_choroidal_splenial.left"></a>

### Posterior choroidal–splenial left

**Model ID:** `artery.connection.posterior_choroidal_splenial.left`

**Description**

Posterior pericallosal (or splenial) branches: these small vessels originate from the P3 segment, parieto-occipital, calcarine, or posterior temporal arteries. They can form a common trunk with the [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) or can anastomose with the latter via a recurrent branch to the fornix. They are directed posteriorly initially and then turn abruptly anterosuperiorly to reach the corpus callosum. They anastomose with the terminal branches of the [pericallosal artery](#structure-artery.anterior.aca_pericallosal_left).

**Source:** `nv(2).pdf`, PDF page 51; printed page 57.

**Parent:** [Medial posterior choroidal plexal representative left](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.left)

**Connection endpoints:** [Medial posterior choroidal plexal representative left](#structure-artery.amendment.medial_posterior_choroidal_plexal_representative.left); [PCA splenial left](#structure-artery.posterior.pca_splenial_left)

<a id="structure-artery.connection.pca_sca_tectal_network.left"></a>

### PCA–SCA tectal network left

**Model ID:** `artery.connection.pca_sca_tectal_network.left`

**Description**

Collicular arteries sometimes arise distinctly from the [P1 segment](#structure-artery.posterior.pca_p1_left) (running medial to P2) or P2 segment. They curve around and send branches to the cerebral peduncle, terminating at the collicular (quadrigeminal) plate. An anastomosis between the PCA and [SCA](#structure-artery.posterior.sca_left) can occur at this location.

**Source:** `nv(2).pdf`, PDF page 48; printed page 54.

**Parent:** [PCA collicular left](#structure-artery.amendment.pca_collicular.left)

**Connection endpoints:** [PCA collicular left](#structure-artery.amendment.pca_collicular.left); [SCA tectal branch left](#structure-artery.amendment.sca_tectal_branch.left)

<a id="structure-artery.connection.aica_sca_pial_border_zone.left"></a>

### AICA–SCA pial border zone left

**Model ID:** `artery.connection.aica_sca_pial_border_zone.left`

**Description**

The [AICA](#structure-artery.posterior.aica_left) has anastomoses with branches of the [PICA](#structure-artery.posterior.pica_left) and [SCA](#structure-artery.posterior.sca_left).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA rostral branch left](#structure-artery.posterior.aica_rostral_branch_left)

**Connection endpoints:** [AICA rostral branch left](#structure-artery.posterior.aica_rostral_branch_left); [SCA caudal hemispheric left](#structure-artery.posterior.sca_caudal_hemispheric_left)

<a id="structure-artery.connection.subarcuate_petrosal_mma.left"></a>

### Subarcuate–petrosal MMA left

**Model ID:** `artery.connection.subarcuate_petrosal_mma.left`

**Description**

The [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right.left) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left)

**Connection endpoints:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left); [MMA petrosal artery left](#structure-artery.eca.maxillary.mma.petrosal.right.left)

<a id="structure-artery.connection.subarcuate_stylomastoid.left"></a>

### Subarcuate–stylomastoid left

**Model ID:** `artery.connection.subarcuate_stylomastoid.left`

**Description**

The [subarcuate branch](#structure-artery.amendment.aica_subarcuate.left) is dural, runs in the petromastoid canal, and anastomoses with the [MMA](#structure-artery.eca.maxillary.mma.right.left) and [stylomastoid](#structure-artery.eca.occipital.stylomastoid.right.left) branches.

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left)

**Connection endpoints:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left); [Stylomastoid artery left](#structure-artery.eca.occipital.stylomastoid.right.left)

<a id="structure-artery.connection.subarcuate_apa_auditory.left"></a>

### Subarcuate–APA auditory left

**Model ID:** `artery.connection.subarcuate_apa_auditory.left`

**Parent:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left)

**Connection endpoints:** [AICA subarcuate left](#structure-artery.amendment.aica_subarcuate.left); [Jugular ascending IAC branch left](#structure-artery.amendment.jugular_ascending_iac_branch.left)

<a id="structure-artery.connection.pica_sca_vermian_border_zone.left"></a>

### PICA–SCA vermian border zone left

**Model ID:** `artery.connection.pica_sca_vermian_border_zone.left`

**Description**

The superior vermian terminal branch of the [SCA](#structure-artery.posterior.sca_left) supplies the vermis and anastomoses with the [AICA](#structure-artery.posterior.aica_left) and [PICA](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 47; printed page 53.

**Parent:** [PICA vermian left](#structure-artery.posterior.pica_vermian_left)

**Connection endpoints:** [PICA vermian left](#structure-artery.posterior.pica_vermian_left); [SCA vermian left](#structure-artery.posterior.sca_vermian_left)

<a id="structure-artery.connection.pica_aica_pial_border_zone.left"></a>

### PICA–AICA pial border zone left

**Model ID:** `artery.connection.pica_aica_pial_border_zone.left`

**Description**

The [AICA](#structure-artery.posterior.aica_left) has anastomoses with branches of the [PICA](#structure-artery.posterior.pica_left) and [SCA](#structure-artery.posterior.sca_left).

**Source:** `nv(2).pdf`, PDF page 46; printed page 52.

**Parent:** [PICA hemispheric left](#structure-artery.posterior.pica_hemispheric_left)

**Connection endpoints:** [PICA hemispheric left](#structure-artery.posterior.pica_hemispheric_left); [AICA caudal branch left](#structure-artery.posterior.aica_caudal_branch_left)

<a id="connections-midline"></a>

## Potential arterial connections, midline

<a id="structure-artery.connection.contralateral_inferior_labial.midline"></a>

### Contralateral inferior labial midline

**Model ID:** `artery.connection.contralateral_inferior_labial.midline`

**Parent:** [Inferior labial artery right](#structure-artery.eca.inferior_labial.right)

**Connection endpoints:** [Inferior labial artery right](#structure-artery.eca.inferior_labial.right); [Inferior labial artery left](#structure-artery.eca.inferior_labial.right.left)

<a id="structure-artery.connection.contralateral_superior_labial.midline"></a>

### Contralateral superior labial midline

**Model ID:** `artery.connection.contralateral_superior_labial.midline`

**Parent:** [Superior labial artery right](#structure-artery.eca.superior_labial.right)

**Connection endpoints:** [Superior labial artery right](#structure-artery.eca.superior_labial.right); [Superior labial artery left](#structure-artery.eca.superior_labial.right.left)

<a id="structure-artery.connection.contralateral_palatal.midline"></a>

### Contralateral palatal midline

**Model ID:** `artery.connection.contralateral_palatal.midline`

**Parent:** [Greater palatine artery right](#structure-artery.eca.greater_palatine.right)

**Connection endpoints:** [Greater palatine artery right](#structure-artery.eca.greater_palatine.right); [Greater palatine artery left](#structure-artery.eca.greater_palatine.right.left)

<a id="structure-artery.connection.contralateral_pharyngeal.midline"></a>

### Contralateral pharyngeal midline

**Model ID:** `artery.connection.contralateral_pharyngeal.midline`

**Description**

Superior, middle, and inferior pharyngeal branches: these branches supply the pharyngeal submucosal spaces and contribute to a rich anastomotic network with the contralateral ascending pharyngeal artery and IMA.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Superior pharyngeal artery right](#structure-artery.eca.superior_pharyngeal.right)

**Connection endpoints:** [Superior pharyngeal artery right](#structure-artery.eca.superior_pharyngeal.right); [Superior pharyngeal artery left](#structure-artery.eca.superior_pharyngeal.right.left)

<a id="structure-artery.connection.contralateral_medial_clival.midline"></a>

### Contralateral medial clival midline

**Model ID:** `artery.connection.contralateral_medial_clival.midline`

**Parent:** [Medial clival artery right](#structure-artery.eca.medial_clival.right)

**Connection endpoints:** [Medial clival artery right](#structure-artery.eca.medial_clival.right); [Medial clival artery left](#structure-artery.eca.medial_clival.right.left)

<a id="structure-artery.connection.odontoid_transverse_arcade.midline"></a>

### Odontoid transverse arcade midline

**Model ID:** `artery.connection.odontoid_transverse_arcade.midline`

**Description**

A descending branch of the hypoglossal artery anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries.

The prevertebral branch, running along the ventral surface of the C1-C2 vertebrae and typically emerging from the neuromeningeal trunk, forms a U-shaped curve and anastomoses medially with C3 vertebral artery radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF pages 14, 54; printed pages 20, 60.

**Parent:** [Odontoid descending artery right](#structure-artery.eca.apa.descending_odontoid.right)

**Connection endpoints:** [Odontoid descending artery right](#structure-artery.eca.apa.descending_odontoid.right); [Odontoid descending artery left](#structure-artery.eca.apa.descending_odontoid.right.left)

<a id="structure-artery.connection.contralateral_lateral_clival.midline"></a>

### Contralateral lateral clival midline

**Model ID:** `artery.connection.contralateral_lateral_clival.midline`

**Description**

The lateral clival artery supplies the dura of the clivus. It has lateral and inferolateral branches which follow, respectively, the superior and inferior petrosal sinuses. There are anastomoses with its contralateral counterpart, the jugular branch of the ascending pharyngeal, and the MMA.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [Lateral clival MHT branch right](#structure-artery.amendment.lateral_clival_mht_branch.right)

**Connection endpoints:** [Lateral clival MHT branch right](#structure-artery.amendment.lateral_clival_mht_branch.right); [Lateral clival MHT branch left](#structure-artery.amendment.lateral_clival_mht_branch.left)

<a id="structure-artery.connection.contralateral_superior_hypophyseal.midline"></a>

### Contralateral superior hypophyseal midline

**Model ID:** `artery.connection.contralateral_superior_hypophyseal.midline`

**Description**

Superior hypophyseal arteries: these small vessels typically arise medially along the paraophthalmic ICA segment and supply the pituitary gland, optic chiasm, and optic nerve and some may supply the hypothalamus. There are anastomoses with their contralateral counterparts and ipsilateral PCOM.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [Superior hypophyseal right](#structure-artery.anterior.superior_hypophyseal_right)

**Connection endpoints:** [Superior hypophyseal right](#structure-artery.anterior.superior_hypophyseal_right); [Superior hypophyseal left](#structure-artery.anterior.superior_hypophyseal_left)

<a id="structure-artery.connection.odontoid_inferior_transverse_arcade.midline"></a>

### Odontoid inferior transverse arcade midline

**Model ID:** `artery.connection.odontoid_inferior_transverse_arcade.midline`

**Description**

A descending branch of the hypoglossal artery anastomoses with its contralateral counterpart and forms the odontoid arch arcade, together with bilateral C3 radicular branches of the vertebral arteries.

The prevertebral branch, running along the ventral surface of the C1-C2 vertebrae and typically emerging from the neuromeningeal trunk, forms a U-shaped curve and anastomoses medially with C3 vertebral artery radicular arteries on the surface of the dens and also its contralateral counterpart (the odontoid arcade).

**Source:** `nv(2).pdf`, PDF pages 14, 54; printed pages 20, 60.

**Parent:** [VA odontoid contribution right](#structure-artery.posterior.va_odontoid_contribution_right)

**Connection endpoints:** [VA odontoid contribution right](#structure-artery.posterior.va_odontoid_contribution_right); [VA odontoid contribution left](#structure-artery.posterior.va_odontoid_contribution_left)

<a id="vascular-landmarks"></a>

## Vascular landmarks

<a id="structure-artery.anterior.anterior_choroidal_right.landmark.plexal_entry_estimate"></a>

### Plexal entry estimate right

**Model ID:** `artery.anterior.anterior_choroidal_right.landmark.plexal_entry_estimate`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_right) enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. The artery often exhibits a sharp curve followed by a posterior turn at the plexal point.

**Source:** `nv(2).pdf`, PDF pages 30–31; printed pages 36–37.

**Parent:** [Anterior choroidal right](#structure-artery.anterior.anterior_choroidal_right)

<a id="structure-artery.anterior.anterior_choroidal_left.landmark.plexal_entry_estimate"></a>

### Plexal entry estimate left

**Model ID:** `artery.anterior.anterior_choroidal_left.landmark.plexal_entry_estimate`

**Description**

The [anterior choroidal artery](#structure-artery.anterior.anterior_choroidal_left) enters the choroidal fissure and terminates in the choroid plexus of the lateral ventricle. The artery often exhibits a sharp curve followed by a posterior turn at the plexal point.

**Source:** `nv(2).pdf`, PDF pages 30–31; printed pages 36–37.

**Parent:** [Anterior choroidal left](#structure-artery.anterior.anterior_choroidal_left)

<a id="structure-artery.posterior.medial_posterior_choroidal_right.landmark.third_ventricular_entry_estimate"></a>

### Third ventricular entry estimate right

**Model ID:** `artery.posterior.medial_posterior_choroidal_right.landmark.third_ventricular_entry_estimate`

**Description**

The [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_right) enters the roof of the third ventricle within the velum interpositum, the small membrane just above and anterior to the pineal gland, to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal right](#structure-artery.posterior.medial_posterior_choroidal_right)

<a id="structure-artery.posterior.lateral_posterior_choroidal_right.landmark.lateral_ventricular_entry_estimate"></a>

### Lateral ventricular entry estimate right

**Model ID:** `artery.posterior.lateral_posterior_choroidal_right.landmark.lateral_ventricular_entry_estimate`

**Description**

The [lateral posterior choroidal artery](#structure-artery.posterior.lateral_posterior_choroidal_right) enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Lateral posterior choroidal right](#structure-artery.posterior.lateral_posterior_choroidal_right)

<a id="structure-artery.posterior.medial_posterior_choroidal_left.landmark.third_ventricular_entry_estimate"></a>

### Third ventricular entry estimate left

**Model ID:** `artery.posterior.medial_posterior_choroidal_left.landmark.third_ventricular_entry_estimate`

**Description**

The [medial posterior choroidal artery](#structure-artery.posterior.medial_posterior_choroidal_left) enters the roof of the third ventricle within the velum interpositum, the small membrane just above and anterior to the pineal gland, to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Medial posterior choroidal left](#structure-artery.posterior.medial_posterior_choroidal_left)

<a id="structure-artery.posterior.lateral_posterior_choroidal_left.landmark.lateral_ventricular_entry_estimate"></a>

### Lateral ventricular entry estimate left

**Model ID:** `artery.posterior.lateral_posterior_choroidal_left.landmark.lateral_ventricular_entry_estimate`

**Description**

The [lateral posterior choroidal artery](#structure-artery.posterior.lateral_posterior_choroidal_left) enters the choroidal fissure and lateral ventricle to supply the choroid plexus.

**Source:** `nv(2).pdf`, PDF page 50; printed page 56.

**Parent:** [Lateral posterior choroidal left](#structure-artery.posterior.lateral_posterior_choroidal_left)

<a id="structure-artery.posterior.pica_right.landmark.telovelotonsillar_loop_estimate"></a>

### Telovelotonsillar loop estimate right

**Model ID:** `artery.posterior.pica_right.landmark.telovelotonsillar_loop_estimate`

**Description**

Conventionally, the apex of the cranial loop serves as the angiographic marker for the telovelotonsillar segment, which typically represents the distal limit for perforators originating from the [PICA](#structure-artery.posterior.pica_right).

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA right](#structure-artery.posterior.pica_right)

<a id="structure-artery.posterior.pica_left.landmark.telovelotonsillar_loop_estimate"></a>

### Telovelotonsillar loop estimate left

**Model ID:** `artery.posterior.pica_left.landmark.telovelotonsillar_loop_estimate`

**Description**

Conventionally, the apex of the cranial loop serves as the angiographic marker for the telovelotonsillar segment, which typically represents the distal limit for perforators originating from the [PICA](#structure-artery.posterior.pica_left).

**Source:** `nv(2).pdf`, PDF page 43; printed page 49.

**Parent:** [PICA left](#structure-artery.posterior.pica_left)

<a id="bone-landmarks"></a>

## Bony foramina, passages and regions

<a id="structure-landmark.optic-canal.right"></a>

### Optic canal right

**Model ID:** `landmark.optic-canal.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.optic-canal.left"></a>

### Optic canal left

**Model ID:** `landmark.optic-canal.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.superior-orbital-fissure.right"></a>

### Superior orbital fissure right

**Model ID:** `landmark.superior-orbital-fissure.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.superior-orbital-fissure.left"></a>

### Superior orbital fissure left

**Model ID:** `landmark.superior-orbital-fissure.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.inferior-orbital-fissure.right"></a>

### Inferior orbital fissure right

**Model ID:** `landmark.inferior-orbital-fissure.right`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) ascends on the posterior wall of the maxillary sinus and traverses the inferior orbital fissure to enter the orbit.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.inferior-orbital-fissure.left"></a>

### Inferior orbital fissure left

**Model ID:** `landmark.inferior-orbital-fissure.left`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) ascends on the posterior wall of the maxillary sinus and traverses the inferior orbital fissure to enter the orbit.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.infraorbital-groove.right"></a>

### Infraorbital groove and canal right

**Model ID:** `landmark.infraorbital-groove.right`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) runs forward on the orbital floor in the infraorbital groove, together with the infraorbital nerve and vein, giving off osseous and muscular branches.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.infraorbital-groove.left"></a>

### Infraorbital groove and canal left

**Model ID:** `landmark.infraorbital-groove.left`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) runs forward on the orbital floor in the infraorbital groove, together with the infraorbital nerve and vein, giving off osseous and muscular branches.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.infraorbital-foramen.right"></a>

### Infraorbital foramen right

**Model ID:** `landmark.infraorbital-foramen.right`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right) exits through the infraorbital foramen with the infraorbital nerve and vein to supply the lateral aspect of the nose, upper lip, and lower eyelid.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.infraorbital-foramen.left"></a>

### Infraorbital foramen left

**Model ID:** `landmark.infraorbital-foramen.left`

**Description**

The [infraorbital artery](#structure-artery.eca.maxillary.infraorbital.right.left) exits through the infraorbital foramen with the infraorbital nerve and vein to supply the lateral aspect of the nose, upper lip, and lower eyelid.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.anterior-ethmoidal.right"></a>

### Anterior ethmoidal canal right

**Model ID:** `landmark.anterior-ethmoidal.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.anterior-ethmoidal.left"></a>

### Anterior ethmoidal canal left

**Model ID:** `landmark.anterior-ethmoidal.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.posterior-ethmoidal.right"></a>

### Posterior ethmoidal canal right

**Model ID:** `landmark.posterior-ethmoidal.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.posterior-ethmoidal.left"></a>

### Posterior ethmoidal canal left

**Model ID:** `landmark.posterior-ethmoidal.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.supraorbital.right"></a>

### Supraorbital notch or foramen right

**Model ID:** `landmark.supraorbital.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.supraorbital.left"></a>

### Supraorbital notch or foramen left

**Model ID:** `landmark.supraorbital.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.supratrochlear.right"></a>

### Frontal notch / supratrochlear exit right

**Model ID:** `landmark.supratrochlear.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.supratrochlear.left"></a>

### Frontal notch / supratrochlear exit left

**Model ID:** `landmark.supratrochlear.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.zygomaticofacial.right"></a>

### Zygomaticofacial foramen right

**Model ID:** `landmark.zygomaticofacial.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.zygomaticofacial.left"></a>

### Zygomaticofacial foramen left

**Model ID:** `landmark.zygomaticofacial.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.zygomaticotemporal.right"></a>

### Zygomaticotemporal foramen right

**Model ID:** `landmark.zygomaticotemporal.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.zygomaticotemporal.left"></a>

### Zygomaticotemporal foramen left

**Model ID:** `landmark.zygomaticotemporal.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.cranio-orbital.right"></a>

### Cranio-orbital / meningolacrimal canal right

**Model ID:** `landmark.cranio-orbital.right`

**Description**

Meningolacrimal artery: partial supply only of the lacrimal gland from the [MMA](#structure-artery.eca.maxillary.mma.right) via the foramen of Hyrtl.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.cranio-orbital.left"></a>

### Cranio-orbital / meningolacrimal canal left

**Model ID:** `landmark.cranio-orbital.left`

**Description**

Meningolacrimal artery: partial supply only of the lacrimal gland from the [MMA](#structure-artery.eca.maxillary.mma.right.left) via the foramen of Hyrtl.

**Source:** `nv(2).pdf`, PDF page 30; printed page 36.

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.accessory-optic.right"></a>

### Accessory optic canal right

**Model ID:** `landmark.accessory-optic.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.accessory-optic.left"></a>

### Accessory optic canal left

**Model ID:** `landmark.accessory-optic.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.nasolacrimal.right"></a>

### Nasolacrimal canal right

**Model ID:** `landmark.nasolacrimal.right`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.nasolacrimal.left"></a>

### Nasolacrimal canal left

**Model ID:** `landmark.nasolacrimal.left`

**Parent:** [Orbit](#structure-landmark.region.orbit)

<a id="structure-landmark.cribriform.right"></a>

### Cribriform foramina right

**Model ID:** `landmark.cribriform.right`

**Parent:** [Anterior base](#structure-landmark.region.anterior-base)

<a id="structure-landmark.cribriform.left"></a>

### Cribriform foramina left

**Model ID:** `landmark.cribriform.left`

**Parent:** [Anterior base](#structure-landmark.region.anterior-base)

<a id="structure-landmark.foramen-caecum.midline"></a>

### Foramen caecum

**Model ID:** `landmark.foramen-caecum.midline`

**Parent:** [Anterior base](#structure-landmark.region.anterior-base)

<a id="structure-landmark.rotundum.right"></a>

### Foramen rotundum right

**Model ID:** `landmark.rotundum.right`

**Description**

The [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right) courses posteriorly accompanied by the maxillary nerve, which it supplies, and enters the cranium through the foramen rotundum to supply dura mater.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.rotundum.left"></a>

### Foramen rotundum left

**Model ID:** `landmark.rotundum.left`

**Description**

The [artery of the foramen rotundum](#structure-artery.eca.maxillary.foramen_rotundum.right.left) courses posteriorly accompanied by the maxillary nerve, which it supplies, and enters the cranium through the foramen rotundum to supply dura mater.

**Source:** `nv(2).pdf`, PDF page 21; printed page 27.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.ovale.right"></a>

### Foramen ovale right

**Model ID:** `landmark.ovale.right`

**Description**

The posterior branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) enters the skull through the foramen ovale or [foramen Vesalius](#structure-landmark.vesalius.right). It supplies the mandibular division of the trigeminal nerve, trigeminal ganglion, and dura mater of Meckel’s cave and the middle cranial fossa.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.ovale.left"></a>

### Foramen ovale left

**Model ID:** `landmark.ovale.left`

**Description**

The posterior branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) enters the skull through the foramen ovale or [foramen Vesalius](#structure-landmark.vesalius.left). It supplies the mandibular division of the trigeminal nerve, trigeminal ganglion, and dura mater of Meckel’s cave and the middle cranial fossa.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.foramen-spinosum.right"></a>

### Foramen spinosum right

**Model ID:** `landmark.foramen-spinosum.right`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right) enters the cranial cavity via the foramen spinosum. It then turns abruptly laterally and runs horizontally, giving off petrosal and cavernous sinus branches.

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.foramen-spinosum.left"></a>

### Foramen spinosum left

**Model ID:** `landmark.foramen-spinosum.left`

**Description**

The [MMA](#structure-artery.eca.maxillary.mma.right.left) enters the cranial cavity via the foramen spinosum. It then turns abruptly laterally and runs horizontally, giving off petrosal and cavernous sinus branches.

**Source:** `nv(2).pdf`, PDF page 18; printed page 24.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.foramen-lacerum.right"></a>

### Foramen lacerum right

**Model ID:** `landmark.foramen-lacerum.right`

**Description**

The [petrosal ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) runs over the cartilage covering the foramen lacerum.

The [vidian artery from the IMA](#structure-artery.eca.maxillary.pterygoid_canal.right) runs through the [vidian canal](#structure-landmark.pterygoid-canal.right) to the foramen lacerum, where it meets the [vidian branch of the petrous ICA](#structure-artery.anterior.vidian_ica_contribution_right).

**Source:** `nv(2).pdf`, PDF pages 26, 53; printed pages 32, 59.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.foramen-lacerum.left"></a>

### Foramen lacerum left

**Model ID:** `landmark.foramen-lacerum.left`

**Description**

The [petrosal ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) runs over the cartilage covering the foramen lacerum.

The [vidian artery from the IMA](#structure-artery.eca.maxillary.pterygoid_canal.right.left) runs through the [vidian canal](#structure-landmark.pterygoid-canal.left) to the foramen lacerum, where it meets the [vidian branch of the petrous ICA](#structure-artery.anterior.vidian_ica_contribution_left).

**Source:** `nv(2).pdf`, PDF pages 26, 53; printed pages 32, 59.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.vesalius.right"></a>

### Sphenoidal emissary foramen (Vesalius) right

**Model ID:** `landmark.vesalius.right`

**Description**

The posterior branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right) enters the skull through the [foramen ovale](#structure-landmark.ovale.right) or foramen Vesalius. It supplies the mandibular division of the trigeminal nerve, trigeminal ganglion, and dura mater of Meckel’s cave and the middle cranial fossa.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.vesalius.left"></a>

### Sphenoidal emissary foramen (Vesalius) left

**Model ID:** `landmark.vesalius.left`

**Description**

The posterior branch of the [accessory meningeal artery](#structure-artery.eca.maxillary.accessory_meningeal.right.left) enters the skull through the [foramen ovale](#structure-landmark.ovale.left) or foramen Vesalius. It supplies the mandibular division of the trigeminal nerve, trigeminal ganglion, and dura mater of Meckel’s cave and the middle cranial fossa.

**Source:** `nv(2).pdf`, PDF page 19; printed page 25.

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.greater-petrosal-hiatus.right"></a>

### Greater petrosal nerve hiatus right

**Model ID:** `landmark.greater-petrosal-hiatus.right`

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.greater-petrosal-hiatus.left"></a>

### Greater petrosal nerve hiatus left

**Model ID:** `landmark.greater-petrosal-hiatus.left`

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.lesser-petrosal-hiatus.right"></a>

### Lesser petrosal nerve hiatus right

**Model ID:** `landmark.lesser-petrosal-hiatus.right`

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.lesser-petrosal-hiatus.left"></a>

### Lesser petrosal nerve hiatus left

**Model ID:** `landmark.lesser-petrosal-hiatus.left`

**Parent:** [Middle base](#structure-landmark.region.middle-base)

<a id="structure-landmark.carotid-canal.right"></a>

### Carotid canal right

**Model ID:** `landmark.carotid-canal.right`

**Description**

The [petrosal ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous) starts vertically in the carotid canal before turning anteromedially and running over the cartilage covering the [foramen lacerum](#structure-landmark.foramen-lacerum.right).

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.carotid-canal.left"></a>

### Carotid canal left

**Model ID:** `landmark.carotid-canal.left`

**Description**

The [petrosal ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous) starts vertically in the carotid canal before turning anteromedially and running over the cartilage covering the [foramen lacerum](#structure-landmark.foramen-lacerum.left).

**Source:** `nv(2).pdf`, PDF page 26; printed page 32.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.caroticotympanic.right"></a>

### Caroticotympanic canaliculi right

**Model ID:** `landmark.caroticotympanic.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.caroticotympanic.left"></a>

### Caroticotympanic canaliculi left

**Model ID:** `landmark.caroticotympanic.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.internal-acoustic.right"></a>

### Internal acoustic meatus right

**Model ID:** `landmark.internal-acoustic.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.internal-acoustic.left"></a>

### Internal acoustic meatus left

**Model ID:** `landmark.internal-acoustic.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.facial-canal.right"></a>

### Facial canal right

**Model ID:** `landmark.facial-canal.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.facial-canal.left"></a>

### Facial canal left

**Model ID:** `landmark.facial-canal.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.stylomastoid.right"></a>

### Stylomastoid foramen right

**Model ID:** `landmark.stylomastoid.right`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right) enters the stylomastoid foramen with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.stylomastoid.left"></a>

### Stylomastoid foramen left

**Model ID:** `landmark.stylomastoid.left`

**Description**

The [stylomastoid artery](#structure-artery.eca.occipital.stylomastoid.right.left) enters the stylomastoid foramen with the facial nerve, which it supplies, contributing to the facial arcade in the temporal bone with the [petrosal branch of the MMA](#structure-artery.eca.maxillary.mma.petrosal.right.left).

**Source:** `nv(2).pdf`, PDF page 11; printed page 17.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.external-acoustic.right"></a>

### External acoustic meatus right

**Model ID:** `landmark.external-acoustic.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.external-acoustic.left"></a>

### External acoustic meatus left

**Model ID:** `landmark.external-acoustic.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.petrotympanic.right"></a>

### Petrotympanic fissure right

**Model ID:** `landmark.petrotympanic.right`

**Description**

The posterior branch of the [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right) enters the tympanic cavity through the petrotympanic fissure to supply the mucosa of the tympanic cavity and the tympanic membrane.

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.petrotympanic.left"></a>

### Petrotympanic fissure left

**Model ID:** `landmark.petrotympanic.left`

**Description**

The posterior branch of the [anterior tympanic artery](#structure-artery.eca.maxillary.anterior_tympanic.right.left) enters the tympanic cavity through the petrotympanic fissure to supply the mucosa of the tympanic cavity and the tympanic membrane.

**Source:** `nv(2).pdf`, PDF page 15; printed page 21.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.tympanic-canaliculus.right"></a>

### Tympanic canaliculus right

**Model ID:** `landmark.tympanic-canaliculus.right`

**Description**

The [inferior tympanic artery](#structure-artery.eca.apa.inferior_tympanic.right) is directed superiorly through the canal of Jacobson ([inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right) canaliculus) to enter the tympanic cavity.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.tympanic-canaliculus.left"></a>

### Tympanic canaliculus left

**Model ID:** `landmark.tympanic-canaliculus.left`

**Description**

The [inferior tympanic artery](#structure-artery.eca.apa.inferior_tympanic.right.left) is directed superiorly through the canal of Jacobson ([inferior tympanic](#structure-artery.eca.apa.inferior_tympanic.right.left) canaliculus) to enter the tympanic cavity.

**Source:** `nv(2).pdf`, PDF page 13; printed page 19.

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.mastoid-canaliculus.right"></a>

### Mastoid canaliculus right

**Model ID:** `landmark.mastoid-canaliculus.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.mastoid-canaliculus.left"></a>

### Mastoid canaliculus left

**Model ID:** `landmark.mastoid-canaliculus.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.cochlear-aqueduct.right"></a>

### Cochlear aqueduct opening right

**Model ID:** `landmark.cochlear-aqueduct.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.cochlear-aqueduct.left"></a>

### Cochlear aqueduct opening left

**Model ID:** `landmark.cochlear-aqueduct.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.vestibular-aqueduct.right"></a>

### Vestibular aqueduct opening right

**Model ID:** `landmark.vestibular-aqueduct.right`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.vestibular-aqueduct.left"></a>

### Vestibular aqueduct opening left

**Model ID:** `landmark.vestibular-aqueduct.left`

**Parent:** [Temporal bone](#structure-landmark.region.temporal-bone)

<a id="structure-landmark.jugular-foramen.right"></a>

### Jugular foramen and fossa right

**Model ID:** `landmark.jugular-foramen.right`

**Description**

The [jugular branch](#structure-artery.eca.apa.jugular.right) of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right) enters the cranium through the jugular foramen. It supplies the glossopharyngeal, vagus, and accessory nerves in addition to meninges.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.jugular-foramen.left"></a>

### Jugular foramen and fossa left

**Model ID:** `landmark.jugular-foramen.left`

**Description**

The [jugular branch](#structure-artery.eca.apa.jugular.right.left) of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left) enters the cranium through the jugular foramen. It supplies the glossopharyngeal, vagus, and accessory nerves in addition to meninges.

**Source:** `nv(2).pdf`, PDF pages 13–14; printed pages 19–20.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.hypoglossal.right"></a>

### Hypoglossal canal right

**Model ID:** `landmark.hypoglossal.right`

**Description**

The [hypoglossal branch](#structure-artery.eca.apa.hypoglossal.right) of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right) enters the cranium through the hypoglossal canal to supply the hypoglossal nerve and meninges.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.hypoglossal.left"></a>

### Hypoglossal canal left

**Model ID:** `landmark.hypoglossal.left`

**Description**

The [hypoglossal branch](#structure-artery.eca.apa.hypoglossal.right.left) of the [neuromeningeal trunk](#structure-artery.eca.apa.neuromeningeal_trunk.right.left) enters the cranium through the hypoglossal canal to supply the hypoglossal nerve and meninges.

**Source:** `nv(2).pdf`, PDF page 14; printed page 20.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.condylar.right"></a>

### Condylar canal right

**Model ID:** `landmark.condylar.right`

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.condylar.left"></a>

### Condylar canal left

**Model ID:** `landmark.condylar.left`

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.mastoid-foramen.right"></a>

### Mastoid foramen right

**Model ID:** `landmark.mastoid-foramen.right`

**Description**

A large mastoid branch of the [occipital artery](#structure-artery.eca.occipital.right) often enters the cranium through the mastoid foramen to supply the posterior fossa dura mater as the posterior meningeal artery.

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.mastoid-foramen.left"></a>

### Mastoid foramen left

**Model ID:** `landmark.mastoid-foramen.left`

**Description**

A large mastoid branch of the [occipital artery](#structure-artery.eca.occipital.right.left) often enters the cranium through the mastoid foramen to supply the posterior fossa dura mater as the posterior meningeal artery.

**Source:** `nv(2).pdf`, PDF pages 11–12; printed pages 17–18.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.foramen-magnum.midline"></a>

### Foramen magnum

**Model ID:** `landmark.foramen-magnum.midline`

**Description**

The V4 segment of the vertebral artery pierces the atlanto-occipital membrane to become intradural, entering the cranial cavity via the foramen magnum.

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Posterior base](#structure-landmark.region.posterior-base)

<a id="structure-landmark.pterygomaxillary.right"></a>

### Pterygomaxillary fissure right

**Model ID:** `landmark.pterygomaxillary.right`

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.pterygomaxillary.left"></a>

### Pterygomaxillary fissure left

**Model ID:** `landmark.pterygomaxillary.left`

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.sphenopalatine-foramen.right"></a>

### Sphenopalatine foramen right

**Model ID:** `landmark.sphenopalatine-foramen.right`

**Description**

The [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right) passes medially through the sphenopalatine foramen to enter the nasal cavity, which it supplies in addition to the paranasal sinuses.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.sphenopalatine-foramen.left"></a>

### Sphenopalatine foramen left

**Model ID:** `landmark.sphenopalatine-foramen.left`

**Description**

The [sphenopalatine artery](#structure-artery.eca.maxillary.sphenopalatine.right.left) passes medially through the sphenopalatine foramen to enter the nasal cavity, which it supplies in addition to the paranasal sinuses.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.pterygoid-canal.right"></a>

### Pterygoid (Vidian) canal right

**Model ID:** `landmark.pterygoid-canal.right`

**Description**

The vidian artery, running horizontally, arises from the distal [IMA](#structure-artery.eca.maxillary.right) and runs through the vidian canal to the [foramen lacerum](#structure-landmark.foramen-lacerum.right), where it meets the [vidian branch of the mandibulovidian artery](#structure-artery.anterior.vidian_ica_contribution_right) from the [petrous ICA](#structure-artery.anterior.internal_carotid_right.segment.petrous).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.pterygoid-canal.left"></a>

### Pterygoid (Vidian) canal left

**Model ID:** `landmark.pterygoid-canal.left`

**Description**

The vidian artery, running horizontally, arises from the distal [IMA](#structure-artery.eca.maxillary.right.left) and runs through the vidian canal to the [foramen lacerum](#structure-landmark.foramen-lacerum.left), where it meets the [vidian branch of the mandibulovidian artery](#structure-artery.anterior.vidian_ica_contribution_left) from the [petrous ICA](#structure-artery.anterior.internal_carotid_left.segment.petrous).

**Source:** `nv(2).pdf`, PDF page 53; printed page 59.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.palatovaginal.right"></a>

### Palatovaginal / pharyngeal canal right

**Model ID:** `landmark.palatovaginal.right`

**Description**

The pharyngeal ([pterygovaginal](#structure-artery.eca.pterygovaginal.right)) artery courses posteromedially and inferiorly through the pharyngeal canal to supply the roof of the pharynx and pharyngeal end of the Eustachian tube.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.palatovaginal.left"></a>

### Palatovaginal / pharyngeal canal left

**Model ID:** `landmark.palatovaginal.left`

**Description**

The pharyngeal ([pterygovaginal](#structure-artery.eca.pterygovaginal.right.left)) artery courses posteromedially and inferiorly through the pharyngeal canal to supply the roof of the pharynx and pharyngeal end of the Eustachian tube.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.vomerovaginal.right"></a>

### Vomerovaginal canal right

**Model ID:** `landmark.vomerovaginal.right`

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.vomerovaginal.left"></a>

### Vomerovaginal canal left

**Model ID:** `landmark.vomerovaginal.left`

**Parent:** [Pterygopalatine region](#structure-landmark.region.pterygopalatine-region)

<a id="structure-landmark.greater-palatine-canal.right"></a>

### Greater palatine canal right

**Model ID:** `landmark.greater-palatine-canal.right`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) enters the greater palatine canal accompanied by the great palatine nerve. Within the canal it gives off the [lesser palatine artery](#structure-artery.eca.lesser_palatine.right), which supplies the soft palate.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.greater-palatine-canal.left"></a>

### Greater palatine canal left

**Model ID:** `landmark.greater-palatine-canal.left`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) enters the greater palatine canal accompanied by the great palatine nerve. Within the canal it gives off the [lesser palatine artery](#structure-artery.eca.lesser_palatine.right.left), which supplies the soft palate.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.greater-palatine-foramen.right"></a>

### Greater palatine foramen right

**Model ID:** `landmark.greater-palatine-foramen.right`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right) becomes the [greater palatine artery](#structure-artery.eca.greater_palatine.right) as it exits the canal through the greater palatine foramen. It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.greater-palatine-foramen.left"></a>

### Greater palatine foramen left

**Model ID:** `landmark.greater-palatine-foramen.left`

**Description**

The [descending palatine artery](#structure-artery.eca.maxillary.descending_palatine.right.left) becomes the [greater palatine artery](#structure-artery.eca.greater_palatine.right.left) as it exits the canal through the greater palatine foramen. It courses anteriorly beneath the hard palate to supply the hard palate, gingiva, and nasal septum.

**Source:** `nv(2).pdf`, PDF page 22; printed page 28.

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.lesser-palatine.right"></a>

### Lesser palatine foramina right

**Model ID:** `landmark.lesser-palatine.right`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.lesser-palatine.left"></a>

### Lesser palatine foramina left

**Model ID:** `landmark.lesser-palatine.left`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.incisive-canal.midline"></a>

### Incisive canal and foramina

**Model ID:** `landmark.incisive-canal.midline`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.superior-alveolar.right"></a>

### Posterior superior alveolar foramina right

**Model ID:** `landmark.superior-alveolar.right`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.superior-alveolar.left"></a>

### Posterior superior alveolar foramina left

**Model ID:** `landmark.superior-alveolar.left`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.canalis-sinuosus.right"></a>

### Canalis sinuosus right

**Model ID:** `landmark.canalis-sinuosus.right`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.canalis-sinuosus.left"></a>

### Canalis sinuosus left

**Model ID:** `landmark.canalis-sinuosus.left`

**Parent:** [Palate and maxilla](#structure-landmark.region.palate-and-maxilla)

<a id="structure-landmark.mandibular-foramen.right"></a>

### Mandibular foramen right

**Model ID:** `landmark.mandibular-foramen.right`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mandibular-foramen.left"></a>

### Mandibular foramen left

**Model ID:** `landmark.mandibular-foramen.left`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mandibular-canal.right"></a>

### Mandibular canal right

**Model ID:** `landmark.mandibular-canal.right`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right) enters the mandibular canal through an opening on the medial surface of the mandibular ramus and then courses anteroinferiorly and medially towards the [mental foramen](#structure-landmark.mental-foramen.right) on the anterior surface of the mandible.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mandibular-canal.left"></a>

### Mandibular canal left

**Model ID:** `landmark.mandibular-canal.left`

**Description**

The [inferior alveolar artery](#structure-artery.eca.maxillary.inferior_alveolar.right.left) enters the mandibular canal through an opening on the medial surface of the mandibular ramus and then courses anteroinferiorly and medially towards the [mental foramen](#structure-landmark.mental-foramen.left) on the anterior surface of the mandible.

**Source:** `nv(2).pdf`, PDF page 20; printed page 26.

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mental-foramen.right"></a>

### Mental foramen right

**Model ID:** `landmark.mental-foramen.right`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mental-foramen.left"></a>

### Mental foramen left

**Model ID:** `landmark.mental-foramen.left`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mandibular-incisive.right"></a>

### Mandibular incisive canal right

**Model ID:** `landmark.mandibular-incisive.right`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.mandibular-incisive.left"></a>

### Mandibular incisive canal left

**Model ID:** `landmark.mandibular-incisive.left`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.lingual-foramina.midline"></a>

### Lingual and accessory mandibular foramina

**Model ID:** `landmark.lingual-foramina.midline`

**Parent:** [Mandible](#structure-landmark.region.mandible)

<a id="structure-landmark.parietal-emissary.right"></a>

### Parietal emissary foramen right

**Model ID:** `landmark.parietal-emissary.right`

**Parent:** [Vault](#structure-landmark.region.vault)

<a id="structure-landmark.parietal-emissary.left"></a>

### Parietal emissary foramen left

**Model ID:** `landmark.parietal-emissary.left`

**Parent:** [Vault](#structure-landmark.region.vault)

<a id="structure-landmark.occipital-emissary.right"></a>

### Occipital emissary foramina right

**Model ID:** `landmark.occipital-emissary.right`

**Parent:** [Vault](#structure-landmark.region.vault)

<a id="structure-landmark.occipital-emissary.left"></a>

### Occipital emissary foramina left

**Model ID:** `landmark.occipital-emissary.left`

**Parent:** [Vault](#structure-landmark.region.vault)

<a id="structure-landmark.diploic.midline"></a>

### Diploic channels and openings

**Model ID:** `landmark.diploic.midline`

**Parent:** [Vault](#structure-landmark.region.vault)

<a id="structure-landmark.piriform.midline"></a>

### Piriform aperture

**Model ID:** `landmark.piriform.midline`

**Parent:** [Nasal boundaries](#structure-landmark.region.nasal-boundaries)

<a id="structure-landmark.choana.right"></a>

### Choana right

**Model ID:** `landmark.choana.right`

**Parent:** [Nasal boundaries](#structure-landmark.region.nasal-boundaries)

<a id="structure-landmark.choana.left"></a>

### Choana left

**Model ID:** `landmark.choana.left`

**Parent:** [Nasal boundaries](#structure-landmark.region.nasal-boundaries)

<a id="structure-landmark.sinus-ostia.midline"></a>

### Paranasal sinus ostia

**Model ID:** `landmark.sinus-ostia.midline`

**Parent:** [Nasal boundaries](#structure-landmark.region.nasal-boundaries)

<a id="structure-landmark.transverse-foramina.right"></a>

### Cervical transverse foramina right

**Model ID:** `landmark.transverse-foramina.right`

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.transverse-foramina.left"></a>

### Cervical transverse foramina left

**Model ID:** `landmark.transverse-foramina.left`

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.atlas-groove.right"></a>

### Atlas vertebral artery groove right

**Model ID:** `landmark.atlas-groove.right`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_right) imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the [arcuate foramen](#structure-landmark.arcuate-foramen.right) (a possible risk factor for paediatric ischaemic stroke).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.atlas-groove.left"></a>

### Atlas vertebral artery groove left

**Model ID:** `landmark.atlas-groove.left`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_left) imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the [arcuate foramen](#structure-landmark.arcuate-foramen.left) (a possible risk factor for paediatric ischaemic stroke).

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.arcuate-foramen.right"></a>

### Arcuate foramen (when present) right

**Model ID:** `landmark.arcuate-foramen.right`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_right) imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the arcuate foramen.

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.arcuate-foramen.left"></a>

### Arcuate foramen (when present) left

**Model ID:** `landmark.arcuate-foramen.left`

**Description**

The [vertebral artery](#structure-artery.posterior.vertebral_left) imprints a groove on the posterior arch of the atlas, which may rarely form a bony ring called the arcuate foramen.

**Source:** `nv(2).pdf`, PDF page 41; printed page 47.

**Parent:** [Upper cervical](#structure-landmark.region.upper-cervical)

<a id="structure-landmark.ica.carotid-entry.right"></a>

### External carotid canal opening right

**Model ID:** `landmark.ica.carotid-entry.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-ascending.right"></a>

### Ascending petrous carotid canal right

**Model ID:** `landmark.ica.carotid-ascending.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-genu.right"></a>

### Petrous carotid genu right

**Model ID:** `landmark.ica.carotid-genu.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-horizontal.right"></a>

### Horizontal petrous carotid canal right

**Model ID:** `landmark.ica.carotid-horizontal.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-exit.right"></a>

### Internal carotid canal opening right

**Model ID:** `landmark.ica.carotid-exit.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.petrous-apex.right"></a>

### Petrous apex right

**Model ID:** `landmark.ica.petrous-apex.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.jugular-fossa.right"></a>

### Jugular fossa right

**Model ID:** `landmark.ica.jugular-fossa.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.styloid-base.right"></a>

### Styloid process base right

**Model ID:** `landmark.ica.styloid-base.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.lingula.right"></a>

### Sphenoid lingula region right

**Model ID:** `landmark.ica.lingula.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.petrolingual.right"></a>

### Petrolingual boundary (estimated) right

**Model ID:** `landmark.ica.petrolingual.right`

**Description**

From the [carotid canal](#structure-landmark.carotid-canal.right) to the petrolingual ligament (approximately the anterior aspect of the petrous ridge).

From the petrolingual ligament to the proximal dural ring.

**Source:** `nv(2).pdf`, PDF pages 26–27; printed pages 32–33.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-sulcus.right"></a>

### Carotid sulcus of sphenoid right

**Model ID:** `landmark.ica.carotid-sulcus.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.posterior-clinoid.right"></a>

### Posterior clinoid process right

**Model ID:** `landmark.ica.posterior-clinoid.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.anterior-clinoid.right"></a>

### Anterior clinoid process right

**Model ID:** `landmark.ica.anterior-clinoid.right`

**Description**

The anterior clinoid process is superolateral to the genu of the [ICA](#structure-artery.anterior.internal_carotid_right). Dural coverage extends medially to the tuberculum sellae from the anterior clinoid process. The dural ring is denser and more tightly adherent superolaterally and slopes inferomedially across the [ICA](#structure-artery.anterior.internal_carotid_right) so the medial and posterior aspects of the [ICA](#structure-artery.anterior.internal_carotid_right) genu can lie in the subarachnoid space.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.optic-strut.right"></a>

### Optic strut region right

**Model ID:** `landmark.ica.optic-strut.right`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.dural-rings.right"></a>

### Proximal and distal dural ring region right

**Model ID:** `landmark.ica.dural-rings.right`

**Description**

This segment incorporates the proximal and distal dural rings (the clinoid [ICA](#structure-artery.anterior.internal_carotid_right) segment); however, the dural anatomy in the anterior clinoid region is complex, variable, and impossible to reliably define on imaging, making it difficult to differentiate intradural and extradural aneurysms in this region.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-entry.left"></a>

### External carotid canal opening left

**Model ID:** `landmark.ica.carotid-entry.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-ascending.left"></a>

### Ascending petrous carotid canal left

**Model ID:** `landmark.ica.carotid-ascending.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-genu.left"></a>

### Petrous carotid genu left

**Model ID:** `landmark.ica.carotid-genu.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-horizontal.left"></a>

### Horizontal petrous carotid canal left

**Model ID:** `landmark.ica.carotid-horizontal.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-exit.left"></a>

### Internal carotid canal opening left

**Model ID:** `landmark.ica.carotid-exit.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.petrous-apex.left"></a>

### Petrous apex left

**Model ID:** `landmark.ica.petrous-apex.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.jugular-fossa.left"></a>

### Jugular fossa left

**Model ID:** `landmark.ica.jugular-fossa.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.styloid-base.left"></a>

### Styloid process base left

**Model ID:** `landmark.ica.styloid-base.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.lingula.left"></a>

### Sphenoid lingula region left

**Model ID:** `landmark.ica.lingula.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.petrolingual.left"></a>

### Petrolingual boundary (estimated) left

**Model ID:** `landmark.ica.petrolingual.left`

**Description**

From the [carotid canal](#structure-landmark.carotid-canal.left) to the petrolingual ligament (approximately the anterior aspect of the petrous ridge).

From the petrolingual ligament to the proximal dural ring.

**Source:** `nv(2).pdf`, PDF pages 26–27; printed pages 32–33.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.carotid-sulcus.left"></a>

### Carotid sulcus of sphenoid left

**Model ID:** `landmark.ica.carotid-sulcus.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.posterior-clinoid.left"></a>

### Posterior clinoid process left

**Model ID:** `landmark.ica.posterior-clinoid.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.anterior-clinoid.left"></a>

### Anterior clinoid process left

**Model ID:** `landmark.ica.anterior-clinoid.left`

**Description**

The anterior clinoid process is superolateral to the genu of the [ICA](#structure-artery.anterior.internal_carotid_left). Dural coverage extends medially to the tuberculum sellae from the anterior clinoid process. The dural ring is denser and more tightly adherent superolaterally and slopes inferomedially across the [ICA](#structure-artery.anterior.internal_carotid_left) so the medial and posterior aspects of the [ICA](#structure-artery.anterior.internal_carotid_left) genu can lie in the subarachnoid space.

**Source:** `nv(2).pdf`, PDF page 27; printed page 33.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.optic-strut.left"></a>

### Optic strut region left

**Model ID:** `landmark.ica.optic-strut.left`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.dural-rings.left"></a>

### Proximal and distal dural ring region left

**Model ID:** `landmark.ica.dural-rings.left`

**Description**

This segment incorporates the proximal and distal dural rings (the clinoid [ICA](#structure-artery.anterior.internal_carotid_left) segment); however, the dural anatomy in the anterior clinoid region is complex, variable, and impossible to reliably define on imaging, making it difficult to differentiate intradural and extradural aneurysms in this region.

**Source:** `nv(2).pdf`, PDF page 29; printed page 35.

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.sella.midline"></a>

### Sellar floor

**Model ID:** `landmark.ica.sella.midline`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.dorsum-sellae.midline"></a>

### Dorsum sellae

**Model ID:** `landmark.ica.dorsum-sellae.midline`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="structure-landmark.ica.clivus.midline"></a>

### Upper clivus

**Model ID:** `landmark.ica.clivus.midline`

**Parent:** [ICA skull-base landmarks](#structure-landmark.ica.group)

<a id="bones"></a>

## Bones and teeth

<a id="structure-bone.frontal"></a>

### Frontal bone

**Model ID:** `bone.frontal`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.occipital"></a>

### Occipital bone

**Model ID:** `bone.occipital`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.sphenoid"></a>

### Sphenoid bone

**Model ID:** `bone.sphenoid`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.ethmoid"></a>

### Ethmoid bone

**Model ID:** `bone.ethmoid`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.vomer"></a>

### Vomer

**Model ID:** `bone.vomer`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.parietal.right"></a>

### Parietal bone, right

**Model ID:** `bone.parietal.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.parietal.left"></a>

### Parietal bone, left

**Model ID:** `bone.parietal.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.temporal.right"></a>

### Temporal bone, right

**Model ID:** `bone.temporal.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.temporal.left"></a>

### Temporal bone, left

**Model ID:** `bone.temporal.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.zygomatic.right"></a>

### Zygomatic bone, right

**Model ID:** `bone.zygomatic.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.zygomatic.left"></a>

### Zygomatic bone, left

**Model ID:** `bone.zygomatic.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.palatine.right"></a>

### Palatine bone, right

**Model ID:** `bone.palatine.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.palatine.left"></a>

### Palatine bone, left

**Model ID:** `bone.palatine.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.nasal.right"></a>

### Nasal bone, right

**Model ID:** `bone.nasal.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.nasal.left"></a>

### Nasal bone, left

**Model ID:** `bone.nasal.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.lacrimal.right"></a>

### Lacrimal bone, right

**Model ID:** `bone.lacrimal.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.lacrimal.left"></a>

### Lacrimal bone, left

**Model ID:** `bone.lacrimal.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.inferior_nasal_concha.right"></a>

### Inferior nasal concha, right

**Model ID:** `bone.inferior_nasal_concha.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.inferior_nasal_concha.left"></a>

### Inferior nasal concha, left

**Model ID:** `bone.inferior_nasal_concha.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.maxilla.right"></a>

### Maxilla, right

**Model ID:** `bone.maxilla.right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.maxilla.left"></a>

### Maxilla, left

**Model ID:** `bone.maxilla.left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.maxillary-alveolar-process-left"></a>

### Maxillary alveolar process left

**Model ID:** `bone.maxillary-alveolar-process-left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.maxillary-alveolar-process-right"></a>

### Maxillary alveolar process right

**Model ID:** `bone.maxillary-alveolar-process-right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.mandibular-condyle-left"></a>

### Mandibular condyle left

**Model ID:** `bone.mandibular-condyle-left`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.mandibular-condyle-right"></a>

### Mandibular condyle right

**Model ID:** `bone.mandibular-condyle-right`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.mandibular-alveolar-process"></a>

### Mandibular alveolar process

**Model ID:** `bone.mandibular-alveolar-process`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-48"></a>

### Tooth 48 (FDI)

**Model ID:** `bone.tooth-48`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-47"></a>

### Tooth 47 (FDI)

**Model ID:** `bone.tooth-47`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-46"></a>

### Tooth 46 (FDI)

**Model ID:** `bone.tooth-46`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-45"></a>

### Tooth 45 (FDI)

**Model ID:** `bone.tooth-45`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-44"></a>

### Tooth 44 (FDI)

**Model ID:** `bone.tooth-44`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-43"></a>

### Tooth 43 (FDI)

**Model ID:** `bone.tooth-43`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-42"></a>

### Tooth 42 (FDI)

**Model ID:** `bone.tooth-42`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-41"></a>

### Tooth 41 (FDI)

**Model ID:** `bone.tooth-41`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-38"></a>

### Tooth 38 (FDI)

**Model ID:** `bone.tooth-38`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-37"></a>

### Tooth 37 (FDI)

**Model ID:** `bone.tooth-37`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-36"></a>

### Tooth 36 (FDI)

**Model ID:** `bone.tooth-36`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-35"></a>

### Tooth 35 (FDI)

**Model ID:** `bone.tooth-35`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-34"></a>

### Tooth 34 (FDI)

**Model ID:** `bone.tooth-34`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-33"></a>

### Tooth 33 (FDI)

**Model ID:** `bone.tooth-33`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-32"></a>

### Tooth 32 (FDI)

**Model ID:** `bone.tooth-32`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-31"></a>

### Tooth 31 (FDI)

**Model ID:** `bone.tooth-31`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-28"></a>

### Tooth 28 (FDI)

**Model ID:** `bone.tooth-28`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-27"></a>

### Tooth 27 (FDI)

**Model ID:** `bone.tooth-27`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-26"></a>

### Tooth 26 (FDI)

**Model ID:** `bone.tooth-26`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-25"></a>

### Tooth 25 (FDI)

**Model ID:** `bone.tooth-25`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-24"></a>

### Tooth 24 (FDI)

**Model ID:** `bone.tooth-24`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-23"></a>

### Tooth 23 (FDI)

**Model ID:** `bone.tooth-23`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-22"></a>

### Tooth 22 (FDI)

**Model ID:** `bone.tooth-22`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-21"></a>

### Tooth 21 (FDI)

**Model ID:** `bone.tooth-21`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-18"></a>

### Tooth 18 (FDI)

**Model ID:** `bone.tooth-18`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-17"></a>

### Tooth 17 (FDI)

**Model ID:** `bone.tooth-17`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-16"></a>

### Tooth 16 (FDI)

**Model ID:** `bone.tooth-16`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-15"></a>

### Tooth 15 (FDI)

**Model ID:** `bone.tooth-15`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-14"></a>

### Tooth 14 (FDI)

**Model ID:** `bone.tooth-14`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-13"></a>

### Tooth 13 (FDI)

**Model ID:** `bone.tooth-13`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-12"></a>

### Tooth 12 (FDI)

**Model ID:** `bone.tooth-12`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.tooth-11"></a>

### Tooth 11 (FDI)

**Model ID:** `bone.tooth-11`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-bone.hyoid"></a>

### Hyoid bone

**Model ID:** `bone.hyoid`

**Parent:** [Bone](#structure-bone)

<a id="structure-bone.mandible"></a>

### Mandible

**Model ID:** `bone.mandible`

**Parent:** [Bone](#structure-bone)

<a id="groups"></a>

## Catalogue groups

<a id="structure-bone"></a>

### Bone

**Model ID:** `bone`

<a id="structure-bone.skull"></a>

### Skull

**Model ID:** `bone.skull`

**Parent:** [Bone](#structure-bone)

<a id="structure-landmark.passages"></a>

### Foramina and passages

**Model ID:** `landmark.passages`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-landmark.region.orbit"></a>

### Orbit

**Model ID:** `landmark.region.orbit`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.anterior-base"></a>

### Anterior base

**Model ID:** `landmark.region.anterior-base`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.middle-base"></a>

### Middle base

**Model ID:** `landmark.region.middle-base`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.temporal-bone"></a>

### Temporal bone

**Model ID:** `landmark.region.temporal-bone`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.posterior-base"></a>

### Posterior base

**Model ID:** `landmark.region.posterior-base`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.pterygopalatine-region"></a>

### Pterygopalatine region

**Model ID:** `landmark.region.pterygopalatine-region`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.palate-and-maxilla"></a>

### Palate and maxilla

**Model ID:** `landmark.region.palate-and-maxilla`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.mandible"></a>

### Mandible

**Model ID:** `landmark.region.mandible`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.vault"></a>

### Vault

**Model ID:** `landmark.region.vault`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.nasal-boundaries"></a>

### Nasal boundaries

**Model ID:** `landmark.region.nasal-boundaries`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.region.upper-cervical"></a>

### Upper cervical

**Model ID:** `landmark.region.upper-cervical`

**Parent:** [Foramina and passages](#structure-landmark.passages)

<a id="structure-landmark.ica.group"></a>

### ICA skull-base landmarks

**Model ID:** `landmark.ica.group`

**Parent:** [Skull](#structure-bone.skull)

<a id="structure-artery"></a>

### Arteries

**Model ID:** `artery`

<a id="notes-authority-amendments"></a>

## Model amendments required by the notes

Decision recorded on 3 October 2026: the supplied notes govern the next model update. The following actions apply bilaterally where the structures are paired. This is an implementation record. Descriptions, temporal branch names, foramen rotundum names and dental aliases have been incorporated in v0.8.2. The catalogue above reflects those display-name changes. The remaining origin and course amendments below are recorded for a separate model update.

| Structure or relationship | Difference identified | Action for the next batch |
| --- | --- | --- |
| STA temporal branch | Notes: posterior deep temporal artery. Model: Middle temporal artery. | Completed in v0.8.2: STA-origin branches use the notes’ name, with stable IDs and former names retained as search aliases. |
| Maxillary temporal branch | Notes: middle deep temporal artery. Model: Posterior deep temporal artery. | Completed in v0.8.2: maxillary-origin branches use the notes’ name, with stable IDs and former names retained as search aliases. They remain distinct from the STA-origin vessels. |
| Dental / alveolar arteries | The notes use inferior dental (or alveolar) and posterior superior dental; the model uses inferior alveolar and posterior superior alveolar. | Completed in v0.8.2: the notes’ dental terms are searchable aliases for the equivalent alveolar names. These equivalent terms alone do not require a change of origin or course. |
| Medial palpebral branches and arcades | The notes describe medial palpebral supply arising from the angular artery and meeting lateral palpebral supply from the lacrimal artery. The model currently parents its medial palpebral branches to the ophthalmic artery. | Represent the angular-origin medial palpebral supply and its connection to the lateral palpebral / lacrimal supply as described. Update the relevant branch parents, connections and courses together; do not resolve this by changing description text alone. |
| AICA subdivisions | Notes: medial and lateral branches. Model: rostral and caudal branches. | Match the existing paths to the medial branch supplying the biventral lobule and lateral branch running in the hemispheric fissure and supplying the semilunar lobules. Update names, relationships and paths where necessary. Do not assume a correspondence solely from the present names. |
| Ciliary arteries | The notes contain a broad ciliary paragraph as well as explicitly posterior-ciliary wording. The model has medial and lateral posterior ciliary representatives. | Keep these representatives tied to the explicit posterior-ciliary description in the notes. Do not apply the entire broad ciliary description to them without identifying which described branches it concerns. |
| Paracentral origin | The notes describe a callosomarginal branch and explicitly allow branches to arise directly from the pericallosal artery. The model uses the direct pericallosal origin. | Retain the configuration permitted by the notes and make that selected variant clear in the eventual description. |
| ICA branches and boundaries | Current branch parents agree with the notes: MHT / ILT cavernous; ophthalmic / superior hypophyseal paraophthalmic; PCom communicating; AChA choroidal. The paraophthalmic boundary begins just before the ophthalmic ostium. | Preserve that agreement. Any subsequently identified conflicting origin, boundary or course must be corrected in the model using the notes. |

Use the actual origins and routes described in the notes when reconciling the physical model. A catalogue parent or a replacement label alone does not correct an incompatible 3D course. This ledger records the differences identified during description preparation; it is not a completed comparison of every 3D course.

<a id="editorial-mapping-notes"></a>

## Editorial mapping notes

These notes are for the later content import, not the Description panel.

- The catalogue above retains the existing model names and IDs as a snapshot for the next import. The temporal and foramen rotundum display names have been amended for v0.8.2. Stable IDs should be retained through those changes. The notes’ “posterior superior dental” and “inferior dental” arteries currently map to the model’s posterior superior alveolar and inferior alveolar arteries.

- The STA-origin vessel called “posterior deep temporal” in the notes maps to the model’s **Middle temporal artery**. The maxillary-origin “middle deep temporal” maps to **Posterior deep temporal artery**. Parentage is used to distinguish them, and the source names remain in the descriptions.

- The notes use a broad “ciliary arteries” paragraph in the ophthalmic section. The model’s posterior ciliary entries instead use the explicitly posterior-ciliary wording in the orbital collateral section. The medial and lateral mesh representatives share that description.

- Numbered perforators, cortical continuations, palpebral arcades and other representative meshes share a branch-family or territory description only where the notes support it. A shared paragraph does not establish a separately described origin or course for every mesh.

- Bony-landmark descriptions are vessel-passage excerpts where the notes state that relationship. The foramen caecum mentioned in the medullary-perforator paragraph is not linked to the skull’s foramen caecum.

- The notes’ ICA segment boundaries are retained, including the paraophthalmic segment starting just proximal to the ophthalmic ostium. This document does not alter geometry or segment boundaries.

- Light copy-edits include “hard plate” to “hard palate”, “Munro” to “Monro”, restoration of line-break hyphens, and the duplicated wording in the masseteric origin sentence. No external reference material has been added.
