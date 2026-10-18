from affected_checks import *
N='MMA petrosquamosal left';P='Middle meningeal left';history=[];accepted=[]
for length in [1.,2.,3.,5.]:
 v,f,p,d=candidate(N,P,length);assert np.array_equal(f,mesh(N)[1]);changed=np.flatnonzero(np.any(p!=v,axis=1));affected=np.flatnonzero(np.any(np.isin(f,changed),axis=1));before=affected_intersections(v,f,affected);after=affected_intersections(p,f,affected);a=v[f];b=p[f];a=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);b=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);reversed=int(np.sum((np.einsum('ij,ij->i',a,b)<=0)&(np.linalg.norm(a,axis=1)>1e-10)));r={'node':N,'parent':P,**d,'movedVertices':len(changed),'affectedTriangles':len(affected),'newAffectedSelfIntersections':len(after-before),'baselineAffectedSelfIntersections':len(before),'candidateAffectedSelfIntersections':len(after),'reversedFaces':reversed};print(json.dumps({k:x for k,x in r.items()if not isinstance(x,list)}),flush=True);history.append(r)
 if after-before or reversed:continue
 rows=[];new=[];increased=[];lo=np.minimum(v[f[affected]].min((0,1)),p[f[affected]].min((0,1)));hi=np.maximum(v[f[affected]].max((0,1)),p[f[affected]].max((0,1)))
 for m in META:
  other=m['name']
  if other in [N,P]:continue
  w,g=mesh(other)
  if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
  aa=local_contacts(v,f[affected],w,g);bb=local_contacts(p,f[affected],w,g)
  if aa or bb:rows.append({'other':other,'before':aa,'after':bb})
  if bb and not aa:new.append(other)
  if bb>aa:increased.append(other)
 r.update(localContacts=rows,newContactObjects=new,increasedContactObjects=increased)
 if new or increased:print('SCENE_FAIL',rows,flush=True);continue
 w,g=mesh(P);old=affected_intersections(np.vstack([v,w]),np.vstack([f,g+len(v)]),affected);post=affected_intersections(np.vstack([p,w]),np.vstack([f,g+len(p)]),affected);r['newAffectedCombinedIntersections']=len(post-old);r['baselineAffectedCombinedIntersections']=len(old);r['candidateAffectedCombinedIntersections']=len(post);r['passed']=not(post-old)
 if r['passed']:
  p.astype('<f4').tofile(OUT/(N+'.positions.bin'));f.astype('<u4').tofile(OUT/(N+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(N+'.normals.bin'));accepted=[r];break
(D.parent/'petro-local-trials.json').write_text(json.dumps({'accepted':accepted,'trials':history},indent=2)+'\n');print(json.dumps({'accepted':len(accepted),'trials':len(history)}),flush=True)
