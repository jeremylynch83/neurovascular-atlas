# Posterior fossa venous expansion v0.9.28

Implements the 31 catalogue entries P01–P31 on page 3 of the supplied Deep and posterior fossa vein catalogue, on the v0.9.27 app baseline. Includes 69 new selectable mesh labels: 67 added courses and two relabelled lower lateral mesencephalic skin components. The D01–D22 expansion remains included. Transmedullary veins remain excluded.

## Anatomy and presentation

- Superior, anterior and inferior hemispheric tributaries, horizontal fissure veins and lateral recess extensions.
- Superior, middle and inferior cerebellar peduncular tributaries; tonsillar, superior/inferior retrotonsillar and medial/lateral supratonsillar components.
- Fine illustrative dentate and fourth-ventricular choroidal tributaries.
- Lateral, preolivary, retro-olivary and posterior medullary channels; unequal transverse medullary connections; a short dorsal cervical spinal segment.
- Cerebral peduncular, tectal and intercollicular channels; one short posterior mesencephalic variant; upper pontomesencephalic sulcal channels distinct from the existing midpontine transverse veins.
- Selected prepontine, inferior petrosal CPA and lower medullary bridges; separately labelled C1 radicular and foraminal components.
- Flattened tentorial routes with unequal calibre, guided by each tentorial leaf.
- The lower existing lateral mesencephalic skin is relabelled as pontotrigeminal, avoiding an overlapping new tube.

Descriptions and linked drainage relationships distinguish the displayed arrangement from variable alternative routes. Existing receiving trunks remain accessible within the appropriate family groups. Wrapped index priority text has been removed from page-2 vein names, and their catalogue descriptions recovered without changing the deep vein geometry.

## Geometry and limits

Circular sweeps use 24 radial stations and approximately 0.2 mm longitudinal stations. Fine illustrative calibres taper at free tips. Tentorial channels use flattened cross-sections. Local labelled unions create shared drainage ostia. Receiving skins have submillimetre vertex welding and minimal degenerate/nonmanifold face cleanup where required. Existing shared collar surfaces are preserved locally. Detailed preparation and validation results are included in docs/validation.

The atlas lacks independent segmentations of dentate nuclei, fourth-ventricular choroid plexus and tela, inferior medullary velum, middle/inferior cerebellar peduncles, medullary olives/pyramids, and cervical nerve root corridors. Related courses are illustrative regional reconstructions constrained by the available gross surfaces. This release does not establish patient-specific centreline geometry or measured calibres. These structures require specialist anatomical review.

Checks cover finite non-degenerate triangles, loaded unit normals, physically shared labelled ostia, selected venous adjacency, retained original receiving collars, and new skin contacts with existing arterial, bony and unrelated venous surfaces. Pial course checks use registered target surfaces; intended deep/fissural/choroidal courses can intersect their target tissue. These checks do not exclude every tissue intersection, prove general solid containment or certify clinical accuracy. Wider pre-existing atlas review limitations remain.

## Sources

Supplied 5 October 2026 catalogue entries P01–P31. Bradac source locators and source fields are retained in anatomy/source/posterior-veins-v0.9.28.json.

- Matsushima et al. Microsurgical anatomy of the veins of the posterior fossa. J Neurosurg. 1983;59:63–105. https://pubmed.ncbi.nlm.nih.gov/6602865/
- https://neuroangio.org/venous-brain-anatomy/veins-posterior-fossa/
- https://neuroangio.org/venous-brain-anatomy/4th-ventricle-and-its-veins/
- https://neuroangio.org/venous-brain-anatomy/lateral-mesencephalic-vein/
- https://neuroangio.org/venous-brain-anatomy/bridging-vein-anterior-brainstem-group/

No source image pixels are redistributed. The delivered render uses actual loaded venous triangles and normals; faint neural context is decimated for this static illustration only.
