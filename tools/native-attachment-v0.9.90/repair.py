import json,sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from explore import load,rims,D
APP=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(APP/'tools/mma-v0952'))
from common import poly,contacts,normals,smooth
sys.path.insert(0,str(APP/'tools/mma-v0958'))
from fold_engine import intersections
vtk=__import__('vtk');vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
OUT=D.parent/'candidate';OUT.mkdir(exist_ok=True)
META=json.load(open(D/'meshes.json'));CACHE={}
def mesh(n):
 if n not in CACHE:CACHE[n]=load(n)
 return CACHE[n]
def order(v,f,rim):
 ed=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1);e,c=np.unique(ed,axis=0,return_counts=True);b=e[c==1];b=b[np.isin(b[:,0],rim)&np.isin(b[:,1],rim)]
 # Weld duplicate source seam points when ordering the physical rim.
 uv,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);adj={}
 for a,b in inv[b]:
  if a!=b:adj.setdefault(int(a),set()).add(int(b));adj.setdefault(int(b),set()).add(int(a))
 assert all(len(x)==2 for x in adj.values()),{k:len(x)for k,x in adj.items()if len(x)!=2}
 seq=[next(iter(adj))];prev=None
 while True:
  nxt=next(x for x in adj[seq[-1]]if x!=prev)
  if nxt==seq[0]:break
  prev=seq[-1];seq.append(nxt)
 assert len(seq)==len(adj)
 return first[seq]
def cropped_contacts(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 t=w[g];gg=g[np.all(t.max(1)>=lo,1)&np.all(t.min(1)<=hi,1)]
 t=v[f];ff=f[np.all(t.max(1)>=lo,1)&np.all(t.min(1)<=hi,1)]
 return int(contacts(v,ff,w,gg))if len(ff)and len(gg)else 0
def candidate(n,parent,length):
 v,f=mesh(n);w,g=mesh(parent);rs=rims(v,f);rp=rims(w,g)
 i,j=min(((i,j)for i in range(len(rs))for j in range(len(rp))),key=lambda ij:np.linalg.norm(v[rs[ij[0]]].mean(0)-w[rp[ij[1]]].mean(0)))
 src=order(v,f,rs[i]);dst=order(w,g,rp[j]);v=v.copy();f=f.copy();original_count=len(v)
 if len(dst)==len(src)+1:
  # Split one boundary triangle at the midpoint of its longest rim edge.
  distances=np.linalg.norm(v[np.roll(src,-1)]-v[src],axis=1);k=int(distances.argmax());a,b=src[k],src[(k+1)%len(src)];ix=next(ix for ix,t in enumerate(f)if a in t and b in t);t=f[ix].copy();new=len(v);v=np.vstack([v,(v[a]+v[b])/2])
  for p in range(3):
   if {int(t[p]),int(t[(p+1)%3])}=={int(a),int(b)}:
    aa,bb,cc=t[p],t[(p+1)%3],t[(p+2)%3];f[ix]=[aa,new,cc];f=np.vstack([f,[new,bb,cc]]);break
  src=np.insert(src,k+1,new)
 assert len(src)==len(dst),(n,len(src),len(dst))
 aa=v[src];best=None
 for seq in [dst,dst[::-1]]:
  for shift in range(len(seq)):
   ix=np.roll(seq,shift);bb=w[ix];err=float(np.sum((aa-aa.mean(0)-(bb-bb.mean(0)))**2))
   if best is None or err<best[0]:best=(err,ix)
 dst=best[1];delta=w[dst]-v[src];centre=delta.mean(0)
 ed=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0);lens=np.linalg.norm(v[ed[:,0]]-v[ed[:,1]],axis=1)
 G=coo_matrix((np.r_[lens,lens],(np.r_[ed[:,0],ed[:,1]],np.r_[ed[:,1],ed[:,0]])),shape=(len(v),len(v))).tocsr();dist=dijkstra(G,indices=src,min_only=True)
 weight=1-smooth(dist/length)
 fixed=np.concatenate([r for k,r in enumerate(rs)if k!=i])
 boundary=np.unique(np.r_[src,fixed,np.flatnonzero(dist>=length)])
 known=np.zeros((len(v),3));known[src]=delta-weight[src,None]*centre
 known[fixed]=-weight[fixed,None]*centre
 # Harmonic residual avoids discontinuities from nearest-rim assignment.
 weights=1/np.maximum(lens,1e-5)
 adjacency=coo_matrix((np.r_[weights,weights],(np.r_[ed[:,0],ed[:,1]],np.r_[ed[:,1],ed[:,0]])),shape=(len(v),len(v))).tocsr()
 L=diags(np.asarray(adjacency.sum(1)).ravel())-adjacency
 free=np.setdiff1d(np.arange(len(v)),boundary)
 known[free]=spsolve(L[free][:,free],-L[free][:,boundary]@known[boundary])
 p=(v+weight[:,None]*centre+known).astype('<f4').astype(float)
 p[src]=w[dst];p[fixed]=v[fixed]
 return v,f,p,{'sourceRim':src.tolist(),'parentRim':dst.tolist(),'originalVertexCount':original_count,'transitionLengthMm':length,'rimShapeRmsMismatchMm':float(np.sqrt(best[0]/len(src))),'maxShiftMm':float(np.linalg.norm(p-v,axis=1).max()),'fixedDistalRimVertices':len(fixed),'distalRimExact':np.array_equal(p[fixed],v[fixed])}
