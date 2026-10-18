# Deferred anatomical issues

These segments remain under anatomical review. Geometry retains the .67 checkpoint plus documented local corrections through v0.9.115. The left MMA petrosquamosal parent interface is repaired; broader acceptance of the 12-segment cohort remains open. The list covers three active networks; it is not a whole-atlas certification.

| Network | Vessel segment | Recorded issue |
|---|---|---|
| left-tentorial-mastoid | MMA–tentorial marginal left | Crosses bone.temporal.left (79 contacted facets). |
| left-tentorial-mastoid | Tentorial marginal left | Recorded dorsal meningeal and MHT native-coordinate attachments restored through v0.9.94. Wider route/receiving-lumen review remains open. |
| left-tentorial-mastoid | MMA petrosquamosal left | Parent opening repaired in v0.9.90: 124 exact coordinates and paired edges. Wider compartment and receiving-network review remain open. |
| left-tentorial-mastoid | Occipital mastoid–MMA petrosquamosal left | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-tentorial-mastoid | Occipital mastoid dural branch left | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-tentorial-mastoid | Occipital mastoid left | Native collar repaired in v0.9.95: 108 exact shared coordinates and paired edges. Wider regional review remains open. |
| right-tentorial | MMA–tentorial marginal right | Crosses bone.temporal.right (132 contacted facets). |
| right-tentorial | Tentorial marginal right | Recorded dorsal meningeal and MHT native-coordinate attachments restored through v0.9.94. Wider route/receiving-lumen review remains open. |
| right-tentorial | MMA petrosquamosal | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-posterior-cavernous | Posterior cavernous MMA–posterolateral ILT left | Crosses bone.sphenoid (68 contacted facets). |
| left-posterior-cavernous | MMA posterior cavernous left | Parent opening repaired in v0.9.91: 181 exact shared coordinates and paired edges after local exterior union. Wider compartment and receiving-network review remains open. |
| left-posterior-cavernous | ILT posterior branch left | Compound root repaired in v0.9.95: 64 anterior-branch and 69 trunk coordinates. Posteromedial native interface remains displaced (88 source port coordinates); wider distal course/bone registration is required. |

Facet and vertex counts are geometric measurements, not numbers of separate anatomical defects. Wider route feasibility, independent anatomical support and bone clearance remain open. Native-interface progress is tracked separately below.

Batch 1 review (v0.9.83) is recorded in [ANATOMICAL_BATCH1_v0.9.83.md](docs/ANATOMICAL_BATCH1_v0.9.83.md) and its [measurements](docs/validation/batch1-v0.9.83.json).

- G02: all 12 original posterior crossing pairs remain free of surface intersections. Limited basilar/APMV depth checks agree with the expected relationship. Wider anatomical acceptance remains incomplete.
- G05 remains open, including bilateral A5: current A2–A5 meshes contact registered brain surfaces. Adjacent segment seam coordinates still match; later generic callosal-repair wording did not establish accepted pial placement.
- G06: general ethmoidal/pericallosal origin support reviewed. ACA falcine and MMA falcine terminal native parent interfaces remain unresolved. Catalogue parents are retained provisionally, and potential anastomoses are not certified open lumens.
- Whole-atlas physical continuity and independent anatomical support remain open.

App integration has separate checks in docs/dsa-selector-validation.json. Passing app checks do not establish anatomical acceptance.

## Middle meningeal course review, v0.9.84 (G07)

All four previously missing course specifications are now authored and exported. There are no remaining course-specification exemptions. The labels describe a pair beside the frontal MMA corridor on each side, not anterior and posterior arterial territories.

Current geometry checks find no neural/arterial intersections or self-intersections in these four surfaces. Common exterior seams connect them with the represented lesser-wing receiver. Catalogue drainage and DSA mapping now agree with this regional configuration.

Remaining issues are exact dural/bony-groove and spinosum containment, capped cranial/caudal endpoints and incomplete receiver closure. The left anterior companion/emissary contact was subsequently cleared in v0.9.85. These are retained for local venous fitting and continuity review, rather than counted as missing specifications. See [batch 2 review](docs/ANATOMICAL_BATCH2_v0.9.84.md) and [measurements](docs/validation/meningeal-v0.9.84.json).

## Local venous fitting, v0.9.85 (G08)

Twenty labels reviewed; three bounded corrections delivered. The left anterior meningeal/emissary overlap is cleared. Both inferior petrosal shafts have small local bone-fit improvements, with native boundaries fixed. Larger trials failed the deformation limit and were excluded.

