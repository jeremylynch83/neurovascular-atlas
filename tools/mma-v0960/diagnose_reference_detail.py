"""Correct the cerebral reference relative to the fixed tentorial roof.

The bilateral roof audit measures up to 2.248 mm of required correction,
including a 0.4 mm separation allowance. Trial a smooth 3 mm superior shift
of the inferior posterior cerebrum, tapering to zero by z=105 mm and y=-65
mm. Carry catalogue-complete cerebral pial vessels with the same field.
Frozen native interfaces are protected with a 10 mm spatial taper. Keep
cerebellum, brainstem, dural sheets, dural vessels and skull fixed. Installation
requires cleared cortex/tentorium references, no new folds, no new cortical
bone/dural pairs and no new moved-vessel/neural contact pairs.

This is a constrained teaching-model fit, not patient-specific registration.
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
targets&=set(FILES)
ports=[]
for row in interfaces:
 a,b=row['a'],row['b']
 if (a in targets)==(b in targets):continue
 ii,jj=matches(a,b)
 if len(ii):ports.extend(mesh[a][0][ii])
ptree=cKDTree(np.array(ports)) if ports else None
def field(v):
 dz=3.*smooth((105.-v[:,2])/25.)*smooth((-v[:,1]-75.)/15.)
 if ptree is not None:
  dd,_=ptree.query(v);dz*=smooth(dd/10.)
 out=np.zeros_like(v);out[:,2]=dz;return out
def preserve_surface_separation(n,v,w,f):
 """Resolve introduced triangle contacts with submicrometre local offsets.

 Float32 export can erase narrow separations in the folded source parcels.
 Trials retain topology, all native pins and coincident-coordinate aliases.
 The maximum cumulative local correction is capped at 0.002 mm. Only an
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
 return w,dict(maximumLocalCorrectionMm=float(np.linalg.norm(w-start,axis=1).max()),steps=steps)

for n in ['brain.calcarine-sulcus.left','brain.calcarine-sulcus.right','brain.superior-occipital-gyri.left','brain.superior-occipital-gyri.right']:
 v,f=mesh[n];w=(v+field(v)).astype('<f4').astype(float);bad=intersections(w,f)-intersections(*load(n));print(n)
 for aa,bb in sorted(bad):
  ids=np.unique(f[[aa,bb]]);print('pair',aa,bb,'centre',v[ids].mean(0).tolist(),'shift',field(v[ids])[:,2].tolist(),'pin',pins(n)[ids].sum())
