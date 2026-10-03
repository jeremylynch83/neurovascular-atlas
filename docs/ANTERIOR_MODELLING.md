# ICA and anterior circulation: Draft 01

This extends the reference reconstruction in RAS millimetres, with the existing right ECA and its original BodyParts3D-derived skull. The separate TopBrain patient is not overlaid without registration. Both ICAs, ACAs and MCAs are represented; detailed ECA branches remain right-sided.

## Source and decision record

- Borden, *3D Angiographic Atlas of Neurovascular Anatomy and Pathology* (2006), chapter 5, printed pp89–93: hierarchy, siphon, ACA and MCA trajectories. Figures 5.1a/b, 5.3, 5.5a and 5.11 were visually inspected in lateral/AP/3D views. The persistent trigeminal artery and aneurysms in examples were excluded. Printed Fischer labels are not equated with Bouthillier C1–C7.
- Kiyosue, *External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment* (2020): existing ECA inputs, orbital/maxillary/ascending pharyngeal pathways, recurrent meningeal and skull-base relations.
- Ferreira et al., *Microsurgical Anatomy of the Anterior Cerebral Circulation: Part 1. The Infraclinoid Internal Carotid Artery*, Barrow Quarterly 18(2), 2002: cervical, petrous, cavernous and clinoid relationships. https://www.barrowneuro.org/for-physicians-researchers/education/grand-rounds-publications-media/barrow-quarterly/volume-18-no-2-2002/microsurgical-anatomy-of-the-anterior-cerebral-circulation-part-1-the-infraclinoid-internal-carotid-artery/
- Geibprasert et al., AJNR 2009;30:1459–1468, doi:10.3174/ajnr.A1500: cross-check of potential orbital, petrous, cavernous, clival and tentorial connections. https://pmc.ncbi.nlm.nih.gov/articles/PMC7051597/

These are reference-guided curves fitted to a different atlas skull. They are not patient segmentation, stereo reconstruction or calibrated measurements. Dense mesh sampling does not confer source-image resolution. Initial courses were manually authored from the references, not extracted automatically from angiographic pixels.

## Represented anatomy

Bilateral common carotid segments, cervical-to-terminal ICA, ophthalmic and selected orbital branches, hypophyseal branches, meningohypophyseal and inferolateral trunks, petrous contributions, PCom and anterior choroidal arteries, A1/pericallosal/callosomarginal ACA branches, a single ACom, M1 and superior/inferior MCA divisions, named cortical branches and selected perforators.

Variant: bilateral MCA bifurcations, paired A2s and pericallosal arteries with a single ACom; no fetal PCA or persistent embryonic carotid–basilar artery. Left courses use a mirrored starting graph with modest specified asymmetry and independent skull fitting. They are not evidence of patient-specific bilateral asymmetry.

PCom endpoints are reserved for the future PCA model. They do not yet complete the posterior circle of Willis. Distal perforators and retinal microvasculature are representative, not exhaustive. No cortical brain, optic nerves, dural rings or cavernous sinus mesh is available in this registered frame, so exact sulcal, cisternal and dural relations remain estimates.

## Potential ECA–ICA pathways

The gold overlay is switched off initially and can be enabled with **Potential ECA–ICA connections**. Each route has two named vessel endpoints and a recorded anatomical route. It is deliberately excluded from the main surface union and its topology tests. Turning it on does not assert that all channels are simultaneously conspicuous or haemodynamically important in one person. Display calibres are illustrative and can exceed the calibre of normally occult anastomoses; they are unsuitable for device sizing or flow simulation.

The overlay includes meningolacrimal/recurrent meningeal, facial–dorsal nasal, STA–supraorbital, infraorbital/deep temporal–orbital, septal–ethmoidal, foramen rotundum/ovale–ILT, cavernous MMA, vidian, tympanic, clival and tentorial routes. This is a selected teaching set, not a complete catalogue of all possible ECA–ICA variants.

## Construction and refinements

1. Preserve the ECA dense paths, 81 surface labels and fixed skull transforms.
2. Author explicit control points, parent attachments, radius profiles, anatomical compartment and source notes. Keep continuous ICA courses through the siphon rather than independent cylinders at segment boundaries.
3. Fit cubic curves and sample by arc length. Reuse transported frames for tube sections.
4. Fit cortical courses inside the cranial surface with a clearance allowance; this is a skull exclusion rule, not a surrogate cortical segmentation. Constrain superficial orbital exits separately.
5. Fit the skull-base ICA with a smooth displacement field. Avoid the earlier failure mode of independently pushing each point, which created kinks. Petrous/tympanic/ethmoidal routes are canal-specific exceptions requiring anatomical review of the coarse skull.
6. Audit all new vessels against the existing ECA. Two first-pass unintended contacts, with the vidian tip and anterior temporal/MMA courses, were identified before finalisation.
7. Union the core circulation with source-face labels retained. Fair only local new junctions and calculate shared normals before splitting into selectable parts. Keep potential anastomoses in a separate asset.
8. Compare actual final triangles with bone, inspect topology, retain reports and produce AP/lateral/skull-base renders. Numerical surface checks do not validate anatomical truth.

## Review priorities

Please review the carotid canal and clinoid relationships first, then the ophthalmic course and ILT/MHT branches. The existing skull has limited small-canal detail; intended intraosseous routes cannot be certified from that mesh. Review distal ACA/MCA curves and branching against brain context when a registered brain model becomes available.

The editable control points, dense results, scripts, input hashes and final checks are retained under `anatomy-source/anterior/`. Copyrighted source pages are not redistributed.
