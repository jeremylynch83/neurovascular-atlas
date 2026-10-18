"""Refresh a position-only DSA recipe using exact, unchanged source index lineage."""
from common import *
m=json.load(open(A/'public/anatomy/manifest.json'));d=json.load(open(A/'public/anatomy/dsa-surfaces.json'));n=json.load(open(W/'spec.json'))['node'];sid=next(s['id']for s in m['structures']if s.get('asset',{}).get('node')==n);old=d['entries'][sid];v,f=scene.mesh(n);p=np.fromfile(W/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(W/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3);assert np.array_equal(f,g)and len(p)==len(v)
# The existing sanitised flips/removals remain bound to exactly the same source faces.
rem=set(old['removed']);flip=set(old['flips']);faces=np.array([t[::-1]if(old['reverse']!=(i in flip))else t for i,t in enumerate(g)if i not in rem]);caps=np.array(old['caps'],dtype=np.int64).reshape(-1,3);extra=np.array(old['extra'],dtype=float);count=len(p)
for k in range(len(extra)):
 rows=caps[np.any(caps==count+k,axis=1)];rim=np.unique(rows[rows<count]);assert np.array_equal(p[rim],v[rim]),'Synthetic projection caps must remain anchored to fixed source port rims'
verts=np.vstack([p,extra]);tri=np.vstack([faces,caps]);q=verts[tri];volume=float(np.einsum('ij,ij->i',q[:,0],np.cross(q[:,1],q[:,2])).sum()/6);assert volume>0
_,_,c,b,_,_=edge_table(verts,tri);assert np.all((c>=2)&(c%2==0)&(b==0));new={**old,'volumeMm3':volume};d['entries'][sid]=new
(W/'updated-dsa-surfaces.json').write_text(json.dumps(d));(W/'projection-refresh.json').write_text(json.dumps({'passed':True,'node':n,'id':sid,'allSourceFaceIndicesRetained':True,'sanitisedFlipsAndRemovalsExact':True,'capVerticesAndConnectivityExact':True,'closedAndOriented':True,'volumeMm3':volume,'otherRecipesExact':len(d['entries'])-1},indent=2)+'\n');print('Updated position-only DSA recipe',sid,volume)
