from model import *
from PIL import Image,ImageDraw,ImageFont
import time
SIZE=900
NAMES=['ICA '+t+' right' for t in ['petrous','cavernous','paraophthalmic','posterior communicating','anterior choroidal','terminus']]+[t+' right' for t in ['Ophthalmic','Superior hypophyseal','Meningohypophyseal trunk','Inferolateral trunk','Tentorial marginal','Dorsal meningeal','Inferior hypophyseal','Basal tentorial MHT branch']]
def render(directory,az=0,el=10,side="right"):
 names=[n.rsplit(" ",1)[0]+" "+side for n in NAMES]
 a,b=np.deg2rad([az,el]);d=np.array([np.cos(a)*np.cos(b),np.sin(a)*np.cos(b),np.sin(b)]);u=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(d,u);centre=np.array([12. if side=="right" else -12.,-43.,70.]);scale=SIZE/33
 zbuf=np.full((SIZE,SIZE),-np.inf);rgb=np.empty((SIZE,SIZE,3),np.uint8);rgb[:]=[32,37,48]
 for name in names:
  v=np.fromfile((directory if (directory/(name+'.positions.bin')).exists() else DATA)/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile((directory if (directory/(name+'.indices.bin')).exists() else DATA)/(name+'.indices.bin'),'<u4').reshape(-1,3)
  npth=directory/(name+'.normals.bin');ns=np.fromfile(npth,'<f4').reshape(-1,3) if npth.exists() else vtk_to_numpy(normals(poly(v,f)).GetPointData().GetNormals());q=v-centre;screen=np.c_[(q@u)*scale+SIZE/2,SIZE/2-(q@up)*scale,q@d];t=screen[f];keep=(t[:,:,0].max(1)>=0)&(t[:,:,0].min(1)<SIZE)&(t[:,:,1].max(1)>=0)&(t[:,:,1].min(1)<SIZE);f=f[keep];t=t[keep];base=np.array([111,149,232] if name.startswith('vein') else [220,65,60],float)
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
 (APP/'review-renders').mkdir(exist_ok=True)
 for side in ['right','left']:
  panels=[]
  for az in ([0,40] if side=='right' else [180,140]):
   panels.append((render(DATA,az,10,side),render(OUT,az,10,side)))
  im=Image.new('RGB',(SIZE*2,SIZE*2+100),'white');dr=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
  for row,(before,after) in enumerate(panels):
   y=50+row*(SIZE+50);im.paste(before,(0,y));im.paste(after,(SIZE,y));dr.text((25,y-35),side.title()+' v0.9.38',fill='black',font=font);dr.text((SIZE+25,y-35),side.title()+' v0.9.39',fill='black',font=font)
  im.save(APP/'review-renders'/('ICA_'+side+'_comparison.png'))
