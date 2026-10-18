"""Small reversible shaft trials with fixed native boundaries, on current meshes.

Keep a trial only when the target improves without new contacts or folds.
No inferred canal, new drainage connection or new branch is manufactured.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'mma-v0952'))
from common import *
sys.path.insert(0,str(Path(__file__).parent/'mma-v0958'))
from fold_engine import intersections
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
APP=Path(__file__).resolve().parents[1];mf=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());cat={s.get('asset',{}).get('node'):s for s in mf['structures'] if s.get('asset')};cache={}
def mesh(n):
 if n not in cache:cache[n]=load(n)
 return cache[n]
def boundary(v,f):
 e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);e,c=np.unique(e,axis=0,return_counts=True);return np.unique(e[c==1])
def collision(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 t=w[g];g=g[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)];t=v[f];f=f[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
 return contacts(v,f,w,g) if len(f) and len(g) else 0
def obstacles(v,p):
 lo=np.minimum(v.min(0),p.min(0));hi=np.maximum(v.max(0),p.max(0));out=[]
 for n,s in cat.items():
  b=s.get('anatomy',{}).get('bounds')
  if b and (np.any(np.array(b[1])<lo) or np.any(np.array(b[0])>hi)):continue
  w,g=mesh(n)
  if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
  out.append((n,s['system'],w,g))
 return out
def assess(n,v,f,p):
 moved=np.linalg.norm(p-v,axis=1)>1e-7;new=[];increased=[];before=[];after=[];shared=np.zeros(len(v),bool)
 for other,system,w,g in obstacles(v,p):
  if other==n:continue
  if system=='vein':shared|=cKDTree(w).query(v)[0]<1e-5
  a=collision(v,f,w,g);b=collision(p,f,w,g)
  if a:before.append({'other':other,'system':system,'contacts':a})
  if b:after.append({'other':other,'system':system,'contacts':b})
  if b and not a:new.append(other)
  if b>a and system in ['bone','brain','artery']:increased.append(other)
 bnd=boundary(v,f);fixed=np.array_equal(p[bnd],v[bnd]);base=intersections(v,f);post=intersections(p,f)
 # Comparing the same face IDs isolates genuine new folds from old defects.
 folds=sorted(post-base)
 tri0=v[f];tri1=p[f];a=np.cross(tri0[:,1]-tri0[:,0],tri0[:,2]-tri0[:,0]);b=np.cross(tri1[:,1]-tri1[:,0],tri1[:,2]-tri1[:,0]);reversed_faces=np.flatnonzero((np.einsum('ij,ij->i',a,b)<=0)&(np.linalg.norm(a,axis=1)>1e-10))
 edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);l0=np.linalg.norm(v[edges[:,1]]-v[edges[:,0]],axis=1);l1=np.linalg.norm(p[edges[:,1]]-p[edges[:,0]],axis=1);ratio=l1[l0>1e-6]/l0[l0>1e-6]
 shared_exact=np.array_equal(p[shared],v[shared]);radii=[]
 for z in np.linspace(v[:,2].min()+.2,v[:,2].max()-.2,48):
  a=section(v,f,2,z);b=section(p,f,2,z)
  if len(a)<8 or len(b)<8:continue
  ra=np.median(np.linalg.norm(a[:,:2]-(a[:,:2].min(0)+a[:,:2].max(0))/2,axis=1));rb=np.median(np.linalg.norm(b[:,:2]-(b[:,:2].min(0)+b[:,:2].max(0))/2,axis=1))
  if ra>1e-5:radii.append(rb/ra)
 calibre=float(np.percentile(np.abs(np.array(radii)-1),95))
 return {'node':n,'maxShiftMm':float(np.linalg.norm(p-v,axis=1).max()),'movedVertices':int(moved.sum()),'nativeBoundaryCoordinatesExact':fixed,'nativeSharedVerticesChecked':int(shared.sum()),'nativeSharedCoordinatesExact':shared_exact,'newContactObjects':new,'increasedBoneNeuralOrArterialContactObjects':increased,'baselineContacts':before,'candidateContacts':after,'baselineSelfIntersections':len(base),'candidateSelfIntersections':len(post),'newSelfIntersectionPairs':folds,'reversedFaces':reversed_faces.tolist(),'edgeLengthRatioP01MedianP99':np.percentile(ratio,[1,50,99]).tolist(),'calibreCheck':{'method':'Matched world-Z section median radius around the XY bounding midpoint; geometric deformation diagnostic, not physiological calibre','radiusRatioP05MedianP95':np.percentile(radii,[5,50,95]).tolist(),'p95AbsoluteFractionalChange':calibre},'passed':fixed and shared_exact and not new and not increased and not folds and not len(reversed_faces) and calibre<=.05}
trials=[];accepted=[]
# A uniform translation at each axial station preserves each shaft contour.
n='vein.middle_meningeal.anterior.left';other='vein.ovale_emissary.left';v,f=mesh(n);w,g=mesh(other);weight=smooth((v[:,2]-48.7)/1.5)*smooth((56-v[:,2])/2.5)
for amplitude in [.08,.12,.18,.25,.35,.5]:
 for vector in [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0]]:
  p=(v+weight[:,None]*amplitude*np.array(vector)).astype('<f4').astype(float);c=collision(p,f,w,g);trial={'node':n,'amplitudeMm':amplitude,'direction':vector,'targetContactPairs':c};trials.append(trial)
  if c:continue
  # Check the immediately adjacent arterial corridor before the full audit.
  if any(collision(p,f,*mesh(a)) for a in ['Middle meningeal left','MMA frontal left']):continue
  check=assess(n,v,f,p);print(json.dumps(check),flush=True);trial['assessment']=check
  if check['passed']:
   write(n,p,f);check['field']={'method':'constant XY displacement in each axial section, with smooth axial taper','direction':vector,'amplitudeMm':amplitude,'zWindowMm':[48.7,50.2,53.5,56.]};accepted.append(check);break
 if accepted:break
# Petrosal shaft fitting: leave the medial free transitions and every current
# interface fixed; move only the already bone-related shaft towards its wall.
screens=json.loads((WORK/'petrosal-sections.json').read_text())
for side in ['left','right']:
 for ext in ['positions','indices','normals']:
  old=OUT/('vein.inferior_petrosal.'+side+'.'+ext+'.bin')
  if old.exists():old.unlink()
 n='vein.inferior_petrosal.'+side;v,f=mesh(n);rows=next(s['sections'] for s in screens if s['id']==n);rows=[r for r in rows if 52<=r['coordinate']<=59]
 centres=np.array([r['centre'] for r in rows]);delta=[]
 for r,c in zip(rows,centres):
  d=np.array(r['closest'])-c;d[2]=0;length=np.linalg.norm(d);delta.append(d/max(length,1e-8)*min(.8,max(0,r['minimumWallGapMm']-.4)))
 delta=gaussian_filter1d(np.array(delta),1.4,axis=0);dist,ix=cKDTree(centres).query(v,k=4);weights=1/(dist+.35)**2;field=np.sum(delta[ix]*weights[:,:,None],axis=1)/weights.sum(1)[:,None];field*=smooth((4-dist[:,0])/2)[:,None]
 bd=boundary(v,f);guard=cKDTree(v[bd]).query(v)[0];field*=smooth(guard/3.5)[:,None];field*=smooth((v[:,2]-50.5)/2.5)[:,None]*smooth((61-v[:,2])/2.5)[:,None];field[bd]=0
 # Keep existing near-bone walls fixed instead of shifting a free section into
 # an adjacent unsegmented bony margin during the local fit.
 bone_dist=np.full(len(v),np.inf)
 for b in FILES:
  if not b.startswith('bone.') or b in ['bone.mandible','bone.hyoid']:continue
  bone_dist=np.minimum(bone_dist,closest(locator(*mesh(b)),v)[1])
 field*=smooth((bone_dist-.45)/.5)[:,None]
 for scale in [1.,.5,.25]:
  p=(v+field*scale).astype('<f4').astype(float)
  check=assess(n,v,f,p);check['scale']=scale;trials.append(check);print(json.dumps(check),flush=True)
  if check['passed'] and check['maxShiftMm']>.01:write(n,p,f);accepted.append(check);break
report={'release':'0.9.85','baseline':'0.9.84','accepted':accepted,'trials':trials,'limitations':'Local geometry acceptance only. Existing bone penetrations, open native walls and absent canal targets remain explicit. No whole-atlas anatomical acceptance.'}
(WORK/'local-vein-trials.json').write_text(json.dumps(report,indent=2)+'\n')
