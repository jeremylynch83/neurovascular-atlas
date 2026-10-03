# Neurovascular anatomy: discrepancy audit and correction specification

**Model:** INR Anatomy Atlas v0.7.4, supplied as `inr-anatomy-atlas-v0.7.4(1).zip`  
**Reference:** Jeremy Lynch's supplied `nv.pdf`, Chapter 2, printed pp. 7-91  
**Audit date:** 3 October 2026  
**Targeted ICA follow-up:** v0.7.6, from `inr-anatomy-atlas-v0.7.6.zip` and `INR_Segments_Authoring_v0.7.6.zip`; segment definitions, branch parents and authoring logic checked.  
**ICA visual reference:** user-supplied `ICA_vascular_segments_Jan_Ting.png`, artwork credited to Jan Ting; inspected directly. See section 5.1.  
**Purpose:** a worklist for correcting and extending the 3D atlas. No model files were changed.

**Scope update, 3 October 2026:** the user has deferred new brain, brainstem, cerebellar, cranial nerve and cervical vertebral context, veins, aortic arch/subclavian access anatomy and the complete spinal vascular system. These remain documented for later, but are outside the current correction batch. G01-G03 are historical v0.7.4 shape observations requiring reassessment after subsequent ICA work. The user now specifically identifies incorrect ICA branch origins relative to the new selectable segments: this is active item A15. The targeted v0.7.6 follow-up confirms that selectable segments exist and checks their metadata/authoring logic; it does not provide a complete new surface or anatomical audit.

| Current status | Items | How to use this document |
| --- | --- | --- |
| **Active arterial worklist** | Missing named branches, branch-specific anastomosis endpoints, cortical branching, arterial segment metadata and nomenclature. | Use the v0.7.4 findings as the baseline; check affected items against the latest model before changing it. |
| **Active ICA origin correction** | A15: physical branch origins must agree with anatomically defined ICA segments in v0.7.6. | Check ostia, segment boundaries and catalogue/relationship assignments together. Correct labels alone do not establish correct origins. |
| **Active GUI requirements** | U01-U02: preserve panel collapse state and show the selected structure in the inspection title. | Include these small interface corrections alongside the arterial work. |
| **RESOLVED** | A01's absence of selectable ICA regions. | v0.7.6 has fourteen selectable regions, seven per side. Preserve them; assess origin and boundary correctness under A15. |
| **REASSESS** | G01-G03: ICA-A1/M1 junction, proximal ophthalmic/PCom bends and PCom/AChA origin positions. | Review the subsequent geometry work first. Close resolved findings and reopen only residual discrepancies. |
| **DEFERRED** | T01-T03, V01-V06, S01-S05, G04-G07, G11 and X12. | Retain for later; do not implement these modules or use their absence as a current completion failure. |
| **Partly deferred** | P01 cervical segmental/enlargement system; X11 ascending/deep cervical extensions; tissue-dependent validation in other arterial items. | Retain selected arterial branches and connections in scope, without expanding into the full cervical/spinal system or adding tissue meshes. |

Deferring tissue context does not establish that the existing vessel courses are correct. Arterial naming, origins, branching and potential connections can still be reviewed against the notes and references; exact tissue relationships remain unvalidated. The facial nerve arterial arcade remains active despite deferral of cranial nerve meshes and the broader nerve-supply graph.

## 1. Main findings and first correction batch

The current arterial correction priorities are incomplete small-branch anatomy, simplified anastomotic endpoints, sparse distal cortical branching and incomplete segment/naming metadata. Several apparent branching discrepancies are legitimate variants or differences in terminology, rather than errors. Wider tissue, venous, access and spinal coverage is deferred under the scope update above.

The first correction batch should address these items:

1. **Correct ICA branch origins within the adopted segments.** In v0.7.6, ophthalmic/superior hypophyseal belong to paraophthalmic, PCom to posterior communicating, AChA to the anterior choroidal ostial region, and A1/M1 to the terminus. Petrous and cavernous branches must also arise within their correct anatomical regions. Review the actual origins and segmentation together, rather than accepting the automatically generated branch parents as anatomical validation. See A15 and section 5.1.
2. **Replace generic ILT branches with their named rami.** The superior branch, anterior medial/lateral rami, posterior medial/lateral rami and recurrent lacerum route are incompletely represented. See A04 and X01-X04.
3. **Correct the infraorbital anastomosis endpoint.** The v0.7.4 overlay connects directly to the main ophthalmic artery despite describing an orbital muscular communication. Add the actual recipient branch or branches and attach there. See X05.
4. **Add the facial nerve arcade and tympanic network.** The petrosal MMA and stylomastoid arteries exist, but their connection is absent. The superior tympanic and subarcuate vessels are also missing. See E08, P04 and X06-X07.
5. **Complete selected ascending pharyngeal collateral routes.** Add the superior pharyngeal carotid/lacerum branch, musculospinal-to-VA route, bilateral odontoid arcade and lateral clival connection. Ascending/deep cervical extensions that require T03 remain deferred. See E15-E19 and X08-X14.
6. **Add clinically important omitted intracranial branches.** Prioritise ACom/subcallosal perforators, anterior choroidal cisternal branches, terminal ICA perforators, direct VA medullary perforators, and the PCA/SCA dural branches. See A06-A08 and P02-P06.
7. **Review ACA/MCA cortical branching and distal connections explicitly.** Reconcile precuneal/superior internal parietal terminology and the selected paracentral origin; review the anterior parietal division assignment; add a selected polar temporal branch and segment metadata; refine representative distal branching and pial/choroidal connection families. See A10-A14, P11-P12 and X18-X19. Exact tissue-based course validation remains deferred.
8. **Preserve explicit panel state and update the inspection title.** Clicking an anatomical structure must not reopen a collapsed panel. The inspection title must use the selected structure's human-readable name, including when the panel is collapsed. See U01-U02.

**ICA geometry:** A15 is active despite the subsequent smoothing work. Separately reassess the older shape concerns G01-G03 before further junction or curve deformation. Selectable ICA segmentation A01 is implemented in v0.7.6 and should be retained.

The existing ACom, bilateral PCom-PCA connections, vertebrobasilar union and paired ASA root union should be retained. The audit found actual shared mesh vertices at their documented connections. Do not rebuild them merely because the catalogue gives a communicating vessel a single display parent.

## 2. What was examined and how to interpret the findings

### 2.1 Evidence examined

- Full text of the 86-page PDF, including its arterial, venous and spinal sections. Printed page numbers are used throughout. For the numbered chapter pages, **PDF page = printed page minus 6**. The final PDF page is blank.
- Visual inspection of selected PDF diagrams, including ICA branches, MCA branches, PCA branches, venous sinuses and spinal vascular organisation.
- `public/anatomy/manifest.json` and `anatomy/generated/complete_manifest.json`: structure names, parent-child hierarchy, geometry bindings, provenance and relationship graph.
- The three shipped GLBs, decoded from meshopt compression for direct inspection of their exported vertices and triangles.
- Orthographic renders of the actual arterial surfaces in anterior and lateral views, an ECA view, a posterior circulation view, and terminal ICA close-ups.
- The modelling documents, landmark register and supplied numerical validation reports. These were treated as process records, not proof of anatomical correctness.
- Targeted primary anatomical studies where the notes were ambiguous or contained a statement that should not become a fixed modelling rule. See section 11.
- Targeted v0.7.6 follow-up: both manifests; `docs/SEGMENTS_v0.7.6.md`; `docs/validation/ica-segment-boundaries-v0.7.6.json`; and the companion authoring files `surface-centrelines.json`, `segments.json` and `tools/segments/segment_ica.py`. Fourteen segment records and twenty direct ICA branch-parent/`branches_to` assignments were checked. The rest of this document's inventory and geometric measurements remain tied to v0.7.4.

This is a catalogue, topology and targeted geometry audit. It is not an exhaustive triangle-intersection audit or a patient-derived anatomical validation. Exact sulcal, ventricular and nerve relations cannot be established from the current assets because the necessary tissues are absent.

### 2.2 Verified inventory

| Item | Shipped model |
| --- | ---: |
| Total catalogue records | 649 |
| Arterial records, including the root group | 420 |
| Named arterial mesh parts | 419 |
| Normal circulation mesh parts | 385 |
| ECA mesh parts, including the two ECA trunks | 162 |
| Anterior circulation mesh parts | 125 |
| Posterior circulation mesh parts | 98 |
| Potential-anastomosis mesh parts | 34, comprising 17 routes on each side |
| Bone catalogue records | 229 |
| Named bone/dental mesh parts | 60 |
| Vein records or mesh parts | 0 |
| Brain records or mesh parts | 0 |

There are 154 landmark records, with status counts of 29 visible, 33 partial, 38 regional, 31 unresolved, 17 variant-unresolved and 6 bone-unavailable. A landmark marker is not a segmented canal or a new vessel.

All 479 mesh-bound structure records have `reviewStatus: unreviewed`. The 23 principal bone records retain `geometryStatus: placeholder` despite having mesh assets; this is a provenance/quality designation, not evidence that the bones are absent. The mandible, bilateral maxillae and 32 FDI-labelled teeth are present.

The supplied anatomy validator passes: 479 named parts and three assets. It checks catalogue consistency, source references and GLB node bindings. It does not establish whether a branch has the right anatomical origin, course or recipient territory.

### 2.3 Classification and priority

| Code | Meaning |
| --- | --- |
| **C** | Confirmed omission, simplified graph or metadata discrepancy, established from the shipped files. |
| **G** | Geometry concern or unresolved anatomical relationship. Requires reference-guided review before changing coordinates. |
| **V** | Valid variant or naming difference. Align terminology or declare the chosen variant; do not automatically change topology. |
| **N** | Clarify the notes before using the statement as a model-generation rule. |

