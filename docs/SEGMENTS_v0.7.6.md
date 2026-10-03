# ICA branch curvature, bifurcation and selectable segments, v0.7.6

The proximal ophthalmic and posterior communicating paths regain gentle curvature. Their v0.7.5 origins and distal endpoints remain fixed. Local path changes are blended into the retained distal course; attached small branches follow their parent. Both A1 centrelines remain unchanged.

The terminal ICA, A1 and M1 share a locally blended surface. A smooth implicit union fills the sharp junction transition, with a gradual spatial fade and protection of adjacent branch collars. The review compares the actual exported surfaces in one colour to make the shape assessable independently of selection colours. Distal branches are cropped in these close-ups.

Both ICAs have seven individually selectable, coloured regions: cervical, petrous, cavernous, paraophthalmic, posterior communicating, anterior choroidal and terminus. These follow Shapiro's endovascular nomenclature. Petrous includes the traditional lacerum region; paraophthalmic includes the clinoid region. The anterior choroidal region surrounds its ostium, with terminus beyond it. Dural and petrolingual boundaries remain estimates in this model.

Each region is an anatomical-tree child of its ICA. Branches sit beneath their originating region. Clicking a surface selects that region. Selecting the whole ICA in the tree highlights and focuses all its regions. Visibility controls use the same subtree behaviour as the rest of the anatomy. Shared vertex positions and normals are retained when dividing the surface, so the coloured boundaries introduce no geometric seams.

## Checks

- Identical source triangles across all fourteen segment partitions, with no missing or duplicate faces and matching shared normals.
- Actual viewer GLTFLoader/MeshoptDecoder resolves 491 meshes. Raycaster selection succeeds for all fourteen ICA regions.
- Whole-ICA focus, segment search and parent/segment visibility subtrees checked against the app implementation.
- Both production base paths and the catalogue build checked. Interactive browser testing was not available.
- Branch origins, distal endpoints and A1 courses retained. Terminal junction regions have no welded-edge anomalies; sampled cavernous/clinoid surfaces remain outside the sphenoid.
- A whole-scene coordinate-weld check detects the same 1,282 coincident edge anomalies at fine vessel tips as v0.7.5, at identical positions outside the edited terminal regions. These are recorded rather than described as an exported whole-scene watertightness pass. The indexed joined authoring surface remains closed before float32 export.

One-off geometry checks stay outside routine installation and builds. Complete canal lumina and dural boundaries remain unresolved as documented in earlier releases.

## Source

Shapiro M et al. *Toward an Endovascular Internal Carotid Artery Classification System*. AJNR. 2014;35:230–236. https://pmc.ncbi.nlm.nih.gov/articles/PMC7965739/
