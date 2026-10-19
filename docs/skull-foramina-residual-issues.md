# Skull foramina: final residual issue register

Release v0.9.141. All eight planned batches are complete. Whole-model anatomical acceptance remains withheld because the following findings need review. No geometry was moved to make the broad screen pass.

## Priority findings

- Four ICA segment/condylar contact pairs occur at the upper cervical-to-petrous transition. Review the separately modelled condylar surfaces and arterial relationship together. Direct sections are in `foramina-batch8-carotid-condyle-sections.png`.
- The anterior tympanic proximal route still meets jaw/condylar surfaces outside its tested fissure window. This retains the earlier B2-AT-01 limitation.
- Two parietal source meshes have non-manifold edges. 1256 zero-area triangles occur across 35 meshes and require source cleanup rather than an unsupported anatomical reconstruction.
- 5 arteries targeted by the repair programme retain material self-contact findings when their entire surfaces are tested at a 0.002 mm bound, beyond the older local test windows.

## What the counts mean

The whole-delivery screen tested 1005 vascular meshes against represented craniofacial bones, including teeth and hyoid. It found 195 contacting pairs: 114 ordinary arterial pairs, 52 potential-connection pairs and 29 venous pairs. These are surface-screen findings, not 195 proven anatomical errors. Dural apposition and bony grooves need different interpretation from a vessel crossing a solid cortical margin. Contact samples are capped at 250 per pair; neither their counts nor their sampled bounds measure penetration volume.

All 605 DSA projection surfaces and the 848 tested injection split sections are closed. Of the entries, 594 are selectable and 11 remain disabled by the existing runtime data. Eighteen do not have one full-length safe range. The sampled injection gate remained inside declared safe ranges. There are 83 three-station course-probe findings, including 6 with an interior station. Boundary-only findings need cap/tolerance review; interior findings must be reconciled with their stored restricted safe ranges. Closure is not proof of a correct anatomical course.

## Vascular and bone pair inventory