| Priority | Meaning |
| --- | --- |
| **P0** | Correct an existing representation that could teach a misleading connection or relationship. |
| **P1** | Add important missing anatomy or anatomical context. |
| **P2** | Improve completeness, segmentation or terminology. |
| **P3** | Optional variant scenes after the reference configuration is corrected. |

**Status overrides priority:** DEFERRED items are outside the current batch, irrespective of their original anatomical importance. REASSESS items require review of the updated model before further correction. RESOLVED identifies a requirement confirmed implemented in the later build. Untagged findings describe the supplied v0.7.4 baseline unless explicitly marked as a v0.7.6 follow-up.

**Absence does not mean regression.** The package deliberately contains one combined arterial scene. A missing vein or arch is a coverage gap relative to the notes, not evidence that it disappeared from an earlier release.

**ID convention:** existing ECA IDs generally end in `.right`/`.left`; anterior and posterior IDs generally end in `_right`/`_left`. Tables quote actual right-sided IDs as locators; apply the corresponding change on both sides unless the item explicitly concerns a variant. Names proposed for new vessels are not existing IDs.

## 3. Proximal vessels and cervical access anatomy

**DEFERRED:** this section is retained for a later access/cervical module. Existing upper cervical arterial connections can still be corrected without building the arch/subclavian scaffold.

| ID / priority / basis | Current model | Discrepancy relative to the notes | Required correction and acceptance condition | Notes |
| --- | --- | --- | --- | --- |
| **T01 / DEFERRED / C** | `artery.anterior.common_carotid_right` and `_left` are truncated cervical segments. No aortic arch, brachiocephalic trunk or subclavian arteries. | The notes describe the arch and the different origins of the right and left CCAs. The model cannot show access anatomy or explain those differences. | Add a selected normal arch configuration: arch to brachiocephalic, left CCA and left subclavian; brachiocephalic to right CCA and right subclavian. Join the existing trunks continuously. Preserve explicit lower truncation boundaries until this is implemented. | pp. 8-11, Figs 2.1-2.2 |
| **T02 / DEFERRED / C** | `artery.posterior.vertebral_right` and `_left` have no subclavian parents or origins. | The V1 origin and selection route are missing. A truncated VA should not appear to originate independently in the neck. | Add bilateral VA origins from the first subclavian part in the selected reference variant. Preserve the V1-V4 course and recheck calibre transitions. | pp. 9, 47-48 |
| **T03 / DEFERRED / C** | No thyrocervical, inferior thyroid, ascending cervical, costocervical, deep cervical or supreme intercostal arteries. | Important cervical collateral and spinal donor systems are absent. | Prioritise the ascending cervical and deep cervical systems with their correct parents, then the remaining subclavian branches. Ascending cervical usually branches from inferior thyroid; deep cervical and supreme intercostal branch from costocervical. Do not attach both directly to the subclavian merely for convenience. | pp. 8-9, 47, 60, 77-79 |

Internal thoracic, suprascapular, transverse cervical and dorsal scapular branches are also absent. They can follow the main cervical collateral additions. Coronary arteries and small thoracic visceral branches are described in the notes but are lower priorities for the present cranial atlas.

The cervical ICA is branch-free in the selected default model, consistent with the notes. Its continuation into the skull base is present. Aortic arch variants, direct arch-origin left VA and persistent carotid-vertebrobasilar arteries belong in optional configurations, not simultaneously in the default anatomy.

## 4. External carotid branching and missing branches

### 4.1 Proximal ECA, facial and superficial temporal territories

The eight principal ECA branches are represented on both sides: superior thyroid, lingual, facial, occipital, ascending pharyngeal, posterior auricular, maxillary and superficial temporal. The lingual branches, facial labial branches, maxillary terminal branches and main MMA divisions are substantially present. Avoid replacing these trees wholesale.

| ID / priority / basis | Current model locator | Finding and correction | Notes |
| --- | --- | --- | --- |
| **E01 / P2 / C** | `artery.eca.superior_thyroid.right` | Superior laryngeal and infrahyoid branches exist; named sternocleidomastoid and cricothyroid branches do not. Add selected representatives and the thyroidal arcade when the inferior thyroid artery is available. | p. 12 |
| **E02 / P2 / C** | `artery.eca.facial.right` | No separately named submandibular gland, facial masseteric or facial buccal branches. Existing `artery.eca.maxillary.masseteric.right` and `.buccal.right` are **maxillary** branches and do not fill this gap. Add the relevant facial branches or explicitly label their omission. | pp. 14-15 |
| **E03 / P2 / C** | `artery.eca.angular.right`; `artery.anterior.lacrimal_right` | The medial/lateral palpebral branches and palpebral arcades are absent. The angular-dorsal nasal connection alone does not represent eyelid supply. Add selected palpebral branches with recipient territories and arcades. | p. 15 |
| **E04 / P2 / C** | `artery.eca.posterior_auricular.right`; `artery.eca.superficial_temporal.right` | Named parotid and auricular branches are absent. Add posterior auricular territory branches and the STA anterior auricular branches if fuller extracranial coverage is intended. | pp. 15-16 |
| **E05 / P2 / C** | `artery.eca.superficial_temporal.transverse_facial.right` | Only one transverse facial part is named. The superior/inferior divisions and their parotid/masseteric branches are not distinguished. Add or segment these rather than treating one terminal line as the full transverse facial tree. | p. 16 |
| **E06 / P2 / C** | `artery.eca.superficial_temporal.right` | The zygomatico-orbital artery is missing. Add its course along the upper zygomatic arch towards the lateral orbital angle and its appropriate distal relationships. | p. 16 |
| **E07 / P2 / V** | `artery.eca.posterior_deep_temporal.right` is a maxillary child; `artery.eca.middle_temporal.right` is an STA child. | The notes use middle deep temporal for the maxillary vessel and posterior deep temporal for an STA territory vessel. The current pattern is compatible with common alternative nomenclature. Reconcile names and aliases with the intended Kiyosue convention before changing a parent. See N03. | pp. 16, 21, 26 |

The stylomastoid vessel is **not missing**. Its actual parent is the posterior auricular artery, although its ID is `artery.eca.occipital.stylomastoid.right`. This is a valid origin. The embedded word `occipital` in a stable ID is misleading technical naming, not an anatomical reason to reparent the artery. Add an alias or internal mapping if needed.

### 4.2 MMA, accessory meningeal and distal maxillary territories

| ID / priority / basis | Current model locator | Finding and correction | Notes |
| --- | --- | --- | --- |
| **E08 / P0 / C** | `artery.eca.maxillary.mma.petrosal.right`; `artery.eca.occipital.stylomastoid.right` | Both vessels exist, but the facial arcade connecting them does not. Add a named potential intratemporal communication with an explicit facial nerve/geniculate relationship. Do not substitute the unrelated MMA-ILT overlay. | pp. 17, 24, 60-61 |
| **E09 / P1 / C** | `artery.eca.maxillary.mma.right` and its frontal/posterior branches | Missing named superior tympanic, paramedian MMA and falcine-related terminal branches. Cavernous MMA is one generic part instead of anterior/posterior components. Add clinically relevant subbranches and distinguish the coronal/paramedian continuation beside the SSS. Keep the petrosal and petrosquamosal branches distinct. | pp. 24-25 |
| **E10 / P1 / C** | `artery.eca.maxillary.accessory_meningeal.right` | A single named trunk represents both extracranial Eustachian/pharyngeal and intracranial ovale/Meckel's cave territories. Add anterior/tubal and posterior/intracranial branches. The existing accessory meningeal-ILT relationship is only one of their connections. | pp. 25-26, 58-59 |
| **E11 / P1 / C** | `artery.eca.maxillary.right` | The artery of the superior orbital fissure is missing. The artery of foramen rotundum is present but cannot represent both passages. Add a distinct SOF artery and its ILT/ophthalmic relationships. Review the wording of its passage in the notes before fitting it. | p. 27, Fig. 2.6 |
| **E12 / P2 / C** | `artery.eca.maxillary.infraorbital.right` | The anterior superior alveolar branch exists, but a distinct orbital muscular branch is absent. This becomes P0 when correcting X05 because it is needed as an anatomically specific donor/recipient route. The inferior rectus/oblique and lacrimal sac contexts are also absent. | p. 27 |
| **E13 / P2 / C** | `artery.eca.posterior_septal.right`; `artery.eca.posterior_lateral_nasal.right` | The main sphenopalatine split exists. Superior/inferior septal subdivisions and the fuller nasal/palatine network are omitted. Add these selectively, plus ethmoidal/palatine relationships. Kiesselbach's plexus should be a distal network, not a new large proximal conduit. | pp. 28-29 |

The inferior alveolar, mental, incisive and mylohyoid vessels are present. The v0.7.3 process record documents a course within an estimated mandibular envelope. This does not certify containment within a segmented mandibular canal. Treat this as G08, not a missing-branch finding.

### 4.3 Occipital and ascending pharyngeal territories

