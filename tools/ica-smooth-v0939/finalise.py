from model import *
import hashlib,shutil

validation=json.loads((OUT/'validation.json').read_text())
selfcheck=json.loads((OUT/'self-intersections.json').read_text())
origins=json.loads((OUT/'origin-restoration.json').read_text())
for row in validation:
 assert row['topologyAfter']['components']==1
 assert row['topologyAfter']['nonManifoldEdges']==0
 assert row['nativeExternalBoundariesExact']
 assert row['mainIcaSinusContacts']==0
for row in selfcheck:
 assert row['intersectionsInvolvingChangedTriangles']==0,row
for row in origins:
 assert row['centroidDisplacementMm']<.000001
 assert row['nativeExternalBoundaryVerticesExact']

revision=json.loads((OUT/'revision.json').read_text())
m=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text())
m['release']='0.9.39'
m['icaSurfaceSmoothing']={'version':'0.9.39','baseline':'0.9.38','method':'Connected tubular surface remeshing, local branch collars and continuous shared normals; fixed ophthalmic origin centres','reviewStatus':'requires-anatomical-review','evidence':'docs/ICA_SMOOTH_v0.9.39.md','validation':'anatomy/source/ica-smooth-v0939/validation.json'}
hashes={'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (APP/'public/anatomy/models').glob('*.glb')}
m['assetRevisions']={k:v[:20] for k,v in hashes.items()}
m['assetByteSizes']={k:(APP/'public/anatomy'/k).stat().st_size for k in hashes}
for s in m['structures']:
 if s.get('vesselCourse'):s['vesselCourse']['geometrySha256']=hashes[s['asset']['file']]
(APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
c=json.loads((APP/'public/anatomy/vessel-courses.json').read_text());c['release']='0.9.39';c['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')]
(APP/'public/anatomy/vessel-courses.json').write_text(json.dumps(c,indent=2)+'\n')
dest=APP/'anatomy/source/ica-smooth-v0939';dest.mkdir(exist_ok=True)
for p in OUT.glob('*.json'):shutil.copy2(p,dest/p.name)
doc='''# ICA surface smoothing v0.9.39

Based on v0.9.38. Rebuilds the petrous/cavernous/paraophthalmic ICA surfaces and the adjoining ophthalmic, superior hypophyseal, inferolateral and meningohypophyseal branch junctions on both sides. The meningohypophyseal stem and its four proximal branch necks are reconstructed together. All 22 named surfaces remain selectable.

One continuous implicit surface is partitioned into the existing labels, then grafted onto the native distal surfaces. A local ring selection fixes the prior distant tentorial collar error. Shared surface normals remove shading seams. The short petrous collars are locally rounded. Ophthalmic ostium centroids match the original positions to within 0.000001 mm after float32 export; their individual ostial vertices have been remeshed.

## Validation

- Each bilateral cohort is one connected surface, with zero non-manifold edges.
- All native outer boundary edges are preserved exactly.
- No ICA/cavernous sinus wall contacts in the checked region.
- No intersections involving changed triangles in the checked region.
- Existing lower petrous bone contacts are retained outside the rebuilt surface.
- The check also detects retained distal branch self-intersections: 116 on the right and 97 on the left. These occur in retained native branch triangles and are not closed by this local ICA junction repair. The entire atlas has not passed a global intersection or anatomical accuracy gate.

Positions and indices are checked against the actual Three.js GLTFLoader output. The production build validates the structure catalogue and course metadata. Bone, brain, venous geometry, vein/artery colours, startup vein visibility and author credits are retained from v0.9.38.

## Reproduction

The modelling scripts require NumPy, SciPy and VTK. Decode the v0.9.38 arterial baseline into `decoded` and retain its exact GLB in `baseline`, then run `repair.py`, `restore_origins.py`, `validate.py`, `selfcheck.py`, `decode_normals.mjs`, `orient_surfaces.py`, `export.mjs`, `finalise.py`, the production build and `check_export.mjs`. The input archive and large intermediate buffers are excluded from the release. The JSON evidence and matched lateral/oblique renders are included.

This is a reference model for expert anatomical review. No vessel course redesign or new anatomical claim is introduced.
'''
doc=doc.replace('116 on the right and 97 on the left',str(selfcheck[0]['retainedNativeTriangleIntersections'])+' on the right and '+str(selfcheck[1]['retainedNativeTriangleIntersections'])+' on the left')
(APP/'docs/ICA_SMOOTH_v0.9.39.md').write_text(doc)
(APP/'README.txt').write_text('Neurovascular Atlas v0.9.39\n\nBilateral ICA and branch-junction smoothing. See docs/ICA_SMOOTH_v0.9.39.md for validation and limits. Put the ZIP beside the existing inr-anatomy.sh and run it as before.\n')
p=APP/'README.md';existing=p.read_text();existing=existing[existing.index('# Neurovascular Atlas v0.9.32'):]
p.write_text('# Neurovascular Atlas v0.9.39\n\nFinishes bilateral ICA surface and branch-collar smoothing. Both sides retain their native outer attachments and fixed ophthalmic origin centres. No new self-intersections or cavernous sinus wall contacts were detected in the checked region. Existing distal hypophyseal self-intersections remain documented. [Method, checks and renders](docs/ICA_SMOOTH_v0.9.39.md).\n\n'+existing)
print('Finalised v0.9.39')
