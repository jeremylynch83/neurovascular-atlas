"""Selected bilateral companion and CPA venous reference courses.
Canal surfaces and nerves are not supplied; these are illustrative courses.
"""
from common import *
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def resample(q,step=.25):
 keep=np.r_[True,np.linalg.norm(np.diff(q,axis=0),axis=1)>1e-5];q=q[keep];s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];t=np.linspace(0,s[-1],max(12,int(s[-1]/step)+1));return PchipInterpolator(s,q)(t)
def tube(q,r):
 p=vtk.vtkPolyData();points=vtk.vtkPoints();points.SetData(numpy_to_vtk(q,deep=True));p.SetPoints(points);line=vtk.vtkCellArray();line.InsertNextCell(len(q));
 for i in range(len(q)):line.InsertCellPoint(i)
 p.SetLines(line);arr=numpy_to_vtk(r,deep=True);arr.SetName('radius');p.GetPointData().SetScalars(arr)
 t=vtk.vtkTubeFilter();t.SetInputData(p);t.SetRadius(1);t.SetVaryRadiusToVaryRadiusByAbsoluteScalar();t.SetNumberOfSides(20);t.CappingOn();t.Update();tri=vtk.vtkTriangleFilter();tri.SetInputConnection(t.GetOutputPort());tri.Update();clean=vtk.vtkCleanPolyData();clean.SetInputConnection(tri.GetOutputPort());clean.SetTolerance(0);clean.Update();normal=vtk.vtkPolyDataNormals();normal.SetInputConnection(clean.GetOutputPort());normal.SplittingOff();normal.ConsistencyOn();normal.AutoOrientNormalsOn();normal.Update();pd=normal.GetOutput();return vtk_to_numpy(pd.GetPoints().GetData()).copy(),vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
def connect(q,receiver,maximum_z=None,avoid_points=None):
 v,f=load(receiver,OUT) if (OUT/(receiver+'.positions.bin')).exists() else load(receiver)
 target=f if maximum_z is None else f[v[f].mean(1)[:,2]<=maximum_z]
 if receiver.startswith('vein.superior_petrosal_vein.'):
  side=receiver.rsplit('.',1)[1];ov,of=load('vein.cerebellopontine_fissure.'+side);dist=cKDTree(ov).query(v[target].mean(1))[0];target=target[dist>1.0]
 if avoid_points is not None:target=target[cKDTree(np.array(avoid_points)).query(v[target].mean(1))[0]>1.4]
 assert len(target), 'No independent receiver surface within the chosen drainage region'
 cp,dd=closest(locator(v,target),q[-1:]);cp=cp[0];direction=cp-q[-1];length=np.linalg.norm(direction);direction/=max(length,1e-8);end=cp+direction*.3
 # Use a smooth independent extracanal drainage stem; distal source is fixed.
 anchor=q[-1];control=np.vstack([q[-min(4,len(q))],anchor,anchor+(end-anchor)*.35,end]);stem=resample(control);start=cKDTree(stem).query(anchor)[1];q=np.vstack([q,stem[start+1:]])
 return resample(q),dict(receiver=receiver,surfaceEntryPoint=cp.tolist(),terminalCentre=end.tolist(),nativeSurfaceGapBeforeStemMm=float(dd[0]),attachment='continuous solid-volume overlap at the receiving venous wall; separate exterior surfaces')
def repel_arteries(q,r,receiver,outward_arteries=False):
 original=q.copy();lo=q.min(0)-2;hi=q.max(0)+2;obstacles=[]
 for n,filename in FILES.items():
  if not (filename in ['complete-circulation.glb','complete-anastomoses.glb'] or n.startswith(('brain.','tooth-','vein.'))):continue
  if n==receiver:continue
  v,f=load(n)
  if np.any(v.max(0)<lo) or np.any(v.min(0)>hi):continue
  fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f));obstacles.append((n,fn,v.min(0),v.max(0)))
 for it in range(90):
  delta=np.zeros_like(q)
  for n,fn,a,b in obstacles:
   active=np.flatnonzero(np.all(q>=a-r-.3,axis=1)&np.all(q<=b+r+.3,axis=1))
   for k in active:
    cp=[0.,0.,0.];d=fn.EvaluateFunctionAndGetClosestPoint(q[k],cp)
    arterial=outward_arteries and FILES.get(n) in ['complete-circulation.glb','complete-anastomoses.glb'];distance=d if arterial else abs(d)
    if distance>=r+.22:continue
    normal=(q[k]-cp)*(-1 if arterial and d<0 else 1);normal/=max(np.linalg.norm(normal),1e-8);delta[k]+=normal*min(r+.22-distance,.2)
  delta=gaussian_filter1d(delta,1.1,axis=0);delta[-1:]=0
  if not delta.any():break
  q+=delta*.6
  q[1:-1]=gaussian_filter1d(q,1.5,axis=0)[1:-1]
 return q,float(np.linalg.norm(q-original,axis=1).max())
