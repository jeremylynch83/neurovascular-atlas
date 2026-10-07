"""Verify round-shaft recovery, retaining branched collectors and their collars."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from vtk.util.numpy_support import vtk_to_numpy
OUT=ROOT.parent/'corrections-work';C=OUT/'candidate';R=OUT/'candidate-round';rev=json.loads((C/'revision.json').read_text());changed={r['node'] for r in rev['changed']};base={n:np.fromfile(C/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float) for n in changed};rounding=json.loads((R/'rounding.json').read_text());round_names={r['node'] for r in rounding['rounding'] if r['node']!='vein.posterior_communicating'}
values={n:(np.fromfile(R/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float) if n in round_names else v) for n,v in base.items()};audit=json.loads((Path(__file__).resolve().parents[2]/'docs/validation/anatomical-clearance-v0.9.29.json').read_text())
def contact_points(a,b):
 col=vtk.vtkCollisionDetectionFilter();col.SetInputData(0,a);col.SetInputData(1,b);tr=vtk.vtkTransform();col.SetTransform(0,tr);col.SetTransform(1,tr);col.SetCollisionModeToHalfContacts();col.Update();return vtk_to_numpy(col.GetContactsOutput().GetPoints().GetData())
centre=contact_points(poly(values['vein.lateral_mesencephalic.right'],meshes['vein.lateral_mesencephalic.right'].f),poly(values['brain.base-of-peduncle.right'],meshes['brain.base-of-peduncle.right'].f)).mean(0)
results=[]
for magnitude in [.3,.6,.9,1.2]:
 candidate={n:v.copy() for n,v in values.items()}
 for n,m in meshes.items():
  if m.file!='brain-context.glb':continue
  v=values.get(n,m.v);d=np.linalg.norm((v-centre)/6,axis=1);w=1-smooth((d-.3)/.7)
  if np.max(w)>1e-7:candidate[n]=v+w[:,None]*[0,-magnitude,0]
 pd={n:poly(v,meshes[n].f) for n,v in candidate.items()};bounds={n:np.array(p.GetBounds()).reshape(3,2).T for n,p in pd.items()};new=[]
 for n,p in pd.items():
  for o,m in meshes.items():
   if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
   b=bounds.get(o,m.bounds)
   if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
   if contacts(p,pd.get(o,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,o])
 hits=[contacts(pd.get(r['one'],meshes[r['one']].pd),pd.get(r['two'],meshes[r['two']].pd)) for r in audit['resolvedAuditContacts']]
 r={'magnitude':magnitude,'centre':centre.tolist(),'newContacts':new,'allAuditContactCounts':hits,'roundNodes':list(round_names)};results.append(r);print('ROUND CHECK',r,flush=True)
 if not new and not any(hits):
  final=OUT/'candidate-final';final.mkdir(exist_ok=True)
  for n,v in candidate.items():v.astype('<f4').tofile(final/(n+'.positions.bin'))
  (final/'rounding.json').write_text(json.dumps(r,indent=2)+'\n');break
(OUT/'rounding-trials.json').write_text(json.dumps(results,indent=2)+'\n')
