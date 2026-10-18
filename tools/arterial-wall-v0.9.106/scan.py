from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table
W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=True)
if (W/'degenerate-scan.json').exists():raise ValueError('Use a fresh scan output directory')
scene=Scene(A,Path(sys.argv[2]).resolve())
from fractions import Fraction as Q

def zero_exact(tri):
 if len(set(map(tuple,tri)))<3:return True
 a,b,c=[[Q(float(x))for x in p]for p in tri];u=[y-x for x,y in zip(a,b)];v=[z-x for x,z in zip(a,c)]
 return u[1]*v[2]==u[2]*v[1]and u[2]*v[0]==u[0]*v[2]and u[0]*v[1]==u[1]*v[0]
rows=[]
for n in sorted(scene.rows):
 if scene.systems[n]!='artery':continue
 v,f=scene.mesh(n);t=v[f].astype(float);cr=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);ids=np.flatnonzero(np.all(cr==0,axis=1));ids=[int(i)for i in ids if zero_exact(t[i])]
 if not ids:continue
 u,e,c,b,d,_=edge_table(v,f);keep=np.ones(len(f),bool);keep[ids]=False;uu,ee,cc,bb,dd,_=edge_table(v,f[keep])
 def keyed(u,e,mask):return {tuple(map(tuple,u[x]))for x in e[mask]}
 boundary=keyed(u,e,c==1);postboundary=keyed(uu,ee,cc==1);bad=keyed(u,e,(c>2)|((c==2)&(b!=0)));postbad=keyed(uu,ee,(cc>2)|((cc==2)&(bb!=0)))
 row={'node':n,'zeroAreaFaceIds':ids,'boundaryBefore':len(boundary),'boundaryAfter':len(postboundary),'newBoundaryEdges':len(postboundary-boundary),'badBefore':len(bad),'badAfter':len(postbad),'newBadEdges':len(postbad-bad),'eligible':not(postboundary-boundary)and not(postbad-bad)};rows.append(row);print(n,len(ids),'zero-area','BOUND',len(boundary),len(postboundary),'BAD',len(bad),len(postbad),'eligible',row['eligible'],flush=True)
(W/'degenerate-scan.json').write_text(json.dumps({'release':'0.9.106','sourceAssets':scene.source_hashes,'rows':rows},indent=2)+'\n')
