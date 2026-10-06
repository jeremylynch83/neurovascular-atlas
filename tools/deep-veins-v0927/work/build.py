from common import *
import manifold3d as mf
from scipy.spatial.transform import Rotation
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
spec=json.loads((OUT/'courses.json').read_text());new={r['id']:r for r in spec['structures']};old=sorted({k for r in new.values() for k in r['outflows'] if k not in new}|{'vein.anterior_communicating'});names=old+sorted(new);base=mf.Manifold.reserve_ids(len(names)+100);capbase=base+len(names);capnext=capbase

def frames(q):
 t=np.gradient(q,axis=0);t/=np.maximum(np.linalg.norm(t,axis=1)[:,None],1e-12);n=np.zeros_like(t);ref=np.eye(3)[np.argmin(abs(t[0]))];n[0]=np.cross(t[0],ref);n[0]/=np.linalg.norm(n[0])
 for i in range(1,len(q)):
  axis=np.cross(t[i-1],t[i]);ss=np.linalg.norm(axis);c=np.clip(t[i-1]@t[i],-1,1);n[i]=Rotation.from_rotvec(axis/ss*np.arctan2(ss,c)).apply(n[i-1]) if ss>1e-12 else n[i-1];n[i]-=t[i]*(n[i]@t[i]);n[i]/=np.linalg.norm(n[i])
 return t,n,np.cross(t,n)
def sweep(part,k):
 q=np.array(part['points']);radius=part['radius'];r=np.full(len(q),radius);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];r*=.42+.58*smooth(arc/max(.8,radius*3));_,n,b=frames(q);sides=24;theta=np.arange(sides)*2*np.pi/sides;v=(q[:,None,:]+r[:,None,None]*(n[:,None,:]*np.cos(theta)[None,:,None]+b[:,None,:]*np.sin(theta)[None,:,None])).reshape(-1,3);f=[]
 for i in range(len(q)-1):
  for j in range(sides):a=i*sides+j;c=i*sides+(j+1)%sides;f.extend([[a,c,a+sides],[c,c+sides,a+sides]])
 start=len(v);v=np.vstack([v,q[0],q[-1]])
 for j in range(sides):f.extend([[start,(j+1)%sides,j],[start+1,(len(q)-1)*sides+j,(len(q)-1)*sides+(j+1)%sides]])
 mm=mf.Mesh(v.astype(np.float32),np.array(f,np.uint32),run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32));s=mf.Manifold(mm)
 assert s.status()==mf.Error.NoError,(k,s.status())
 return s

def oldsolid(k):
 global capnext
 m=meshes[k];v=m.v;f=m.f;_,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);v=v[first];f=inv[f];tri=v[f];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);f=f[area>1e-10];original=len(f);directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);_,ids,count=np.unique(np.sort(directed,1),axis=0,return_index=True,return_counts=True);e=directed[ids[count==1]];G=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False)
 for label in np.unique(cc[e.ravel()]):
  edge=e[cc[e[:,0]]==label];pts=np.unique(edge);centre=v[pts].mean(0);ci=len(v);v=np.vstack([v,centre]);f=np.vstack([f,np.c_[edge[:,1],edge[:,0],np.full(len(edge),ci)]])
 mm=mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=np.array([0,original*3,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k),capnext],np.uint32),tolerance=.00001);capnext+=1;mm.merge();s=mf.Manifold(mm);assert s.status()==mf.Error.NoError,(k,s.status());return s
solids=[oldsolid(k) for k in old];print('Retained outlets',len(old),flush=True)
for k,r in new.items():
 for part in r['parts']:solids.append(sweep(part,k))
print('Union',len(solids),'solids',flush=True);s=mf.Manifold.batch_boolean(solids,mf.OpType.Add);assert s.status()==mf.Error.NoError;smesh=s.to_mesh();v=np.array(smesh.vert_properties[:,:3]);f=np.array(smesh.tri_verts);labels=np.zeros(len(f),int)
for i,id in enumerate(smesh.run_original_id):labels[smesh.run_index[i]//3:smesh.run_index[i+1]//3]=int(id)-base
tri=v[f];a=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);keep=(labels<len(names))&(a>0);f=f[keep];labels=labels[keep];nn=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
for j in range(3):np.add.at(nn,f[:,j],fn)
nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-15)
report={'release':'0.9.27','baseline':'0.9.26','newLabels':sorted(new),'changed':[],'unionStatus':str(s.status()),'manifoldBeforeRemovingArtificialSourceCaps':True,'baselineAssetSha256':__import__('hashlib').sha256((ROOT/'baseline/models/venous.glb').read_bytes()).hexdigest()}
for i,k in enumerate(names):
 ff=f[labels==i];assert len(ff)>0,('Lost label',k);used,inv=np.unique(ff,return_inverse=True);v[used].astype('<f4').tofile(OUT/(k+'.positions.bin'));inv.astype('<u4').reshape(-1,3).tofile(OUT/(k+'.indices.bin'));nn[used].astype('<f4').tofile(OUT/(k+'.normals.bin'));report['changed'].append({'node':k,'vertices':len(used),'triangles':len(ff),'new':k in new})
np.savez_compressed(OUT/'joined-skin.npz',positions=v,faces=f,labels=labels,names=names);(OUT/'revision.json').write_text(json.dumps(report,indent=2)+'\n');print('Built',len(names),'labelled skins',len(f),'triangles',flush=True)
