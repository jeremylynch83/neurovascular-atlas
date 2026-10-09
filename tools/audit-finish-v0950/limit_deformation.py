"""Accept the largest local displacement without new self-intersections."""
from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def intersections(v,f):
 v,inv=np.unique(v,axis=0,return_inverse=True);f=inv[f];tri=v[f];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);valid=area>1e-10;lo=tri.min(1);hi=tri.max(1);c=tri.mean(1);r=np.linalg.norm(tri-c[:,None],axis=2).max(1);tree=cKDTree(c);pairs=set()
 for start in range(0,len(f),96):
  a=np.arange(start,min(start+96,len(f)));near=tree.query_ball_point(c[a],r[a]+r.max());b=np.concatenate(near);a=np.repeat(a,[len(k) for k in near]);mask=(a<b)&valid[a]&valid[b];a,b=a[mask],b[mask];mask=np.all(lo[a]<=hi[b]+1e-8,axis=1)&np.all(lo[b]<=hi[a]+1e-8,axis=1)&~np.any(f[a,:,None]==f[b,None,:],axis=(1,2));a,b=a[mask],b[mask]
  for x,y in zip(a,b):
   if vtk.vtkTriangle.TrianglesIntersect(*tri[x],*tri[y]):pairs.add((int(x),int(y)))
 return pairs
rev=json.loads((OUT/'revision.json').read_text());trials=[]
for row in rev['changed']:
 n=row['node']
 if n not in FILES:continue
 v,f=load(n);q,g=load(n,OUT);base=intersections(v,f);delta=q-v
 for alpha in [1.,.8,.6,.4,.2,.1,0.]:
  p=(v+alpha*delta).astype('<f4').astype(float);after=intersections(p,g);new=after-base;trial=dict(node=n,scale=alpha,newIntersections=len(new));trials.append(trial);print(trial,flush=True)
  if not new:
   write(n,p,g);row['acceptedDisplacementScale']=alpha;row['maxShiftMm']=float(np.linalg.norm(p-v,axis=1).max());break
(OUT/'revision.json').write_text(json.dumps(rev,indent=2)+'\n');(OUT/'deformation-trials.json').write_text(json.dumps(trials,indent=2)+'\n')
