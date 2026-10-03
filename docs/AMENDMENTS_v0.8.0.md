# Arterial amendments and panel state, v0.8.0

Implements the active arterial and GUI scope of the supplied discrepancy audit. The model remains a bilateral reference reconstruction. The new fine vessels and potential channels have illustrative calibre and regional courses; they are not independent patient segmentations.

## Changes

- 190 additional named arterial branch meshes, giving 575 normal arterial paths and 587 selectable vascular surface parts after ICA segmentation.
- 167 separate potential routes, including branch-specific orbital/ILT endpoints, facial and tympanic arcades, pharyngeal and clival circles, bilateral odontoid links, selected tentorial, pial and choroidal networks.
- A curved paraophthalmic shoulder and posterior return into the communicating/choroidal regions. Ophthalmic, superior hypophyseal and PCom departures are refitted with the ICA. A1/M1 terminal coordinates and distal communicating connections stay fixed.
- Explicit anatomical ICA branch parents. Ophthalmic/superior hypophyseal belong to paraophthalmic, PCom to communicating, AChA to choroidal, terminal perforators and A1/M1 to terminus. MHT and ILT daughters remain under their trunks.
- Provisional ACA, MCA, PICA and PCA segment ranges and regional plexal/loop landmarks. These ranges are metadata, not new tissue-derived anatomical segmentations.
- Collapse state for each panel persists through scene/tree selection and clearing/reselecting. Inspection titles update to the selected display name while collapsed.

## ICA reference comparison

The Jan Ting diagram supplied by the user is the visual target for branch order, regional membership and curved proximal departures. It is not used as a source of millimetre dimensions. The final bilateral lateral and oblique review images use the exported surface and include connected daughter parts, in segment colours and a common colour. The paraophthalmic shoulder has been reshaped without changing the terminal A1/M1 points.

The proximal dural-ring and petrolingual boundaries remain estimated model stations. The PCom transition is at its planned ostial station; the short AChA region surrounds its ostium. An ostial collar can cross a colour boundary. Anatomical parent roles are explicitly assigned rather than inferred from nearest surface labels.

| Side | PCom to AChA centreline arc separation |
| --- | ---: |
| Right | 3.97 mm |
| Left | 4.45 mm |

These are distances in this reference model, not population measurements or a patient-specific lumen measurement.

## Preserved configurations and naming

- Paracentral retains its declared pericallosal origin; anterior parietal retains its declared inferior MCA division origin. Both are selected variable configurations, rather than graph-only reparenting to an illustrated alternative.
- Maxillary posterior deep temporal and STA middle temporal retain their parents, with the Kiyosue naming aliases added. Precuneal/superior internal parietal and splenial/posterior pericallosal aliases are reconciled.
- Stylomastoid remains a posterior auricular child despite its historical ID. Direct APA origin of inferior tympanic is retained.
- The existing ILT posterior part includes the common posterior division and its posterolateral continuation; the added posteromedial ramus leaves that common part. Superior, anteromedial, anterolateral, posteromedial, posterolateral and recurrent lacerum routes are named.
- The small new muscular ophthalmic take-off is distinct from the retinal ostium. No retinal collateral is fabricated. The CRA/ciliary order is not presented as universal.
- AChA plexal entry is a regional estimate, not a universal boundary excluding distal parenchymal supply. Davidoff and Schechter uses a selected proximal P2/ambient origin. Falx cerebri and falx cerebelli routes are separate.

## Checks performed for this geometry update

- Native joined surface: one connected component, genus 2, finite coordinates and a watertight indexed surface before label partition. New incidental contacts were corrected so additions introduce no extra normal arterial loops.
- New branch centreline starts coincide with their intended parent axis. All potential routes have explicit named endpoints, matching relationships and separate exported meshes.
- Existing normal communicating unions are retained. Potential routes are never fused into the normal circulation.
- Meshopt compression round-trips buffer views exactly, without decimation or quantisation. Catalogue asset names and the actual Three.js loader are checked.
- All fourteen ICA regions pass raycaster selection checks. Whole-ICA focus, recursive visibility and segment search pass.
- Actual App/Detail component state checks cover independent collapse state, clear/reselect and collapsed title updates. These are hook-level interaction checks; an end-to-end browser test was not available.
- TypeScript, root deployment build and GitHub Pages subpath build pass. The bone asset is byte-identical to v0.7.6.

