"""Transport retained arteries through the exact additional context map.

Source arterial triangles are clipped against the IMAGE of each original
material tetrahedron. Thus the before skin preserves the delivered surface,
and both its source and target fragments share the brain coordinate map.
"""
import itertools,json
import numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap,arterial_movable,close_roundoff_holes
from reconcile_anterior_brainstem import clip
from reconcile_brainstem import sha
from refine_context_skin import save_replaced
W=APP/'.authoring/brainstem21-section'

def load(path):
 a=np.load(path);m=VolumeMap.__new__(VolumeMap);m.origin=a['origin'];m.delta=a['delta'];m.shape=np.array(m.delta.shape);return m

def main():
 old=load(APP/'.authoring/brainstem20-lower-final/volume-map.npz')
 new=load(W/'volume-map.npz')
 brain_hash=sha(W/'brain-trial.glb');field_hash=sha(W/'volume-map.npz')
 doc,data=read_glb(APP/'.authoring/brainstem19/arteries-baseline.glb');records=mesh_records(doc,data)
 maximum=float(abs(new.delta-old.delta).max())
 active=np.argwhere(abs(new.delta-old.delta)>1e-9)
 region_lo=old.origin+active.min(0)-1;region_hi=old.origin+active.max(0)+1
 region_lo[1]-=float(old.delta.max())
 def inverse(p):
  lo=p[:,1]-maximum-8;hi=p[:,1]+maximum+8
  for _ in range(32):
   q=p.copy();q[:,1]=(lo+hi)/2;less=old.apply(q)[:,1]<p[:,1];lo[less]=q[less,1];hi[~less]=q[~less,1]
  q=p.copy();q[:,1]=(lo+hi)/2;return q
 tetra_cache={}
 def tetra(i,j,k,order):
  key=(i,j,k,*order)
  if key in tetra_cache:return tetra_cache[key]
  cell=np.array([i,j,k],float);points=[cell.copy()]
  for axis in order:cell=cell.copy();cell[axis]+=1;points.append(cell.copy())
  a=np.array(points);b=old.apply(a);c=new.apply(a)
  planes=[]
  for omit in range(4):
   face=b[[x for x in range(4) if x!=omit]];normal=np.cross(face[1]-face[0],face[2]-face[0]);normal/=np.linalg.norm(normal);offset=normal@face[0]
   if normal@b[omit]-offset<0:normal=-normal;offset=-offset
   planes.append((normal,offset))
  result=(b,c,np.linalg.inv((b[1:]-b[0]).T),planes)
  tetra_cache[key]=result;return result
 source={};target={};changes=[]
 for key,r in records.items():
  if not arterial_movable(key):continue
  p=r['old'].astype(float);reference=inverse(p);moved=new.apply(reference)-p
  if np.linalg.norm(moved,axis=1).max()<1e-5:continue
  before=[];after=[];unchanged_faces=0
  for number,t in enumerate(p[r['faces']]):
   # A conservative region contains every changed field tetrahedron.
   if np.any(t.max(0)<region_lo) or np.any(t.min(0)>region_hi):
    before.append(t);after.append(t);unchanged_faces+=1;continue
   lo=np.floor(t.min(0)).astype(int);hi=np.floor(t.max(0)).astype(int)
   for i in range(lo[0],hi[0]+1):
    px=clip(clip(t,np.array([1,0,0]),i),np.array([-1,0,0]),-i-1)
    if len(px)<3:continue
    for k in range(lo[2],hi[2]+1):
     pz=clip(clip(px,np.array([0,0,1]),k),np.array([0,0,-1]),-k-1)
     if len(pz)<3:continue
     # Old field is nonnegative in this ROI and has at most 4.1 mm motion.
     low=int(np.floor(pz[:,1].min()))-1;high=int(np.floor(pz[:,1].max()+float(old.delta.max())))+1
     for j in range(low,high+1):
      for order in itertools.permutations(range(3)):
       b,c,inv,planes=tetra(i,j,k,order);poly=pz
       for normal,offset in planes:
        poly=clip(poly,normal,offset)
        if len(poly)<3:break
       if len(poly)<3:continue
       bary=(poly-b[0])@inv.T;q=c[0]+bary@(c[1:]-c[0])
       for n in range(1,len(poly)-1):
        tri=poly[[0,n,n+1]]
        if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))<1e-9:continue
        before.append(tri);after.append(q[[0,n,n+1]])
   if number and number%500==0:print('Clipped',key,number,flush=True)
  a=np.array(before).reshape(-1,3);b=np.array(after).reshape(-1,3)
  _,ids,indices=np.unique(np.round(a,6),axis=0,return_index=True,return_inverse=True);a=a[ids];b=b[ids];f=indices.reshape(-1,3)
  _,unique_faces=np.unique(np.sort(f,axis=1),axis=0,return_index=True);f=f[np.sort(unique_faces)]
  m=trimesh.Trimesh(a,f,process=False);n=trimesh.Trimesh(b,f,process=False)
  source[key]=(a,f,m.vertex_normals);target[key]=(b,f,n.vertex_normals)
  original=trimesh.Trimesh(p,r['faces'],process=False);area_error=abs(m.area/original.area-1);assert area_error<1e-5,(key,area_error)
  changes.append({'node':key,'sourceTriangles':len(r['faces']),'materialTriangles':len(f),'sourceSurfaceAreaRelativeError':float(area_error),'maximumDisplacementMm':float(np.linalg.norm(b-a,axis=1).max())})
  print('Staged artery',changes[-1],flush=True)
 save_replaced(W/'arteries-source.glb',doc,data,source);save_replaced(W/'arteries-trial.glb',doc,data,target)
 assert field_hash==sha(W/'volume-map.npz'), 'Staged field changed during transport'
 assert brain_hash==sha(W/'brain-trial.glb'), 'Staged brain changed during transport'
 (W/'arterial-transport.json').write_text(json.dumps({'brainSha256':brain_hash,'fieldSha256':field_hash,'arterialSourceSha256':sha(W/'arteries-source.glb'),'arterialTrialSha256':sha(W/'arteries-trial.glb'),'changes':changes,'appliedToApp':False},indent=2)+'\n')

if __name__=='__main__':main()
