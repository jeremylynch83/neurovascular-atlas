from common import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
rev=json.loads((OUT/'revision.json').read_text());new=set(rev['newLabels']);arrays={}
for row in rev['changed']:
 k=row['node'];v=np.fromfile(OUT/(k+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(OUT/(k+'.indices.bin'),'<u4').reshape(-1,3);n=np.fromfile(OUT/(k+'.loaded-normals.bin'),'<f4').reshape(-1,3);arrays[k]=(v,f,n)
fig=plt.figure(figsize=(18,8),facecolor='#10141c');light=np.array([.4,.6,.7]);light/=np.linalg.norm(light)
for i,(elev,azim,title) in enumerate([(8,90,'Anterior'),(10,0,'Right lateral'),(85,90,'Superior')]):
 ax=fig.add_subplot(1,3,i+1,projection='3d');ax.set_facecolor('#10141c')
 for k in ['brain.lateral-ventricle.right','brain.lateral-ventricle.left','brain.third-ventricle','brain.thalamus.right','brain.thalamus.left','brain.hippocampus.right','brain.hippocampus.left']:
  m=meshes[k];tri=m.v[m.f];coll=Poly3DCollection(tri,facecolor='#c6cad6',alpha=.10,linewidth=0,edgecolor='none',rasterized=True);ax.add_collection3d(coll)
 for k,(v,f,n) in arrays.items():
  normal=n[f].mean(1);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-15);shade=.42+.58*np.maximum(normal@light,0);colour=np.array([.33,.84,.79]) if k in new else np.array([.56,.48,.94]);rgb=np.clip(colour*shade[:,None],0,1);coll=Poly3DCollection(v[f],facecolors=rgb,linewidth=0,edgecolor='none',rasterized=True);ax.add_collection3d(coll)
 ax.set(xlim=(-48,49),ylim=(-144,6),zlim=(67,139));ax.set_box_aspect((97,150,72),zoom=1.15);ax.set_proj_type('ortho');ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.set_title(title,color='white',fontsize=18,pad=-3)
fig.suptitle('Deep venous additions · v0.9.27 review',color='white',fontsize=24);fig.text(.5,.045,'New veins: teal    Existing receiving veins: violet    Ventricles, thalamus and hippocampus: faint grey',ha='center',color='#c9d0dc',fontsize=12);fig.text(.5,.015,'22 families · 44 side-specific labels · Representative fine tributaries; transmedullary veins excluded',ha='center',color='#a5aebb',fontsize=11);fig.subplots_adjust(left=0,right=1,bottom=.06,top=.92,wspace=0);fig.savefig(OUT/'deep-veins-v0.9.27.png',dpi=150,facecolor=fig.get_facecolor());print('Rendered exact delivered skins/normals',flush=True)
