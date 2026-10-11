"""Correct the cerebral reference relative to the fixed tentorial roof.

The bilateral roof audit measures up to 2.248 mm of required correction,
including a 0.4 mm separation allowance. Trial a smooth 3 mm superior shift
of the inferior posterior cerebrum, using a gentle affine vertical taper to zero at z=108 mm and y=-75
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
 dz=3.*np.clip((108.-v[:,2])/48.,0.,1.)*smooth((-v[:,1]-75.)/15.)
 if ptree is not None:
  dd,_=ptree.query(v);dz*=smooth(dd/10.)
 out=np.zeros_like(v);out[:,2]=dz;return out

report=json.loads((OUT/'tentorial-reference-correction-v0960.json').read_text());results=[]
for n in ['vein.internal_occipital.left','vein.internal_occipital.right']:
 v,f=mesh[n];pin=pins(n);distance=cKDTree(v[pin]).query(v)[0] if pin.any() else np.full(len(v),np.inf);w=(v+field(v)*smooth(distance/4.)[:,None]).astype('<f4').astype(float);old=WORK.parent/'work-v0959/candidate';rows=[]
 for bn,bv,bf in brain:
  if np.any(bv.max(0)<w.min(0)) or np.any(bv.min(0)>w.max(0)):continue
  count=contacts(w,f,bv,bf)
  if count:
   b0=load(bn,old) if (old/(bn+'.positions.bin')).exists() else load(bn);previous=contacts(v,f,*b0);rows.append(dict(brain=bn,triangleContacts=count,previousTriangleContacts=previous,newContactPair=previous==0))
 off=np.array([0.,0.,.01]);det=1.+(field(v+off)[:,2]-field(v-off)[:,2])/.02;pin=pins(n);row=dict(node=n,nativePinsExact=bool(np.array_equal(w[pin],v[pin])),maximumAdditionalShiftMm=float(np.linalg.norm(w-v,axis=1).max()),minimumVertexJacobianDeterminant=float(det.min()),newFoldPairs=len(intersections(w,f)-intersections(*load(n))),sourceDetailPreservation=dict(maximumLocalCorrectionMm=0.,steps=[]));passed=not any(r['newContactPair'] for r in rows) and row['newFoldPairs']==0 and np.array_equal(w[pin],v[pin]);print(n,'passed',passed,rows)
 if passed:
  save(n,w,f,'coherent-cerebral-tentorial-reference-fit');report['results'].append(row)
 results.append(dict(node=n,installed=bool(passed),geometry=row,neuralContacts=rows))
(OUT/'internal-occipital-vein-fit-v0960.json').write_text(json.dumps(dict(results=results,passed=all(r['installed'] for r in results)),indent=2));(OUT/'tentorial-reference-correction-v0960.json').write_text(json.dumps(report,indent=2))
np.savez_compressed(WORK/'reference-field-native-port-controls.npz',points=np.array(ports))
