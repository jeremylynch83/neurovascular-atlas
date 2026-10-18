import sys,numpy as np
from pathlib import Path
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0,str(Path(__file__).parent));from explore import load
W=Path(sys.argv[1]);A=Path(sys.argv[2]);fig,axes=plt.subplots(2,2,figsize=(12,10));fig.patch.set_facecolor('#f6f6f3')
names=['MMA paramedian left','MMA paramedian right','MMA falcine terminal left','MMA falcine terminal right'];ss,sf=load('vein.superior_sagittal')
for col,title in enumerate(['Before: separated attachments and sinus overlap','After: joined routes below the sinus']):
 for row,(dims,limits,label)in enumerate([([0,2],[[-6,6],[145,166]],'Coronal projection (X / Z)'),([1,2],[[-59,-42],[145,166]],'Sagittal projection (Y / Z)')]):
  ax=axes[row,col];t=ss[sf];mask=(t[:,:,1].max(1)>-59)&(t[:,:,1].min(1)<-42)&(t[:,:,2].max(1)>145)&(t[:,:,2].min(1)<167);ax.add_collection(PolyCollection(t[mask][:,:,dims],facecolors='#5398c2',edgecolors='none',alpha=.22))
  for n in names:
   if col==0:v,f=load(n)
   else:v=np.fromfile(W/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(W/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3)
   t=v[f];mask=(t[:,:,0].max(1)>-6)&(t[:,:,0].min(1)<6)&(t[:,:,1].max(1)>-59)&(t[:,:,1].min(1)<-42)&(t[:,:,2].max(1)>145)&(t[:,:,2].min(1)<166);ax.add_collection(PolyCollection(t[mask][:,:,dims],facecolors='#b22930'if'paramedian'in n else'#e59b36',edgecolors='none',alpha=.85))
  ax.set_xlim(limits[0]);ax.set_ylim(limits[1]);ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_xlabel('RAS '+('X'if row==0 else'Y')+' (mm)');ax.set_ylabel('RAS Z (mm)');ax.set_title((title+'\n'if row==0 else'')+label,fontsize=10)
fig.suptitle('Bilateral MMA / falcine attachment reconstruction\nRed: paramedian MMA. Orange: falcine terminal. Blue: superior sagittal sinus.',fontsize=13)
fig.text(.5,.018,'Orthographic projections of exported triangles. Projection overlaps can occur despite 3D separation.\nThe 3D checks find no sinus contacts or sampled vertices inside the closed sinus proxy.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.065,1,.92]);fig.savefig(A/'docs/validation/mma-falcine-v0.9.88.png',dpi=150);plt.close(fig)
