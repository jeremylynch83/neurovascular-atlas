# Neurovascular Atlas v0.9.124

Corrects bilateral SCA and PCA dural branch routes along the inferior tentorium and their four descriptions. Parent junction coordinates are retained. Existing PCA inlet/hippocampal reference overlap remains open. The eight original schematic collateral overlays are unchanged and require a separate refit. See docs/TENTORIAL_v0.9.124.md.

Mobile header: all controls remain on one top row. The two-line logo is centred and scales to fit. Search collapses to an icon before Layers; tapping it opens a search field below. Layers keeps its label until the narrowest widths. Geometry, DSA data and the v0.9.121 description audit are unchanged.

Adds bilateral posterior inferior ophthalmic vein connections to the superior ophthalmic veins, preserving pterygoid and cavernous junctions. Conservatively softens the left IOV kink. See docs/OPHTHALMIC_v0.9.120.md. This remains a reference teaching reconstruction requiring clinical review.

Lossless vessel index encoding reduces the three vessel files by about 9.3 MB, retaining all source positions, normals, indices, triangle order and repaired geometry exactly. See docs/VESSEL_INDEX_ENCODING_v0.9.119.md. The brain simplification trial from v0.9.118 is retained unchanged.

Experimental brain simplification candidate, based on v0.9.117. See docs/BRAIN_SIMPLIFICATION_v0.9.118.md. Compare with the unchanged v0.9.117 release before adopting this candidate.

The brain file is reduced from 29.1 MB to 26.3 MB by simplifying 29 larger cerebral and cerebellar parcels. All retained vertex positions and normals are copied exactly, with no coordinate rounding or smoothing. The other 164 brain parcels and all four other models remain unchanged. Protected anchor triangles are remapped to their new face IDs. See docs/BRAIN_SIMPLIFICATION_v0.9.118.md for surface measurements and comparison limits.

Bone and arteries load first. Veins and brain load in the background, with loading feedback only in the expanded Layers and anatomy panel. Pending selections show Please wait and run when ready. See docs/STAGED_LOADING_v0.9.116.md. All anatomy is retained from v0.9.115.


Installer-compatible source release with DSA vessel inspection and selectable injection points, the five anatomical bookmarks and one compressed model set.

v0.9.115 removes nine microscopic exact self-contact pairs in the left inferior petrosal wall using three Float32 coordinate corrections, each under 0.000006 mm. Three left-sided pairs remain. Native junctions, all source face indices, stored normals and all other meshes remain exact. Regional petrosal fitting, bone relationships and full receiving lumens remain open.