Superior petrosal reconstruction, inferior petrosal open walls and existing self-intersections, detailed vertebral/canal/nerve/globe containment, and continuous receiving lumens remain open. No missing targets or branches were invented. See [batch 3](docs/ANATOMICAL_BATCH3_v0.9.85.md) and [measurements](docs/validation/local-veins-v0.9.85.json).

## Falcotentorial/Galenic review, v0.9.86 (G01)

A limited 1.5 mm straight-sinus shaft and adjoining dural correction reduces tissue-contact counts, with native venous interfaces fixed. G01 remains open: all four audited sinus/cortical contact pairs, Galenic/splenial registration, posterior arterial contacts and full native lumen closure remain unresolved. Broader Galenic and falx-body trials failed regression checks and are excluded. No whole-region acceptance is claimed. See [batch 4](docs/ANATOMICAL_BATCH4_v0.9.86.md) and [measurements](docs/validation/falcotentorial-v0.9.86.json).

## Native falcine attachment correction, v0.9.87 (G06)

The left A5/falcine native rim is now connected. A5, the original distal falcine surface and its anastomotic interface remain fixed. Right ACA and both MMA parent attachments remain unresolved. G05 pericallosal registration remains open. Failed wider trials are excluded. See [batch 5](docs/ANATOMICAL_BATCH5_v0.9.87.md).

## Bilateral MMA falcine joins, v0.9.88 (G06 continuation)

Both terminal/paramedian native interfaces are repaired, and the four revised surfaces clear the superior sagittal sinus model. Each paramedian mesh stays connected from its retained incoming rim to the new terminal join. Its upstream frontal-MMA rim remains unmatched, as before; whole-network lumen continuity is not certified. Right ACA attachment and G05 remain open. See [continued batch 5](docs/ANATOMICAL_BATCH5_CONTINUATION_v0.9.88.md).

## Upstream MMA openings, v0.9.89 (G06 continuation)

Both frontal-MMA/paramedian native junctions now have open shared interfaces. Parent distal tips, proximal rims, anterior-division seams and the v0.9.88 distal falcine joins remain fixed. Local changes fit within the original combined vessel envelopes, allowing negligible Float32 rounding. Existing bone contact, exact dural containment, right ACA attachment, G05 pericallosal registration and full distal receiving-lumen review remain open. Facet counts change with local triangulation and do not measure new anatomical penetration. See [upstream continuation](docs/ANATOMICAL_BATCH5_UPSTREAM_v0.9.89.md).

## Petrosquamosal native interface and right ACA feasibility, v0.9.90

The left MMA petrosquamosal parent opening is repaired locally. Failed native-interface records in the deferred cohort decrease from 10 to 9, while wider review of all 12 segments remains open. The right ACA port lies inside the registered cingulate cortical surface; tested local outlet shortening fails the deformation or clearance gates and is excluded. Right ACA and G05 require wider registration work. See [continuation](docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.90.md).

## Cavernous native junction, v0.9.91

The left posterior cavernous MMA parent opening is repaired locally. Failed native-interface records decrease from 9 to 8; wider review of all 12 deferred segments remains open. The parent moves by at most 0.15 mm. Signed-depth sampling shows no new inside samples or deeper bone penetration. Source bone contacts remain, and retessellated facet counts do not certify bone clearance. The proximal route clears the ovale emissary vein; all other attachment coordinates and source corner normals are retained. See [continuation](docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.91.md).

## Tentorial native wall gaps, v0.9.92

Seven added triangles close four small wall gaps without moving any source vertex or changing any source face or normal. Both dorsal meningeal attachments regain all recorded native coordinates. Two of the three missing right meningohypophyseal interface coordinates are restored, leaving one missing there. Failed native-interface records decrease from eight to six; all 12 segments remain under wider review. Right ACA, pericallosal registration, bone/dural fit and full receiving lumens remain open. See [continuation](docs/NATIVE_ATTACHMENT_CONTINUATION_v0.9.92.md).

## Native attachment batch 2, v0.9.94

The three remaining small tentorial/MHT gaps are patched: two left and one right. All 13 left and 10 right recorded MHT native coordinates are now present. Original positions, normals and triangles remain exact. Failed native-interface records decrease from six to four. The left occipital mastoid opening requires proximal cap/collar reconstruction; the three left ILT interfaces require coupled collector reconstruction. Bounded snap trials were excluded and are documented for batch 3. All 12 segments remain under wider anatomical review. See [batch 2](docs/NATIVE_ATTACHMENT_BATCH2_v0.9.94.md).