| ID / priority / basis | Current model locator | Finding and correction | Notes |
| --- | --- | --- | --- |
| **E14 / P2 / C** | `artery.eca.occipital.right`; `.occipital_mastoid.right` | Scalp, descending and mastoid parts exist. Named proximal SCM branches and the mastoid/posterior meningeal subdivisions along the sigmoid region are incomplete. Extend the mastoid dural tree and its connections, rather than adding a duplicate generic occipital vessel. | pp. 17-18 |
| **E15 / P1 / C** | `artery.eca.superior_pharyngeal.right` | Missing separate Eustachian/tubal and carotid branches. The carotid branch to the lacerum/ILT region is a major omitted dangerous route. Add those subbranches and connect to the correct recipient. | pp. 19, 58 |
| **E16 / P1 / C** | `artery.eca.apa.right`; `.apa.neuromeningeal_trunk.right` | The musculospinal branch is absent. A hypoglossal-derived descending odontoid part is present, but is not a substitute for the lateral C2-C3 musculospinal communication. Add the musculospinal branch separately. | pp. 19, 60 |
| **E17 / P1 / C/G** | `artery.eca.apa.descending_odontoid.right`; `artery.posterior.va_odontoid_contribution_right` | The model has one ipsilateral connection per side, with the VA contribution described as C2. The notes refer to C3 radicular contributors and a contralaterally connected odontoid arcade. Add the transverse/cross-midline arcade and distinguish its contributors. The exact segmental level needs cervical vertebrae and reviewed source anatomy. | pp. 20, 47, 60 |
| **E18 / P1 / C** | `artery.eca.apa.jugular.right`; `.lateral_clival.right`; `.medial_clival.right` | Jugular/hypoglossal trunks and both clival territories exist, but only the medial clival-MHT potential connection is recorded. Add the lateral clival-MHT connection and the relevant contralateral clival links. | pp. 19-20, 33-34, 58 |
| **E19 / P1 / C** | `artery.eca.apa.posterior_meningeal.right`; `.apa.sigmoid_sinus_branch.right` | No separately named falx cerebelli artery or ascending internal-auditory-canal branch from the jugular division. Add these and their posterior fossa dural connections. Distinguish falx cerebelli from the supratentorial falx cerebri. | pp. 19-20 |

The basic APA division into pharyngeal and neuromeningeal trunks, three pharyngeal branches, inferior tympanic, jugular and hypoglossal branches is already present. Inferior tympanic origin directly from the APA is an acceptable variant. Do not force it to be a neuromeningeal child solely because that is a common origin.

## 5. ICA, ophthalmic, ACA and MCA anatomy

| ID / priority / basis | Current model locator | Finding and correction | Notes |
| --- | --- | --- | --- |
| **A01 / RESOLVED / C** | `artery.anterior.internal_carotid_right` | The v0.7.4 absence of selectable ICA regions is resolved in v0.7.6: seven NYU/Shapiro regions per side are present. Preserve the selectable regions. Their correct anatomical boundaries and branch origins are a separate requirement under A15; NYU and Bouthillier boundaries must not be treated as interchangeable. | pp. 30-37, Fig. 2.8; v0.7.6 follow-up |
| **A02 / P1 / C** | `artery.anterior.vidian_ica_contribution_right`; `.caroticotympanic_right` | ICA vidian and caroticotympanic parts exist. The mandibular branch/mandibulovidian split is missing, leaving the pharyngeal/Eustachian arterial circle incomplete. Add the mandibular branch from the petrous territory, with its appropriate soft-tissue route and connections. | pp. 32, 58-59 |
| **A03 / P1 / C/V** | `artery.anterior.meningohypophyseal_trunk_right`; `.tentorial_marginal_right`; `.dorsal_meningeal_right`; `.inferior_hypophyseal_right` | A common three-branch MHT arrangement is present. The notes distinguish basal/lateral tentorial and lateral/medial clival components in more detail. Add the absent basal tentorial branch and named clival subdivisions/relationships. Do not label the current three-branch pattern intrinsically wrong: a generic dorsal meningeal artery may encompass part of the clival territory. | pp. 33-34 |
| **A04 / P0 / C** | `artery.anterior.inferolateral_trunk_right`; `.ilt_anterior_branch_right`; `.ilt_posterior_branch_right` | Only two generic ILT daughters exist. There is no named superior branch, anteromedial/anterolateral split, posteromedial/posterolateral split or recurrent lacerum branch. Add those rami and use them as the actual connection endpoints. Keep optional McConnell capsular branches separate from the core ILT branch correction. | p. 34, Fig. 2.8, pp. 58-61 |
| **A05 / P1 / C** | `artery.anterior.ophthalmic_right`; `.lacrimal_right`; `.anterior_ethmoidal_right` | Central retinal, two posterior ciliary, lacrimal, supraorbital, supratrochlear, dorsal nasal and both ethmoidals exist. Missing orbital muscular, palpebral and explicit recurrent meningeal branches; anterior ethmoidal meningeal/falcine continuation is also absent. Add these before routing corresponding overlays to a large ophthalmic trunk. Do not generate retinal anastomoses as though they were routine collaterals. | pp. 35-36, 59 |
| **A06 / P1 / C** | `artery.anterior.anterior_choroidal_right` | A single approximate cisternal/plexal course has no named children. The important cisternal perforators and territory branches described in the notes are missing. Add selected branches towards the optic tract, internal capsule, peduncular and temporal/choroidal territories, constrained by tissue context. Include a plexal landmark and the posterior choroidal network, without imposing a blanket absence of distal parenchymal branches. See N01. | pp. 36-37 |
| **A07 / P1 / C** | `artery.anterior.internal_carotid_right`, terminal region | No named terminal ICA perforators to the anterior perforated substance. Existing MCA/ACA lenticulostriates do not represent all ICA terminus branches. Add selected terminal ICA perforators with reviewed origins and targets. | p. 37 |
| **A08 / P1 / C** | `artery.anterior.anterior_communicating` | The ACom connection exists, but there are no named ACom perforators or subcallosal artery. Add the subcallosal artery and representative hypothalamic/septal/chiasmatic branches. Keep their supply distinct from the recurrent artery of Heubner. | pp. 41-42 |
| **A09 / P2 / C** | `artery.anterior.medial_lenticulostriate_right`; `.lateral_lenticulostriate_1_right` through `_3_right` | One medial and three lateral examples per side form a teaching sample, not the full perforator anatomy in the notes. Add representative groups and territory information; do not invent a fixed universal number. Origin variants from A1/M2 can be optional configurations. | pp. 40, 44 |
| **A10 / P2 / C/V** | `artery.anterior.aca_pericallosal_right`; `.callosomarginal_right`; `.paracentral_right` | A2-A5 are combined under pericallosal. Internal frontal branches arise from callosomarginal, but paracentral is a direct pericallosal child. The notes show the latter as a callosomarginal branch. This is a valid variable origin. For strict concordance with the illustrated configuration, move its origin to the callosomarginal **and update the surface**, or explicitly declare the present variant. Add segment boundaries separately. | pp. 40-43 |
| **A11 / P2 / C/V** | `artery.anterior.precuneal_right`; `.inferior_internal_parietal_right`; `artery.posterior.pca_splenial_right` | A precuneal vessel may correspond to part of the superior parietal territory; PCA splenial corresponds to posterior pericallosal terminology. Add aliases before declaring these branches absent. Truly absent named ACA short/long callosal and falcine branches should be added selectively. The ACA-PCA perisplenial connection is absent from the relationship graph. | pp. 42-43, 57 |
| **A12 / P2 / C** | `artery.anterior.mca_superior_division_right`; `.mca_inferior_division_right`; named cortical children | M1 and two divisions exist, with most major cortical names. There is no explicit M3 stage, and no consistently defined M2-M3-M4 transition. Add segment ranges and courses through the insular/opercular anatomy. A cortical branch label alone cannot establish whether the vessel traverses the correct fissure. | pp. 44-46 |
| **A13 / P2 / C** | `artery.anterior.anterior_temporal_right`; `.middle_temporal_right`; `.posterior_temporal_right` | Anterior, middle and posterior temporal branches exist, but a distinct polar temporal branch is missing. Add it as a selected branch pattern. Use temporo-occipital/occipitotemporal aliases where appropriate; those names alone do not establish an omission. | pp. 45-46, Fig. 2.12 |
| **A14 / P2 / C/V** | `artery.anterior.anterior_parietal_right`; `.mca_inferior_division_right` | The anterior parietal artery is an inferior-division child on both sides, differing from the superior-division arrangement in Fig. 2.12. Review the chosen division pattern and declare it, or align the graph and surface with the illustrated configuration. Parietal origins vary, so the present parent is not automatically an anatomical error. Several named MCA vessels also have only one generic distal cortical twig; refine representative distal ramification without implying a complete or universal tree. [R8] | pp. 45-46, Fig. 2.12 |
| **A15 / P0 / G** | v0.7.6 `artery.anterior.internal_carotid_right.segment.paraophthalmic`; `.segment.posterior-communicating`; `.segment.anterior-choroidal`; corresponding branches and left-sided regions | The user reports that ICA branch origins remain incorrect relative to the new segments. Current metadata gives the expected branch parents, but those parents and several segment cuts are computed from the existing origins. This is not independent anatomical verification. Correct the physical ostia, segment boundaries, ICA/proximal branch curvature and graph together on both sides against the supplied Jan Ting diagram and notes. Retain recent refinements where they meet that visual target. See section 5.1. | pp. 30-37, Fig. 2.8; supplied diagram [J]; v0.7.6 follow-up; [R11] |

The main ACA cortical names are present bilaterally: orbitofrontal, frontopolar, three internal frontal branches, paracentral, precuneal and inferior internal parietal. Precuneal can represent superior internal parietal anatomy; confirm the territory before adding another vessel. [R9] Paracentral origin from pericallosal or callosomarginal is variable. [R10] The MCA has eleven main named cortical branches per side; the distinct polar temporal label is absent. Do not count the additional generic cortical twigs as separate missing main branches. Tissue registration is deferred, so these catalogue findings do not certify sulcal courses.

### 5.1 ICA branch origins and segment agreement, v0.7.6 follow-up

Use the **NYU/Shapiro endovascular scheme** already adopted by the latest build. The expected reference pattern below follows the supplied notes, pp. 30-37, Fig. 2.8. The original Shapiro classification was checked for consistency. [R11]

**Required visual target:** the user-supplied `ICA_vascular_segments_Jan_Ting.png` [J]. Its branch/segment relationships **and illustrated ICA/proximal branch curves** are the explicit reference for A15. Matching colours and branch names alone is insufficient. The diagram agrees with the adopted seven-region scheme.

