# Cavernous cavity and venous entries, v0.9.10

4 October 2026. Implements the user's annotated review: a slimmer cavernous cavity, concave lateral wall and roof, and smoothly attached SMCV and sphenoparietal/lesser-wing channels.

## Shape and attachments

The cavernous body is rebuilt from wall profiles, replacing the rounded envelope. Its outer wall bows inward along the anteroposterior course. The roof also curves inward, with no rounded anterior recess. The anterior intercavernous connection is lowered and moved posteriorly to blend into the revised roof.

The terminal superficial middle cerebral vein and lesser-wing channel are rebuilt as smoothly curving, tapered receiving channels. Their mouths blend into the cavernous space through a single welded venous surface. The former thin joining plate and ragged terminal tips are removed. Exported surface normals are identical across the four labelled junctions, retaining smooth shading when the meshes are drawn separately.

All 104 vein labels remain in one connected network. The completed arterial, anastomotic and skull GLBs are byte-identical to v0.9.9. No interface or rendering changes are included.

## Measured checks

These values describe the teaching mesh in its authoring coordinate system. They are not calibrated patient measurements or venous wall thicknesses.

| Check | Right | Left |
| --- | ---: | ---: |
| Cavernous label volume, v0.9.9, temporarily capped | 1,040.8 mm³ | 1,040.9 mm³ |
| Cavernous label volume, v0.9.10, temporarily capped | 823.6 mm³ | 824.1 mm³ |
| Reduction in that volume estimate | 20.9% | 20.8% |
| Roof inward depth below its endpoint chord | 1.12 mm | 1.13 mm |
| Lateral wall inward depth from its endpoint chord | 0.40 mm | 0.41 mm |

The lateral measurement uses the actual triangulated surface at z = 63 mm and y = −50, −46 and −42 mm, below the rebuilt entries. Roof samples use y = −49, −43.5 and −39 mm. These samples confirm local inward curvature; they are not a claim that every surface point, including tributary mouths, is concave. Capped label volume depends on how the open label ports are temporarily closed.

The common venous skin is watertight, consistently wound and has positive volume: 235,269 vertices and 470,786 triangles. All 196,494 original exterior vertices outside the replacement remain unchanged. Direct triangle intersection tests find no cavernous sinus/ICA crossings on either side. The rebuilt terminal channels also have no detected ICA or skull crossings within the replacement interior, excluding the retained overlap collar and peripheral courses. Their sampled lesser-wing/bone gaps are approximately 0.20–0.22 mm.

The four direct CS/entry boundaries contain shared welded edges. Their 95th-percentile adjacent-face angles fall from approximately 63–70° to 25–43°. This is a triangulation smoothness measure, not an anatomical angle. Exported shared-vertex normal differences are zero.

- [Topology, preservation and ICA clearance](validation/venous-morphology-v0.9.10.json)
- [Actual surface contours and direct junction edges](validation/cavernous-contours-and-joins-v0.9.10.json)
- [Terminal channel clearances and exported normals](validation/cavernous-entry-clearances-v0.9.10.json)
- [Local authoring report](validation/cavernous-local-build-v0.9.10.json)
- [Viewer checks](validation/venous-viewer-v0.9.10.json)
- [Interface checks](validation/venous-ui-v0.9.10.json)
- [Build and installer checks](validation/venous-build-v0.9.10.json)

The separate review ZIP contains matched v0.9.9/v0.9.10 views from six directions, opaque contour views, an entry close-up and coronal sections. Rendered label colours show the actual delivered meshes and normals; the cameras and scale match between releases. The ICA and skull are unchanged in these comparison images. Review images are excluded from the install ZIP.

## References and remaining limits

The reference basis remains the original angiography and selective sampling DynaCT at [Neuroangio](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/), with the anatomical sources in [the v0.9.8 review](CAVERNOUS_v0.9.8.md). This release implements the user's contour and attachment corrections in a teaching reconstruction. The represented venous drainage pattern is one model configuration, not a universal patient pattern.

No matched patient dataset is available for quantitative image-to-mesh registration. The existing low petrous/lacerum skull canal relationship remains unresolved. Cranial nerves, pituitary, dural rings and venous septa are not rendered. Historical arterial before/after measurements in the geometry report describe the retained v0.9.7 ICA correction, not a new arterial change in this release.
