from common import *
import manifold3d as mf
from scipy.spatial.transform import Rotation
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
spec=json.loads((OUT/'courses.json').read_text());new={r['id']:r for r in spec['structures']};old=sorted({k for r in new.values() for k in r['outflows'] if k not in new}|{p[t] for r in new.values() for p in r['parts'] for t in ['receiver','startReceiver'] if p.get(t) and p[t] not in new}|{r['sourcePartition']['node'] for r in new.values() if 'sourcePartition' in r});names=old+sorted(new);base=mf.Manifold.reserve_ids(len(names)+100);capbase=base+len(names);capnext=capbase

def frames(q):
 t=np.gradient(q,axis=0);t/=np.maximum(np.linalg.norm(t,axis=1)[:,None],1e-12);n=np.zeros_like(t);ref=np.eye(3)[np.argmin(abs(t[0]))];n[0]=np.cross(t[0],ref);n[0]/=np.linalg.norm(n[0])
 for i in range(1,len(q)):
  axis=np.cross(t[i-1],t[i]);ss=np.linalg.norm(axis);c=np.clip(t[i-1]@t[i],-1,1);n[i]=Rotation.from_rotvec(axis/ss*np.arctan2(ss,c)).apply(n[i-1]) if ss>1e-12 else n[i-1];n[i]-=t[i]*(n[i]@t[i]);n[i]/=np.linalg.norm(n[i])
 return t,n,np.cross(t,n)
def sweep(part,k):
 q=np.array(part['points']);radius=part['radius'];r=np.full(len(q),radius);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];r*=1 if part.get('startReceiver') else .42+.58*smooth(arc/max(.8,radius*3));
 if part.get('freeCaudalTip'):r*=.42+.58*smooth((arc[-1]-arc)/max(.8,radius*3))
 _,n,b=frames(q);
 if part.get('flattenedTentorial'):
  target=new[k]['surfaceTarget'];normals=[]
  for pt in q:
   pp=surface(target,pt,0);pn=surface(target,pt,1)-pp;normals.append(pn)
  n=np.array(normals);t=np.gradient(q,axis=0);t/=np.maximum(np.linalg.norm(t,axis=1)[:,None],1e-12);n-=t*(n*t).sum(1)[:,None];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);b=np.cross(t,n);n*=.30
 sides=24;theta=np.arange(sides)*2*np.pi/sides;v=(q[:,None,:]+r[:,None,None]*(n[:,None,:]*np.cos(theta)[None,:,None]+b[:,None,:]*np.sin(theta)[None,:,None])).reshape(-1,3);f=[]
 for i in range(len(q)-1):
  for j in range(sides):a=i*sides+j;c=i*sides+(j+1)%sides;f.extend([[a,c,a+sides],[c,c+sides,a+sides]])
 start=len(v);v=np.vstack([v,q[0],q[-1]])
 for j in range(sides):f.extend([[start,(j+1)%sides,j],[start+1,(len(q)-1)*sides+j,(len(q)-1)*sides+(j+1)%sides]])
 mm=mf.Mesh(v.astype(np.float32),np.array(f,np.uint32),run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32));s=mf.Manifold(mm)
 assert s.status()==mf.Error.NoError,(k,s.status())
 return s

