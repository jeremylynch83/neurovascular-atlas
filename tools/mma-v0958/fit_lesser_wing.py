"""Audit the medial collector against the inferior lesser-wing surface.

The medial channel belongs under the lesser sphenoid wing. Lateral entering
meningeal channels may use bony canals; a medial collector must not be made
intradiploic merely to avoid cortex. This trial is not installed automatically.
"""
import sys,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.spatial.distance import cdist
from types import SimpleNamespace
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
sp=importlib.util.spec_from_file_location('extract',Path(__file__).parents[1]/'brainstem-quality-v0948/extract_curves.py');ex=importlib.util.module_from_spec(sp);sp.loader.exec_module(ex)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']};bv,bf=load('bone.sphenoid');tri=bv[bf];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.linalg.norm(normal,axis=1)[:,None];take=(normal[:,2]<-.35)&(tri.mean(1)[:,2]>70)&(tri.mean(1)[:,2]<89)&(tri.mean(1)[:,1]>-35)&(tri.mean(1)[:,1]<-10);l=locator(bv,bf[take]);reports=[]
brain=[(n,*load(n,OUT))if n in changed else(n,*load(n))for n in FILES if n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'))]
for side in ['right','left']:
 n='vein.sphenoparietal.'+side;sv,sf=load(n);q,r,_,_=ex.extract(SimpleNamespace(v=sv,f=sf));x=np.load(OUT/('receiver-network-installed-'+side+'.npz'));v=x['v'].astype(float);f=x['f'];initial=v.copy();initialunion=np.load(OUT/('receiver-seam-completed-'+side+'.npz'))['v'];d,ii=cKDTree(initialunion).query(q,k=8);weights=1/np.maximum(d,.05)**2;q+=np.sum(weights[:,:,None]*(v-initialunion)[ii],axis=1)/weights.sum(1)[:,None]
 controls=[];targets=[]
 for p,rad in zip(q,r):
  if not 22<abs(p[0])<41:continue
  a=p.copy();b=p.copy();a[2]=60.;b[2]=100.;t=vtk.reference(0.);hit=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cid=vtk.reference(0)
  if not l.IntersectWithLine(a,b,1e-7,t,hit,pc,sub,cid):continue
  deficit=max(p[2]-(hit[2]-rad-.15),0.)
  if deficit>0:controls.append(p);targets.append(min(deficit,6.))
 pts=np.array(controls);targets=np.array(targets);assert len(pts)>3,'No reliable lesser-wing inferior-face controls'
 for start in range(0,len(v),1000):
  p=v[start:start+1000];dd=cdist(p,pts);w=np.exp(-dd**2/8.);taper=smooth((6-dd.min(1))/4.)*smooth((abs(p[:,0])-18)/8.)*(1-smooth((abs(p[:,0])-37)/5.));v[start:start+len(p),2]-=(w@targets)/np.maximum(w.sum(1),1e-30)*taper
 neural=[];lo=v.min(0);hi=v.max(0)
 for bn,bb,gg in brain:
  if np.any(bb.max(0)<lo)or np.any(bb.min(0)>hi):continue
  bt=bb[gg];bbf=gg[np.all(bt.max(1)>=lo,axis=1)&np.all(bt.min(1)<=hi,axis=1)];count=contacts(v,f,bb,bbf)
  if count:neural.append(dict(brain=bn,triangleContacts=count))
 folds=intersections(v,f);np.savez_compressed(OUT/('receiver-lesser-wing-trial-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'),owner=x['owner'])
 reports.append(dict(side=side,inferiorFaceControls=len(pts),maximumTargetDropMm=float(targets.max()),maximumSurfaceShiftMm=float(np.linalg.norm(v-initial,axis=1).max()),neuralContacts=neural,selfFolds=len(folds),passed=not neural and not folds,installed=False));print(reports[-1],flush=True)
(OUT/'receiver-lesser-wing-trial.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
