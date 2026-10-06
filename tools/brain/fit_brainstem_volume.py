"""Fit connected venous material in three dimensions, with fixed dural skin.

An ordered tetrahedral coordinate field keeps X/Z unchanged. Complete cells
occupied by retained veins and bone are stationary. Source facets are split
at every field boundary before applying the map. Outputs are authoring trials.
"""
import json,itertools
import numpy as np,trimesh
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix,hstack,vstack,eye,save_npz
from scipy.optimize import linprog
from fit_vessels import APP,read_glb,mesh_records,ray_tree,hits,curve_from_mesh
from fit_brainstem_shear import SELECTED
from reconcile_brainstem import ANTERIOR,TRANSVERSE,sha
from reconcile_local_volume import WORK,split_mesh,close_roundoff_holes
from transport_local_volume import load_map
from refine_context_skin import save_replaced

PRIMARY=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal'])

class Grid:
 def __init__(self,records):
  self.origin=np.array([-52.,-136.,-36.]);self.step=np.array([2.,2.,2.]);self.shape=np.array([55,60,68]);self.delta=np.zeros(self.shape)
  self.points=np.stack(np.meshgrid(*[self.origin[i]+self.step[i]*np.arange(self.shape[i]) for i in range(3)],indexing='ij'),axis=-1).reshape(-1,3)
  p=np.concatenate([records[k]['old'] for k in SELECTED]);tree=cKDTree(p[:,[0,2]])
  active=(tree.query(self.points[:,[0,2]])[0]<10).reshape(self.shape)
  active[:,[0,-1],:]=False;active[[0,-1],:,:]=False;active[:,:,[0,-1]]=False
  self.frozen=~active
 def freeze(self,meshes):
  for m in meshes:
   t=m.vertices[m.faces];lo=(t.min(1)-self.origin)/self.step;hi=(t.max(1)-self.origin)/self.step
   keep=np.all(hi>=0,axis=1)&np.all(lo<self.shape-1,axis=1)
   for a,b in zip(lo[keep],hi[keep]):
    a=np.maximum(0,np.floor(a).astype(int));b=np.minimum(self.shape-1,np.floor(b).astype(int)+1)
    self.frozen[a[0]:b[0]+1,a[1]:b[1]+1,a[2]:b[2]+1]=True
 def rows(self,p):
  u=(p-self.origin)/self.step;i=np.floor(u).astype(int);v=u-i;good=np.all(i>=0,axis=1)&np.all(i<self.shape-1,axis=1)
  i=np.clip(i,0,self.shape-2);order=np.argsort(-v,axis=1);fraction=np.take_along_axis(v,order,axis=1)
  weights=np.column_stack([1-fraction[:,0],fraction[:,0]-fraction[:,1],fraction[:,1]-fraction[:,2],fraction[:,2]]);weights[~good]=0
  ids=[np.ravel_multi_index(i.T,self.shape)]
  for a in range(3):
   i[np.arange(len(i)),order[:,a]]+=1;ids.append(np.ravel_multi_index(i.T,self.shape))
  return np.array(ids).T,weights
 def apply(self,p):
  ids,w=self.rows(p);q=p.copy();q[:,1]+=(self.delta.ravel()[ids]*w).sum(1);return q
 def refine(self,m):
  temp=trimesh.Trimesh((m.vertices-self.origin)/self.step,m.faces,process=False);p,f=split_mesh(temp);p=self.origin+p*self.step
  if m.is_watertight:f,_=close_roundoff_holes(p,f)
  return trimesh.Trimesh(p,f,process=False)