| Feature in the supplied diagram | Required model relationship |
| --- | --- |
| Ophthalmic branch from the orange paraophthalmic region | Its actual ICA ostium lies in paraophthalmic, distal to the cavernous/paraophthalmic transition and proximal to PCom. It must not emerge from the cavernous region in the selected normal configuration. |
| PCom branch from the red communicating region | The paraophthalmic/communicating transition is at the PCom ostial region; PCom belongs to the beginning of communicating. |
| Thin AChA branch from the pink choroidal region | Its ostium lies in the choroidal region, distal to PCom and proximal to terminus. |
| Terminal bifurcation in the magenta terminus region | A1 and M1 arise at the distal ICA terminus; the choroidal region ends proximal to that bifurcation. |
| Curved carotid course through cavernous and paraophthalmic into the distal ICA | Match the illustrated course and smooth changes in curvature in the corresponding projection, with continuous taper and a smooth terminal bifurcation. |
| Curved proximal ophthalmic and PCom branches | Match the illustrated curved departures and proximal arcs. Avoid straight stubs, abrupt angulation and flattened bends introduced by moving origins. |

Compare the complete exported ICA and attached branches with this picture in a corresponding lateral view, then confirm origins, curvature and junction shape in oblique views and on the other side. Segment boundaries must fit the intended anatomy and corrected ostia. The picture is a schematic: match its course, bends, branch departures and region relationships; obtain millimetre dimensions from the authoring model and anatomical references rather than literal pixel measurements. Branches absent from the illustration, including superior hypophyseal, MHT and ILT, remain governed by the notes and source references.

| Selectable ICA region | Anatomical extent | Expected ICA origins in the selected normal configuration |
| --- | --- | --- |
| **Cervical** | CCA bifurcation to carotid canal entry. | Usually no branches. |
| **Petrous** | Canal entry to petrolingual ligament; includes the traditional lacerum portion. | Caroticotympanic, vidian contribution and the proposed mandibular branch. |
| **Cavernous** | Petrolingual ligament to estimated proximal dural-ring region. | MHT, usually at posterior genu; ILT, usually from horizontal cavernous ICA. Their daughters retain these trunks as parents. |
| **Paraophthalmic** | Estimated cavernous exit/proximal dural-ring region to PCom ostium; includes the clinoid region. | Ophthalmic and superior hypophyseal branches. |
| **Posterior communicating** | PCom ostium to AChA ostium. | PCom at the proximal boundary. |
| **Anterior choroidal** | ICA immediately surrounding the AChA ostium. | AChA and selected local perforators. |
| **Terminus** | Beyond the AChA ostial region to ICA bifurcation. | Terminal ICA perforators, ACA A1 and MCA M1. |

**What v0.7.6 already does:** both sides have the expected catalogue parents for the ten currently represented direct ICA branches/daughters: caroticotympanic and vidian to petrous; MHT and ILT to cavernous; ophthalmic and superior hypophyseal to paraophthalmic; PCom to posterior communicating; AChA to anterior choroidal; A1 and M1 to terminus. All twenty corresponding `branches_to` relationships agree with those parents. This resolves availability of segment selection, not anatomical correctness of the origins.

**Why the current checks are insufficient:** `tools/segments/segment_ica.py` derives PCom/AChA region limits from nearest sampled ICA centreline positions of the existing branch starts, with branch-radius offsets. It then assigns each branch parent using that same nearest-sample calculation. The cavernous/paraophthalmic transition uses a retained route station. Consequently, a wrongly placed origin can still obtain a plausible parent and colour because the boundary and parent were generated from its current location. The supplied viewer tests establish selection and tree behaviour, not correct anatomical ostia.

**Required correction and acceptance:**

1. Review the anatomical ICA course, available skull-base landmarks and the branch origins together. Confirm the segment definitions before accepting the colour boundaries. Retain uncertainty on estimated dural/petrolingual landmarks; new tissue meshes remain deferred.
2. Trace each branch to its actual ICA ostium. Correct the origin, segment boundary, or both where the chosen normal anatomy is inconsistent. Do not fix an origin discrepancy solely by changing its parent or moving a colour boundary around an incorrect origin.
3. Keep ophthalmic and superior hypophyseal origins within paraophthalmic; use the PCom ostium as the paraophthalmic/communicating transition; place AChA at its own ostial region, distal to PCom and proximal to the terminus. Check the usual branch order along the ICA centreline rather than relying only on global height.
4. Fit the ICA and proximal ophthalmic/PCom curves to the illustrated visual target. Retain recent curve and junction refinements where consistent with that target, and preserve valid distal connections and branch calibre. Moving an ostium must include refitting its proximal arc and rebuilding a smooth junction. Inspect the complete exported surface from multiple views.
5. Make selectable surface regions, catalogue parents, `branches_to` relationships, descriptions and attached anastomoses agree after correction. Check both sides independently. An ostium at a shared segment boundary may have a collar spanning that boundary; arbitrary nearest-face ownership alone is not evidence of an anatomical error.
6. Keep ophthalmic daughters attached to ophthalmic, MHT/ILT daughters to their respective trunks, and PCom perforators to PCom. Segment membership does not convert these into direct ICA branches. Explicitly declared origin variants require their own configuration.
7. Record a final comparison against the supplied Jan Ting diagram showing the ICA silhouette/curves, proximal branch arcs, ophthalmic/PCom/AChA origins and terminal daughter origins on correctly named ICA regions. Include both the segment colours and a common-colour view so label agreement, curvature and ostial shape can be assessed separately. A15 remains open until the physical representation meets these targets.

Do not equate the NYU posterior communicating region with the whole Bouthillier C7 segment: the latter also includes the choroidal and terminal portions distinguished separately here.

### 5.2 Requested GUI corrections

These are explicit user requirements. The current panel behaviour has not been independently tested in this audit.

| ID / priority | Required behaviour | Acceptance check |
| --- | --- | --- |
| **U01 / P1** | Each collapsible panel keeps its current expanded/collapsed state during anatomical selection. A collapsed panel reopens only when the user explicitly expands it. Keep each panel's state independent. | Collapse both panels, select several vessels and ICA segments in the scene, and confirm neither reopens. Explicitly expand the anatomy tree and repeat selections there: the tree stays open and inspection stays collapsed. Repeat with inspection open and tree collapsed using scene selections. Inspection content updates without changing panel state. |
| **U02 / P1** | The inspection panel title shows the selected structure's human-readable name. Update the title even while collapsed, so the selected structure remains identifiable. | Select different structures with the inspection panel open and collapsed. The title matches the current selection, including side/segment where present in its display name; internal catalogue IDs are not used as the title. |

### Correct patterns to preserve

- The ophthalmic, superior hypophyseal, PCom and anterior choroidal branches are present; the MHT and ILT are present on both sides.
- The ACA and MCA are ICA terminal daughters, with bilateral MCA bifurcation configurations.
- The recurrent artery of Heubner is attached to the pericallosal/A2 territory, an acceptable origin. It is not necessarily misplaced just because the notes also discuss it under A1.
- Posterior parietal and angular MCA children under the inferior division are compatible with the selected division pattern. Cortical territory assignment varies with dominance.
- The single ACom joins both A1 territories. Its right-sided display parent does not make it a unilateral artery.

## 6. Vertebral, basilar, cerebellar and PCA anatomy

**Scope:** P01's fuller cervical segmental/radicular and cervical enlargement system is deferred with the spinal module. Its missing anterior meningeal branch remains an arterial work item. Other named posterior arterial omissions remain active; tissue-based loop and ventricular-course validation is deferred.

| ID / priority / basis | Current model locator | Finding and correction | Notes |
| --- | --- | --- | --- |
| **P01 / P1 / C** | `artery.posterior.vertebral_right`; `.va_muscular_c1_right`; `.va_muscular_c2_right`; `.va_odontoid_contribution_right` | Selected upper cervical branches are present, but there is no fuller C1-C6 segmental spinal/radicular system, cervical enlargement artery or anterior meningeal branch. Add reviewed segmental contributors and the artery of cervical enlargement. Also add V1-V4 boundaries once vertebral context is available. | pp. 47-48, 77-79 |
| **P02 / P1 / C** | `artery.posterior.vertebral_right`; `.pica_medullary_perforator_right` | A PICA medullary perforator is present, but direct VA medullary perforators are missing. Add them as a separate donor group; do not assume all medullary supply comes from PICA. | pp. 48-49 |
| **P03 / P1 / C** | `artery.posterior.pica_right`; existing vermian, hemispheric, tonsillar, choroidal and medullary daughters | Five PICA anatomical segments and their landmarks are not distinguished. Add segment ranges and a telovelotonsillar loop landmark; review the loops against medulla, tonsils and fourth-ventricular context. The main PICA tree exists. A missing segment label is not a missing PICA. | pp. 49-50 |
| **P04 / P1 / C** | `artery.posterior.aica_right`; `.labyrinthine_right`; `.aica_rostral_branch_right`; `.aica_caudal_branch_right` | The subarcuate dural branch is missing, along with explicit fourth-ventricular choroidal supply and cochlear/anterior vestibular subdivision of the labyrinthine artery. Prioritise the subarcuate route and its MMA/stylomastoid connections. Reconcile rostral/caudal versus medial/lateral territory names by actual courses, rather than mechanically renaming them. | p. 52 |
| **P05 / P1 / C** | `artery.posterior.sca_right` and hemispheric/vermal children | Missing named proximal SCA perforators, tectal branch/network and artery of Wollschlaeger and Wollschlaeger. Add a distinct SCA dural branch to the medial tentorial territory, with its documented origin and compartment. | pp. 52-53 |
| **P06 / P1 / C** | `artery.posterior.pca_p2_p3_right` | The artery of Davidoff and Schechter is absent. Add the selected P2/proximal ambient-origin dural branch and its falcotentorial course. The notes' description of the falcotentorial region is a target territory, not a sufficient origin rule. See N04. | pp. 25, 57 |
| **P07 / P2 / C** | `artery.posterior.basilar`; `.pontine_paramedian_1_right` through `_3_right`; `.pontine_circumferential_right` | Selected paramedian and one circumferential example per side exist. Median, short circumflex and long circumflex groups are not separately represented. Add selected examples with correct pontine routes and targets, without implying a complete universal perforator count. | p. 51 |
| **P08 / P1 / C** | `artery.posterior.pca_p1_right`; `.pca_p2_p3_right`; `.peduncular_perforator_right` | There are thalamoperforator, thalamogeniculate and peduncular examples, but no named PCA long/short circumflex or collicular arteries. A peduncular perforator is not interchangeable with a circumflex/collicular branch. Add those branches and the PCA-SCA tectal network. | pp. 54-56 |
| **P09 / P2 / C** | `artery.posterior.pcom_perforator_right` | Only one generic PCom perforator per side, without a separately named tuberothalamic artery or anterior thalamoperforating group. Add representative branches/territories and appropriate aliases. Preserve the fact that a small PCom can still have significant perforators. | pp. 36, 54 |
| **P10 / P2 / C** | `artery.posterior.pca_p2_p3_right`; calcarine/parieto-occipital/temporal children | P2 and P3 are one part; P4 cortical ranges are not explicitly defined. Separate their metadata or surface labels at reviewed cisternal/cortical boundaries. Existing inferior temporal and splenial branches substantially correspond to the named cortical tree. | pp. 54-57 |
| **P11 / P1 / C/G** | `artery.posterior.medial_posterior_choroidal_right`; `.lateral_posterior_choroidal_right` | Both posterior choroidal trunks exist, but ventricular entry landmarks, plexal networks and anterior/posterior choroidal anastomoses are missing. Add the choroidal networks after registering the third/lateral ventricles, velum interpositum and choroid plexus. A line ending near an estimated ventricle does not certify the relevant supply. | pp. 36, 56-57 |
| **P12 / P1 / C** | ACA, MCA, PCA and cerebellar distal trees | Pial border-zone connections are not recorded in the graph: ACA-MCA, MCA-PCA, ACA-PCA splenial, PICA-AICA-SCA and the tectal network. Add selected potential distal connections as a separate teaching layer, at the proper pial surfaces. Do not fuse all nearby crossing branches. | pp. 40, 42, 46, 49, 52-57 |

