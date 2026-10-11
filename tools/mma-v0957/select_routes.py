"""Keep only small, successful regional corrections and match adjoining collars."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
import shutil
base=WORK.parent/'work-v0956-outward/candidate'
trial=json.loads((OUT/'regional-collateral-corrections.json').read_text())
selected={r['node'] for r in trial['results'] if r['passedNeuralContacts'] and r['maximumAdditionalShiftMm']<2}
kept={n:load(n,OUT) for n in selected}
original=json.loads((base/'revision.json').read_text())
for r in trial['results']:
 n=r['node']
 if n in selected:continue
 for ext in ['positions','indices','normals']:
  p=base/(n+'.'+ext+'.bin');out=OUT/p.name
  if p.exists():shutil.copyfile(p,out)
  else:out.unlink(missing_ok=True)
rev=original;rev.update(release='0.9.57',status='regional-course-candidate')
changed={r['node']:r for r in rev['changed']};rows=[]
for n,(v,f) in kept.items():
 old,_=load(n);before=load(n,base)[0];oldkeys=np.ascontiguousarray(old.astype('<f4')).view('V12').ravel();bykey={bytes(k):i for i,k in enumerate(oldkeys)}
 changed[n].update(field='regional-orbital-floor',maxShiftMm=float(np.linalg.norm(v-old,axis=1).max()))
 for other in FILES:
  if other==n:continue
  ov,of=load(other);keys=np.ascontiguousarray(ov.astype('<f4')).view('V12').ravel()
  pairs=[(i,bykey[bytes(k)])for i,k in enumerate(keys)if bytes(k) in bykey]
  if not pairs:continue
  oi,ni=np.array(pairs).T;delta=v[ni]-before[ni]
  if np.linalg.norm(delta,axis=1).max()<1e-7:continue
  assert not other.startswith(('brain.','bone.')), 'Native reference must remain fixed'
  pv,pf=load(other,OUT) if (OUT/(other+'.positions.bin')).exists() else (ov,of)
  dd,ix=cKDTree(ov[oi]).query(ov);weight=1-smooth(dd/3)
  pv+=delta[ix]*weight[:,None];pv[oi]=v[ni]
  write(other,pv,pf);changed[other]=dict(node=other,file=FILES[other],vertices=len(pv),triangles=len(pf),topologyExact=True,field='matched-orbital-interface',maxShiftMm=float(np.linalg.norm(pv-ov,axis=1).max()))
  rows.append(dict(a=n,b=other,matchedVertices=len(oi),maximumChangeMm=float(np.linalg.norm(delta,axis=1).max())))
# The left native origin needs a gentler transition to avoid a tiny fold.
n='MMA orbital left';v,f=load(n,OUT);before,_=load(n,base)
centre=np.array([-45.6229,-27.734,66.611]);weight=smooth((np.linalg.norm(before-centre,axis=1)-.65)/1.25)
write(n,before+(v-before)*weight[:,None],f)
rev['changed']=list(changed.values());(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'route-selection.json').write_text(json.dumps(dict(selected=sorted(selected),matchedInterfaces=rows,rejected=[r['node']for r in trial['results']if r['node']not in selected],reason='Retain only contact-free corrections below 2 mm. Larger or unresolved experiments are excluded.'),indent=2))
print('Selected',sorted(selected),'matched',rows,flush=True)
