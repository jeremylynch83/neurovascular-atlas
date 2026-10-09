from common import *
from PIL import Image
SIZE=650
def render(directory,names,centre,extent,az=90,el=0,clip=None):
 a,b=np.deg2rad([az,el]);d=np.array([np.cos(a)*np.cos(b),np.sin(a)*np.cos(b),np.sin(b)]);u=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(d,u);centre=np.array(centre);scale=SIZE/extent
 zbuf=np.full((SIZE,SIZE),-np.inf);rgb=np.empty((SIZE,SIZE,3),np.uint8);rgb[:]=[32,37,48]
 for name in names:
  v=np.fromfile((directory if (directory/(name+'.positions.bin')).exists() else DATA)/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile((directory if (directory/(name+'.indices.bin')).exists() else DATA)/(name+'.indices.bin'),'<u4').reshape(-1,3)
  ns=normals(v,f);
  if clip:f=f[clip(v[f].mean(1))]
  q=v-centre;screen=np.c_[(q@u)*scale+SIZE/2,SIZE/2-(q@up)*scale,q@d];t=screen[f];keep=(t[:,:,0].max(1)>=0)&(t[:,:,0].min(1)<SIZE)&(t[:,:,1].max(1)>=0)&(t[:,:,1].min(1)<SIZE);f=f[keep];t=t[keep];base=np.array([111,149,232] if name.startswith('vein') else ([186,186,176] if name.startswith(('brain.','bone.')) else [220,65,60]),float)
  for tri,face in zip(t,f):
   xx=tri[:,0];yy=tri[:,1];den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
   if abs(den)<1e-7:continue
   x0=max(0,int(np.floor(xx.min())));x1=min(SIZE-1,int(np.ceil(xx.max())));y0=max(0,int(np.floor(yy.min())));y1=min(SIZE-1,int(np.ceil(yy.max())))
   X,Y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
   w0=((yy[1]-yy[2])*(X-xx[2])+(xx[2]-xx[1])*(Y-yy[2]))/den;w1=((yy[2]-yy[0])*(X-xx[2])+(xx[0]-xx[2])*(Y-yy[2]))/den;w2=1-w0-w1
   inside=(w0>=-1e-7)&(w1>=-1e-7)&(w2>=-1e-7);depth=w0*tri[0,2]+w1*tri[1,2]+w2*tri[2,2];zb=zbuf[y0:y1+1,x0:x1+1];draw=inside&(depth>zb)
   if not draw.any():continue
   nn=w0[...,None]*ns[face[0]]+w1[...,None]*ns[face[1]]+w2[...,None]*ns[face[2]];nn/=np.maximum(np.linalg.norm(nn,axis=2)[...,None],1e-12)
   light=np.array([.25,.45,.85]);shade=.45+.55*np.abs(nn@light);col=np.minimum(base[None,None,:]*shade[...,None],255).astype(np.uint8);zb[draw]=depth[draw];rgb[y0:y1+1,x0:x1+1][draw]=col[draw]
 print('Rendered',names,flush=True);return Image.fromarray(rgb)

if __name__=='__main__':
 render(DATA,['bone.temporal.right','Labyrinthine right','AICA right'],[30,-70,52],45,az=-145,el=20).save(WORK/'temporal-inner.png')
 render(DATA,['bone.occipital','Hypoglossal branch','vein.anterior_condylar.right'],[18,-73,31],37,az=15,el=0,clip=lambda q:(q[:,0]<36)&(q[:,1]>-87)&(q[:,2]<53)).save(WORK/'condylar-inner.png')
