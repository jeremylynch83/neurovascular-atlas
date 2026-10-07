"""Fit the connected ACA family with a gradual smooth coordinate flow."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
OUT=ROOT.parent/'corrections-work';curves=json.loads((OUT/'curves.json').read_text());cl=locator(meshes['brain.corpus-callosum'].pd)
control=[];target=[]
for side in ['right','left']:
 for seg in ['A2','A3','A4','A5']:
  n=f'ACA {seg} {side}';q=np.array(curves[n]['points']);rad=np.array(curves[n]['radii']);near=np.array([close(cl,p)[0] for p in q]);dist=np.linalg.norm(q-near,axis=1);out=near+(q-near)/np.maximum(dist[:,None],1e-6)*(rad[:,None]+.85)
  if seg=='A2':out=q+(out-q)*smooth((q[:,2]-95)/13)[:,None]
  out=gaussian_filter1d(out,2,axis=0)
  idx=np.unique(np.r_[np.arange(0,len(q),max(1,len(q)//14)),len(q)-1]);control.extend(q[idx]);target.extend(out[idx])
control=np.array(control);target=np.array(target);delta=target-control
# Co-located controls are averaged to keep the field well conditioned at seams.
keys=np.round(control/.75).astype(int);uniq,inv=np.unique(keys,axis=0,return_inverse=True);cs=np.zeros((len(uniq),3));ds=np.zeros_like(cs);count=np.bincount(inv)
for j in range(3):np.add.at(cs[:,j],inv,control[:,j]);np.add.at(ds[:,j],inv,delta[:,j])
control=cs/count[:,None];delta=ds/count[:,None]
results=[]
for fraction in [.75,1.]:
 C=OUT/('aca-'+str(fraction));C.mkdir(exist_ok=True);selected={};pts=[];offset=0;spans={}
 tree=cKDTree(control)
 for n,m in meshes.items():
  if m.file!='complete-circulation.glb':continue
  distance=tree.query(m.v)[0];mask=distance<18
  if not mask.any():continue
  spans[n]=(offset,offset+int(mask.sum()),mask);pts.append(m.v[mask]);offset+=int(mask.sum())
 vertices=np.vstack(pts);original=vertices.copy()
 for step in range(40):
  centre=control+fraction*delta*(step/40);rb=RBFInterpolator(centre,fraction*delta/40,neighbors=18,kernel='thin_plate_spline',smoothing=1.)
  dist=cKDTree(centre).query(vertices)[0];mask=dist<18
  change=np.zeros_like(vertices);change[mask]=rb(vertices[mask])*(1-smooth((dist[mask]-4)/14))[:,None];vertices+=change
 for n,(a,b,mask) in spans.items():
  m=meshes[n];v=m.v.copy();v[mask]=vertices[a:b]
  if np.max(abs(v-m.v))<1e-7:continue
  v.astype('<f4').tofile(C/(n+'.positions.bin'));selected[n]=poly(v,m.f)
 new=[]
 for n,p in selected.items():
  bounds=np.array(p.GetBounds()).reshape(3,2).T
  for other,m in meshes.items():
   if m.file not in ['brain-context.glb','venous.glb','craniofacial.glb']:continue
   if np.any(bounds[1]<m.bounds[0]) or np.any(m.bounds[1]<bounds[0]):continue
   if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
 print('ACA TRIAL',fraction,'changed',len(selected),'new',new,flush=True)
 results.append({'fraction':fraction,'changed':list(selected),'newContacts':new,'directory':C.name})
(OUT/'aca-trials.json').write_text(json.dumps(results,indent=2)+'\n')
