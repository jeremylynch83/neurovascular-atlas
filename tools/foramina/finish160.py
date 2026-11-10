"""One-shot sibling-collar reconciliation and local meningeal root fairing."""
from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
A=Path(__file__).resolve().parents[2];B=Path(sys.argv[1]).resolve();sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={s['id']:s for s in M['structures']};source=json.load(open(A/'public/anatomy/dsa-surfaces.json'));flow=json.load(open(A/'public/anatomy/dsa-flow.json'));old=Glb(B/'public/anatomy/models/complete-circulation.glb');g=Glb(A/'public/anatomy/models/complete-circulation.glb');oldData={sid:old.mesh(r['asset']['node'])for sid,r in rows.items()if r.get('asset',{}).get('file')=='models/complete-circulation.glb'};current={sid:g.mesh(rows[sid]['asset']['node'])for sid in oldData};targets={};moves={};report=[]
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def field(p,d):
 _,ii=np.unique(np.round(p,6),axis=0,return_index=True);p=p[ii];d=d[ii];tree=cKDTree(p);fit=RBFInterpolator(p,d,kernel='linear',degree=0,smoothing=1e-12,neighbors=None if len(p)<1024 else 32)
 def move(q):
  q=np.asarray(q,float);dd=tree.query(q)[0];w=smooth((2-dd)/2);r=q.copy();sel=w>0
  if sel.any():r[sel]+=w[sel,None]*fit(q[sel])
  return r
 return move
def shared(sid,except_ids=()):
 fixed=np.zeros(len(oldData[sid][0]),bool);op=oldData[sid][0]
 for other,(pp,ff,nn)in oldData.items():
  if other==sid or other in except_ids:continue
  fixed|=cKDTree(pp).query(op,distance_upper_bound=2e-5)[0]<2e-5
 return fixed
for tail in ['right','right.left']:
 for base,owner in [('artery.eca.superficial_temporal.','artery.carotid.external.'),('artery.eca.maxillary.masseteric.','artery.eca.posterior_deep_temporal.')]:
  sid=base+tail;parent=owner+tail;p,f,_=current[sid];d,ii=cKDTree(oldData[parent][0]).query(oldData[sid][0],distance_upper_bound=2e-5);sel=d<2e-5;fixed=shared(sid,(parent,))&~sel;control=np.r_[p[sel],p[fixed]];delta=np.r_[current[parent][0][ii[sel]]-p[sel],np.zeros((int(fixed.sum()),3))];move=field(control,delta);q=move(p);q[sel]=current[parent][0][ii[sel]];q[fixed]=p[fixed];targets[sid]=q;moves[sid]=move;report.append({'id':sid,'method':'Reconcile the shared sibling collar; retain the controlling parent and all other shared interfaces.','maximumMoveMm':float(np.linalg.norm(q-p,axis=1).max())})
for tail in ['right','right.left']:
 for base in ['artery.eca.maxillary.mma.','artery.eca.maxillary.accessory_meningeal.']:
  sid=base+tail;p,f,_=current[sid];fixed=shared(sid);_,ix,remap=np.unique(np.round(p,6),axis=0,return_index=True,return_inverse=True);v=p[ix].copy();faces=remap[f];edges=np.unique(np.sort(np.r_[faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]],axis=1),axis=0);ii=np.r_[edges[:,0],edges[:,1]];jj=np.r_[edges[:,1],edges[:,0]];mat=coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(len(v),len(v))).tocsr();degree=np.asarray(mat.sum(1)).ravel();mat=mat.multiply(1/np.maximum(degree,1)[:,None]).tocsr();locked=np.zeros(len(v),bool);np.logical_or.at(locked,remap,fixed)
  parent='artery.eca.maxillary.'+tail;root=cKDTree(oldData[parent][0]).query(oldData[sid][0],distance_upper_bound=2e-5)[0]<2e-5;distance=cKDTree(p[root]).query(v)[0];weight=smooth(distance/.25)*smooth((4-distance)/2);weight[locked]=0
  for _ in range(600):
   for rate in [.5,-.53]:v+=rate*weight[:,None]*(mat@v-v)
  q=v[remap];q[fixed]=p[fixed];targets[sid]=q;moves[sid]=field(p,q-p);report.append({'id':sid,'method':'Local Taubin root fairing within 4 mm; all shared interface vertices fixed.','maximumMoveMm':float(np.linalg.norm(q-p,axis=1).max())})
for sid,q in targets.items():
 p,f,_=current[sid];g.replace(rows[sid]['asset']['node'],q,f);move=moves[sid]
 if source['entries'][sid].get('extra'):source['entries'][sid]['extra']=move(source['entries'][sid]['extra']).tolist()
 rows[sid]['flowCourseGuide']={'geometrySha256':'pending','points':move(flow['entries'][sid]['points']).tolist()};rows[sid]['vesselCourse']['fitting']['revision160']['collarFinishing']=next(r for r in report if r['id']==sid)
h=g.save();source['sourceHashes']['models/complete-circulation.glb']=h;source['assetRevisions']['models/complete-circulation.glb']=h[:20];actual=Glb(A/'public/anatomy/models/complete-circulation.glb')
for sid,row in rows.items():
 if row.get('asset',{}).get('file')!='models/complete-circulation.glb':continue
 if row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
 if sid in targets:
  p,f,_=actual.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(source));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[r['vesselCourse']for r in M['structures']if r.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2));(A/'docs/revision160-collar-finishing.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
