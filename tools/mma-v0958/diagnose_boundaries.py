"""Measure source anatomical boundaries, rather than carve cortex around tubes."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
cats={s['asset']['node']:s['anatomy']['category']for s in json.loads((WORK.parent/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
mesh={n:load(n,OUT)if n in changed else load(n)for n in FILES}
bones=[n for n in FILES if n.startswith('bone.') and n.split('.')[1] in ['sphenoid','frontal','occipital','parietal','temporal']]
surfaces=['brain.falx-cerebri','brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left']
locs={n:locator(*mesh[n])for n in bones+surfaces}
def witnesses(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
 ids=vtk_to_numpy(c.GetContactCells(0)).astype(int)if c.GetNumberOfContacts()else np.empty(0,int)
 return v[np.unique(f[ids])]
rows=[]
for r in json.loads((OUT/'full-mma-brain-check.json').read_text())['contacts']:
 if r['brain'].startswith(('brain.falx','brain.tentorium')):continue
 p=witnesses(*mesh[r['artery']],*mesh[r['brain']]);ds={n:closest(l,p)[1]for n,l in locs.items()}
 nearest=min(bones,key=lambda n:ds[n].min())
 row=dict(**r,witnessBounds=[p.min(0).tolist(),p.max(0).tolist()],nearestBone=nearest,boneDistanceRange=[float(ds[nearest].min()),float(ds[nearest].max())],duralDistanceRanges={n:[float(ds[n].min()),float(ds[n].max())]for n in surfaces})
 rows.append(row);print(row,flush=True)
(WORK/'boundary-diagnostics.json').write_text(json.dumps(rows,indent=2))
fig,axs=plt.subplots(2,3,figsize=(17,10))
configs=[(1,-49,(20,43,38,75),'Petrosal / cavernous, coronal'),(1,-26,(24,54,64,96),'Lesser wing receiver, coronal'),(1,-109,(0,65,55,112),'Tentorial collateral, coronal'),(0,2,(-70,-30,133,168),'Falcine collateral, sagittal'),(2,64,(10,55,-65,-20),'Cavernous routes, axial'),(2,80,(25,55,-40,-12),'Receiver, axial')]
for ax,(axis,val,limits,title)in zip(axs.ravel(),configs):
 plane=vtk.vtkPlane();o=[0.,0.,0.];o[axis]=val;normal=[0,0,0];normal[axis]=1;plane.SetOrigin(o);plane.SetNormal(normal)
 axes=[k for k in range(3)if k!=axis]
 for n,(v,f)in mesh.items():
  cortex=cats.get(n)=='cerebral_cortex';dura=n in surfaces;bone=n in bones;vessel=n.startswith(('MMA ','Middle meningeal','vein.sphenoparietal','Superior tympanic','Davidoff'))
  if not(cortex or dura or bone or vessel):continue
  if v[:,axis].min()>val or v[:,axis].max()<val:continue
  c=vtk.vtkCutter();c.SetInputData(poly(v,f));c.SetCutFunction(plane);c.Update();out=c.GetOutput()
  if not out.GetNumberOfPoints():continue
  pts=vtk_to_numpy(out.GetPoints().GetData());lines=out.GetLines();lines.InitTraversal();ids=vtk.vtkIdList();segs=[]
  while lines.GetNextCell(ids):
   vv=[ids.GetId(i)for i in range(ids.GetNumberOfIds())]
   for a,b in zip(vv[:-1],vv[1:]):segs.append(pts[[a,b]][:,axes])
  colour='#c59035'if bone else '#286891'if dura else '#d22637'if vessel else '#648772'
  ax.add_collection(LineCollection(segs,colors=colour,linewidths=1.2 if vessel or dura else .65))
 ax.set(xlim=limits[:2],ylim=limits[2:],title=title,xlabel='xyz'[axes[0]]+' (mm)',ylabel='xyz'[axes[1]]+' (mm)');ax.set_aspect('equal');ax.grid(alpha=.2)
fig.suptitle('Exact mesh sections | green cortex, gold skull, blue dural reflections, red vessels');fig.tight_layout()
fig.savefig(WORK/'boundary-sections.png',dpi=140)
