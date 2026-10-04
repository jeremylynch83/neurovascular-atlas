"""Independent surface-contour and labelled venous junction checks."""
from pathlib import Path
import sys,json,numpy as np,vtk,trimesh
from vtk.util.numpy_support import vtk_to_numpy
from refine_cavernous import read_glb,accessor,closed_artery
from reference import APP,ROOT,poly
results={}
ids=[r['id'] for r in json.loads((ROOT/'cavernous-local-build.json').read_text())['parts']]
for release,path in [('0.9.9',ROOT/'baseline-v0.9.9/venous-raw.glb'),('0.9.10',ROOT/'venous-raw.glb')]:
 d,b=read_glb(path);cur={}
 for node in d['nodes']:
  if node['name'] not in ['vein.cavernous.right','vein.cavernous.left']:continue
  q=d['meshes'][node['mesh']]['primitives'][0];p=accessor(d,b,q['attributes']['POSITION']).copy();f=accessor(d,b,q['indices']).reshape(-1,3).copy();pd=poly(p,f);sign=1 if node['name'].endswith('right') else -1
  def section(y):
   pl=vtk.vtkPlane();pl.SetOrigin(0,y,0);pl.SetNormal(0,1,0)
   cut=vtk.vtkCutter();cut.SetInputData(pd);cut.SetCutFunction(pl);cut.Update()
   return cut.GetOutput()
  roof_y=[-49,-43.5,-39];wall_y=[-50,-46,-42];wall_z=63.;roofs=[];walls=[]
  for y in roof_y:
   sec=section(y);pp=vtk_to_numpy(sec.GetPoints().GetData())
   lat=pp[:,0] if sign==1 else 1.3-pp[:,0]
   keep=(lat>7)&(lat<18)&(pp[:,2]>67)
   roofs.append(float(pp[keep,2].max()))
  for y in wall_y:
   sec=section(y);pp=vtk_to_numpy(sec.GetPoints().GetData())
   lines=vtk_to_numpy(sec.GetLines().GetData());cross=[];i=0
   while i<len(lines):
    count=lines[i];chain=pp[lines[i+1:i+count+1]];i+=count+1
    for a,bb in zip(chain[:-1],chain[1:]):
     if (a[2]-wall_z)*(bb[2]-wall_z)<=0 and abs(bb[2]-a[2])>1e-8:
      point=a+(bb-a)*(wall_z-a[2])/(bb[2]-a[2])
      cross.append(point[0] if sign==1 else 1.3-point[0])
   walls.append(float(max(cross)) if cross else None)
  t=(roof_y[1]-roof_y[0])/(roof_y[2]-roof_y[0])
  roof_dip=roofs[0]*(1-t)+roofs[2]*t-roofs[1]
  t=(wall_y[1]-wall_y[0])/(wall_y[2]-wall_y[0])
  wall_dip=walls[0]*(1-t)+walls[2]*t-walls[1] if all(w is not None for w in walls) else None
  closed=closed_artery(p,f);mass=vtk.vtkMassProperties();mass.SetInputData(closed);mass.Update()
  cur[node['name']]={'roof_sample_y_mm':roof_y,'wall_sample_y_mm':wall_y,'wall_sample_z_mm':wall_z,'roof_z_mm':roofs,'lateral_wall_x_in_symmetry_frame_mm':walls,'roof_inward_chord_depth_mm':float(roof_dip),'lateral_wall_inward_chord_depth_mm':wall_dip,'temporarily_capped_label_volume_mm3':mass.GetVolume()}
  if release=='0.9.10':assert roof_dip>.5 and wall_dip is not None and wall_dip>.3,(node['name'],roof_dip,wall_dip)
 meshfile=ROOT/('baseline-v0.9.9/venous-mesh.npz' if release=='0.9.9' else 'venous-mesh.npz');v=np.load(meshfile);p,f,l=v['positions'],v['faces'],v['labels'];nn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20)
 e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);tri=np.tile(np.arange(len(f)),3);ix=np.lexsort((e[:,1],e[:,0]));se=e[ix];st=tri[ix];same=np.all(se[1:]==se[:-1],axis=1);ta=st[:-1][same];tb=st[1:][same]
 joins={}
 for side in ['right','left']:
  cs=ids.index('vein.cavernous.'+side)
  for name in ['superficial_middle_cerebral','sphenoparietal']:
   sid='vein.'+name+'.'+side;vein=ids.index(sid);mask=((l[ta]==cs)&(l[tb]==vein))|((l[tb]==cs)&(l[ta]==vein));angles=np.degrees(np.arccos(np.clip(np.einsum('ij,ij->i',nn[ta[mask]],nn[tb[mask]]),-1,1)))
   assert len(angles)>10,sid
   joins[sid]={'shared_welded_edges':int(mask.sum()),'face_dihedral_median_degrees':float(np.median(angles)),'face_dihedral_p95_degrees':float(np.percentile(angles,95)),'face_dihedral_max_degrees':float(angles.max())}
   if release=='0.9.10':assert np.percentile(angles,95)<50,sid
 results[release]={'contours':cur,'joins':joins,'whole_network_volume_mm3':trimesh.Trimesh(p,f,process=False).volume}
results['scope']='Measures actual model surfaces and direct label adjacency. Capped label volumes are authoring estimates, not calibrated patient dimensions; contour checks sample the cavity between venous entries.'
(APP/'docs/validation/cavernous-contours-and-joins-v0.9.10.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
