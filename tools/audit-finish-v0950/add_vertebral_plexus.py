"""Representative ventrolateral upper transverse venous plexus, not cervical segmentation."""
from common import *
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter,gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());paths=json.loads((OUT/'new-vein-paths.json').read_text())
replace={'vein.vertebral_periarterial_plexus.'+side for side in ['right','left']};rev['newLabels']=[n for n in rev['newLabels'] if n not in replace];rev['changed']=[r for r in rev['changed'] if r['node'] not in replace];paths=[p for p in paths if p['node'] not in replace]
for side,sign in [('right',1),('left',-1)]:
 d=np.load(WORK/('Vertebral V2 '+side+'.curve.npz'));q=d['q'];order=np.argsort(q[:,2]);q=q[order];interp=PchipInterpolator(q[:,2],q);z=np.linspace(-62,-16,240);a=interp(z);branches=[]
 for theta in [20,50,78]:
  angle=np.deg2rad(theta);offset=np.array([sign*3.8*np.cos(angle),3.8*np.sin(angle),0]);branches.append(a+offset)
 vv,ff=load('vein.vertebral.'+side);centres=[];st=np.arange(-63,-14,.5)
 for zz in st:
  p=section(vv,ff,2,zz);centres.append((p.min(0)+p.max(0))/2)
 vi=PchipInterpolator(st,gaussian_filter1d(np.array(centres),1,axis=0));links=[]
 for zz in [-60,-39,-18]:
  k=np.argmin(abs(z-zz));collector=vi(zz)
  # All links remain on the ventrolateral side of V2, outside its wall.
  for b in branches:
   t=np.linspace(0,1,25);links.append(b[k]+t[:,None]*(collector-b[k]))
 curves=branches+links;allq=np.concatenate(curves);lo=allq.min(0)-1;hi=allq.max(0)+1;spacing=.12;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1);field=np.full(dims,3.,np.float32);radius=.34
 for curve in curves:
  for a,b in zip(curve[:-1],curve[1:]):
   low=np.maximum(np.floor((np.minimum(a,b)-radius-.25-lo)/sp).astype(int),0);high=np.minimum(np.ceil((np.maximum(a,b)+radius+.25-lo)/sp).astype(int)+1,dims);sl=tuple(slice(int(x),int(y)) for x,y in zip(low,high));p=np.stack(np.meshgrid(*[lo[j]+np.arange(low[j],high[j])*sp[j] for j in range(3)],indexing='ij'),axis=-1);ab=b-a;t=np.clip(np.sum((p-a)*ab,axis=-1)/max(np.dot(ab,ab),1e-12),0,1);sdf=np.linalg.norm(p-a-t[...,None]*ab,axis=-1)-radius;field[sl]=np.minimum(field[sl],sdf)
 field=gaussian_filter(field,.65);im=vtk.vtkImageData();im.SetDimensions(*dims);im.SetOrigin(*lo);im.SetSpacing(*sp);im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(order='F'),deep=True));iso=vtk.vtkFlyingEdges3D();iso.SetInputData(im);iso.SetValue(0,0);iso.Update();clean=vtk.vtkCleanPolyData();clean.SetInputConnection(iso.GetOutputPort());clean.SetTolerance(0);clean.Update();fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputConnection(clean.GetOutputPort());fair.SetNumberOfIterations(10);fair.SetPassBand(.2);fair.NormalizeCoordinatesOn();fair.Update();normal=vtk.vtkPolyDataNormals();normal.SetInputConnection(fair.GetOutputPort());normal.SplittingOff();normal.ConsistencyOn();normal.AutoOrientNormalsOn();normal.Update();pd=normal.GetOutput();v=vtk_to_numpy(pd.GetPoints().GetData()).copy();f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].copy();node='vein.vertebral_periarterial_plexus.'+side;write(node,v,f)
 rev['newLabels'].append(node);rev['changed'].append(dict(node=node,file='venous.glb',vertices=len(v),triangles=len(f),topology='new closed connected plexiform regional surface'))
 paths.append(dict(node=node,family='vertebral_periarterial_plexus',side=side,points=[c.tolist() for c in curves],radiusMm=radius,attachment=dict(receiver='vein.vertebral.'+side,terminalCentres=[vi(zz).tolist() for zz in [-60,-39,-18]],attachment='three representative venous links join the unchanged dominant collecting channel by solid-volume overlap'),sourceCorridor='Actual V2 course with a ventrolateral interconnected reference plexus',scope='Selected upper plexiform pattern; levels, transverse foraminal containment and full circumferential microanatomy are not established without cervical vertebrae'))
 print('Built',node,len(v),len(f),flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2)+'\n');(OUT/'new-vein-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
