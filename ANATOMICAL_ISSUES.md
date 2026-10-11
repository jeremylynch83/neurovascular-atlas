# Deferred anatomical issues

These issues are retained for future work. They are unresolved and are not accepted anatomical corrections. Vessel geometry remains at the unchanged .67 checkpoint. The list covers 12 segments in three active networks; it is not a whole-atlas certification.

| Network | Vessel segment | Recorded issue |
|---|---|---|
| left-tentorial-mastoid | MMA–tentorial marginal left | Crosses bone.temporal.left (79 contacted facets). |
| left-tentorial-mastoid | Tentorial marginal left | Missing exact native attachment to Dorsal meningeal left (1 source port vertices). Missing exact native attachment to Meningohypophyseal trunk left (2 source port vertices). |
| left-tentorial-mastoid | MMA petrosquamosal left | Missing exact native attachment to Middle meningeal left (124 source port vertices). |
| left-tentorial-mastoid | Occipital mastoid–MMA petrosquamosal left | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-tentorial-mastoid | Occipital mastoid dural branch left | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-tentorial-mastoid | Occipital mastoid left | Missing exact native attachment to Occipital left (106 source port vertices). |
| right-tentorial | MMA–tentorial marginal right | Crosses bone.temporal.right (132 contacted facets). |
| right-tentorial | Tentorial marginal right | Missing exact native attachment to Dorsal meningeal right (2 source port vertices). Missing exact native attachment to Meningohypophyseal trunk right (3 source port vertices). |
| right-tentorial | MMA petrosquamosal | Requires review within the coupled route and parent reconstruction; do not assume the whole segment needs replacement. |
| left-posterior-cavernous | Posterior cavernous MMA–posterolateral ILT left | Crosses bone.sphenoid (68 contacted facets). |
| left-posterior-cavernous | MMA posterior cavernous left | Missing exact native attachment to MMA cavernous left (98 source port vertices). |
| left-posterior-cavernous | ILT posterior branch left | Missing exact native attachment to ILT anterior branch left (64 source port vertices). Missing exact native attachment to ILT posteromedial ramus left (88 source port vertices). Missing exact native attachment to Inferolateral trunk left (69 source port vertices). |

Facet and vertex counts are geometric measurements, not numbers of separate anatomical defects. All three components still fail route feasibility, independent anatomical support, bone clearance and source-native interface checks.

Other open anatomical work includes falcine parent support review and whole-atlas continuity. App integration, delivered buffers and browser runtime have separate passing checks in VALIDATION.json; these do not establish anatomical acceptance.

## App integration metadata, v0.9.68

Four new, unreviewed meningeal vein meshes have no authored vessel-course specification. They remain visible in this working app; their anatomical course is not certified:

- vein.middle_meningeal.anterior.left
- vein.middle_meningeal.anterior.right
- vein.middle_meningeal.posterior.left
- vein.middle_meningeal.posterior.right
