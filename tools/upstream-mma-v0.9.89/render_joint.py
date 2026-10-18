from union_candidate import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
fig=plt.figure(figsize=(12,9));fig.patch.set_facecolor('#f8f7f3')
for row,side in enumerate(['left','right']):
 names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];v,f=mesh(names[1]);rr=max(rims(v,f),key=lambda r:abs(v[r,0].mean()));centre=v[rr].mean(0)
 for col in [0,1]:
  ax=fig.add_subplot(2,2,row*2+col+1,projection='3d');parts=[]
  for i,n in enumerate(names):
   if col==0:p,g=mesh(n)
   else:p=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3)
   parts.append((p,g));t=p[g]-centre;mask=np.linalg.norm(t.mean(1),axis=1)<1.8;ax.add_collection3d(Poly3DCollection(t[mask],facecolors=['#a4aab0','#df8d35'][i],edgecolors='#555555'if col else 'none',linewidths=.10,alpha=.95))
  if col:
   p,g=parts[0];q,h=parts[1];shared=set(map(tuple,p))&set(map(tuple,q));u,e,c=boundary(p,g);segments=np.array([[u[a]-centre,u[b]-centre]for(a,b),cnt in zip(e,c)if cnt==1 and tuple(u[a])in shared and tuple(u[b])in shared]);ax.add_collection3d(Line3DCollection(segments,colors='#008c62',linewidths=2.0));title='After: open native junction'
  else:title='Before: overlapping vessel walls'
  ax.set_title(side.capitalize()+' | '+title,fontsize=11);ax.set_xlim(-1.4,1.4);ax.set_ylim(-1.4,1.4);ax.set_zlim(-1.4,1.4);ax.set_box_aspect((1,1,1));ax.view_init(25,135 if side=='left'else 45);ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.set_zlabel('Z (mm)');ax.tick_params(labelsize=7)
fig.suptitle('Frontal MMA to paramedian branch: local native junctions\nGrey: frontal MMA. Orange: paramedian branch. Green: exact shared opening.',fontsize=13);fig.text(.5,.025,'Coordinates shown relative to the original branch inlet. Local external-wall projections do not certify the full network.\nThe parent distal tips and all other labelled attachment coordinates are retained.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.06,1,.92]);fig.savefig(D.parent/'upstream-mma-v0.9.89.png',dpi=150)
