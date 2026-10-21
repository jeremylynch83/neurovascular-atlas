"""Repair shading over the reshaped local patch without changing geometry."""
from pathlib import Path
import sys,numpy as np,json
from scipy.spatial import cKDTree
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb,normals
import importlib.util
sp=importlib.util.spec_from_file_location('author',A/'tools/foramina/revise146-optic.py');author=importlib.util.module_from_spec(sp);sp.loader.exec_module(author)
g=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=g.mesh('bone.sphenoid');base=n.copy();geometric=normals(p,f);tree=cKDTree(p);ids=np.flatnonzero(author.active(p));dist,near=tree.query(p[ids],k=64,distance_upper_bound=1.1);valid=near<len(p);near=np.minimum(near,len(p)-1);weight=np.exp(-np.minimum(dist,100)**2/.4**2)*valid
n=geometric.copy()
for _ in range(4):
 nn=n[near];dot=np.sum(nn*n[ids,None,:],axis=2);w=weight*np.maximum(0,(dot-.15)/.85)**2;sm=(nn*w[:,:,None]).sum(1)/np.maximum(w.sum(1)[:,None],1e-20);sm/=np.maximum(np.linalg.norm(sm,axis=1)[:,None],1e-20);n[ids]=sm
# A normal-only change. Keep unrelated shading exactly as delivered.
n[~author.active(p)]=base[~author.active(p)];g.replace('bone.sphenoid',p,f,n);sha=g.save();(A/'anatomy/source/foramina/revision146-shading.json').write_text(json.dumps({'method':'Local bilateral spatial smoothing of geometric normals; opposing surfaces excluded. Vertex positions and topology unchanged.','vertices':len(ids),'assetSha256':sha},indent=2)+'\n');print('Local normals repaired',sha,flush=True)
