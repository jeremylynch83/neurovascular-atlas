"""Final proximal parent-wall fairing. Native ports and distal geometry stay fixed."""
from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.sparse import coo_matrix
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={r['id']:r for r in M['structures']};surface=json.load(open(A/'public/anatomy/dsa-surfaces.json'));g=Glb(A/'public/anatomy/models/complete-circulation.glb');report=[];changed=[]
for tail in ['right','right.left']:
 sid='artery.eca.maxillary.'+tail;p,f,n=g.mesh(rows[sid]['asset']['node']);edges,c=np.unique(np.sort(np.r_[f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]],axis=1),axis=0,return_counts=True);fixed=np.zeros(len(p),bool);fixed[np.unique(edges[c==1])]=True;sign=1 if tail=='right'else -1;s=p@np.array([-.6*sign,.8,0]);fixed|=s>=-47.6;ii=np.r_[edges[:,0],edges[:,1]];jj=np.r_[edges[:,1],edges[:,0]];mat=coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(len(p),len(p))).tocsr();degree=np.asarray(mat.sum(1)).ravel();mat=mat.multiply(1/np.maximum(degree,1)[:,None]).tocsr();t=np.clip((s+72.9)/1.5,0,1);w=t*t*(3-2*t);t=np.clip((-47.6-s)/1.5,0,1);w*=t*t*(3-2*t);w[fixed]=0;q=p.copy()
 for _ in range(150):
  for rate in [.5,-.53]:q+=rate*w[:,None]*(mat@q-q)
 q[fixed]=p[fixed];assert np.array_equal(q[fixed],p[fixed]);g.replace(rows[sid]['asset']['node'],q,f);rec={'id':sid,'iterations':150,'maximumMoveMm':float(np.linalg.norm(q-p,axis=1).max()),'method':'Local Taubin fairing with every native port vertex and all retained distal vertices fixed.'};report.append(rec);rows[sid]['vesselCourse']['fitting']['revision160']['surfaceFairing']=rec;changed.append(sid)
h=g.save();surface['sourceHashes']['models/complete-circulation.glb']=h;surface['assetRevisions']['models/complete-circulation.glb']=h[:20];actual=Glb(A/'public/anatomy/models/complete-circulation.glb')
for sid,row in rows.items():
 if row.get('asset',{}).get('file')!='models/complete-circulation.glb':continue
 if row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
 if sid in changed:
  p,f,_=actual.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[r['vesselCourse']for r in M['structures']if r.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2));(A/'docs/revision160-final-wall-fairing.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
