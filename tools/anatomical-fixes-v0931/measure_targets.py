"""Inspect the retained mesh targets before changing the teaching model."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from extract_curves import extract
from vtk.util.numpy_support import vtk_to_numpy
OUT=ROOT.parent/'corrections-work';OUT.mkdir(exist_ok=True)
targets=['Basilar','SCA right','Vertebral V4 right','Vertebral V4 left','vein.anterior_pontomesencephalic','vein.anterior_medullary','vein.pontomedullary.left','vein.pontomedullary.right','vein.marginal','vein.straight','vein.galen','vein.inferior_sagittal','brain.falx-cerebri','brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left','brain.corpus-callosum']+[f'ACA {s} {side}' for side in ['right','left'] for s in ['A2','A3','A4','A5']]
for n in targets:
 m=meshes[n];print(n,'bounds',np.round(m.bounds,2).tolist(),'verts',len(m.v),flush=True)
pairs=[('Basilar','vein.anterior_pontomesencephalic'),('SCA right','vein.anterior_pontomesencephalic'),('Vertebral V4 left','vein.marginal'),('Vertebral V4 left','vein.pontomedullary.left'),('Vertebral V4 right','vein.anterior_medullary'),('Vertebral V4 right','vein.pontomedullary.right'),('Vertebral V4 right','vein.pontomedullary.left')]
report=[]
for a,b in pairs:
 coll=vtk.vtkCollisionDetectionFilter();coll.SetInputData(0,meshes[a].pd);coll.SetInputData(1,meshes[b].pd);tr=vtk.vtkTransform();coll.SetTransform(0,tr);coll.SetTransform(1,tr);coll.SetCollisionModeToHalfContacts();coll.SetCellTolerance(1e-7);coll.Update()
 points=vtk_to_numpy(coll.GetContactsOutput().GetPoints().GetData())
 r={'one':a,'two':b,'contacts':coll.GetNumberOfContacts(),'contactPointBounds':np.array([points.min(0),points.max(0)]).tolist(),'centroid':points.mean(0).tolist()}
 print('CONTACT',r,flush=True);report.append(r)
(OUT/'targets.json').write_text(json.dumps(report,indent=2)+'\n')
curves={}
for n in ['vein.straight','vein.galen','vein.inferior_sagittal','vein.anterior_pontomesencephalic','vein.anterior_medullary','vein.pontomedullary.left','vein.pontomedullary.right']+[f'ACA {s} {side}' for side in ['right','left'] for s in ['A2','A3','A4','A5']]:
 q,r,param,t=extract(meshes[n]);curves[n]={'points':q.tolist(),'radii':r.tolist(),'t':t.tolist()};np.save(OUT/(n+'.param.npy'),param)
 print('CURVE',n,'ends',q[[0,-1]].round(2).tolist(),'radius',np.percentile(r,[5,50,95]).round(2).tolist(),flush=True)
(OUT/'curves.json').write_text(json.dumps(curves)+'\n')
