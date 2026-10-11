"""Move cavernous collaterals to the medial, dural side of the temporal pole.

This direction follows the lateral cavernous wall rather than diving farther
down through temporal cortex. Native shared attachments are transferred to
their partner with a smooth collar. All affected partners require validation.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
current=lambda n:load(n,OUT)if n in changed else load(n)
neighbours=[(n,*current(n))for n in FILES if n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'))]
def collision_ids(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
 return vtk_to_numpy(c.GetContactCells(0)).astype(int)if c.GetNumberOfContacts()else np.empty(0,int)
def save(n,v,f):
 write(n,v,f);sv,sf=load(n);row=dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=np.array_equal(f,sf),field='cavernous-dural-course',maxShiftMm=float(np.linalg.norm(v-sv,axis=1).max()))
 for i,r in enumerate(rev['changed']):
  if r['node']==n:rev['changed'][i]=row;break
 else:rev['changed'].append(row)
 changed.add(n)
def propagate(n,w):
 sv,_=load(n);keys={bytes(k):i for i,k in enumerate(np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel())};updates=[]
 for other in FILES:
  if other==n:continue
  ov,of=load(other);ii=[];jj=[]
  for j,k in enumerate(np.ascontiguousarray(ov.astype('<f4')).view('V12').ravel()):
   if bytes(k)in keys:jj.append(j);ii.append(keys[bytes(k)])
  if not jj:continue
  v,f=current(other);jj=np.array(jj);ii=np.array(ii);shift=w[ii]-v[jj]
  if np.max(np.linalg.norm(shift,axis=1))<1e-5:continue
  dd,idx=cKDTree(v[jj]).query(v);weight=1-smooth(dd/6.);nv=v+shift[idx]*weight[:,None];nv[jj]=w[ii];save(other,nv,f);updates.append(other)
 return updates
reports=[]
for side,sign in [('right',1),('left',-1)]:
 for prefix in ['MMA posterior cavernous ','MMA cavernous–ILT ']:
  if '--left-floor'in sys.argv and(side!='left'or prefix!='MMA posterior cavernous '):continue
  n=prefix+side;v,f=current(n);x=np.load(WORK.parent/'work-v0956-outward'/(n+'.curve.npz'));par=x['param'];tt=x['tt'];shift=np.zeros(len(tt));history=[]
  direction=np.array([0.,0.,-1.])if '--left-floor'in sys.argv else np.array([-sign,0.,0.])
  for it in range(60):
   w=v+np.interp(par,tt,shift)[:,None]*direction;lo=w.min(0)-.05;hi=w.max(0)+.05;hit=[];pairs=[]
   for bn,bv,bf in neighbours:
    if np.any(bv.max(0)<lo)or np.any(bv.min(0)>hi):continue
    tri=bv[bf];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);ids=collision_ids(w,f,bv,bf[take])
    if len(ids):hit.extend(par[f[ids]].ravel());pairs.append(dict(brain=bn,triangleContacts=len(ids)))
   history.append(dict(iteration=it,pairs=pairs,maximumAdditionalShiftMm=float(shift.max())))
   if not hit:break
   ids=np.unique(np.searchsorted(tt,np.clip(hit,tt[0],tt[-1])));active=np.zeros(len(tt));active[ids]=1.;active=maximum_filter1d(active,size=max(3,int(1.5/np.median(np.diff(tt)))));active=gaussian_filter1d(active,1.5/np.median(np.diff(tt)));active/=max(active.max(),1e-10)
   shift=np.minimum(shift+.10*active,4.);shift=gaussian_filter1d(shift,.25/np.median(np.diff(tt)))
  save(n,w,f);updates=propagate(n,w);row=dict(node=n,passed=not history[-1]['pairs'],partners=updates,history=history);reports.append(row);print(n,history[-1],flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'cavernous-route-fit.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
