"""Exact ordered section shear of the connected anterior venous group.

Only the three longitudinal veins, four transverse veins, anterior spinal
transition and posterior communicating vein move. Their collector outlets
remain fixed. Material triangles are split on every field boundary first.
"""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix,eye,hstack,vstack
from scipy.optimize import linprog
from scipy.interpolate import RBFInterpolator
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh
from build_targets import poly
from reconcile_brainstem import ANTERIOR,TRANSVERSE,sha
from fit_brainstem_shear import ShearGrid
from reconcile_anterior_brainstem import split_mesh,InterfaceMap
from refine_context_skin import save_replaced
W=APP/'.authoring/brainstem21-section'
KEYS=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal','vein.posterior_communicating'])

def main():
 global W
 parser=argparse.ArgumentParser();parser.add_argument('--brain-directory',default='.authoring/brainstem21-skin');parser.add_argument('--output-directory',default='.authoring/brainstem21-section');parser.add_argument('--preserve-xz',action='store_true');args=parser.parse_args()
 W=APP/args.output_directory
 W.mkdir(exist_ok=True)
 # Preserve a previous candidate with its matching evidence, then remove its
 # active name. A failed new solve must not leave an old result as its output.
 if (W/'veins-trial.glb').exists():
  history=W/'previous-candidates'/sha(W/'veins-trial.glb')
  history.mkdir(parents=True,exist_ok=True)
  for name in ['veins-trial.glb','veins-source.glb','brain-trial.glb','volume-map.npz','section-map.npz','solver.json','acceptance.json','containment.json']:
   if (W/name).exists():shutil.copyfile(W/name,history/name)
 for name in ['veins-trial.glb','section-map.npz','acceptance.json','acceptance-progress.json','containment.json','infeasibility.json']:
  (W/name).unlink(missing_ok=True)
 shutil.copyfile(APP/args.brain_directory/'brain-trial.glb',W/'brain-trial.glb')
 shutil.copyfile(APP/args.brain_directory/'volume-map.npz',W/'volume-map.npz')
 d,b=read_glb(APP/'.authoring/brainstem19/veins-baseline.glb');records=mesh_records(d,b)
 g=ShearGrid();g.x=np.arange(-33.,35.);g.z=np.arange(-30.,101.);g.shape=(len(g.x),len(g.z));g.delta=np.zeros(g.shape)
 outside=np.concatenate([r['old'] for k,r in records.items() if k not in KEYS]);tree=cKDTree(outside)
 frozen=np.zeros(g.shape,bool)
 frozen[[0,-1],:]=True;frozen[:,[0,-1]]=True;frozen[:,g.z<0]=True
 shared=[]
 for k in KEYS:
  r=records[k];p=r['old'];is_shared=tree.query(p)[0]<2e-5;shared.extend(p[is_shared])
  edges=np.vstack([r['faces'][:,[0,1]],r['faces'][:,[1,2]],r['faces'][:,[2,0]]])
  for edge in edges[is_shared[edges].all(1)]:
   a,c=p[edge];lo=np.floor(np.minimum(a[[0,2]],c[[0,2]])-[g.x[0],g.z[0]]).astype(int);hi=np.floor(np.maximum(a[[0,2]],c[[0,2]])-[g.x[0],g.z[0]]).astype(int)+1
   lo=np.maximum(lo,0);hi=np.minimum(hi,np.array(g.shape)-1);frozen[lo[0]:hi[0]+1,lo[1]:hi[1]+1]=True
 ids,_=g.rows(np.array(shared));frozen.ravel()[ids.ravel()]=True
 xx,zz=np.meshgrid(g.x,g.z,indexing='ij')
 # Follow the lateral pontine surface before entering the fixed petrosal
 # collector. A purely AP fit wrongly forces this terminal section in front
 # of the pons. This ordered X/Z map rounds the pons instead.
 tx=abs(xx-.65)
 lateral=np.interp(tx,[0,12,16,18,21,50],[0,0,.5,1.4,0,0])
 vertical=np.interp(zz,[-100,45,50,55,61,66,200],[0,0,0,1,1,0,0])
 xdelta=np.sign(xx-.65)*lateral*vertical
 upper=-5*np.clip((zz-67)/14,0,1)**2*(3-2*np.clip((zz-67)/14,0,1))
 width=np.clip((tx-9)/13,0,1);upper*=1-width*width*(3-2*width)
 dip_vertical=np.interp(zz,[-100,49,57,62,70,200],[0,0,1,1,0,0])
 dip=-np.where(xx>.65,2.2,1.6)*np.interp(tx,[0,12,16,18,21,50],[0,0,.5,1.,0,0])*dip_vertical
 zdelta=upper+dip
 if args.preserve_xz:xdelta[:]=0;zdelta[:]=0
 zdelta[frozen]=0
 # Every X/Z material triangle must retain positive orientation. Y transport
 # is a shear, so these determinants also bound the full 3D Jacobian.
 mapped_x=xx+xdelta;mapped_z=zz+zdelta
 determinants=[]
 for offsets in [[(0,0),(1,0),(1,1)],[(0,0),(1,1),(0,1)]]:
  a,b_,c=[np.stack([mapped_x[i:i+g.shape[0]-1,j:j+g.shape[1]-1],mapped_z[i:i+g.shape[0]-1,j:j+g.shape[1]-1]],axis=-1) for i,j in offsets]
  u=b_-a;v=c-a;determinants.append(u[:,:,0]*v[:,:,1]-u[:,:,1]*v[:,:,0])
 minimum_det=float(np.min(determinants));assert minimum_det>.25,minimum_det
 assert np.min(1+np.diff(xdelta,axis=0))>.5
 def lateral_map(p):
  ids,w=g.rows(p);q=p.copy();q[:,0]+=(xdelta.ravel()[ids]*w).sum(1);q[:,2]+=(zdelta.ravel()[ids]*w).sum(1);return q
 assert np.max(np.linalg.norm(lateral_map(np.array(shared))-np.array(shared),axis=1))<1e-6
 brain=trimesh.load(W/'brain-trial.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
 def loc(mesh):
  l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(mesh));l.BuildLocator();return l
 stem=loc(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]))
 bone=loc(trimesh.util.concatenate(list(bones.geometry.values())))
 neighbours=loc(trimesh.util.concatenate([m for k,m in brain.geometry.items() if not any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle','ventricle','sulc','lat-fis','aqueduct'])]))
 vein_scene=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
 retained=loc(trimesh.util.concatenate([m for k,m in vein_scene.geometry.items() if k not in KEYS]))
 outlet_tree=cKDTree(np.array(shared))
 def first(l,a,c):
  t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
  return q[1] if l.IntersectWithLine(a,c,1e-8,t,q,pc,sub,cell) else None
 cache={}
 def surface(x,z):
  key=(round(float(x),6),round(float(z),6))
  if key not in cache:
   f=first(stem,[x,5,z],[x,-145,z]);bb=first(bone,[x,f+.1 if f is not None else -115,z],[x,25,z]);cache[key]=(f,bb)
  return cache[key]
 source={};samples=[];wishes=[]
 for k in sorted(KEYS):
  r=records[k];old=trimesh.Trimesh(r['old'],r['faces'],process=False)
  temp=trimesh.Trimesh(old.vertices[:,[1,0,2]],old.faces,process=False)
  p,f=split_mesh(temp,InterfaceMap.__new__(InterfaceMap));p=p[:,[1,0,2]]
  m=trimesh.Trimesh(p,f,process=False);source[k]=(p,f,m.vertex_normals)
  axis=0 if k in TRANSVERSE or k=='vein.posterior_communicating' else 2
  curve=curve_from_mesh(old,axis=axis,n=120)
  for q in curve:
   mapped=lateral_map(q[None,:])[0]
   front,_=surface(mapped[0],mapped[2]);samples.append(q[[0,2]]);wishes.append(0 if front is None else front+1.3-q[1])
  print('Section-refined',k,len(p),flush=True)
 save_replaced(W/'veins-source.glb',d,b,source)
 N=np.prod(g.shape);nodes=np.array([[x,0,z] for x in g.x for z in g.z])
 samples=np.array(samples);wishes=np.array(wishes);_,unique=np.unique(np.round(samples,5),axis=0,return_index=True)
 desired=RBFInterpolator(samples[unique],wishes[unique],neighbors=24,smoothing=.5,kernel='gaussian',epsilon=.1,degree=0)(nodes[:,[0,2]])
 desired=np.clip(desired,-20,25);desired[frozen.ravel()]=0
 rows=[];cols=[];data=[];rhs=[];metadata=[]
 def add(ids,w,limit,meta):
  j=len(rhs);rows.extend([j]*3);cols.extend(ids);data.extend(w);rhs.append(limit);metadata.append(meta)
 for k,(p,f,_) in source.items():
  m=trimesh.Trimesh(p,f,process=False);q=np.vstack([p,m.triangles.mean(1),m.triangles[:,[0,1]].mean(1),m.triangles[:,[1,2]].mean(1),m.triangles[:,[2,0]].mean(1)])
  ids,weights=g.rows(q)
  mapped=lateral_map(q)
  for i,v in enumerate(q):
   front,bb=surface(mapped[i,0],mapped[i,2])
   if front is not None:add(ids[i],-weights[i],v[1]-front-.4,[k,'tissue',v.tolist()])
   if bb is not None and front is not None:add(ids[i],weights[i],bb-.4-v[1],[k,'bone',v.tolist()])
   if outlet_tree.query(v)[0]>2 and front is not None:
    origin=[mapped[i,0],front+.1 if front is not None else v[1]+.1,mapped[i,2]];end=[mapped[i,0],25,mapped[i,2]]
    for name,obstacle in [('retained-vein',retained)]:
     ceiling=first(obstacle,origin,end)
     if ceiling is not None:add(ids[i],weights[i],ceiling-.1-v[1],[k,name,v.tolist()])
  print('Constrained wall',k,len(rhs),flush=True)
 M=len(rhs);A=coo_matrix((data,(rows,cols)),shape=(M,N)).tocsr();Z=coo_matrix((M,N))
 C=[hstack([A,Z]),hstack([eye(N),-eye(N)]),hstack([-eye(N),-eye(N)])];R=[np.array(rhs),desired,-desired]
 # Bound the shear gradient while maintaining unit determinant exactly.
 edges=[];limits=[]
 for i in range(g.shape[0]):
  for j in range(g.shape[1]):
   a=i*g.shape[1]+j
   if i+1<g.shape[0]:edges.append([a,a+g.shape[1]]);limits.append(3.)
   if j+1<g.shape[1]:edges.append([a,a+1]);limits.append(3.)
 edges=np.array(edges);E=coo_matrix((np.tile([1.,-1.],len(edges)),(np.repeat(np.arange(len(edges)),2),edges.ravel())),shape=(len(edges),N)).tocsr();ZE=coo_matrix((len(edges),N));C.extend([hstack([E,ZE]),hstack([-E,ZE])]);R.extend([np.array(limits),np.array(limits)])
 K=E.shape[0]
 smooth_C=[hstack([c,coo_matrix((c.shape[0],K))]) for c in C]
 smooth_C.extend([hstack([E,ZE,-eye(K)]),hstack([-E,ZE,-eye(K)])])
 result=linprog(np.r_[np.zeros(N),np.ones(N),np.full(K,.15)],A_ub=vstack(smooth_C).tocsr(),b_ub=np.r_[np.concatenate(R),np.zeros(2*K)],bounds=[(0,0) if fixed else (-25,30) for fixed in frozen.ravel()]+[(0,None)]*(N+K),method='highs',options={'time_limit':55})
 report={'success':bool(result.success),'message':result.message,'minimumCoordinateJacobianDeterminant':minimum_det,'brainSha256':sha(W/'brain-trial.glb'),'sourceSha256':sha(W/'veins-source.glb'),'wallConstraints':M,'appliedToApp':False,'preserveXZ':args.preserve_xz}
 (W/'solver.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
 if not result.success:
  soft=linprog(np.r_[np.zeros(N),np.full(N,.001),np.ones(M)],A_ub=vstack([hstack([A,Z,-eye(M)])]+[hstack([c,coo_matrix((c.shape[0],M))]) for c in C[1:]]).tocsr(),b_ub=np.concatenate(R),bounds=[(0,0) if fixed else (-25,30) for fixed in frozen.ravel()]+[(0,None)]*(N+M),method='highs',options={'time_limit':55})
  if soft.success:
   slack=soft.x[2*N:];idx=np.argsort(-slack)[:40];report['maximumViolationMm']=float(slack.max());report['violations']=[[*metadata[i],float(slack[i])] for i in idx if slack[i]>1e-5]
   (W/'infeasibility.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
  raise SystemExit(1)
 g.delta=result.x[:N].reshape(g.shape);target={}
 for k,(p,f,_) in source.items():
  q=g.apply(p);lateral=lateral_map(p);q[:,0]=lateral[:,0];q[:,2]=lateral[:,2];m=trimesh.Trimesh(q,f,process=False);target[k]=(q,f,m.vertex_normals)
 save_replaced(W/'veins-trial.glb',d,b,target)
 np.savez_compressed(W/'section-map.npz',x=g.x,z=g.z,delta=g.delta,xdelta=xdelta,zdelta=zdelta,fixed=frozen)
 report['candidateSha256']=sha(W/'veins-trial.glb')
 report['minimumRequestedStemAndBoneClearanceMm']=.4
 report['minimumRequestedRetainedVeinClearanceMm']=.1
 (W/'solver.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Staged section-preserving venous fit',flush=True)

if __name__=='__main__':main()
