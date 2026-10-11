"""Bounded, profile-preserving route trials with simultaneous obstacle gates.

Use the existing falx and tentorial sheets as references. Keep delivered ports
and native shared coordinates fixed. Reject neural intersections, new folds,
new arterial/bone/venous contacts and strict closed-parcel containment.
Every trial is checked after float32 export rounding, before installation.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0959'))
from route_tools import *
from scipy.ndimage import gaussian_filter1d

baseline=WORK.parent/'work-v0959/candidate'
meshes={n:current(n) for n in FILES}
bounds={n:(v.min(0),v.max(0)) for n,(v,f) in meshes.items()}
oldpairs={}
oldfolds={}
eligible={r['node'] for r in json.loads((OUT/'mma-neural-containment-screen.json').read_text())['brainTopology'] if r['eligibleForContainmentScreen']}
enclosed={}
history=[]

def strict_inside(w):
 hits=[]
 for n in eligible:
  lo,hi=bounds[n];take=np.flatnonzero(np.all(w>=lo,axis=1)&np.all(w<=hi,axis=1))
  if not len(take):continue
  if n not in enclosed:
   v,f=meshes[n];vv,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True);sf=poly(vv.astype(float),inv[f]);dist=vtk.vtkImplicitPolyDataDistance();dist.SetInput(sf);enclosed[n]=(sf,dist)
  sf,dist=enclosed[n];pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(w[take],deep=True));inp=vtk.vtkPolyData();inp.SetPoints(pts)
  s=vtk.vtkSelectEnclosedPoints();s.SetInputData(inp);s.SetSurfaceData(sf);s.SetTolerance(1e-8);s.CheckSurfaceOn();s.Update();inside=vtk_to_numpy(s.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
  ids=take[inside];depth=np.array([abs(dist.EvaluateFunction(w[i])) for i in ids]);depth=depth[depth>.02]
  if len(depth):hits.append(dict(brain=n,vertices=len(depth),maximumDepthMm=float(depth.max())))
 return hits

def gates(n,w,f):
 nh=neural(w,f)
 if nh:return dict(neural=nh,passed=False)
 inside=strict_inside(w)
 if inside:return dict(containment=inside,passed=False)
 if n not in oldfolds:oldfolds[n]=intersections(*load(n))
 nf=intersections(w,f)-oldfolds[n]
 if nf:return dict(newFolds=len(nf),passed=False)
 lo,hi=w.min(0)-.05,w.max(0)+.05;new=[];existing=[]
 for other,(v,g) in meshes.items():
  if other==n or other.startswith('brain.'):continue
  ol,oh=bounds[other]
  if np.any(oh<lo) or np.any(ol>hi):continue
  c=contacts(w,f,v,g)
  if not c:continue
  key=(n,other)
  if key not in oldpairs:oldpairs[key]=contacts(*load(n,baseline),v,g)
  row=dict(other=other,triangleContacts=c,previousTriangleContacts=oldpairs[key])
  (new if not oldpairs[key] else existing).append(row)
 return dict(neural=[],containment=[],newFolds=0,newContacts=new,existingContacts=existing,passed=not new)

def attempt(n,v,f,q,new,param,tt,r,settings):
 pin=pins(n);near=np.minimum(tt-tt[0],tt[-1]-tt)
 rotation=smooth((near-settings.get('rotationPortMm',.5))/1.)
 w,old,newp=tube(v,q,new,param,tt,rotation);w[pin]=v[pin];w=w.astype('<f4').astype(float)
 error=abs(np.linalg.norm(v-old,axis=1)-np.linalg.norm(w-newp,axis=1));free=~pin
 row=dict(node=n,settings=settings,maximumShiftMm=float(np.linalg.norm(w-v,axis=1).max()),maximumFreeProfileErrorMm=float(error[free].max()),nativePinsExact=bool(np.array_equal(w[pin],v[pin])))
 row.update(gates(n,w,f));row['passed']=row['passed'] and row['nativePinsExact'] and row['maximumFreeProfileErrorMm']<1e-4
 history.append(row)
 if row['passed']:
  save(n,w,f,'simultaneous-gates-profile-preserving-dural-reconstruction')
  np.savez_compressed(WORK/(n+'.v0960-curve.npz'),q=new,r=r,param=param,tt=tt,rotationWeight=rotation)
  meshes[n]=(w,f);bounds[n]=(w.min(0),w.max(0));print('INSTALLED',json.dumps(row),flush=True)
  return True
 return False

names=['ACA falcine–MMA falcine left','ACA falcine–MMA falcine right','Occipital mastoid–MMA petrosquamosal left','MMA–tentorial marginal left','MMA–tentorial marginal right']
for n in names:
 v,f=meshes[n];a=np.load(WORK/(n+'.continuation-curve.npz'));q=a['q'];tt=a['tt'];param=a['param'];r=a['r'];installed=False
 if n.startswith('ACA'):
  pin=pins(n);pd=np.min(abs(tt[:,None]-param[pin][None,:]),axis=1);end=tt[0] if abs(q[0,0])>abs(q[-1,0]) else tt[-1];enddist=abs(tt-end)
  sign=-1 if n.endswith('left') else 1
  for collar in [.7,1.,1.5,2.,3.,4.]:
   for target in [.5+sign*.43,.5+sign*.2,.5]:
    for lift in [0.,.5,1.,1.5,2.,3.]:
     new=q.copy();weight=smooth(pd/collar);new[:,0]+=weight*(target-q[:,0]);new[:,2]+=lift*weight*np.exp(-((enddist-4.)/4.)**2)
     if attempt(n,v,f,q,new,param,tt,r,dict(collarMm=collar,falxTargetX=target,cingulateTransitionLiftMm=lift)):installed=True;break
    if installed:break
   if installed:break
 else:
  side='left' if n.endswith('left') else 'right';tv,tf=meshes['brain.tentorium-cerebelli.'+side];tri=tv[tf];nn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);lc=locator(tv,tf[nn[:,2]<-.01]);cp,_=closest(lc,q)
  heights=[]
  for i,p in enumerate(q):
   aa=p.copy();bb=p.copy();aa[2]=0.;bb[2]=120.;t=vtk.reference(0.);hit=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cid=vtk.reference(0)
   found=lc.IntersectWithLine(aa,bb,1e-7,t,hit,pc,sub,cid);heights.append(hit[2] if found else cp[i,2])
  floor=gaussian_filter1d(np.array(heights),2)
  for collar in [.5,.75,1.,1.5,2.,3.,4.,6.]:
   for clearance in [.15,.4,.8,1.2]:
    new=q.copy();weight=smooth((tt-tt[0])/collar)*smooth((tt[-1]-tt)/collar);new[:,2]+=weight*(np.minimum(floor-r-clearance,q[:,2])-q[:,2])
    if attempt(n,v,f,q,new,param,tt,r,dict(endCollarMm=collar,referenceClearanceMm=clearance)):installed=True;break
   if installed:break
 print('FINISHED',n,'installed',installed,'trials',sum(row['node']==n for row in history),flush=True)
 (OUT/'residual-route-trials-v0960.json').write_text(json.dumps(dict(method=__doc__,results=history),indent=2))
