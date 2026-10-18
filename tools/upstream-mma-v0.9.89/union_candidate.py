from union_probe import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def arrays(p):return vtk_to_numpy(p.GetPoints().GetData()).astype('<f4').astype(float),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
def inside(points,surface):
 q=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(points,deep=True));q.SetPoints(pts);c=vtk.vtkSelectEnclosedPoints();c.SetSurfaceData(surface);c.SetInputData(q);c.SetTolerance(1e-10);c.Update();return vtk_to_numpy(c.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
def compact(v,f):
 u=np.unique(f);inv=np.full(len(v),-1);inv[u]=np.arange(len(u));return v[u],inv[f].astype(np.uint32)
def boundary(v,f):
 u,ix=np.unique(v,axis=0,return_inverse=True);ed=np.vstack([ix[f][:,[0,1]],ix[f][:,[1,2]],ix[f][:,[2,0]]]);edges,c=np.unique(np.sort(ed,1),axis=0,return_counts=True);return u,edges,c
if __name__=='__main__':
 reports=[]
 for side in ['left','right']:
  names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];other=[closed(names[1]),closed(names[0])];parts={};row={'side':side,'changes':[]}
  for i,n in enumerate(names,1):
   reader=vtk.vtkXMLPolyDataReader();reader.SetFileName(str(D.parent/(side+'-split'+str(i)+'.vtp')));reader.Update();o=reader.GetOutput();v,f=arrays(o);native=vtk_to_numpy(o.GetCellData().GetArray('Native')).astype(bool);centres=v[f].mean(1);keep=~inside(centres,other[i-1]);capsKept=int(np.sum(keep&~native));p,g=compact(v,f[keep&native]);parts[n]=(p,g);p.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.tofile(OUT/(n+'.indices.bin'));row['changes'].append({'node':n,'vertices':len(p),'triangles':len(g),'exteriorCapTriangles':capsKept,'selfIntersections':len(intersections(p,g))});print(row['changes'][-1],flush=True)
  p,f=parts[names[0]];q,g=parts[names[1]];u,e,c=boundary(np.vstack([p,q]),np.vstack([f,g+len(p)]));shared={tuple(a)for a in p}&{tuple(a)for a in q};row.update(sharedCoordinates=len(shared),combinedBoundaryEdges=int(np.sum(c==1)),nonManifoldEdges=int(np.sum(c>2)),combinedSelfIntersections=len(intersections(np.vstack([p,q]),np.vstack([f,g+len(p)]))))
  print(row,flush=True);reports.append(row)
 (D.parent/'union-candidate.json').write_text(json.dumps(reports,indent=2)+'\n')
