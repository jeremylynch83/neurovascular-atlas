"""Render original and rejected meshes, explicitly labelled as a trial."""
from common import *
import importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('renderer',Path(__file__).resolve().parents[1]/'relationships-v0949/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
out=Image.new('RGB',(1340,1580),'#f4f4ef');d=ImageDraw.Draw(out)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,29);small=ImageFont.truetype(font,19)
d.text((20,18),'Neurovascular Atlas | MMA reconstruction review',font=title,fill='#172335')
d.text((20,66),'REJECTED TRIAL. Exact mesh triangles. This comparison is not an anatomical validation.',font=small,fill='#9c2b2b')
for row,(side,az) in enumerate([('right',0),('left',180)]):
 suffix=' left' if side=='left' else '';sign=-1 if side=='left' else 1
 names=[x+suffix for x in ['Middle meningeal','MMA frontal','MMA frontal anterior division','MMA orbital','MMA posterior convexity']]
 y=110+row*710
 d.text((20,y),side.capitalize()+' | retained v0.9.51 source',font=small,fill='#172335')
 d.text((680,y),side.capitalize()+' | rejected reconstruction',font=small,fill='#9c2b2b')
 for col,directory in enumerate([DATA,OUT]):
  im=mod.render(directory,names,[sign*38,-32,88],140,az=az,el=0);out.paste(im,(20+col*660,y+33))
d.text((20,1535),'46 shared interfaces: 0.000 mm gaps. Trial fails brain contacts and new self-intersections.',font=small,fill='#354354')
out.save(WORK/'MMA_reconstruction_review.png')
