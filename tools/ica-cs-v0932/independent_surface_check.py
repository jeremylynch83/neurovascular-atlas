from pathlib import Path
import numpy as np,json,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
from scipy.spatial import cKDTree
from model import ROOT,DATA,OUT
import sys
D=ROOT/'exported' if '--exported' in sys.argv else OUT
B=DATA
def load(n):
 d=D if (D/(n+'.positions.bin')).exists() else B
 return np.fromfile(d/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(d/(n+'.indices.bin'),'<u4').reshape(-1,3)
def poly(v,f):
 p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(v,deep=True));p.SetPoints(pts);cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype('int64').ravel(),deep=True));p.SetPolys(cells);return p
report=[]
for side in ['right','left']:
 v,f=load('vein.cavernous.'+side);p=poly(v,f);cl=vtk.vtkCleanPolyData();cl.SetInputData(p);cl.SetTolerance(0);cl.Update();pd=cl.GetOutput();v=vtk_to_numpy(pd.GetPoints().GetData());f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:];tri=v[f];c=tri.mean(1);radius=np.linalg.norm(tri-c[:,None],axis=2).max(1);lo=tri.min(1);hi=tri.max(1);tree=cKDTree(c);bad=[]
 for st in range(0,len(f),64):
  ii=np.arange(st,min(st+64,len(f)));ls=tree.query_ball_point(c[ii],radius[ii]+radius.max());a=np.repeat(ii,[len(l) for l in ls]);b=np.concatenate(ls);k=a<b;a=a[k];b=b[k];k=np.all(hi[a]>=lo[b],axis=1)&np.all(hi[b]>=lo[a],axis=1)&~np.any(f[a,:,None]==f[b,None,:],axis=(1,2));a=a[k];b=b[k]
  for aa,bb in zip(a,b):
   if vtk.vtkTriangle.TrianglesIntersect(*tri[aa],*tri[bb]):bad.append((int(aa),int(bb)))
 branches={}
 for stem in ['Meningohypophyseal trunk','Inferolateral trunk','Inferior hypophyseal','Dorsal meningeal','Tentorial marginal','Basal tentorial MHT branch','Medial clival MHT branch','Lateral clival MHT branch','ILT superior ramus','ILT anterolateral ramus','ILT recurrent lacerum ramus','Ophthalmic','Superior hypophyseal','Posterior communicating','Anterior choroidal']:
  av,af=load(stem+' '+side);b=poly(av,af);col=vtk.vtkCollisionDetectionFilter();col.SetInputData(0,p);col.SetInputData(1,b);tr=vtk.vtkTransform();col.SetTransform(0,tr);col.SetTransform(1,tr);col.SetCollisionModeToHalfContacts();col.SetCellTolerance(1e-7);col.Update();branches[stem]=int(col.GetNumberOfContacts())
 report.append({'side':side,'sinusSelfIntersections':len(bad),'sinusSelfPairs':bad,'localArterialBranchSinusContacts':branches});print(report[-1],flush=True)
(OUT/'independent-surface-check.json').write_text(json.dumps(report,indent=2))
