from model import *
from scipy.spatial import cKDTree
v,f=arrays(combine(['vein.basilar_plexus'],True));c=np.array([9.27462,-58.21493,53.55102]);t=v[f];tc=t.mean(1);sel=np.linalg.norm(tc-c,axis=1)<1.7;ff=f[sel];tri=v[ff];lo=tri.min(1);hi=tri.max(1);cross=[]
for a in range(len(ff)):
 for b in range(a+1,len(ff)):
  if np.any(ff[a,:,None]==ff[b,None,:]) or np.any(lo[a]>hi[b]) or np.any(lo[b]>hi[a]):continue
  if vtk.vtkTriangle.TrianglesIntersect(*tri[a],*tri[b]):cross.append([a,b])
print('Basilar collar intersections',len(cross));(OUT/'basilar-collar-check.json').write_text(json.dumps({'testedFaces':int(sel.sum()),'radiusMm':1.7,'nonAdjacentTriangleIntersections':len(cross),'passed':len(cross)==0},indent=2))
