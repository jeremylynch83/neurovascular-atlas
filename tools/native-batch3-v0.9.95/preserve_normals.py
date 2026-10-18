"""Preserve exact retained corner normals and normal seams after retopology."""
from pathlib import Path
import sys,json,numpy as np
W=Path(sys.argv[1]);choice=sys.argv[2];D=W/'decoded';O=W/'candidate';O.mkdir(exist_ok=True)
N=['Occipital left','Occipital mastoid left','ILT posterior branch left'];C={};S={}
def load(d,n):return np.fromfile(d/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(d/(n+'.indices.bin'),'<u4').reshape(-1,3)
for n in N:C[n]=load(W/('occipital/union'if n.startswith('Occipital')else choice),n)
for n in N+['ILT anterior branch left','Inferolateral trunk left','ILT posteromedial ramus left']:
 v,f=load(D,n);norm=np.fromfile(D/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4);S[n]=(v,f,norm)
v=np.vstack([p for p,g in C.values()]);g=[];off=0
for p,f in C.values():g.append(f+off);off+=len(p)
f=np.vstack(g);u,inv=np.unique(v,axis=0,return_inverse=True);t=v[f].astype(float);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);acc=np.zeros((len(u),3))
for k in range(3):np.add.at(acc,inv[f[:,k]],cross)
l=np.linalg.norm(acc,axis=1);assert np.all(l>0);acc/=l[:,None];computed={tuple(x):np.r_[np.rint(z*32767).clip(-32767,32767).astype('<i2'),0].astype('<i2')for x,z in zip(u,acc)}
# Existing external labels are exact normal authorities at their fixed ports.
external={}
for n in ['ILT anterior branch left','Inferolateral trunk left','ILT posteromedial ramus left']:
 p,g,nn=S[n]
 for x,z in zip(p,nn):external.setdefault(tuple(x),z)
# The occipital parent supplies the old collar rim normals.
p,g,nn=S['Occipital left'];parent={tuple(x):z for x,z in zip(p,nn)};common=set(map(tuple,C[N[0]][0]))&set(map(tuple,C[N[1]][0]));external.update({x:parent.get(x,computed[x])for x in common})
report=[]
for n in N:
 p,g=C[n];v,f,nn=S[n];faces={tuple(sorted(map(tuple,v[t]))):{tuple(v[i]):nn[i]for i in t}for t in f};old={tuple(x):z for x,z in zip(v,nn)};verts=[];norms=[];tri=[];lookup={};reused=0
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
