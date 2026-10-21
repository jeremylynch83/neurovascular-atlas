"""Restore the upper lesser-wing surface and use the paired native indentations.
The location is a mesh-fitted teaching reconstruction, not patient CT anatomy.
"""
from pathlib import Path
import sys,json,numpy as np,trimesh,manifold3d as m3d
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb,normals

def manifold(p,f):
 m=m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(p,np.float32),tri_verts=np.asarray(f,np.uint32)));assert m.status()==m3d.Error.NoError;return m

def cylinder(mid,axis,u,v,ru,rv,start,end):
 theta=np.arange(128)*2*np.pi/128
 vv=np.concatenate([mid+s*axis+ru*np.cos(theta)[:,None]*u+rv*np.sin(theta)[:,None]*v for s in [start,end]])
 ff=[]
 for i in range(128):
  j=(i+1)%128;ff.extend([[i,j,j+128],[i,j+128,i+128]])
 vv=np.vstack([vv,mid+start*axis,mid+end*axis])
 for i in range(128):
  j=(i+1)%128;ff.extend([[256,j,i],[257,i+128,j+128]])
 t=trimesh.Trimesh(vv,ff,process=False);t.fix_normals();return manifold(t.vertices,t.faces)

if __name__=='__main__':
 # Read the preceding release explicitly so authoring is reproducible.
 B=A.parent/'inr-anatomy-atlas-v0.9.146';g=Glb(B/'public/anatomy/models/craniofacial.glb');p,f,n=g.mesh('bone.sphenoid');bone=manifold(p,f)
 src=np.load(A/'anatomy/source/foramina/revision145-native-sources.npz');native=manifold(src['sphenoid_positions'],src['sphenoid_faces']);S=json.load(open(A/'anatomy/source/foramina/revision145-optic.json'));out={}
 for side,q in S.items():
  mid=(np.array(q['a'])+q['b'])/2;axis,u,v=[np.array(q[k])for k in ['axis','u','v']]
  # Restore all of the preceding local roof deformation, including its bore.
  crop=cylinder(mid,axis,u,v,11.0,11.0,-24.0,8.0)
  bone=(bone-crop)+(native^crop)
  # Pixel-to-surface projection of the centre of each original depression.
  off=1.15 if side=='right'else -1.15
  newmid=mid+off*u+5.0*v
  cutter=cylinder(newmid,axis,u,v,2.25,1.85,-18,15);bone=bone-cutter
  out[side]={'axis':axis.tolist(),'u':u.tolist(),'v':v.tolist(),'mid':newmid.tolist(),'radialAxesMm':[4.5,3.7],'depressionFit':'Native indentation below preceding opening; confirmed in cranial and oblique views.','sourceProjectionOffsetMm':[off,-5.0],'previousMid':mid.tolist()}
 assert bone.status()==m3d.Error.NoError
 mesh=bone.to_mesh();p=np.asarray(mesh.vert_properties[:,:3],float);f=np.asarray(mesh.tri_verts,np.int32);t=trimesh.Trimesh(p,f,process=False);assert t.is_watertight and t.is_winding_consistent
 # All other craniofacial nodes are inherited without modification.
 dest=Glb(A/'public/anatomy/models/craniofacial.glb');dest.replace('bone.sphenoid',p,f,normals(p,f));sha=dest.save()
 (A/'anatomy/source/foramina/revision147-optic.json').write_text(json.dumps(out,indent=2)+'\n');print('Saved',len(p),len(f),sha,flush=True)
