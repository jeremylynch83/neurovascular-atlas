# Tentorial dural arteries v0.9.124

Corrected the right and left SCA dural branches (Wollschlaeger and Wollschlaeger) and PCA dural branches (Davidoff and Schechter). The SCA branches now approach medially and run beneath the tentorial leaf. The PCA branches pass through the incisural opening and follow the deep posteromedial tentorium towards the falcotentorial region. Their four descriptions now explain the inferior tentorial course and distinguish the usual proximal P2/P1-P2 origin from the falcotentorial destination.

The four native parent junctions retain all 581 original shared coordinate values exactly. Other 1,246 meshes, all parent arteries, brain, bone and venous assets are unchanged. The PCA tube bodies were reconstructed with a retained native inlet collar and an illustrative radius derived from the source profile; this is recorded in their radius policies. Coordinates are exported losslessly. DSA projection recipes and four injection courses were refreshed. All four remain selectable.

## Limits retained explicitly

The original PCA take-off region overlaps the registered hippocampal model. Parent-junction coordinates and brain geometry are held fixed, so a local inlet/brain reference overlap remains. The repair does not certify full brain clearance or clinical anatomical acceptance.

Eight schematic potential collateral overlays remain exactly as delivered in v0.9.123. Their experimental refits were rejected after spatial checks. These overlays are not native joined vessel walls and require a separate refit against the corrected branch routes. Their catalogue relationships are retained and their IDs are listed in the validation report. Failed trial meshes are not installed.

Earlier deferred brain and venous review requirements remain open. Prior source-hash guards have not been promoted to new anatomical approval.

## Validation

- No new self-intersections in the four changed vessel surfaces.
- No changed-route crossings of the tentorium, parent arteries, other native vessels, veins or bone. The remaining registered-brain contact is confined to the PCA inlet reference mismatch described above.
- All 581 parent-junction coordinate values retained exactly; names and anatomical graph unchanged.
- All 1,246 other decoded position/index geometries exact; four other model GLB files byte-identical.
- 828 closed oriented DSA proxies; 579 selectable arterial courses; 2,355 closed flow sections; directed injection, meningeal companion-channel and timing checks passed.
- Production typecheck, build and compression passed. Four changed descriptions have persistent build-time overrides; all their internal links resolve.

Accepted position, index and normal buffers are retained under anatomy/source/tentorial-v0.9.124. The detailed audit is docs/validation/tentorial-v0.9.124.json.

## Sources

- Byrne JV, Garcia M. Tentorial dural fistulas and the medial dural-tentorial branch of the SCA. AJNR 2013. https://doi.org/10.3174/ajnr.A3519
- Griessenauer CJ et al. The artery of Davidoff and Schechter: anatomical study with neurosurgical case correlates. https://pubmed.ncbi.nlm.nih.gov/23705581/
- Bhatia KD et al. Artery of Davidoff and Schechter supply in dural arteriovenous fistulas. https://pmc.ncbi.nlm.nih.gov/articles/PMC7015213/
