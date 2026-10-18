from union_candidate import *
def weld_parts(parts,tolerance=2e-5):
 names=list(parts);verts=np.vstack([parts[n][0]for n in names]);offsets=np.r_[0,np.cumsum([len(parts[n][0])for n in names])];source={tuple(x)for n in names for x in mesh(n)[0]};near=cKDTree(verts).query_pairs(tolerance);parent=np.arange(len(verts))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for a,b in near:
  i,j=root(a),root(b)
  if i==j:continue
  aa=tuple(verts[i])in source;bb=tuple(verts[j])in source
  if aa and bb and not np.array_equal(verts[i],verts[j]):continue
  if bb:i,j=j,i
  parent[j]=i
 reps=np.array([root(i)for i in range(len(verts))]);p=verts[reps];shift=float(np.linalg.norm(p-verts,axis=1).max());result={};removed={}
 for i,n in enumerate(names):
  q=p[offsets[i]:offsets[i+1]];g=parts[n][1];area=np.linalg.norm(np.cross(q[g[:,1]]-q[g[:,0]],q[g[:,2]]-q[g[:,0]]),axis=1);keep=area>1e-10;removed[n]=int(np.sum(~keep));q,g=compact(q,g[keep]);result[n]=(q,g)
 return result,{'maxWeldDisplacementMm':shift,'removedDegenerateTriangles':removed,'toleranceMm':tolerance}
