from common import *
from PIL import Image,ImageDraw,ImageFont
import time
SIZE=720
NAMES=MEDIAN+[r['name'] for r in META if r['name'].startswith(('vein.transverse_pontine','vein.pontomedullary','vein.pontomesencephalic_sulcus','vein.lateral_anterior_pontomesencephalic','vein.transverse_medullary','vein.prepontine_bridge'))]+['Basilar','Vertebral V4 right','Vertebral V4 left','Anterior spinal','AICA right','AICA left','SCA right','SCA left','PCA P1 right','PCA P1 left','Anterior spinal root right','Anterior spinal root left']
if '--context' in sys.argv:
 NAMES += ['brain.pons.left','brain.pons.right','brain.medulla-oblongata.left','brain.medulla-oblongata.right','brain.midbrain.left','brain.midbrain.right']
def render(directory,az=90,el=0):
 a,b=np.deg2rad([az,el]);d=np.array([np.cos(a)*np.cos(b),np.sin(a)*np.cos(b),np.sin(b)]);u=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(d,u);centre=np.array([0.,-67.,48.]);scale=SIZE/66
 zbuf=np.full((SIZE,SIZE),-np.inf);rgb=np.empty((SIZE,SIZE,3),np.uint8);rgb[:]=[32,37,48]
 for name in NAMES:
  v=np.fromfile((directory if (directory/(name+'.positions.bin')).exists() else DATA)/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile((directory if (directory/(name+'.indices.bin')).exists() else DATA)/(name+'.indices.bin'),'<u4').reshape(-1,3)
  ns=normals(v,f);q=v-centre;screen=np.c_[(q@u)*scale+SIZE/2,SIZE/2-(q@up)*scale,q@d];t=screen[f];keep=(t[:,:,0].max(1)>=0)&(t[:,:,0].min(1)<SIZE)&(t[:,:,1].max(1)>=0)&(t[:,:,1].min(1)<SIZE);f=f[keep];t=t[keep];base=np.array([111,149,232] if name.startswith('vein') else ([186,186,176] if name.startswith('brain.') else [220,65,60]),float)
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
 print('Rendered',directory,flush=True);return Image.fromarray(rgb)
if __name__=='__main__':
 before=render(DATA);after=render(OUT);im=Image.new('RGB',(SIZE*2,SIZE+65),'white');im.paste(before,(0,65));im.paste(after,(SIZE,65));dr=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);dr.text((25,18),'v0.9.45: anterior view',fill='black',font=font);dr.text((SIZE+25,18),'v0.9.46: anterior view',fill='black',font=font);im.save(WORK/('anterior-context-comparison.png' if '--context' in sys.argv else 'anterior-comparison.png'))
 before=render(DATA,az=20);after=render(OUT,az=20);im=Image.new('RGB',(SIZE*2,SIZE+65),'white');im.paste(before,(0,65));im.paste(after,(SIZE,65));dr=ImageDraw.Draw(im);dr.text((25,18),'v0.9.45: oblique view',fill='black',font=font);dr.text((SIZE+25,18),'v0.9.46: oblique view',fill='black',font=font);im.save(WORK/('oblique-context-comparison.png' if '--context' in sys.argv else 'oblique-comparison.png'))