| ID | Priority | Vessel | Bone | Review context |
|---|---|---|---|---|
| B8-C163 | P1 | artery.anterior.internal_carotid_right.segment.cervical | bone.mandibular-condyle-right | carotid-condyle-interface |
| B8-C164 | P1 | artery.anterior.internal_carotid_right.segment.petrous | bone.mandibular-condyle-right | carotid-condyle-interface |
| B8-C165 | P1 | artery.anterior.internal_carotid_left.segment.cervical | bone.mandibular-condyle-left | carotid-condyle-interface |
| B8-C166 | P1 | artery.anterior.internal_carotid_left.segment.petrous | bone.mandibular-condyle-left | carotid-condyle-interface |
| B8-C001 | P2 | artery.connection.mma_lacrimal__meningolacrimal.right | bone.sphenoid | potential-connection |
| B8-C002 | P2 | artery.connection.sta_supraorbital.right | bone.frontal | potential-connection |
| B8-C003 | P2 | artery.connection.accessory_meningeal_ilt.right | bone.sphenoid | potential-connection |
| B8-C004 | P2 | artery.connection.vidian_eca_ica.right | bone.sphenoid | potential-connection |
| B8-C005 | P2 | artery.connection.deep_temporal_lacrimal.right | bone.zygomatic.right | potential-connection |
| B8-C006 | P2 | artery.connection.septal_anterior_ethmoidal.right | bone.ethmoid | potential-connection |
| B8-C007 | P2 | artery.connection.mma_tentorial_marginal.right | bone.temporal.right | potential-connection |
| B8-C008 | P2 | artery.connection.apha_clival_mht.right | bone.sphenoid | potential-connection |
| B8-C009 | P2 | artery.connection.mma_lacrimal__meningolacrimal.left | bone.sphenoid | potential-connection |
| B8-C010 | P2 | artery.connection.sta_supraorbital.left | bone.frontal | potential-connection |
| B8-C011 | P2 | artery.connection.accessory_meningeal_ilt.left | bone.sphenoid | potential-connection |
| B8-C012 | P2 | artery.connection.vidian_eca_ica.left | bone.sphenoid | potential-connection |
| B8-C013 | P2 | artery.connection.deep_temporal_lacrimal.left | bone.zygomatic.left | potential-connection |
| B8-C014 | P2 | artery.connection.septal_anterior_ethmoidal.left | bone.ethmoid | potential-connection |
| B8-C015 | P2 | artery.connection.mma_tentorial_marginal.left | bone.temporal.left | potential-connection |
| B8-C016 | P2 | artery.connection.apha_clival_mht.left | bone.sphenoid | potential-connection |
| B8-C017 | P2 | artery.connection.tubal_pterygovaginal_circle.right | bone.sphenoid | potential-connection |
| B8-C018 | P2 | artery.connection.mandibular_vidian_circle.right | bone.sphenoid | potential-connection |
| B8-C019 | P2 | artery.connection.tubal_maxillary_vidian_circle.right | bone.sphenoid | potential-connection |
| B8-C020 | P2 | artery.connection.clival_posterior_cavernous_mma.right | bone.temporal.right | potential-connection |
| B8-C021 | P2 | artery.connection.lateral_clival_recurrent_ilt.right | bone.sphenoid | potential-connection |
| B8-C022 | P2 | artery.connection.occipital_mastoid_mma_petrosquamosal.right | bone.parietal.right | potential-connection |
| B8-C023 | P2 | artery.connection.mma_tentorial_pca_dural.right | bone.occipital | potential-connection |
| B8-C024 | P2 | artery.connection.transverse_facial_infraorbital.right | bone.zygomatic.right | potential-connection |
| B8-C025 | P2 | artery.connection.posterior_septal_posterior_ethmoidal.right | bone.ethmoid | potential-connection |
| B8-C026 | P2 | artery.connection.septal_palatine_network.right | bone.maxilla.right | potential-connection |
| B8-C027 | P2 | artery.connection.septal_palatine_network.right | bone.maxillary-alveolar-process-right | potential-connection |
| B8-C028 | P2 | artery.connection.sta_occipital_scalp.right | bone.parietal.right | potential-connection |
| B8-C029 | P2 | artery.connection.sta_mma_transosseous_potential.right | bone.parietal.right | potential-connection |
| B8-C030 | P2 | artery.connection.occipital_mma_transosseous_potential.right | bone.parietal.right | potential-connection |
| B8-C031 | P2 | artery.connection.posterior_cavernous_mma_posterolateral_ilt.left | bone.sphenoid | potential-connection |
| B8-C032 | P2 | artery.connection.tubal_accessory_meningeal_circle.left | bone.sphenoid | potential-connection |
| B8-C033 | P2 | artery.connection.tubal_mandibular_ica_circle.left | bone.sphenoid | potential-connection |
| B8-C034 | P2 | artery.connection.tubal_pterygovaginal_circle.left | bone.sphenoid | potential-connection |
| B8-C035 | P2 | artery.connection.mandibular_vidian_circle.left | bone.sphenoid | potential-connection |
| B8-C036 | P2 | artery.connection.tubal_maxillary_vidian_circle.left | bone.sphenoid | potential-connection |
| B8-C037 | P2 | artery.connection.lateral_clival_apa_mht.left | bone.temporal.left | potential-connection |
| B8-C038 | P2 | artery.connection.clival_posterior_cavernous_mma.left | bone.temporal.left | potential-connection |
| B8-C039 | P2 | artery.connection.lateral_clival_recurrent_ilt.left | bone.sphenoid | potential-connection |
| B8-C040 | P2 | artery.connection.anterior_falcine_mma_paramedian.left | bone.frontal | potential-connection |
| B8-C041 | P2 | artery.connection.mma_tentorial_pca_dural.left | bone.occipital | potential-connection |
| B8-C042 | P2 | artery.connection.mma_tentorial_pca_dural.left | bone.parietal.left | potential-connection |
| B8-C043 | P2 | artery.connection.pica_aica_pial_border_zone.left | bone.occipital | potential-connection |
| B8-C044 | P2 | artery.connection.transverse_facial_infraorbital.left | bone.zygomatic.left | potential-connection |
| B8-C045 | P2 | artery.connection.posterior_septal_posterior_ethmoidal.left | bone.ethmoid | potential-connection |
| B8-C046 | P2 | artery.connection.septal_palatine_network.left | bone.maxilla.left | potential-connection |
| B8-C047 | P2 | artery.connection.septal_palatine_network.left | bone.maxillary-alveolar-process-left | potential-connection |
| B8-C048 | P2 | artery.connection.sta_occipital_scalp.left | bone.parietal.left | potential-connection |
| B8-C049 | P2 | artery.connection.sta_mma_transosseous_potential.left | bone.parietal.left | potential-connection |
| B8-C050 | P2 | artery.connection.occipital_mma_transosseous_potential.left | bone.parietal.left | potential-connection |
| B8-C051 | P2 | artery.connection.contralateral_medial_clival.midline | bone.sphenoid | potential-connection |
| B8-C052 | P2 | artery.connection.contralateral_pharyngeal.midline | bone.vomer | potential-connection |
| B8-C053 | P2 | artery.eca.superior_laryngeal.right | bone.hyoid | arterial-bone-interface |
| B8-C054 | P2 | artery.eca.infrahyoid.right | bone.hyoid | arterial-bone-interface |
| B8-C055 | P2 | artery.eca.sublingual.right | bone.mandible | arterial-bone-interface |
| B8-C056 | P2 | artery.eca.ascending_palatine.right | bone.sphenoid | arterial-bone-interface |
| B8-C057 | P2 | artery.eca.occipital_mastoid.right | bone.occipital | arterial-bone-interface |
| B8-C058 | P2 | artery.eca.occipital_mastoid.right | bone.temporal.right | arterial-bone-interface |
| B8-C059 | P2 | artery.eca.superficial_temporal.transverse_facial.right | bone.temporal.right | arterial-bone-interface |
| B8-C060 | P2 | artery.eca.superficial_temporal.transverse_facial.right | bone.zygomatic.right | arterial-bone-interface |
| B8-C061 | P2 | artery.eca.middle_temporal.right | bone.parietal.right | arterial-bone-interface |
| B8-C062 | P2 | artery.eca.middle_temporal.right | bone.temporal.right | arterial-bone-interface |
| B8-C063 | P2 | artery.eca.maxillary.deep_auricular.right | bone.temporal.right | arterial-bone-interface |
| B8-C064 | P2 | artery.eca.maxillary.anterior_tympanic.right | bone.mandible | arterial-bone-interface |
| B8-C065 | P2 | artery.eca.maxillary.anterior_tympanic.right | bone.mandibular-condyle-right | arterial-bone-interface |
| B8-C066 | P2 | artery.eca.anterior_deep_temporal.right | bone.sphenoid | arterial-bone-interface |
| B8-C067 | P2 | artery.eca.pterygoid_muscular.right | bone.sphenoid | arterial-bone-interface |
| B8-C068 | P2 | artery.eca.psa_anterior_division.right | bone.maxilla.right | arterial-bone-interface |
| B8-C069 | P2 | artery.eca.maxillary.accessory_meningeal.right | bone.sphenoid | arterial-bone-interface |
| B8-C070 | P2 | artery.eca.maxillary.mma.right | bone.sphenoid | arterial-bone-interface |
| B8-C071 | P2 | artery.eca.maxillary.mma.frontal.right | bone.frontal | arterial-bone-interface |
| B8-C072 | P2 | artery.eca.maxillary.mma.frontal.right | bone.sphenoid | arterial-bone-interface |
| B8-C073 | P2 | artery.eca.mma_frontal_anterior_division.right | bone.frontal | arterial-bone-interface |
| B8-C074 | P2 | artery.eca.mma_frontal_posterior_division.right | bone.frontal | arterial-bone-interface |
| B8-C075 | P2 | artery.eca.mma_frontal_posterior_division.right | bone.parietal.right | arterial-bone-interface |
| B8-C076 | P2 | artery.eca.maxillary.mma.posterior_convexity.right | bone.sphenoid | arterial-bone-interface |
| B8-C077 | P2 | artery.eca.maxillary.mma.posterior_convexity.right | bone.parietal.right | arterial-bone-interface |
| B8-C078 | P2 | artery.eca.maxillary.mma.posterior_convexity.right | bone.temporal.right | arterial-bone-interface |
| B8-C079 | P2 | artery.eca.mma_parietal_ascending.right | bone.parietal.right | arterial-bone-interface |
| B8-C080 | P2 | artery.eca.mma_posterior_terminal.right | bone.parietal.right | arterial-bone-interface |
| B8-C081 | P2 | artery.eca.maxillary.mma.petrosquamosal.right | bone.occipital | arterial-bone-interface |
| B8-C082 | P2 | artery.eca.maxillary.mma.petrosquamosal.right | bone.parietal.right | arterial-bone-interface |
| B8-C083 | P2 | artery.eca.maxillary.mma.petrosquamosal.right | bone.temporal.right | arterial-bone-interface |
| B8-C084 | P2 | artery.eca.mma_cavernous.right | bone.sphenoid | arterial-bone-interface |
| B8-C085 | P2 | artery.eca.mma_orbital.right | bone.sphenoid | arterial-bone-interface |
| B8-C086 | P2 | artery.eca.superior_pharyngeal.right | bone.palatine.right | arterial-bone-interface |
| B8-C087 | P2 | artery.eca.medial_clival.right | bone.occipital | arterial-bone-interface |
| B8-C088 | P2 | artery.eca.medial_clival.right | bone.sphenoid | arterial-bone-interface |
| B8-C089 | P2 | artery.eca.apa.descending_odontoid.right | bone.occipital | arterial-bone-interface |
| B8-C090 | P2 | artery.eca.lateral_clival.right | bone.temporal.right | arterial-bone-interface |
| B8-C091 | P2 | artery.anterior.vidian_ica_contribution_right | bone.sphenoid | arterial-bone-interface |
| B8-C092 | P2 | artery.anterior.ilt_posterior_branch_left | bone.sphenoid | arterial-bone-interface |
| B8-C093 | P2 | artery.anterior.vidian_ica_contribution_left | bone.sphenoid | arterial-bone-interface |
| B8-C094 | P2 | artery.eca.superior_laryngeal.right.left | bone.hyoid | arterial-bone-interface |
| B8-C095 | P2 | artery.eca.infrahyoid.right.left | bone.hyoid | arterial-bone-interface |
| B8-C096 | P2 | artery.eca.sublingual.right.left | bone.mandible | arterial-bone-interface |
| B8-C097 | P2 | artery.eca.ascending_palatine.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C098 | P2 | artery.eca.superficial_temporal.transverse_facial.right.left | bone.temporal.left | arterial-bone-interface |
| B8-C099 | P2 | artery.eca.superficial_temporal.transverse_facial.right.left | bone.zygomatic.left | arterial-bone-interface |
| B8-C100 | P2 | artery.eca.maxillary.deep_auricular.right.left | bone.temporal.left | arterial-bone-interface |
| B8-C101 | P2 | artery.eca.maxillary.anterior_tympanic.right.left | bone.mandible | arterial-bone-interface |
| B8-C102 | P2 | artery.eca.maxillary.anterior_tympanic.right.left | bone.mandibular-condyle-left | arterial-bone-interface |
| B8-C103 | P2 | artery.eca.anterior_deep_temporal.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C104 | P2 | artery.eca.pterygoid_muscular.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C105 | P2 | artery.eca.maxillary.accessory_meningeal.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C106 | P2 | artery.eca.maxillary.mma.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C107 | P2 | artery.eca.maxillary.mma.frontal.right.left | bone.frontal | arterial-bone-interface |
| B8-C108 | P2 | artery.eca.maxillary.mma.frontal.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C109 | P2 | artery.eca.maxillary.mma.frontal.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C110 | P2 | artery.eca.mma_frontal_anterior_division.right.left | bone.frontal | arterial-bone-interface |
| B8-C111 | P2 | artery.eca.mma_frontal_posterior_division.right.left | bone.frontal | arterial-bone-interface |
| B8-C112 | P2 | artery.eca.mma_frontal_posterior_division.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C113 | P2 | artery.eca.maxillary.mma.posterior_convexity.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C114 | P2 | artery.eca.maxillary.mma.posterior_convexity.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C115 | P2 | artery.eca.maxillary.mma.posterior_convexity.right.left | bone.temporal.left | arterial-bone-interface |
| B8-C116 | P2 | artery.eca.mma_parietal_ascending.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C117 | P2 | artery.eca.mma_posterior_terminal.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C118 | P2 | artery.eca.maxillary.mma.petrosquamosal.right.left | bone.parietal.left | arterial-bone-interface |
| B8-C119 | P2 | artery.eca.maxillary.mma.petrosquamosal.right.left | bone.temporal.left | arterial-bone-interface |
| B8-C120 | P2 | artery.eca.mma_cavernous.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C121 | P2 | artery.eca.mma_orbital.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C122 | P2 | artery.eca.apa.pharyngeal_trunk.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C123 | P2 | artery.eca.superior_pharyngeal.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C124 | P2 | artery.eca.superior_pharyngeal.right.left | bone.vomer | arterial-bone-interface |
| B8-C125 | P2 | artery.eca.superior_pharyngeal.right.left | bone.palatine.left | arterial-bone-interface |
| B8-C126 | P2 | artery.eca.medial_clival.right.left | bone.occipital | arterial-bone-interface |
| B8-C127 | P2 | artery.eca.medial_clival.right.left | bone.sphenoid | arterial-bone-interface |
| B8-C128 | P2 | artery.eca.apa.descending_odontoid.right.left | bone.occipital | arterial-bone-interface |
| B8-C129 | P2 | artery.eca.lateral_clival.right.left | bone.temporal.left | arterial-bone-interface |
| B8-C130 | P2 | artery.amendment.mandibular_ica_branch.right | bone.sphenoid | arterial-bone-interface |
| B8-C131 | P2 | artery.amendment.mandibular_ica_branch.left | bone.sphenoid | arterial-bone-interface |
| B8-C132 | P2 | artery.amendment.medial_clival_mht_branch.right | bone.occipital | arterial-bone-interface |
| B8-C133 | P2 | artery.amendment.medial_clival_mht_branch.left | bone.occipital | arterial-bone-interface |
| B8-C134 | P2 | artery.amendment.lateral_clival_mht_branch.right | bone.temporal.right | arterial-bone-interface |
| B8-C135 | P2 | artery.amendment.lateral_clival_mht_branch.left | bone.temporal.left | arterial-bone-interface |
| B8-C136 | P2 | artery.amendment.ilt_anterolateral_ramus.right | bone.sphenoid | arterial-bone-interface |
| B8-C137 | P2 | artery.amendment.ilt_anterolateral_ramus.left | bone.sphenoid | arterial-bone-interface |
| B8-C138 | P2 | artery.amendment.ilt_posteromedial_ramus.right | bone.sphenoid | arterial-bone-interface |
| B8-C139 | P2 | artery.amendment.ilt_posteromedial_ramus.left | bone.sphenoid | arterial-bone-interface |
| B8-C140 | P2 | artery.amendment.ilt_recurrent_lacerum_ramus.right | bone.sphenoid | arterial-bone-interface |
| B8-C141 | P2 | artery.amendment.ilt_recurrent_lacerum_ramus.left | bone.sphenoid | arterial-bone-interface |
| B8-C142 | P2 | artery.amendment.transverse_facial_superior_division.right | bone.temporal.right | arterial-bone-interface |
| B8-C143 | P2 | artery.amendment.transverse_facial_superior_division.right | bone.zygomatic.right | arterial-bone-interface |
| B8-C144 | P2 | artery.amendment.transverse_facial_superior_division.left | bone.temporal.left | arterial-bone-interface |
| B8-C145 | P2 | artery.amendment.transverse_facial_superior_division.left | bone.zygomatic.left | arterial-bone-interface |
| B8-C146 | P2 | artery.amendment.transverse_facial_inferior_division.right | bone.temporal.right | arterial-bone-interface |
| B8-C147 | P2 | artery.amendment.transverse_facial_inferior_division.right | bone.zygomatic.right | arterial-bone-interface |
| B8-C148 | P2 | artery.amendment.transverse_facial_inferior_division.left | bone.temporal.left | arterial-bone-interface |
| B8-C149 | P2 | artery.amendment.zygomatico_orbital.right | bone.zygomatic.right | arterial-bone-interface |
| B8-C150 | P2 | artery.amendment.zygomatico_orbital.left | bone.zygomatic.left | arterial-bone-interface |
| B8-C151 | P2 | artery.amendment.mma_paramedian.right | bone.frontal | arterial-bone-interface |
| B8-C152 | P2 | artery.amendment.mma_paramedian.left | bone.frontal | arterial-bone-interface |
| B8-C153 | P2 | artery.amendment.superior_pharyngeal_tubal_branch.right | bone.sphenoid | arterial-bone-interface |
| B8-C154 | P2 | artery.amendment.superior_pharyngeal_tubal_branch.left | bone.sphenoid | arterial-bone-interface |
| B8-C155 | P2 | artery.amendment.superior_pharyngeal_carotid_branch.right | bone.sphenoid | arterial-bone-interface |
| B8-C156 | P2 | artery.amendment.superior_pharyngeal_carotid_branch.left | bone.sphenoid | arterial-bone-interface |
| B8-C157 | P2 | artery.amendment.polar_temporal.right | bone.sphenoid | arterial-bone-interface |
| B8-C158 | P2 | artery.amendment.polar_temporal.left | bone.sphenoid | arterial-bone-interface |
| B8-C159 | P2 | artery.amendment.prefrontal_distal_ramus.right | bone.frontal | arterial-bone-interface |
| B8-C160 | P2 | artery.amendment.prefrontal_distal_ramus.left | bone.frontal | arterial-bone-interface |
| B8-C161 | P2 | artery.amendment.precentral_distal_ramus.right | bone.parietal.right | arterial-bone-interface |
| B8-C162 | P2 | artery.amendment.precentral_distal_ramus.left | bone.parietal.left | arterial-bone-interface |
| B8-C167 | P2 | vein.sigmoid.right | bone.temporal.right | venous-bone-interface |
| B8-C168 | P2 | vein.superior_petrosal.right | bone.temporal.right | venous-bone-interface |
| B8-C169 | P2 | vein.inferior_petrosal.right | bone.occipital | venous-bone-interface |
| B8-C170 | P2 | vein.inferior_petrosal.right | bone.temporal.right | venous-bone-interface |
| B8-C171 | P2 | vein.sphenoparietal.right | bone.sphenoid | venous-bone-interface |
| B8-C172 | P2 | vein.superior_petrosal_vein.right | bone.temporal.right | venous-bone-interface |
| B8-C173 | P2 | vein.superior_petrosal.left | bone.temporal.left | venous-bone-interface |
| B8-C174 | P2 | vein.inferior_petrosal.left | bone.occipital | venous-bone-interface |
| B8-C175 | P2 | vein.inferior_petrosal.left | bone.temporal.left | venous-bone-interface |
| B8-C176 | P2 | vein.sphenoparietal.left | bone.sphenoid | venous-bone-interface |
| B8-C177 | P2 | vein.superior_petrosal_vein.left | bone.temporal.left | venous-bone-interface |
| B8-C178 | P2 | vein.maxillary.left | bone.mandible | venous-bone-interface |
| B8-C179 | P2 | vein.deep_facial.left | bone.mandible | venous-bone-interface |
| B8-C180 | P2 | vein.posterior_intercavernous | bone.sphenoid | venous-bone-interface |
| B8-C181 | P2 | vein.basilar_plexus | bone.occipital | venous-bone-interface |
| B8-C182 | P2 | vein.basilar_plexus | bone.sphenoid | venous-bone-interface |
| B8-C183 | P2 | vein.basilar_plexus | bone.temporal.right | venous-bone-interface |
| B8-C184 | P2 | vein.inferior_alveolar.right | bone.mandible | venous-bone-interface |
| B8-C185 | P2 | vein.inferior_alveolar.left | bone.mandible | venous-bone-interface |
| B8-C186 | P2 | vein.middle_meningeal.anterior.left | bone.frontal | venous-bone-interface |
| B8-C187 | P2 | vein.middle_meningeal.anterior.left | bone.sphenoid | venous-bone-interface |
| B8-C188 | P2 | vein.middle_meningeal.anterior.left | bone.parietal.left | venous-bone-interface |
| B8-C189 | P2 | vein.middle_meningeal.anterior.right | bone.frontal | venous-bone-interface |
| B8-C190 | P2 | vein.middle_meningeal.anterior.right | bone.sphenoid | venous-bone-interface |
| B8-C191 | P2 | vein.middle_meningeal.posterior.left | bone.frontal | venous-bone-interface |
| B8-C192 | P2 | vein.middle_meningeal.posterior.left | bone.sphenoid | venous-bone-interface |
| B8-C193 | P2 | vein.middle_meningeal.posterior.left | bone.parietal.left | venous-bone-interface |
| B8-C194 | P2 | vein.middle_meningeal.posterior.right | bone.frontal | venous-bone-interface |
| B8-C195 | P2 | vein.middle_meningeal.posterior.right | bone.sphenoid | venous-bone-interface |

## Residual whole-surface self contacts

| Artery | Material face pairs | Maximum plane-crossing bound (mm) |
|---|---:|---:|
| artery.anterior.internal_carotid_right.segment.cervical | 8 | 0.031747 |
| artery.eca.maxillary.descending_palatine.right | 4 | 0.010479 |
| artery.eca.maxillary.descending_palatine.right.left | 9 | 0.012521 |
| artery.eca.maxillary.right | 579 | 0.110152 |
| artery.eca.maxillary.right.left | 572 | 0.112877 |

These bounds are geometric screens, not a measured tissue-penetration depth. The final release preserves the baseline geometry exactly. Full per-finding bounds, restricted DSA ranges and unsegmented/variant inventory are in `skull-foramina-residual-issues.json`. Fine temporal canals, individual sinus outlets and unselected accessory/emissary variants remain explicitly unmodelled where source detail is insufficient.
