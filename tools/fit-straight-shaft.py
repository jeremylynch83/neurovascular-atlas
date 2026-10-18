"""Bounded connected-field trial, with explicit regression gates. Authoring only."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'mma-v0952'));from common import *
sys.path.insert(0,str(Path(__file__).parent/'mma-v0958'));from fold_engine import intersections
from scipy.interpolate import PchipInterpolator
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
APP=Path(__file__).resolve().parents[1];mf=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());cat={s['asset']['node']:s for s in mf['structures'] if s.get('asset')};cache={}
def mesh(n):
 if n not in cache:cache[n]=load(n)
 return cache[n]
def field(v,amplitude,n=None):
 x,y,z=v.T;weight=(1-smooth((abs(x-.64)-7)/11))*smooth((y+128)/8)*(1-smooth((y+111)/5))*smooth((z-70)/8)*(1-smooth((z-105)/15));
 if n=='brain.falx-cerebri':weight*=1-smooth((z-falx_edge(y)-.25)/3.)
 p=v.copy();p[:,2]-=amplitude*weight;return p.astype('<f4').astype(float)
def collision(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 t=w[g];g=g[np.all(t.max(1)>=lo,1)&np.all(t.min(1)<=hi,1)];t=v[f];f=f[np.all(t.max(1)>=lo,1)&np.all(t.min(1)<=hi,1)];return contacts(v,f,w,g) if len(f) and len(g) else 0
fv,ff=mesh('brain.falx-cerebri');ys=np.arange(-129,-105,.5);falx_edge=PchipInterpolator(ys,[section(fv,ff,1,y)[:,2].min() for y in ys],extrapolate=True)
amplitude=float(sys.argv[2]) if len(sys.argv)>2 else 2.;candidate={}
for n,s in cat.items():
 if n not in ['vein.straight','brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']:continue
 v,f=mesh(n);p=field(v,amplitude,n)
 if not np.array_equal(v,p):candidate[n]=p
rows=[];done={}
for n,p in candidate.items():
 v,f=mesh(n);tri=v[f];t=p[f];cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);post=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);flip=int(((np.einsum('ij,ij->i',cross,post)<=0)&(np.linalg.norm(cross,axis=1)>1e-10)).sum());folds=intersections(p,f)-intersections(v,f)
 row={'node':n,'system':cat[n]['system'],'maximumDisplacementMm':float(np.linalg.norm(p-v,axis=1).max()),'movedVertices':int((np.linalg.norm(p-v,axis=1)>1e-7).sum()),'reversedFaces':flip,'newSelfIntersectionPairs':sorted(folds),'contacts':[],'newContactObjects':[],'increasedNeuralBoneOrArterialContacts':[]}
 lo=np.minimum(p.min(0),v.min(0));hi=np.maximum(p.max(0),v.max(0))
 for other,s in cat.items():
  if other==n:continue
  bb=s.get('anatomy',{}).get('bounds')
  if other in candidate:bb=[np.minimum(mesh(other)[0].min(0),candidate[other].min(0)).tolist(),np.maximum(mesh(other)[0].max(0),candidate[other].max(0)).tolist()]
  if bb and (np.any(np.array(bb[1])+.01<lo) or np.any(np.array(bb[0])-.01>hi)):continue
  w,g=mesh(other);q=candidate.get(other,w)
  key=tuple(sorted([n,other]))
  if key in done:a,b=done[key]
  else:a=collision(v,f,w,g);b=collision(p,f,q,g);done[key]=(a,b)
  if a or b:row['contacts'].append({'other':other,'system':s['system'],'before':a,'after':b})
  # Dural intersections with vessels are not treated as brain parenchyma;
  # quantify them separately. No new independent contact object is accepted.
  if b and not a:row['newContactObjects'].append(other)
  if b>a and s['system'] in ['brain','bone','artery'] and not (cat[n]['system']=='brain' and s['system'] in ['artery','vein']) and not other.startswith(('brain.falx','brain.tentorium')):row['increasedNeuralBoneOrArterialContacts'].append(other)
 row['passed']=not flip and not folds and not row['newContactObjects'] and not row['increasedNeuralBoneOrArterialContacts'];rows.append(row);print(json.dumps(row),flush=True)
 # Stage only, never alter the app from this trial.
 p.astype('<f4').tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(n+'.normals.bin'))
report={'release':'0.9.86','amplitudeMm':amplitude,'field':'Pure inferior displacement, shared across the straight-sinus shaft and the three dural reflections; all sinus native boundaries fixed within compact XYZ support. Globally monotone Z field for amplitudes below 8/1.5 mm.','minimumBaseFieldJacobianDeterminant':1-amplitude*1.5/8,'geometryChanges':rows,'passed':all(r['passed'] for r in rows)};(WORK/('shaft-fit-'+str(amplitude)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
