from model import *
from scipy.spatial import cKDTree
import sys,time
results=[]
for side in ['regional-veins']:
 names=json.load(open(OUT/'repair.json'))['changed'];p=combine(names,True);vv,ff=arrays(p);tt=vv[ff];keep=np.all(tt.max(1)>[-22,-59,57.5],axis=1)&np.all(tt.min(1)<[23,-31,79.5],axis=1);p=poly(vv,ff[keep])
 v,f=arrays(p);t=v[f];c=t.mean(1);r=np.linalg.norm(t-c[:,None],axis=2).max(1);lo=t.min(1);hi=t.max(1);tree=cKDTree(c);pairs=[]
 for start in range(0,len(f),64):
  ids=np.arange(start,min(start+64,len(f)));ns=tree.query_ball_point(c[ids],r[ids]+r.max());aa=np.repeat(ids,[len(n) for n in ns]);bb=np.concatenate(ns);keep=aa<bb;aa=aa[keep];bb=bb[keep];keep=np.all(lo[aa]<=hi[bb]+1e-8,axis=1)&np.all(lo[bb]<=hi[aa]+1e-8,axis=1)&(np.linalg.norm(c[aa]-c[bb],axis=1)<=r[aa]+r[bb]);aa=aa[keep];bb=bb[keep];keep=~np.any(f[aa,:,None]==f[bb,None,:],axis=(1,2));aa=aa[keep];bb=bb[keep]
  for a,b in zip(aa,bb):
   if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append([int(a),int(b)])
 out={'side':side,'nonAdjacentIntersections':len(pairs),'pairs':pairs,'centres':[[c[a].tolist(),c[b].tolist()] for a,b in pairs[:40]]};results.append(out);print(side,len(pairs),out['centres'][:10],flush=True)
(OUT/'venous-self-intersections.json').write_text(json.dumps(results,indent=2))
