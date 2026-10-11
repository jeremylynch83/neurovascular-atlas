from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
guides=json.loads((WORK/'mma-guides.json').read_text())
fig,axs=plt.subplots(2,2,figsize=(12,12))
for ax,z in zip(axs.flat,[55,75,100,140]):
 for n in FILES:
  if n.startswith('bone.') or n.startswith('brain.'):
   v,f=load(n)
   if v[:,2].min()>z or v[:,2].max()<z:continue
   p=section(v,f,2,z)
   if len(p):ax.scatter(p[:,0],p[:,1],s=1,c='#555555' if n.startswith('bone.') else '#d69b77',alpha=.7)
 for g in guides:
  q=np.array(g['points']);old=np.array(g['oldPoints']);near=np.abs(q[:,2]-z)<1
  ax.scatter(q[near,0],q[near,1],s=12,c='red');near=np.abs(old[:,2]-z)<1;ax.scatter(old[near,0],old[near,1],s=10,c='blue')
 ax.set_aspect('equal');ax.set_title('z = '+str(z)+' mm');ax.grid(alpha=.2)
fig.suptitle('Bone grey, brain tan, source guide blue, trial guide red')
fig.savefig(WORK/'corridor-sections.png',dpi=160)
