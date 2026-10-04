# Cavernous sinus wall correction, v0.9.9

4 October 2026. Follows the user's review of the v0.9.8 cavernous envelope: the outer lateral edge should be straight or concave, with no anterior rounded bump.

## Resulting shape

The outer lateral wall is limited by a straight to gently concave profile. The posterior contour is restrained to reduce its dome. The anterior rounded horn and the anterolateral ellipsoidal recess are removed. A thin anterior roof connection and a flat lesser-wing entry preserve the neighbouring venous junctions. The new lesser-wing entry is also constrained by the retained sphenoid and temporal bone surfaces. Its local triangle/bone intersection checks pass on both sides, with sampled surface gaps of approximately 0.23 mm. These gaps are authoring clearance, not anatomical wall thickness.

The main envelope still tapers towards its superior and inferior ends. It is not replaced by a rectangular solid. Surface smoothing rounds the wall intersections without reinstating the original lateral bulge. The anterior/posterior intercavernous channels and all named tributaries remain represented.

The arterial, optional arterial connection and skull GLBs are identical to v0.9.8. The interface and renderer are unchanged. The new meshes replace the existing venous asset, without an extra runtime model copy.

## Verification

The full delivered venous skin remains one watertight connected network with consistent winding and positive volume. All 104 named venous structures remain. The geometry audit checks the actual displayed cavernous sinus/ICA triangle surfaces independently of the temporary closed authoring masks. Outside the regional replacement, 196,494 original venous vertices remain unchanged.

Small disconnected scraps of the newly drawn cavernous envelope are excluded only after confirming their bounds and labels. A detached retained tributary causes authoring to fail. The quantitative values in the report describe this mesh; they are not measurements of real venous wall thickness or patient anatomy.

- [Geometry and clearance](validation/venous-morphology-v0.9.9.json)
- [Local authoring report](validation/cavernous-local-build-v0.9.9.json)
- [Viewer fixture](validation/venous-viewer-v0.9.9.json)
- [UI fixture](validation/venous-ui-v0.9.9.json)
- [Build and installer checks](validation/venous-build-v0.9.9.json)

The companion review ZIP contains six matched v0.9.8/v0.9.9 views in translucent and opaque states, coronal sections, and the geometry report. Opaque views make the wall contours easier to assess; translucent views retain the ICA relationship. Images are excluded from the app install ZIP.

## Anatomical limits and references

This is a reference-guided teaching reconstruction with illustrative calibres and inferred dural boundaries. The unresolved low petrous/lacerum skull canal is retained. Cranial nerves, pituitary, dural rings and detailed venous septa are not rendered. A matched skull, arterial and venous dataset is needed to establish patient-specific registration and quantitative image-to-mesh accuracy.

The angiographic and anatomical references remain those in [the v0.9.8 review](CAVERNOUS_v0.9.8.md), including original angiography and selective sampling DynaCT at [Neuroangio](https://neuroangio.org/venous-brain-anatomy/cavernous-sinus/). The v0.9.9 contour change implements the user's anatomical review rather than a new patient segmentation.
