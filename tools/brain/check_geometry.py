"""Authoring QA for registered geometry and retained baseline assets."""
from pathlib import Path
import sys,json,hashlib,zipfile
import numpy as np,trimesh,vtk
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'venous'))
from reference import bone_surface
APP=Path(__file__).resolve().parents[2];root=APP.parent;manifest=json.loads((APP/'public/anatomy/manifest.json').read_text());brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',force='scene');reg=json.loads((APP/'anatomy/source/brain/registration.json').read_text());report={'release':'0.9.14','registration':reg,'surfaces':len(brain.geometry),'triangles':sum(len(m.faces) for m in brain.geometry.values()),'baseline_asset_hashes':{}}
with zipfile.ZipFile(root/'baseline/inr-anatomy-atlas-v0.9.13.zip') as z:
 for name in z.namelist():
  if name.startswith('public/anatomy/models/') and name.endswith('.glb'):
   old=hashlib.sha256(z.read(name)).hexdigest();new=hashlib.sha256((APP/name).read_bytes()).hexdigest();assert old==new,name;report['baseline_asset_hashes'][name]=new
 old=json.loads(z.read('anatomy/generated/complete_manifest.json'));rows={s['id']:s for s in manifest['structures']}
 assert all(s==rows[s['id']] for s in old['structures']);assert all(r in manifest['relationships'] for r in old['relationships']);report['baseline_catalogue_preserved']=True
for s in manifest['structures']:
 if not s.get('anatomy'):continue
 m=brain.geometry[s['id']];assert np.isfinite(m.vertices).all();assert m.faces.max()<len(m.vertices)
 if s['side']=='left':assert m.centroid[0]<.7,s['id']
 if s['side']=='right':assert m.centroid[0]>.5,s['id']
report['laterality']='All sided mesh centroids retain RAS laterality'
loc=vtk.vtkStaticCellLocator();loc.SetDataSet(bone_surface());loc.BuildLocator();near={}
for category in ['cerebral_cortex','cerebellum','brainstem','dural_reflections']:
 vertices=np.concatenate([brain.geometry[s['id']].vertices for s in manifest['structures'] if s.get('anatomy',{}).get('category')==category]);vertices=vertices[::max(1,len(vertices)//5000)];dist=[]
 for p in vertices:
  q=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);d=vtk.reference(0.);loc.FindClosestPoint(p,q,ci,sub,d);dist.append(float(d)**.5)
 near[category]={'sampled_vertices':len(dist),'minimum_skull_surface_distance_mm':min(dist),'median_skull_surface_distance_mm':float(np.median(dist)),'within_0_5_mm_count':sum(d<.5 for d in dist)}
report['sampled_skull_proximity']=near;report['scope']='Shared atlas registration. Nearest-vertex skull registration residuals and sampled surface proximity are not patient accuracy estimates or exhaustive intersection tests. Visual review includes AP, lateral section, superior and posterior fossa views.'
(APP/'docs/validation/brain-registration-v0.9.14.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
