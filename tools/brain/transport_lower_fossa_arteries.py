"""Carry posterior arterial relationships with the registered lower fossa.

The existing ICA and central arterial corrections are retained exactly. Shared
arterial boundary collars are stationary cells of the common ordered field.
"""
import json,numpy as np,trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap,arterial_movable
from refine_context_skin import save_replaced
from constrain_reconciliation import freeze
from reconcile_brainstem import sha
W=APP/'.authoring/brainstem20-lower-final';P=APP/'.authoring/brainstem19-coordinated'
v=np.load(W/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.shape=np.array(v['delta'].shape);m.delta=v['delta'].copy();m.mask=v['mask'].copy()
bd,bb=read_glb(APP/'.authoring/brainstem19/arteries-baseline.glb');baseline=mesh_records(bd,bb);sd,sb=read_glb(P/'arteries-source-refined.glb');refined=mesh_records(sd,sb)
selected={k for k,r in baseline.items() if arterial_movable(k) and np.max(abs(m.amount(r['old'])))>1e-5}
outside=np.concatenate([r['old'] for k,r in baseline.items() if k not in selected]);tree=cKDTree(outside)
for k in selected:
 r=baseline[k];shared=tree.query(r['old'])[0]<2e-5;edges=np.vstack([r['faces'][:,[0,1]],r['faces'][:,[1,2]],r['faces'][:,[2,0]]]);edges=edges[shared[edges].all(1)]
 for edge in edges:
  lo=np.maximum(0,np.floor(r['old'][edge].min(0)-m.origin).astype(int));hi=np.minimum(m.shape-1,np.floor(r['old'][edge].max(0)-m.origin).astype(int)+1)
  if np.all(hi>=lo):m.delta[lo[0]:hi[0]+1,lo[1]:hi[1]+1,lo[2]:hi[2]+1]=0;m.mask[lo[0]:hi[0]+1,lo[1]:hi[1]+1,lo[2]:hi[2]+1]=True
for iteration in range(60):
 old=m.delta.copy()
 for j in range(1,m.shape[1]):m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j-1,:]-.15,m.delta[:,j-1,:]+.15);m.delta[:,j,:][m.mask[:,j,:]]=0
 for j in range(m.shape[1]-2,-1,-1):m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j+1,:]-.15,m.delta[:,j+1,:]+.15);m.delta[:,j,:][m.mask[:,j,:]]=0
 if np.max(abs(m.delta-old))<1e-9:break
source={};target={};changes=[]
for k in sorted(selected):
 r=refined[k];p,f=r['old'],r['faces'];q=m.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
 source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
 changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'role':'retained-posterior-relationship-transport','sourceTriangles':len(baseline[k]['faces']),'refinedTriangles':len(f)})
 print('Transported',k,changes[-1]['maximumDisplacementMm'],flush=True)
save_replaced(W/'arteries-source-refined.glb',bd,bb,source);save_replaced(W/'arteries-trial.glb',bd,bb,target)
np.savez_compressed(W/'arterial-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
(W/'artery-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged posterior artery transport',len(changes),flush=True)
