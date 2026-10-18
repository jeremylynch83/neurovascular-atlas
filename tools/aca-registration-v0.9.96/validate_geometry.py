from common import *
from cache import BVH
from geometry import triangle_crosses
from regional_validation import face_key
T=W/'accepted';names=['ACA A5 right','Precuneal right','ACA falcine branch right'];C={n:(np.fromfile(T/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(T/(n+'.indices.bin'),'<u4').reshape(-1,3))for n in names};trees={n:BVH.build(*m)for n,m in C.items()};changed={};origins={};rows=[];problems=[]
for n,(p,g)in C.items():
 v,f=scene.mesh(n);source={face_key(v[t])for t in f};ids=np.array([i for i,t in enumerate(g)if face_key(p[t])not in source]);changed[n]=ids;t=p[g[ids]].astype(float);areas=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2;assert areas.min()>1e-10
 predicted=np.fromfile(W/'sheared'/(n+'.positions.bin'),'<f4').reshape(-1,3)if n!='ACA falcine branch right'else v;sourcefaces={face_key(predicted[t]):i for i,t in enumerate(f)};origins[n]={i:sourcefaces.get(face_key(p[t]))for i,t in enumerate(g)}
 row={'node':n,'sourceVertices':len(v),'sourceTriangles':len(f),'vertices':len(p),'triangles':len(g),'changedTriangles':len(ids),'retainedSourceTriangles':len(g)-len(ids),'minimumChangedAreaMm2':float(areas.min())}
 if n!='ACA falcine branch right':
  a=v[f].astype(float);b=predicted[f].astype(float);dot=(np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0])*np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0])).sum(1);assert np.all(dot>0);row['maximumSourceDisplacementMm']=float(np.linalg.norm(predicted-v,axis=1).max());row['sourceNormalOppositeFaces']=0
 # Every exact source attachment is either fixed or mapped identically in both labels.
 row['attachments']=[];sourcekeys=set(map(tuple,v));lookup={tuple(x):q for x,q in zip(v,predicted)}if n!='ACA falcine branch right'else {tuple(x):x for x in v}
 for other in scene.nearby(v.min(0),v.max(0)):
  if other==n:continue
  w,h=scene.mesh(other);common=sourcekeys&set(map(tuple,w))
  if not common:continue
  expected={tuple(lookup[x])for x in common};q,k=C.get(other,(w,h));assert expected<=set(map(tuple,p)),(n,other,'lost own attachment');assert expected<=set(map(tuple,q)),(n,other,'lost partner attachment')
  row['attachments'].append({'other':other,'sourceCoordinatesRetainedOrMappedIdentically':len(common)})
 rows.append(row);print('READY',n,len(ids),flush=True)
checks=0;crossings=[];tissue_contacts=[];preexisting_self=[]
for n,(p,g)in C.items():
 for i in changed[n]:
  a=p[g[i]].astype(float);lo=a.min(0)-1e-7;hi=a.max(0)+1e-7
  for other in sorted(set(scene.nearby(lo,hi))|set(C)):
   w,h=C.get(other,scene.mesh(other));tree=trees.get(other)or scene.bvh(other)
   for j in tree.query(lo,hi):
    if n==other and i==j:continue
    b=w[h[j]].astype(float)
    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
    checks+=1
    if not triangle_crosses(a,b):continue
    row={'node':n,'face':int(i),'other':other,'otherFace':int(j)}
    # The two existing cortical embeddings are assessed using paired source /
    # candidate signed-depth samples, never accepted from contact counts alone.
    if origins[n].get(int(i))is not None and n in ['ACA A5 right','Precuneal right']and other in ['brain.cingulate-gyrus-and-sulcus-middle-posterior-part.right','brain.cingulate-gyrus-and-sulcus-posterior-dorsal-part.right']:tissue_contacts.append(row)
    elif n==other and origins[n].get(int(i))is not None and origins[n].get(int(j))is not None and triangle_crosses(scene.mesh(n)[0][scene.mesh(n)[1][origins[n][int(i)]]],scene.mesh(n)[0][scene.mesh(n)[1][origins[n][int(j)]]]):preexisting_self.append(row)
    else:crossings.append(row)
 print('CHECKED',n,checks,'strict-crossings',len(crossings),'existing-cortical-contact-facets',len(tissue_contacts),flush=True)
# Native edge topology must improve after fitting the previously detached branch.
def stats(parts):
 vv=[];ff=[];o=0
 for v,f in parts:vv.append(v);ff.append(f+o);o+=len(v)
 u,e,c,b,d,_=edge_table(np.vstack(vv),np.vstack(ff));return {'boundaryEdges':int(sum(c==1)),'nonManifoldEdges':int(sum(c>2)),'misorientedEdges':int(sum((c==2)&(b!=0)))}
before=stats([scene.mesh(n)for n in names]);after=stats(list(C.values()));assert after['boundaryEdges']<before['boundaryEdges'];assert after['nonManifoldEdges']<=before['nonManifoldEdges'];assert after['misorientedEdges']<=before['misorientedEdges'];report={'passedStrictGeometry':not crossings,'changes':rows,'trianglePairsChecked':checks,'crossings':crossings,'existingCorticalContactsForDepthRegression':tissue_contacts,'preExistingSelfCrossingsRetained':preexisting_self,'nativeNetwork':{'before':before,'after':after},'scope':'Existing cortical embedding of two translated vessels is handled separately using paired depth regression. Every other changed-face crossing, including every new collar face and self-intersection, is rejected.'};(T/'geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:report[k]for k in ['passedStrictGeometry','trianglePairsChecked','nativeNetwork']},flush=True)

sys.exit(0 if report['passedStrictGeometry'] else 1)
