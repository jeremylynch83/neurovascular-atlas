"""Measure collateral routes in the unchanged reference frame."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
base=WORK.parent/'work-v0956-outward'
neural=Neural()
rows=[]
targets={r['artery'] for r in json.loads((base/'candidate/full-mma-brain-check.json').read_text())['contacts']}
for n in FILES:
 if n not in targets:continue
 x=np.load(base/(n+'.curve.npz'));v,f=load(n);w,g=load(n,base/'candidate') if (base/'candidate'/(n+'.positions.bin')).exists() else (v,f)
 # Continuous source arc coordinate averages the measured wall displacement.
 tt=x['tt'];par=x['param'];d=w-v
 shift=np.array([np.average(d,weights=np.exp(-((par-t)/.4)**2)+1e-30,axis=0) for t in tt])
 q=x['q']+shift;r=x['r'];ds,gr=neural.evaluate(q)
 if (ds<r).any():
  bad=np.flatnonzero(ds<r);row=dict(node=n,ends=q[[0,-1]].round(3).tolist(),radii=r[[0,-1]].round(3).tolist(),minClearance=float((ds-r).min()),badRange=q[bad][[0,-1]].round(3).tolist(),badFraction=float(len(bad)/len(q)))
  rows.append(row);print(row,flush=True)
 np.savez_compressed(WORK/(n+'.current-curve.npz'),q=q,r=r,tt=tt,param=par,source=x['q'])
(WORK/'route-diagnostics.json').write_text(json.dumps(rows,indent=2))
