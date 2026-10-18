from probe import *
from geometry import edge_table,triangle_crosses_exact
from vtk.util.numpy_support import vtk_to_numpy
O=W/'candidate'
changed={}
for p in O.glob('vein.*.positions.bin'):
 if '.branch.'in p.name:continue
 n=p.name[:-len('.positions.bin')];changed[n]=(np.fromfile(p,'<f4').reshape(-1,3),np.fromfile(O/(n+'.indices.bin'),'<u4').reshape(-1,3))
def contacts(v,f,w,g,exact=True):
 # VTK supplies broad intersection pairs; the native binary-coordinate
 # predicate discards shared boundary vertices/edges and numerical contacts.
 a=poly(v,f);b=poly(w,g);c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,a);c.SetInputData(1,b);t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetCollisionModeToAllContacts();c.Update()
 if not c.GetNumberOfContacts():return []
 aa=vtk_to_numpy(c.GetContactCells(0));bb=vtk_to_numpy(c.GetContactCells(1));pairs=set(zip(map(int,aa),map(int,bb)))
 return [(i,j)for i,j in pairs if not exact or triangle_crosses_exact(v[f[i]].astype(float),w[g[j]].astype(float))]
results=[]
for n,(v,f)in changed.items():
 oldv,oldf=scene.mesh(n);u,e,c,b,*_=edge_table(v,f);_,oe,oc,ob,*_=edge_table(oldv,oldf)
 topology={'node':n,'boundaryEdges':int(sum(c==1)),'badEdges':int(sum(c>2)+sum((c==2)&(b!=0))),'sourceBoundaryEdges':int(sum(oc==1)),'sourceBadEdges':int(sum(oc>2)+sum((oc==2)&(ob!=0)))}
 print(topology,flush=True);results.append(topology)
 oldfaces={tuple(sorted(map(tuple,t)))for t in oldv[oldf]};mask=np.array([tuple(sorted(map(tuple,t)))not in oldfaces for t in v[f]])
 g=f[mask];lo=v[g].min((0,1));hi=v[g].max((0,1))
 found=[]
 for other in scene.nearby(lo,hi):
  if other==n:continue
  w,h=changed.get(other,scene.mesh(other));q=w[h];ids=np.flatnonzero(np.all(q.max(1)>=lo,axis=1)&np.all(q.min(1)<=hi,axis=1))
  if not len(ids):continue
  cross=contacts(v,g,w,h[ids]);
  if cross:
   baseline=contacts(oldv,oldf,*scene.mesh(other))
   row={'other':other,'newRegionCrossingPairs':len(cross),'sourceWholeMeshCrossingPairs':len(baseline),'positions':[v[g[i]].mean(0).tolist()for i,j in cross[:8]]};found.append(row);print(n,row,flush=True)
 results.append({'node':n,'changedFaces':len(g),'contacts':found})
for side in ['right','left']:
 names=['vein.inferior_ophthalmic.'+side,'vein.superior_ophthalmic.'+side,'vein.pterygoid_plexus.'+side];parts=[];off=0
 for n in names:
  v,f=changed.get(n,scene.mesh(n));parts.append((v,f+off));off+=len(v)
 v=np.vstack([a for a,b in parts]);f=np.vstack([b for a,b in parts]);u,e,c,b,*_=edge_table(v,f);row={'network':side,'boundaryEdges':int(sum(c==1)),'badEdges':int(sum(c>2)+sum((c==2)&(b!=0)))};print(row,flush=True);results.append(row)
(O/'geometry-check.json').write_text(json.dumps(results,indent=2))
