# Vertebral and posterior circulation: Draft 01

Release v0.5.0 adds 98 posterior vessel parts to the 206 existing carotid/ECA parts, in the same RAS millimetre frame and original skull context. This is an editable reference reconstruction, not patient segmentation. The model does not become more anatomically certain merely by increasing mesh resolution.

## Evidence used

- Borden, *3D Angiographic Atlas of Neurovascular Anatomy and Pathology* (2006), Chapter 6, printed pp163–167; AP/lateral angiograms in Fig6.1 and 3D views in Fig6.2 were visually inspected. Fig6.4's normal circulation was also reviewed. These establish the selected branch hierarchy, major curves and relative calibre. Coordinates were authored manually, not recovered by calibrated biplane reconstruction. Source images are not redistributed.
- Giotta Lucifero et al., *Microsurgical Neurovascular Anatomy of the Brain: The Posterior Circulation (Part II)*, 2021. Cadaver-based segment and branch relationship cross-check. DOI: 10.23750/abm.v92iS4.12119. https://pubmed.ncbi.nlm.nih.gov/34437362/
- Párraga et al., *Microsurgical anatomy of the posterior cerebral artery in three-dimensional images*, 2011. PCA segment definitions and cisternal landmarks. DOI: 10.1016/j.wneu.2010.10.053. https://pubmed.ncbi.nlm.nih.gov/21492726/
- Kiyosue, *External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment* (2020), particularly Fig3.17: ascending pharyngeal–vertebral muscular and odontoid communications. Enlarged channels in pathological examples are not treated as normal measured calibre.

## Represented anatomy and variant

Bilateral vertebral arteries extend from a truncated lower cervical V1 through estimated V2/V3 to V4. There are no subclavian origins or aortic arch in this draft. The left VA is modestly larger. Both VAs join a single basilar artery. Bilateral PICA, AICA and SCA are present, with selected hemispheric/vermal, tonsillar, choroidal and labyrinthine branches. Selected pontine, medullary and thalamic perforators, posterior choroidals and proximal anterior/posterior spinal arteries are included.

Both PCAs have adult P1 connections from the basilar apex. Each PCom joins the exact P1/P2 junction. PCA cortical branches include calcarine, parieto-occipital, inferior temporal, splenial and selected smaller cortical branches. The anterior tree and right ECA retain their named selection labels.

No fetal PCA, duplicated SCA, fenestration, PICA-ending VA or persistent carotid–basilar artery is represented. Left-sided starting paths use mirrored reference curves with explicit modest adjustments and independent skull constraints, not patient-specific bilateral reconstruction. Distal perforators and cortical branches are selected examples, not an exhaustive arterial tree.

## Relations and limitations

The original skull constrains physical bone exclusion. Intracranial paths were authored using atlas relationships before fitting the skull. Cerebellar branches are constrained within a posterior-fossa envelope; the skull envelope does not identify a pial surface. No brainstem, cerebellum, tonsils, ventricular walls, cranial nerves or cervical vertebrae are registered in this scene. V2 transverse-foraminal position, V3 atlas-groove relation, exact AICA meatal loop and distal sulcal courses therefore need anatomical review against future tissue context.

The coarse skull does not resolve all small canals. Short labyrinthine branches enter the temporal bone towards the internal acoustic canals and are explicitly recorded exceptions. Existing petrous ICA, ophthalmic, ethmoidal and vidian canal exceptions remain. Exceptions are unresolved relationships, not clearance passes. The main VAs, cerebellar and cortical vessels must not be permitted to pass through bone merely to make a reference-shaped curve fit.

## Cross-circulation junction correction

The previous CCA/ICA used separately capped tubes, with the ECA union added at the same origin. That left an annular shoulder despite a watertight union. The new model lofts each CCA continuously into its ICA, with a smooth radius transition through the bifurcation region. The ECA is joined to this continuous trunk. This fixes the geometry before surface smoothing.

All normal vessel surfaces are unioned together, including communicating endpoints. The same local smoothing pass now includes legacy ECA origins, anterior origins, posterior origins, the vertebrobasilar junction, both PCom/PCA joins and the merged anterior spinal roots. The support radius depends on the local parent radius; tiny branches are not globally blurred. Full-surface normals are calculated before partitioning into named selectable parts. Shared labels therefore do not introduce shading seams or independent capped cylinders.

Isolating/hiding a labelled neighbour can expose the shared internal interface. This is a display consequence of splitting one skin into selectable parts, not a hole in the complete circulation. Review junctions with all their connected neighbours visible. Close-up review images use a common colour at the carotid bifurcation to distinguish geometry from colour boundaries.

## Potential channels

The default-off gold overlay now has 17 selected routes. It retains the 14 anterior routes and adds occipital–VA C1 muscular, descending occipital–VA C2 muscular and ascending pharyngeal–VA odontoid pathways. Endpoints use the actual named vessel paths. Overlay radii are illustrative, not measured normal channels or simulation lumina. The routes are excluded from the normal vessel union and topology tests. This is not a complete catalogue of potential posterior dural communications.

## Refinements and validation

1. Preserve source paths, branch labels and the fixed RAS skull frame.
2. Author posterior curves and explicit connections to the anterior graph; record compartments and variant.
3. Replace the separate CCA/ICA caps with continuous geometry and smoothly interpolated radius profiles.
4. Fit V3/V4 through the existing foramen-magnum opening. The first-pass posterior occipital-rim collision was corrected, not exempted.
5. Adjust cerebellar paths to clear bone and unrelated vessels, including the existing hypoglossal meningeal and occipital arteries. Smooth fitted displacements to avoid kinks.
6. Check radii, curvature and child origins; audit new paths against all existing arteries with an explicit local allowance at genuine junctions.
7. Union, locally fair and partition the single surface with shared normals. Expect two independent cycles: the completed circle of Willis and the paired anterior spinal root connection. The old ECA genus-zero requirement is inappropriate here.
8. Test final triangles against bones, preserve exception locations, inspect AP/lateral/oblique and enlarged junction renders, and test the actual browser build and package.

The authoring code, dense centreline/radius data, numerical reports and input hashes are retained in `anatomy-source/posterior/`. See its README for rebuilding. The mesh is intended for anatomical review; a device simulator would additionally need validated luminal geometry, physical properties and contact constraints.

## Release checks

The final joined surface is watertight with consistent winding, one connected component and the two intended cycles. All 33,833 shared partition vertices have identical normals. New vessel paths have no unintended contact beyond the 0.08 mm overlap tolerance and explicit local junction allowances. There are no new ECA/bone contact pairs after the shared smoothing pass; the superficial occipital main vessel remains clear. Small canal exceptions are retained in the report. The production build and browser selection/visibility/connection/switching checks passed. The extracted anatomy setup reused case001 successfully. Docker itself was not available in the build environment.
