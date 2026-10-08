from model import *
from scipy.spatial import cKDTree
import sys,time
results=[]
for side in ['right','left']:
 names=[r['node'] for r in json.loads((OUT/'revision.json').read_text())['changed'] if r['node'].endswith(side)];p=combine(names,True)
 vv,ff=arrays(p);lo=np.array([2 if side=='right' else -25,-60,55]);hi=np.array([25 if side=='right' else -1,-28,82]);p=p # Check the entire repaired cohort, including distal collars.
 v,f=arrays(p);t=v[f];c=t.mean(1);r=np.linalg.norm(t-c[:,None],axis=2).max(1);lo=t.min(1);hi=t.max(1);groups=[]
 for group in np.unique(np.floor(np.log2(np.maximum(r,.001))).astype(int)):
  ids=np.flatnonzero(np.floor(np.log2(np.maximum(r,.001))).astype(int)==group);groups.append((ids,cKDTree(c[ids]),r[ids].max()))
 pairs=[]
 for start in range(0,len(f),64):
  ids=np.arange(start,min(start+64,len(f)));ns=[[] for _ in ids]
  for gi,tree,mr in groups:
   found=tree.query_ball_point(c[ids],r[ids]+mr)
   for k,neighbors in enumerate(found):ns[k].extend(gi[neighbors].tolist())
  aa=np.repeat(ids,[len(n) for n in ns]);bb=np.concatenate(ns).astype(int);keep=aa<bb;aa=aa[keep];bb=bb[keep];keep=np.all(lo[aa]<=hi[bb]+1e-8,axis=1)&np.all(lo[bb]<=hi[aa]+1e-8,axis=1)&(np.linalg.norm(c[aa]-c[bb],axis=1)<=r[aa]+r[bb]);aa=aa[keep];bb=bb[keep];keep=~np.any(f[aa,:,None]==f[bb,None,:],axis=(1,2));aa=aa[keep];bb=bb[keep]
  for a,b in zip(aa,bb):
   if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append([int(a),int(b)])
 def keys(a):return np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()
 def facekeys(a,b):return np.ascontiguousarray(np.sort(keys(a)[b],axis=1)).view('V36').ravel()
 native=np.concatenate([facekeys(*load(n)) for n in names]);same=np.isin(facekeys(v,f),native);new=[pair for pair in pairs if not np.all(same[pair])]
 out={'retainedNativeTriangleIntersections':len(pairs)-len(new),'intersectionsInvolvingChangedTriangles':len(new),'side':side,'nonAdjacentIntersections':len(pairs),'pairs':pairs,'centres':[[c[a].tolist(),c[b].tolist()] for a,b in pairs[:40]]};results.append(out);print(side,len(pairs),out['centres'][:10],flush=True)
(OUT/'self-intersections.json').write_text(json.dumps(results,indent=2))
