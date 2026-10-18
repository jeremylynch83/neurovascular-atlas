from union_candidate import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=['MMA frontal left','MMA paramedian left','MMA frontal','MMA paramedian right'];new={n:(np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3))for n in N};result={'changes':[],'interfaces':[],'contacts':[]};passed=True
for side in ['left','right']:
 names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];p,f=new[names[0]];q,g=new[names[1]];shared=set(map(tuple,p))&set(map(tuple,q));v=np.vstack([p,q]);h=np.vstack([f,g+len(p)]);u,ix=np.unique(v,axis=0,return_inverse=True);edges={}
 for t in ix[h]:
  for k in range(3):
   a,b=map(int,t[[k,(k+1)%3]]);key=tuple(sorted([a,b]));c=edges.setdefault(key,[0,0]);c[0]+=1;c[1]+=1 if a<b else -1
 pu,pe,pc=boundary(p,f);port={tuple(sorted([tuple(pu[e[0]]),tuple(pu[e[1]])]))for e,c in zip(pe,pc)if c==1 and tuple(pu[e[0]])in shared and tuple(pu[e[1]])in shared};se=[c for e,c in edges.items()if tuple(sorted([tuple(u[e[0]]),tuple(u[e[1]])]))in port];assert len(se)==len(shared),(len(se),len(shared));assert all(c==[2,0]for c in se);folds=intersections(v,h);assert not folds
 result['interfaces'].append({'side':side,'matchedCoordinates':len(shared),'pairedOppositelyOrientedEdges':len(se),'combinedSelfIntersections':0})
 ov,of=mesh(names[1]);incoming=max(rims(ov,of),key=lambda r:abs(ov[r,0].mean()));centre=ov[incoming].mean(0)
 for n in names:
  p,f=new[n];v,g=mesh(n);oldkeys=set(map(tuple,v));keys=set(map(tuple,p));oldfaces={tuple(sorted(map(tuple,v[t])))for t in g};faces={tuple(sorted(map(tuple,p[t])))for t in f};removed=oldfaces-faces;added=faces-oldfaces;region=max(np.linalg.norm(np.asarray(t)-centre,axis=1).max()for t in removed|added);assert region<2.0,(n,region)
  protected=[];port_counts=[]
  for r in rims(v,g):
   if n==names[1]and np.array_equal(r,incoming):continue
   assert all(tuple(x)in keys for x in v[r]);port_counts.append(len(r))
  # Every original coordinate shared with any other retained label stays fixed.
  sharedchecks=[]
  lo=v.min(0);hi=v.max(0)
  for m in META:
   other=m['name']
   if other in names:continue
   w,gg=mesh(other)
   if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
   match=oldkeys&set(map(tuple,w))
   if match:assert match<=keys,(n,other,len(match-keys));sharedchecks.append({'other':other,'retainedSharedCoordinates':len(match)})
  row={'node':n,'vertices':len(p),'triangles':len(f),'retainedOriginalVertices':sum(tuple(x)in keys for x in v),'retainedOriginalFaces':len(oldfaces&faces),'removedFaces':len(removed),'newFaces':len(added),'maxChangedFaceDistanceFromOriginalInletMm':float(region),'protectedNativeRimVertexCounts':port_counts,'otherLabelSharedCoordinates':sharedchecks,'selfIntersections':len(intersections(p,f))};assert row['selfIntersections']==0;result['changes'].append(row);print(json.dumps(row),flush=True)
  # Test the complete local scene; unchanged remote triangles need no retest.
  for m in META:
   other=m['name']
   if other in names:continue
   w,gg=mesh(other)
   if np.any(w.max(0)<np.minimum(v.min(0),p.min(0)))or np.any(w.min(0)>np.maximum(v.max(0),p.max(0))):continue
   before=cropped_contacts(v,g,w,gg);after=cropped_contacts(p,f,w,gg)
   if before or after:
    rr={'node':n,'other':other,'before':before,'after':after};result['contacts'].append(rr)
    if after>before:print('RETESSSELLATED_CONTACT_COUNT',rr,flush=True)
   if after and not before:passed=False;print('NEW_CONTACT_OBJECT',rr,flush=True)
result['topologyAndContactObjectsPassed']=passed;result['facetCountIncreasesRequireEnvelopeCheck']=True;result['passed']=False;(D.parent/'native-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':passed,'interfaces':result['interfaces'],'contactPairs':len(result['contacts'])}),flush=True)
