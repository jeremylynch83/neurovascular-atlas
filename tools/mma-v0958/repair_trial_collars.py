"""Repair displacement collars in neural-clear trials without shrinking tubes.

The Laplacian acts on displacement, not on surface coordinates. Native
ports and the successful remote route remain fixed. Every result must pass
fresh neural and self-fold checks before installation.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
audit=json.loads((OUT/'overlooked-collateral-repair.json').read_text())
interfaces=json.loads((OUT/'native-interface-validation.json').read_text())['exactSharedInterfaces']
brain=[(n,*load(n,OUT)) if n in changed else(n,*load(n))for n in FILES if n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'))]
reports=[]
for row in audit['results']:
    if row['installed'] or row['history'][-1]['contacts'] or not row['newFoldPairs']:continue
    n=row['node'];sv,sf=load(n);initial,f=load(n,OUT)if n in changed else(sv,sf)
    x=np.load(OUT/(n+'.bounded-route-trial.npz'));v=x['v'].astype(float);f=x['f'];baseline=intersections(sv,sf);new=intersections(v,f)-baseline
    partners={r['b']if r['a']==n else r['a']for r in interfaces if n in [r['a'],r['b']]};foreign=set()
    for k in partners:foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
    pin=np.array([bytes(k)in foreign for k in np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel()])
    affected=np.unique(f[np.unique(np.array(list(new)).ravel())]);dd=cKDTree(sv[affected]).query(sv)[0]
    edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]]
    weights=1/np.maximum(np.linalg.norm(sv[aa]-sv[bb],axis=1),.025);graph=coo_matrix((weights,(aa,bb)),shape=(len(v),len(v))).tocsr();lap=diags(np.asarray(graph.sum(1)).ravel())-graph
    history=[];installed=False
    for support in [1.,1.5,2.5,4.,6.]:
        fixed=np.flatnonzero(pin|(dd>support));free=np.flatnonzero(~(pin|(dd>support)));d=v-sv
        if len(free):d[free]=spsolve((lap[free][:,free]+diags(np.full(len(free),1e-5))).tocsc(),-(lap[free][:,fixed]@d[fixed]))
        q=sv+d
        _,inv,cnt=np.unique(sv,axis=0,return_inverse=True,return_counts=True);values=np.zeros((len(cnt),3));np.add.at(values,inv,q);values/=cnt[:,None]
        for i in np.flatnonzero(pin):values[inv[i]]=initial[i]
        q=values[inv]
        folds=intersections(q,f)-baseline;lo=q.min(0)-.05;hi=q.max(0)+.05;contacts_found=[]
        for bn,bv,bf in brain:
            if np.any(bv.max(0)<lo)or np.any(bv.min(0)>hi):continue
            t=bv[bf];take=np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)
            if not take.any():continue
            count=contacts(q,f,bv,bf[take])
            if count:contacts_found.append(dict(brain=bn,triangleContacts=count))
        exact=np.array_equal(q[pin].astype('<f4'),initial[pin].astype('<f4'))
        result=dict(supportMm=support,newFoldPairs=len(folds),neuralContacts=contacts_found,nativeCollarsExact=exact,maximumCollarRepairMm=float(np.linalg.norm(q-v,axis=1).max()))
        history.append(result);print(n,result,flush=True)
        if not folds and not contacts_found and exact:
            write(n,q,f);installed=True
            for r in rev['changed']:
                if r['node']==n:r.update(field='overlooked-collateral-harmonic-displacement-collar',maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()));break
            break
    reports.append(dict(node=n,installed=installed,history=history))
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'overlooked-collateral-collar-repair.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
