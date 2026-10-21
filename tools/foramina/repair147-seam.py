"""Resolve a micron-scale penetration at the native Boolean patch seam.
Project the near T-junction vertex onto the opposite edge, maintaining all
triangle indices. No vessel geometry or canal wall is changed.
"""
from pathlib import Path
import sys,json,numpy as np,trimesh
from scipy.spatial import cKDTree
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
g=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=g.mesh('bone.sphenoid');tree=cKDTree(p)
coords=np.array([[16.961101531982422,-29.60982894897461,64.69618225097656],[16.906444549560547,-29.5887451171875,64.66907501220703],[17.000625610351562,-29.619586944580078,64.71306610107422],[19.71072006225586,-27.267919540405273,67.7816162109375]])
d,ids=tree.query(coords);assert d.max()<.02;ci,ai,bi,di=ids;c,a,b,apex=p[ids];edge=b-a;t=np.dot(c-a,edge)/np.dot(edge,edge);proj=a+t*edge;inward=apex-(a+np.dot(apex-a,edge)/np.dot(edge,edge)*edge);inward/=np.linalg.norm(inward);new=proj;move=np.linalg.norm(new-c);assert move<.02,(move,c,new);p[ci]=new;mesh=trimesh.Trimesh(p,f,process=False);assert mesh.is_watertight and mesh.is_winding_consistent;g.replace('bone.sphenoid',p,f,n);sha=g.save();rec={'vertex':int(ci),'original':c.tolist(),'corrected':new.tolist(),'displacementMm':float(move),'method':'Snap a near T-junction vertex onto the opposite edge; triangle connectivity unchanged.','assetSha256':sha};(A/'anatomy/source/foramina/revision147-seam.json').write_text(json.dumps(rec,indent=2)+'\n');print(rec,flush=True)