## Native attachment batch 3, v0.9.95

The left occipital mastoid collar now has 108 exact paired native edges. The left ILT compound root matches all 64 anterior-branch and 69 trunk coordinates. Failed native-interface records decrease from four to one. The posteromedial outlet remains displaced: broader trials fold or cross the current sphenoid model, and all 141 protected distal attachment coordinates lie inside that model. Wider distal course/bone registration and independent canal support are required. All 12 deferred segments retain wider anatomical review. See [batch 3](docs/NATIVE_ATTACHMENT_BATCH3_v0.9.95.md).

## ACA registration batch 4, v0.9.96

The right A5/falcine native attachment is repaired with 32 paired edges. A bounded connected 2.1 mm medial adjustment and 5 mm geodesic precuneal taper reduce existing cortical embedding. The malformed parent lip is set back by 0.25 mm; all other original native joins remain fixed or mapped identically in both labels. Two of three historically reported local self-intersection pairs were removed. The remaining recorded pair is reclassified as a shared-vertex false positive in v0.9.101 using exact coordinates; see batch 9 below. The broader bilateral A2-A5 registration, residual cortical embedding and full G06 receiving-lumen continuity remain open. The separate 12-segment cohort still has one recorded ILT interface defect. See [batch 4](docs/ACA_REGISTRATION_BATCH4_v0.9.96.md).

## Galenic and torcular native wall gaps, v0.9.97

Eleven small mixed-label gaps are closed with 61 wall triangles, using existing atlas coordinates. All original positions, normals and faces remain exact. The separate basal/Galen gap inside the corpus callosum is excluded, as are crossing/degenerate local alternatives. The wider Galenic/cortical and sinus/dural registration, remote non-manifold edges, disconnected torcular component and full receiving lumens remain unresolved. The 12-segment arterial cohort still has one ILT interface defect. See [batch 5](docs/GALENIC_JUNCTION_BATCH5_v0.9.97.md).

## Local venous junction batch 6, v0.9.98

One native wall gap at the left inferior petrosal sinus/basilar plexus interface is closed with three triangles and existing atlas coordinates. Every original position, normal and face remains exact. The regional petrosal open walls, components, old bad edges, self-intersections and tissue contacts remain unresolved. Closed companion meshes have not been certified as connected receiving lumens. The larger/bad-edge cavernous/sphenoparietal boundary is excluded. See [batch 6](docs/LOCAL_VENOUS_BATCH6_v0.9.98.md).

## Integrated venous junction batch 7, v0.9.99

The scan covers all 231 venous meshes. 39 small mixed-label wall gaps are closed with 76 triangles across 14 labels, with all source positions, normals and faces retained. Only passing local candidates are installed. Single-label ports, bad-edge components, larger gaps, tissue-embedded patches and crossing alternatives are excluded. Remote topology defects, regional petrosal/Galenic/cortical/dural registration, full receiving lumens, canal targets and the separate ILT interface remain open. See [batch 7](docs/INTEGRATED_VENOUS_BATCH7_v0.9.99.md).

## Arterial junction batch 8, v0.9.100

The scan covers all 766 arterial meshes. 15 small mixed-label wall gaps are closed with 53 triangles across 5 labels, with all source positions, normals and faces retained. Only passing local candidates are installed, with every appended edge checked against all 766 arterial meshes. Single-label ports, bad-edge components, larger gaps, tissue-embedded patches and crossing alternatives are excluded. Remote topology defects, regional petrosal/Galenic/cortical/dural registration, full receiving lumens, canal targets and the separate ILT interface remain open. See [batch 8](docs/ARTERIAL_JUNCTION_BATCH8_v0.9.100.md).

## Intersection classification batch 9, v0.9.101

The single recorded residual right A5 pair (faces 5129/5204) meets only at a shared vertex. A near-parallel tolerance cut had incorrectly expanded that point into an overlap interval. Exact binary-coordinate half-space and interval checks clear this flag; an exact local audit of 323 pairs finds no positive crossing. All geometry remains unchanged. This corrects a numerical finding and does not resolve G05 cortical/pericallosal registration, G06 full receiving lumens, other regional defects or the separate ILT interface. See [batch 9](docs/INTERSECTION_BATCH9_v0.9.101.md).

## Exact-zero-area source cleanup batch 10, v0.9.102

