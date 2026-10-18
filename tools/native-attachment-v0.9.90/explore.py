import json,sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
D=Path(sys.argv[1]).resolve()/'decoded'
def load(n):
 return np.fromfile(D/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(D/(n+'.indices.bin'),'<u4').reshape(-1,3)
def rims(v,f):
 ed=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1);e,c=np.unique(ed,axis=0,return_counts=True);b=e[c==1]
 G=coo_matrix((np.ones(len(b)*2),(np.r_[b[:,0],b[:,1]],np.r_[b[:,1],b[:,0]])),shape=(len(v),len(v))).tocsr();_,lab=connected_components(G)
 return [np.flatnonzero(lab==k)for k in np.unique(lab[np.unique(b)])]
if __name__=='__main__':
 for side in ['left','right']:
  for child,parent in [('ACA falcine branch','ACA A5'),('MMA falcine terminal','MMA paramedian')]:
   a=child+' '+side;b=parent+' '+side;v,f=load(a);w,g=load(b);ra=rims(v,f);rb=rims(w,g)
   i,j=min(((i,j)for i in range(len(ra))for j in range(len(rb))),key=lambda ij:np.linalg.norm(v[ra[ij[0]]].mean(0)-w[rb[ij[1]]].mean(0)))
   av=v[ra[i]];bv=w[rb[j]];delta=bv.mean(0)-av.mean(0);dist,ix=cKDTree(bv).query(av+delta)
   print(a,b,'rims',len(av),len(bv),'unique',len(np.unique(av,axis=0)),len(np.unique(bv,axis=0)),'shift',delta,'mismatch p50/max',np.median(dist),dist.max(), 'mapping_unique',len(np.unique(ix)),flush=True)
   print('bounds centred',np.ptp(av,axis=0),np.ptp(bv,axis=0),flush=True)
