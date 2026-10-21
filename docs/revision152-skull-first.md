# v0.9.152: skull-first progressive loading

Loads the existing craniofacial asset first and makes the AP skull scene interactive after its first successful render. The skull retains its existing ghosted visibility. The initial explanatory HTML and failure/retry behaviour are retained.

Then loads the existing arterial starter pack, main intracranial branches, smaller regional branches, anastomoses, veins and brain, in that order. Geometry arrives without automatic camera movement. DSA retains its existing readiness gates.

The initial model download is now the skull: 17,505,832 bytes raw, approximately 15.4 MB gzip. Total arterial-plus-skull download remains 88,785,576 bytes raw, approximately 66.0 MB gzip. No source geometry or generated pack bytes changed.

The earlier revision151 notes and measurements describe the artery-first release. They are retained as historical reports and do not describe the initial order in this version. This revision reruns the production build, actual loader/CPU scene checks, catalogue/DSA comparisons and HTML fallback checks. Successful GPU rendering and browser performance remain unverified because the available browser does not support WebGL.

Build with `npm ci` then `npm run build`. The ZIP contains sources and generated packs; it is not a deployment.
