from embedded_union import *
from vtk.util.numpy_support import vtk_to_numpy
reports=[]
for side in ['left','right']:
 names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];surfs=[closed(n)for n in names];dist=[]
 for s in surfs:
  d=vtk.vtkImplicitPolyDataDistance();d.SetInput(s);dist.append(d)
 for n in names:
  p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3);v,g=mesh(n);oldfaces={tuple(sorted(map(tuple,v[t])))for t in g};changed=[t for t in f if tuple(sorted(map(tuple,p[t])))not in oldfaces];t=p[changed];samples=np.vstack([t.reshape(-1,3),t.mean(1),(t[:,0]+t[:,1])/2,(t[:,1]+t[:,2])/2,(t[:,2]+t[:,0])/2]);samples=np.unique(samples,axis=0);dd=np.array([[d.EvaluateFunction(x)for d in dist]for x in samples]);outside=dd.min(1);nearnew=samples[outside>2e-5];print(n,'max outside union',outside.max(),'expanded samples',len(nearnew),flush=True)
  tissue=[]
  if len(nearnew):
   for m in META:
    if not (m['name'].startswith('brain.')or m['name'].startswith('bone.')):continue
    w,h=mesh(m['name'])
    if np.any(w.max(0)<nearnew.min(0))or np.any(w.min(0)>nearnew.max(0)):continue
    # Source tissue meshes need not be closed. Record intersections of new
    # triangles whose sample expands beyond the original combined vessel.
    q=t[np.any(np.array([[min(d.EvaluateFunction(x)for d in dist)>2e-5 for x in tri]for tri in t]),axis=1)];cnt=cropped_contacts(p,np.array(changed)[np.any(np.array([[min(d.EvaluateFunction(x)for d in dist)>2e-5 for x in tri]for tri in t]),axis=1)],w,h)
    if cnt:tissue.append({'other':m['name'],'contactsWithExpandedFaces':cnt})
  row={'node':n,'changedFaceSamples':len(samples),'maxOutsideBaselineCombinedVesselMm':float(outside.max()),'samplesOutsideByMoreThan20Nanometres':len(nearnew),'expandedFaceTissueContacts':tissue};reports.append(row);print(row,flush=True)
(D.parent/'envelope-validation.json').write_text(json.dumps(reports,indent=2)+'\n')