revision=json.loads((OUT/'revision.json').read_text())
families=['inferior_alveolar','infraorbital','internal_auditory']
replace={'vein.'+family+'.'+side for family in families for side in ['right','left']}
revision['newLabels']=[n for n in revision['newLabels'] if n not in replace];revision['changed']=[r for r in revision['changed'] if r['node'] not in replace]
paths=[p for p in json.loads((OUT/'new-vein-paths.json').read_text()) if p['node'] not in replace] if (OUT/'new-vein-paths.json').exists() else []
for side,sign in [('right',1),('left',-1)]:
 for family,artery,offset,radius in [('inferior_alveolar','Inferior alveolar',np.array([-sign*.9,.0,-.25]),.28),('infraorbital','Infraorbital',np.array([-sign*1.5,0,.5]),.25)]:
  name=artery+(' left' if side=='left' else '');curve=np.load(WORK/(name+'.curve.npz'));q=curve['q'];q=q if q[0,1]<q[-1,1] else q[::-1]
  if family=='inferior_alveolar':q=q[(q[:,1]>-43)&(q[:,1]<-9)]
  q=q[::-1]+offset # distal tissue towards the infratemporal venous collector
  receiver='vein.pterygoid_plexus.'+side;q,attachment=connect(q,receiver);q,adjust=repel_arteries(q,radius,receiver);r=radius*(.65+.35*smooth(np.arange(len(q))/8));v,f=tube(q,r);node='vein.'+family+'.'+side;write(node,v,f)
  revision['newLabels'].append(node);revision['changed'].append(dict(node=node,file='venous.glb',vertices=len(v),triangles=len(f),topology='new closed smooth reference tube'))
  paths.append(dict(node=node,family=family,side=side,points=q.tolist(),radiusMm=radius,arterialClearanceAdjustmentMm=adjust,attachment=attachment,sourceCorridor=name,scope='reference course through the existing arterial canal corridor; lumen and nerve containment unverified'))
  print('Built',node,len(v),len(f),flush=True)
 # A selected CPA drainage path, distinct from the intrabony route to the IPS.
 record=json.loads(Path('anatomy/source/relationships-v0949/acoustic-paths.json').read_text())
 # The authoring record format is retained independently; use the actual mesh
 # terminal near the porus as the surface-region anchor.
 v,f=load('Labyrinthine '+side);region=v[(v[:,2]>55)&(v[:,1]<-68)];start=np.median(region,axis=0);start[0]-=sign*.7;start[1]-=.7
 q=np.vstack([start,start+np.array([-sign*.25,-.3,.1]),start+np.array([-sign*.5,-.6,.2])]);receiver='vein.superior_petrosal_vein.'+side;q,attachment=connect(q,receiver,maximum_z=float(start[2]+2.5));q,adjust=repel_arteries(q,.22,receiver);r=np.full(len(q),.22);v,f=tube(q,r);node='vein.internal_auditory.'+side;write(node,v,f);revision['newLabels'].append(node);revision['changed'].append(dict(node=node,file='venous.glb',vertices=len(v),triangles=len(f),topology='new closed smooth reference tube'))
 paths.append(dict(node=node,family='internal_auditory',side=side,points=q.tolist(),radiusMm=.22,arterialClearanceAdjustmentMm=adjust,attachment=attachment,sourceCorridor='internal acoustic surface region to superior petrosal vein',scope='selected CPA venous drainage pattern; does not depict the separate intrabony drainage or cochlear/vestibular aqueduct veins'))
revision['method']+=' Selected companion and CPA veins use capped smooth tubes, surface-based drainage stems and illustrative radii.'
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'new-vein-paths.json').write_text(json.dumps(paths,indent=2)+'\n');print(json.dumps([{k:v for k,v in p.items() if k!='points'} for p in paths],indent=2))