The adult P1-PCom configurations, single basilar artery, bilateral PICA/AICA/SCA and paired proximal ASA roots are valid selected anatomy. The basilar having the right VA as its display parent is acceptable because the left VA connection is separately recorded and present in the mesh. Similarly, the ASA's right-root display parent does not mean its left root is absent.

## 7. Anastomoses: current routes and required corrections

**Scope:** named arterial endpoints and selected connection families remain active. X12 and X11's ascending/deep cervical extensions are deferred with T03. New brain, nerve or cervical vertebral meshes are not required in the current batch; precise tissue-level route validation remains pending.

### 7.1 Audit of all 17 existing route families

Each family has right and left instances in `complete-anastomoses.glb` and corresponding `potential_anastomosis` relationships. They are deliberately separate from the normal circulation union. Keep that separation: these illustrative channels should not all become conspicuous large normal vessels in the reference scene.

| Existing route family | Assessment | Action |
| --- | --- | --- |
| `mma_lacrimal__meningolacrimal` | Correct general territory. The cranio-orbital/Hyrtl canal is unresolved. | Retain; verify canal route and lacrimal attachment once the small passage is available. Distinguish partial lacrimal supply from whole-orbit meningo-ophthalmic variants. |
| `mma_ophthalmic__recurrent_meningeal` | SOF recurrent route is recognised, but its endpoints are generic cavernous MMA and main ophthalmic trunk. | **X01 / P0 / C:** add an explicit recurrent meningeal/ophthalmic branch and distinguish it from the ILT deep recurrent route and the Hyrtl canal route. Do not assume that a direct large-trunk connector depicts the right branch-level anatomy. |
| `angular_dorsal_nasal` | Appropriate named facial-ophthalmic endpoints. | Retain; add palpebral/nasal subnetworks separately rather than expanding this one route to represent them all. |
| `sta_supraorbital` | Appropriate selected scalp-ophthalmic route. | Retain; add supratrochlear and other scalp arcades selectively. |
| `infraorbital_ophthalmic` | The relationship ends at `artery.anterior.ophthalmic_right`, while its note says orbital muscular communication. | **X05 / P0 / C:** add the actual orbital muscular and/or distal lacrimal recipient route. The current endpoint is anatomically overgeneralised. Preserve separate muscular versus lacrimal pathways rather than simply moving every connection to lacrimal. |
| `foramen_rotundum_ilt` | Correct route family, but ends at generic `ilt_anterior_branch`. | **X02 / P0 / C:** attach to the anterolateral ILT ramus after creating the anterior split. |
| `accessory_meningeal_ilt` | Correct ovale route family, but ends at generic `ilt_posterior_branch`. | **X03 / P0 / C:** distinguish the posterior intracranial accessory meningeal branch and posteromedial ILT recipient. |
| `mma_cavernous_ilt` | Represents only a generic MMA-to-main-ILT link. | **X04 / P0 / C:** resolve anterior/posterior MMA cavernous connections and superior/posterolateral ILT territories. Connect named branches through their proper regional routes. |
| `vidian_eca_ica` | Appropriate maxillary-to-ICA vidian contributors. | Retain; add mandibular/pharyngeal/tubal circle branches and relationships separately. |
| `inferior_tympanic_caroticotympanic` | Appropriate tympanic family, with both branches represented. | Retain; expand the tympanic network without representing an aberrant ICA in the default scene. |
| `deep_temporal_lacrimal` | Appropriate selected anterior deep temporal-lacrimal route. | Retain; refine the zygomatic/inferior orbital route and the distal lacrimal recipient. |
| `septal_anterior_ethmoidal` | Appropriate selected septal-ethmoidal route. | Retain; add posterior ethmoidal and palatine routes separately. |
| `mma_tentorial_marginal` | Appropriate selected petrosquamosal/marginal tentorial communication. | Retain; it does not cover basal tentorial, falcine or all posterior fossa connections. |
| `apha_clival_mht` | Correct medial clival/dorsal meningeal territory connection, with generic MHT recipient naming. | **X08 / P1 / C:** clarify the recipient clival subdivision and add the distinct jugular/lateral clival route. |
| `occipital_vertebral_c1` | Appropriate selected C1 muscular family. | Retain; refine its segmental donor/recipient after C1 is registered. Do not rename it as a persistent proatlantal artery. |
| `occipital_descending_vertebral_c2` | Appropriate selected C2 muscular family. | Retain; add cervical donor connections separately and check the deep versus superficial descending branch. |
| `apha_odontoid_vertebral` | Only an ipsilateral representative link. | **X09 / P1 / C/G:** extend to the actual bilateral odontoid arcade, with prevertebral/descending contributors, transverse links and reviewed levels. Avoid treating a single straight link as the full arcade. |

The two infraorbital overlays approach the main ophthalmic mesh to within approximately **0.028 mm on the right and 0.017 mm on the left**. Their recorded graph endpoint is also the main ophthalmic artery. This supports the endpoint finding; proximity alone does not establish a patent anatomical lumen. No separate ophthalmic muscular artery exists in the current catalogue.

### 7.2 Missing connection families

The following are absent from the relationship graph. Some require adding a missing branch first. Draw them as small potential networks with explicit endpoints and anatomical compartments, not as arbitrary long straight links.

| ID / priority | Required connection family | Notes |
| --- | --- | --- |
| **X06 / P0** | Petrosal MMA to stylomastoid artery: the facial nerve arcade. | pp. 17, 24, 60-61 |
| **X07 / P1** | Tympanic network joining anterior tympanic, inferior tympanic, superior tympanic, stylomastoid and caroticotympanic branches; subarcuate connections where represented. | pp. 17, 19, 24, 52 |
| **X10 / P1** | Superior pharyngeal carotid branch to recurrent lacerum/ILT route; distinguish this from the clival-MHT route. | pp. 19, 34, 58 |
| **X11 / P1** | APA musculospinal to VA C2-C3/segmental route, ascending cervical and deep cervical. | pp. 19, 60 |
| **X12 / DEFERRED** | Ascending cervical/deep cervical to VA; descending occipital to cervical donor systems. Requires T03. | pp. 9, 17, 47, 60 |
| **X13 / P1** | Eustachian/pharyngeal circle: superior pharyngeal, accessory meningeal anterior/tubal, pterygovaginal, maxillary vidian and petrous ICA mandibular/vidian contributors. | pp. 19, 25, 28, 58-59 |
| **X14 / P1** | Jugular APA/lateral clival to MHT, contralateral clival communications, and selected clival-MMA/ILT links. | pp. 19-20, 33-34 |
| **X15 / P1** | Occipital mastoid/posterior meningeal to APA sigmoid/jugular/hypoglossal and MMA petrosquamosal dural networks; selected AICA subarcuate communication. | pp. 17-18, 24-25, 52 |
| **X16 / P1** | Anterior ethmoidal/anterior falcine to anterior MMA/paramedian branches; posterior falcine/falx cerebelli networks with their correct compartments. | pp. 20, 25, 35, 59 |
| **X17 / P1** | MMA/APA/occipital tentorial networks to PCA Davidoff-Schechter and SCA Wollschlaeger-Wollschlaeger dural branches. | pp. 25, 53, 57 |
| **X18 / P1** | Choroidal connections: anterior to lateral posterior choroidal; medial to lateral posterior choroidal; selected posterior choroidal/splenial networks. | pp. 36, 56-57 |
| **X19 / P1** | Pial collateral networks: ACA-MCA, MCA-PCA, pericallosal-splenial, PCA-SCA tectal, and PICA-AICA-SCA. | pp. 42, 46, 49, 52-57 |
| **X20 / P2** | Extracranial facial/buccal/transverse facial/infraorbital connections, labial/palatine/septal networks and scalp STA-occipital-posterior auricular arcades. | pp. 14-18, 26-29 |
| **X21 / P2** | Contralateral pharyngeal, labial, palatal, clival and hypophyseal communications where appropriate. The duplicated bilateral trees currently do not capture these cross-midline networks. | pp. 15, 19-20, 33-35 |
| **X22 / P2** | Potential transosseous scalp-dural relationships between STA/occipital and MMA. Distinguish normal potential channels from pathological enlargement. | pp. 18, 25 |

