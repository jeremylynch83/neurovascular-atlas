"""Resolve actual companion-vein brain intersections towards the lateral skull.

The native receiver endpoints remain fixed. Common receiver exterior creation
is a separate required operation, so mutual stem overlaps remain provisional.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
from scipy.ndimage import gaussian_filter
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/build_paired_veins.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef) and x.name=='solid'],type_ignores=[]),'solid','exec'))
def hits(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.Update()
 return vtk_to_numpy(c.GetContactCells(0)).astype(int) if c.GetNumberOfContacts() else np.empty(0,int)
brain=[(n,*load(n))for n in FILES if n.startswith('brain.') and not n.startswith(('brain.tentorium','brain.falx'))]
rev=json.loads((OUT/'revision.json').read_text());rows=json.loads((OUT/'paired-channel-candidates.json').read_text())['channels'];reports=[]
for side in ['right','left']:
 n='vein.middle_meningeal.posterior.'+side;source=np.load(OUT/(n+'.curve.npz'));q=source['q'].copy();r=source['r'];stem=source['stem'].copy();original=q.copy();oldstem=stem.copy();j=cKDTree(q).query(stem[0])[1];direction=np.array([1 if side=='right' else -1,0,0]);history=[]
 for iteration in range(24):
  v,f=load(n,OUT) if iteration==0 else solid([(q,r),(stem,np.full(len(stem),.23))])
  lo=v.min(0)-.01;hi=v.max(0)+.01;pts=[];pairs=[]
  for bn,bv,bf in brain:
   if np.any(bv.max(0)<lo)or np.any(bv.min(0)>hi):continue
   tri=bv[bf];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);ids=hits(v,f,bv,bf[take])
   if len(ids):pts.append(v[f[ids]].reshape(-1,3));pairs.append(dict(other=bn,triangleContacts=len(ids)))
  history.append(dict(iteration=iteration,contacts=pairs,maximumShiftMm=float(np.linalg.norm(q-original,axis=1).max())))
  print(n,iteration,history[-1],flush=True)
  if not pts:break
  ht=cKDTree(np.vstack(pts));dd=ht.query(q)[0];sd=ht.query(stem)[0]
  dq=.16*np.exp(-dd**2/(2*.8**2));ds=.16*np.exp(-sd**2/(2*.8**2));ds*=smooth(np.linalg.norm(stem-oldstem[-1],axis=1)/1.)
  q+=dq[:,None]*direction;stem+=ds[:,None]*direction;stem[0]=q[j];stem[-1]=oldstem[-1]
  if np.linalg.norm(q-original,axis=1).max()>3:break
 if history[-1]['contacts']:
  reports.append(dict(node=n,applied=False,history=history));continue
 write(n,v,f);np.savez(OUT/(n+'.curve.npz'),q=q,r=r,stem=stem)
 for row in rows:
  if row['node']==n:row.update(vertices=len(v),triangles=len(f),additionalLateralAdjustmentMm=float(np.linalg.norm(q-original,axis=1).max()))
 for row in rev['changed']:
  if row['node']==n:row.update(vertices=len(v),triangles=len(f),field='contact-driven-lateral-companion-correction')
 reports.append(dict(node=n,applied=True,history=history))
(OUT/'paired-channel-candidates.json').write_text(json.dumps(dict(status='provisional-not-exported',channels=rows,duplicatedLesserWingChannel=False,receiverExteriorMerged=False),indent=2));(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'companion-neural-corrections.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
