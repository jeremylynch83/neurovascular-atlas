"""Screen MMA vertices against closed, manifold, fold-free neural parcels.

Open or defective parcels are explicitly excluded. Negative screens never
certify clearance from those excluded parcels or from the complete brain.
"""
from route_tools import *
folds={r['node']:r['candidate'] for r in json.loads((OUT/'brain-self-intersections.json').read_text())['results']}
names=[n for n in FILES if 'MMA' in n or n.startswith('Middle meningeal')]
audits=[];rows=[]
for n,bv,bf in brain:
 vv,inv=np.unique(bv.astype('<f4'),axis=0,return_inverse=True);ff=inv[bf]
 edges=np.sort(np.vstack([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
 degenerate=int(np.any(np.diff(np.sort(ff,axis=1),axis=1)==0,axis=1).sum());boundary=int((counts==1).sum());nonmanifold=int((counts>2).sum());self_folds=folds.get(n)
 if self_folds is None and boundary==0 and nonmanifold==0 and degenerate==0:
  self_folds=len(intersections(vv.astype(float),ff))
 eligible=boundary==0 and nonmanifold==0 and degenerate==0 and self_folds==0
 audits.append(dict(node=n,boundaryEdges=boundary,nonmanifoldEdges=nonmanifold,collapsedTriangles=degenerate,selfIntersections=self_folds,eligibleForContainmentScreen=eligible))
 if not eligible:continue
 surface=poly(vv.astype(float),ff);distance=vtk.vtkImplicitPolyDataDistance();distance.SetInput(surface)
 for an in names:
  av,af=current(an);inside_box=np.all(av>=vv.min(0),axis=1)&np.all(av<=vv.max(0),axis=1);ids=np.flatnonzero(inside_box)
  if not len(ids):continue
  points=vtk.vtkPoints();points.SetData(numpy_to_vtk(av[ids],deep=True));input_data=vtk.vtkPolyData();input_data.SetPoints(points)
  select=vtk.vtkSelectEnclosedPoints();select.SetInputData(input_data);select.SetSurfaceData(surface);select.SetTolerance(1e-8);select.CheckSurfaceOn();select.Update();inside=vtk_to_numpy(select.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
  chosen=ids[inside];depth=np.array([abs(distance.EvaluateFunction(av[i])) for i in chosen]);chosen=chosen[depth>.02];depth=depth[depth>.02]
  if len(chosen):
   row=dict(artery=an,brain=n,containedVertices=int(len(chosen)),maximumDepthMm=float(depth.max()),minimumDepthMm=float(depth.min()));rows.append(row);print(row,flush=True)
report=dict(method=__doc__,checkedMmaLabels=len(names),eligibleBrainParcels=sum(r['eligibleForContainmentScreen'] for r in audits),excludedBrainParcels=sum(not r['eligibleForContainmentScreen'] for r in audits),strictContainmentPairs=rows,brainTopology=audits,fullBrainContainmentValidated=False,passedEligibleParcelScreen=not rows)
(OUT/'mma-neural-containment-screen.json').write_text(json.dumps(report,indent=2));print('Containment pairs',len(rows),'Eligible parcels',report['eligibleBrainParcels'],flush=True)
