"""Prove the corrected transverse vein is behind the artery, outside the pons."""
from common import *
v,f=load('vein.transverse_pontine.left');q,_=load('vein.transverse_pontine.left',OUT)
a,b=load('Basilar');tree=vtk.vtkOBBTree();tree.SetDataSet(poly(a,b));tree.BuildLocator()
rows=[]
for before,point in zip(v,q):
    if not (-3.5<point[0]<1 and 53.5<point[2]<57.5):continue
    points=vtk.vtkPoints();ids=vtk.vtkIdList()
    tree.IntersectWithLine([point[0],-40,point[2]],[point[0],-85,point[2]],points,ids)
    if points.GetNumberOfPoints():
        rear=min(points.GetPoint(i)[1] for i in range(points.GetNumberOfPoints()))
        front=max(points.GetPoint(i)[1] for i in range(points.GetNumberOfPoints()))
        rows.append(dict(x=float(point[0]),z=float(point[2]),veinBeforeY=float(before[1]),veinAfterY=float(point[1]),
                         arteryAnteriorY=front,arteryPosteriorY=rear,posteriorClearanceMm=rear-float(point[1])))
report=dict(release='0.9.47',sampledVertices=len(rows),passed=bool(rows) and all(r['posteriorClearanceMm']>0 for r in rows),
            minimumPosteriorClearanceMm=min(r['posteriorClearanceMm'] for r in rows),
            beforeAnteriorVertices=sum(r['veinBeforeY']>r['arteryAnteriorY'] for r in rows),
            afterPosteriorVertices=sum(r['veinAfterY']<r['arteryPosteriorY'] for r in rows),
            method='Anterior-posterior rays through actual basilar triangles at transverse-vein vertex x/z coordinates; smaller arterial crossings are not assigned a universal depth rule.')
(OUT/'depth.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if not report['passed']:
    print('Failed samples', [r for r in rows if r['posteriorClearanceMm']<=0][:10]);sys.exit(1)
