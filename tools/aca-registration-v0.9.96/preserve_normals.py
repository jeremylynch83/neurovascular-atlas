"""Preserve exact retained source corner normals and native normal seams."""
from pathlib import Path
import sys,json,numpy as np
W=Path(sys.argv[1]);D=W/'decoded';I=W/'accepted';O=W/'candidate';O.mkdir(exist_ok=True);N=['ACA A5 right','Precuneal right','ACA falcine branch right'];C={};S={}
def load(d,n):return np.fromfile(d/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(d/(n+'.indices.bin'),'<u4').reshape(-1,3)
for n in N:C[n]=load(I,n)
for n in json.load(open(D/'normal-inputs.json')):
 p,g=load(D,n);nn=np.fromfile(D/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4);assert len(nn)==len(p);S[n]=(p,g,nn)
p=np.vstack([p for p,g in C.values()]);ff=[];off=0
for v,f in C.values():ff.append(f+off);off+=len(v)
f=np.vstack(ff);u,inv=np.unique(p,axis=0,return_inverse=True);t=p[f].astype(float);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);acc=np.zeros_like(u,dtype=float)
for k in range(3):np.add.at(acc,inv[f[:,k]],cross)
l=np.linalg.norm(acc,axis=1);assert np.all(l>0);acc/=l[:,None];computed={tuple(x):np.r_[np.rint(z*32767).clip(-32767,32767).astype('<i2'),0].astype('<i2')for x,z in zip(u,acc)};external={}
for n,(v,f,nn)in S.items():
 if n not in N:
  for x,z in zip(v,nn):external.setdefault(tuple(x),z)
report=[]
for n,(p,g)in C.items():
 v,f,nn=S[n];faces={tuple(sorted(map(tuple,v[t]))):{tuple(v[i]):nn[i]for i in t}for t in f};old={tuple(x):z for x,z in zip(v,nn)};verts=[];norms=[];tri=[];lookup={};reused=0
 for t in g:
  source=faces.get(tuple(sorted(map(tuple,p[t]))));ids=[]
  if source:reused+=1
  for i in t:
   x=tuple(p[i]);normal=source[x]if source else external.get(x,old.get(x,computed[x]));key=(x,tuple(normal));j=lookup.get(key)
   if j is None:j=len(verts);lookup[key]=j;verts.append(p[i]);norms.append(normal)
   ids.append(j)
  tri.append(ids)
 np.array(verts,dtype='<f4').tofile(O/(n+'.positions.bin'));np.array(norms,dtype='<i2').tofile(O/(n+'.normal-snorm16.bin'));np.array(tri,dtype='<u4').tofile(O/(n+'.indices.bin'));report.append({'node':n,'vertices':len(verts),'triangles':len(g),'retainedSourceTrianglesWithExactCornerNormals':reused})
(W/'normal-provenance.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
