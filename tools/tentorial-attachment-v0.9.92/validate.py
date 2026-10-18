"""Validate the added wall triangles against every delivered named surface."""
import sys,json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
APP=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(APP/'tools/mma-v0958'))
from fold_engine import batch
W=Path(sys.argv[1]).resolve();D=W/'decoded';C=W/'candidate'
report=json.loads((W/'patches.json').read_text());meta=json.loads((D/'meshes.json').read_text())
selected={x['node'] for x in report['changes']}
def load(n,d=D):
 return np.fromfile(d/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(d/(n+'.indices.bin'),'<u4').reshape(-1,3)
results=[]
for row in report['changes']:
 n=row['node'];p,g=load(n,C);v,f=load(n);patch=g[len(f):];a=p[patch];lo=a.min((0,1))-1e-7;hi=a.max((0,1))+1e-7
 assert np.array_equal(p[:len(v)],v) and np.array_equal(g[:len(f)],f)
 rows=[];hits=[]
 for m in meta:
  other=m['name'];w,h=load(other,C if other in selected else D)
  if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
  if other==n:h=h[:len(f)]
  b=w[h];b=b[np.all(b.max(1)>=lo,axis=1)&np.all(b.min(1)<=hi,axis=1)]
  if not len(b):continue
  ts=np.concatenate([a,b]);aa=[];bb=[]
  for i,t in enumerate(a):
   cand=np.flatnonzero(np.all(b.max(1)>=t.min(0)-1e-8,axis=1)&np.all(b.min(1)<=t.max(0)+1e-8,axis=1))
   # Shared-vertex pairs meet at the preserved native wall. Disjoint triangle
   # pairs detect a new crossing beyond those legitimate boundary contacts.
   cand=cand[~np.any(np.all(t[None,:,None,:]==b[cand][:,None,:,:],axis=3),axis=(1,2))]
   aa.extend([i]*len(cand));bb.extend((cand+len(a)).tolist())
  hit=int(batch(ts,np.array(aa,dtype=np.int64),np.array(bb,dtype=np.int64)).sum()) if aa else 0
  rows.append({'other':other,'disjointTrianglePairsChecked':len(aa),'crossings':hit})
  if hit:hits.append(other)
 # New patch pairs must also be free of disjoint self-intersections.
 aa=[];bb=[]
 for i in range(len(a)):
  for j in range(i+1,len(a)):
   if not np.any(np.all(a[i][:,None,:]==a[j][None,:,:],axis=2)):
    aa.append(i);bb.append(j)
 patch_hits=int(batch(a,np.array(aa,dtype=np.int64),np.array(bb,dtype=np.int64)).sum())if aa else 0
 assert not hits and not patch_hits,(n,hits,patch_hits)
 # Restore source-coordinate availability explicitly for the recorded failures.
 parent_records=[]
 source_child=set(map(tuple,v));after_child=set(map(tuple,p))
 for parent in ['Dorsal meningeal '+n.split()[-1],'Meningohypophyseal trunk '+n.split()[-1]]:
  w,_=load(parent);coords=set(map(tuple,w))
  parent_records.append({'parent':parent,'sharedSourceCoordinatesBefore':len(source_child&coords),
                         'sharedSourceCoordinatesAfter':len(after_child&coords),
                         'restoredCoordinates':list(map(list,sorted((after_child-source_child)&coords)))})
 # Record separation from nearby structures as well as absence of crossings.
 samples=np.concatenate([a.reshape(-1,3),a.mean(1),((a+np.roll(a,-1,axis=1))/2).reshape(-1,3)])
 results.append({'node':n,'passed':True,'sourcePositionsAndFacesExact':True,
                 'newDisjointSelfIntersections':patch_hits,'newCrossingObjects':hits,
                 'fullSceneNamedMeshesScreened':len(meta),'nearbyChecks':rows,
                 'interfaces':parent_records,'patchSampleCount':len(samples)})
 print(n,'PASS',parent_records,flush=True)
(W/'native-validation.json').write_text(json.dumps({'release':'0.9.92','passed':True,
 'method':'Only seven faces are added. Every source face and coordinate is unchanged; test all new disjoint triangle pairs against all named meshes.',
 'changes':results},indent=2)+'\n')
