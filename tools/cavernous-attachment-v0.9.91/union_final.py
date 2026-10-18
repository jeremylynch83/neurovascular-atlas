from repair import *
sys.path.insert(0,str(D.parent/'deps'))
import manifold3d as manifold
NAMES=['MMA cavernous left','MMA posterior cavernous left']
def compact(v,f):
 used=np.unique(f);inv=np.full(len(v),-1);inv[used]=np.arange(len(used));return v[used],inv[f].astype('<u4')
def boundary(v,f):
 u,ix=np.unique(v,axis=0,return_inverse=True);e=np.sort(np.vstack([ix[f][:,[0,1]],ix[f][:,[1,2]],ix[f][:,[2,0]]]),axis=1);e,c=np.unique(e,axis=0,return_counts=True);return u,e,c
def inputs():
 recipes=json.load(open(D.parent/'screened-dsa-surfaces.json'));manifest=json.load(open(APP/'public/anatomy/manifest.json'));result=[]
 for n in NAMES:
  x=np.load(D.parent/('screened-'+n+'.npz'));v=x['v'];f=x['f'];sid=next(s['id']for s in manifest['structures']if s.get('asset',{}).get('node')==n);r=recipes['entries'][sid];assert not r['reverse']and not r['flips']and not r['removed'];vv=np.vstack([v,r['extra']]);ff=np.vstack([f,np.array(r['caps']).reshape(-1,3)]);result.append((vv,ff,len(f)))
 return result
if __name__=='__main__':
 data=inputs();start=manifold.Manifold.reserve_ids(2);solids=[]
 for i,(v,f,_)in enumerate(data):
  u,ix=np.unique(v,axis=0,return_inverse=True);g=ix[f];s=manifold.Manifold(manifold.Mesh64(vert_properties=np.ascontiguousarray(u,np.float64),tri_verts=np.ascontiguousarray(g,np.uint64),run_index=np.array([0,3*len(g)],np.uint64),run_original_id=np.array([start+i],np.uint32),face_id=np.arange(len(g),dtype=np.uint64)));print(NAMES[i],s.status(),flush=True);assert s.status()==manifold.Error.NoError;solids.append(s)
 union=solids[0]+solids[1];assert union.status()==manifold.Error.NoError;o=union.to_mesh64();v=np.asarray(o.vert_properties)[:,:3].astype('<f4').astype(float);f=np.asarray(o.tri_verts);runs=np.asarray(o.run_index)//3;ids=np.asarray(o.run_original_id);faceids=np.asarray(o.face_id);parts={};reports=[];centre=np.load(D.parent/'fitted-parent.npz')['v'][np.array(json.load(open(D.parent/'route-input.json'))['parentRim'])].mean(0)
 for i,n in enumerate(NAMES):
  selected=np.zeros(len(f),bool);synthetic=np.zeros(len(f),bool)
  for k,oid in enumerate(ids):
   if oid!=start+i:continue
   sl=slice(runs[k],runs[k+1]);native=faceids[sl]<data[i][2];local=np.linalg.norm(v[f[sl]].mean(1)-centre,axis=1)<1.;selected[sl]=native|local;synthetic[sl]=~native&local
  p,g=compact(v,f[selected]);parts[n]=(p,g);reports.append({'node':n,'exteriorJunctionCapTriangles':int(synthetic.sum()),'vertices':len(p),'triangles':len(g),'selfIntersections':len(intersections(p,g))})
 # Float32 may collapse adjacent Boolean split points. Preserve distinct source
 # coordinates and use exact source representatives wherever possible.
 verts=np.vstack([parts[n][0]for n in NAMES]);offsets=np.r_[0,np.cumsum([len(parts[n][0])for n in NAMES])];source={tuple(x)for n in NAMES for x in mesh(n)[0]};source.update(tuple(x)for x in np.load(D.parent/'fitted-parent.npz')['v']);parents=np.arange(len(verts))
 def root(i):
  while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
  return i
 for a,b in cKDTree(verts).query_pairs(2e-5):
  i,j=root(a),root(b)
  if i==j:continue
  aa=tuple(verts[i])in source;bb=tuple(verts[j])in source
  if aa and bb and not np.array_equal(verts[i],verts[j]):continue
  if bb:i,j=j,i
  parents[j]=i
 q=verts[[root(i)for i in range(len(verts))]];maxshift=float(np.linalg.norm(q-verts,axis=1).max())
 for i,n in enumerate(NAMES):
  p=q[offsets[i]:offsets[i+1]];g=parts[n][1];area=np.linalg.norm(np.cross(p[g[:,1]]-p[g[:,0]],p[g[:,2]]-p[g[:,0]]),axis=1);p,g=compact(p,g[area>1e-10]);parts[n]=(p,g);p.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.tofile(OUT/(n+'.indices.bin'));reports[i].update(finalVertices=len(p),finalTriangles=len(g),finalSelfIntersections=len(intersections(p,g)),removedDegenerateTriangles=int(np.sum(area<=1e-10)))
 p,g=parts[NAMES[0]];q,h=parts[NAMES[1]];v=np.vstack([p,q]);f=np.vstack([g,h+len(p)]);u,e,c=boundary(v,f);report={'changes':reports,'maxWeldDisplacementMm':maxshift,'sharedCoordinates':len(set(map(tuple,p))&set(map(tuple,q))),'nonManifoldEdges':int(np.sum(c>2)),'boundaryEdges':int(np.sum(c==1)),'combinedSelfIntersections':len(intersections(v,f))};print(json.dumps(report),flush=True);(D.parent/'union-validation.json').write_text(json.dumps(report,indent=2)+'\n')
