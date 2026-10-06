# Round posterior trunks, v0.9.24

The previous pass smoothed vertices but retained the repeated shaft and junction bulges. This pass extracts geodesic cross-section centrelines, smooths them over an approximately 2 mm physical scale and creates 48-sided circular sweeps. Shaft radii come from robust measurements of the delivered model. PCA P1/P2 boundaries share positions and tangents; basilar bifurcations use their original interface centroids.

Seven intracranial trunks are reconstructed: basilar, left/right PCA P1, left/right PCA P2/P3 and left/right vertebral V4. Cervical vertebral courses are retained. Sixty-one adjacent labels are included in the joined skin, with original distal branch geometry beyond a short proximal trim. A shared smooth placement field keeps reconstructed label seams coincident. It can change local cross-sectional dimensions, so unchanged calibre is not claimed.

All named atlas structures are retained. Only the circulation GLB is replaced. Mesh indices and counts change. Exact buffer round trips and the actual Three.js GLTFLoader validate the export. The render is an orthographic Matplotlib surface render of the actual triangle meshes and normals, not a browser GPU screenshot.

## Limits

This is a review build. The full triangle intersection gate has not passed: remaining vessel-to-vein contacts are listed in `validation/round-trunks-geometry-v0.9.24.json`. Existing baseline contacts are recorded separately. Open tissue skins do not support a general solid-containment claim. Surface collars to unchanged adjacent labels use a 0.025 mm maximum closest-surface tolerance. No clinical accuracy is established by smoothing.
