"""Correct the cerebral reference relative to the fixed tentorial roof.

The bilateral roof audit measures up to 2.248 mm of required correction,
including a 0.4 mm separation allowance. Trial a smooth 3 mm superior shift
of the inferior posterior cerebrum, tapering to zero by z=105 mm and y=-65
mm. Carry catalogue-complete cerebral pial vessels with the same field.
Frozen native interfaces are protected with a 4 mm spatial taper. Keep
cerebellum, brainstem, dural sheets, dural vessels and skull fixed. Installation
requires cleared cortex/tentorium references, no new folds, no new cortical
bone/dural pairs and no new moved-artery/neural contact pairs.

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
 if s['system']=='vein':return s['id'].startswith(('vein.deep','vein.cortical','vein.superficial')) or s['id'] in ['vein.galen','vein.basal.right','vein.basal.left','vein.internal_cerebral.right','vein.internal_cerebral.left']
 while s:
  if s['id'] in roots:return True
  s=by.get(s.get('parent'))
 return False
targets={n for n in FILES if cats.get(n)=='cerebral_cortex'}|{s['asset']['node'] for s in by.values() if s.get('asset') and cerebral_pial(s)}
targets&=set(FILES)
ports=[]
for row in interfaces:
 a,b=row['a'],row['b']
 if (a in targets)==(b in targets):continue
 ii,jj=matches(a,b)
 if len(ii):ports.extend(mesh[a][0][ii])
ptree=cKDTree(np.array(ports)) if ports else None
def field(v):
 dz=3.*smooth((105.-v[:,2])/25.)*smooth((-v[:,1]-65.)/15.)
 if ptree is not None:
  dd,_=ptree.query(v);dz*=smooth(dd/10.)
 out=np.zeros_like(v);out[:,2]=dz;return out

rows=[]
for n in sorted(targets):
 v,f=load(n,WORK.parent/'work-v0959/candidate') if (WORK.parent/'work-v0959/candidate'/(n+'.positions.bin')).exists() else load(n)
 d=field(v)
 if d[:,2].max()<1e-5:continue
 off=np.array([0.,0.,.01]);det=1.+(field(v+off)[:,2]-field(v-off)[:,2])/.02
 row=dict(node=n,minimumVertexJacobianDeterminant=float(det.min()),maximumShiftMm=float(d[:,2].max()));rows.append(row)
print('minimum',min(r['minimumVertexJacobianDeterminant'] for r in rows))
(OUT/'tentorial-field-jacobian-v0960.json').write_text(json.dumps(dict(results=rows,passed=all(r['minimumVertexJacobianDeterminant']>.3 for r in rows)),indent=2))