Normal communicating arteries in the circle of Willis are anatomically different from these potential collateral overlays. Keep their graph and display semantics distinct. A crossing seen in a projection is not enough to add an anastomosis.

## 8. Geometry, tissue relationships and cranial nerve supply

**Current status:** G01-G03 require reassessment after the user's subsequent ICA geometry work. All measurements and geometry concerns below refer to the supplied v0.7.4 assets. G04-G07 and G11 are deferred; their absence does not block the current arterial correction batch. G08-G10 remain relevant to available bone passages, bilateral reference geometry and calibre provenance.

### 8.1 Targeted terminal ICA measurements

The figures below are **centroids of coincident exported surface vertices at label boundaries**, measured in RAS millimetres. They are useful for locating the junction regions. They are not original centreline ostia, luminal measurements or anatomical target coordinates. Broad collars can shift these centroids away from the actual branch centreline origin.

| Attachment | Right centroid `(R, A, S)` mm | Left centroid `(R, A, S)` mm |
| --- | --- | --- |
| Ophthalmic-ICA seam | `(10.544, -40.514, 74.410)` | `(-8.864, -40.715, 73.932)` |
| PCom-ICA seam | `(10.729, -42.823, 75.799)` | `(-9.045, -43.096, 74.919)` |
| AChA-ICA seam | `(13.695, -42.761, 79.627)` | `(-11.980, -43.075, 78.548)` |
| A1-ICA seam | `(16.124, -36.469, 84.749)` | `(-16.265, -36.253, 84.844)` |
| M1-ICA seam | `(18.325, -37.602, 83.996)` | `(-18.094, -37.588, 83.820)` |

The PCom-AChA seam-centroid distance is 4.843 mm on the right and 4.667 mm on the left. The notes describe a usual 2-4 mm origin separation, but these are different measurements. This is a reason to review the **actual ostia and ICA arc length**, not proof that the model violates that range. Likewise, increasing a global `S` coordinate is not by itself a valid anatomical correction.

The sampled v0.7.4 ICA branch interfaces have shared vertices, so the original concern was not simple disconnection. Whether residual shape or calibre-transition problems remain after the subsequent work has not been assessed.

| ID / priority / basis | Concern | Required correction / acceptance condition |
| --- | --- | --- |
| **G01 / REASSESS / G** | Terminal ICA/A1/M1 confluence: the close-ups show a broad junction region that deserves review despite shared vertices and the previous M1 refinement. | Reconstruct a clean carotid terminus with continuous taper and smooth daughter origins, using reviewed oblique and orthogonal views. Inspect with all connected label parts present and a common colour. Do not diagnose holes from a view that hides the neighbouring labels. |
| **G02 / REASSESS / G** | PCom root has an abrupt proximal turn; AChA/PCom levels need review in relation to the terminal ICA, rather than merely the skull. | Fit the communicating and choroidal segment origins together. Preserve the usual proximal-to-distal sequence: ophthalmic origin, PCom, AChA, terminus. Review branch direction, ostial position and proximal radius; assess curvature and unintended contact on the final skin. |
| **G03 / REASSESS / G** | Ophthalmic proximal course has marked angulation, with an estimated optic-canal route. Its correct height cannot be certified from the skull alone. | Fit the origin, proximal curve and canal entry together, with an optic nerve and reviewed dural-ring estimate. Preserve the chosen supraoptic crossing pattern. Moving the ostium alone can distort the neighbouring surface and is not sufficient. |
| **G04 / DEFERRED / C/G** | No cerebrum, insula, corpus callosum, interhemispheric surface or sulcal context. | Add registered tissue surfaces before certifying ACA pericallosal/callosomarginal and MCA insular/opercular/cortical courses. Retain uncertainty on the current manually fitted cortical paths. |
| **G05 / DEFERRED / C/G** | No pons, medulla, midbrain, cerebellum, tonsils, flocculus or fourth-ventricular context. | Register those tissues, then fit VA/basilar courses and PICA/AICA/SCA loops and territories. Skull clearance alone does not prove a cerebellar branch is pial or correctly located. |
| **G06 / DEFERRED / C/G** | No optic nerves/chiasm/tracts, cranial nerves, pituitary, dura or cavernous sinus mesh. | Add selected anatomy or validated landmarks for optic relations, III between PCA/SCA, AICA VII/VIII/IAC relations, the facial canal arcade, and APA IX-XII supply. Keep nerve supply as a separate relationship from a vessel merely passing through the same foramen. |
| **G07 / DEFERRED / C/G** | No C1-C7 vertebrae, atlas groove, dens, spinal cord or nerve-root context. | Register cervical anatomy before certifying V2 foraminal passage, V3 course, odontoid arcade level or cervical spinal artery locations. Estimated upper-cervical curves are not validated segmental anatomy. |
| **G08 / P1 / G** | Carotid canal, optic canal, mandibular canal and several small passages are unresolved or regional estimates. Dural rings are estimated. | Keep visible bone anchors separate from estimated lumen paths and soft-tissue boundaries. Add resolved canal geometry if available, then test vessel surfaces against the permitted canal/foramen routes. Preserve the correct rule that ICA passes above the lacerum cartilage rather than vertically through the opening. |
| **G09 / P2 / C/G** | Bilateral trees are generated from mirrored starting paths with modest adjustments, not independent bilateral segmentations. | Declare this as a reference configuration. Preserve shared reusable geometry where appropriate, but review branch origins and skull/tissue fitting separately on each side. Do not imply the near-symmetry is a measured anatomical finding. |
| **G10 / P2 / C/G** | Vessel calibre is illustrative; small branches can be enlarged for visibility. Overlay calibre is also illustrative. | Record calibre provenance and distinguish true model scale from display enhancement. Use reviewed vessel-specific radius profiles. Numerical watertightness, mesh density and uniform taper do not validate real luminal diameters or haemodynamics. |
| **G11 / DEFERRED / C** | No structured cranial-nerve supply graph, despite numerous vessel/foramen landmarks. | Add `supplies`-type relationships for the selected nerve segments: ILT/MHT for cavernous nerves, petrosal/stylomastoid/internal auditory for VII, labyrinthine for VIII, jugular APA for IX-XI, hypoglossal APA for XII and musculospinal APA for spinal XI. Review optic nerve versus retinal supply separately. Reference Table 2.1 with its caveats. |

### 8.2 Connection checks that passed

These comparisons found exactly coincident vertex positions at the specified interfaces, using a 0.00001 mm numerical threshold:

| Interface | Shared vertices found |
| --- | ---: |
| ACom to left A1 | 53 |
| Right PCom to right PCA P1 | 56 |
| Left PCom to left PCA P1 | 49 |
| Left VA to basilar | 82 |
| Left ASA root to common ASA | 66 |

Together with the parent branch graph, these support the presence of the intended bilateral connections. They do not certify the local lumen shape. The supplied whole-surface geometry report describes one connected component, genus 2 and a watertight surface. That is a topology result, not an anatomical clearance certificate.

## 9. Entirely missing venous and spinal coverage

**DEFERRED:** V01-V06 and S01-S05 are retained for later modules. No venous or complete spinal anatomy is requested in the current batch.

### 9.1 Venous modules

No named veins, venous sinuses or venous meshes exist in this release. The arterial jugular, sigmoid and clival branches are arteries supplying adjacent structures; they must not be mistaken for veins with similar names.

| ID / priority | Missing module and minimum anatomy | Connection requirements | Notes |
| --- | --- | --- | --- |
| **V01 / DEFERRED** | Dural sinus scaffold: SSS, ISS, straight sinus, torcular, paired transverse/sigmoid sinuses, jugular bulbs and IJVs; include occipital/marginal variants deliberately. | ISS and vein of Galen join the straight sinus; the straight sinus and SSS drain towards the torcular/transverse systems; sigmoid continues to jugular bulb/IJV. Use a network rather than an arterial single-parent tree. | pp. 64-68, Figs 2.16-2.17 |
| **V02 / DEFERRED** | Cavernous venous system: cavernous and intercavernous sinuses, SOV/IOV, superior/inferior petrosal sinuses, basilar/clival plexuses, pterygoid plexus and selected emissary channels. | Provide routes to the IJV, transverse/sigmoid junction, pterygoid plexus and contralateral cavernous sinus. Register the ICA and cavernous nerves within the appropriate compartments. | pp. 62-63, 67-68 |
| **V03 / DEFERRED** | Superficial cortical collectors: superficial middle cerebral/Sylvian, Trolard and Labbe, selected superior/inferior cortical and bridging veins. | Represent variable collector dominance and recipient sinuses. Avoid mandatory identical Trolard/Labbe trees on both sides. | pp. 69-70 |
| **V04 / DEFERRED** | Deep system: paired internal cerebral veins, basal veins of Rosenthal, vein of Galen, septal/thalamostriate/choroidal veins and selected medullary/subependymal veins. | Constrain courses with ventricles, corpus callosum, thalamus and midbrain; include basal vein variants and venous circle connections as chosen configurations. | pp. 70-73, Fig. 2.18 |
| **V05 / DEFERRED** | Posterior fossa drainage: petrosal vein complex, lateral mesencephalic, anterior pontomesencephalic/pontine/medullary channels, precentral cerebellar, vermian, hemispheric and tonsillar veins. | Connect the Galenic, petrosal and tentorial/torcular drainage systems and the anterior spinal venous continuation. | pp. 74-76, Fig. 2.19 |
| **V06 / DEFERRED** | Extracranial and craniocervical drainage: facial/deep facial, maxillary/retromandibular, EJV/anterior jugular, suboccipital/vertebral plexuses, condylar/emissary/diploic channels and brachiocephalic veins. | Include anterior condylar confluence, hypoglossal/condylar routes and vertebral venous drainage. Do not simply mirror the artery tree or infer valve behaviour from vessel shape. | pp. 62-63, 67, 69 |

