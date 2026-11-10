"""One-shot final fit: retain native side branches and fit parent collars to them."""
from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
A=Path(__file__).resolve().parents[2];B=Path(sys.argv[1]).resolve();sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={r['id']:r for r in M['structures']};original=json.load(open(B/'anatomy/generated/complete_manifest.json'));oldRows={r['id']:r for r in original['structures']};surface=json.load(open(A/'public/anatomy/dsa-surfaces.json'));oldSurface=json.load(open(B/'public/anatomy/dsa-surfaces.json'));flow=json.load(open(A/'public/anatomy/dsa-flow.json'));g=Glb(A/'public/anatomy/models/complete-circulation.glb');old=Glb(B/'public/anatomy/models/complete-circulation.glb');changed=json.load(open(A/'anatomy/source/foramina/revision160-arteries.json'));keep={f'artery.carotid.external.{tail}'for tail in ['right','right.left']}|{f'artery.eca.superficial_temporal.{tail}'for tail in ['right','right.left']}|{f'artery.eca.maxillary.{tail}'for tail in ['right','right.left']};restore={r['id']for r in changed}-keep;report=[];bound=[]
def field(p,d):
 _,ix=np.unique(np.round(p,6),axis=0,return_index=True);p=p[ix];d=d[ix];tree=cKDTree(p);fit=RBFInterpolator(p,d,kernel='linear',degree=0,smoothing=1e-12,neighbors=None)
 def move(q):
  q=np.asarray(q,float);dist=tree.query(q)[0];w=np.clip((2-dist)/2,0,1);w=w*w*(3-2*w);out=q.copy();sel=w>0
  if sel.any():out[sel]+=w[sel,None]*fit(q[sel])
  return out
 return move
for tail in ['right','right.left']:
 sid='artery.eca.maxillary.'+tail;p,f,n=g.mesh(rows[sid]['asset']['node']);tree=cKDTree(p);controls=[];dest=[]
 for child in sorted(restore):
  if rows[child]['side']!=rows[sid]['side']:continue
  cp,cf,cn=g.mesh(rows[child]['asset']['node']);op,of,on=old.mesh(oldRows[child]['asset']['node']);assert len(cp)==len(op);dist,ix=tree.query(cp,distance_upper_bound=2e-5);sel=dist<2e-5
  if not sel.any():continue
  controls.extend(p[ix[sel]]);dest.extend(op[sel]);report.append({'parent':sid,'nativeBranch':child,'sharedVertices':int(sel.sum()),'maximumCollarFitMm':float(np.linalg.norm(p[ix[sel]]-op[sel],axis=1).max())})
 controls=np.array(controls);dest=np.array(dest);zero=[]
 for parent in ['artery.carotid.external.'+tail,'artery.eca.superficial_temporal.'+tail]:
  pp,ff,nn=g.mesh(rows[parent]['asset']['node']);dist,ix=tree.query(pp,distance_upper_bound=2e-5);zero.extend(p[ix[dist<2e-5]])
 sign=1 if rows[sid]['side']=='right'else -1;axis=np.array([-.6*sign,.8,0]);native=(p@axis)>=-47.6;cut=np.abs(p@axis+47.6)<1e-4;zero.extend(p[cut]);zero=np.array(zero);control=np.r_[controls,zero];delta=np.r_[dest-controls,np.zeros_like(zero)];move=field(control,delta);q=move(p);q[native]=p[native]
 dist,ix=tree.query(controls);q[ix]=dest
 if len(zero):q[tree.query(zero)[1]]=zero
 g.replace(rows[sid]['asset']['node'],q,f)
 if surface['entries'][sid].get('extra'):surface['entries'][sid]['extra']=move(surface['entries'][sid]['extra']).tolist()
 rows[sid]['flowCourseGuide']={'geometrySha256':'pending','points':move(flow['entries'][sid]['points']).tolist()};rows[sid]['vesselCourse']['fitting']['revision160']['branchPolicy']='Native side-branch geometry retained; rebuilt parent collars fitted to the original shared rings.'
 bound.append(sid)
for sid in sorted(restore):
 p,f,n=old.mesh(oldRows[sid]['asset']['node']);g.replace(rows[sid]['asset']['node'],p,f,n);surface['entries'][sid]=json.loads(json.dumps(oldSurface['entries'][sid]));rows[sid]['vesselCourse']=json.loads(json.dumps(oldRows[sid]['vesselCourse']))
 if oldRows[sid].get('flowCourseGuide'):rows[sid]['flowCourseGuide']=json.loads(json.dumps(oldRows[sid]['flowCourseGuide']));bound.append(sid)
 else:rows[sid].pop('flowCourseGuide',None)
h=g.save();surface['sourceHashes']['models/complete-circulation.glb']=h;surface['assetRevisions']['models/complete-circulation.glb']=h[:20];actual=Glb(A/'public/anatomy/models/complete-circulation.glb')
for sid,row in rows.items():
 if row.get('asset',{}).get('file')!='models/complete-circulation.glb':continue
 if row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
 if sid in bound:
  p,f,n=actual.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[r['vesselCourse']for r in M['structures']if r.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2));(A/'docs/revision160-native-branch-collars.json').write_text(json.dumps(report,indent=2));(A/'anatomy/source/foramina/revision160-arteries.json').write_text(json.dumps([r for r in changed if r['id']in keep],indent=2));print('Restored',len(restore),'native branches; retained',len(keep),'corrected parent/junction meshes',flush=True)
