"""Topology, preservation, arterial joins, and local skull-clearance checks."""
import sys,json,hashlib
from pathlib import Path
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from vtk.util.numpy_support import vtk_to_numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from refine_cavernous import read_glb,accessor,whole_veins,move_artery,closed_artery
from reference import APP,ROOT,poly,records,arrays
OUT=ROOT/'review-v0.9.11';OUT.mkdir(exist_ok=True)
report=json.loads((ROOT/'cavernous-local-build.json').read_text())
v=np.load(ROOT/'venous-mesh.npz');p,f=v['positions'],v['faces'];mesh=trimesh.Trimesh(p,f,process=False)
assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
assert np.isfinite(p).all() and np.isfinite(v['normals']).all()
report['watertight']=True;report['winding_consistent']=True;report['positive_volume']=True;report['minimum_triangle_area_mm2']=float(mesh.area_faces.min())
assert report['minimum_triangle_area_mm2']>1e-12
bp,bf=arrays(next(r for r in records if r['name']=='bone.sphenoid'));bone=poly(bp,bf);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(bone)
arteries={};localstats={}
for version,path in [('before',APP/'.authoring/circulation-raw.glb'),('after',APP/'.authoring/circulation-refined.glb')]:
 d,b=read_glb(path);items=[]
 for node in d['nodes']:
  if 'ICA cavernous' not in node['name']:continue
  pr=d['meshes'][node['mesh']]['primitives'][0];ap=accessor(d,b,pr['attributes']['POSITION']).copy();af=accessor(d,b,pr['indices']).reshape(-1,3).copy();pd=poly(ap,af);dist=np.array([sdf.EvaluateFunction(q) for q in ap]);upper=ap[:,2]>57.0
  localstats[version+' '+node['name']]={'minimum_sphenoid_distance_mm':float(dist.min()),'vertices_inside_sphenoid':int((dist<-.05).sum()),'upper_region_z_over_57mm_minimum_distance':float(dist[upper].min()),'upper_region_vertices_inside_sphenoid':int((dist[upper]<-.05).sum()),'limitation':'Vertex sampling of retained mesh, not a CT-based canal segmentation or exhaustive triangle intersection test'}
  items.append((node['name'],pd,ap,af))
 arteries[version]=items
report['ica_sphenoid_sampling']=localstats
report['ica_sphenoid_sampling_baseline']='Historical v0.9.7 arterial correction, retained unchanged in v0.9.11.'
# Surface vertices and triangle centroids test the actual arterial exclusions.
report['cavernous_ica_surface_clearance']={}
for name,pd,ap,af in arteries['after']:
 side=name.split()[-1];aid=whole_veins(APP/'.authoring/venous-original.glb')[3].index('vein.cavernous.'+side)
 ff=f[v['labels']==aid];used=np.unique(ff);points=np.r_[p[used],p[ff].mean(1)]
 arterial=vtk.vtkImplicitPolyDataDistance();arterial.SetInput(pd)
 lo=ap.min(0)+np.array([-.2,-.2,.8]);hi=ap.max(0)-np.array([-.2,-.2,.8]);keep=np.all((points>lo)&(points<hi),axis=1);dd=np.array([arterial.EvaluateFunction(q) for q in points[keep]])
 inter=vtk.vtkIntersectionPolyDataFilter();inter.SetInputData(0,poly(p,ff));inter.SetInputData(1,pd)
 inter.SplitFirstOutputOff();inter.SplitSecondOutputOff();inter.SetTolerance(1e-5);inter.Update()
 crossings=inter.GetOutput(0).GetNumberOfLines();assert crossings==0,(side,crossings)
 report['cavernous_ica_surface_clearance'][side]={'samples':len(dd),'minimum_sampled_unsigned_surface_distance_mm':float(np.abs(dd).min()),'triangle_intersection_lines':int(crossings),'note':'Checks the actual displayed surfaces. Open label boundaries make signed inside/outside distances unreliable; temporary closure fans are authoring masks, not anatomical dural boundaries.'}
# The same deformation of every local mesh keeps shared seam coordinates shared.
old,ob=read_glb(APP/'.authoring/circulation-raw.glb');new,nb=read_glb(APP/'.authoring/circulation-refined.glb');maxerror=0.;unchanged=0
for n1,n2 in zip(old['nodes'],new['nodes']):
 if 'mesh' not in n1:continue
 a1=old['meshes'][n1['mesh']]['primitives'][0]['attributes']['POSITION'];a2=new['meshes'][n2['mesh']]['primitives'][0]['attributes']['POSITION'];q=accessor(old,ob,a1).copy();r=accessor(new,nb,a2).copy();expected=move_artery(q.astype(float)).astype(np.float32);maxerror=max(maxerror,float(np.linalg.norm(r-expected,axis=1).max()));unchanged+=int(np.array_equal(q,r))
assert maxerror<1e-6
report['arterial_deformation_consistency']={'maximum_shared_coordinate_field_difference_mm':maxerror,'unchanged_meshes':unchanged,'note':'Identical coordinate field across segments and branch attachments; not a new patient vessel segmentation'}
report['retained_skull_sha256']=hashlib.sha256((APP/'public/anatomy/models/craniofacial.glb').read_bytes()).hexdigest()
report['scope']='Reference-guided teaching mesh. Figures from separate patients and uncalibrated projections do not provide patient-specific registration or exact dimensions.'
(APP/'docs/validation/venous-morphology-v0.9.11.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'geometry-checks.json').write_text(json.dumps(report,indent=2)+'\n')
fig,axes=plt.subplots(2,3,figsize=(15,10))
vp,vf,_,_=whole_veins(APP/'.authoring/venous/venous-raw.glb');vp=poly(vp,vf)
for ax,y in zip(axes.ravel(),[-52,-48,-44,-40,-36,-32]):
 for pd,col,lw in [(bone,'#52525b',.7),(vp,'#2c6ac5',.6)]+[(pd,'#a1a1aa',.9) for _,pd,_,_ in arteries['before']]+[(pd,'#c52d25',1.0) for _,pd,_,_ in arteries['after']]:
  plane=vtk.vtkPlane();plane.SetOrigin(0,y,0);plane.SetNormal(0,1,0);c=vtk.vtkCutter();c.SetCutFunction(plane);c.SetInputData(pd);c.Update();section=c.GetOutput()
  if not section.GetNumberOfPoints():continue
  pp=vtk_to_numpy(section.GetPoints().GetData());lines=vtk_to_numpy(section.GetLines().GetData());i=0
  while i<len(lines):
   n=lines[i];q=pp[lines[i+1:i+n+1]];ax.plot(q[:,0],q[:,2],color=col,lw=lw);i+=n+1
 ax.set_xlim(-25,26);ax.set_ylim(46,81);ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_title(f'Coronal section y = {y} mm');ax.set_xlabel('Model x (mm)');ax.set_ylabel('Model z (mm)')
fig.suptitle('Skull and sinus relationships: grey old ICA, red corrected ICA, blue sinus, dark grey bone',fontsize=14);fig.tight_layout(rect=[0,0,1,.97]);fig.savefig(OUT/'11-coronal-sections.png',dpi=150);plt.close(fig)
print(json.dumps({'topology':'passed','triangles':report['triangles'],'venous_clearance':report['cavernous_ica_surface_clearance'],'ica_skull':localstats},indent=2))
