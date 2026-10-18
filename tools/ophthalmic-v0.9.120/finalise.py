from probe import *
from collections import defaultdict,deque
O=W/'candidate';E=W/'export';E.mkdir(exist_ok=True);author=json.loads((O/'authoring.json').read_text());data={};sums=defaultdict(lambda:np.zeros(3))
for side in ['right','left']:
 for part in ['inferior_ophthalmic','superior_ophthalmic']:
  n='vein.'+part+'.'+side;v=np.fromfile(O/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(O/(n+'.indices.bin'),'<u4').reshape(-1,3);data[n]=(v,f)
  t=v[f].astype(float);norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
  for tri,nn in zip(t,norm):
   for q in tri:sums[tuple(q)]+=nn
normals={k:v/max(np.linalg.norm(v),1e-20)for k,v in sums.items()};reports=[]
for n,(v,f)in data.items():
 oldv,oldf=scene.mesh(n);oldnorm=np.fromfile(O/(n+'.source-normals.bin'),'<i2').reshape(-1,4);oldfaces=defaultdict(deque)
 for j,t in enumerate(oldv[oldf]):oldfaces[tuple(sorted(map(tuple,t)))].append(j)
 spec=next(x for x in author['results']if x['side']==n.rsplit('.',1)[1]);holes=[spec['iovHole']['rimCentre'],spec['sovHole']['rimCentre']];points=[];nn=[];faces=[];lookup={};retained=0
 for tri in f:
  coords=v[tri];pool=oldfaces.get(tuple(sorted(map(tuple,coords))));old=pool.popleft()if pool else None;oldbypos={tuple(oldv[i]):oldnorm[i]for i in oldf[old]}if old is not None else {};face=[]
  for q in coords:
   key=tuple(q);generated=normals[key];source=oldbypos.get(key)
   if source is not None:
    distance=min(np.linalg.norm(q-c)for c in holes);mix=np.clip((2.7-distance)/1.2,0,1);mix=mix*mix*(3-2*mix)
    if mix==0:normal=source;retained+=1
    else:
     normal=source[:3].astype(float)/32767*(1-mix)+generated*mix;normal/=max(np.linalg.norm(normal),1e-20);normal=np.r_[np.rint(normal*32767),0].astype('<i2')
   else:normal=np.r_[np.rint(generated*32767),0].astype('<i2')
   dedup=q.tobytes()+normal.tobytes()
   if dedup not in lookup:lookup[dedup]=len(points);points.append(q);nn.append(normal)
   face.append(lookup[dedup])
  faces.append(face)
 pp=np.array(points,dtype='<f4');gg=np.array(faces,dtype='<u4');np.array(nn,dtype='<i2').tofile(E/(n+'.normal-snorm16.bin'));pp.tofile(E/(n+'.positions.bin'));gg.tofile(E/(n+'.indices.bin'))
 reports.append({'node':n,'vertices':len(pp),'triangles':len(gg),'sourceFaceCornersWithExactNormals':retained,'positionSha256':__import__('hashlib').sha256(pp.tobytes()).hexdigest(),'indicesSha256':__import__('hashlib').sha256(gg.tobytes()).hexdigest()});print(reports[-1],flush=True)
(E/'changes.json').write_text(json.dumps(reports,indent=2))