Twenty-one exact-zero-area triangles are removed from the anterior spinal vein, left inferior ophthalmic vein and bilateral pterygoid plexus. Twenty-three invalid native edges are cleared; affected global bad edges fall from 26 to 3. No new boundary or bad edge is introduced. All vertices, normals and positive-area source faces remain exact. Two anterior spinal and one left pterygoid zero-area face remain because their removal would expose new boundaries. Regional registration, receiving lumens and the separate ILT interface remain open. See [batch 10](docs/ZERO_AREA_BATCH10_v0.9.102.md).

## Native port and collinear-wall repair batch 11, v0.9.103

The three guarded zero-area faces from batch 10 are resolved. Removing the two anterior spinal degenerates exposes two per-label port edges which pair exactly and oppositely with the anterior medullary vein; no global boundary is added. A left pterygoid collinear sliver is removed by merging two tiny coplanar wall triangles into their exact union. Global affected bad edges fall from three to zero. All vertex positions and stored normals remain exact. Larger registration, full receiving lumens, remote bad edges and the separate ILT interface remain open. See [batch 11](docs/NATIVE_PORT_BATCH11_v0.9.103.md).

## Arterial exact-zero-area cleanup batch 12, v0.9.104

The scan finds 453 exact-zero-area triangles across 100 arterial meshes. Of these, 384 are removed across 86 labels after local/global topology checks; 69 remain guarded. Affected global bad edges fall from 483 to 88, clearing 395 invalid edges without new boundaries. All original positive-area faces, positions and stored normals remain exact. This does not close the larger anatomical registration, full receiving-lumen or ILT interface findings. See [batch 12](docs/ARTERIAL_ZERO_AREA_BATCH12_v0.9.104.md).

## Arterial native-port cleanup batch 13, v0.9.105

Fifty-nine guarded zero-area triangles are removed across 29 arterial labels after exact subset search and native-port validation. Newly exposed per-label edges each pair oppositely with a retained positive-area wall edge from a different artery label. Affected global bad edges decrease from 85 to 11, with no new global boundary or bad edge. All positive-area source faces, positions and stored normals remain exact. Ten guarded zero-area faces, wider registration and receiving-lumen findings, and the separate ILT interface remain open. See [batch 13](docs/ARTERIAL_PORT_BATCH13_v0.9.105.md).

## Arterial native wall batch 14, v0.9.106

The right lacrimal wall is subdivided exactly at the existing lateral superior palpebral junction vertex, replacing a zero-area line facet without changing wall shape or area. A small left PICA medullary/posterior spinal native wall gap is closed with seven triangles and one copied native coordinate/normal. Three zero-area faces, three bad coordinate edges and seven global boundary edges are cleared, with no new global boundary or bad edge. Seven guarded zero-area faces remain.

A left PICA vermian subdivision trial is excluded because source faces 7390 and 7392 have a genuine pre-existing positive wall crossing, confirmed by exact binary-coordinate arithmetic. The original production mesh is retained. ACom gap trials fail projected-polygon triangulation and remain excluded. Regional registration, receiving lumens and the separate ILT interface stay open. See [batch 14](docs/ARTERIAL_WALL_BATCH14_v0.9.106.md).

## Right A4 shaft registration batch 15, v0.9.107

A bounded right A4 mid-shaft shear moves 1,647 existing vertices by at most 2.508 mm while retaining every source face index and all four native interfaces (324 shared coordinates). The central fitted section maximum sampled depth falls from 1.69 to 0.17 mm. Across the complete changed region, depth falls from 1.72 to 1.34 mm, with no new sampled entry or additional depth. Residual right A4 cortical embedding remains. Broad A2 and connected A4-A5 trials fail tissue or branch-shape gates and are excluded. Bilateral A2, left ACA, distal ACA/callosal fit, full receiving lumens and wider G05/G06 remain open. See [batch 15](docs/ACA_SHAFT_BATCH15_v0.9.107.md).

## Left A4 anterior shaft registration batch 16, v0.9.108

A bounded anterior shaft shear moves 896 existing vertices by at most 2.693 mm, retaining all 8,445 source triangles and all four native interfaces (323 shared coordinates). Central plateau sampled depth falls from 1.227 mm to zero. Changed-region inside samples fall from 10,574 to 5,377, with no new sampled entry or additional depth. The worst residual changed-region depth remains 2.522 mm. All other meshes, including the right A4 fit, stay exact. Wider G05/G06 and the ILT interface remain open. See [batch 16](docs/ACA_SHAFT_BATCH16_v0.9.108.md).

## Bilateral A5 shaft registration batch 17, v0.9.109

