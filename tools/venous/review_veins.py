import json
import numpy as np
from reference import *
APP=ROOT.parents[1]
spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text());ids=[s['id'] for s in spec['structures']]
data=np.load(ROOT/'venous-mesh.npz');p=data['positions'];f=data['faces'];labels=data['labels']
paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
items=[]
for i,s in enumerate(spec['structures']):
 c=s['color'];col=tuple(int(c[j:j+2],16)/255 for j in [1,3,5]);pd=poly(p,f[labels==i]);pd.GetPointData().SetNormals(numpy_to_vtk(data['normals'],deep=True));items.append((pd,col,1))
skull=bone_surface()
render(items,ROOT/'veins-right.png',view=(1,0,0),center=(0,-65,35),scale=140)
render(items,ROOT/'veins-front.png',view=(0,1,0),center=(0,-65,35),scale=140)
render(items+[(skull,(.8,.75,.65),.08)],ROOT/'veins-context.png',view=(1,.45,.15),center=(0,-65,65),scale=115)
deep=[it for it,s in zip(items,spec['structures']) if s['group'] in ['deep','posterior'] or s['id'].startswith(('vein.straight','vein.cavernous','vein.superior_petrosal','vein.inferior_petrosal'))]
render(deep,ROOT/'veins-deep.png',view=(1,.6,.35),center=(0,-75,84),scale=58)
print('Rendered',flush=True)
report=[]
for rec in records:
 if rec['file']!='craniofacial' or 'tooth' in rec['name']:continue
 bp,bf=arrays(rec);pd=poly(bp,bf);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(pd)
 lo,hi=np.array(rec['bounds']);
 for path in paths:
  q=np.array(path['points']);r=np.array(path['radii']);mask=np.all((q>=lo-r[:,None])&(q<=hi+r[:,None]),axis=1)
  candidates=np.flatnonzero(mask)
  if not len(candidates):continue
  dd=np.array([sdf.EvaluateFunction(q[i]) for i in candidates]);bad=candidates[dd<r[candidates]-.1]
  if len(bad):report.append({'id':path['id'],'bone':rec['name'],'samples':len(bad),'inside':int(np.sum(dd<-.1)),'min_signed_distance':float(dd.min()),'point':q[candidates[np.argmin(dd)]].round(3).tolist()})
(ROOT/'veins-bone-review.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
