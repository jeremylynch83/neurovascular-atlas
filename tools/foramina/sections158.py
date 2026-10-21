"""Measure native V4 wall sections from the reviewed closed flow projection."""
from pathlib import Path
import sys,json,numpy as np,vtk
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import least_squares
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
m=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={r['id']:r for r in m['structures']};g=Glb(A/'public/anatomy/models/complete-circulation.glb');surfaces=json.load(open(A/'public/anatomy/dsa-surfaces.json'));out={}
for side in ['left','right']:
 sid=f'artery.posterior.vertebral_{side}.segment.v4';p,f,n=g.mesh(rows[sid]['asset']['node']);s=surfaces['entries'][sid];p=np.r_[p,np.asarray(s['extra']).reshape(-1,3)];f=np.array([tri[::-1]if bool(s['reverse'])!=(i in s['flips'])else tri for i,tri in enumerate(f)if i not in s['removed']]);f=np.r_[f,np.asarray(s['caps']).reshape(-1,3)]
 mesh=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(p,deep=True));mesh.SetPoints(vp);cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype('int64').ravel(),deep=True));mesh.SetPolys(cells);ys=np.arange(-92.75,-74.25,.25);centres=[];shapes=[];previous=np.array([9 if side=='right'else-9,29.])
 for y in ys:
  plane=vtk.vtkPlane();plane.SetOrigin(0,y,0);plane.SetNormal(0,1,0);cut=vtk.vtkCutter();cut.SetInputData(mesh);cut.SetCutFunction(plane);cut.Update();strip=vtk.vtkStripper();strip.SetInputConnection(cut.GetOutputPort());strip.JoinContiguousSegmentsOn();strip.Update();v=strip.GetOutput();pts=vtk_to_numpy(v.GetPoints().GetData());loops=[];ids=vtk.vtkIdList();lines=v.GetLines();lines.InitTraversal()
  while lines.GetNextCell(ids):
   ix=np.array([ids.GetId(k)for k in range(ids.GetNumberOfIds())]);poly=pts[ix][:,[0,2]]
   if len(poly)>8 and np.linalg.norm(poly[0]-poly[-1])<1e-4:
    lengths=np.linalg.norm(np.diff(poly,axis=0),axis=1);arc=np.r_[0,lengths.cumsum()];ss=np.linspace(0,arc[-1],160,endpoint=False);samples=np.c_[np.interp(ss,arc,poly[:,0]),np.interp(ss,arc,poly[:,1])];loops.append(samples)
  assert loops,(side,y,'no closed section');q=min(loops,key=lambda q:np.linalg.norm(q.mean(0)-previous));c=q.mean(0);cov=np.cov(q.T)*2;e,U=np.linalg.eigh(cov);r=np.sqrt(np.maximum(e,.01));angle=np.arctan2(U[1,1],U[0,1]);initial=[c[0],c[1],np.log(r[1]),np.log(r[0]),angle]
  def residual(v):
   cx,cz,lr1,lr2,a=v;u=q-[cx,cz];xx=np.cos(a)*u[:,0]+np.sin(a)*u[:,1];zz=-np.sin(a)*u[:,0]+np.cos(a)*u[:,1];return (xx/np.exp(lr1))**2+(zz/np.exp(lr2))**2-1
  fit=least_squares(residual,initial,loss='soft_l1',f_scale=.08,max_nfev=80);cx,cz,lr1,lr2,a=fit.x;R=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);shape=R@np.diag(np.exp([2*lr1,2*lr2]))@R.T;centres.append([cx,cz]);shapes.append(shape);previous=np.array([cx,cz])
 centres=gaussian_filter1d(np.array(centres),1.5,axis=0);shapes=gaussian_filter1d(np.array(shapes),1.5,axis=0);out[side+'_y']=ys;out[side+'_centres']=centres;out[side+'_shapes']=shapes
 print(side,'native minor radius',np.percentile(np.sqrt(np.linalg.eigvalsh(shapes)[:,0]),[5,50,95]),flush=True)
np.savez(A/'anatomy/source/foramina/revision158-native-sections.npz',**out)
