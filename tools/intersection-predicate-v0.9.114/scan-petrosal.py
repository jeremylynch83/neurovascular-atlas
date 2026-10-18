from common import *
rows=[]
for n in ['vein.inferior_petrosal.left','vein.inferior_petrosal.right']:
 v,f=scene.mesh(n);tree=scene.bvh(n);pairs=[];checks=0
 for i,t in enumerate(v[f].astype(float)):
  lo=t.min(0)-1e-7;hi=t.max(0)+1e-7
  for j in tree.query(lo,hi):
   if j<=i:continue
   b=v[f[j]].astype(float)
   if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
   checks+=1
   if triangle_crosses(t,b):pairs.append({'faces':[int(i),int(j)],'sharedIndices':sorted(set(map(int,f[i]))&set(map(int,f[j]))),'bounds':[np.minimum(t.min(0),b.min(0)).tolist(),np.maximum(t.max(0),b.max(0)).tolist()]})
 row={'node':n,'vertices':len(v),'faces':len(f),'trianglePairsChecked':checks,'selfCrossings':pairs};rows.append(row);print(row,flush=True)
(W/'petrosal-self-scan.json').write_text(json.dumps(rows,indent=2)+'\n')
