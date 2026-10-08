from model import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
RENDERS=APP/'review-renders';RENDERS.mkdir(exist_ok=True)
EXPORT=ROOT/'exported'
STEMS=['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary']
def exported(n):return np.fromfile(EXPORT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(EXPORT/(n+'.indices.bin'),'<u4').reshape(-1,3)
def draw(ax,n,after):
 v,f=exported(n) if after else load(n)
 p=normals(poly(v,f));nv=vtk_to_numpy(p.GetPointData().GetNormals());t=v[f];nn=nv[f].mean(1);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
 col=np.array((.43,.58,.91) if n.startswith('vein') else (.91,.68,.23));cols=col[None,:]*(.5+.5*np.abs(nn@np.array([.5,.2,.84])))[:,None]
 ax.add_collection3d(Poly3DCollection(t,facecolors=cols,edgecolors='none',rasterized=True))
def panel(ax,after,azim=0,elev=0,bilateral=False):
 for s in (['right','left'] if bilateral else ['right']):
  for n in ['ICA cavernous '+s,'ICA paraophthalmic '+s,'Meningohypophyseal trunk '+s,'Inferolateral trunk '+s,'Ophthalmic '+s,'vein.cavernous.'+s]+['vein.'+t+'.'+s for t in STEMS]:draw(ax,n,after)
 for n in ['vein.anterior_intercavernous','vein.posterior_intercavernous','vein.basilar_plexus']:draw(ax,n,after)
 ax.set_xlim(-24 if bilateral else 0,27);ax.set_ylim(-66,-27);ax.set_zlim(50,85);ax.set_box_aspect((51 if bilateral else 27,39,35));ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.set_facecolor('#202530');ax.set_title('v0.9.34 repaired' if after else 'v0.9.33 surface defects',fontsize=16)
for label,kw in [('lateral',{'azim':0}),('oblique',{'azim':25,'elev':18}),('AP',{'azim':90,'bilateral':True})]:
 fig=plt.figure(figsize=(16,9),facecolor='white')
 for i,after in enumerate([False,True]):panel(fig.add_subplot(1,2,i+1,projection='3d'),after,**kw)
 fig.suptitle('Cavernous sinus wall repair: '+label,fontsize=21);fig.text(.1,.03,'Opaque surfaces from exported app meshes. Same camera and scale. Blue: venous wall. Gold: retained arteries.',fontsize=11);fig.subplots_adjust(left=0,right=1,top=.90,bottom=.06,wspace=.03);fig.savefig(RENDERS/('ICA_CS_surface_repair_'+label+'.png'),dpi=130);plt.close(fig)
