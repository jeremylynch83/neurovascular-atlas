"""Remove local neighbour conflicts while transporting the pial context together."""
import sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from vtk.util.numpy_support import vtk_to_numpy
OUT=ROOT.parent/'corrections-work';base=json.loads((OUT/'common-context-trials.json').read_text())[0];names=set(base['changed']);allowed=names|{n for n,m in meshes.items() if m.file=='brain-context.glb'}
vertices={n:np.fromfile(OUT/'common-0'/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float) for n in names}
def after(n,v):return poly(v[n],meshes[n].f) if n in v else meshes[n].pd
def bump(v,c,d):
 r=np.linalg.norm((v-c)/6,axis=1);w=1-smooth((r-.25)/.75);return w[:,None]*np.array(d)
def collisions(a,b):
 coll=vtk.vtkCollisionDetectionFilter();coll.SetInputData(0,a);coll.SetInputData(1,b);tr=vtk.vtkTransform();coll.SetTransform(0,tr);coll.SetTransform(1,tr);coll.SetCollisionModeToHalfContacts();coll.SetCellTolerance(1e-7);coll.Update();pd=coll.GetContactsOutput();pts=vtk_to_numpy(pd.GetPoints().GetData()) if pd.GetNumberOfPoints() else np.empty((0,3));return pts
def new_contacts(v):
 pd={n:after(n,v) for n in v};bounds={n:np.array(p.GetBounds()).reshape(3,2).T for n,p in pd.items()};new=[]
 for n,p in pd.items():
  for o,m in meshes.items():
   if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
   b=bounds.get(o,m.bounds)
   if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
   if contacts(p,pd.get(o,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,o])
 return sorted(set(tuple(sorted(p)) for p in new))
remaining=new_contacts(vertices);steps=[]
for iteration in range(5):
 if not remaining:break
 a,b=remaining[0];pts=collisions(after(a,vertices),after(b,vertices));c=pts.mean(0);best=None
 deltas=[np.array(d)*size for size in [.6,1.2,1.8,2.4] for d in [[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[1,0,0],[-1,0,0]]]
 for d,mode in itertools.product(deltas,['common','veins-only']):
  candidate={n:v.copy() for n,v in vertices.items()}
  selected=allowed if mode=='common' else {n for n,m in meshes.items() if m.file=='venous.glb'}
  for n in selected:
   v=vertices.get(n,meshes[n].v);change=bump(v,c,d)
   if np.max(abs(change))>1e-7:candidate[n]=v+change
  if contacts(after(a,candidate),after(b,candidate),True):continue
  targets=json.loads((OUT/'targets.json').read_text())[3:]
  if any(contacts(after(r['one'],candidate),after(r['two'],candidate),True) for r in targets):continue
  new=new_contacts(candidate)
  print('REFINE',iteration,mode,c.round(2).tolist(),d.tolist(),'remaining',new,flush=True)
  if len(new)<len(remaining):best=(candidate,new,d,mode);break
 if best is None:break
 vertices,remaining,d,mode=best;steps.append({'centre':c.tolist(),'extent':[6,6,6],'delta':d.tolist(),'plateau':.25,'mode':mode})
C=OUT/'common-refined';C.mkdir(exist_ok=True)
for n,v in vertices.items():v.astype('<f4').tofile(C/(n+'.positions.bin'))
report={'baseline':base,'refinements':steps,'newContacts':remaining,'changed':list(vertices)};(C/'revision.json').write_text(json.dumps(report,indent=2)+'\n');print('REFINED RESULT',report,flush=True)
