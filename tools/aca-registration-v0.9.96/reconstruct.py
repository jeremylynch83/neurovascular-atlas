"""Replay the bounded right ACA correction from shipped source buffers.

Stages meshes only. NumPy, SciPy and VTK are authoring dependencies.
"""
from pathlib import Path
import sys,json,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'repair'))
from geometry import edge_table,cycles
from collar import build_collar
W=Path(sys.argv[1]).resolve();D=W/'decoded';O=W/'replayed';O.mkdir(exist_ok=True)
def load(n):return np.fromfile(D/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(D/(n+'.indices.bin'),'<u4').reshape(-1,3)
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
def distances(v,f,seeds):
 edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);length=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);graph=coo_matrix((np.r_[length,length],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(v),len(v))).tocsr();return dijkstra(graph,indices=seeds,min_only=True)
parent='ACA A5 right';branch='Precuneal right';falcine='ACA falcine branch right';v,f=load(parent);p=v.copy();centre=np.array([-81.089037675,119.357321323]);radius=np.linalg.norm(v[:,1:]-centre,axis=1);p[:,0]+=-2.1*(1-smooth((radius-2)/10));p=p.astype('<f4');shear=W/'sheared';shear.mkdir(exist_ok=True);p.tofile(shear/(parent+'.positions.bin'));f.tofile(shear/(parent+'.indices.bin'))
# The adjacent branch has a shorter geodesic taper, constrained by the actual
# moved parent coordinates, rather than the broad spatial parent field.
w,g=load(branch);u,inv=np.unique(w,axis=0,return_inverse=True);uf=inv[g];auth={tuple(x):q for x,q in zip(v,p)};rim=np.array([i for i,x in enumerate(u)if tuple(x)in auth]);assert len(rim)==148;dd=distances(u,uf,rim);q=u.copy();q[:,0]-=2.1*(1-smooth(dd/5));q[rim]=np.array([auth[tuple(u[i])]for i in rim]);q=q[inv].astype('<f4');q.tofile(shear/(branch+'.positions.bin'));g.tofile(shear/(branch+'.indices.bin'));q.tofile(O/(branch+'.positions.bin'));g.tofile(O/(branch+'.indices.bin'))
# Remove the malformed local parent lip. Every other native boundary stays fixed.
u,inv=np.unique(p,axis=0,return_inverse=True);uf=inv[f];_,e,c,b,d,_=edge_table(u,uf);loops=cycles(d[c==1]);sourcecentre=np.array([3.75458021958669,-81.08903767512395,119.35732132349258]);target=min(loops,key=lambda x:np.linalg.norm(u[x].mean(0)-(sourcecentre-[2.1,0,0])));protected=set(np.unique(d[c==1]))-set(target);dd=distances(u,uf,target);delete=np.any(dd[uf]<.25,axis=1)&~np.any(np.isin(uf,list(protected)),axis=1);h=uf[~delete];used=np.unique(h);lookup=np.full(len(u),-1);lookup[used]=np.arange(len(used));p=u[used].astype('<f4');h=lookup[h].astype('<u4');assert int(sum(delete))==168
uu,e,c,b,d,_=edge_table(p,h);loops=cycles(d[c==1]);port=min((uu[x]for x in loops),key=lambda x:np.linalg.norm(x.mean(0)-(sourcecentre-[2.1,0,0])));assert len(port)==32
v,f=load(falcine);q,g,detail=build_collar(v,f,p,h,port.mean(0),[0,0,121.],[0,0,1],steps=18)
for n,(a,b)in {parent:(p,h),falcine:(q,g)}.items():a.tofile(O/(n+'.positions.bin'));b.tofile(O/(n+'.indices.bin'))
(O/'reconstruction.json').write_text(json.dumps({'parentShear':{'amplitudeMm':2.1,'centreYZ':centre.tolist(),'plateauMm':2,'supportMm':12},'precunealGeodesicTaperMm':5,'parentLipGeodesicSetbackMm':.25,'removedParentTriangles':int(sum(delete)),'collar':detail},indent=2)+'\n');print('Staged the three replay meshes; validation and installation are separate.')
