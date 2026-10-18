from union_final import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(12,7));centre=np.array([-22.3,-46.2,53.5]);colours=['#6e8ca6','#d78734']
for k in [0,1]:
 ax=fig.add_subplot(1,2,k+1,projection='3d')
 for n,c in zip(NAMES,colours):
  if k:p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3)
  else:p,f=mesh(n)
  t=p[f]-centre;keep=np.all(t.mean(1)>[-5,-2,-5],1)&np.all(t.mean(1)<[6,3,6],1);ax.add_collection3d(Poly3DCollection(t[keep],facecolors=c,edgecolors='#444444',linewidths=.08,alpha=.95))
 n='vein.ovale_emissary.left';p,f=mesh(n);t=p[f]-centre;keep=np.linalg.norm(t.mean(1),axis=1)<6;ax.add_collection3d(Poly3DCollection(t[keep],facecolors='#b7a3c7',alpha=.35,edgecolors='none'))
 ax.set_xlim(-5,6);ax.set_ylim(-2,3);ax.set_zlim(-5,6);ax.set_box_aspect((11,5,11));ax.view_init(18,-102);ax.set_xlabel('X offset (mm)');ax.set_ylabel('Y offset (mm)');ax.set_zlabel('Z offset (mm)');ax.set_title('Baseline: 3.93 mm native opening gap'if not k else'Repaired: 181 paired native boundary edges');ax.tick_params(labelsize=8)
fig.suptitle('Left cavernous MMA native junction, v0.9.91\nBlue: parent. Orange: posterior branch. Purple: ovale emissary vein.',fontsize=13);fig.text(.5,.025,'The reconstructed proximal route clears the emissary vein. Other native rims and the distal branch remain exact.\nThe parent moves by at most 0.15 mm. Wider bone and compartment review remains open.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.08,1,.9]);fig.savefig(D.parent/'cavernous-v0.9.91.png',dpi=150)
