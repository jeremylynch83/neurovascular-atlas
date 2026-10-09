# Vessel relationship corrections, v0.9.49

This release corrects the confirmed catalogue mismatch and the main reference-course findings from the v0.9.48 relationship audit. It improves local artery–vein relationships and dural bone apposition while retaining the previous interface, selection halo, skull transparency behaviour, pontine venous rebuild and labial/ICA corrections.

## Corrections

| Finding | Implemented change |
| --- | --- |
| Left mandibular incisive artery linked to the maxillary incisive canal | Removed the incorrect association. Retained the mandibular incisive canal association. The artery remains in the lower jaw. |
| Vertebral venous channel posterolateral to V2 | Rerouted its foraminal segment ventrolaterally, with curved transitions around V2 and fixed suboccipital/deep cervical attachments. Corrected the description of the transverse foraminal canal and upper plexiform organisation. |
| Facial vein too anterior in the lower cheek | Rerouted the facial/deep facial course posterior and lateral to the facial artery. Transported their common junction. Bowed the illustrative transverse facial–facial arterial connection anteriorly to clear the venous crossing, retaining its endpoints. |
| Superficial temporal vein separated from the preauricular artery | Fitted a monotone-height course using the actual bone and arterial surfaces as obstacles, with arterial attraction and fixed drainage/scalp endpoints. This preserves anatomical variation rather than duplicating the arterial path. |
| Hypoglossal arterial branch above the condylar venous region | Lowered its local course towards the anterior condylar corridor. Transported the attached clival/odontoid collars and retained fixed neuromeningeal and posterior attachments. Added the missing hypoglossal passage association. |
| Labyrinthine arteries left below the acoustic region | Reconstructed continuous CPA approaches from their native AICA locations to the internal acoustic region, with cochlear and vestibular branches. Used the modelled brain, bone, arteries and veins as obstacles. |
| Frontal MMA gaps beneath the inner skull | Applied local inner-table fitting, then rebuilt the frontal trunk and anterior division as tubular networks with radius-aware bone clearance. Removed inherited overlapping facets rather than translating them. |
| MMA orbital description and passage association selected different routes | Made the existing Hyrtl meningo-orbital teaching variant explicit and removed its superior orbital fissure association. Separate recurrent meningeal/SOF pathways remain catalogued. The Hyrtl canal itself is not demonstrated in this mesh. |

## Mesh quality and scope

Each acoustic network has three disjoint selectable exterior patches. Each frontal meningeal network has two. The combined exterior of each of these four regional networks is closed and manifold, with no internal junction caps. Individual labels have intentional open interfaces at their shared boundaries. Native parent attachments use continuous solid-volume overlap at the original AICA or middle meningeal location. This does not make the entire atlas a single welded or printable manifold.

The acoustic networks use a 0.06 mm authoring grid; the meningeal networks use 0.14 mm. Source radius estimates are smoothed and bounded because old folded surfaces inflate those estimates. Small acoustic terminal branches use illustrative smaller radii. Retained meshes use local deformations, and their geometric contour-radius changes are recorded. None of these diameters is a calibrated patient measurement.

[Machine-readable validation](validation/relationships-v0.9.49.json) contains baseline and candidate contact comparisons, native interfaces and volume attachments, topology, per-label and combined-network self-intersection tests, exact patch coverage, placement screens, hashes, actual Three.js/Meshopt loading and production build results. Existing wider atlas contacts are retained in the comparison register; the entire head is not certified as intersection-free.

## Unresolved anatomy

The skull does not supply segmented lumens for the internal acoustic, hypoglossal, Vidian, palatovaginal and other small canals, and cervical vertebrae are absent. The provisional supraorbital, ethmoidal, stylomastoid, jugular and palatine measurements were distances to approximate point guides, not independent measurements of canal-centre error. This release annotates that distinction and does not move vessels to those points merely to reduce a screening number.

The new acoustic and hypoglossal courses are reference corrections. Canal containment, nerve relationships and complete cervical plexus/bone fit remain unverified. A hypoglossal arterial collar can overlap the unperforated occipital mesh because its lumen is not represented. The vertebral mesh remains a representative dominant venous channel with a suboccipital plexus, not a complete intraforaminal plexus. Fine companion veins missing from the atlas are still coverage gaps. Wider anatomical review remains pending.

## Final verification

The release changes 26 mesh labels. All 26 final surfaces and all four combined reconstructed networks have zero detected self-intersections. Each regional network is a single closed, consistently oriented manifold with exact, disjoint selectable patch coverage. Retained shared collars have zero positional mismatch, and all four rebuilt native parent attachments pass the solid-volume connection screen. There are no new unexpected contact pairs. A new left hypoglossal collar contact with the unsegmented occipital canal corridor remains explicitly recorded, alongside the expected acoustic label boundary. Existing contact pairs, including changes within their contact regions, remain listed for wider review.

The actual Three.js GLTFLoader and MeshoptDecoder reproduce the exported positions and indices exactly and load unit normals. Untouched labels retain their baseline positions and indices. The skull and brain assets retain their exact v0.9.48 hashes. The catalogue contracts, brain bindings, TypeScript compilation and production build pass.

In the sampled horizontal sections, median superficial temporal artery–vein separation falls from 21.42 to 5.45 mm on the right and 21.65 to 5.19 mm on the left. These are geometric screens of this reference model, not clinical measurements or a universal normal separation.

Matched views: [frontal meningeal](review-renders/meningeal-right-comparison.png), [acoustic](review-renders/acoustic-right-comparison.png), [superficial temporal](review-renders/temporal-right-comparison.png), [facial](review-renders/facial-right-comparison.png) and [vertebral](review-renders/vertebral-comparison.png).

## Reproduction

Use the exact v0.9.48 baseline assets and decode them into a working directory with `tools/decode-posterior-baseline.mjs`. Preserve the baseline GLBs separately. All Python authoring commands below take that working directory as their first argument. The source path records are retained in `anatomy/source/relationships-v0949`.

1. Run `acoustic_path.py` and `temporal_path.py`, or copy the saved path records into the working directory.
2. Run `model.py`, `acoustic_rebuild.py`, then `meningeal_rebuild.py`.
3. Run `validate.py`, `self_check.py`, `metrics.py` and `quality.py`.
4. Run `export.mjs` with candidate and exact baseline GLB directories, then `catalogue.py` and `npm run build`.
5. Run `check_export.mjs` with candidate and baseline decoded directories, then `evidence.py`.

The tools are in `tools/relationships-v0949`. Read the evidence scopes when interpreting the checks. Baseline guides and anatomical source references remain attached to their catalogue entries.

## Anatomical references

- Magro et al. (2015), *Venous organization in the transverse foramen*, DOI [10.3171/2014.10.JNS14906](https://doi.org/10.3171/2014.10.JNS14906).
- Mazzoni et al. (2025), *The vascular anatomy of the internal auditory canal*, DOI [10.14639/0392-100X-A1054](https://doi.org/10.14639/0392-100X-A1054).
- Siwetz et al. (2024), facial arterial and venous relationships, DOI [10.3390/medicina60050805](https://doi.org/10.3390/medicina60050805).
- Eberlová et al. (2020), middle meningeal bony canals and grooves, DOI [10.5603/FM.a2019.0098](https://doi.org/10.5603/FM.a2019.0098).
- Tanoue et al. (2010), craniocervical venous organisation, DOI [10.1259/bjr/85248833](https://doi.org/10.1259/bjr/85248833).
