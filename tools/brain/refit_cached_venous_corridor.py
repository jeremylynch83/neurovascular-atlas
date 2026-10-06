"""Rebind cached wall constraints to the resized, ordered brain field.

X/Z coordinates are invariant. Inverting the previous ordered field recovers
exact source surface stations; the new field then yields the new surface. No
ray samples or tissue constraints are dropped, and a changed source is rejected.
"""
import json,numpy as np,trimesh
from scipy.sparse import load_npz,coo_matrix,eye,hstack,vstack
from scipy.optimize import linprog
from fit_vessels import APP,read_glb
from reconcile_local_volume import VolumeMap
from fit_brainstem_volume import Grid
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
P=APP/'.authoring/brainstem20-lower-final';W=APP/'.authoring/brainstem20-space'
def mapping(path):
 v=np.load(path);m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.delta=v['delta'];m.mask=v['mask'];m.shape=np.array(m.delta.shape);return m
old=mapping(P/'volume-map.npz');new=mapping(W/'volume-map.npz');system=np.load(P/'venous-volume-system.npz');meta=json.loads((P/'venous-volume-constraints.json').read_text());A=load_npz(P/'venous-volume-A.npz');E=load_npz(P/'venous-volume-E.npz');rhs=system['rhs'].copy();unknown=system['unknown'];N=len(unknown);M=len(rhs)
assert str(system['brainSha256'])==sha(P/'brain-trial.glb');assert str(system['sourceSha256'])==sha(P/'veins-volume-source.glb')
ids=np.array([i for i,r in enumerate(meta) if r[1]=='tissue']);p=np.array([meta[i][2] for i in ids]);front_old=p.copy();front_old[:,1]=p[:,1]-rhs[ids]-.18
lo=np.full(len(p),-145.);hi=np.full(len(p),5.)
for step in range(27):
 mid=(lo+hi)/2;q=front_old.copy();q[:,1]=mid;mapped=old.apply(q)[:,1];left=mapped<front_old[:,1];lo[left]=mid[left];hi[~left]=mid[~left]
source=front_old.copy();source[:,1]=(lo+hi)/2;error=float(np.max(abs(old.apply(source)[:,1]-front_old[:,1])));assert error<2e-5,error
front_new=new.apply(source)[:,1];rhs[ids]=p[:,1]-front_new-.18
print('Rebound tissue constraints',len(ids),'inverse error',error,flush=True)
desired=system['desired'].copy();points=np.stack(np.meshgrid(*[system['origin'][i]+system['step'][i]*np.arange(system['shape'][i]) for i in range(3)],indexing='ij'),axis=-1).reshape(-1,3)[unknown];desired+=(new.apply(points)-old.apply(points))[:,1]
Z=coo_matrix((M,N));ZE=coo_matrix((E.shape[0],N));limits=system['edgeLimits'].copy();nonlongitudinal=limits[:,0]>2;limits[nonlongitudinal]=8.
C=vstack([hstack([A,Z]),hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)]),hstack([E,ZE]),hstack([-E,ZE])]).tocsr();b=np.r_[rhs,desired,-desired,limits[:,0],limits[:,1]]
solution=linprog(np.r_[np.zeros(N),np.ones(N)],A_ub=C,b_ub=b,bounds=[(-20,30)]*N+[(0,None)]*N,method='highs',options={'time_limit':55})
report={'success':bool(solution.success),'message':solution.message,'brainSha256':sha(W/'brain-trial.glb'),'sourceSha256':sha(P/'veins-volume-source.glb'),'tissueConstraintsRebound':len(ids),'inverseFieldErrorMm':error,'allWallConstraintsRetained':M,'variableNodes':N}
(W/'venous-solver.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
if not solution.success:
 softC=vstack([hstack([A,Z,-eye(M)])]+[hstack([c,coo_matrix((c.shape[0],M))]) for c in [hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)]),hstack([E,ZE]),hstack([-E,ZE])]]).tocsr()
 soft=linprog(np.r_[np.zeros(N),np.full(N,.001),np.ones(M)],A_ub=softC,b_ub=b,bounds=[(-20,30)]*N+[(0,None)]*(N+M),method='highs',options={'time_limit':55})
 if soft.success:
  slack=soft.x[2*N:];idx=np.argsort(-slack)[:30];report['maximumViolationMm']=float(slack.max());report['violations']=[[*meta[i],float(slack[i])] for i in idx if slack[i]>1e-5];(W/'venous-infeasibility.json').write_text(json.dumps(report,indent=2)+'\n');print('Minimum wall violation',report['maximumViolationMm'],flush=True)
 raise SystemExit(1)
grid=Grid.__new__(Grid);grid.origin=system['origin'];grid.step=system['step'];grid.shape=system['shape'];grid.delta=np.zeros(grid.shape);grid.delta.ravel()[unknown]=solution.x[:N];grid.frozen=system['frozen']
doc,data=read_glb(APP/'.authoring/brainstem19/veins-baseline.glb');source=trimesh.load(P/'veins-volume-source.glb',process=False);target={};changes=[]
from fit_brainstem_shear import SELECTED
for k in sorted(SELECTED):
 a=source.geometry[k];q=grid.apply(a.vertices);bb=trimesh.Trimesh(q,a.faces,process=False);target[k]=(q,a.faces,bb.vertex_normals);changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-a.vertices,axis=1).max())})
save_replaced(W/'veins-trial.glb',doc,data,target);np.savez_compressed(W/'venous-map.npz',origin=grid.origin,step=grid.step,delta=grid.delta,frozen=grid.frozen);(W/'vein-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged connected vein fit',flush=True)
