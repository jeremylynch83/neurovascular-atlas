# ICA / cavernous sinus reconstruction in v0.9.32

The v0.9.31 cavernous sinus did not enclose the distal cavernous limb and anterior genu. This revision jointly fits a recognisable cavernous loop and a compact independent sinus body to the approved lateral sketch. It keeps the ophthalmic arteries and bone fixed and leaves the lower bend outside the sinus. This is an anatomical review build.

## Geometry and fixed anatomy

The course now rises posteriorly, turns into a short forward limb, rounds into the anterior genu, and exits towards the native ophthalmic attachment. The superior ICA retains its original near-ostial wall and distal segment surfaces. The sinus is an independent rounded parasellar chamber, elongated anteroposteriorly and narrow across its local mediolateral section. Its outer shape is fitted to the retained sphenoid and temporal bone; an arterial bore is subtracted afterwards. It has no ICA-following outer sleeve and does not wrap the lower bend.

Both complete ophthalmic meshes remain exact, including their topology. All 222 native shared ostial vertices remain at their original coordinates, and all 313 original parent-wall triangles incident on those ostia survive unchanged. The superior hypophyseal attachment rings and native wall collars are also retained. Bone and brain assets and registration remain unchanged.

The original source meshes contain folded parent walls. Transporting those walls into the new course produced self-intersections, so the affected parent tube is reconstructed from the source-derived centreline radius profile rather than accepted as a deformed mesh. The course is faired before reconstruction to avoid tight offset bends. Source radii are smoothed and bounded to 2.15–2.65 mm; this is an illustrative atlas calibre, not a patient measurement. Measured radius ratios are in `anatomy/source/ica-cs-v0932/validation.json`.

The lower source course below the estimated petrolingual entry is frozen. The retained lower portion is assigned to the existing petrous label. The two Vidian ICA contribution branches remain physically attached to that lower region, and their catalogue parents are updated accordingly. No new segment names or mesh labels are introduced.

## Connections and boundaries

The meningohypophyseal and inferolateral trunks are attached through ordered native root rings. Local branch and anastomosis collars follow the same bounded coordinate field. The cavernous veins are built as a common regional surface and partitioned into their existing selectable labels. The local arterial distance field includes the ICA and nearby arterial branches, so the sinus solid has clearance around the MHT, ILT and their local rami as well as the parent wall. Every arterial surface stays fixed during this venous clearance step. Each sinus shares surface vertices with the superior and inferior petrosal routes, superior ophthalmic vein, sphenoparietal and superficial middle cerebral routes, ovale emissary route, anterior and posterior intercavernous channels, and basilar plexus. Native remote vein sections are joined through ordered triangulated rings. The right prepontine bridge retains its native ring at the reconstructed basilar plexus.

The entry is the existing estimated petrolingual level, z57.5 mm right and z57.4 mm left in the registered app coordinates. The distal cavernous wall is partitioned at the independent bone-fitted sinus envelope. This is an estimated proximal dural transition, not segmented dura. Before repartitioning, the transported original cavernous wall above entry is checked against the independent body; it is not relabelled to hide a protruding course. Legacy whole-ICA authoring arc ranges remain identified as legacy estimates.

## Verification

| Requirement | Evidence |
| --- | --- |
| Fixed ophthalmic origin and wall | Both entire OA meshes exact; 112 right / 110 left shared ostial vertices; 160 right / 153 left native incident parent faces preserved |
| Genu close to origin | Measured centreline arc 5.9 mm right / 5.6 mm left, compared with 17.4 / 17.8 mm at the original anterior genu; anatomical stations and projection method are recorded |
| Compact independent chamber | Matched lateral, oblique and bilateral renders; outer shape defined before the arterial bore |
| Containment | Vertices, edge midpoints and four interior samples per triangle; largest positive interpolated boundary residual approximately 0.013 mm, within the documented 0.04 mm discretisation tolerance |
| Bone clearance | Zero detected triangle contacts between either rebuilt ICA parent surface and retained bone; zero between either cavernous sinus label and bone |
| Perivascular space | Zero artery–sinus surface contacts; sampled minimum gaps approximately 0.27 mm right / 0.29 mm left |
| Bend validity | Minimum curvature-radius / tube-radius ratio 1.07 right / 1.11 left over the reconstructed z59–77.3 mm shaft before native grafts; no detected non-adjacent triangle intersections on the final combined cavernous/paraophthalmic walls |
| Mesh and connections | Finite positions and unit normals; no zero-area output triangles; all native remote splice rings matched; every affected previously shared catalogue vascular join retained or explicitly reassigned at the estimated lower boundary |
| App integration | Catalogue validation, TypeScript/Vite production build and actual Three.js GLTFLoader/MeshoptDecoder checks pass; unchanged positions/indices remain exact |

The measurements are sampled or tolerance-limited geometry checks, not analytical proof of all possible intersections or independent anatomical approval. Details, mesh counts, hashes and per-junction results are in the accompanying JSON reports.

## Renders and remaining limits

The AP comparison also uses a matched orthographic camera. The renders use surfaces decoded from the exported production GLBs. The lateral comparison uses the same scale and camera before and after. The sphenoid is cut away and simplified for display; the actual app bone geometry is untouched. The apparent open upper end is an original named-vessel boundary with adjoining branches omitted from the regional view. No new clinical end cap is added.

The model does not resolve dura, cranial nerves, septa, or all skull-base canal lumina. Lower petrous/canal contacts remain in the retained source below the corrected cavernous region. These are explicitly outside the successful local clearance gate. The broader straight-sinus, pericallosal and other existing review issues remain open. Independent anatomical review is still required.

## Reproducing the modelling

`tools/ica-cs-v0932` contains the source-derived centreline inputs, reconstruction, joint fitting, venous network, grafting, validation, rendering and export scripts. `prepare.py` decodes the v0.9.31 vascular baselines supplied separately as `ICA_CS_source_baselines_v0.9.31.zip` together with the unchanged production bone/brain. The Python modelling workflow requires NumPy, SciPy, VTK and Matplotlib. The app itself needs only the existing npm/Docker workflow.

Run the stages in the order documented in `tools/ica-cs-v0932/README.md`. Large distance grids and decoded buffers are temporary work products and are omitted from the release. The accepted geometry and all measured evidence are included.
