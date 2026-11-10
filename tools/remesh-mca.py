"""MCA-only smooth tube reconstruction; individual capped branches overlap at joins."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.interpolate import splprep,splev
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
A=Path(__file__).resolve().parents[1];B=A.parent/'inr-anatomy-atlas-v0.9.160';sys.path.insert(0,str(A/'tools/foramina'))
from geometry import Glb
M=json.loads((B/'anatomy/generated/complete_manifest.json').read_text());rows={s['id']:s for s in M['structures']};plan=json.loads((A/'anatomy/source/mca/courses.json').read_text());rr={r['id']:r for r in plan['routes']};surface=json.loads((B/'public/anatomy/dsa-surfaces.json').read_text());env=np.load(A/'anatomy/source/mca/skull-envelope.npz');centre=env['centre'];dirs=env['points']-centre;limits=np.linalg.norm(dirs,axis=1);dirs/=limits[:,None];tree=cKDTree(dirs);glbs={f:Glb(B/'public/anatomy'/f) for f in ['models/complete-circulation.glb','models/complete-anastomoses.glb']}
for f,g in glbs.items():g.path=A/'public/anatomy'/f
new={};radii={};original={}
for i,r in rr.items():
 s=rows[i];p,f,n=glbs[s['asset']['file']].mesh(s['asset']['node']);old=np.asarray(r['originalPoints']);old[:,1]*=-1;dist=cKDTree(old).query(p)[0];radius=float(np.clip(np.percentile(dist,45),.08,2.0));radius*=.5 if 'lenticulostriate' in i else 1.;radii[i]=radius;original[i]=(p,f)
 q=np.array(r['points']);q[:,1]*=-1
 if r['potential']:
  # Potential-link distal ends outside the MCA follow the unchanged baseline.
  for j,e in enumerate(r['connection']['endpoints']):
   if e not in rr:
    delta=old[0 if j==0 else -1]-q[0 if j==0 else -1];u=np.linspace(0,1,len(q));q+=((1-u) if j==0 else u)[:,None]*delta
 if 'mca_m1_' in i:
  delta=old[0]-q[0];u=np.r_[0,np.linalg.norm(np.diff(q,axis=0),axis=1).cumsum()];q+=np.clip(1-u/5,0,1)[:,None]*delta
 # Smooth source-derived small-course noise; approved parent course remains close.
 keep=np.r_[True,np.linalg.norm(np.diff(q,axis=0),axis=1)>1e-6];q=q[keep]
 if not r['mainFramework']:
  ends=q[[0,-1]].copy();q=gaussian_filter1d(q,sigma=max(2,len(q)/35),axis=0,mode='nearest');q[0]=ends[0];q[-1]=ends[1]
 u=np.r_[0,np.linalg.norm(np.diff(q,axis=0),axis=1).cumsum()];u/=u[-1];tck,_=splprep(q.T,u=u,s=.02 if r['mainFramework'] else 2.,k=min(3,len(q)-1));count=max(35,int(np.linalg.norm(np.diff(q,axis=0),axis=1).sum()/.35));q=np.array(splev(np.linspace(0,1,count),tck)).T
 delta=q-centre;d=np.linalg.norm(delta,axis=1);cap=np.min(limits[tree.query(delta/d[:,None],k=3)[1]],axis=1)-radius-1.;q=centre+delta*np.minimum(1,cap/d)[:,None]
 new[i]=q
# Reattach each daughter to the final parent curve, with a short smooth blend.
for _ in range(3):
 for i,r in rr.items():
  parent=r['physicalParent']
  if parent in new and not r['potential']:
   p=new[i];target=new[parent][cKDTree(new[parent]).query(p[0])[1]];u=np.r_[0,np.linalg.norm(np.diff(p,axis=0),axis=1).cumsum()];delta=target-p[0];new[i]=p+np.clip(1-u/3,0,1)[:,None]*delta
for i,r in rr.items():
 if not r['potential']:continue
 old=np.array(r['originalPoints']);old[:,1]*=-1
 for j,e in enumerate(r['connection']['endpoints']):
  if e not in new:
   k=0 if j==0 else -1;p=new[i];u=np.linspace(0,1,len(p));new[i]+=((1-u) if j==0 else u)[:,None]*(old[k]-p[k])
 for j,e in enumerate(r['connection']['endpoints']):
  if e in new:
   k=0 if j==0 else -1;p=new[i];target=new[e][cKDTree(new[e]).query(p[k])[1]];u=np.linspace(0,1,len(p));new[i]+=((1-u) if j==0 else u)[:,None]*(target-p[k])
report=[]
for i,q in new.items():
 r=rr[i];s=rows[i];radius=radii[i];n=len(q);t=np.gradient(q,axis=0);t/=np.linalg.norm(t,axis=1)[:,None];a=np.zeros_like(t);a[0]=np.cross(t[0],[0,0,1] if abs(t[0,2])<.9 else [1,0,0]);a[0]/=np.linalg.norm(a[0])
 for k in range(1,n):
  v=a[k-1]-t[k]*np.dot(a[k-1],t[k]);a[k]=v/np.linalg.norm(v)
 b=np.cross(t,a);sides=12 if radius<.3 else 20;ang=np.arange(sides)*2*np.pi/sides;profile=radius*(1-.25*np.linspace(0,1,n));p=(q[:,None,:]+profile[:,None,None]*(a[:,None,:]*np.cos(ang)[None,:,None]+b[:,None,:]*np.sin(ang)[None,:,None])).reshape(-1,3);f=[]
 for k in range(n-1):
  for j in range(sides):
   x=k*sides+j;y=k*sides+(j+1)%sides;f.extend([[x,y,y+sides],[x,y+sides,x+sides]])
 p=np.r_[p,q[:1],q[-1:]]
 for j in range(sides):f.extend([[n*sides,(j+1)%sides,j],[n*sides+1,(n-1)*sides+j,(n-1)*sides+(j+1)%sides]])
 f=np.array(f,dtype=np.uint32);vol=np.einsum('ij,ij->i',p[f[:,0]],np.cross(p[f[:,1]],p[f[:,2]])).sum()/6
 if vol<0:f=f[:,[0,2,1]];vol=-vol
 glbs[s['asset']['file']].replace(s['asset']['node'],p,f)
 if i in surface['entries']:surface['entries'][i]={'vertexCount':len(p),'extra':[],'reverse':False,'flips':[],'removed':[],'caps':[],'faces':len(f),'volumeMm3':float(vol)}
 c=s['vesselCourse'];c['radiusPolicy']='reconstruct-illustrative-tube';c['reviewStatus']='requires-anatomical-target' if c.get('missingTargets') else 'requires-anatomical-review';c['fitting']={'radiusProfile':{'method':'Illustrative circular profile from baseline wall-to-guide distances; deliberate 0.5 lenticulostriate diameter multiplier; smooth distal taper','node':i,'measuredPatientProfile':False,'tubeRadiusP05MedianP95':np.percentile(profile,[5,50,95]).tolist()},'mca161':{'brainIntersections':'accepted for approximate regional fit','source':'complete course scaffold version 3','externalConnections':'MCA ends follow revised parents; external endpoints retained'}};c['meshQuality']={'watertightScope':'individual branch exterior','parentJoinType':'overlapping exteriors'}
 if not r['potential']:s['flowCourseGuide']={'geometrySha256':'pending','points':q.tolist()}
 report.append({'id':i,'vertices':len(p),'faces':len(f),'radiusMm':radius})
for file,g in glbs.items():
 h=g.save();surface['sourceHashes'][file]=h;surface.setdefault('assetRevisions',{})[file]=h[:20];actual=Glb(A/'public/anatomy'/file)
 for s in rows.values():
  if s.get('asset',{}).get('file')!=file:continue
  if s.get('vesselCourse'):s['vesselCourse']['geometrySha256']=h
  if s['id'] in new and s.get('flowCourseGuide'):
   p,f,_=actual.mesh(s['asset']['node']);s['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
M['release']='0.9.161';(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2));(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));v=json.loads((B/'public/anatomy/vessel-courses.json').read_text());v['release']='0.9.161';v['courses']=[s['vesselCourse'] for s in M['structures'] if s.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v));(A/'docs/revision161-mca.json').write_text(json.dumps({'release':'0.9.161','method':'Smooth individual capped tubes with overlapping exterior junctions','MCAparts':70,'connectionParts':8,'changed':report,'ACAmeshChanges':0},indent=2));print('Saved smooth MCA meshes',len(new),flush=True)
