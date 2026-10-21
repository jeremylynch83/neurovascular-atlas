"""Bilateral V4 straightening from measured native wall sections.
Only shared cuffs of connected branches follow the revised parent walls.
"""
from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.interpolate import PchipInterpolator,RBFInterpolator,CubicSpline
from scipy.spatial import cKDTree
from scipy.optimize import isotonic_regression
from scipy.sparse import coo_matrix
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'))
from geometry import Glb,normals
from tube_transport import smooth
M=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={r['id']:r for r in M['structures']};flow=json.load(open(A/'public/anatomy/dsa-flow.json'));profiles={};axes={}
sections=np.load(A/'anatomy/source/foramina/revision158-native-sections.npz')
for side in ['left','right']:
 y=sections[side+'_y'];centres=sections[side+'_centres'];shapes=sections[side+'_shapes'];centre=CubicSpline(y,centres);factor=CubicSpline(y,np.linalg.cholesky(shapes));radius=float(np.median(np.sqrt(np.linalg.eigvalsh(shapes)[8:-8,0])));start=-92.4;end=-75.5;z0=centre(start)[1];z1=centre(end)[1];t=np.clip((y-start)/2,0,1);weight=t*t*t*(10+t*(-15+6*t));t=np.clip((end-y)/2,0,1);weight*=t*t*t*(10+t*(-15+6*t));raw=centres[:,1]+weight*(z0+(z1-z0)*(y-start)/(end-start)-centres[:,1]);monotone=PchipInterpolator(y,isotonic_regression(raw,increasing=True).x);profiles[side]=(centre,factor,radius,start,end,z0,z1,monotone)
 yy=np.linspace(y[0],y[-1],400);old=centre(yy);axes[side]=(np.c_[old[:,0],yy,old[:,1]],None)
def parent_warp(p,side):
 p=np.asarray(p,float);q=p.copy();centre,factor,radius,start,end,z0,z1,monotone=profiles[side];y=p[:,1];t=np.clip((y-start)/2,0,1);w=t*t*t*(10+t*(-15+6*t));t=np.clip((end-y)/2,0,1);w*=t*t*t*(10+t*(-15+6*t));sel=w>0
 if not sel.any():return q
 yy=y[sel];c=centre(yy);L=factor(yy);off=p[sel][:,[0,2]]-c;unit=np.linalg.solve(L,off[...,None])[...,0];slope=(z1-z0)/(end-start);vx=centre(yy,1)[:,0];shape=np.tile(np.eye(2),(len(yy),1,1))+np.einsum('ni,nj->nij',np.c_[vx,monotone(yy,1)],np.c_[vx,monotone(yy,1)]);targetFactor=np.linalg.cholesky(shape)*radius;new=np.c_[c[:,0],z0+slope*(yy-start)]+np.einsum('nij,nj->ni',targetFactor,unit);xz=p[sel][:,[0,2]];out=xz+w[sel,None]*(new-xz);raw=c[:,1]+w[sel]*(z0+slope*(yy-start)-c[:,1]);out[:,1]+=monotone(yy)-raw;q[sel,0]=out[:,0];q[sel,2]=out[:,1];return q
for side in ['left','right']:
 before=axes[side][0];axes[side]=(before,parent_warp(before,side))