def assess(n,parent,v,f,p,details):
 _,oldf=mesh(n);oldv,_=mesh(n);baself=intersections(oldv,oldf);postself=intersections(p,f)
 # Existing face IDs survive; the single inserted face is new.
 newfold=postself-baself
 t0=v[f];t1=p[f];a=np.cross(t0[:,1]-t0[:,0],t0[:,2]-t0[:,0]);b=np.cross(t1[:,1]-t1[:,0],t1[:,2]-t1[:,0]);reversed_=int(np.sum((np.einsum('ij,ij->i',a,b)<=0)&(np.linalg.norm(a,axis=1)>1e-10)))
 lo=np.minimum(v.min(0),p.min(0));hi=np.maximum(v.max(0),p.max(0));rows=[];new=[];increased=[]
 for m in META:
  other=m['name']
  if other==n:continue
  w,g=mesh(other)
  if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
  pre=cropped_contacts(oldv,oldf,w,g);post=cropped_contacts(p,f,w,g)
  if pre or post:rows.append({'other':other,'before':pre,'after':post,'intendedParentInterface':other==parent})
  if other!=parent:
   if post and not pre:new.append(other)
   if post>pre:increased.append(other)
 src=details['sourceRim'];dst=details['parentRim'];wv,_=mesh(parent);exact=np.array_equal(p[src],wv[dst])
 return {'node':n,'parent':parent,**details,'parentRimCoordinatesExact':exact,'baselineSelfIntersections':len(baself),'candidateSelfIntersections':len(postself),'newSelfIntersectionPairs':sorted(newfold)[:20],'reversedFaces':reversed_,'minimumTriangleAreaMm2':float(np.linalg.norm(b,axis=1).min()/2),'contacts':rows,'newContactObjectsExcludingParent':new,'increasedContactObjectsExcludingParent':increased,'passed':exact and details['distalRimExact']and not newfold and not reversed_ and not new and not increased}
if __name__=='__main__':
 report=[];accepted=[]
 for side in ['left','right']:
  for child,parent,lengths in [('ACA falcine branch','ACA A5',[10.,14.,18.,22.]),('MMA falcine terminal','MMA paramedian',[2.,4.,6.])]:
   n=child+' '+side;pn=parent+' '+side
   for length in lengths:
    v,f,p,d=candidate(n,pn,length);r=assess(n,pn,v,f,p,d);report.append(r);print(json.dumps(r),flush=True)
    if r['passed']:
     p.astype('<f4').tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(n+'.normals.bin'));accepted.append(r);break
 (D.parent/'attachment-trials.json').write_text(json.dumps({'accepted':accepted,'trials':report},indent=2)+'\n')
