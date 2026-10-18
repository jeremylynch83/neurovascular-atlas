from round_geometry import *
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy
m=json.load(open(APP/'public/anatomy/manifest.json'));s=next(s for s in m['structures']if s.get('asset',{}).get('node')=='vein.superior_sagittal');r=json.load(open(APP/'public/anatomy/dsa-surfaces.json'))['entries'][s['id']];v,f=mesh('vein.superior_sagittal');verts=np.vstack([v,r['extra']]);removed=set(r['removed']);flips=set(r['flips']);tri=np.array([t[::-1]if(r['reverse']!=(i in flips))else t for i,t in enumerate(f)if i not in removed]);tri=np.vstack([tri,np.array(r['caps']).reshape(-1,3)]);clean=vtk.vtkCleanPolyData();clean.SetInputData(poly(verts,tri));clean.SetTolerance(0.);clean.Update();surface=clean.GetOutput()
def inside(points):
 p=vtk.vtkPolyData();ps=vtk.vtkPoints();ps.SetData(numpy_to_vtk(points,deep=True));p.SetPoints(ps);q=vtk.vtkSelectEnclosedPoints();q.SetInputData(p);q.SetSurfaceData(surface);q.SetTolerance(1e-8);q.Update();return vtk_to_numpy(q.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
rows=[]
for n in ['MMA paramedian left','MMA falcine terminal left','MMA paramedian right','MMA falcine terminal right']:
 old,_=mesh(n);p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float);before=int(inside(old).sum());after=int(inside(p).sum());assert after==0,(n,after);rows.append({'node':n,'baselineVerticesInsideSinusProxy':before,'candidateVerticesInsideSinusProxy':after,'candidateVerticesChecked':len(p)})
(D.parent/'sinus-volume-check.json').write_text(json.dumps({'passed':True,'method':'VTK point inclusion in closed, oriented DSA sinus proxy; a geometric diagnostic, not anatomical certification.','results':rows},indent=2)+'\n');print(json.dumps(rows))
