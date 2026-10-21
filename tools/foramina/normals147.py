"""Retain source shading on unchanged faces; no vertex positions are moved."""
from pathlib import Path
import sys,numpy as np,trimesh,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb,normals
B=A.parent/'inr-anatomy-atlas-v0.9.146';g=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=g.mesh('bone.sphenoid');n=normals(p,f);src=np.load(A/'anatomy/source/foramina/revision145-native-sources.npz');old=Glb(B/'public/anatomy/models/craniofacial.glb').mesh('bone.sphenoid');native=(src['sphenoid_positions'],src['sphenoid_faces'],src['sphenoid_normals'])
for pp,ff,nn in [old,native]:
 pd=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(pp,deep=True));pd.SetPoints(vp);cells=vtk.vtkCellArray();cells.SetCells(len(ff),numpy_to_vtkIdTypeArray(np.c_[np.full(len(ff),3),ff].astype('int64').ravel(),deep=True));pd.SetPolys(cells);loc=vtk.vtkStaticCellLocator();loc.SetDataSet(pd);loc.BuildLocator();near=np.zeros_like(p);ids=np.zeros(len(p),int);dist=np.zeros(len(p))
 for i,pt in enumerate(p):
  cp=[0.,0.,0.];cell=vtk.reference(0);sub=vtk.reference(0);d=vtk.reference(0.);loc.FindClosestPoint(pt,cp,cell,sub,d);near[i]=cp;ids[i]=int(cell);dist[i]=float(d)
 sel=dist<1e-8;tri=pp[ff[ids[sel]]];w=trimesh.triangles.points_to_barycentric(tri,near[sel]);vals=(nn[ff[ids[sel]]]*w[:,:,None]).sum(1);valid=np.isfinite(vals).all(1);idx=np.flatnonzero(sel)[valid];n[idx]=vals[valid];print('Inherited normals',len(idx),flush=True)
n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);g.replace('bone.sphenoid',p,f,n);print(g.save(),flush=True)