G=Glb(A/'public/anatomy/models/complete-circulation.glb');data={sid:G.mesh(row['asset']['node'])for sid,row in rows.items()if row.get('asset',{}).get('file')=='models/complete-circulation.glb'}
targets={sid:parent_warp(data[sid][0],rows[sid]['side'])for sid in data if sid.startswith('artery.posterior.vertebral_')and sid.endswith('.segment.v4')};fields={};cuffs=[];fairing={}
# Fair the two short transitions without moving any shared interface vertex.
uniqueInfo={sid:np.unique(np.round(v[0],5),axis=0,return_inverse=True)for sid,v in data.items()};allp=np.concatenate([v[0]for v in uniqueInfo.values()]);_,allkeys,counts=np.unique(allp,axis=0,return_inverse=True,return_counts=True);offset=0;shared={}
for sid,(points,remap)in uniqueInfo.items():shared[sid]=(counts[allkeys[offset:offset+len(points)]]>1)[remap];offset+=len(points)
for sid,q in list(targets.items()):
 p,f,n=data[sid];_,ix,remap=np.unique(np.round(p,5),axis=0,return_index=True,return_inverse=True);v=q[ix].copy();faces=remap[f];edges=np.r_[faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]];edges=np.unique(np.sort(edges,axis=1),axis=0);ii=np.r_[edges[:,0],edges[:,1]];jj=np.r_[edges[:,1],edges[:,0]];mat=coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(len(v),len(v))).tocsr();degree=np.asarray(mat.sum(1)).ravel();mat=mat.multiply(1/np.maximum(degree,1)[:,None]).tocsr();fixed=np.zeros(len(v),bool);np.logical_or.at(fixed,remap,shared[sid]);yy=p[ix,1];weight=np.maximum(np.exp(-((yy+91.6)/1.6)**2),np.exp(-((yy+76.1)/1.6)**2));weight[fixed]=0
 for _ in range(120):
  for factor in [.5,-.53]:v+=factor*weight[:,None]*(mat@v-v)
 smoothed=v[remap];fairing[sid]={'method':'Local Taubin fairing at the two transition bands; shared interfaces fixed.','iterations':120,'maximumVertexChangeMm':float(np.linalg.norm(smoothed-q,axis=1).max())};targets[sid]=smoothed;print('Transition fairing',sid,fairing[sid]['maximumVertexChangeMm'],flush=True)

def make_field(controls,delta):
 _,idx=np.unique(np.round(controls,5),axis=0,return_index=True);controls=controls[idx];delta=delta[idx];tree=cKDTree(controls);fit=RBFInterpolator(controls,delta,kernel='linear',degree=0,smoothing=1e-12,neighbors=None if len(controls)<=1024 else 32);outer=max(8,1.8*np.linalg.norm(delta,axis=1).max())
 def move(p):
  p=np.asarray(p,float);d=tree.query(p)[0];w=smooth((outer-d)/outer);q=p.copy();sel=w>0
  if sel.any():q[sel]+=w[sel,None]*fit(p[sel])
  return q
 return move
for level in range(8):
 print('Checking cuff layer',level+1,flush=True)
 source=np.concatenate([data[sid][0]for sid in targets]);target=np.concatenate(list(targets.values()));tree=cKDTree(source);added={}
 for sid,(p,f,n)in data.items():
  if sid in targets:continue
  d,ix=tree.query(p,distance_upper_bound=2e-5);sel=d<2e-5
  if not sel.any():continue
  delta=target[ix[sel]]-p[sel]
  if np.linalg.norm(delta,axis=1).max()<2e-5:continue
  print('Fitting cuff',sid,'controls',int(sel.sum()),flush=True);field=make_field(p[sel],delta);fields[sid]=field;added[sid]=field(p);cuffs.append({'id':sid,'sharedVertices':int(sel.sum()),'maximumCuffDisplacementMm':float(np.linalg.norm(delta,axis=1).max())})
 targets.update(added)
 if not added:break
 print('Cuff layer',level+1,len(added),flush=True)
def warp(p,sid):
 return parent_warp(p,rows[sid]['side'])if sid in targets and sid not in fields else fields[sid](p)if sid in fields else np.asarray(p,float).copy()
if __name__=='__main__':
 out={}
 for side in ['left','right']:
  for sid in [f'artery.posterior.vertebral_{side}.segment.v4',f'artery.posterior.pica_{side}.segment.p1']:
   p,f,n=data[sid];out[sid+'_before']=p;out[sid+'_after']=targets.get(sid,warp(p,sid));out[sid+'_f']=f;print(sid,'maximum move',np.linalg.norm(warp(p,sid)-p,axis=1).max(),flush=True)
  out[side+'_axis_before'],out[side+'_axis_after']=axes[side]
 np.savez(A/'anatomy/source/foramina/revision158-preview.npz',**out)
 (A/'anatomy/source/foramina/revision158-cuffs.json').write_text(json.dumps(cuffs,indent=2)+'\n')