When venous modelling resumes, V01-V02 would support dural AVF and transvenous route teaching; V03-V05 would support AVM drainage and normal cerebral venous interpretation. These are future modules, not current correction priorities.

### 9.2 Spinal modules

The model contains proximal `artery.posterior.anterior_spinal`, bilateral anterior spinal roots and bilateral `posterior_spinal` parts. These are **short proximal representations**. There is no complete spinal vascular system or registered cord.

| ID / priority | Missing anatomy | Required representation | Notes |
| --- | --- | --- | --- |
| **S01 / DEFERRED** | Lateral spinal artery and cervical enlargement artery; fuller cervical segmental/radicular donors. | Distinguish lateral spinal from a generic posterior spinal trunk. Represent its connection to the cervical pial network. Add selected Lazorthes donor anatomy with a declared origin. | pp. 47-49, 77-79, 84-86 |
| **S02 / DEFERRED** | Continuous ASA/PSA axes, vaso corona, radiculomedullary/radiculopial feeders and sulcal/radial branches. | Add a registered spinal cord and nerve roots. Distinguish pure radicular supply, ASA-contributing radiculomedullary supply and pial-contributing radiculopial supply. Include the normal network pattern without imposing a feeder at every level. | pp. 77-88 |
| **S03 / DEFERRED** | Thoracic/lumbar/sacral donors, Adamkiewicz artery, conus basket and filum terminale artery. | Add relevant intercostal, subcostal, lumbar, iliolumbar/lateral sacral/median sacral branches and the selected feeder configuration. Reproduce the hairpin and conus ASA-PSA connections using cord/root context. | pp. 77-80, 83-86, Figs 2.21-2.22 |
| **S04 / DEFERRED** | Intrinsic/extrinsic cord veins, anterior/posterior longitudinal collectors, radicular veins, foraminal and epidural plexuses, basivertebral veins and azygos/ascending lumbar outlets. | Build a venous network with transverse and longitudinal communications and variable transdural exits. Do not assume that a draining vein exits with its feeding artery. | pp. 78, 81, 89-91 |
| **S05 / DEFERRED** | Embryological variants and intrinsic microvascular detail. | Add as separate teaching scenes after the normal spinal scaffolds. Do not encode the inconsistent statements about sulcal anastomoses as hard constraints; see N05. | pp. 82-88 |

## 10. Variants and source statements requiring care

### 10.1 Valid default anatomy and optional variants

The following are absent but are **not errors in a deliberately selected reference configuration**. Their absence only becomes a gap if the atlas is expected to teach variants:

| Region | Optional variants in the notes | Priority |
| --- | --- | --- |
| Arch and neck | Common arch origin, direct arch-origin left VA, aberrant subclavian/right arch patterns, unusual ECA branch trunks or origins. | P3 |
| ICA and orbit | Aberrant ICA, persistent stapedial, persistent hypoglossal/proatlantal/trigeminal arteries, cavernous/dorsal ophthalmic, whole-orbit meningo-ophthalmic supply, MMA from ophthalmic. The otic artery is debated and should not become routine anatomy. | P3 |
| ACA/MCA | Hypoplastic A1, infraoptic/interoptic A1, duplicated/fenestrated ACom, azygos/bihemispheric ACA, absent callosomarginal, accessory/duplicated MCA, MCA trifurcation and division dominance variants. | P3 |
| Posterior circulation | Fetal PCA, PICA-ending VA, extradural PICA, AICA-PICA trunk, absent/duplicated PICA, duplicated SCA, P1-origin SCA, Percheron artery, basilar fenestration/non-fusion and termination variants. | P3 |
| Venous/spinal | Sinus hypoplasia, alternative cortical/deep outflows, persistent falcine channels, ASA-root asymmetry and variable radiculomedullary donors. | Declare the selected baseline; additional scenes P3. |

When adding a variant, alter all dependent vessels and compartments. For example, a whole-orbit meningo-ophthalmic supply variant is not created by adding another large MMA-ophthalmic bridge while leaving a fully normal ICA ophthalmic artery unchanged.

### 10.2 Do not implement these statements literally without clarification

| ID / basis | Statement in the notes | Consequence for modelling |
| --- | --- | --- |
| **N01 / N** | p. 37 states that no vessels supplying parenchyma arise beyond the anterior choroidal plexal point. | This is too absolute. A primary 3D rotational angiography study identified plexal-segment perforators, including courses towards the posterior limb of the internal capsule. Add the plexal landmark, but do not encode it as a universal boundary after which all branches are non-parenchymal. [R3] |
| **N02 / N** | p. 64 says the ISS joins the internal cerebral veins to form the vein of Galen. p. 72 gives the correct downstream arrangement. | For the normal venous scaffold, paired ICVs form Galen; Galen joins ISS at the straight sinus. Avoid creating a false ISS-to-ICV confluence upstream of Galen. [R7] |
| **N03 / N/V** | pp. 16 and 26 use posterior deep temporal for an STA-related vessel and middle deep temporal for the maxillary branch. | Standard anatomical literature also uses anterior/posterior deep temporal for maxillary branches and middle temporal for the STA branch. Current origins therefore need terminology reconciliation, not automatic reversal. Establish the intended naming convention and aliases. [R6] |
| **N04 / N** | p. 57 describes Davidoff-Schechter as arising from PCA near the falcotentorial junction. | The selected usual origin should be P2/proximal ambient territory, with a course to the tentorium/falcotentorial region. A cadaveric study found P2 origins; do not start the vessel at its distal target merely by following the sentence literally. [R5] |
| **N05 / N** | p. 80 describes absence of interlevel sulcal communication, whereas pp. 87-88 and Fig. 2.22 describe longitudinal intrasulcal/intrinsic anastomoses. | Resolve the distinction between ordinary end-arterial functional supply, small anatomical connections and enlargement in shunting disease before designing intrinsic spinal topology. Do not require both absolute absence and extensive normal communication. |
| **N06 / N** | The APA neuromeningeal description includes foramen magnum entry, while the named jugular and hypoglossal divisions have their own foramina. | Model each actual branch passage independently. Do not route both the jugular and hypoglossal arteries through the foramen magnum and then back through their named canals. Distinguish the descending/prevertebral/musculospinal routes. [R2] |
| **N07 / N** | p. 35 places the central retinal origin within the optic canal and implies a fixed ciliary/retinal sequence. | Origin and branch order vary. A primary dissection study found the common CRA origin distal to the orbital end of the canal. Fit a declared reference pattern and optic nerve course, rather than treating the note as a universal canal origin. [R4] |
| **N08 / N** | p. 27 describes the maxillary SOF artery passing through the sphenopalatine foramen. | Review this passage wording before generating coordinates. The sphenopalatine foramen is the nasal entry of the sphenopalatine system; the named SOF connection needs its own route. Do not use a nasal-foramen landmark as proof of the orbital/cavernous passage. |

These are qualifications for building the model. They are not a full editorial or clinical-treatment review of the chapter. Statements about a site being safe to embolise should not become anatomical geometry rules or automatic treatment recommendations in the atlas.

## 11. Implementation order and completion checks

### 11.1 Work packages

| Batch | Work | Completion condition |
| --- | --- | --- |
| **Reassess subsequent ICA shape work** | G01-G03. A01 segment selection is confirmed implemented in v0.7.6. | Preserve the fourteen selectable regions and valid recent refinements; correct only confirmed residual shape discrepancies. |
| **1. ICA origins and existing arterial endpoints** | A15; A04; X01-X05; missing recipient branches; branch naming reconciliation. | ICA ostia agree with the anatomical regions and segment metadata on both sides; anastomoses use correct named endpoints and branch-specific routes. |
| **GUI corrections** | U01-U02; can proceed independently of arterial geometry. | Selection preserves each panel's collapse state, and the inspection title shows the current structure's display name. |
| **2. Dangerous-route completion** | Facial/tympanic arcade, subarcuate, pharyngeal/lacerum and musculospinal-to-VA routes, clival and odontoid networks; missing MHT/ILT/MMA branches. | Selected arterial routes have correct named endpoints and reference-guided courses; cervical donor extensions requiring T03 remain deferred. |
| **3. Intracranial branches and cortical tree** | A06-A14 and P02-P12; P01 anterior meningeal branch; selected X18-X19 networks. | Important named omissions addressed, cortical parent/alias choices declared, representative distal branching refined and segment metadata added. Exact tissue-based validation remains pending. |
| **Deferred modules** | T01-T03; V01-V06; S01-S05; G04-G07 and G11; X12. | No implementation required in the current batch. Reopen when the user resumes these modules. |

The current batches do not require new tissue meshes, venous anatomy, arch/subclavian origins or the complete spinal system. Missing tissue context remains a limit on anatomical course validation, rather than a prerequisite for completing the current branch and endpoint work.

### 11.2 Actual files to change later

- **Catalogue/relationships:** `anatomy/generated/complete_manifest.json` is the source used to build `public/anatomy/manifest.json`. Update the source and regenerate the public manifest rather than editing only the browser copy.
- **Normal vessel geometry:** `public/anatomy/models/complete-circulation.glb`.
- **Potential connection geometry:** `public/anatomy/models/complete-anastomoses.glb`.
- **Bone/dental geometry:** `public/anatomy/models/craniofacial.glb`.
- **Passage/landmark records:** `public/anatomy/landmarks.json` and the corresponding manifest landmark records. These must remain consistent.
- **Data schema/viewer:** add appropriate network semantics, segment ranges and supply relationships only where needed. Do not encode a multi-parent venous or anastomotic network solely through the display hierarchy.

