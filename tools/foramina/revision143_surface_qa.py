"""Independent triangle SAT screen of the edited surface and its source join."""
from pathlib import Path
import json,sys,numpy as np,trimesh,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray

def crossing(a,b,tol=.002):
 na=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);nb=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);na/=np.maximum(np.linalg.norm(na,axis=1)[:,None],1e-20);nb/=np.maximum(np.linalg.norm(nb,axis=1)[:,None],1e-20);d=np.sum((a-b[:,0,None])*nb[:,None],axis=2);e=np.sum((b-a[:,0,None])*na[:,None],axis=2);bound=np.minimum(np.maximum(0,np.minimum(d.max(1),-d.min(1))),np.maximum(0,np.minimum(e.max(1),-e.min(1))));ids=np.flatnonzero(bound>tol)
 if not len(ids):return ids,bound[ids]
 aa=a[ids];bb=b[ids];ea=np.roll(aa,-1,axis=1)-aa;eb=np.roll(bb,-1,axis=1)-bb;axes=np.concatenate([na[ids,None,:],nb[ids,None,:],np.cross(ea[:,:,None,:],eb[:,None,:,:]).reshape(-1,9,3)],axis=1);axes/=np.maximum(np.linalg.norm(axes,axis=2)[:,:,None],1e-20);ap=np.einsum('nki,nji->nkj',aa,axes);bp=np.einsum('nki,nji->nkj',bb,axes);sep=(ap.max(1)<bp.min(1)-1e-7)|(bp.max(1)<ap.min(1)-1e-7);ok=~sep.any(1);return ids[ok],bound[ids[ok]]

def check(p,fa,fb=None):
 import fcl
 selfcheck=fb is None;fb=fa if selfcheck else fb
 def obj(f):
  m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
 other=obj(fb);_,ix=np.unique(np.round(p,5),axis=0,return_inverse=True);aa=ix[fa];bb=ix[fb];hits=[];depth=[];total=0;tested=0
 for start in range(0,len(fa),1500):
  blockfaces=fa[start:start+1500];result=fcl.CollisionResult();count=fcl.collide(obj(blockfaces),other,fcl.CollisionRequest(num_max_contacts=200000,enable_contact=True),result);assert count<200000,'Contact enumeration exceeded the per-block limit';total+=count;pairs=np.array([(c.b1+start,c.b2)for c in result.contacts],dtype=int).reshape(-1,2)
  if selfcheck:pairs=pairs[pairs[:,0]<pairs[:,1]]
  pairs=pairs[~(aa[pairs[:,0],:,None]==bb[pairs[:,1],None,:]).any((1,2))];tested+=len(pairs)
  for st in range(0,len(pairs),20000):
   block=pairs[st:st+20000];ids,bound=crossing(p[fa[block[:,0]]],p[fb[block[:,1]]]);hits.extend(block[ids].tolist());depth.extend(bound.tolist())
 print('FCL total candidate contacts',total,flush=True)
 return {'candidateTrianglePairs':tested,'materialCrossings':len(hits),'maximumPlaneCrossingBoundMm':max(depth,default=0),'examples':hits[:20]}
