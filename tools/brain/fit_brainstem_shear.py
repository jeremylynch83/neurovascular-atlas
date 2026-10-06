"""Constrained, piecewise affine Y shear of anterior brainstem venous skin.

Wall constraints use the actual refined source vertices. Shared collector
edges occupy stationary field cells. The field has unit Jacobian determinant;
material facets are split before applying it. No production writes occur.
"""
import itertools,json
import numpy as np,trimesh
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,vstack,eye,save_npz
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,ray_tree,hits
from reconcile_brainstem import ANTERIOR,TRANSVERSE,sha
from reconcile_anterior_brainstem import split_mesh as split_yz,InterfaceMap
from reconcile_local_volume import WORK
from transport_local_volume import load_map
from refine_context_skin import save_replaced
SELECTED=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']])
class ShearGrid:
 def __init__(self):
  self.x=np.arange(-29.,30.);self.z=np.arange(-28.,92.);self.shape=(len(self.x),len(self.z));self.delta=np.zeros(self.shape)
 def rows(self,p):
  u=p[:,0]-self.x[0];v=p[:,2]-self.z[0];i=np.floor(u).astype(int);j=np.floor(v).astype(int);good=(i>=0)&(j>=0)&(i<self.shape[0]-1)&(j<self.shape[1]-1);i=np.clip(i,0,self.shape[0]-2);j=np.clip(j,0,self.shape[1]-2);u=np.clip(u-i,0,1);v=np.clip(v-j,0,1)
  low=u>=v;ids=np.column_stack([i*self.shape[1]+j,(i+low)*self.shape[1]+j+(~low),(i+1)*self.shape[1]+j+1]);weights=np.column_stack([1-np.maximum(u,v),np.abs(u-v),np.minimum(u,v)]);weights[~good]=0
  return ids,weights
 def apply(self,p):
  ids,w=self.rows(p);q=p.copy();q[:,1]+=(self.delta.ravel()[ids]*w).sum(1);return q

