"""Bounded neural-clearance experiment for the remaining MMA collaterals.

The control taper targets 3 mm from the skull-directed course. Interpolation
can exceed that target; the measured maximum is reported and excess prevents
application. This experiment is not an anatomical acceptance criterion.
"""
from clear_neural import *
base=WORK.parent/'work-v0956-outward'
old_guides=json.loads((base/'tree-guides.json').read_text());core={g['node'] for g in old_guides}
guides=[]
for n in FILES:
    if not n.startswith(('MMA ','Middle meningeal')):continue
    data=np.load(base/(n+'.curve.npz'));guides.append(dict(node=n,oldPoints=data['q'].tolist(),radiusMm=data['r'].tolist()))
old=np.concatenate([np.asarray(g['oldPoints'])[::3] for g in guides]);rr=np.concatenate([np.asarray(g['radiusMm'])[::3] for g in guides])
q=arterial_field()(old);flow=np.load(base/'outward-flow.npz')
for p,d in zip(flow['points'],flow['vectors']):q=Step(p,d)(q)
initial=q.copy();neural=Neural();steps=[];spans=[];start=0
for g in guides:
    size=len(g['oldPoints'][::3]);spans.append(slice(start,start+size));start+=size
history=[]
for iteration in range(100):
    dist,grad=neural.evaluate(q);deficit=np.maximum(rr+.25-dist,0)
    delta=grad*np.minimum(deficit*.5,.1)[:,None]
    for span in spans:delta[span]=gaussian_filter1d(delta[span],1,axis=0)
    delta*=smooth((old[:,2]-44)/9)[:,None]
    displacement=q-initial;length=np.linalg.norm(displacement,axis=1)
    delta*=smooth((3-length)/.5)[:,None]
    step=Step(q.copy(),delta,sigma=1.5,support=6)
    steps.append((q.copy(),delta));q=step(q)
    row=dict(iteration=iteration,deficientStations=int((deficit>.05).sum()),minimumClearanceMm=float((dist-rr).min()),maximumShiftMm=float(np.linalg.norm(q-initial,axis=1).max()))
    history.append(row)
    if iteration%10==0:print(row,flush=True)
np.savez_compressed(WORK/'collateral-flow.npz',points=np.asarray([p for p,d in steps]),vectors=np.asarray([d for p,d in steps]),old=old,initial=initial,final=q,radii=rr)
dist,_=neural.evaluate(q);rows=[]
for g,span in zip(guides,spans):rows.append(dict(node=g['node'],minimumClearanceMm=float((dist[span]-rr[span]).min()),unclearStations=int((dist[span]<rr[span]).sum())))
(WORK/'collateral-flow-report.json').write_text(json.dumps(dict(method=__doc__,history=history,branches=rows,appliedToMeshes=False,acceptableForApplication=history[-1]['maximumShiftMm']<=3 and not any(r['unclearStations'] for r in rows)),indent=2))
print('Residual branches',[r for r in rows if r['unclearStations']],flush=True)
