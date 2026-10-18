from affected_checks import *
from pathlib import Path
N='MMA petrosquamosal left';P='Middle meningeal left';r=json.load(open(D.parent/'petro-local-trials.json'))['accepted'][0];v,f=mesh(N);w,g=mesh(P);p=np.fromfile(OUT/(N+'.positions.bin'),'<f4').reshape(-1,3).astype(float);ff=np.fromfile(OUT/(N+'.indices.bin'),'<u4').reshape(-1,3);assert np.array_equal(ff,f);src=np.array(r['sourceRim']);dst=np.array(r['parentRim']);assert np.array_equal(p[src],w[dst]);u,inv=np.unique(np.vstack([p,w]),axis=0,return_inverse=True);tri=np.vstack([f,g+len(p)]);edges={}
for t in inv[tri]:
 for i in range(3):
  a,b=map(int,t[[i,(i+1)%3]]);key=tuple(sorted([a,b]));c=edges.setdefault(key,[0,0]);c[0]+=1;c[1]+=1 if a<b else -1
port=inv[src];paired=[edges[tuple(sorted([int(a),int(b)]))]for a,b in zip(port,np.roll(port,-1))];assert all(c==[2,0]for c in paired),paired
oldnormal=np.fromfile(D/(N+'.normals.bin'),'<f4').reshape(-1,3);parentnormal=np.fromfile(D/(P+'.normals.bin'),'<f4').reshape(-1,3);newnormal=normals(p,f).astype('<f4');moved=np.flatnonzero(np.any(p!=v,1));affected=np.flatnonzero(np.any(np.isin(f,moved),1));needed=np.unique(f[affected]);nn=oldnormal.copy();nn[needed]=newnormal[needed];nn[src]=parentnormal[dst]
other=[]
for rr in rims(v,f):
 if not np.array_equal(np.sort(rr),np.sort(src)):nn[rr]=oldnormal[rr];assert np.array_equal(p[rr],v[rr]);other.extend(rr.tolist())
nn.tofile(OUT/(N+'.normals.bin'));r.update(sharedNativeCoordinates=124,pairedOppositeBoundaryEdges=124,indicesExact=True,unmovedVerticesExact=int(np.sum(np.all(p==v,1))),otherNativeRimVerticesPreserved=len(other),retainedOtherPortNormalsExact=True)
# A moved coordinate cannot have been an existing labelled attachment.
for m in META:
 if m['name']in [N,P]or m['file']!='complete-circulation.glb':continue
 q,h=mesh(m['name'])
 if np.any(q.max(0)<v[moved].min(0))or np.any(q.min(0)>v[moved].max(0)):continue
 dd,_=cKDTree(q).query(v[moved]);assert not np.any(dd==0),(m['name'],'moved a shared native coordinate')
(D.parent/'accepted-corrections.json').write_text(json.dumps({'accepted':[{'node':N,'passed':True}]},indent=2)+'\n');(D.parent/'native-validation.json').write_text(json.dumps({'passed':True,'release':'0.9.90','correction':r},indent=2)+'\n')
manifest=json.load(open(APP/'public/anatomy/manifest.json'));sid=next(s['id']for s in manifest['structures']if s.get('asset',{}).get('node')==N);ds=json.load(open(D.parent/'old-dsa-surfaces.json'));recipe=ds['entries'][sid];assert not recipe['removed']and not recipe['flips']and not recipe['reverse'];caps=np.array(recipe['caps']).reshape(-1,3);extra=np.array(recipe['extra']);changedcentres=[]
for i in range(len(extra)):
 vertex=len(v)+i;native=np.unique(caps[np.any(caps==vertex,1)]);native=native[native<len(v)]
 if np.any(np.any(p[native]!=v[native],1)):
  extra[i]+=np.mean(p[native]-v[native],0);changedcentres.append(i)
recipe['extra']=extra.tolist();vertices=np.vstack([p,extra]);t=vertices[np.vstack([f,caps])];recipe['volumeMm3']=float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6);assert recipe['volumeMm3']>0;(D.parent/'updated-dsa-surfaces.json').write_text(json.dumps(ds));(D.parent/'projection-refresh.json').write_text(json.dumps({'passed':True,'node':N,'id':sid,'indicesCapsAndOrientationExact':True,'changedCapCentres':changedcentres,'volumeMm3':recipe['volumeMm3'],'rationale':'Native indices and topology are exact; translate only the affected cap centre by its native boundary mean displacement.'},indent=2)+'\n')
print(json.dumps({'passed':True,'pairedEdges':len(paired),'unmovedVertices':r['unmovedVerticesExact'],'otherPortVertices':len(other),'changedDSACapCentres':changedcentres}))
