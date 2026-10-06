"""Package the accepted context adjustment as an explicitly partial review build.

Failed vessel fits and wider registration candidates are never applied. Every
surface anchor is rebound to the delivered triangle buffer and hash.
"""
import copy,json,hashlib,shutil,zipfile,numpy as np,trimesh,vtk
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap
from build_targets import poly
from reconcile_brainstem import sha
W=APP/'.authoring/brainstem20-lower-final';PUB=APP/'public/anatomy';VERSION='0.9.19'
accept=json.loads((W/'context-validation.json').read_text());assert accept['passed'] and not accept['failures'];assert accept['brainCandidateSha256']==sha(W/'brain-trial.glb');assert accept['brainSourceSha256']==sha(W/'brain-source-refined.glb');assert next(r for r in accept['clivalContacts'] if r[0]=='vein.basilar_plexus')[2]==0
registration=json.loads((W/'registration.json').read_text());assert registration['brainSha256']==accept['brainCandidateSha256']
v=np.load(W/'volume-map.npz');mapping=VolumeMap.__new__(VolumeMap);mapping.origin=v['origin'];mapping.delta=v['delta'];mapping.mask=v['mask'];mapping.shape=np.array(mapping.delta.shape)
baseline=APP/'../recovered/inr-anatomy-atlas-v0.9.18.zip'
with zipfile.ZipFile(baseline) as archive:manifest=json.loads(archive.read('anatomy/generated/complete_manifest.json'))
brain=trimesh.load(W/'brain-trial.glb',process=False);hash_=sha(W/'brain-trial.glb');changed={r['node'] for r in registration['changes']};locators={}
def rebind(anchor):
 target=anchor['structureId'];m=brain.geometry[target]
 if target not in locators:
  loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(m));loc.BuildLocator();locators[target]=loc
 query=mapping.apply(np.array([anchor['position']]))[0] if target in changed else anchor['position'];closest=[0.,0.,0.];cell,sub,distance=vtk.reference(0),vtk.reference(0),vtk.reference(0.);locators[target].FindClosestPoint(query,closest,cell,sub,distance)
 tri=int(cell);weights=trimesh.triangles.points_to_barycentric(m.vertices[m.faces[[tri]]],np.array([closest]))[0];weights=np.clip(weights,0,1);weights/=weights.sum();anchor.update(triangleIndex=tri,barycentric=weights.tolist(),position=(weights@m.vertices[m.faces[tri]]).tolist(),assetSha256=hash_)
for s in manifest['structures']:
 if s.get('surfaceAnchor'):
  rebind(s['surfaceAnchor']);s['landmark']['point']=s['surfaceAnchor']['position']
 for anchor in s.get('secondarySurfaceAnchors',[]):rebind(anchor)
rows={r['id']:r for r in manifest['structures']}
for s in manifest['structures']:
 guide=s.get('vesselGuide');landmark=s.get('landmark')
 if guide and guide.get('anchorIds'):
  landmark['course']=[rows[k]['surfaceAnchor']['position'] for k in guide['anchorIds']];landmark['point']=landmark['course'][0]
 elif guide and not s.get('surfaceAnchor') and any(k in changed for k in guide.get('surfaceStructureIds',[])) and landmark:
  if landmark.get('point'):landmark['point']=mapping.apply(np.array([landmark['point']]))[0].tolist()
  if landmark.get('course'):landmark['course']=mapping.apply(np.array(landmark['course'])).tolist()
 course=s.get('vesselCourse')
 if course:course['brainAssetSha256']=hash_
manifest['release']=VERSION;manifest['releaseChannel']='anatomical-review';manifest['brainRegistration']['registeredAssetSha256']=hash_
manifest['brainRegistration']['regionalAdjustments']=[{'release':VERSION,'requestedAPScale':.94,'requestedSagittalRotationDegrees':-2,'fieldSha256':sha(W/'volume-map.npz'),'method':registration['method'],'contextEvidence':'docs/validation/brainstem-context-v0.9.19.json'}]
manifest['brainAdjustmentPolicy']['scope']='Local shape and size registration of brain structures, with vessel fitting assessed separately'
manifest['brainAdjustmentPolicy']['preserve']=['overall skull registration','regional anatomical shape and neighbouring interfaces','sulcal banks and ventricular relationships']
manifest['brainAdjustmentPolicy']['appliedAdjustments']=[{'release':VERSION,'status':'context-adjustment-awaiting-anatomical-review','geometry':registration['changes'],'maximumDisplacementMm':registration['maximumDisplacementMm'],'requestedAPScale':.94,'completeVenousRefitApplied':False}]
manifest['assetRevisions']['models/brain-context.glb']=hash_[:20]
manifest['vesselCourseState']='partially-fitted-awaiting-review'
# Retained vessel asset identities must remain exact. Failed fits are excluded.
for name in ['venous.glb','complete-circulation.glb','craniofacial.glb','complete-anastomoses.glb']:
 baseline=APP/'../recovered/inr-anatomy-atlas-v0.9.18.zip'
 import zipfile
 with zipfile.ZipFile(baseline) as z:assert hashlib.sha256(z.read('public/anatomy/models/'+name)).hexdigest()==sha(PUB/'models'/name),name
shutil.copyfile(W/'brain-trial.glb',PUB/'models/brain-context.glb')
(APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
landmarks=json.loads((PUB/'brain-landmarks.json').read_text());landmarks['registration']=manifest['brainRegistration'];landmarks['anchors']=[r for r in manifest['structures'] if r.get('landmark') and r['system']=='brain'];(PUB/'brain-landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
courses=json.loads((PUB/'vessel-courses.json').read_text());courses.update(release=VERSION,brainRegistration=manifest['brainRegistration'],courses=[r['vesselCourse'] for r in manifest['structures'] if r.get('vesselCourse')]);(PUB/'vessel-courses.json').write_text(json.dumps(courses,indent=2)+'\n')
for file in ['package.json','package-lock.json']:
 p=APP/file;data=json.loads(p.read_text());data['version']=VERSION
 if file=='package-lock.json':data['packages']['']['version']=VERSION
 p.write_text(json.dumps(data,indent=2)+'\n')
shutil.copyfile(W/'context-validation.json',APP/'docs/validation/brainstem-context-v0.9.19.json');shutil.copyfile(W/'registration.json',APP/'docs/validation/brainstem-registration-v0.9.19.json')
report={'release':VERSION,'channel':'anatomical-review','baseline':'0.9.18','appliedToApp':True,'appliedGroups':['lower-brainstem-context-size-registration'],'complete':False,'deferredGroups':['anterior-brainstem-vein-refit','posterior-arterial-transport','wider-upper-brainstem-registration'],'brainAssetSha256':hash_,'brainContextChecksPassed':True,'clivalPlexusTriangleContactsAfter':0,'vesselAssetsRetainedExactly':True,'limitations':['The model is a composite atlas, not patient-specific anatomy.','Complete venous routing is unresolved. The solver could not fit the full anterior/transverse venous system with its existing fixed collectors.','The failed posterior arterial transport and wider context candidates are excluded. Existing arterial and venous anatomy requires further fitting to the adjusted context.','Open atlas cut surfaces do not establish solid containment.','Context checks pass independently of complete vascular fitting; this is a partial review build.']}
(APP/'docs/validation/brainstem-review-v0.9.19.json').write_text(json.dumps(report,indent=2)+'\n');print('Published partial context review build; all failed vascular and wider context candidates excluded.',flush=True)
