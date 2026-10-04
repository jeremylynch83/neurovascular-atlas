"""Independent topology and local clearance audit of the v0.9.7 export."""
import json
import numpy as np
import trimesh
import vtk
from reference import APP,ROOT,poly
from refine_cavernous import read_glb,accessor

build=json.loads((ROOT/'cavernous-local-build.json').read_text())
data=np.load(ROOT/'venous-mesh.npz');p,f,labels=data['positions'],data['faces'],data['labels']
mesh=trimesh.Trimesh(p,f,process=False)
assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
assert np.isfinite(p).all() and np.isfinite(data['normals']).all()
assert len(np.unique(labels))==104
report={'release':'0.9.7','vertices':len(p),'triangles':len(f),'named_structures':104,
        'watertight':True,'winding_consistent':True,'positive_volume':True,'connected_components':build['connected_components'],
        'minimum_triangle_area_mm2':float(mesh.area_faces.min()),
        'scope':'Checks actual mesh geometry; no clinical or patient-segmentation validation',
        'local_replacement':build}
assert mesh.area_faces.min()>0
ids=[s['id'] for s in build['parts']]
doc,buf=read_glb(APP/'.authoring/circulation-refined.glb')
report['cavernous_ica_clearance']={}
for node in doc['nodes']:
 if 'ICA cavernous' not in node['name']:continue
 prim=doc['meshes'][node['mesh']]['primitives'][0]
 ap=accessor(doc,buf,prim['attributes']['POSITION']);af=accessor(doc,buf,prim['indices']).reshape(-1,3)
 side='right' if 'right' in node['name'] else 'left'
 vf=f[labels==ids.index('vein.cavernous.'+side)]
 inter=vtk.vtkIntersectionPolyDataFilter();inter.SetInputData(0,poly(p,vf));inter.SetInputData(1,poly(ap,af))
 inter.SplitFirstOutputOff();inter.SplitSecondOutputOff();inter.SetTolerance(1e-5);inter.Update()
 lines=inter.GetOutput(0).GetNumberOfLines()
 assert lines==0,(side,lines)
 sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(ap,af))
 used=np.unique(vf);dist=np.array([sdf.EvaluateFunction(v) for v in p[used]])
 report['cavernous_ica_clearance'][side]={'triangle_intersection_lines':int(lines),'minimum_surface_signed_distance_mm':float(dist.min()),
    'note':'Signed distance on a named arterial segment is unreliable beyond its open label interfaces; exact triangle intersections are checked independently.'}
(APP/'docs/validation/venous-morphology-v0.9.7.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='local_replacement'},indent=2))
