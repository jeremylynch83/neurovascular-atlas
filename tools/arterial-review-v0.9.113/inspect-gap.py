from common import *
from collections import defaultdict
hist=json.load(open(A/'anatomy/source/arterial-junctions-v0.9.100/small-boundary-components.json'));r=next(x for x in hist if x['labels']==['SCA right','Wollschlaeger and Wollschlaeger artery right']and x['vertices']==8);q=np.array(r['loops'][0],dtype='<f4');keys=set(map(tuple,q));inc=defaultdict(list)
for n in scene.rows:
 if scene.systems[n]!='artery':continue
 v,f=scene.mesh(n)
 mask=np.array([tuple(p)in keys for p in v]);ids=np.flatnonzero(np.any(mask[f],axis=1))
 for i in ids:
  for j,k in [(0,1),(1,2),(2,0)]:
   x,y=v[f[i,j]],v[f[i,k]]
   if tuple(x)in keys and tuple(y)in keys:inc[tuple(sorted([tuple(x),tuple(y)]))].append({'node':n,'face':int(i),'direction':1 if tuple(x)<tuple(y)else-1,'indices':f[i].tolist()})
rows=[]
for i in range(len(q)):
 x,y=q[i],q[(i+1)%len(q)];e=tuple(sorted([tuple(x),tuple(y)]));hits=inc[e];rows.append({'edge':[x.tolist(),y.tolist()],'loopDirection':1 if tuple(x)<tuple(y)else-1,'source':hits});print(i,hits)
(W/'gap-baseline.json').write_text(json.dumps({'loop':q.tolist(),'labels':r['labels'],'spanMm':r['spanMm'],'edges':rows},indent=2)+'\n')
print('Scene',len(scene.rows),scene.stats)
