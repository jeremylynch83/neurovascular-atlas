from union_final import *
rows=[]
for n in NAMES:
 p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3);nn=np.fromfile(OUT/(n+'.normals.bin'),'<f4').reshape(-1,3);v,f=mesh(n);old=np.fromfile(D/(n+'.normals.bin'),'<f4').reshape(-1,3);faces={tuple(sorted(map(tuple,v[t]))):{tuple(v[i]):old[i]for i in t}for t in f};verts=[];norms=[];tri=[];lookup={};reused=0
 for t in g:
  source=faces.get(tuple(sorted(map(tuple,p[t]))));ids=[]
  if source:reused+=1
  for i in t:
   norm=source[tuple(p[i])]if source else nn[i];key=(*map(float,p[i]),*map(float,norm));j=lookup.get(key)
   if j is None:j=len(verts);lookup[key]=j;verts.append(p[i]);norms.append(norm)
   ids.append(j)
  tri.append(ids)
 np.array(verts,dtype='<f4').tofile(OUT/(n+'.positions.bin'));np.array(norms,dtype='<f4').tofile(OUT/(n+'.normals.bin'));np.array(tri,dtype='<u4').tofile(OUT/(n+'.indices.bin'));rows.append({'node':n,'verticesAfterPreservingSourceCornerNormals':len(verts),'retainedSourceTrianglesWithExactCornerNormals':reused})
(D.parent/'normal-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
