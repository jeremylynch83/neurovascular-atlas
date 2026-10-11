"""Audit and correct native cortex fit to fixed skull and dural references.

Corrections are driven by original bone/falx penetrations, never by artery
clearance. Apply the same smooth ambient flow to neural surfaces and nearby
pial vessels. Dural vessels, skull and reflections remain fixed.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.spatial.distance import cdist
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
cats={s['asset']['node']:s['anatomy']['category']for s in json.loads((WORK.parent/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
mesh={n:load(n,OUT)if n in changed else load(n)for n in FILES}
brain=[n for n in FILES if cats.get(n)=='cerebral_cortex']
constraints=[];reports=[];falxconstraints=[]
for bn in ['bone.sphenoid','bone.frontal','bone.temporal.right','bone.temporal.left','brain.falx-cerebri']:
 bv,bf=load(bn);tri=bv[bf];nc=normals(bv,bf);fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(bv,bf));dural=bn.startswith('brain.')
 tn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);tn/=np.maximum(np.linalg.norm(tn,axis=1)[:,None],1e-15)
 inward=np.einsum('ij,ij->i',tn,np.array([.624,-60.,108.])-tri.mean(1))>0
 iloc=locator(bv,bf[inward])if not dural else None
 for n in brain:
  if not dural and not any(t in n for t in ['orbital','temporal-pole','parahippocampal']):continue
  v,f=mesh[n]if '--incremental'in sys.argv else load(n)
  if np.any(v.max(0)<bv.min(0))or np.any(v.min(0)>bv.max(0)):continue
  count=contacts(v,f,bv,bf)
  if not count:continue
  candidates=np.unique(np.vstack([v,v[f].mean(1)]),axis=0)
  use=np.all(candidates>=bv.min(0)-2,axis=1)&np.all(candidates<=bv.max(0)+2,axis=1)
  pts=candidates[use];ds=np.array([fn.EvaluateFunction(p)for p in pts]);active=ds<.65
  pts=pts[active];ds=ds[active]
  if not len(pts):continue
  gg=[];deficit=[]
  if dural:
   sign=1 if n.endswith('.right')else -1
   iloc=locator(bv,bf[tn[:,0]*sign>.35])
  cp,cd=closest(iloc,pts)
  for j,p in enumerate(pts):
   g=(cp[j]-p)/max(cd[j],1e-8)
   # Choose intracranial exits and correct interhemispheric separation.
   desired=np.array([1 if n.endswith('.right')else -1,0,0.])if dural else np.array([0.,-60.,108.])-p
   if np.dot(g,desired)<0:g=-g
   if dural:g=np.array([sign,0.,0.])
   gg.append(g);deficit.append(cd[j]+.65 if ds[j]<0 else max(.65-cd[j],0))
  gg=np.array(gg);deficit=np.clip(deficit,0,4.5)
  (falxconstraints if dural else constraints).append((pts,gg*deficit[:,None]));reports.append(dict(brain=n,reference=bn,sourceTriangleContacts=count,controlCount=len(pts),maximumConstraintMm=float(deficit.max())))
points=np.vstack([p for p,d in constraints]);vectors=np.vstack([d for p,d in constraints]);sigma=5.;support=18.
fp=np.vstack([p for p,d in falxconstraints]);fv=np.vstack([d for p,d in falxconstraints]);fv=np.linalg.norm(fv,axis=1)
def field(v):
 out=np.zeros_like(v,dtype=float)
 for start in range(0,len(v),1000):
  p=v[start:start+1000];dd=cdist(p,points);w=np.exp(-dd**2/(2*sigma**2));taper=smooth((support-dd.min(1))/(support-sigma));d=(w@vectors)/np.maximum(w.sum(1)[:,None],1e-30)*taper[:,None]
  # The two medial surfaces have opposite constraint directions. Averaging
  # signed controls across the thin fissure would cancel the correction.
  fd=cdist(p,fp);fw=np.exp(-fd**2/(2*5.**2));amp=(fw@fv)/np.maximum(fw.sum(1),1e-30)*smooth((15-fd.min(1))/10)
  d[:,0]+=np.tanh((p[:,0]-.624)/.02)*amp
  out[start:start+len(p)]=d
 return out
samples=points.copy();jac=np.zeros((len(samples),3,3));eps=.02
for k in range(3):
 off=np.zeros(3);off[k]=eps;jac[:,:,k]=(field(samples+off)-field(samples-off))/(2*eps)
det=np.linalg.det(jac+np.eye(3));report=dict(method=__doc__,constraints=reports,minimumControlJacobianDeterminant=float(det.min()),maximumControlShiftMm=float(np.linalg.norm(field(points),axis=1).max()),applied=False)
np.savez_compressed(WORK/'reference-fit-field.npz',points=points,vectors=vectors,sigma=sigma,support=support,falxPoints=fp,falxAmplitudes=fv)
(WORK/'reference-fit-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if '--apply'in sys.argv:
 assert det.min()>.3,'Refusing a non-positive or severely compressed reference fit'
 # Explicit intracranial pial families. Cavernous, meningeal and extracranial
 # arteries remain in the fixed dural/skull frame.
 prefixes=('ACA ','MCA ','PCA ','SCA ','AICA ','PICA ','Basilar','Vertebral V4','Anterior choroidal','Posterior communicating','ICA supraclinoid','ICA ophthalmic','Lenticulostriate','Anterior communicating')
 targets=[n for n in FILES if n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'))or n.startswith(prefixes)or n.startswith(('vein.superficial','vein.cortical','vein.deep_middle','vein.internal_cerebral','vein.basal','vein.great_cerebral'))]
 for n in targets:
  v,f=mesh[n];d=field(v)
  if np.max(np.linalg.norm(d,axis=1))<1e-5:continue
  q=v+d;write(n,q,f);sv,sf=load(n);row=dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=True,field='skull-and-falx-reference-fit',maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()))
  for i,r in enumerate(rev['changed']):
   if r['node']==n:rev['changed'][i]=row;break
  else:rev['changed'].append(row)
 report['applied']=True;report['affectedLabels']=targets
 (OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'reference-fit-audit.json').write_text(json.dumps(report,indent=2))
