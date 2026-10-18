from region import *
rows=[]
for n in ['ACA A3 left','ACA A5 left','ACA A3 right','ACA A5 right']:
 v,f=scene.mesh(n);keys=set(map(tuple,v));row={'node':n,'bounds':[v.min(0).tolist(),v.max(0).tolist()],'attachments':[]}
 for other in scene.nearby(v.min(0),v.max(0)):
  if other==n:continue
  q,g=scene.mesh(other);shared=keys&set(map(tuple,q))
  if not shared:continue
  s=np.array(list(shared));row['attachments'].append({'other':other,'count':len(shared),'bounds':[s.min(0).tolist(),s.max(0).tolist()]})
 rows.append(row);print(json.dumps(row),flush=True)
(W/'attachments.json').write_text(json.dumps(rows,indent=2)+'\n')