def main():
 d,b=read_glb(WORK/'veins-baseline.glb');records=mesh_records(d,b);grid=Grid(records)
 source_scene=trimesh.load(WORK/'veins-baseline.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
 # Bone is checked against the final skin, rather than occupying conservative
 # voxel boxes that can pin a vessel several millimetres from the actual bone.
 grid.freeze([m for k,m in source_scene.geometry.items() if k not in SELECTED])
 unknown=np.flatnonzero(~grid.frozen.ravel());lookup=np.full(np.prod(grid.shape),-1,int);lookup[unknown]=np.arange(len(unknown));N=len(unknown)
 print('Field nodes',N,'stationary',int(grid.frozen.sum()),flush=True)
 outside=np.concatenate([r['old'] for k,r in records.items() if k not in SELECTED]);tree=cKDTree(outside)
 shared=np.concatenate([r['old'][tree.query(r['old'])[0]<1e-5] for k,r in records.items() if k in SELECTED]);fixed=cKDTree(shared)
 mapping=load_map();brain=trimesh.load(WORK/'brain-baseline.glb',process=False)
 stem=ray_tree(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]))
 mesh=trimesh.util.concatenate(list(bones.geometry.values()));tri=mesh.vertices[mesh.faces];lo=np.array([-53,-137,-36]);hi=np.array([57,-15,100]);keep=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);bone=ray_tree(trimesh.Trimesh(mesh.vertices,mesh.faces[keep],process=False))
 cache={}
 def surface(x,z):
  key=(round(float(x),6),round(float(z),6))
  if key in cache:return cache[key]
  h=hits(stem,[x,5,z],[x,-145,z]);front=float(mapping.apply(h)[:,1].max()) if len(h) else None
  h=hits(bone,[x,-135,z],[x,20,z]);h=h[h[:,1]>(front+.1 if front is not None else -115)] if len(h) else h;bony=float(h[:,1].min()) if len(h) else None
  cache[key]=(front,bony);return front,bony
 refined={};source={};samples=[];values=[]
 for k in sorted(SELECTED):
  old=source_scene.geometry[k];m=grid.refine(old);refined[k]=m;source[k]=(m.vertices,m.faces,m.vertex_normals)
  if k in PRIMARY:
   course=curve_from_mesh(old,axis=0 if k in TRANSVERSE else 2,n=100)
   for p in course:
    front,_=surface(p[0],p[2]);target=p[1] if front is None else front+1.5;samples.append(p);values.append(target-p[1])
  print('Refined',k,len(m.vertices),len(m.faces),flush=True)
 save_replaced(WORK/'veins-volume-source.glb',d,b,source)
 samples=np.array(samples);values=np.array(values);stree=cKDTree(samples);dist,idx=stree.query(grid.points[unknown],k=8);weights=1/(dist*dist+1)**2;desired=(weights*values[idx]).sum(1)/weights.sum(1);desired*=np.exp(-np.maximum(0,dist[:,0]-5)**2/16**2);desired=np.clip(desired,-15,25)
 rows=[];cols=[];data=[];rhs=[];metadata=[]
 def add(ids,w,limit,meta):
  index=len(rhs);ids=lookup[ids];good=ids>=0;rows.extend([index]*int(good.sum()));cols.extend(ids[good].tolist());data.extend(w[good].tolist());rhs.append(limit);metadata.append(meta)
 for k,m in refined.items():
  # Centres and edge midpoints prevent a wall facet bridging a narrow ridge.
  p=np.vstack([m.vertices,m.triangles.mean(1)]);ids,w=grid.rows(p);distance=fixed.query(p)[0]
  for n,q in enumerate(p):
   front,bony=surface(q[0],q[2])
   if k in PRIMARY and front is not None and distance[n]>6:add(ids[n],-w[n],q[1]-front-.18,[k,'tissue',q.tolist()])
   if bony is not None and bony>q[1]+.1:add(ids[n],w[n],bony-.18-q[1],[k,'bone',q.tolist()])
  print('Wall constraints',k,len(rhs),flush=True)
 M=len(rhs);A=coo_matrix((data,(rows,cols)),shape=(M,N)).tocsr();Z=coo_matrix((M,N)).tocsr();constraints=[hstack([A,Z]),hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)])];bounds=[np.array(rhs),desired,-desired]
 # Strict anterior/posterior order in every tetrahedron. Spatial shear limits
 # also bound the distortion of the collector transition walls.
 edges=[];limits=[]
 for axis in range(3):
  ids=np.arange(np.prod(grid.shape)).reshape(grid.shape);a=[slice(None)]*3;c=a.copy();a[axis]=slice(None,-1);c[axis]=slice(1,None);pairs=np.column_stack([ids[tuple(a)].ravel(),ids[tuple(c)].ravel()]);pairs=pairs[np.any(lookup[pairs]>=0,axis=1)]
  for s,t in pairs:
   edges.append((s,t));limits.append((.85*grid.step[axis],1.5*grid.step[axis]) if axis==1 else (1.8*grid.step[axis],1.8*grid.step[axis]))
 edges=np.array(edges);ids=lookup[edges];er=np.repeat(np.arange(len(edges)),2);ec=ids.ravel();val=np.tile([1.,-1.],len(edges));good=ec>=0;E=coo_matrix((val[good],(er[good],ec[good])),shape=(len(edges),N)).tocsr();Z=coo_matrix((len(edges),N)).tocsr();constraints.extend([hstack([E,Z]),hstack([-E,Z])]);bounds.extend([np.array(limits)[:,0],np.array(limits)[:,1]])
 save_npz(WORK/'venous-volume-A.npz',A);save_npz(WORK/'venous-volume-E.npz',E)
 np.savez_compressed(WORK/'venous-volume-system.npz',rhs=np.array(rhs),desired=desired,unknown=unknown,origin=grid.origin,step=grid.step,shape=grid.shape,frozen=grid.frozen,edgeLimits=np.array(limits),brainSha256=sha(WORK/'brain-trial.glb'),sourceSha256=sha(WORK/'veins-volume-source.glb'))
 (WORK/'venous-volume-constraints.json').write_text(json.dumps(metadata))
 lp=linprog(np.r_[np.zeros(N),np.ones(N)],A_ub=vstack(constraints).tocsr(),b_ub=np.concatenate(bounds),bounds=[(-20,30)]*N+[(0,None)]*N,method='highs')
 report={'success':bool(lp.success),'message':lp.message,'variableNodes':N,'wallConstraints':M,'brainSha256':sha(WORK/'brain-trial.glb')}
 (WORK/'venous-volume-solver.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
 if not lp.success:
  soft=linprog(np.r_[np.zeros(N),np.full(N,.001),np.ones(M)],A_ub=vstack([hstack([A,coo_matrix((M,N)),-eye(M)])]+[hstack([a,coo_matrix((a.shape[0],M))]) for a in constraints[1:]]).tocsr(),b_ub=np.concatenate(bounds),bounds=[(-20,30)]*N+[(0,None)]*(N+M),method='highs')
  if soft.success:
   slack=soft.x[2*N:];indices=np.argsort(-slack)[:40];report['totalViolationMm']=float(slack.sum());report['maximumViolationMm']=float(slack.max());report['violations']=[[*metadata[i],float(slack[i])] for i in indices if slack[i]>1e-5];(WORK/'venous-volume-infeasibility.json').write_text(json.dumps(report,indent=2)+'\n');grid.delta.ravel()[unknown]=soft.x[:N];np.savez_compressed(WORK/'venous-volume-rejected-map.npz',origin=grid.origin,step=grid.step,delta=grid.delta,frozen=grid.frozen);print('Minimum violation',report['maximumViolationMm'],flush=True)
  raise SystemExit(1)
 grid.delta.ravel()[unknown]=lp.x[:N];replacements={};changes=[]
 for k,m in refined.items():
  q=grid.apply(m.vertices);target=trimesh.Trimesh(q,m.faces,process=False);replacements[k]=(q,m.faces,target.vertex_normals);changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-m.vertices,axis=1).max()),'sourceTriangles':len(source_scene.geometry[k].faces),'refinedTriangles':len(m.faces)})
 save_replaced(WORK/'veins-volume-trial.glb',d,b,replacements);np.savez_compressed(WORK/'venous-volume-map.npz',origin=grid.origin,step=grid.step,delta=grid.delta,frozen=grid.frozen)
 (WORK/'vein-volume-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged connected venous field',flush=True)

if __name__=='__main__':main()