Numerical topology does not establish anatomical course or calibre. Earlier very fine exported tip coincidences can still affect position-only weld diagnostics; the topology assertion above applies to the native indexed union before named-part float32 export. No geometry rebuild/check has been added to routine application startup or installation.

## Remaining limits and deferred work

New brain, brainstem, cerebellar, cranial nerve and cervical vertebral meshes; venous modules; arch/subclavian access anatomy; full spinal vascular systems; and their dependent cervical donor extensions remain deferred as requested. This includes T01–T03, V01–V06, S01–S05, G04–G07, G11 and X12, plus the deferred portions of P01 and X11.

G08 remains unresolved where the source skull lacks a resolved small canal lumen. Existing visible bone anchors and regional/unresolved canal estimates retain those distinctions. No new scan or lumen surface was invented. Precise pial, plexal, nerve, ventricular and cervical-level route validation remains pending the deferred tissue registration. The selected distal/choroidal and odontoid networks are represented now with those limitations recorded.

## Audit-item implementation ledger

| Item | Branch meshes | Potential routes | Other changes |
| --- | ---: | ---: | --- |
| A01 | 0 | 0 | Preserved fourteen selectable ICA regions; whole-ICA and segment selection/focus/visibility checked. |
| A02 | 2 | 2 | Reference-guided regional geometry. |
| A03 | 6 | 0 | Reference-guided regional geometry. |
| A04 | 8 | 0 | Existing named part clarified; stable ID preserved. |
| A05 | 20 | 0 | Reference-guided regional geometry. |
| A06 | 10 | 0 | Reference-guided regional geometry. |
| A07 | 4 | 0 | Reference-guided regional geometry. |
| A08 | 7 | 0 | Reference-guided regional geometry. |
| A09 | 4 | 0 | Reference-guided regional geometry. |
| A10 | 0 | 0 | Provisional A2-A5 ranges; declared pericallosal paracentral origin. |
| A11 | 8 | 2 | Aliases/selected configuration recorded. |
| A12 | 0 | 0 | Provisional M2/M3/M4 ranges and retained cortical courses. |
| A13 | 2 | 0 | Aliases/selected configuration recorded. |
| A14 | 16 | 0 | Aliases/selected configuration recorded. |
| A15 | 0 | 0 | Physical OA/PCom take-offs refitted; explicit anatomical parents and ostial segment plan; bilateral surface review. |
| E01 | 4 | 0 | Reference-guided regional geometry. |
| E02 | 6 | 0 | Reference-guided regional geometry. |
| E03 | 8 | 4 | Reference-guided regional geometry. |
| E04 | 6 | 0 | Reference-guided regional geometry. |
| E05 | 8 | 0 | Reference-guided regional geometry. |
| E06 | 2 | 2 | Reference-guided regional geometry. |
| E07 | 0 | 0 | Aliases/selected configuration recorded. |
| E08 | 0 | 2 | Aliases/selected configuration recorded. |
| E09 | 10 | 0 | Reference-guided regional geometry. |
| E10 | 4 | 0 | Reference-guided regional geometry. |
| E11 | 2 | 4 | Reference-guided regional geometry. |
| E12 | 4 | 0 | Reference-guided regional geometry. |
| E13 | 4 | 6 | Reference-guided regional geometry. |
| E14 | 4 | 2 | Reference-guided regional geometry. |
| E15 | 4 | 0 | Reference-guided regional geometry. |
| E16 | 2 | 0 | Reference-guided regional geometry. |
| E17 | 2 | 4 | Aliases/selected configuration recorded. |
| E18 | 2 | 4 | Reference-guided regional geometry. |
| E19 | 4 | 0 | Reference-guided regional geometry. |
| G01 | 0 | 0 | Retained terminal coordinates and lateral M1 course. The ICA/A1/M1 junction is reviewed with all connected arterial labels present. |
| G02 | 0 | 0 | PCom origin and proximal arc refitted with the paraophthalmic shoulder; AChA remains distal to PCom. |
| G03 | 0 | 0 | Ophthalmic origin and proximal arc refitted, with distal orbital course retained. Optic nerve and resolved canal lumen remain unavailable. |
| G08 | 0 | 0 | Preserved existing bone estimates; unresolved canal and dural boundaries remain explicitly unverified. |
| G09 | 0 | 0 | Bilateral reference template declared. |
| G10 | 0 | 0 | Illustrative radius provenance recorded per vessel. |
| P01 | 2 | 0 | Reference-guided regional geometry. |
| P02 | 4 | 0 | Reference-guided regional geometry. |
| P03 | 0 | 0 | Five provisional PICA ranges and regional loop landmark. |
| P04 | 8 | 4 | Reference-guided regional geometry. |
| P05 | 6 | 0 | Reference-guided regional geometry. |
| P06 | 2 | 0 | Reference-guided regional geometry. |
| P07 | 5 | 0 | Reference-guided regional geometry. |
| P08 | 8 | 2 | Reference-guided regional geometry. |
| P09 | 4 | 0 | Reference-guided regional geometry. |
| P10 | 0 | 0 | Provisional P2/P3/P4 ranges. |
| P11 | 6 | 6 | Reference-guided regional geometry. |
| P12 | 0 | 18 | Reference-guided regional geometry. |
| U01 | 0 | 0 | Inspection open state lifted above selection lifecycle; independent from anatomy panel. |
| U02 | 0 | 0 | Selected human-readable name retained as collapsed/open inspection title. |
| X01 | 6 | 8 | Reference-guided regional geometry. |
| X02 | 2 | 2 | Reference-guided regional geometry. |
| X03 | 4 | 2 | Reference-guided regional geometry. |
| X04 | 6 | 4 | Reference-guided regional geometry. |
| X05 | 6 | 6 | Reference-guided regional geometry. |
| X06 | 0 | 2 | Reference-guided regional geometry. |
| X07 | 4 | 10 | Reference-guided regional geometry. |
| X08 | 2 | 2 | Reference-guided regional geometry. |
| X09 | 2 | 4 | Reference-guided regional geometry. |
| X10 | 4 | 2 | Reference-guided regional geometry. |
| X11 | 2 | 2 | Reference-guided regional geometry. |
| X13 | 6 | 10 | Reference-guided regional geometry. |
| X14 | 4 | 8 | Reference-guided regional geometry. |
| X15 | 6 | 10 | Reference-guided regional geometry. |
| X16 | 10 | 6 | Reference-guided regional geometry. |
| X17 | 6 | 8 | Reference-guided regional geometry. |
| X18 | 6 | 6 | Reference-guided regional geometry. |
| X19 | 4 | 18 | Reference-guided regional geometry. |
| X20 | 18 | 22 | Reference-guided regional geometry. |
| X21 | 0 | 7 | Reference-guided regional geometry. |
| X22 | 0 | 4 | Reference-guided regional geometry. |