repairs=[]
def oldsolid(k):
 global capnext
 m=meshes[k];cleaner=vtk.vtkCleanPolyData();cleaner.SetInputData(m.pd);cleaner.ToleranceIsAbsoluteOn();cleaner.SetAbsoluteTolerance(.0004);cleaner.ConvertPolysToLinesOff();cleaner.Update();pd=cleaner.GetOutput();v=vtk_to_numpy(pd.GetPoints().GetData()).copy();f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
 area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1);f=f[area>1e-10];_,unique=np.unique(np.sort(f,1),axis=0,return_index=True);f=f[np.sort(unique)]
 removed=[]
 for it in range(20):
  e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);u,inv,c=np.unique(np.sort(e,1),axis=0,return_inverse=True,return_counts=True);bad=np.flatnonzero(c>2)
  if not len(bad):break
  tri=np.unique(np.flatnonzero(np.isin(inv,bad))%len(f));ar=np.linalg.norm(np.cross(v[f[tri,1]]-v[f[tri,0]],v[f[tri,2]]-v[f[tri,0]]),axis=1);j=tri[np.argmin(ar)];removed.append(float(ar.min()/2));f=np.delete(f,j,axis=0)
 # Restore consistent local triangle winding after removing microscopic nonmanifold slivers.
 for repair_iteration in range(60):
  nf=len(f);ee=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);uu,ii,cc=np.unique(np.sort(ee,1),axis=0,return_inverse=True,return_counts=True);order=np.argsort(ii);start=np.r_[0,np.cumsum(cc)];adj=[[] for _ in range(nf)]
  for edge in np.flatnonzero(cc==2):
   a,b=order[start[edge]:start[edge+1]];fa,fb=a%nf,b%nf;same=(ee[a,0]==ee[b,0]);adj[fa].append((fb,same));adj[fb].append((fa,same))
  flip=np.full(nf,-1,np.int8);conflict=None
  for seed in range(nf):
   if flip[seed]>=0:continue
   flip[seed]=0;stack=[seed]
   while stack and conflict is None:
    a=stack.pop()
    for b,same in adj[a]:
     wanted=flip[a]^int(same)
     if flip[b]<0:flip[b]=wanted;stack.append(b)
     elif flip[b]!=wanted:conflict=(a,b);break
   if conflict:break
  if conflict is None:break
  ar=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1);j=min(conflict,key=lambda j:ar[j]);removed.append(float(ar[j]/2));f=np.delete(f,j,axis=0)
 assert conflict is None,('Nonorientable receiver',k)
 mask=flip==1;f[mask]=f[mask][:,[0,2,1]]
 directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);_,ids,count=np.unique(np.sort(directed,1),axis=0,return_index=True,return_counts=True);e=directed[ids[count==1]];original=len(f)
 # Cap each directed cycle separately, including loops which meet at a pinched vertex.
 remaining=set(map(tuple,e.tolist()));loops=[]
 while remaining:
  a,b=next(iter(remaining));remaining.remove((a,b));path=[a,b]
  while path[-1]!=path[0]:
   options=[edge for edge in remaining if edge[0]==path[-1]]
   assert options,('Open boundary chain',k,path[-1])
   edge=min(options,key=lambda e: np.linalg.norm(v[e[1]]-v[path[0]]));remaining.remove(edge)
   if edge[1] in path and edge[1]!=path[0]:
    j=path.index(edge[1]);loops.append(path[j:]+[edge[1]]);path=path[:j+1]
   else:path.append(edge[1])
  loops.append(path)
 for path in loops:
  edge=np.array(list(zip(path[:-1],path[1:])));ci=len(v);v=np.vstack([v,v[np.unique(edge)].mean(0)]);f=np.vstack([f,np.c_[edge[:,1],edge[:,0],np.full(len(edge),ci)]])
 mm=mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=np.array([0,original*3,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k),capnext],np.uint32),tolerance=.00001);capnext+=1;mm.merge();solid=mf.Manifold(mm);assert solid.status()==mf.Error.NoError,(k,solid.status());repairs.append({'node':k,'weldToleranceMm':.0004,'duplicateOrDegenerateFaceCleanup':True,'removedNonmanifoldTriangleAreasMm2':removed,'artificialCapCycles':len(loops)});print('Receiver',k,'cycles',len(loops),'tiny face repairs',removed,flush=True);return solid
solids=[oldsolid(k) for k in old];print('Retained outlets',len(old),flush=True)
for k,r in new.items():
 for part in r['parts']:solids.append(sweep(part,k))