Place inr-anatomy-atlas-v0.9.124.zip beside your existing inr-anatomy.sh, then run:

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.124.zip
```

This imports the source release, rebuilds Docker locally, verifies v0.9.124 and publishes through your configured GitHub Pages workflow.

The models use meshopt compression, a shared 16-bit position grid and 12-bit octahedral normals. Original coordinates are retained around tiny faces wherever rounding would collapse or reverse them. Vertex and triangle order are preserved. No simplification or anatomical structures removed. The local corrections in v0.9.85 and v0.9.86 use lossless Float32 positions, with no further coordinate quantisation. Surface anchors, coordinates and asset hashes are refreshed. See docs/compression-validation.json for measured displacement and normal error.

Click the detector/vessel icon beside bookmarks to enter DSA mode without changing the view. Choose injection point asks for an artery through search or a click, then a point along its course. The complete arterial tree appears without veins. Change artery appears after vessel selection. Geometry preparation runs in the background and is cached. Bookmarks supply proximal injection defaults. Playback starts at the first opacified 0.5 s frame and loops at 2 frames/s until paused. Standard previous, play, pause and next icons control playback. Click or tap an opacified artery or vein to inspect it and pause the frame. The inspection pane keeps its ordinary position and open/closed state. Rotate to separate overlapping vessels. See docs/DSA_MODE.md for implementation and validation.

Batch 1 anatomy review: all 12 original posterior crossing pairs remain clear. Pericallosal registration and falcine parent interfaces remain open, with current measurements replacing stale warnings. See docs/ANATOMICAL_BATCH1_v0.9.83.md. That review did not change model buffers.

For a local source build, run npm ci and npm run build. For Docker, run ./docker.sh restart.

Jeremy Lynch, Sean McIlhone. See attribution and licence files.

Batch 2: four middle meningeal course specifications are complete. The paired frontal-MMA channels now have named drainage and companion relationships, with matching DSA routing. Canal containment and full drainage continuity remain open. See docs/ANATOMICAL_BATCH2_v0.9.84.md.

Batch 3: twenty local venous labels reviewed and three bounded corrections delivered. The left meningeal/emissary overlap is cleared; both inferior petrosal shafts have small local fit improvements. Regional reconstruction and exact fine containment/continuity remain open. See docs/ANATOMICAL_BATCH3_v0.9.85.md.

Batch 4: a limited straight-sinus shaft/medial dural correction reduces tissue contacts, preserving native venous joins. The larger Galenic refit and remaining G01 tissue/arterial and lumen defects remain open. See docs/ANATOMICAL_BATCH4_v0.9.86.md.

Batch 5: repaired the left A5/falcine native attachment with a rounded native collar. Right ACA and bilateral MMA attachments, pericallosal registration and wider G06 remain open. See docs/ANATOMICAL_BATCH5_v0.9.87.md.

Batch 5 continuation: bilateral MMA paramedian/falcine native joins reconstructed, with clearance from the represented superior sagittal sinus. The right ACA attachment, pericallosal registration and upstream frontal-MMA/paramedian native joins remain open. See docs/ANATOMICAL_BATCH5_CONTINUATION_v0.9.88.md.

Batch 5 further continuation: both upstream frontal-MMA/paramedian openings are repaired. Previous falcine joins and all other native attachments remain fixed. Right ACA attachment, pericallosal registration and whole-network receiving-lumen review remain open. See docs/ANATOMICAL_BATCH5_UPSTREAM_v0.9.89.md.

Native attachment continuation: the left MMA petrosquamosal parent opening now has 124 exact shared coordinates and paired boundary edges. One failed native-interface record is cleared; wider review of the 12 deferred segments remains open. Right ACA outlet trials remain excluded because of cortical registration and deformation failures. See docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.90.md.

The left posterior cavernous MMA parent opening is repaired in v0.9.91 with 181 paired boundary edges. Eight failed native-interface records remained at that checkpoint. See docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.91.md.

Native attachment continuation in v0.9.92 closes four tiny tentorial wall gaps with seven triangles. Both dorsal meningeal native attachments are restored, reducing failed interface records from eight to six. Original positions, triangles and normals remain exact. Right ACA and wider anatomical issues remain open. See docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.92.md.

Batch 1 repair tooling (v0.9.93): reusable cached geometry/BVHs, automatic bounded wall-gap detection, explicit seam alignment, incremental checks and a trial journal. See tools/repair/README.md and docs/REPAIR_PIPELINE_BATCH1_v0.9.93.md. Production anatomy and DSA data are unchanged from v0.9.92.

Native attachment batch 2 (v0.9.94): three small tentorial/MHT wall patches restore both recorded MHT coordinate interfaces. Four native-interface records remained for collar/regional reconstruction in batch 3. See docs/NATIVE_ATTACHMENT_BATCH2_v0.9.94.md.

Native attachment batch 3: reconstruct the left occipital mastoid collar and restore the two compound ILT root joins. Failed native-interface records decrease from four to one. The posteromedial ILT outlet still needs wider distal course/bone registration. See docs/NATIVE_ATTACHMENT_BATCH3_v0.9.95.md.

ACA registration batch 4, v0.9.96: right native A5/falcine attachment repaired, with 32 paired edges. A bounded 2.1 mm connected A5/precuneal shift and 0.25 mm parent-lip setback clear the local outlet. Existing remote cortical embedding and one local source self-intersection pair remain; G05 and full G06 acceptance stay open. See docs/ACA_REGISTRATION_BATCH4_v0.9.96.md.

Galenic junction batch 5, v0.9.97: 61 added wall triangles close 11 small mixed-label native gaps around the Galenic tributaries and torcular/inferior vermian/occipital interfaces. Original vertex positions, normals and faces remain exact. Larger Galenic/cortical and sinus/dural registration remains open. See docs/GALENIC_JUNCTION_BATCH5_v0.9.97.md.

Local venous junction batch 6: see docs/LOCAL_VENOUS_BATCH6_v0.9.98.md.

Integrated venous native junction batch 7: see docs/INTEGRATED_VENOUS_BATCH7_v0.9.99.md.

Arterial native junction batch 8: see docs/ARTERIAL_JUNCTION_BATCH8_v0.9.100.md.

Intersection-classification batch 9: see docs/INTERSECTION_BATCH9_v0.9.101.md.

Exact-zero-area source cleanup batch 10: see docs/ZERO_AREA_BATCH10_v0.9.102.md.

Native port and collinear-wall repair batch 11: see docs/NATIVE_PORT_BATCH11_v0.9.103.md.

Arterial source cleanup batch 12: see docs/ARTERIAL_ZERO_AREA_BATCH12_v0.9.104.md.

Arterial native-port cleanup batch 13: see docs/ARTERIAL_PORT_BATCH13_v0.9.105.md.

Arterial native wall batch 14: see docs/ARTERIAL_WALL_BATCH14_v0.9.106.md.

ACA shaft registration batch 15: see docs/ACA_SHAFT_BATCH15_v0.9.107.md.

ACA shaft registration batch 16: see docs/ACA_SHAFT_BATCH16_v0.9.108.md.

ACA shaft registration batch 17: see docs/ACA_SHAFT_BATCH17_v0.9.109.md.

ACA shaft registration batch 18: see docs/ACA_SHAFT_BATCH18_v0.9.110.md.

ACA distal fit batch 19: see docs/ACA_TAIL_BATCH19_v0.9.111.md.

ACA distal fit batch 20: see docs/ACA_TAIL_BATCH20_v0.9.112.md.

Native wall review batch 21: see docs/ARTERIAL_REVIEW_BATCH21_v0.9.113.md.

Intersection predicate batch 22: see docs/INTERSECTION_PREDICATE_BATCH22_v0.9.114.md.

Petrosal wall cleanup batch 23: see docs/PETROSAL_WALL_BATCH23_v0.9.115.md.
