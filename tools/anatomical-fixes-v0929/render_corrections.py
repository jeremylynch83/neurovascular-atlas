from geometry import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb
APP=Path(__file__).resolve().parents[2];OUT=APP/'docs/validation';C=ROOT/'candidate';revision=json.loads((C/'revision.json').read_text());changed={r['node'] for r in revision['changed']}
def add(ax,n,c,after=False,alpha=1,crop=None):
 m=meshes[n]
 if after and n in changed:v=np.fromfile(C/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(C/(n+'.indices.bin'),'<u4').reshape(-1,3)
 else:v=m.v;f=m.f
 if crop:
  lo,hi=np.array(crop);f=f[np.all(v[f].mean(1)>=lo,1)&np.all(v[f].mean(1)<=hi,1)]
 tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-9);shade=.62+.38*np.abs(normal@np.array([.5,.5,.707]));col=np.array(to_rgb(c))*shade[:,None]
 ax.add_collection3d(Poly3DCollection(tri,facecolors=col,edgecolor='none',alpha=alpha,linewidth=0,rasterized=True))
def setup(ax,limits,view):
 ax.set(xlim=limits[0],ylim=limits[1],zlim=limits[2]);ax.set_box_aspect([b-a for a,b in limits]);ax.view_init(*view);ax.set_proj_type('ortho');ax.set_axis_off()
def save(fig,file,caption,legend):
 fig.legend(handles=[Patch(facecolor=c,label=t) for c,t in legend],loc='lower center',bbox_to_anchor=(.5,.04),ncol=3,frameon=False,fontsize=10);fig.text(.5,.015,caption,ha='center',fontsize=9,color='#454545');fig.subplots_adjust(left=0,right=1,bottom=.16,top=.89,wspace=0);fig.savefig(OUT/file,dpi=160,bbox_inches='tight',facecolor='white');plt.close(fig)
fig=plt.figure(figsize=(11,6));arts=['PCA P1 right','PCA P2-P3 right','Posterior communicating right','Thalamoperforator 2 right','PCA long circumflex right','PCA short circumflex right'];veins=['vein.lateral_mesencephalic.right','vein.posterior_communicating','vein.cerebral_peduncular.right']
for i,after in enumerate([False,True]):
 ax=fig.add_subplot(1,2,i+1,projection='3d')
 for n in arts:add(ax,n,'#b93543',after)
 for n in veins:add(ax,n,'#226ba8',after)
 setup(ax,[(-1,20),(-69,-46),(69,87)],(18,100));ax.set_title('v0.9.28 baseline' if not after else 'v0.9.29 accepted local overpass',fontsize=13)
fig.suptitle('Five audited crossing pairs cleared in the right mesencephalic region',fontsize=15)
save(fig,'anatomical-overpass-v0.9.29.png','Exact checked mesh surfaces. Seven other audited crossing pairs remain open.',[('#b93543','Arteries'),('#226ba8','Veins')])
fig=plt.figure(figsize=(11,6))
for i,after in enumerate([False,True]):
 ax=fig.add_subplot(1,2,i+1,projection='3d')
 add(ax,'vein.cavernous.right','#a1bed4',after,.28)
 for n,c in [('ICA petrous right','#db8b32'),('ICA cavernous right','#bd3443'),('ICA paraophthalmic right','#7653ad'),('Ophthalmic right','#008b7e')]:add(ax,n,c,after)
 setup(ax,[(2,23),(-61,-25),(38,84)],(5,0));ax.set_title('v0.9.28 labels' if not after else 'v0.9.29 labels',fontsize=13)
fig.suptitle('ICA surface preserved; NYU segment partition corrected provisionally',fontsize=15)
save(fig,'anatomical-ica-partition-v0.9.29.png','Boundary uses the existing estimated proximal dural-ring reference. No ring surface is segmented.',[('#bd3443','Cavernous label'),('#7653ad','Paraophthalmic label'),('#a1bed4','Cavernous sinus')])
print('Rendered two before / after evidence images')
