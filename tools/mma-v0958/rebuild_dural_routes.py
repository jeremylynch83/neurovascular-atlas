"""Reconstruct collaterals against their anatomical dural reference.

Falcine twigs run within the falx, not the medial frontal cortex. The
MMA tentorial connection follows the deep tentorial sheet and joins the
Davidoff/Schechter terminal segment. The PCA origin is held fixed.
These routes are inferred from source dural landmarks and dissection studies;
they are not recovered patient-specific vessels.
"""
import sys,ast,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.ndimage import gaussian_filter1d
from types import SimpleNamespace
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
p=Path(__file__).parents[1]/'brainstem-quality-v0948/extract_curves.py'
sp=importlib.util.spec_from_file_location('extract',p);ex=importlib.util.module_from_spec(sp);sp.loader.exec_module(ex)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
current=lambda n:load(n,OUT)if n in changed else load(n)
def curve(n):
 v,f=current(n);q,r,param,tt=ex.extract(SimpleNamespace(v=v,f=f));return v,f,q,r,param,tt
def tube(v,q,new,param,tt):
 # Translate and rotate each cross section by the minimal tangent rotation.
 old=np.column_stack([np.interp(param,tt,q[:,k])for k in range(3)])
 newp=np.column_stack([np.interp(param,tt,new[:,k])for k in range(3)])
 a=np.gradient(q,axis=0);a/=np.linalg.norm(a,axis=1)[:,None]
 b=np.gradient(new,axis=0);b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-8)
 a=np.column_stack([np.interp(param,tt,a[:,k])for k in range(3)]);a/=np.linalg.norm(a,axis=1)[:,None]
 b=np.column_stack([np.interp(param,tt,b[:,k])for k in range(3)]);b/=np.linalg.norm(b,axis=1)[:,None]
 c=np.cross(a,b);dot=(a*b).sum(1);rad=v-old
 rot=rad+np.cross(c,rad)+np.cross(c,np.cross(c,rad))/np.maximum(1+dot[:,None],1e-8)
 return newp+rot
def save(n,v,f):
 write(n,v,f);sv,sf=load(n)
 row=dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=np.array_equal(f,sf),field='dural-landmark-reconstruction',maxShiftMm=float(np.linalg.norm(v-sv,axis=1).max()))
 for i,r in enumerate(rev['changed']):
  if r['node']==n:rev['changed'][i]=row;break
 else:rev['changed'].append(row)
 changed.add(n)
def propagate_shared(n,before,after):
 source,_=load(n);keys={bytes(k):i for i,k in enumerate(np.ascontiguousarray(source.astype('<f4')).view('V12').ravel())}
 updates=[]
 for other in FILES:
  if other==n:continue
  sv,sf=load(other);jj=[];ii=[]
  for j,k in enumerate(np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel()):
   if bytes(k)in keys:jj.append(j);ii.append(keys[bytes(k)])
  if not jj:continue
  v,f=current(other);jj=np.array(jj);ii=np.array(ii);shift=after[ii]-v[jj]
  if np.max(np.linalg.norm(shift,axis=1))<1e-5:continue
  d,ix=cKDTree(v[jj]).query(v);weight=1-smooth(d/8.)
  w=v+weight[:,None]*shift[ix];w[jj]=after[ii]
  save(other,w,f);updates.append(dict(node=other,sharedVertices=len(jj),maximumShiftMm=float(np.linalg.norm(w-v,axis=1).max())))
 return updates
reports=[]
for side,sign in [('right',1),('left',-1)]:
 n='MMA falcine terminal '+side;v,f,q,r,param,tt=curve(n)
 # Median surface gives the sheet centre rather than an external cortex path.
 fv,ff=load('brain.falx-cerebri');cp,ds=closest(locator(fv,ff),q)
 new=q.copy();new[:,0]=.5+sign*.43
 w=tube(v,q,new,param,tt);save(n,w,f);updates=propagate_shared(n,v,w)
 np.savez_compressed(WORK/(n+'.dural-curve.npz'),q=new,r=r,param=param,tt=tt)
 reports.append(dict(node=n,reference='brain.falx-cerebri',method='paired intrafalcine routes around source midplane x=0.5 mm',partners=updates,maxShiftMm=float(np.linalg.norm(w-v,axis=1).max())))
 n='MMA tentorial–PCA dural '+side;v,f,q,r,param,tt=curve(n)
 tv,tf=load('brain.tentorium-cerebelli.'+side);cp,ds=closest(locator(tv,tf),q)
 # This source sheet is a thick closed shell. Select its inferior/deep face
 # for each xy coordinate, rather than use the nearer superior cortex side.
 tri=tv[tf];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);lower=norm[:,2]<-.01
 l=locator(tv,tf[lower]);cp,_=closest(l,q)
 new=q.copy();heights=[]
 for j,p in enumerate(q):
  a=p.copy();b=p.copy();a[2]=0.;b[2]=120.;t=vtk.reference(0.);hit=[0.,0.,0.];pcoords=[0.,0.,0.];sub=vtk.reference(0);cid=vtk.reference(0)
  found=l.IntersectWithLine(a,b,1e-7,t,hit,pcoords,sub,cid)
  heights.append(hit[2]if found else cp[j,2])
 new[:,2]=gaussian_filter1d(np.array(heights),2)-r-.10
 # Lateral attachment must meet the neighbouring petrosquamosal wall.
 w=tube(v,q,new,param,tt);save(n,w,f);updates=propagate_shared(n,v,w)
 # ADS attaches to the medial end. Retain the source PCA end and bend only
 # the dural segment toward the new endpoint with a smooth arc taper.
 an='Davidoff–Schechter '+side
 if an not in FILES:an=next(k for k in FILES if 'Davidoff'in k and k.endswith(side))
 av,af,aq,ar,ap,at=curve(an);med=int(np.argmin(abs(new[[0,-1],0])));endpoint=new[[0,-1]][med]
 oldend=q[[0,-1]][med];which=int(np.argmin(np.linalg.norm(aq[[0,-1]]-oldend,axis=1)));tail=which*(len(aq)-1)
 # Keep the original wall relationship at the endpoint, including radius.
 d=endpoint-oldend;u=(at-at[0])/(at[-1]-at[0]);weight=smooth((u-.25)/.75)if which else smooth((.75-u)/.75)
 anew=aq+weight[:,None]*d;aw=tube(av,aq,anew,ap,at);save(an,aw,af);au=propagate_shared(an,av,aw)
 np.savez_compressed(WORK/(n+'.dural-curve.npz'),q=new,r=r,param=param,tt=tt)
 np.savez_compressed(WORK/(an+'.dural-curve.npz'),q=anew,r=ar,param=ap,tt=at)
 reports.append(dict(node=n,reference='brain.tentorium-cerebelli.'+side,partners=updates,distalPartner=an,distalPartnerUpdates=au,maxShiftMm=float(np.linalg.norm(w-v,axis=1).max()),distalPartnerShiftMm=float(np.linalg.norm(aw-av,axis=1).max())))
rev.update(release='0.9.58',status='dural-reference-reconstruction-candidate',brainSkullCorrectionAuthorised=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'dural-route-reconstruction.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2));print(json.dumps(reports,indent=2))
