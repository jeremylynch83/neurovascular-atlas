"""Render measured meshes, never diagrams substituted for the model."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT=ROOT.parent/'corrections-work';OUT.mkdir(exist_ok=True)
ART=(.75,.16,.2);VEIN=(.14,.39,.74);TISSUE=(.79,.74,.67);DURA=(.57,.47,.7)
groups={
 'posterior-upper':([(n,ART,1) for n in ['Basilar','SCA right','SCA left','PCA P1 right','PCA P1 left']]+[(n,VEIN,1) for n in ['vein.anterior_pontomesencephalic','vein.anterior_pontine','vein.posterior_communicating']]+[(n,TISSUE,.28) for n in ['brain.pons.right','brain.pons.left','brain.midbrain.right','brain.midbrain.left']], [0,-66,68], [1,1,.35], 22),
 'posterior-lower':([(n,ART,1) for n in ['Basilar','Vertebral V4 right','Vertebral V4 left','PICA right','PICA left']]+[(n,VEIN,1) for n in ['vein.anterior_medullary','vein.pontomedullary.right','vein.pontomedullary.left','vein.marginal']]+[(n,TISSUE,.24) for n in ['brain.pons.right','brain.pons.left','brain.medulla-oblongata.right','brain.medulla-oblongata.left']], [0,-78,37], [0,1,.15], 24),
 'falcotentorial':([(n,VEIN,1) for n in ['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence']]+[(n,DURA,.3) for n in ['brain.falx-cerebri','brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left']]+[('brain.corpus-callosum',TISSUE,.65)], [0,-82,103], [1,0,0], 78),
 'pericallosal':([(f'ACA {s} {side}',ART,1) for side in ['right','left'] for s in ['A2','A3','A4','A5']]+[('brain.corpus-callosum',TISSUE,.85)]+[(n,(.68,.79,.66),.35) for n in meshes if 'brain.cingulate-gyrus' in n and n.endswith('.right')], [0,-55,109], [1,0,0], 50)
}
for key,(parts,centre,direction,scale) in groups.items():
 if '--only-crossings' in sys.argv and key not in ['posterior-upper','posterior-lower']:continue
 fig=plt.figure(figsize=(10,8.5));ax=fig.add_subplot(projection='3d')
 for name,col,opacity in parts:
  m=meshes[name];v=m.v;f=m.f
  if '--after' in sys.argv and (OUT/'candidate-final'/(name+'.positions.bin')).exists():
   v=np.fromfile(OUT/'candidate-final'/(name+'.positions.bin'),'<f4').reshape(-1,3)
  if len(f)>25000:
   dec=vtk.vtkDecimatePro();dec.SetInputData(poly(v,f));dec.SetTargetReduction(1-25000/len(f));dec.PreserveTopologyOn();dec.Update();pd=dec.GetOutput();v=vtk_to_numpy(pd.GetPoints().GetData());f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:]
  tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-9);shade=.64+.36*np.abs(normal@np.array([.5,.5,.707]));colors=np.array(col)*shade[:,None]
  ax.add_collection3d(Poly3DCollection(tri,facecolors=colors,edgecolor='none',alpha=opacity,linewidth=0,rasterized=True))
 ax.set(xlim=(centre[0]-scale,centre[0]+scale),ylim=(centre[1]-scale,centre[1]+scale),zlim=(centre[2]-scale,centre[2]+scale));ax.set_box_aspect([1,1,1]);ax.set_proj_type('ortho');ax.view_init(0 if direction[1]==0 else 10,0 if direction[1]==0 else 75);ax.set_axis_off();ax.set_title(key+' '+('v0.9.31' if '--after' in sys.argv else 'v0.9.30 baseline'));fig.subplots_adjust(0,0,1,.95);fig.savefig(OUT/(key+('-after' if '--after' in sys.argv else '-before')+'.png'),dpi=120,facecolor='white');plt.close(fig);print('Rendered',key,flush=True)
