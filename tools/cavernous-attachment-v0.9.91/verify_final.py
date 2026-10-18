from union_final import *
from vtk.util.numpy_support import numpy_to_vtk
data=inputs();dist=[]
for v,f,_ in data:
 d=vtk.vtkImplicitPolyDataDistance();d.SetInput(poly(v,f));dist.append(d)
parts={n:(np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3))for n in NAMES};result={'changes':[],'contacts':[],'envelopes':[],'passed':True}
shared=set(map(tuple,parts[NAMES[0]][0]))&set(map(tuple,parts[NAMES[1]][0]));v=np.vstack([parts[n][0]for n in NAMES]);f=np.vstack([parts[NAMES[0]][1],parts[NAMES[1]][1]+len(parts[NAMES[0]][0])]);u,ix=np.unique(v,axis=0,return_inverse=True);ed={}
for t in ix[f]:
 for a,b in zip(t,np.roll(t,-1)):
  c=ed.setdefault(tuple(sorted([int(a),int(b)])),[0,0]);c[0]+=1;c[1]+=1 if a<b else -1
pu,pe,pc=boundary(*parts[NAMES[0]]);port={tuple(sorted([tuple(pu[e[0]]),tuple(pu[e[1]])]))for e,c in zip(pe,pc)if c==1 and tuple(pu[e[0]])in shared and tuple(pu[e[1]])in shared};se=[c for e,c in ed.items()if tuple(sorted([tuple(u[e[0]]),tuple(u[e[1]])]))in port];assert len(se)==len(shared)and all(c==[2,0]for c in se);result['interface']={'matchedCoordinates':len(shared),'pairedOppositeBoundaryEdges':len(se),'combinedSelfIntersections':len(intersections(v,f))};assert not result['interface']['combinedSelfIntersections']
t=v[f];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);acc=np.zeros_like(u)
for k in range(3):np.add.at(acc,ix[f[:,k]],cross)
acc/=np.linalg.norm(acc,axis=1)[:,None];off=0
for n in NAMES:
 p,g=parts[n];ov,of=mesh(n);keys=set(map(tuple,p));oldkeys=set(map(tuple,ov));originalnormal=np.fromfile(D/(n+'.normals.bin'),'<f4').reshape(-1,3);lookup={tuple(x):originalnormal[i]for i,x in enumerate(ov)};nn=acc[ix[off:off+len(p)]].copy();off+=len(p)
 for i,x in enumerate(p):
  if tuple(x)in lookup and tuple(x)not in shared:nn[i]=lookup[tuple(x)]
 nn.astype('<f4').tofile(OUT/(n+'.normals.bin'))
 protected=[]
 for r in rims(ov,of):
  if n==NAMES[0]and len(r)==98:continue
  if n==NAMES[1]and len(r)==98:continue
  assert set(map(tuple,ov[r]))<=keys,(n,'lost remote rim');protected.append(len(r))
 if n==NAMES[1]:assert set(map(tuple,ov[ov[:,2]>=54]))<=keys
 attachments=[]
 for m in META:
  other=m['name']
  if other in NAMES:continue
  w,h=mesh(other)
  if np.any(w.max(0)<np.minimum(ov.min(0),p.min(0)))or np.any(w.min(0)>np.maximum(ov.max(0),p.max(0))):continue
  oldshared=oldkeys&set(map(tuple,w));assert oldshared<=keys,(n,other,'removed attachment',len(oldshared-keys))
  if oldshared:attachments.append({'other':other,'coordinatesRetained':len(oldshared)})
  before=cropped_contacts(ov,of,w,h);after=cropped_contacts(p,g,w,h)
  if before or after:result['contacts'].append({'node':n,'other':other,'before':before,'after':after})
  # A partition can gain an existing contact from its partner after union.
  if after and not before:
   partner=next(x for x in NAMES if x!=n);pv,pf=mesh(partner);assert cropped_contacts(pv,pf,w,h)>0,(n,other,'new contacted object')
  if other=='vein.ovale_emissary.left':assert after==0
 oldfaces={tuple(sorted(map(tuple,ov[t])))for t in of};changed=np.array([t for t in g if tuple(sorted(map(tuple,p[t])))not in oldfaces]);t=p[changed];samples=np.unique(np.vstack([t.reshape(-1,3),t.mean(1),(t[:,0]+t[:,1])/2,(t[:,1]+t[:,2])/2,(t[:,2]+t[:,0])/2]),axis=0);dd=np.array([min(d.EvaluateFunction(x)for d in dist)for x in samples]);assert dd.max()<=2e-5,(n,dd.max());env={'node':n,'changedTriangleSamples':len(samples),'maxOutsideScreenedUnionMm':float(dd.max())};result['envelopes'].append(env)
 row={'node':n,'vertices':len(p),'triangles':len(g),'retainedOriginalCoordinates':len(oldkeys&keys),'protectedRemoteRimVertexCounts':protected,'otherLabelAttachments':attachments,'selfIntersections':len(intersections(p,g))};assert not row['selfIntersections'];result['changes'].append(row);print(json.dumps(row),flush=True)
result['parentBoneDepthScreen']=json.load(open(D.parent/'fitted-parent.json'));result['union']=json.load(open(D.parent/'union-validation.json'));(D.parent/'native-validation.json').write_text(json.dumps(result,indent=2)+'\n');(D.parent/'accepted-corrections.json').write_text(json.dumps({'accepted':[{'node':n,'passed':True}for n in NAMES]},indent=2)+'\n');print(json.dumps({'passed':True,'interface':result['interface'],'envelopes':result['envelopes']}),flush=True)