Counts overlap when an added structure addresses more than one audit item. P03/P10/A12 ranges are provisional metadata, not a claim of tissue-validated segment boundaries. The full machine-readable ledger identifies every branch/route by name.

## Source references

- User-supplied discrepancy audit and Jan Ting ICA segment diagram; Kiyosue chapter/page references are retained in the source audit.
- Shapiro et al. ICA classification: https://pmc.ncbi.nlm.nih.gov/articles/PMC7965739/
- Geibprasert et al. named extracranial–intracranial routes: https://pmc.ncbi.nlm.nih.gov/articles/PMC7051597/
- Hacein-Bey et al. ascending pharyngeal branches: https://pmc.ncbi.nlm.nih.gov/articles/PMC8185735/
- Davidoff–Schechter anatomical study: https://pubmed.ncbi.nlm.nih.gov/23705581/

## Rebuilding and installation

Use the existing permanent `inr-anatomy.sh` with the new release ZIP beside it. The ZIP contains the runnable app, compressed models and GitHub Pages workflow. The installer checks the served manifest version. No new data download is required.

Authoring scripts are supplied separately. The native ICA checkpoint allows branch/network regeneration without rebuilding the older releases. Full ICA reconstruction also references the preserved v0.7.3 refinement inputs, listed by hash in the authoring archive. These modelling scripts are not run during app build or installation.
