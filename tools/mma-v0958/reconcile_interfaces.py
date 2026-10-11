"""Reconcile native pial/dural interfaces after the reference fit.

Dural-frame owners remain authoritative at shared ports. Other transformed
pial junctions use a common float32 coordinate. Corrections taper over 6 mm.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
rev=json.loads((OUT/'revision.json').read_text());rows={r['node']:r for r in rev['changed']};names=list(FILES);old=[];new=[];owners=[];local=[];mesh={}
for j,n in enumerate(names):
 v,f=load(n);q,g=load(n,OUT)if n in rows else(v,f);assert np.array_equal(f,g)
 mesh[n]=(q,g);old.append(v.astype('<f4'));new.append(q.astype('<f4'));owners.append(np.full(len(v),j,np.int32));local.append(np.arange(len(v),dtype=np.int32))
sv=np.concatenate(old);q=np.concatenate(new);owners=np.concatenate(owners);local=np.concatenate(local);keys=np.ascontiguousarray(sv).view('V12').ravel();order=np.argsort(keys);kk=keys[order];starts=np.r_[0,np.flatnonzero(kk[1:]!=kk[:-1])+1,len(kk)];lengths=np.diff(starts);targets={};groups=0;largest=0.
for a,b in zip(starts[:-1][lengths>1],starts[1:][lengths>1]):
 ids=order[a:b];own=np.unique(owners[ids])
 if len(own)<2:continue
 p=q[ids];gap=float(np.linalg.norm(p-p[0],axis=1).max())
 fixed=[i for i in ids if rows.get(names[owners[i]],{}).get('field')not in ['skull-and-falx-reference-fit','catalogue-complete-pial-reference-fit']]
 target=q[fixed[0]]if fixed else p.mean(0).astype('<f4');groups+=int(gap>=1e-8);largest=max(largest,gap)
 for i in ids:
  n=names[owners[i]];targets.setdefault(n,{})[int(local[i])]=target
del old,new,sv,q,owners,local,keys,order,kk,starts
report=[]
for n,t in targets.items():
 v,f=mesh[n];ids=np.array(list(t));dest=np.array([t[i]for i in ids]);shift=dest-v[ids];dd,idx=cKDTree(v[ids]).query(v);weight=1-smooth(dd/6.);nv=v+shift[idx]*weight[:,None];nv[ids]=dest;write(n,nv,f);source,_=load(n)
 row=rows.get(n,dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=True,field='pial-interface-collar-fit'));row.update(maxShiftMm=float(np.linalg.norm(nv-source,axis=1).max()),referenceInterfaceBlend=True);rows[n]=row
 report.append(dict(node=n,sharedVertices=len(ids),maximumCorrectionMm=float(np.linalg.norm(nv-v,axis=1).max())));print(report[-1],flush=True)
rev['changed']=list(rows.values());(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'reference-interface-repair.json').write_text(json.dumps(dict(method=__doc__,changedCoordinateGroups=groups,maximumInitialMismatchMm=largest,results=report),indent=2))
