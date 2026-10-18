from union_candidate import *
report=json.load(open(D.parent/'manifold-union.json'));accepted=[];rows=[]
for side in ['left','right']:
 names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];parts=[(np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3))for n in names];v=np.vstack([x[0]for x in parts]);f=np.vstack([parts[0][1],parts[1][1]+len(parts[0][0])]);u,inv=np.unique(v,axis=0,return_inverse=True);t=v[f];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);acc=np.zeros_like(u)
 for k in range(3):np.add.at(acc,inv[f[:,k]],cross)
 lens=np.linalg.norm(acc,axis=1);assert np.all(lens>1e-12);acc/=lens[:,None];shared=set(map(tuple,parts[0][0]))&set(map(tuple,parts[1][0]));offset=0
 for n,(p,g)in zip(names,parts):
  ov,of=mesh(n);old=np.fromfile(D/(n+'.normals.bin'),'<f4').reshape(-1,3);oldmap={tuple(q):old[i]for i,q in enumerate(ov)};nn=acc[inv[offset:offset+len(p)]].copy();retained=0
  for i,q in enumerate(p):
   key=tuple(q)
   if key in oldmap and key not in shared:nn[i]=oldmap[key];retained+=1
  nn.astype('<f4').tofile(OUT/(n+'.normals.bin'));offset+=len(p);accepted.append({'node':n,'passed':True});rows.append({'node':n,'reusedOriginalNormals':retained,'newInterfaceNormalsShared':True})
(D.parent/'accepted-corrections.json').write_text(json.dumps({'accepted':accepted},indent=2)+'\n');(D.parent/'normal-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
