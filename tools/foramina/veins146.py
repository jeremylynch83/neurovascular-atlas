"""Small smooth lifts of posterior orbitofrontal venous courses above the roof."""
from pathlib import Path
import sys,numpy as np,json
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
centres=np.array([[-12.25,-30.25,77.95],[13.65,-30.25,77.95]])
def warp(p):
 p=np.asarray(p,float).copy()
 for c in centres:
  r=np.linalg.norm(p-c,axis=1);w=np.clip((3.5-r)/2.5,0,1);w=w*w*(3-2*w);p[:,2]+=.85*w
 return p
if __name__=='__main__':
 g=Glb(A/'public/anatomy/models/venous.glb');rec=[]
 for name in g.nodes:
  p,f,n=g.mesh(name);q=warp(p);move=np.linalg.norm(q-p,axis=1)
  if move.max()<1e-7:continue
  eps=1e-4;J=np.stack([(warp(p+np.eye(3)[k]*eps)-warp(p-np.eye(3)[k]*eps))/(2*eps)for k in range(3)],axis=2);assert np.linalg.det(J).min()>.4;n=np.linalg.solve(np.swapaxes(J,1,2),n[...,None])[...,0];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);g.replace(name,q,f,n);rec.append({'node':name,'maximumDisplacementMm':float(move.max())})
 sha=g.save();(A/'anatomy/source/foramina/revision146-venous.json').write_text(json.dumps({'method':'Smooth local superior displacement of posterior orbitofrontal venous segments to avoid impressions in the reconstructed bony roof. Shared local field preserves any nearby junction coordinates.','centres':centres.tolist(),'maximumLiftMm':.85,'changed':rec,'assetSha256':sha},indent=2)+'\n');print(rec,flush=True)
