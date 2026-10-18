from probe import *
from geometry import triangle_crosses_exact
from vtk.util.numpy_support import vtk_to_numpy
O=W/'candidate';reports=[]
for side in ['right','left']:
 n='vein.inferior_ophthalmic.'+side;v=np.fromfile(O/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(O/(n+'.indices.bin'),'<u4').reshape(-1,3);oldv,oldf=scene.mesh(n);oldfaces={tuple(sorted(map(tuple,t)))for t in oldv[oldf]};changed=np.array([tuple(sorted(map(tuple,t)))not in oldfaces for t in v[f]]);ids=np.flatnonzero(changed)
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f[ids]));c.SetInputData(1,poly(v,f));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetCollisionModeToAllContacts();c.Update();aa=vtk_to_numpy(c.GetContactCells(0));bb=vtk_to_numpy(c.GetContactCells(1));pairs={tuple(sorted([int(ids[i]),int(j)]))for i,j in zip(aa,bb)if ids[i]!=j};cross=[];checked=0
 for i,j in pairs:
  a=v[f[i]].astype(float);b=v[f[j]].astype(float)
  if len(set(map(tuple,a))&set(map(tuple,b)))>=2:continue
  checked+=1
  if triangle_crosses_exact(a,b):cross.append([i,j])
 row={'node':n,'changedFaces':len(ids),'nonAdjacentCandidatesChecked':checked,'crossingPairs':cross};reports.append(row);print(row,flush=True)
(O/'selfcheck.json').write_text(json.dumps({'passed':not any(x['crossingPairs']for x in reports),'results':reports},indent=2))
