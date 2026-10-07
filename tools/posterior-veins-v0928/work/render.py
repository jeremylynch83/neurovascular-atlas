from common import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
rev=json.loads((OUT/'revision.json').read_text());new=set(rev['newLabels']);arrays={}
for row in rev['changed']:
 k=row['node'];v=np.fromfile(OUT/(k+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(OUT/(k+'.indices.bin'),'<u4').reshape(-1,3);npth=OUT/(k+'.loaded-normals.bin');n=np.fromfile(npth if npth.exists() else OUT/(k+'.normals.bin'),'<f4').reshape(-1,3);arrays[k]=(v,f,n)
context=[]
for k,m in meshes.items():
 if k.startswith('brain.') and any(s in k for s in ['pons.','medulla-oblongata','midbrain.','tonsil-of','upper-cervical','biventral','semilunar','quadrangular','vermis','flocculus.']):
  bins=np.floor(m.v/1.2).astype(np.int32);unique,inv=np.unique(bins,axis=0,return_inverse=True);v=np.zeros((len(unique),3));np.add.at(v,inv,m.v);v/=np.bincount(inv)[:,None];f=inv[m.f];f=f[(f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2])];_,first=np.unique(np.sort(f,axis=1),axis=0,return_index=True);f=f[np.sort(first)];context.append(v[f])
fig=plt.figure(figsize=(18,9),facecolor='#10141c');light=np.array([.4,.6,.7]);light/=np.linalg.norm(light)
for i,(elev,azim,title) in enumerate([(8,90,'Anterior'),(10,0,'Right lateral'),(8,-90,'Posterior')]):
 ax=fig.add_subplot(1,3,i+1,projection='3d');ax.set_facecolor('#10141c')
 for tri in context:ax.add_collection3d(Poly3DCollection(tri,facecolor='#c6cad6',alpha=.10,linewidth=0,edgecolor='none',rasterized=True))
 for k,(v,f,n) in arrays.items():
  if any(s in k for s in ['vein.vertebral','vein.suboccipital','vein.transverse.','vein.cavernous','vein.marginal','vein.basal.','vein.galen']):continue
  normal=n[f].mean(1);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-15);shade=.42+.58*np.maximum(normal@light,0);colour=np.array([.33,.84,.79]) if k in new else np.array([.56,.48,.94]);rgb=np.clip(colour*shade[:,None],0,1);ax.add_collection3d(Poly3DCollection(v[f],facecolors=rgb,linewidth=0,edgecolor='none',rasterized=True))
 ax.set(xlim=(-48,49),ylim=(-145,-48),zlim=(-27,100));ax.set_box_aspect((97,97,127),zoom=1.4);ax.set_proj_type('ortho');ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.set_title(title,color='white',fontsize=18,pad=-3)
fig.suptitle('Posterior fossa venous additions · v0.9.28 review',color='white',fontsize=24);fig.text(.5,.055,'New and relabelled components: teal    Receiving vessels: violet    Neural anatomy: faint grey',ha='center',color='#c9d0dc',fontsize=12);fig.text(.5,.025,'Page 3 P01–P31 · Selected asymmetric routes · Fine regional anatomy and calibres remain illustrative',ha='center',color='#a5aebb',fontsize=11);fig.subplots_adjust(left=0,right=1,bottom=.08,top=.92,wspace=0);fig.savefig(OUT/'posterior-veins-v0.9.28.png',dpi=150,facecolor=fig.get_facecolor());print('Rendered delivered labelled mesh geometry',flush=True)
