# Deep venous additions, v0.9.27

Implements page 2 entries D01-D22 of Deep_Posterior_Fossa_Vein_Catalogue.pdf (5 October 2026). D23 transmedullary veins are excluded. The 22 family groups contain 44 side-specific selectable meshes and 70 collector/tributary components. Left calibres are modestly smaller in this selected teaching pattern; bilateral similarity is not a claim of anatomical symmetry.

## Coverage

- D01-D07: direct lateral, lateral and medial atrial, interrupted longitudinal caudate arcade, anterior and transverse caudate, inferior ventricular collectors.
- D08-D12: internal occipital, posterior callosal, anterior/superior/inferior thalamic veins.
- D13-D18: uncal, hippocampal, inferior striate, insular, posterior septal and inferior choroidal veins.
- D19-D22: olfactory, posterior orbitofrontal, representative hypothalamic and regional deep medullary tributaries.

Direct lateral and lateral atrial courses occupy separate ventricular territories in this selected pattern; their labels are not treated as universally distinct synonyms. The caudate arcade is interrupted rather than a complete ring. The hippocampal group includes a longitudinal collector and transverse inputs. The insular group includes anterior, central and posterior representatives. Medullary channels are sparse, small, tapered deep white matter examples, not a DVA or a superficial-to-deep transmedullary network. Alternative parasellar outflows are not all instantiated.

## Geometry and verification

Courses use registered neural surfaces, radius-aware circular sweeps, physical smoothing and local obstacle clearance. New and receiving skins are joined with labelled boolean unions. Artificial closure faces for retained source cuts are removed afterwards. Fourteen retained receiving labels gain local ostia; unrelated existing veins, arteries, brain, skull and anastomoses are retained.

`validation/deep-veins-geometry-v0.9.27.json` records non-degenerate geometry, 56 selected drainage/arcade junctions, preserved external collars with a 0.025 mm surface tolerance, authored label adjacency, and new skin contacts against retained arteries, bone and untouched veins. `validation/deep-veins-courses-v0.9.27.json` records radius/curvature and body-target centreline checks. `validation/deep-veins-loader-v0.9.27.json` checks exact positions and indices through the actual Three.js loader, unit normals and asset hashes. These checks do not establish clinical anatomical correctness, exclude every tissue intersection or establish solid containment for open tissue skins.

The render uses the exact delivered meshes and quantised loaded normals in an orthographic surface renderer; it is not a browser GPU screenshot. The source PDF and reference image pixels are not redistributed.

## Evidence and limits

The supplied catalogue retains source-specific courses and drainage from Bradac, Rhoton, Terminologia Anatomica and Neuroangio. Main public primary teaching references:

- https://neuroangio.org/venous-brain-anatomy/internal-cerebral-vein/
- https://neuroangio.org/venous-brain-anatomy/basal-vein-of-rosenthal/

`anatomy/source/deep-veins-v0.9.27.json` retains all 22 source-field records, authored curves, selected receiving structures and placement parameters. This is an illustrative teaching reconstruction. It contains no measured patient centreline or normal vein calibre data. Hypothalamic, transverse caudate, medullary and other fine tributaries remain representative until a registered human exemplar supports individual channels. Wider baseline anatomical review, including the prior posterior arterial/venous contacts, remains pending.
