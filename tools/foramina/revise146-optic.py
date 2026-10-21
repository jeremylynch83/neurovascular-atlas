"""Locally reshape the existing upper sphenoid roots; no separate collars.
Run once against the revision145 sphenoid. Other nodes remain byte-for-byte unchanged.
"""
from pathlib import Path
import sys,json,numpy as np,trimesh
from scipy.interpolate import PchipInterpolator
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
S=json.load(open(A/'anatomy/source/foramina/revision145-optic.json'))
def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
def local(p,q):
 mid=(np.array(q['a'])+q['b'])/2;d=p-mid
 return mid,d@q['axis'],d@q['u'],d@q['v']
def active(p):
 w=np.zeros(len(p),bool)
 for q in S.values():
  mid,s,u,v=local(p,q);w|=(s>-23)&(s<7)&(u*u+v*v<100)
 return w

def refine(p,f,n):
 for it in range(7):
  raw=np.stack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]],axis=1);edges,inv=np.unique(np.sort(raw.reshape(-1,2),axis=1),axis=0,return_inverse=True);ei=inv.reshape(-1,3)
  mids=p[edges].mean(1);mark=(np.linalg.norm(p[edges[:,1]]-p[edges[:,0]],axis=1)>.60)&(active(mids)|active(p[edges[:,0]])|active(p[edges[:,1]]))
  if not mark.any():break
  ids=np.full(len(edges),-1,int);ids[mark]=np.arange(mark.sum())+len(p);p=np.vstack([p,mids[mark]]);nn=n[edges[mark]].mean(1);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20);n=np.vstack([n,nn]);m=ids[ei];flags=((m>=0)*np.array([1,2,4])).sum(1);new=[f[flags==0]]
  for flag,rot in [(1,0),(2,1),(4,2)]:
   t=np.roll(f[flags==flag],-rot,axis=1);mm=np.roll(m[flags==flag],-rot,axis=1);a,b,c=t.T;x=mm[:,0];new.extend([np.column_stack([a,x,c]),np.column_stack([x,b,c])])
  for flag,rot in [(5,0),(3,1),(6,2)]:
   t=np.roll(f[flags==flag],-rot,axis=1);mm=np.roll(m[flags==flag],-rot,axis=1);a,b,c=t.T;x=mm[:,0];z=mm[:,2];new.extend([np.column_stack([a,x,z]),np.column_stack([x,b,c]),np.column_stack([x,c,z])])
  t=f[flags==7];mm=m[flags==7];a,b,c=t.T;x,y,z=mm.T;new.extend([np.column_stack([a,x,z]),np.column_stack([x,b,y]),np.column_stack([z,y,c]),np.column_stack([x,y,z])]);f=np.vstack(new).astype(np.int32)
  print('refine',it,len(p),len(f),flush=True)
 return p,f,n

def warp(points):
 p=np.asarray(points,dtype=float).copy()
 for side,q in S.items():
  mid,s,u,v=local(p,q);r=np.hypot(u,v);sel=(s>-23)&(s<7)&(r<10)
  ss=s[sel];uu=u[sel];vv=v[sel];rr=r[sel]
  # The displacement is along the canal axis. Its axial derivative remains
  # positive, so the continuous map cannot fold or create an independent sleeve.
  proximal=smooth((ss+23)/16)
  roof_taper=1-smooth((ss+1.5)/4.5)
  floor_taper=1-smooth((ss+5)/6)
  radial=1-smooth((rr-3)/7)
  height=smooth((-vv+1.85)/3.7)
  displacement=(-5.8*height*roof_taper+2.2*(1-height)*floor_taper)*proximal*radial
  p[sel]+=displacement[:,None]*np.array(q['axis'])
  # Modest taper: maintain an oval central bore and a taller orbital mouth.
  news=ss+displacement
  su=PchipInterpolator([-23,-8,-2,2,7],[1,1.04,.96,.89,1])(news)
  sv=PchipInterpolator([-23,-8,-2,2,7],[1,1.04,1,1.08,1])(news)
  blend=1-smooth((rr-2.7)/5.3)
  p[sel]+=(uu*(su-1)*blend)[:,None]*np.array(q['u'])+(vv*(sv-1)*blend)[:,None]*np.array(q['v'])
 return p

if __name__=='__main__':
 bones=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=bones.mesh('bone.sphenoid');p,f,n=refine(p,f,n);before=p.copy();eps=1e-4;J=np.stack([(warp(p+np.eye(3)[k]*eps)-warp(p-np.eye(3)[k]*eps))/(2*eps)for k in range(3)],axis=2);n=np.linalg.solve(np.swapaxes(J,1,2),n[...,None])[...,0];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);p=warp(p);t=trimesh.Trimesh(p,f,process=False);assert t.is_watertight and t.is_winding_consistent
 bones.replace('bone.sphenoid',p,f,n);sha=bones.save();method={'release':'0.9.146','method':'Smooth local axial reshaping of existing optic roofs and floors, with modest variable oval calibre. No independent collars or tubes.','maximumVertexDisplacementMm':float(np.linalg.norm(p-before,axis=1).max()),'watertight':bool(t.is_watertight),'windingConsistent':bool(t.is_winding_consistent),'vertices':len(p),'triangles':len(f),'assetSha256':sha,'source':'revision145 craniofacial.glb; revision145-optic.json retains the registered axes','nativeEnvelope':'The local lesser-wing surface is intentionally reshaped to restore roof length. The former subtraction-only native-envelope condition is superseded in this patch.'};(A/'anatomy/source/foramina/revision146-method.json').write_text(json.dumps(method,indent=2)+'\n');print(method,flush=True)
