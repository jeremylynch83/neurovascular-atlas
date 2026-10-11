"""Check source skull/brain intersection points near the trial MMA course."""
from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
guides=json.loads((WORK/'mma-guides.json').read_text());tree=cKDTree(np.concatenate([g['points'] for g in guides]));rows=[]
def crop(v,f):
 t=v[f];centre=t.mean(1);radius=np.linalg.norm(t-centre[:,None],axis=2).max(1);return f[tree.query(centre)[0]<radius+4]
for bone in ['bone.sphenoid','bone.temporal.left','bone.temporal.right','bone.parietal.left','bone.parietal.right','bone.frontal']:
 v,f=load(bone);tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);centre=tri.mean(1);f=crop(v,f[np.einsum('ij,ij->i',normal,centre-[0,-60,95])<0])
 if not len(f):continue
 for brain in FILES:
  if not brain.startswith('brain.'):continue
  w,g=load(brain);g=crop(w,g)
  if not len(g):continue
  c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
  p=c.GetContactsOutput().GetPoints()
  if p is None:continue
  points=vtk_to_numpy(p.GetData());d=tree.query(points)[0];points=points[d<3.5]
  if not len(points):continue
  row=dict(bone=bone,brain=brain,contactPointCount=len(points),minDistanceToGuideMm=float(d.min()),sampleContactPoints=points[::max(1,len(points)//5)].tolist());rows.append(row);print(json.dumps(row),flush=True)
(WORK/'reference-corridor-conflicts.json').write_text(json.dumps(dict(scope='Exact source inner-table/brain surface intersections within 3.5 mm of the trial MMA guide. Does not prove every possible alternative course is impossible.',pairs=rows),indent=2))
