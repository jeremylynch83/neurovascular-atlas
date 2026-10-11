"""CPU rendering of the exact triangles. No OpenGL is required."""
from common import *
from software_renderer import render
from PIL import Image,ImageDraw,ImageFont
page=Image.new('RGB',(1340,1530),'#f5f6f7');draw=ImageDraw.Draw(page);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
draw.text((20,14),'Neurovascular Atlas: fresh MMA tree and paired-vein trial',fill='#172335',font=font)
draw.text((20,54),'REJECTED CANDIDATE. Actual mesh triangles; context is a faint overlay.',fill='#aa2626',font=small)
for row,side in enumerate(['right','left']):
 sign=1 if side=='right' else -1;suffix=' left' if side=='left' else '';centre=[sign*34,-30,93];az=0 if side=='right' else 180;y=90+row*695
 context=render(DATA,['bone.sphenoid','bone.temporal.'+side,'bone.parietal.'+side,'bone.frontal'],centre,140,az=az)
 ghost=Image.blend(Image.new('RGB',context.size,(32,37,48)),context,.24)
 for col,after in enumerate([False,True]):
  names=[base+suffix for base in ['Middle meningeal','MMA frontal','MMA frontal anterior division','MMA frontal posterior division','MMA orbital','MMA posterior convexity']]
  if after:names.append('vein.middle_meningeal.'+side)
  im=render(OUT if after else DATA,names,centre,140,az=az);ar=np.array(im);mask=np.any(ar!=[32,37,48],axis=2);out=np.array(ghost);out[mask]=ar[mask]
  draw.text((20+col*660,y),side.capitalize()+(' | fresh candidate' if after else ' | accepted v0.9.51'),fill='#172335',font=small);page.paste(Image.fromarray(out),(20+col*660,y+28))
draw.text((20,1497),'Red: arteries. Blue: paired veins. Trial fails acceptance and is not an installable release.',fill='#172335',font=small);page.save(WORK/'MMA_v0953_comparison.png')
