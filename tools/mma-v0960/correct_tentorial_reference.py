"""Correct the cerebral reference relative to the fixed tentorial roof.

The bilateral roof audit measures up to 2.248 mm of required correction,
including a 0.4 mm separation allowance. Trial a smooth 3 mm superior shift
of the inferior posterior cerebrum, using a gentle affine vertical taper to zero at z=108 mm and y=-75
mm. Carry catalogue-complete cerebral pial vessels with the same field.
Frozen native interfaces are protected with a 10 mm spatial taper. Keep
cerebellum, brainstem, dural sheets, dural vessels and skull fixed. Installation
requires fewer cortex/tentorium reference pairs, no new folds, no new cortical
bone/dural pairs and no new moved-vessel/neural contact pairs.

Three unresolved dural territories are kept in their prior frame with a 3 mm core and 12 mm smooth transition. This retains their existing relationships while allowing correction elsewhere. This is a constrained teaching-model fit, not patient-specific registration.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0959'))
from route_tools import *

mesh={n:current(n) for n in FILES}
cats={s['asset']['node']:s['anatomy']['category'] for s in json.loads((WORK.parent/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
mf=json.loads((WORK.parent/'public/anatomy/manifest.json').read_text());by={s['id']:s for s in mf['structures']}
rootnodes=['MCA M1 left','MCA M1 right','PCA P1 left','PCA P1 right','Anterior choroidal left','Anterior choroidal right','Posterior communicating left','Posterior communicating right','ACA A1 left','ACA A1 right']
roots={s['id'] for s in by.values() if s.get('asset',{}).get('node') in rootnodes}
def cerebral_pial(s):
 if s.get('displayGroup')=='anastomoses' or s.get('asset',{}).get('node','').startswith(('Davidoff','Wollschlaeger','Posterior meningeal','VA anterior meningeal')):return False
 if s['system']=='vein':return s['id'].startswith(('vein.deep_medullary','vein.cortical','vein.superficial','vein.deep_middle')) or s['id'] in ['vein.galen','vein.basal.right','vein.basal.left','vein.internal_cerebral.right','vein.internal_cerebral.left']
 while s:
  if s['id'] in roots:return True
  s=by.get(s.get('parent'))
 return False
targets={n for n in FILES if cats.get(n) in ['cerebral_cortex','deep_landmarks','ventricles'] and n not in ['brain.fourth-ventricle','brain.aqueduct-of-midbrain']}|{s['asset']['node'] for s in by.values() if s.get('asset') and cerebral_pial(s)}
targets.update(['vein.internal_occipital.left','vein.internal_occipital.right'])
targets&=set(FILES)
ports=[]
for row in interfaces:
 a,b=row['a'],row['b']
 if (a in targets)==(b in targets):continue
 ii,jj=matches(a,b)
 if len(ii):ports.extend(mesh[a][0][ii])
previous_controls=WORK/'reference-field-native-port-controls.npz'
if previous_controls.exists():ports.extend(np.load(previous_controls)['points'])
ptree=cKDTree(np.array(ports)) if ports else None
guard=cKDTree(np.load(WORK/'unresolved-dural-reference-guards.npz')['points'])
def field(v):
 dz=3.*np.clip((108.-v[:,2])/48.,0.,1.)*smooth((-v[:,1]-75.)/15.)
 if ptree is not None:
  dd,_=ptree.query(v);dz*=smooth(dd/10.)
 gd,_=guard.query(v);dz*=smooth((gd-3.)/12.)
 out=np.zeros_like(v);out[:,2]=dz;return out
def preserve_surface_separation(n,v,w,f):
 """Preserve folded source detail without adding triangle contacts.

 Float32 export can erase narrow separations in the folded source parcels.
 Trials retain topology, all native pins and coincident-coordinate aliases.
 Micrometre trials are tried first. If necessary, blend the added reference
 displacement back towards the prior checkpoint in a broad neighbourhood.
 The blend never moves a point beyond either delivered endpoint. Only an
 actual reduction in the exact new-pair count is accepted at each step.
 """
 source=intersections(*load(n));start=w.copy();pin=pins(n)
 _,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True)
 steps=[]
 for it in range(8):
  bad=intersections(w,f)-source
  if not bad:break
  ff=np.array([a for a,b in sorted(bad)]);tri=w[f[ff]];nn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-15)
  vectors=np.zeros_like(w);counts=np.zeros(len(w))
  for face,normal in zip(f[ff],nn):
   for ix in face:vectors[ix]+=normal;counts[ix]+=1
  vv=np.zeros((inv.max()+1,3));cc=np.zeros(inv.max()+1)
  np.add.at(vv,inv,vectors);np.add.at(cc,inv,counts);vectors=vv[inv]/np.maximum(cc[inv,None],1.)
  vectors[pin]=0.;best=None
  for step in [.00001,.00003,.0001,.0003,.001]:
   for sign in [1.,-1.]:
    t=(w+sign*step*vectors).astype('<f4').astype(float)
    if np.linalg.norm(t-start,axis=1).max()>.002:continue
    remaining=intersections(t,f)-source
    if len(remaining)<len(bad):best=(t,len(remaining),step,sign);break
   if best is not None:break
  if best is None:break
  w,count,step,sign=best;steps.append(dict(iteration=it,remainingNewPairs=count,normalStepMm=step,sign=sign))
 for it in range(6):
  bad=intersections(w,f)-source
  if not bad:break
  faces=np.unique(np.array(list(bad)).ravel());centres=v[f[faces]].mean(1);dd=cKDTree(centres).query(v)[0];best=None
  core=float(dd[np.unique(f[faces])].max())+.5
  for radius in [10.,15.,20.]:
   alpha=smooth((dd-core)/radius);t=(v+(w-v)*alpha[:,None]).astype('<f4').astype(float);t[pin]=w[pin]
   remaining=intersections(t,f)-source
   if len(remaining)<len(bad):best=(t,len(remaining),radius);break
  if best is None:break
  w,count,radius=best;steps.append(dict(iteration=it,remainingNewPairs=count,priorGeometryFixedCoreMm=core,priorGeometryBlendRadiusMm=radius))
 return w,dict(maximumLocalCorrectionMm=float(np.linalg.norm(w-start,axis=1).max()),steps=steps,interpretation='A local source-detail blend is distinct from the ambient reference field. Its actual mesh is fold-checked; the ambient Jacobian does not describe the additional local blend.')
trial={};rows=[]
for n in sorted(targets):
 v,f=mesh[n];d=field(v)
 if np.linalg.norm(d,axis=1).max()<1e-5:continue
 w=(v+d).astype('<f4').astype(float)
 detail=dict(maximumLocalCorrectionMm=0.,steps=[])
 if n.startswith('brain.') and intersections(w,f)-intersections(*load(n)):w,detail=preserve_surface_separation(n,v,w,f)
 trial[n]=(w,f)
 off=np.array([0.,0.,.01]);det=1.+(field(v+off)[:,2]-field(v-off)[:,2])/.02
 row=dict(node=n,maximumAdditionalShiftMm=float(np.linalg.norm(w-v,axis=1).max()),minimumVertexJacobianDeterminant=float(det.min()),newFoldPairs=len(intersections(w,f)-intersections(*load(n))),sourceDetailPreservation=detail)
 rows.append(row);print('GEOMETRY',json.dumps(row),flush=True)
allmesh={**mesh,**trial};reference=[];new=[]
for n,(v,f) in allmesh.items():
 if cats.get(n)!='cerebral_cortex':continue
 for bn in [k for k in FILES if k.startswith('bone.')]+['brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']:
  bv,bf=allmesh[bn]
  if np.any(bv.max(0)<v.min(0)) or np.any(bv.min(0)>v.max(0)):continue
  c=contacts(v,f,bv,bf)
  if not c:continue
  previous=contacts(*mesh[n],bv,bf);r=dict(a=n,b=bn,triangleContacts=c,previousTriangleContacts=previous)
  if bn.startswith('brain.tentorium'):reference.append(r)
  if previous==0:new.append(r)
for n,(v,f) in trial.items():
 if n.startswith('brain.'):continue
 for bn in [k for k in FILES if k.startswith('brain.') and not k.startswith(('brain.falx','brain.tentorium'))]:
  bv,bf=allmesh[bn]
  if np.any(bv.max(0)<v.min(0)) or np.any(bv.min(0)>v.max(0)):continue
  c=contacts(v,f,bv,bf)
  if not c:continue
  previous=contacts(*mesh[n],*mesh[bn])
  if previous==0:new.append(dict(a=n,b=bn,triangleContacts=c,previousTriangleContacts=previous))
print('REFERENCE',len(reference),'NEW',len(new),flush=True)
report=dict(method=__doc__,maximumReferenceDeficitMm=2.248,maximumFieldMm=3.,results=rows,remainingCortexTentoriumContacts=reference,newRelationshipPairs=new,installed=len(reference)<10 and not new and all(r['newFoldPairs']==0 and r['minimumVertexJacobianDeterminant']>.3 for r in rows))
if report['installed']:
 for n,(v,f) in trial.items():save(n,v,f,'coherent-cerebral-tentorial-reference-fit')
(OUT/'tentorial-reference-correction-v0960.json').write_text(json.dumps(report,indent=2));print('INSTALLED',report['installed'],flush=True)
