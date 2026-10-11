"""Fit the entire connected venous exterior against the corrected scene.

The native cavernous ports remain fixed. Small smooth signed-distance steps
act on a shared surface, avoiding four disconnected receiver overlaps.
This remains a trial until independent triangle/fold checks pass.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.spatial.distance import cdist
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/self_check.py').read_text());exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='intersections'],type_ignores=[]),'folds','exec'))
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
def hit(v,f,w,g):
 ids=None
 if '--spatial'in sys.argv:
  tri=v[f];other=w[g];lo=other.min((0,1))-1e-7;hi=other.max((0,1))+1e-7;ids=np.flatnonzero(np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1))
  if not len(ids):return np.empty(0,int)
  f=f[ids]
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
 cells=vtk_to_numpy(c.GetContactCells(0)).astype(int)if c.GetNumberOfContacts()else np.empty(0,int)
 return ids[cells]if ids is not None else cells
reports=[]
for side in ['right','left']:
 x=np.load(OUT/('receiver-seam-completed-'+side+'.npz'));v=x['v'].astype(float);f=x['f'];initial=v.copy();lo=v.min(0)-4;hi=v.max(0)+4;ob=[]
 for n in FILES:
  neural=n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'));arterial=FILES[n]in ['complete-circulation.glb','complete-anastomoses.glb']
  if not(neural or arterial):continue
  w,g=load(n,OUT)if n in changed else load(n)
  if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
  tri=w[g];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);g=g[take]
  if not len(g):continue
  fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(w,g));ob.append((n,w,g,fn,neural))
 history=[]
 for it in range(70):
  controls=[];vectors=[];rows=[]
  for n,w,g,fn,neural in ob:
   ids=hit(v,f,w,g)
   if not len(ids):continue
   rows.append(dict(other=n,triangleContacts=len(ids)));pts=np.unique(np.vstack([v[np.unique(f[ids])],v[f[ids]].mean(1)]),axis=0);ds=np.array([fn.EvaluateFunction(p)for p in pts]);gr=[]
   for p in pts:
    a=[0.,0.,0.];fn.EvaluateGradient(p,a);a=np.asarray(a);a/=max(np.linalg.norm(a),1e-8);gr.append(a)
   delta=np.asarray(gr)*np.minimum(np.maximum(.16-ds,.02),.14 if '--spatial'in sys.argv else .08)[:,None];controls.append(pts);vectors.append(delta)
  row=dict(iteration=it,contacts=rows,maximumDisplacementMm=float(np.linalg.norm(v-initial,axis=1).max()));history.append(row);print(side,it,row,flush=True)
  if not rows:break
  pts=np.vstack(controls);delta=np.vstack(vectors)
  if '--fast'in sys.argv or '--spatial'in sys.argv:
   cells=np.floor(pts/.20).astype(int);_,ii=np.unique(cells,axis=0,return_index=True);pts=pts[ii];delta=delta[ii]
  for start in range(0,len(v),1200):
   p=v[start:start+1200];dd=cdist(p,pts);weight=np.exp(-dd**2/(2*.8**2));taper=smooth((3-dd.min(1))/2.2)*smooth((abs(p[:,0])-18)/8)
   v[start:start+len(p)]+=(weight@delta)/np.maximum(weight.sum(1)[:,None],1e-30)*taper[:,None]
 before=intersections(initial,f);after=intersections(v,f);new=after-before
 suffix='-spatial'if '--spatial'in sys.argv else '-fast'if '--fast'in sys.argv else ''
 np.savez_compressed(OUT/('receiver-common-wall-fit'+suffix+'-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'))
 reports.append(dict(side=side,passed=not history[-1]['contacts']and not new,newFoldPairs=len(new),maximumDisplacementMm=float(np.linalg.norm(v-initial,axis=1).max()),history=history,installed=False))
(OUT/('receiver-common-wall-fit'+suffix+'-validation.json')).write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
