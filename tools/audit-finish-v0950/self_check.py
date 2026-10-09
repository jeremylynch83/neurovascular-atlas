from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());results=[]
def intersections(v,f):
 _,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);v=v[first];f=inv[f];t=v[f];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1);valid=area>1e-10;lo=t.min(1);hi=t.max(1);cent=t.mean(1);rad=np.linalg.norm(t-cent[:,None],axis=2).max(1);tree=cKDTree(cent);pairs=[]
 for start in range(0,len(f),96):
  aa=np.arange(start,min(start+96,len(f)));near=tree.query_ball_point(cent[aa],rad[aa]+rad.max());bb=np.concatenate(near);aa=np.repeat(aa,[len(k) for k in near]);keep=(aa<bb)&valid[aa]&valid[bb];aa=aa[keep];bb=bb[keep];keep=np.all(lo[aa]<=hi[bb]+1e-8,axis=1)&np.all(lo[bb]<=hi[aa]+1e-8,axis=1)&(np.linalg.norm(cent[aa]-cent[bb],axis=1)<=rad[aa]+rad[bb]);aa=aa[keep];bb=bb[keep];keep=~np.any(f[aa,:,None]==f[bb,None,:],axis=(1,2));aa=aa[keep];bb=bb[keep]
  for a,b in zip(aa,bb):
   if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append((int(a),int(b)))
 return set(pairs)
for row in rev['changed']:
 n=row['node'];
 if '--meningeal-only' in sys.argv and 'middle_meningeal' not in n:continue
 if '--acoustic-only' in sys.argv and not n.startswith(('Labyrinthine','Common cochlear','Anterior vestibular')):continue
 q,g=load(n,OUT)
 if n in FILES:
  v,f=load(n);before=intersections(v,f);retop=not (q.shape==v.shape and np.array_equal(f,g))
 else:before=set();retop=True
 after=intersections(q,g);new=after if retop else after-before;r=dict(node=n,baseline=len(before),candidate=len(after),newIntersections=len(new),newPairs=sorted(new)[:20]);results.append(r);print(json.dumps(r),flush=True)

for family in ['acoustic','meningeal']:
 for side in ['right','left']:
  p=OUT/(family+'-network-'+side+'.npz')
  if p.exists():
   x=np.load(p);pairs=intersections(x['v'],x['f']);rr=dict(node='combined '+family+' network '+side,baseline=0,candidate=len(pairs),newIntersections=len(pairs),newPairs=sorted(pairs)[:20]);results.append(rr);print(json.dumps(rr),flush=True)
r=dict(release='0.9.50',results=results,passed=all(x['newIntersections']==0 for x in results),scope='Per-label non-adjacent triangle intersections, excluding coincident-coordinate adjacency, compared by exact original face IDs. Does not certify the whole atlas network.')
(OUT/'self-intersections.json').write_text(json.dumps(r,indent=2)+'\n')
