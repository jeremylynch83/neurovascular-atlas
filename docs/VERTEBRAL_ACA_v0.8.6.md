# Vertebral and ACA sections, v0.8.6

**Superseded VA station placement:** The V2/V3 and V3/V4 stations from this release were corrected in v0.8.9 against the supplied annotated diagram. The definitions below remain applicable; ACA stations are unchanged. See VERTEBRAL_v0.8.9.md.

Both vertebral arteries now have selectable V1–V4 sections. Both ACAs have
selectable A1–A5 sections. The section definitions and descriptions follow
the supplied `nv(2).pdf`, printed pages 40–43 and 47–48, including Figures
2.10 and 2.13. Descriptions retain the notes' wording and clickable links.

| Section | Definition from the notes |
| --- | --- |
| V1, preforaminal | Proximal course until transverse-foramen entry, typically C6 |
| V2, foraminal | Ascending course to the C2 transverse foramina |
| V3, extracranial | From C2 through C1 and the atlas groove to dural entry |
| V4, intracranial | Intradural course to the vertebrobasilar junction |
| A1, pre-communicating | ICA to ACOM, directed forwards and medially |
| A2, post-communicating | Distal to ACOM to the rostrum/genu junction |
| A3, precallosal | Around the genu of the corpus callosum |
| A4, supracallosal | From the body of the corpus callosum to coronal-suture level |
| A5, postcallosal | Continuation posterior to the coronal suture |

## Model boundaries

This release partitions the retained vessel surfaces. It does not redirect
their courses or alter calibre. The existing A1 surfaces and shared terminal
ICA junction are unchanged. The four original vertebral/pericallosal meshes
are split by assigning each original triangle to one section; no caps or
internal faces are added. Boundary vertices retain their exact positions
and normals, including on both sides of each section join.

The model has no registered cervical vertebrae, corpus callosum or coronal
suture. V1/V2 uses the retained reference course's estimated C6-entry station;
V2/V3 uses its estimated C2 station; V3/V4 uses its estimated dural-entry
station near the foramen magnum. V1 remains truncated without a reconstructed
subclavian origin. A2–A5 promote the existing documented station plan
(24%, 39% and 70% of distal ACA arc). The A4/A5 station represents an estimated
coronal-suture level. These are reference estimates, not measured tissue
boundaries. Exact stations and source paths are recorded in
`validation/vertebral-aca-sections.json`.

Branches are nested under the section containing their retained attachment.
Orbitofrontal, frontopolar and recurrent Heubner branches are under A2;
callosomarginal is under A3. The model retains its permitted direct
pericallosal paracentral origin. The upper-cervical odontoid contributor
retains its existing estimated-level qualification; this release does not
claim it is a registered C3 origin or move it into a different cervical level.

## Selection and visibility

The whole ACA sits beneath the ICA terminus. A1 and the distal pericallosal
group sit beneath the ACA; A2–A5 sit beneath the distal group. Existing A1,
pericallosal and vertebral IDs remain valid, preserving description links.
Whole-vessel focus and highlight include the vessel's sections, without
highlighting its ordinary branches. Visibility checkboxes retain subtree
behaviour. Each individual section can be selected, focused and hidden.

## Verification

- All 18 bilateral sections load through the actual Three.js GLTFLoader and
  are individually picked by the actual raycaster with the full model present.
- Individual and whole-artery focus, highlight, subtree hiding and nested
  pericallosal grouping pass the engine checks.
- Each partitioned surface contains exactly the same triangle positions and
  normals as its source. All 583 other circulation meshes retain every
  attribute and index byte. The other two GLB files are byte-identical.
- The atlas still has 6,442,421 triangles. The 766 opaque vascular sections
  and branches retain the existing batch, with 61 default mesh draw objects
  including bone context. No GPU FPS improvement is claimed for segmentation.
- All 735 descriptions and 1,758 clickable links pass the component checks;
  the reviewed Markdown catalogue matches the manifest exactly.
- Production builds pass for the local root and GitHub Pages subpath.

The checks use the actual loader, geometry, raycaster and React handlers,
with a test renderer and hook fixture. They are not a full browser/GPU test
or a new recurring anatomical validation pipeline.
