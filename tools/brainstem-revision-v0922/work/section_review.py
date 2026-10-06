import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from geometry import *
import json
p=json.loads((ROOT/'candidate/revision.json').read_text())
for r in p['changed']:
 k=r['node'];meshes[k].new=np.fromfile(ROOT/'candidate'/(k+'.positions.bin'),'<f4').reshape(-1,3).astype(float)
fig,axes=plt.subplots(1,2,figsize=(11,7),sharex=True,sharey=True)
for ax,after,title in zip(axes,[False,True],['v0.9.21','v0.9.22: pons +1.7 mm, midbrain +0.8 mm']):
 for names,colour,lw in [(['bone.occipital','bone.sphenoid'],'#90949b',1.3),(['brain.pons.left','brain.pons.right','brain.midbrain.left','brain.midbrain.right'],'#ab804c',2),(['Basilar'],'#b7353c',1.5),(['vein.basilar_plexus'],'#4778ba',1.6)]:
  for k in names:
   m=meshes[k];plane=vtk.vtkPlane();plane.SetOrigin(.15,0,0);plane.SetNormal(1,0,0);cut=vtk.vtkCutter();cut.SetCutFunction(plane);cut.SetInputData(poly(m.new if after else m.v,m.f));cut.Update();pd=cut.GetOutput();segments=[]
   for i in range(pd.GetNumberOfCells()):
    c=pd.GetCell(i);segments.append([[pd.GetPoint(c.GetPointId(j))[1],pd.GetPoint(c.GetPointId(j))[2]] for j in range(c.GetNumberOfPoints())])
   if segments:ax.add_collection(LineCollection(segments,colors=colour,linewidths=lw))
 if after:
  for k in ['brain.pons.left','brain.pons.right']:
   m=meshes[k];plane=vtk.vtkPlane();plane.SetOrigin(.15,0,0);plane.SetNormal(1,0,0);cut=vtk.vtkCutter();cut.SetCutFunction(plane);cut.SetInputData(m.pd);cut.Update();pd=cut.GetOutput();segments=[]
   for i in range(pd.GetNumberOfCells()):
    c=pd.GetCell(i);segments.append([[pd.GetPoint(c.GetPointId(j))[1],pd.GetPoint(c.GetPointId(j))[2]] for j in range(c.GetNumberOfPoints())])
   ax.add_collection(LineCollection(segments,colors='#ab804c',linewidths=1,linestyles='dashed',alpha=.55))
 ax.set(xlim=(-90,-39),ylim=(42,91),aspect='equal',title=title,xlabel='Anterior direction → (mm)');ax.grid(alpha=.12)
axes[0].set_ylabel('Superior coordinate (mm)')
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([0],[0],color=c,lw=2,label=n) for c,n in [('#90949b','Clivus / skull base'),('#ab804c','Pons / midbrain'),('#b7353c','Basilar artery'),('#4778ba','Clival plexus (retained geometry)')]],loc='lower center',ncol=2,frameon=False)
fig.suptitle('Neurovascular Atlas: matched near-midline sagittal sections',fontweight='bold');fig.subplots_adjust(bottom=.15,wspace=.12)
fig.savefig(ROOT/'app/docs/validation/brainstem-before-after-v0.9.22.png',dpi=170)
