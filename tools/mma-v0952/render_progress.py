"""Software rasterisation of exact retained and provisional mesh triangles."""
from common import *
import importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('renderer',Path(__file__).resolve().parents[1]/'relationships-v0949/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
out=Image.new('RGB',(1340,1595),'#f4f4ef');draw=ImageDraw.Draw(out)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,28);small=ImageFont.truetype(font,17)
draw.text((20,16),'Neurovascular Atlas | MMA reconstruction progress',font=title,fill='#172335')
draw.text((20,59),'UNRELEASED CANDIDATE. Geometry gates fail. These views are not anatomical validation.',font=small,fill='#9c2b2b')
for row,(side,az) in enumerate([('right',0),('left',180)]):
 suffix=' left' if side=='left' else '';sign=1 if side=='right' else -1
 base=[n+suffix for n in ['Middle meningeal','MMA frontal','MMA frontal anterior division','MMA posterior convexity','MMA petrosquamosal']]
 for col,candidate in enumerate([False,True]):
  names=base+(['vein.middle_meningeal.'+n+'.'+side for n in ['anterior','posterior']]+['vein.sphenoparietal.'+side] if candidate else [])
  x=20+col*660;y=102+row*720
  draw.text((x,y),side.capitalize()+' | '+('provisional reconstruction and paired veins' if candidate else 'retained v0.9.51 source'),font=small,fill='#9c2b2b' if candidate else '#172335')
  out.paste(mod.render(OUT if candidate else DATA,names,[sign*38,-47,91],155,az=az,el=0),(x,y+32))
draw.text((20,1555),'Isolated vessels. Bone canals and full anatomical relationships are not certified by these views.',font=small,fill='#354354')
out.save(WORK/'MMA_reconstruction_progress.png')
print(WORK/'MMA_reconstruction_progress.png',flush=True)
