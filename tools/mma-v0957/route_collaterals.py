"""Regional, contact-driven collateral correction with exact native collars.

Inferior directions keep skull-base routes on the floor side of the temporal
lobe. Falcine routes move medially. Native brain/skull and all shared source
vertices are fixed. This corrects intersections; it does not certify canals.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
from scipy.ndimage import maximum_filter1d
base=WORK.parent/'work-v0956-outward/candidate'
rev=json.loads((OUT/'revision.json').read_text())
neighbours=[(n,*load(n)) for n in FILES if n.startswith('brain.') and not n.startswith(('brain.falx','brain.tentorium'))]
source_sets={n:set(map(bytes,np.ascontiguousarray(load(n)[0].astype('<f4')).view('V12').ravel())) for n in FILES}

def collision_ids(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
 return vtk_to_numpy(c.GetContactCells(0)).astype(int) if c.GetNumberOfContacts() else np.empty(0,int)

reports=[]
for path in sorted(WORK.glob('*.current-curve.npz')):
 n=path.name[:-len('.current-curve.npz')]
 if 'tentorial' in n or 'petrosquamosal' in n:continue
 x=np.load(path);par=x['param'];tt=x['tt'];q=x['q'];v,f=load(n,base) if (base/(n+'.positions.bin')).exists() else load(n)
 old,_=load(n);keys=np.ascontiguousarray(old.astype('<f4')).view('V12').ravel()
 foreign=set().union(*(s for k,s in source_sets.items() if k!=n and len(source_sets[n]&s)>4))
 pin=np.array([bytes(k) in foreign for k in keys]);anchors=par[pin]
 collar=np.ones(len(tt)) if not len(anchors) else smooth(np.min(abs(tt[:,None]-anchors[None,:]),axis=1)/2.5)
 side=-1 if n.endswith(' left') else 1
 direction=np.array([-side,0,0.]) if 'falcine' in n else np.array([0,0,-1.])
 shift=np.zeros(len(tt));history=[]
 for iteration in range(150):
  delta=np.interp(par,tt,shift)[:,None]*direction
  delta[pin]=0;w=v+delta;lo=w.min(0)-.01;hi=w.max(0)+.01;hit=[];pairs=[]
  for bn,bv,bf in neighbours:
   if np.any(bv.max(0)<lo) or np.any(bv.min(0)>hi):continue
   tri=bv[bf];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
   ids=collision_ids(w,f,bv,bf[take])
   if len(ids):hit.extend(par[f[ids]].ravel());pairs.append(dict(brain=bn,triangleContacts=len(ids)))
  history.append(dict(iteration=iteration,pairs=pairs,maximumShiftMm=float(shift.max())))
  if not hit:break
  if iteration%15==0:print(n,iteration,sum(r['triangleContacts']for r in pairs),round(shift.max(),3),flush=True)
  ids=np.unique(np.searchsorted(tt,np.clip(hit,tt[0],tt[-1])));active=np.zeros(len(tt));active[ids]=1
  # Spread the correction over a smooth 3 mm collar, without moving the anchor.
  active=maximum_filter1d(active,size=max(3,int(1./np.median(np.diff(tt)))))
  active=gaussian_filter1d(active,1.5/np.median(np.diff(tt)))
  active/=max(active.max(),1e-10)
  shift=np.minimum(shift+.2*active*collar,6.)
  shift=gaussian_filter1d(shift,.4/np.median(np.diff(tt)))
 write(n,w,f)
 for row in rev['changed']:
  if row['node']==n:row.update(field='regional-collateral-course',maxShiftMm=float(np.linalg.norm(w-old,axis=1).max()));break
 else:rev['changed'].append(dict(node=n,file=FILES[n],vertices=len(w),triangles=len(f),topologyExact=True,field='regional-collateral-course',maxShiftMm=float(np.linalg.norm(w-old,axis=1).max())))
 np.savez_compressed(WORK/(n+'.corrected-curve.npz'),q=q+shift[:,None]*direction,r=x['r'],shift=shift,tt=tt)
 row=dict(node=n,nativePinnedVertices=int(pin.sum()),maximumAdditionalShiftMm=float(shift.max()),passedNeuralContacts=not history[-1]['pairs'],finalPairs=history[-1]['pairs'],history=history)
 reports.append(row);print('FINAL',n,row['maximumAdditionalShiftMm'],row['finalPairs'],flush=True)
rev.update(release='0.9.57',status='regional-course-candidate')
(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'regional-collateral-corrections.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