print('Union',len(solids),'solids',flush=True);s=mf.Manifold.batch_boolean(solids,mf.OpType.Add);assert s.status()==mf.Error.NoError;smesh=s.to_mesh();v=np.array(smesh.vert_properties[:,:3]);f=np.array(smesh.tri_verts);labels=np.zeros(len(f),int)
for i,id in enumerate(smesh.run_original_id):labels[smesh.run_index[i]//3:smesh.run_index[i+1]//3]=int(id)-base
# Relabel the lower existing lateral mesencephalic triangles without an overlapping tube.
for k,row in new.items():
 if 'sourcePartition' in row:
  src=row['sourcePartition'];mask=(labels==names.index(src['node']))&(v[f].mean(1)[:,2]<src['belowZ']);labels[mask]=names.index(k)
tri=v[f];a=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);keep=(labels<len(names))&(a>0);f=f[keep];labels=labels[keep]
# Retain source interface patches where closing the receiving label alone obscured a shared collar.
restored=[];parts=[p for row in new.values() for p in row['parts']];course_trees=[(cKDTree(np.array(p['points'])),p['radius']) for p in parts]
for k in old:
 m=meshes[k];tree=cKDTree(m.v);shared=[]
 for other,mm in meshes.items():
  if mm.file!=m.file or other in names:continue
  if np.any(m.bounds[1]<mm.bounds[0]-.001) or np.any(mm.bounds[1]<m.bounds[0]-.001):continue
  points=mm.v[tree.query(mm.v,distance_upper_bound=.0007)[0]<.0007]
  if len(points)>=3:shared.append(points)
 if not shared:continue
 shared=np.concatenate(shared);st=cKDTree(shared);cent=m.v[m.f].mean(1);near=st.query(cent,distance_upper_bound=1.8)[0]<1.8
 clearance=np.full(len(cent),np.inf)
 for ct,rr in course_trees:clearance=np.minimum(clearance,ct.query(cent)[0]-rr)
 near&=clearance>.22
 oldf=f[labels==names.index(k)];loc=locator(poly(v,oldf));indices=[]
 for j in np.flatnonzero(near):
  tri=m.v[m.f[j]]
  if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))<1e-10:continue
  if max(close(loc,p)[1] for p in tri)> .001:indices.append(j)
 if indices:
  offset=len(v);v=np.vstack([v,m.v]);f=np.vstack([f,m.f[indices]+offset]);labels=np.r_[labels,np.full(len(indices),names.index(k))];restored.append({'node':k,'sourceCollarTrianglesRestored':len(indices)})
nn=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
for j in range(3):np.add.at(nn,f[:,j],fn)
length=np.linalg.norm(nn,axis=1);bad=length<1e-12
if bad.any():
 best=np.zeros(len(v))
 for face,norm in zip(f,fn):
  size=np.linalg.norm(norm)
  for index in face:
   if bad[index] and size>best[index]:nn[index]=norm;best[index]=size
nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-15)
report={'release':'0.9.28','baseline':'0.9.27','newLabels':sorted(new),'changed':[],'receiverPreparation':repairs,'retainedSourceCollarPatches':restored,'unionStatus':str(s.status()),'manifoldBeforeRemovingArtificialSourceCaps':True,'baselineAssetSha256':__import__('hashlib').sha256((ROOT/'baseline/models/venous.glb').read_bytes()).hexdigest()}
for i,k in enumerate(names):
 ff=f[labels==i];assert len(ff)>0,('Lost label',k);used,inv=np.unique(ff,return_inverse=True);v[used].astype('<f4').tofile(OUT/(k+'.positions.bin'));inv.astype('<u4').reshape(-1,3).tofile(OUT/(k+'.indices.bin'));nn[used].astype('<f4').tofile(OUT/(k+'.normals.bin'));report['changed'].append({'node':k,'vertices':len(used),'triangles':len(ff),'new':k in new})
np.savez_compressed(OUT/'joined-skin.npz',positions=v,faces=f,labels=labels,names=names);(OUT/'revision.json').write_text(json.dumps(report,indent=2)+'\n');print('Built',len(names),'labelled skins',len(f),'triangles',flush=True)