def main():
 d,b=read_glb(WORK/'veins-baseline.glb');records=mesh_records(d,b);grid=ShearGrid()
 mapping=load_map()
 brain=trimesh.load(WORK/'brain-baseline.glb',process=False)
 stem=ray_tree(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]))
 bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);mesh=trimesh.util.concatenate(list(bones.geometry.values()));tri=mesh.vertices[mesh.faces];lo=np.array([-29,-115,-28]);hi=np.array([30,30,92]);keep=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);bone=ray_tree(trimesh.Trimesh(mesh.vertices,mesh.faces[keep],process=False))
 cache={}
 def surface(x,z):
  key=(float(x),float(z))
  if key in cache:return cache[key]
  h=hits(stem,[x,5,z],[x,-145,z])
  front=float(mapping.apply(h)[:,1].max()) if len(h) else None
  h=hits(bone,[x,-135,z],[x,30,z]);anterior=h[h[:,1]>(front+.1 if front is not None else -115)] if len(h) else h
  bony=float(anterior[:,1].min()) if len(anterior) else None
  cache[key]=(front,bony);return front,bony

 outside=np.concatenate([r['old'] for k,r in records.items() if k not in SELECTED]);tree=cKDTree(outside);shared=[]
 for k in SELECTED:
  p=records[k]['old'];shared.extend(p[tree.query(p)[0]<1e-5])
 shared=np.array(shared);fixed=cKDTree(shared[:,[0,2]])
 node_p=np.array([[x,0,z] for x in grid.x for z in grid.z]);ids,w=grid.rows(shared);frozen=np.zeros(np.prod(grid.shape),bool);frozen[ids.ravel()]=True
 frozen.reshape(grid.shape)[[0,-1],:]=True;frozen.reshape(grid.shape)[:,[0,-1]]=True
 for k in SELECTED:
  r=records[k];p=r['old'];is_shared=tree.query(p)[0]<1e-5
  for edge in np.vstack([r['faces'][:,[0,1]],r['faces'][:,[1,2]],r['faces'][:,[2,0]]]):
   if not is_shared[edge].all():continue
   a,c=p[edge];lo=np.floor(np.minimum(a[[0,2]],c[[0,2]])-[grid.x[0],grid.z[0]]).astype(int);hi=np.floor(np.maximum(a[[0,2]],c[[0,2]])-[grid.x[0],grid.z[0]]).astype(int)+1;lo=np.maximum(lo,0);hi=np.minimum(hi,np.array(grid.shape)-1);frozen.reshape(grid.shape)[lo[0]:hi[0]+1,lo[1]:hi[1]+1]=True
 source={};refined={};samples=[];values=[]
 for k in sorted(SELECTED):
  r=records[k];old=trimesh.Trimesh(r['old'],r['faces'],process=False);tmp=trimesh.Trimesh(old.vertices[:,[1,0,2]],old.faces,process=False);dummy=InterfaceMap.__new__(InterfaceMap);p,f=split_yz(tmp,dummy);p=p[:,[1,0,2]];m=trimesh.Trimesh(p,f,process=False);source[k]=(p,f,m.vertex_normals);refined[k]=m
  course=curve_from_mesh(old,axis=0 if k in TRANSVERSE else 2,n=100)
  for q in course:
   front,bony=surface(q[0],q[2])
   if front is not None:target=front+(1.4 if q[2]>65 else 1.7)
   else:target=q[1]
   samples.append(q[[0,2]]);values.append(target-q[1])
  print('Refined',k,len(p),flush=True)
 save_replaced(WORK/'veins-source-refined.glb',d,b,source)
 samples=np.array(samples);values=np.array(values);_,unique=np.unique(np.round(samples,5),axis=0,return_index=True);rbf=RBFInterpolator(samples[unique],values[unique],smoothing=.3,neighbors=24,kernel='gaussian',epsilon=.1,degree=0);desired=np.clip(rbf(node_p[:,[0,2]]),-20,25);desired[frozen]=0
 rows=[];cols=[];data=[];bounds=[];constraint_count=0;metadata=[]
 def constraint(ids,weights,limit,kind,key,p):
  nonlocal constraint_count
  rows.extend([constraint_count]*3);cols.extend(ids.tolist());data.extend(weights.tolist());bounds.append(limit);metadata.append([key,kind,p.tolist()]);constraint_count+=1
 for k,m in refined.items():
  ids,w=grid.rows(m.vertices);distance=fixed.query(m.vertices[:,[0,2]])[0]
  for n,p in enumerate(m.vertices):
   front,bony=surface(p[0],p[2])
   if front is not None and distance[n]>6:constraint(ids[n],-w[n],p[1]-front-.18,'tissue',k,p)
   if bony is not None and bony>p[1]+.1:constraint(ids[n],w[n],bony-.18-p[1],'bone',k,p)

  print('Wall constraints',k,constraint_count,flush=True)
 N=len(node_p);A=coo_matrix((data,(rows,cols)),shape=(constraint_count,N)).tocsr();zero=coo_matrix((constraint_count,N)).tocsr();constraints=[hstack([A,zero]),hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)])];rhs=[np.array(bounds),desired,-desired]
 # Limit section shear so collector transitions retain usable wall envelopes.
 edge=[];edge_limit=[]
 for i in range(grid.shape[0]):
  for j in range(grid.shape[1]):
   a=i*grid.shape[1]+j
   if i+1<grid.shape[0]:edge.append((a,a+grid.shape[1]));edge_limit.append(1.8)
   if j+1<grid.shape[1]:edge.append((a,a+1));edge_limit.append(2.4)
 e=np.array(edge);E=coo_matrix((np.tile([1.,-1.],len(e)),(np.repeat(np.arange(len(e)),2),e.ravel())),shape=(len(e),N)).tocsr();Z=coo_matrix((len(e),N)).tocsr();constraints.extend([hstack([E,Z]),hstack([-E,Z])]);rhs.extend([np.array(edge_limit),np.array(edge_limit)])
 limits=[(0,0) if frozen[n] else (-25,30) for n in range(N)]+[(0,None)]*N
 save_npz(WORK/'venous-constraints.npz',A);np.savez_compressed(WORK/'venous-solver-input.npz',rhs=np.array(bounds),desired=desired,frozen=frozen,edges=e,edgeLimits=np.array(edge_limit));(WORK/'venous-constraint-points.json').write_text(json.dumps(metadata))
 result=linprog(np.r_[np.zeros(N),np.ones(N)],A_ub=vstack(constraints).tocsr(),b_ub=np.concatenate(rhs),bounds=limits,method='highs')
 (WORK/'venous-field-solver.json').write_text(json.dumps({'success':bool(result.success),'status':result.message,'constraints':constraint_count,'fixedNodes':int(frozen.sum())},indent=2)+'\n')
 if not result.success:
  M=constraint_count
  relaxed=[hstack([A,zero,-eye(M)])]+[hstack([a,coo_matrix((a.shape[0],M)).tocsr()]) for a in constraints[1:]]
  soft=linprog(np.r_[np.zeros(N),np.full(N,.001),np.ones(M)],A_ub=vstack(relaxed).tocsr(),b_ub=np.concatenate(rhs),bounds=limits+[(0,None)]*M,method='highs')
  if soft.success:
   slack=soft.x[2*N:];indices=np.argsort(-slack)[:40];(WORK/'venous-infeasibility.json').write_text(json.dumps({'totalMinimumViolationMm':float(slack.sum()),'maximumViolationMm':float(slack.max()),'violations':[[*metadata[i],float(slack[i])] for i in indices if slack[i]>1e-5]},indent=2)+'\n')
 assert result.success,result.message
 grid.delta=result.x[:N].reshape(grid.shape);target={};changes=[]
 for k,m in refined.items():
  p,f=m.vertices,m.faces;q=grid.apply(p);a=trimesh.Trimesh(q,f,process=False);target[k]=(q,f,a.vertex_normals);changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'refinedTriangles':len(f)})
 save_replaced(WORK/'veins-trial.glb',d,b,target);np.savez_compressed(WORK/'venous-shear.npz',x=grid.x,z=grid.z,delta=grid.delta,fixed=frozen)
 (WORK/'vein-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged constrained venous shear',flush=True)
if __name__=='__main__':main()
