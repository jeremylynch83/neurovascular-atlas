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

report=json.loads((OUT/'tentorial-reference-correction-v0960.json').read_text());checks=[]
for row in report['results']:
 steps=row.get('sourceDetailPreservation',{}).get('steps',[])
 if not any('priorGeometryFixedCoreMm' in step for step in steps):continue
 n=row['node'];base=WORK.parent/'work-v0959/candidate';v,f=load(n,base) if (base/(n+'.positions.bin')).exists() else load(n);source=intersections(*load(n));w=(v+field(v)).astype('<f4').astype(float);patches=[]
 assert not any('normalStepMm' in step for step in steps),'A microscopic correction needs separate accounting'
 for step in steps:
  bad=intersections(w,f)-source;faces=np.unique(np.array(list(bad)).ravel());centres=v[f[faces]].mean(1);core=step['priorGeometryFixedCoreMm'];radius=step['priorGeometryBlendRadiusMm'];tree=cKDTree(centres);alpha=smooth((tree.query(v)[0]-core)/radius);w=(v+(w-v)*alpha[:,None]).astype('<f4').astype(float);patches.append((tree,core,radius))
 def combined(points):
  dz=field(points)[:,2]
  for tree,core,radius in patches:dz*=smooth((tree.query(points)[0]-core)/radius)
  return dz
 eps=np.array([0.,0.,.01]);det=1+(combined(v+eps)-combined(v-eps))/.02;actual,_=current(n);error=np.linalg.norm(actual-w,axis=1).max();result=dict(node=n,minimumComposedVertexJacobianDeterminant=float(det.min()),maximumReconstructionErrorMm=float(error),passed=bool(det.min()>.3 and error<.0001));checks.append(result);print(result)
(OUT/'source-detail-composed-field-validation-v0960.json').write_text(json.dumps(dict(results=checks,passed=all(r['passed'] for r in checks),scope='Finite differences of the scalar reference field and retained source-detail blends at delivered vertices; not a clinical registration or full volumetric mesh certificate.'),indent=2))
