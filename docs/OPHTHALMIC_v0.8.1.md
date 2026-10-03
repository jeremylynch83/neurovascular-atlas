# Ophthalmic correction, v0.8.1

Both ophthalmic origins now lie just distal to the anterior genu on the retained ICA centreline. The paraophthalmic region begins 1 mm of centreline arc before its ophthalmic origin. This is a model-specific boundary estimate, not a measured dural ring.

The proximal ophthalmic curves use an endpoint-tangent-matched cubic spline. The distal orbital paths, both ICA centrelines, PCom/AChA origins, A1/M1 centrelines, and all other 573 vessel paths are retained from v0.8.0. Calibres and anatomical parents are unchanged.

## Checks

- One connected native surface with the existing two normal arterial loops and a watertight indexed surface before label partition.
- All fourteen ICA segments selectable with the actual Three.js loader and raycaster.
- Root and GitHub Pages subpath production builds pass.
- Meshopt buffer views round-trip exactly, without quantisation.
- Bones, potential-route asset and UI source files are byte-identical to v0.8.0.
- The ZIP is verified before atomic publication.
- These are one-off authoring checks, not an added installation or startup step.

## Model positions

| Side | Ophthalmic height increase | Arc beyond genu | Boundary before origin |
| --- | ---: | ---: | ---: |
| Right | 3.03 mm | 0.48 mm | 1.00 mm |
| Left | 3.32 mm | 0.57 mm | 1.00 mm |

Coordinates are reference reconstruction dimensions, not patient measurements. The supplied screenshot guided the correction.
