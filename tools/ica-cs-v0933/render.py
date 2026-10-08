from model import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb
RENDERS=ROOT/'renders';RENDERS.mkdir(exist_ok=True)
def draw(ax,name,color,alpha=1,after=True,decimate=0):
 if after and '--exported' in __import__('sys').argv:
  v=np.fromfile(ROOT/'exported'/(name+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(ROOT/'exported'/(name+'.indices.bin'),'<u4').reshape(-1,3);p=poly(v,f)
 else:p=poly(*load(name,after))
 if name.startswith('bone.'):
  p=crop(p,np.array([-24,-65,46]),np.array([24,-25,89]));plane=vtk.vtkPlane();plane.SetOrigin(8,0,0);plane.SetNormal(-1,0,0);c=vtk.vtkClipPolyData();c.SetInputData(p);c.SetClipFunction(plane);c.Update();p=c.GetOutput()
 if decimate:
  d=vtk.vtkDecimatePro();d.SetInputData(p);d.SetTargetReduction(decimate);d.PreserveTopologyOn();d.Update();p=d.GetOutput()
 p=normals(p);v,f=arrays(p);t=v[f];n=vtk_to_numpy(p.GetPointData().GetNormals())[f].mean(1);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-10);light=np.array([.6,.2,.8]);shade=.65+.3*np.abs(n@light);cols=np.clip(np.array(to_rgb(color))[None,:]*shade[:,None],0,1);pc=Poly3DCollection(t,facecolors=cols,edgecolors='none',alpha=alpha,zsort='average',rasterized=True);ax.add_collection3d(pc)
def panel(ax,after=True,oblique=False,network=False,bilateral=False,bone=True):
 if bone:draw(ax,'bone.sphenoid','#cfb991',.35,after, .55)
 sides=['right','left'] if bilateral else ['right']
 for s in sides:
  for name in ['ICA petrous ','ICA cavernous ','ICA paraophthalmic ','ICA posterior communicating ','ICA anterior choroidal ','ICA terminus ']:
   if any(a['name']==name+s for a in META):draw(ax,name+s,'#e87c31',1,after,.25)
  draw(ax,'Ophthalmic '+s,'#008778',1,after,.20)
  if network:
   for stem in ['Meningohypophyseal trunk','Inferolateral trunk','Inferior hypophyseal','Dorsal meningeal','Tentorial marginal']:
    draw(ax,stem+' '+s,'#e87c31',.95,after,.40)
  draw(ax,'vein.cavernous.'+s,'#6fa0e5',.24,after,.20)
  if network:
   for stem in ['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary']:draw(ax,'vein.'+stem+'.'+s,'#568bd0',.55,after,.25)
 if network and bilateral:
  for m in ['anterior_intercavernous','posterior_intercavernous','basilar_plexus']:draw(ax,'vein.'+m,'#568bd0',.55,after,.25)
 centre=[0 if bilateral else 11,-45,68];span=[25 if bilateral else 15,20,24];ax.set_xlim(centre[0]-span[0],centre[0]+span[0]);ax.set_ylim(centre[1]-span[1],centre[1]+span[1]);ax.set_zlim(centre[2]-span[2],centre[2]+span[2]);ax.set_box_aspect(span);ax.set_proj_type('ortho');ax.view_init(elev=0 if bilateral else (18 if oblique else 0),azim=90 if bilateral else(25 if oblique else 0));ax.set_axis_off()
 if not bilateral:ax.invert_yaxis()
def main():
 fig=plt.figure(figsize=(18,10),facecolor='white')
 for i,after in enumerate([False,True]):
  ax=fig.add_subplot(1,2,i+1,projection='3d');panel(ax,after);ax.set_title('Current v0.9.32' if not after else 'Refined v0.9.33',fontsize=18,pad=0,color='#203446')
 fig.suptitle('Smaller posterior sinus and smoother connected surfaces',fontsize=21)
 fig.text(.07,.035,'Same scale and camera. Orange: ICA   Teal: fixed ophthalmic artery   Blue: sinus   Beige: bone cutaway',fontsize=11,color='#687787')
 fig.subplots_adjust(left=0,right=1,bottom=.06,top=.9,wspace=0);fig.savefig(RENDERS/'ICA_CS_refinement_lateral.png',dpi=145);plt.close(fig)
 for label,kwargs in [('ICA_CS_refinement_oblique',{'oblique':True,'network':True}),('ICA_CS_refinement_AP',{'bilateral':True,'network':True})]:
  fig=plt.figure(figsize=(18,10),facecolor='white')
  for i,after in enumerate([False,True]):
   ax=fig.add_subplot(1,2,i+1,projection='3d');panel(ax,after,**kwargs);ax.set_title('Current v0.9.32' if not after else 'Refined v0.9.33',fontsize=17,pad=0,color='#203446')
  fig.suptitle('Connected venous surfaces: '+('AP' if 'AP' in label else 'oblique'),fontsize=21)
  fig.text(.07,.025,'Ophthalmic origins and bone fixed. Model comparison, not patient-specific anatomy.',fontsize=11,color='#687787')
  fig.subplots_adjust(left=0,right=1,bottom=.04,top=.9,wspace=0);fig.savefig(RENDERS/(label+'.png'),dpi=150);plt.close(fig)
 fig=plt.figure(figsize=(14,10),facecolor='white');ax=fig.add_subplot(111,projection='3d');panel(ax,True,oblique=True,network=True);fig.suptitle('Refined v0.9.33: ICA, compact sinus and tributary joins',fontsize=21,color='#203446');fig.subplots_adjust(left=0,right=1,bottom=.04,top=.95);fig.savefig(RENDERS/'ICA_CS_refinement_detail.png',dpi=155);plt.close(fig)
if __name__=='__main__':main()
