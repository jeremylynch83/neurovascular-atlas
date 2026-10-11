"""Bounded trials for overlooked dural collaterals, with native collars fixed.

Cavernous/clival routes move medially; falcine routes move towards the falx;
posterior dural routes move towards the cranial wall. Tube cross-sections
are translated together along the recovered curve, avoiding wall shrinkage.
Only trials with zero neural contacts and no new folds are installed.
Bone relations and anatomical validity remain separate release checks.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.ndimage import gaussian_filter1d, maximum_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev = json.loads((OUT/'revision.json').read_text()); changed = {r['node'] for r in rev['changed']}
interfaces = json.loads((OUT/'native-interface-validation.json').read_text())['exactSharedInterfaces']
audit = json.loads((OUT/'all-mma-neural-validation.json').read_text())
bad = ['Posterior cavernous MMA–posterolateral ILT left']
current = lambda n: load(n, OUT) if n in changed else load(n)
brain = [(n,*current(n)) for n in FILES if n.startswith('brain.') and not n.startswith(('brain.falx','brain.tentorium'))]
def collision_ids(v,f,w,g):
    c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
    return vtk_to_numpy(c.GetContactCells(0)).astype(int) if c.GetNumberOfContacts() else np.empty(0,int)
reports=[]
for n in bad:
    v,f=current(n);sv,sf=load(n);x=np.load(WORK/(n+'.continuation-curve.npz'));par=x['param'];tt=x['tt']
    partners={r['b'] if r['a']==n else r['a'] for r in interfaces if n in [r['a'],r['b']]}
    foreign=set()
    for k in partners: foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
    pin=np.array([bytes(k) in foreign for k in np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel()])
    anchors=par[pin];collar=smooth(np.min(abs(tt[:,None]-anchors[None,:]),axis=1)/2.) if len(anchors) else np.ones(len(tt))
    sign=-1 if n.endswith(' left') else 1
    if 'cavernous' in n or n.startswith('ACA falcine'): direction=np.array([0.,0.,-1.])
    elif n.startswith('Anterior falcine'): direction=np.array([0.,1.,0.])
    elif 'tentorial marginal' in n: direction=np.array([0.,0.,-1.])
    elif 'Occipital mastoid' in n: direction=np.array([sign,0.,0.])
    else: raise ValueError(n)
    shift=np.zeros(len(tt));history=[];last_hits=None
    for it in range(61):
        delta=np.interp(par,tt,shift)[:,None]*direction;delta[pin]=0;w=v+delta
        lo=w.min(0)-.05;hi=w.max(0)+.05;rows=[];hits=[]
        for bn,bv,bf in brain:
            if np.any(bv.max(0)<lo) or np.any(bv.min(0)>hi):continue
            t=bv[bf];take=np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)
            if not take.any():continue
            ids=collision_ids(w,f,bv,bf[take])
            if len(ids):rows.append(dict(brain=bn,triangleContacts=len(ids)));hits.extend(par[f[ids]].ravel())
        history.append(dict(iteration=it,contacts=rows,maximumShiftMm=float(shift.max())))
        if not hits:break
        if it%15==0:print(n,it,sum(r['triangleContacts']for r in rows),round(float(shift.max()),3),flush=True)
        active=np.zeros(len(tt));ix=np.unique(np.clip(np.searchsorted(tt,hits),0,len(tt)-1));active[ix]=1
        spacing=max(float(np.median(np.diff(tt))),1e-4)
        active=maximum_filter1d(active,size=max(3,int(1./spacing)));active=gaussian_filter1d(active,1.5/spacing);active/=max(active.max(),1e-10)
        shift=np.minimum(shift+.08*active*collar,3.0);shift=gaussian_filter1d(shift,.2/spacing)
    newfolds=intersections(w,f)-intersections(sv,sf)
    exact=np.array_equal(w[pin].astype('<f4'),v[pin].astype('<f4'))
    passed=not history[-1]['contacts'] and not newfolds and exact
    np.savez_compressed(OUT/(n+'.floor-route-trial.npz'),v=w.astype('<f4'),f=f.astype('<u4'))
    if passed:
        write(n,w,f)
        for row in rev['changed']:
            if row['node']==n:row.update(field='left-cavernous-floor-collateral-repair',maxShiftMm=float(np.linalg.norm(w-sv,axis=1).max()));break
        else:rev['changed'].append(dict(node=n,file=FILES[n],vertices=len(w),triangles=len(f),topologyExact=True,field='left-cavernous-floor-collateral-repair',maxShiftMm=float(np.linalg.norm(w-sv,axis=1).max())))
        changed.add(n)
    result=dict(node=n,installed=passed,passed=passed,nativePinnedVertices=int(pin.sum()),nativeCollarsExact=exact,newFoldPairs=len(newfolds),maximumAdditionalShiftMm=float(np.linalg.norm(w-v,axis=1).max()),direction=direction.tolist(),history=history)
    reports.append(result);print('RESULT',n,passed,len(history[-1]['contacts']),len(newfolds),flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'left-cavernous-floor-repair.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
