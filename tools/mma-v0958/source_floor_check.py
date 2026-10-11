"""Quantify native cortex/bone penetrations at the cranial floor."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
targets=['orbital-gyri','temporal-pole','medial-occipitotemporal-gyrus-parahippocampal']
rows=[]
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
for side in ['right','left']:
 for target in targets:
  n='brain.'+target+'.'+side;v,f=load(n,OUT)if '--candidate'in sys.argv and n in changed else load(n)
  for bn in ['bone.sphenoid','bone.frontal','bone.temporal.'+side]:
   bv,bf=load(bn);c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(bv,bf));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update();nc=c.GetNumberOfContacts()
   fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(bv,bf));ids=np.flatnonzero(np.all(v>=bv.min(0)-.1,axis=1)&np.all(v<=bv.max(0)+.1,axis=1));d=np.full(len(v),10.);d[ids]=[fn.EvaluateFunction(p)for p in v[ids]];inside=d<0
   row=dict(brain=n,bone=bn,triangleContacts=nc,sourceVerticesInsideBone=int(inside.sum()),maxPenetrationMm=float(-min(d.min(),0)),insideBounds=[v[inside].min(0).tolist(),v[inside].max(0).tolist()]if inside.any()else None)
   rows.append(row);print(row,flush=True)
   np.savez_compressed(WORK/(n+'--'+bn+('.candidate'if '--candidate'in sys.argv else '')+'.floor-check.npz'),d=d)
(WORK/('candidate-floor-check.json'if '--candidate'in sys.argv else 'source-floor-check.json')).write_text(json.dumps(rows,indent=2))
