# Foramina and facial surface correction, v0.9.145

Both optic canals now have an enclosed oval isthmus measuring 3.7 x 4.5 mm at model scale. Eight stations over a 1.75 mm axial interval were checked with 96 radial wall rays per station. The mouths retain the source's oblique, asymmetric wall lengths. The superior sphenoid is constructed by subtraction within its original envelope. The maximum signed outward vertex distance from that source is under 0.000004 mm, within floating-point precision. No projecting collar is added. The optic nerve remains unsegmented.

The lowered duplicate mental exit is removed on each side. The mandibular and mental courses are fitted back to the native opening, with a nominal 2.5 mm mental bore. Lateral ramus cuts are removed. Reversed normals on original cap faces, including the triangular mental-region marks, are corrected and blended across component boundaries.

Posterior superior alveolar branches retain their registered intraosseous portions. Their small passages follow the vascular surfaces with 0.10 mm radial clearance. Native facial contours are protected outside each cut, replacing the former broad cortical grooves. Small residual orbital and medial coronoid display-surface contacts are cleared locally.

Validation completed:

- Production build: one combined scene, 1,258 named parts and five model assets.
- Eight orbital and twenty facial vessel/connection checks: no bone-surface contacts in their checked regions.
- Twenty-eight updated arterial flow courses: 129 closed split sections across three injection positions per course. Safe ranges retained; two endpoint samples are within the existing 0.00001 mm serialization tolerance.
- Edited sphenoid, mandible and maxillary surfaces: consistent winding, no non-manifold edges and no introduced independent material self-intersection region.
- Exact decoded comparisons retain the previous temporal corrections, 53 other craniofacial parts, 581 circulation meshes, 159 arterial connection meshes and 229 venous meshes.
- Final actual-mesh renders reviewed from both facial sides and along each optic bore, including an isthmus cutaway.

The craniofacial model remains an open, component-based teaching reconstruction. Four existing internal/palatal triangle crossings and previously documented source anastomotic overlaps remain. Two triangle-pair migrations stay within an existing source contact region. These are recorded separately in the QA reports; this revision introduces no new independent crossing region. Diameters are illustrative adult model targets, rather than patient-calibrated measurements.

The revision145 method and saved geometry are authoritative for these edited passages; earlier source-control JSON files are retained as authoring history. Validation scripts are tools/foramina/validate-revision145.py and tools/foramina/validate-revision145-flow.mjs. Geometry QA additionally needs NumPy, trimesh, rtree, VTK and python-fcl. Normal app builds use the existing package dependencies.
