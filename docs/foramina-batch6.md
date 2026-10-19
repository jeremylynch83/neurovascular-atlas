# Facial and mandibular passages, batch 6

Release v0.9.139 changes ten bone meshes and twelve arterial display parts, and adds six landmarks. It continues v0.9.138 without changing the application interactions or camera behaviour.

## Delivered geometry

- Bilateral infraorbital grooves continue into enclosed anterior canals and fitted facial exits. The shared corridor clears both the retained artery and vein. Local roof reconstruction closes defects in the orbital floor while the posterior groove stays open superiorly.
- The inferior alveolar canals traverse the mandibular rami and bodies. The revised arterial paths lie below the premolar and canine roots and continue into the mental and incisive divisions. The terminal incisive channels are blind continuations, without an invented obligatory midline exit.
- Mental openings follow the delivered cortical exits. Mylohyoid grooves are separate, open medial sulci; the mylohyoid arteries remain extrabony.
- The right posterior superior alveolar and bilateral principal anterior superior alveolar passages are fitted around their retained arterial routes. The left posterior superior alveolar landmark remains partially fitted. Posterior superior alveolar arterial arrays and native dental branch interfaces remain unchanged.
- A selected bifurcating zygomatic configuration connects orbital entry with malar and temporal outlets. This is an illustrative configuration, not a claim about a universal number of foramina.
- The lacrimal fossa continues into a locally reconstructed bony nasolacrimal corridor towards the inferior meatus. Soft lacrimal drainage structures are not segmented.
- Supraorbital and supratrochlear arterial surfaces are locally fitted around the frontal rim. Notches remain open, without forced complete bony rings.

The new landmark pairs are infraorbital canal, mylohyoid groove and zygomaticoorbital entry. Initial guides are fitted to actual left and right cortical intersections. New canal geometry is reference-guided teaching reconstruction; dimensions are estimates, not patient measurements.

## Verification

The included JSON reports record checks on the delivered decoded assets: artery/vein contacts against all craniofacial bones including teeth; mesh winding and non-manifold edges; perpendicular canal sections; preserved source surface normals on the mandible; exact identity of unaffected mesh arrays and the venous and brain assets; native branch interfaces; potential-link attachments; DSA split closure and safe course ranges. Earlier batch DSA checks are repeated. The production build and archive hashes are checked separately.

The perpendicular section check samples 16 directions at each core station. All 24 sampled stations have bony walls in every direction. This regional sample does not establish whole-model validity or biological wall thickness.

## Remaining limitations

The source incisive arterial surfaces contain small folds. Their material contact regions are retained and recorded, with no new material contact regions introduced by this deformation. The right incisive DSA course retains a short unsafe interval, documented explicitly in the DSA report; injection eligibility continues to respect the runtime safe ranges. This release does not declare that vessel fully validated.

The left supraorbital, both supratrochlear and left posterior superior alveolar markers remain partially fitted and retain that status. Their final cortical fitting review is included in batch 7. Fine dental microchannels, accessory foramina, canalis sinuosus terminal branches and selected variants also remain there. Batch 8 is whole-model validation. Earlier regional repair reports are historical evidence for their own releases.

Unchanged mandibular surface vertices retain their original float32 normals. Only new canal-wall vertices receive newly calculated normals, preserving the previous mandibular shading repair.

## Reference basis

- Orhan et al., infraorbital canal/groove/foramen CBCT study: https://pubmed.ncbi.nlm.nih.gov/26868217/
- Singh, infraorbital foramen dry-skull morphometry: https://pubmed.ncbi.nlm.nih.gov/21519552/
- Mental foramen morphology and morphometry: https://pubmed.ncbi.nlm.nih.gov/26062695/
- Kabak et al., mandibular incisive canal CBCT study: https://pubmed.ncbi.nlm.nih.gov/27837264/
- Kawata et al., zygomatic canals and foramina micro-CT study: https://acbjournal.org/journal/view.html?uid=821&vmd=Full
- Bony nasolacrimal canal CBCT study: https://pmc.ncbi.nlm.nih.gov/articles/PMC11345068/

Citations guide connectivity, relationships and variation. Published population dimensions are not treated as measurements of this model. No paper figures are redistributed.
