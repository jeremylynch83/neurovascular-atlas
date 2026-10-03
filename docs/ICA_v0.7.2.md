# ICA skull-base correction, v0.7.2

The bilateral ICA reconstruction in v0.7.0/0.7.1 entered too medially, near the jugular fossae, and swept too far laterally in the cavernous region. This release revises those courses against the actual temporal and sphenoid meshes. The supplied reference screenshots inform anatomical relationships; their coordinates were not transferred to this model.

## Changes

- Move each external carotid entry region approximately 9 mm laterally and 6 mm anteriorly relative to the previous reconstruction.
- Ascend within the estimated petrous corridor, then turn anteriorly and medially towards the petrous apex. The ICA passes above the foramen lacerum region, not vertically through its cartilage-filled opening.
- Bring the cavernous course beside the sella and the clinoid ascent medial to the anterior clinoid.
- Carry dependent origins and shared junctions with the ICA, preserving the cervical origin and terminal ICA endpoint. Refit the proximal ophthalmic course towards its retained orbital-apex target.
- Adjust the neighbouring inferior hypophyseal and tympanic courses around the revised ICA. Carry the potential connection endpoints with their recorded donor and recipient vessels; the 34 connection relationships are unchanged.
- Add 33 selectable landmarks under **Skull → ICA skull-base landmarks**. Entries distinguish actual bone-surface anchors from estimated canal, ligament and dural regions. Existing carotid-canal entries now follow the revised course.

The bone mesh and the previous MMA and infraorbital corrections are retained. The app's existing tree, focus and visibility controls handle the new landmarks. No geometry authoring or anatomical audit runs during installation or app builds.

## Method and limits

Coordinates are RAS millimetres. Side-specific stations constrain a locally interpolated, faired curve. Dense old/new arc correspondence transports the original joined vascular surface without resampling its triangles or reducing vessel calibre. Hierarchical root collars give parent and child surfaces the same deformation around their shared junctions; local seam fairing follows on the joined skin. Short attached trunks can therefore move beyond their initially proposed centreline displacement. The exported `surface-centrelines.json` records that final deformation.

This remains a reference-guided teaching reconstruction. The temporal mesh does not resolve a complete carotid canal lumen, and dural rings and the petrolingual ligament are not segmented. Those locations are explicitly estimated. The petrous route cannot be certified as canal-contained from this mesh, and the existing optic corridor has the same source-resolution limitation. Landmark labels do not imply patient-specific anatomy or anatomical approval.

The authoring audit checks the actual exported joined mesh for finite geometry, retained face incidence, watertight topology and consistent winding. It samples exported C4/C5 surface vertices and face centres against the sphenoid and screens new close approaches to neighbouring vessels. These are regional numerical checks, not an exhaustive self-intersection or anatomical correctness proof. Matched-camera review images show the actual exported geometry with selected vessels and cropped/translucent bones; the release retains the full bone mesh.

See `validation/ica-v0.7.2.json` and the compression reports for this release's measured results. Meshopt compression is verified by exact buffer round-trip. Reference images and full authoring intermediates are kept outside the installation ZIP.

## Anatomical references

- Bouthillier A, van Loveren HR, Keller JT. Segments of the internal carotid artery: a new classification. *Neurosurgery*, 1996. https://pubmed.ncbi.nlm.nih.gov/8837792/
- Osawa S et al. Microsurgical anatomy and surgical exposure of the petrous segment of the internal carotid artery. *Neurosurgery*, 2008. https://pubmed.ncbi.nlm.nih.gov/18981828/
- Ziyal IM et al. Proposed classification of segments of the internal carotid artery: anatomical study with angiographical interpretation. *Neurologia Medico-Chirurgica*, 2005. https://www.jstage.jst.go.jp/article/nmc/45/4/45_4_184/_article

## Authoring only

Overlay `INR_ICA_Authoring_v0.7.2.zip` on the previous `INR_Foramina_Authoring_v0.7.0.zip` workspace, retaining its `anatomy-source/foramina`, `anatomy-source/combined` and tool dependencies. The patch README lists the generation commands. Do not run this pipeline as a routine application validation step.
