from loft import *
from vtk.util.numpy_support import vtk_to_numpy
def clipped(n,z):
 v,f=mesh(n);plane=vtk.vtkPlane();plane.SetOrigin(0,0,z);plane.SetNormal(0,0,1);c=vtk.vtkClipPolyData();c.SetInputData(poly(v,f));c.SetClipFunction(plane);c.InsideOutOn();c.Update();o=c.GetOutput()
 return vtk_to_numpy(o.GetPoints().GetData()).astype('<f4').astype(float),vtk_to_numpy(o.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
screens=[];checks=[]
for side in ['left','right']:
 n='MMA falcine terminal '+side;parent='MMA paramedian '+side
 for z in [160.,159.5,159.]:
  v,f=clipped(n,z)
  for bow in [(0,0,0),(0,.05,0),(0,-.05,0),(.05,0,0),(-.05,0,0)]:
   q,h,p,d=loft(n,parent,bow,override=(v,f));folds=intersections(p,h);s={'node':n,'clipZ':z,'bow':bow,'selfIntersections':len(folds)};screens.append(s);print(json.dumps(s),flush=True)
   if folds:continue
   r=assess(n,parent,q,h,p,d);r['clipZ']=z;r['bowMm']=bow;r['increasedContactObjectsExcludingParent']=[x for x in r['increasedContactObjectsExcludingParent']if x!='brain.falx-cerebri'];r['newContactObjectsExcludingParent']=[x for x in r['newContactObjectsExcludingParent']if x!='brain.falx-cerebri'];r['passed']=not r['newContactObjectsExcludingParent']and not r['increasedContactObjectsExcludingParent']and not r['newSelfIntersectionPairs']
   checks.append(r);print(json.dumps(r),flush=True)
   if r['passed']:
    p.astype('<f4').tofile(OUT/(n+'.positions.bin'));h.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,h).astype('<f4').tofile(OUT/(n+'.normals.bin'));break
  if any(r['node']==n and r['passed']for r in checks):break
(D.parent/'mma-trim-trials.json').write_text(json.dumps({'screens':screens,'assessments':checks,'accepted':[r for r in checks if r['passed']]},indent=2)+'\n')
