"""Compare moved faces with baseline, including neighbours and native interfaces."""
from common import *
from collections import Counter
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']};checks=[];pairs=[];collars=[]
mesh={n:load(n) for n in FILES};bounds={n:(v.min(0),v.max(0)) for n,(v,f) in mesh.items()}
after={n:load(n,OUT) for n in changed}
def collision_faces(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update();a=c.GetContactCells(0);return np.unique(vtk_to_numpy(a)).tolist() if a is not None else []
for name in sorted(changed):
 v,f=mesh[name];q,g=after[name];retop=not (q.shape==v.shape and np.array_equal(f,g));moving=np.ones(len(f),bool) if retop else np.any(np.linalg.norm(q[f]-v[f],axis=2)>1e-6,axis=1);fm=f[moving];fp=g if retop else fm;lo=np.minimum(v.min(0),q.min(0))-.2;hi=np.maximum(v.max(0),q.max(0))+.2
 for other,(w,h) in mesh.items():
  if other==name or (other in changed and other<name):continue
  ol,oh=bounds[other]
  if np.any(oh<lo)|np.any(ol>hi):continue
  t=w[h];crop=np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)
  if not crop.any():continue
  shared=cKDTree(w).query(v)[0]<1e-5
  if not retop and shared.any() and not other.startswith(('bone.','brain.','tooth')):
   wa=after.get(other,(w,h))[0];nearest=cKDTree(w).query(v[shared])[1];gap=np.linalg.norm(q[shared]-wa[nearest],axis=1);collars.append(dict(a=name,b=other,sharedVertices=int(shared.sum()),maxMismatchMm=float(gap.max()),movedSharedVertices=int(np.sum(np.linalg.norm(q[shared]-v[shared],axis=1)>1e-6))))
  # Whole partner cropped to the swept box; changed partner uses same original face IDs.
  before=collision_faces(v,fm,w,h[crop]);wa,ha=after.get(other,(w,h));aftercrop=np.all(wa[ha].max(1)>=lo,axis=1)&np.all(wa[ha].min(1)<=hi,axis=1);ac=collision_faces(q,fp,wa,ha[aftercrop]);new=ac if retop else list(set(ac)-set(before))
  if before or ac:
   row=dict(a=name,b=other,baselineMovedFacesInContact=len(before),candidateMovedFacesInContact=len(ac),newContactFaces=len(new),existingSharedInterface=bool(shared.any()),retopologised=retop,sampleNewContactCentres=q[fp[new]].mean(1)[::max(1,len(new)//4)].tolist());pairs.append(row);print(json.dumps(row),flush=True)
 edge=np.sort(np.vstack([g[:,[0,1]],g[:,[1,2]],g[:,[2,0]]]),axis=1);_,counts=np.unique(edge,axis=0,return_counts=True);tri=q[g];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);old=v[f];oa=np.linalg.norm(np.cross(old[:,1]-old[:,0],old[:,2]-old[:,0]),axis=1)
 checks.append(dict(node=name,boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),baselineDegenerateFaces=int(np.sum(oa<1e-11)),candidateDegenerateFaces=int(np.sum(area<1e-11)),newDegenerateFaces=int(np.sum(area<1e-11)) if retop else int(np.sum((area<1e-11)&(oa>=1e-11))),topologyExact=not retop))
print('Collars',json.dumps(collars),flush=True)
r=dict(release='0.9.49',meshChecks=checks,contacts=pairs,collars=collars,passedNewDegenerateFaces=all(r['newDegenerateFaces']==0 for r in checks),passedSharedCollars=all(r['maxMismatchMm']<1e-4 for r in collars),notes=['Native touching labelled interfaces are expected. New contact face IDs are diagnostic, not necessarily new anatomical collision sites.','Unsegmented hypoglossal and IAC canals cause bone overlap and require separate corridor review.'])
(OUT/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
