from model import *
from PIL import Image,ImageDraw,ImageFont
import time
SIZE=900
STEMS=['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary']
NAMES=['vein.cavernous.'+s for s in ['right','left']]+['vein.'+t+'.'+s for s in ['right','left'] for t in STEMS]+['vein.anterior_intercavernous','vein.posterior_intercavernous','vein.basilar_plexus']+['ICA '+t+' '+s for s in ['right','left'] for t in ['cavernous','paraophthalmic','petrous']]+['Ophthalmic '+s for s in ['right','left']]+['Meningohypophyseal trunk '+s for s in ['right','left']]+['Inferolateral trunk '+s for s in ['right','left']]
def render(directory,az=35,el=30):
 a,b=np.deg2rad([az,el]);d=np.array([np.cos(a)*np.cos(b),np.sin(a)*np.cos(b),np.sin(b)]);u=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(d,u);centre=np.array([11.,-38.,72.]);scale=SIZE/30
 zbuf=np.full((SIZE,SIZE),-np.inf);rgb=np.empty((SIZE,SIZE,3),np.uint8);rgb[:]=[32,37,48]
 for name in NAMES:
  v=np.fromfile(directory/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(directory/(name+'.indices.bin'),'<u4').reshape(-1,3)
  pd=normals(poly(v,f));ns=vtk_to_numpy(pd.GetPointData().GetNormals());q=v-centre;screen=np.c_[(q@u)*scale+SIZE/2,SIZE/2-(q@up)*scale,q@d];t=screen[f];keep=(t[:,:,0].max(1)>=0)&(t[:,:,0].min(1)<SIZE)&(t[:,:,1].max(1)>=0)&(t[:,:,1].min(1)<SIZE);f=f[keep];t=t[keep];base=np.array([111,149,232] if name.startswith('vein') else [224,171,70],float)
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
 before=render(ROOT.parent/'ica-cs-v0934/exported');after=render(ROOT/'exported');im=Image.new('RGB',(SIZE*2, SIZE+95),'white');im.paste(before,(0,65));im.paste(after,(SIZE,65));dr=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24);dr.text((25,18),'v0.9.34 anterior rim',fill='black',font=font);dr.text((SIZE+25,18),'v0.9.35 revised rim',fill='black',font=font);dr.text((25,SIZE+70),'Depth-buffer render of final exported triangles; same camera and scale.',fill='black',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17));im.save(APP/'review-renders/ICA_CS_rim_repair_depth.png')
