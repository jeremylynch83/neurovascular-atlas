from repair import *
from fold_engine import batch

def affected_intersections(v,f,selected):
 _,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);u=v[first];g=inv[f];t=u[g];lo=t.min(1);hi=t.max(1);cent=t.mean(1);rad=np.linalg.norm(t-cent[:,None],axis=2).max(1);valid=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-10;tree=cKDTree(cent);pairs=set()
 for i in selected:
  if not valid[i]:continue
  near=np.asarray(tree.query_ball_point(cent[i],rad[i]+rad.max()),dtype=np.int64);near=near[(near!=i)&valid[near]];near=near[np.all(lo[i]<=hi[near]+1e-8,1)&np.all(lo[near]<=hi[i]+1e-8,1)]
  near=near[~np.any(g[i][None,:,None]==g[near][:,None,:],axis=(1,2))]
  if len(near):
   aa=np.full(len(near),i,np.int64);hit=batch(t,aa,near);pairs.update(tuple(sorted([int(i),int(j)]))for j in near[hit])
 return pairs

def local_contacts(v,f,w,g):
 if not len(f)or not len(g):return 0
 a=v[f];b=w[g];lo=np.maximum(a.min((0,1)),b.min((0,1)));hi=np.minimum(a.max((0,1)),b.max((0,1)))
 if np.any(lo>hi):return 0
 gg=g[np.all(b.max(1)>=lo,1)&np.all(b.min(1)<=hi,1)];return int(contacts(v,f,w,gg))if len(gg)else 0
