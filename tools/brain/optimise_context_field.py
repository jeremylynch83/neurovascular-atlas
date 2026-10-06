"""Preserve closed regional volumes while solving an ordered displacement.

Volume is linear in the Y coordinates when X/Z stay fixed. The LP therefore
constrains the actual material surface volume, rather than a voxel surrogate.
This is a staged authoring solve; no production files are written.
"""
import json,numpy as np,trimesh
from scipy.sparse import coo_matrix,eye,hstack,vstack
from scipy.optimize import linprog
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap
from constrain_reconciliation import freeze
from fit_brainstem_shear import SELECTED
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
PREVIOUS=APP/'.authoring/brainstem19-coordinated';WORK=APP/'.authoring/brainstem20-optimised'

def weights(m,p):
 u=p-m.origin;i=np.floor(u).astype(int);v=u-i;good=np.all(i>=0,axis=1)&np.all(i<m.shape-1,axis=1);i=np.clip(i,0,m.shape-2)
 order=np.argsort(-v,axis=1);frac=np.take_along_axis(v,order,axis=1);w=np.column_stack([1-frac[:,0],frac[:,0]-frac[:,1],frac[:,1]-frac[:,2],frac[:,2]]);w[~good]=0
 ids=[np.ravel_multi_index(i.T,m.shape)]
 for a in range(3):i[np.arange(len(i)),order[:,a]]+=1;ids.append(np.ravel_multi_index(i.T,m.shape))
 return np.array(ids).T,w

def main():
 WORK.mkdir(exist_ok=True)
 z=np.load(PREVIOUS/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=z['origin'];m.shape=np.array(z['delta'].shape);m.mask=z['mask'].copy();m.delta=z['delta'].copy()
 veins=trimesh.load(PREVIOUS/'veins-baseline.glb',process=False)
 frozen_veins={'vein.occipital_sinus','vein.marginal','vein.inferior_vermian.left','vein.inferior_vermian.right','vein.posterior_communicating'}
 freeze(m.mask,m.origin,veins,frozen_veins)
 active=(z['delta']>1e-8)&~m.mask
 unknown=np.flatnonzero(active.ravel());lookup=np.full(np.prod(m.shape),-1,int);lookup[unknown]=np.arange(len(unknown));N=len(unknown)
 print('Unknown nodes',N,flush=True)
 sd,sb=read_glb(PREVIOUS/'brain-source-refined.glb');records=mesh_records(sd,sb);brain=trimesh.load(PREVIOUS/'brain-source-refined.glb',process=False)
 target=z['delta'].ravel()[unknown].copy()
 x,y,zz=np.unravel_index(unknown,m.shape);points=np.column_stack([x,y,zz])+m.origin
 # Shift only the anterior tissue and its immediately adjoining context.
 target*=np.clip((points[:,1]+115)/22,0,1)
 constraints=[];rhs=[];volumes=[]
 for k,r in records.items():
  a=brain.geometry[k]
  if not a.is_watertight or not (k.startswith('brain.') and np.any(z['delta'])):continue
  p=r['old'];f=r['faces'];coeff=np.zeros(len(p))
  for a0,b,c in [(0,1,2),(1,2,0),(2,0,1)]:np.add.at(coeff,f[:,a0],np.cross(p[f[:,b]],p[f[:,c]])[:,1]/6)
  ids,w=weights(m,p);indices=lookup[ids];values=-(coeff[:,None]*w);good=indices>=0
  row=coo_matrix((values[good],(np.zeros(int(good.sum()),int),indices[good])),shape=(1,N)).tocsr();row.eliminate_zeros()
  if not row.nnz:continue
  limit=.01*abs(a.volume);constraints += [hstack([row,coo_matrix((1,N))]),hstack([-row,coo_matrix((1,N))])];rhs += [np.array([limit]),np.array([limit])];volumes.append({'node':k,'volumeMm3':float(a.volume),'maximumChangeFraction':.01})
 print('Closed volume constraints',len(volumes),flush=True)
 ids=np.arange(np.prod(m.shape)).reshape(m.shape);all_E=[];all_limits=[]
 for axis in range(3):
  a=[slice(None)]*3;b=a.copy();a[axis]=slice(None,-1);b[axis]=slice(1,None);pairs=np.column_stack([ids[tuple(a)].ravel(),ids[tuple(b)].ravel()]);pairs=pairs[np.any(lookup[pairs]>=0,axis=1)]
  idx=lookup[pairs];rr=np.repeat(np.arange(len(pairs)),2);cc=idx.ravel();vv=np.tile([-1.,1.],len(pairs));good=cc>=0
  E=coo_matrix((vv[good],(rr[good],cc[good])),shape=(len(pairs),N)).tocsr();zero=coo_matrix((len(pairs),N))
  # det(dF)=1-d(delta)/dy. Every tetrahedron remains strictly ordered.
  upper=.7 if axis==1 else 1.5;lower=1.5
  constraints += [hstack([E,zero]),hstack([-E,zero])];rhs += [np.full(len(pairs),upper),np.full(len(pairs),lower)]
 constraints += [hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)])];rhs += [target,-target]
 # Most weight falls on the exposed brainstem. Posterior tissue is a soft
 # companion target subject to exact volume/interface constraints.
 importance=np.ones(N);importance[(points[:,1]>-95)&(np.abs(points[:,0]-.65)<16)&(points[:,2]>24)&(points[:,2]<76)]=8
 sol=linprog(np.r_[np.zeros(N),importance],A_ub=vstack(constraints).tocsr(),b_ub=np.concatenate(rhs),bounds=[(0,8)]*N+[(0,None)]*N,method='highs',options={'time_limit':55})
 report={'success':bool(sol.success),'message':sol.message,'unknownNodes':N,'closedVolumeConstraints':volumes}
 (WORK/'solver.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
 if not sol.success:raise SystemExit(1)
 m.delta=np.zeros(m.shape);m.delta.ravel()[unknown]=sol.x[:N];m.minimumYDerivative=float(1-np.diff(m.delta,axis=1).max())
 doc,data=read_glb(PREVIOUS/'brain-baseline.glb');source={};target={};changes=[]
 for k,r in records.items():
  p,f=r['old'],r['faces'];q=m.apply(p);maximum=float(np.linalg.norm(q-p,axis=1).max())
  if maximum<1e-5:continue
  a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
  changes.append({'node':k,'maximumDisplacementMm':maximum,'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None,'closedSource':bool(a.is_watertight),'closedCandidate':bool(b.is_watertight)})
 save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target)
 np.savez_compressed(WORK/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
 (WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n');(WORK/'map.json').write_text(json.dumps({'method':'ordered exact tetrahedral field, protected dural venous cells, closed regional volume changes bounded to one percent','minimumYDerivative':m.minimumYDerivative,'brainSha256':sha(WORK/'brain-trial.glb'),'changes':changes},indent=2)+'\n')
 print('Optimised brain candidate staged',flush=True)
if __name__=='__main__':main()
