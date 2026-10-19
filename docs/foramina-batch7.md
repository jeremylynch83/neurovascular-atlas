# Small passages and selected configurations, batch 7

Release v0.9.140 follows v0.9.139. It changes four bone meshes and six arterial display parts. It adds 26 catalogue inventory entries without fabricated coordinates.

## Cribriform region

The source ethmoid and frontal meshes overlapped as solid blocks at the olfactory roof. Drilling small holes in only the ethmoid would have left long blind channels or a frontal obstruction. This release locally reconstructs two olfactory fossae and their thin ethmoid floors, with medial and lateral margins, an underlying olfactory cleft and an anterior communication into the nasal cavity. It does not claim recovery of microscopic source detail.

The selected floor heights are 69.4 mm on the model right and 69.8 mm on the left in atlas coordinates. Vertical plate thickness is 0.95 mm. These are fitted teaching-model dimensions, not patient or published population measurements. The midline crista galli remains above the plates; its protected source vertices are checked for exact position preservation. The surrounding lateral bone and existing ethmoidal arterial routes remain separate.

Each plate has ten short olfactory perforations in a selected, staggered pattern, with radii of 0.28-0.37 mm. Counts and spacing are illustrative. The individual channels open into the subplate cleft and towards the anterior cranial fossa. Olfactory nerve filaments are not segmented, and no existing artery is relabelled as an olfactory filament.

Each of the twenty perforations is checked against all craniofacial bones along its axis, against sixteen perpendicular wall rays, and for communication from beneath the plate into the nasal cavity. The four frontal notches are checked for both bounded and open directions. Direct mesh sections are included in `foramina-batch7-mesh-sections.png`.

## Retained defects resolved

The two incisive arterial surfaces contained folds at distal bends. Only their distal surfaces are reconstructed with smooth 0.48 mm nominal calibre, tapering to the retained terminal territory. The native proximal attachment coordinates are preserved. Their geometry-bound injection guides and derived closed surfaces are rebuilt and checked for full safe DSA ranges. The previously documented right incisive unsafe interval is removed only if the rebuilt delivered geometry passes those checks.

The supratrochlear arterial fits preserve their exact ophthalmic origins and scalp attachments. The left supraorbital and both supratrochlear markers are fitted to actual open frontal-rim notches. The left posterior superior alveolar artery and its anterior division are fitted together; their shared interface and the maxillary origin remain intact. The principal tuberosity opening is fitted to actual cortical intersections. All four partial markers carried from batch 6 become visible following regional checks.

The mandible, mandibular alveolar process, teeth and their shading arrays are unchanged from v0.9.139. Unchanged vertices on the four edited bones retain their original float32 surface normals.

## Fine-canal and variant decisions

`anatomy/source/foramina/small-scope.json` records explicit decisions. New named entries cover the canaliculus innominatus, foramen tympanicum, accessory ethmoidal/mental/infraorbital exits, musculotubal canals, special anterior cribriform openings, persistent midline skull-base canals and named sinus drainage regions.

Unselected accessory and emissary variants retain variant-unresolved status, no coordinates and no asserted patency. Standard microcanals or sinus outlets that cannot be independently established in this coarse source remain explicitly unsegmented. The tympanic and mastoid canaliculi, cochlear and vestibular aqueducts require higher-resolution temporal anatomy. Their unresolved status does not imply biological absence. The grouped olfactory holes are not used to claim the special anterior ethmoidal or cribroethmoidal foramina. The foramen caecum is not converted into an obligatory patent venous channel.

This is a limited educational configuration. Whole-model validation, an integrated residual issue register and review of the remaining scope limitations form batch 8.

## Verification and references

Validation reports accompany the release: vessel-bone contacts including teeth, surface self-contacts at a 0.002 mm tolerance, exact native arterial interfaces, potential-link attachments, DSA split closure and safe ranges, bone topology/components, source-normal preservation, catalogue consistency and exact identity of unaffected geometry. DSA regressions for batches 1-6 and the production build are checked before packaging.

- Patron et al. The forgotten foramina: anterior cribriform plate dissection and histology. https://pubmed.ncbi.nlm.nih.gov/25823692/
- Vasvari et al. Surgical anatomy of the cribriform plate and adjacent areas. https://pubmed.ncbi.nlm.nih.gov/15747213/
- Fallucco et al. Anatomical morphology of the supraorbital notch. https://doi.org/10.1097/PRS.0b013e31826d9c8d
- Ginsberg et al. Skull-base foramina: normal variation on high-resolution CT. https://pubmed.ncbi.nlm.nih.gov/8192074/

These sources guide relationships and variation. Citation only; no paper illustrations are redistributed. Earlier regional reports describe their own releases and remain historical records.
