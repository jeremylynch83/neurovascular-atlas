from common import *
x=json.loads((OUT/'courses.json').read_text());targets=['brain.pons.left','brain.pons.right','brain.medulla-oblongata.left','brain.medulla-oblongata.right','brain.midbrain.left','brain.midbrain.right','brain.upper-cervical-cord'];fields={}
for k in targets:
 field=vtk.vtkImplicitPolyDataDistance();field.SetInput(meshes[k].pd);fields[k]=field
report=[]
for row in x['structures']:
 if row['mode'] not in ['bridging','pial','cisternal']:continue
 for part in row['parts']:
  q=np.array(part['points']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];mask=(arc>3)&(arc<arc[-1]-3)
  if not mask.any():continue
  for k,field in fields.items():
   if np.any(q[mask].max(0)<meshes[k].bounds[0]) or np.any(q[mask].min(0)>meshes[k].bounds[1]):continue
   d=np.array([field.EvaluateFunction(p) for p in q[mask]]);minimum=float(d.min())
   if minimum<-.03:report.append({'vein':row['id'],'target':k,'minimumCentrelineSignedDistanceMm':minimum,'insideSamples':int((d<-.03).sum())})
(OUT/'brainstem-body-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('Brainstem body entries',len(report));print(report)
