from round_geometry import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def components(v,f):
 u,inv=np.unique(v,axis=0,return_inverse=True);h=inv[f];e=np.vstack([h[:,[0,1]],h[:,[1,2]],h[:,[2,0]]]);G=coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(len(u),len(u))).tocsr();_,lab=connected_components(G);sizes=np.bincount(lab);return sorted([int(s)for s in sizes if s>1],reverse=True)
R=json.load(open(D.parent/'mma-network-trials.json'));assert len(R['accepted'])==2;new={};retention=[]
for d in R['accepted']:
 side=d['side'];names=['MMA paramedian '+side,'MMA falcine terminal '+side]
 for n in names:
  v,f=mesh(n);p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float);g=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3);used=np.unique(g);inv=np.full(len(p),-1);inv[used]=np.arange(len(used));p=p[used];g=inv[g].astype(np.uint32)
  key='sharedParentIndices'if n==names[0]else'sharedChildIndices';d[key]=inv[d[key]].tolist();assert min(d[key])>=0
  sizes=components(p,g);before=components(v,f)
  if n==names[0]:assert len(sizes)==1
  else:assert len(sizes)==len(before)
  keys={tuple(q)for q in p};protected=[]
  if n==names[0]:
   rr=rims(v,f);j=max(range(len(rr)),key=lambda i:abs(v[rr[i],0].mean()));protected=v[rr[j]];assert all(tuple(q)in keys for q in protected)
  else:protected=v[v[:,2]<=d['childCutZ']];assert all(tuple(q)in keys for q in protected)
  retention.append({'node':n,'originalNativeOrDistalVerticesRetainedExactly':len(protected),'originalVerticesRetainedExactly':sum(tuple(q)in keys for q in v),'baselineComponentVertexCounts':before,'candidateComponentVertexCounts':sizes,'noNewDisconnectedComponents':True})
  p.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.astype('<u4').tofile(OUT/(n+'.indices.bin'));new[n]=(p,g)
 p,f=new[names[0]];q,g=new[names[1]];assert np.array_equal(p[d['sharedParentIndices']],q[d['sharedChildIndices']]);vertices=np.vstack([p,q]);faces=np.vstack([f,g+len(p)]);u,inv=np.unique(vertices,axis=0,return_inverse=True);edges={}
 for t in inv[faces]:
  for k in range(3):
   a,b=map(int,t[[k,(k+1)%3]])
   if a==b:continue
   e=tuple(sorted([a,b]));rr=edges.setdefault(e,[0,0]);rr[0]+=1;rr[1]+=1 if a<b else -1
 port=inv[d['sharedParentIndices']];ks=[tuple(sorted([int(a),int(b)]))for a,b in zip(port,np.roll(port,-1))];assert all(edges[k]==[2,0]for k in ks)
 combined=intersections(vertices,faces);assert not combined
 d['sharedRimEdgesChecked']=len(ks);d['sharedRimUnpairedEdges']=0;d['sharedCoordinatesExact']=True;d['combinedSelfIntersections']=len(combined)
 t=vertices[faces];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);acc=np.zeros_like(u)
 for k in range(3):np.add.at(acc,inv[faces[:,k]],cross)
 length=np.linalg.norm(acc,axis=1);assert np.all(length>1e-12);nn=acc/length[:,None];nn[inv[:len(p)]].astype('<f4').tofile(OUT/(names[0]+'.normals.bin'));nn[inv[len(p):]].astype('<f4').tofile(OUT/(names[1]+'.normals.bin'))
cross=[]
for a in ['MMA paramedian left','MMA falcine terminal left']:
 for b in ['MMA paramedian right','MMA falcine terminal right']:
  before=cropped_contacts(*mesh(a),*mesh(b));after=cropped_contacts(*new[a],*new[b]);assert after<=before;cross.append({'a':a,'b':b,'before':before,'after':after})
R['crossNetworkContacts']=cross;R['retention']=retention;R['sharedNormalsMethod']='Area-weighted normals on the combined exterior wall, welded by exact coordinates at the new ring.';(D.parent/'mma-network-trials.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({'retention':retention,'sharedEdges':[r['sharedRimEdgesChecked']for r in R['accepted']],'passed':True}))
