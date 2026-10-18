from repair import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
r=json.load(open(D.parent/'native-validation.json'))['correction'];v,f=mesh(r['node']);w,g=mesh(r['parent']);p=np.fromfile(OUT/(r['node']+'.positions.bin'),'<f4').reshape(-1,3);src=np.array(r['sourceRim']);dst=np.array(r['parentRim']);centre=w[dst].mean(0);a=w[dst]-centre;_,_,axes=np.linalg.svd(a);basis=np.vstack([axes[0],axes[1],axes[2]]);fig=plt.figure(figsize=(11,6));fig.patch.set_facecolor('#f8f7f3')
for col in [0,1]:
 ax=fig.add_subplot(1,2,col+1,projection='3d')
 for vertices,faces,colour in [(w,g,'#a1a7af'),(v if col==0 else p,f,'#df8d35')]:
  t=(vertices[faces]-centre)@basis.T;mask=np.linalg.norm(t.mean(1),axis=1)<1.5;ax.add_collection3d(Poly3DCollection(t[mask],facecolors=colour,edgecolors='#444444',linewidths=.12,alpha=.95))
 line=((v[src]if col==0 else p[src])-centre)@basis.T;line=np.vstack([line,line[0]]);ax.plot(*line.T,color='#b15c05'if col==0 else'#008c62',lw=2)
 ax.set_title('Before: separated native rims'if col==0 else'After: 124 exact shared rim coordinates',fontsize=11);ax.set_xlim(-1.1,1.1);ax.set_ylim(-1.1,1.1);ax.set_zlim(-1.1,1.1);ax.set_box_aspect((1,1,1));ax.view_init(23,135);ax.set_xlabel('Local U (mm)');ax.set_ylabel('Local V (mm)');ax.set_zlabel('Normal (mm)');ax.tick_params(labelsize=7)
fig.suptitle('Left MMA petrosquamosal native attachment\nGrey: middle meningeal parent. Orange: petrosquamosal branch.',fontsize=13);fig.text(.5,.025,'Only 294 vertices move, by at most 0.413 mm. All indices and the other 281 native rim coordinates are retained.\nA local shared opening does not certify the complete tentorial/mastoid network.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.08,1,.9]);fig.savefig(D.parent/'petrosquamosal-v0.9.90.png',dpi=150)