**Authoring inputs were missing from the original v0.7.4 archive.** The later `INR_Segments_Authoring_v0.7.6.zip` provides segment centrelines, radii, baseline metadata and relevant authoring scripts. Use these retained inputs for A15 rather than treating the exported GLB as the only source. Its scripts also refer to other retained authoring stages; recover any required dependencies before running a full rebuild. The app's `build-anatomy.sh` validates and builds manifests; it does not recreate vessel geometry.

**A15 authoring locations:** in the v0.7.6 companion archive, inspect `authoring/anatomy-source/segments/surface-centrelines.json`, `centrelines.json`, `segments.json`, `baseline-manifest.json`, and `authoring/tools/segments/edit_paths.py` / `segment_ica.py`. Propagate changes into the current app's source/public manifests, ICA surface partition and connection assets. Generated parent/segment agreement must be supplemented with the anatomical review in section 5.1.

### 11.3 Acceptance checklist

- [ ] Each work item is recorded as corrected, deliberately deferred or retained as a declared variant.
- [ ] Every added branch has a reviewed parent, ostium, course, compartment, territory and source; no relationship-only branch is counted as mesh-complete.
- [ ] Every potential anastomosis uses anatomically specific endpoint branches. Its route passes through the correct canal/foramen or tissue compartment.
- [ ] ACom, bilateral PCom-PCA, both vertebrobasilar limbs and ASA-root connections remain present after editing.
- [ ] Origin and endpoint changes propagate to the dense paths, final surface, labels, connection overlays and landmarks. Changing a JSON parent alone is insufficient.
- [ ] A15: direct ICA branch ostia and anatomically defined NYU regions agree on both sides, including ophthalmic/superior hypophyseal, PCom and AChA. Segment selection and graph agreement are retained, without using automatically generated boundaries as independent proof of correct origins.
- [ ] A15: the exported model has been compared directly with the supplied Jan Ting diagram for ophthalmic, PCom, AChA and terminal bifurcation relationships; a colour-label match alone is insufficient.
- [ ] A15: ICA curvature, proximal ophthalmic/PCom arcs and junction shape match the illustrated target in corresponding views, without introducing sharp bends or damaging valid distal connections.
- [ ] U01-U02: anatomical selection preserves both panels' collapse state, and the inspection title updates to the selected human-readable structure name even when collapsed.
- [ ] G01-G03 are reassessed against the subsequent ICA work before further deformation. Any remaining ICA/MCA and other junction changes are reviewed in AP, lateral and oblique views with all neighbours visible, and in a common colour to separate shape from label shading.
- [ ] Final geometry has finite coordinates, intended topology, smooth local taper and normals, no unwanted fusion or folding, and retained branch calibre. Bone/tissue relations are checked in the intended compartments.
- [ ] Arterial routes are checked against available references and bone context, with exact pial, ventricular, nerve and cervical tissue relationships explicitly left unvalidated. Registered tissue validation is deferred and does not block this batch.
- [ ] Dural/pial, retinal/orbital, arterial/venous and normal/variant/potential categories are distinguishable.
- [ ] Arterial nerve-supply descriptions are distinct from passage relationships. New nerve meshes and the full structured nerve-supply graph are deferred.
- [ ] Bilateral corrections are reviewed independently. Cross-midline networks are not omitted merely because the vessel assets are duplicated.
- [ ] Human-readable names and relevant aliases are visible to users. Internal IDs remain stable where possible.
- [ ] The normal reference configuration is declared, and optional variants are separate selectable scenes/configurations.
- [ ] Metadata and asset hashes are regenerated, the supplied validator passes, and the final production viewer is inspected. Passing the validator alone is not anatomical sign-off.

## 12. References and reproducibility

### 12.1 Supplied sources

**N:** `nv.pdf`, supplied Chapter 2. Main branch/collateral register reference. All page citations above use printed page numbers. Figures and text were read as anatomical teaching references, not calibrated coordinate or diameter data.

**J:** `ICA_vascular_segments_Jan_Ting.png`, supplied by the user, with artwork credit to Jan Ting. The original image was visually inspected. Explicit visual correction reference for A15 and section 5.1: seven ICA regions, ICA/proximal branch curves, ophthalmic/PCom/AChA origins and the terminal bifurcation. This is a schematic, not patient-derived geometry or a calibrated measurement source.

**M:** INR Anatomy Atlas v0.7.4 supplied archive. Key evidence files: both manifests, the three GLBs, `public/anatomy/landmarks.json`, `docs/ANTERIOR_MODELLING.md`, `docs/POSTERIOR_MODELLING.md`, `docs/ICA_v0.7.2.md`, `docs/REFINEMENT_v0.7.3.md` and the validation reports. Earlier process descriptions are historical: the manifest and exported GLBs determine current presence and connections.

### 12.2 External anatomical checks

- **R1:** Geibprasert S et al. *Dangerous extracranial-intracranial anastomoses and supply to the cranial nerves: vessels the neurointerventionalist needs to know.* AJNR. 2009;30:1459-1468. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7051597/). Used to cross-check route families and branch-specific orbital recipients.
- **R2:** Hacein-Bey L et al. *The ascending pharyngeal artery: branches, anastomoses, and clinical significance.* AJNR. 2002;23:1246-1256. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8185735/). Used to check distinct jugular/hypoglossal, musculospinal, pharyngeal and collateral routes.
- **R3:** Hamasaki T et al. *Variations in the branching patterns of the anterior choroidal artery: an angiographic study with special reference to temporal lobe epilepsy surgery.* Acta Neurochir. 2022. [Publisher abstract](https://link.springer.com/article/10.1007/s00701-022-05294-8), [PubMed](https://pubmed.ncbi.nlm.nih.gov/35789290/). Used to qualify the absolute plexal-point statement.
- **R4:** *Microsurgical anatomy of the central retinal artery.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/17038951/). Used to qualify a fixed intracanalicular CRA origin.
- **R5:** Griessenauer CJ et al. *The artery of Davidoff and Schechter: an anatomical study with neurosurgical case correlates.* Br J Neurosurg. 2013;27:815-818. [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/23705581/). Used to distinguish the P2 origin from the falcotentorial target.
- **R6:** *The arterial supply of the temporalis muscle.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/16703282/); *Arterial branches to the temporal muscle.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/18702239/). Used to check temporal-vessel naming equivalence and avoid erroneous reparenting.
- **R7:** *Anatomical features of the straight sinus and its tributaries.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/1244434/). Used alongside the notes' own p. 72 description to check the ISS-Galen-straight sinus confluence.
- **R8:** Oo EM et al. *Variable Anatomy of the Middle Cerebral Artery from Its Origin to the Edge of the Sylvian Fissure: A Direct Fresh Brain Study.* ScientificWorldJournal. 2021. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7969099/). Used in the cortical-branch follow-up to check variable parietal division origins and distinguish a selected pattern from a universal branching rule.
- **R9:** *Microsurgical Anatomy of the Precuneal Artery: Does It Really Exist? Clarifying an Ambiguous Vessel Under the Microscope.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/29506249/). Used to qualify precuneal/superior internal parietal naming equivalence.
- **R10:** *The microsurgical anatomy of the paracentral lobule artery: a cadaveric series.* [Primary anatomical study, PubMed](https://pubmed.ncbi.nlm.nih.gov/39666091/). Used to confirm variable pericallosal/callosomarginal origins.
- **R11:** Shapiro M, Becske T, Riina HA et al. *Toward an Endovascular Internal Carotid Artery Classification System.* AJNR. 2014;35:230-236. DOI 10.3174/ajnr.A3666. [Primary classification paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7965739/). Used alongside the supplied notes for the adopted seven regions, branch-based distal boundaries and separation from Bouthillier terminology.

### 12.3 Input identifiers

```text
nv.pdf SHA-256
4e64fd6620196358d1452d35195ac94674ad6c3fbbd6575b9c9acf2d01b392d2

inr-anatomy-atlas-v0.7.4(1).zip SHA-256
6cf1ea52110102512ca8e34292719276714cd4ea51a56e4458994e12a2d5202f

Manifest release: 0.7.4
Manifest schemaVersion: 0.3.6
Coordinates: RAS; units: mm

Manifest asset revision prefixes
craniofacial.glb:          8339b8ca742b11268077
complete-circulation.glb: 7e21905cb4f87fadc9be
complete-anastomoses.glb: 30c353b079f11954d7cc
```

**Supplied ICA visual reference:**

```text
ICA_vascular_segments_Jan_Ting.png SHA-256
b984acc1193ab915c5a010b77b6e8a897cb4c59e54f149908154c1ce540f0939
```

**Targeted ICA follow-up inputs:**

```text
inr-anatomy-atlas-v0.7.6.zip SHA-256
0416de3a8a0cf30208350970c1218d9d13803c56692e2db29f9786d12e4bf55e

INR_Segments_Authoring_v0.7.6.zip SHA-256
e0ec84c5a9af4411ce1681914c6de53ddaa4245ab108c11affcbebcc244957e0

Follow-up manifest release: 0.7.6
Classification: Shapiro endovascular ICA regions, 2014
Checked: 14 segment records and 20 direct ICA branch/daughter assignments
```

The baseline anatomical evidence and inventory concern the identified v0.7.4 files. A01/A15 and section 5.1 incorporate a targeted v0.7.6 segment/branch-parent follow-up; the wider newer model has not been re-audited. Recheck affected baseline items if later releases changed their graph or geometry, and apply the current scope statuses before implementing any item.
