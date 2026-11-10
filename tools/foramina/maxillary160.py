"""Local bilateral IMA wall regularisation and ECA junction fairing, from v159."""
from pathlib import Path
import sys,json,os,numpy as np
from scipy.interpolate import CubicSpline,RBFInterpolator,UnivariateSpline
from scipy.ndimage import gaussian_filter1d,median_filter
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb,normals

def smooth(v):
 v=np.clip(v,0,1);return v*v*v*(10+v*(-15+6*v))

BASE=Path(os.environ.get('ATLAS_SOURCE_BASE',A));M=json.load(open(BASE/'anatomy/generated/complete_manifest.json'));assert M.get('release')!='0.9.160','One-shot authoring tool: supply the reviewed v159 source via ATLAS_SOURCE_BASE';rows={s['id']:s for s in M['structures']};flow=json.load(open(BASE/'public/anatomy/dsa-flow.json'));G=Glb(BASE/'public/anatomy/models/complete-circulation.glb');G.path=A/'public/anatomy/models/complete-circulation.glb';data={sid:G.mesh(s['asset']['node'])for sid,s in rows.items()if s.get('asset',{}).get('file')=='models/complete-circulation.glb'}
# Interpolate through the main wall, excluding cuts through side-port caps.
# These reviewed stations retain the broad native course and remove cap-induced
# centreline excursions. Coordinates are in the common oblique section frame.
from scipy.interpolate import PchipInterpolator
stations=np.array([-73,-72,-71,-70.3,-69,-67.1,-65.5,-63.9,-62.3,-60.7,-59.1,-57.5,-55.9,-54.3,-52.7,-51.1,-49.5,-47.9,-46.3])
centres=np.array([[1.3,30],[.3,28.2],[-.3,26.4],[-.9,25.73],[-1.9,25.9],[-2.54,26.57],[-3.315,27.88],[-4.1,28.9],[-4.55,29.45],[-3.9,29.875],[-3.055,29.92],[-1.555,29.74],[.555,29.67],[3.385,30.14],[6.67,31.415],[9.68,33.06],[11.65,34.78],[12.665,36.2],[12.9,37.48]])
grid=np.arange(-73,-46.3,.1);centre=CubicSpline(grid,gaussian_filter1d(PchipInterpolator(stations,centres)(grid),2,axis=0));profiles={side:centre for side in ['right','left']}

def field(controls,delta,outer=6):
 _,ix=np.unique(np.round(controls,5),axis=0,return_index=True);controls=controls[ix];delta=delta[ix];tree=cKDTree(controls);fit=RBFInterpolator(controls,delta,kernel='linear',degree=0,smoothing=1e-12,neighbors=None if len(controls)<1024 else 32)
 def move(p):
  p=np.asarray(p,float);d=tree.query(p)[0];w=smooth((outer-d)/outer);q=p.copy();sel=w>0
  if sel.any():q[sel]+=w[sel,None]*fit(p[sel])
  return q
 return move

from remesh160 import rebuild
targets={};writers={};cuffs=[];meshTargets={};remeshReports={};interfaceControls={}
for side,tail in [('right','right'),('left','right.left')]:
 sid='artery.eca.maxillary.'+tail;p,f,n=data[sid];q,g,ctl,dst,rec=rebuild(p,f,side,profiles[side]);print('Rebuilt',sid,rec,flush=True);meshTargets[sid]=(q,g);remeshReports[sid]=rec;interfaceControls[sid]=(ctl,dst)
 move=field(ctl,dst-ctl,outer=4);writers[sid]=move;oldMapped=p.copy();d,ix=cKDTree(ctl).query(p,distance_upper_bound=2e-5);sel=d<2e-5;oldMapped[sel]=dst[ix[sel]];targets[sid]=oldMapped
# Carry all shared branch collars, including the adjoining ECA/ST bifurcation.
for layer in range(8):
 tree=cKDTree(np.concatenate([data[sid][0]for sid in targets]));dst=np.concatenate(list(targets.values()));added={}
 for sid,(p,f,n)in data.items():
  if sid in targets:continue
  d,ix=tree.query(p,distance_upper_bound=2e-5);sel=d<2e-5
  if not sel.any():continue
  delta=dst[ix[sel]]-p[sel]
  if np.linalg.norm(delta,axis=1).max()<2e-5:continue
  move=field(p[sel],delta,outer=4);writers[sid]=move;added[sid]=move(p);cuffs.append({'id':sid,'sharedVertices':int(sel.sum()),'maximumCuffDisplacementMm':float(np.linalg.norm(delta,axis=1).max())})
 targets.update(added)
 if not added:break
if __name__=='__main__':
 out={}
 for side,tail in [('right','right'),('left','right.left')]:
  for base in ['artery.carotid.external.','artery.eca.maxillary.']:
   sid=base+tail;p,f,n=data[sid];q,g=meshTargets.get(sid,(targets.get(sid,p),f));out[sid+'_before']=p;out[sid+'_after']=q;out[sid+'_f']=f;out[sid+'_after_f']=g
 np.savez(A/'anatomy/source/foramina/revision160-preview.npz',**out);print('Changed',len(targets),'nodes');print(json.dumps(cuffs,indent=2))