Two bounded inter-junction shaft shears preserve all source vertices and triangles, all ten native interfaces (980 shared coordinates), both A4 fits and the repaired falcine roots. Central plateau sampled depth falls from 0.244 mm left and 0.405 mm right to zero, with no new sampled tissue entry or extra depth. Residual transition and proximal/distal cortical embedding remain. Wider G05/G06 and the separate ILT native interface remain open. See [batch 17](docs/ACA_SHAFT_BATCH17_v0.9.109.md).

## Bilateral anterior A4 shaft registration batch 18, v0.9.110

Two bounded anterior A4 shaft shears preserve all source vertices and triangles, all eight native interfaces (647 shared coordinates), earlier A4 fit regions, both A5 fits and the repaired falcine roots. Central plateau sampled depth falls from 2.116 to 0.547 mm left and 1.638 to 0.091 mm right, with no new sampled tissue entry or extra depth. Residual transition and proximal/distal cortical embedding remain. Wider G05/G06 and the separate ILT native interface remain open. See [batch 18](docs/ACA_SHAFT_BATCH18_v0.9.110.md).

## Distal right A5 fit batch 19, v0.9.111

A bounded 1 mm medial fit beyond the last native branch junction moves 408 existing vertices and retains all 8,172 source triangles, all five native interfaces (456 shared coordinates), earlier A5 fit regions and all other meshes. The right A5 is continuously separated from the right posterior dorsal and posteroventral cingulate surfaces, with complete wall coverage. The recorded maximum sampled depths of 0.255 and 0.932 mm fall to zero. Right middle-posterior cingulate embedding, other ACA/cortical registration and wider G05/G06 remain open. See [batch 19](docs/ACA_TAIL_BATCH19_v0.9.111.md).

## Distal left A5 shaft fit batch 20, v0.9.112

A bounded 0.707107 mm outward/superior fit moves 463 existing vertices and affects 998 source triangles. All 8,424 face indices, five native interfaces (524 shared coordinates), previous fit regions, terminal tip and all other meshes remain exact. Sampled corpus-callosum depth falls from 0.255 to 0.195 mm; continuous separation is certified for 1,209 distal wall triangles with source Y <= -95.1 mm. The transition/attachment overlap and one rigidly retained native self-contact pair remain unresolved. Wider G05/G06 and other regional findings remain open. See [batch 20](docs/ACA_TAIL_BATCH20_v0.9.112.md).

## Native arterial wall review batch 21, v0.9.113

No new geometry is installed. The 132 boundary-only SCA/Wollschlaeger closures and 4,620 examined local retriangulations fail retained-wall contact checks. Across 23 other surviving small mixed-label loops, 637 boundary-only triangulations are screened; the 13 loops with surface-clear options have native rim vertices inside registered olfactory or gyrus rectus tissue. These recorded local methods are deferred. Wider receiving-wall reconstruction or coordinated vessel/cortex registration remains necessary. This review does not prove that other repair methods cannot succeed. See [batch 21](docs/ARTERIAL_REVIEW_BATCH21_v0.9.113.md) and the source-hash guard in tools/arterial-review-v0.9.113.

## Intersection predicate batch 22, v0.9.114

The authoring validator previously reported 33 bilateral inferior petrosal contact pairs. Exact coordinate checks reject 11 false positives and retain 22 true cases (12 left, 10 right), including adjacent faces. These counts use a different definition from older non-adjacent-only reports. Geometry is unchanged and no anatomical defect is claimed resolved. The 132 direct SCA gap closures still fail under the corrected predicate. Exclusion reuse now requires model and implementation hashes; legacy geometry-only records cannot be reused automatically. See [batch 22](docs/INTERSECTION_PREDICATE_BATCH22_v0.9.114.md).

Batch 22 also reclassifies the left A5 pair (source faces 1156 and 1222) as a tolerance artefact: exact checks find no crossing. Its earlier reported inherited contact is superseded by this finding. No wall geometry changes. The residual left A5/corpus-callosum overlap remains 0.195 mm.

## Petrosal wall cleanup batch 23, v0.9.115

Three Float32 coordinate corrections, maximum 0.000005395 mm, remove nine microscopic exact left inferior petrosal self-contact pairs. Twelve pairs fall to three; their remaining source triangles are unchanged. The three native interfaces (119 shared coordinates), all 203 boundary edges, every source face index and stored normal component remain fixed. No new named-surface contact or sampled tissue entry is introduced. This is numerical wall cleanup, not regional anatomical acceptance. Bone fit, the ten right-sided pairs, full receiving lumens and other findings remain open. See [batch 23](docs/PETROSAL_WALL_BATCH23_v0.9.115.md).
