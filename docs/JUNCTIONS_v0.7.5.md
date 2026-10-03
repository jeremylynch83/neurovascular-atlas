# ICA junction and panel corrections, v0.7.5

Both M1 origins now leave the terminal ICA smoothly in a lateral direction. PCOM origins have moved approximately 4.8 mm on the right and 5.2 mm on the left upwards along the retained ICA. Anterior choroidal origins have moved approximately 1.6 mm and 2.6 mm upwards. Ophthalmic origins have moved approximately 1.4 mm and 1.0 mm downwards. These distances describe this teaching model, not prescribed patient measurements.

The proximal ophthalmic and PCOM curves are refitted with smooth interpolation and a blend into their retained distal courses. Branch descendants follow their attachment. All distal centreline endpoints and both A1 centrelines are retained. The terminal 2.5 mm of the ICA skin tapers to a 1.45 mm radius, burying the parent end cap within the joined A1/M1 surface instead of leaving an exposed flat roof.

Small bilateral ICA junction regions are reconstructed jointly from swept tubes. A surface boolean union removes intersecting internal skins; local fairing smooths shared branch junctions and transitions into the retained surface. A1's proximal surface participates in this join although its course is unchanged. Shared normals are calculated before splitting the independently selectable anatomical parts. Bones, mandibular routes and the donor/recipient graph of all 34 potential connections remain unchanged. Lossless meshopt compression does not quantise positions or decimate triangles.

One-off authoring checks inspect the connected exported surface, shared seam normals, origin ordering, retained endpoints, M1 lateral departure and sampled cavernous/clinoid clearance against the sphenoid. Exact coordinate checks, area comparison and bidirectional surface-distance sampling check unchanged MMA and infraorbital geometry, including near-coplanar faces retriangulated by the boolean kernel. For the latter, vertex coordinates are identical and the maximum bidirectional centroid distance is below 0.001 mm; the measured deviations are recorded in the audit. These checks are not an added installation or routine build stage. The model retains the canal-lumen and estimated dural-boundary limitations documented for v0.7.2.

The details panel omits associated-passage relationships, passage contents and notes. Both panel titles use the same 13 px UI font and reduced padding, with a 6 px gap between panels. Authoring metadata remains in the catalogue.

## Anatomical sources

- Gibo et al., 1981, *Microsurgical anatomy of the supraclinoid portion of the internal carotid artery*, https://pubmed.ncbi.nlm.nih.gov/7277004/.
- Ferreira et al., 1990, *Microsurgical anatomy of the anterior choroidal artery*, https://pubmed.ncbi.nlm.nih.gov/2094191/.

The review image renders the actual exported mesh with matched before/after cameras. It is not an independent clinical validation or an interactive-browser screenshot.
