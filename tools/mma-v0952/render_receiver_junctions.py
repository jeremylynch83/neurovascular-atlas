"""Render exact completed receiver triangles, with explicit release status."""
from common import *
import importlib.util,shutil
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('renderer',Path(__file__).resolve().parents[1]/'relationships-v0949/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
preview=WORK/'receiver-preview';preview.mkdir(exist_ok=True)
out=Image.new('RGB',(1340,1550),'#f4f4ef');draw=ImageDraw.Draw(out)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,27);small=ImageFont.truetype(font,17)
draw.text((20,16),'Neurovascular Atlas | shared meningeal receiver junctions',font=title,fill='#172335')
draw.text((20,59),'UNRELEASED. Exact mesh surfaces. Registration and bone relationships still fail acceptance.',font=small,fill='#9c2b2b')
for row,side in enumerate(['right','left']):
    sign=1 if side=='right' else -1;name='vein.meningeal_network.'+side
    mesh=np.load(OUT/('receiver-seam-completed-'+side+'.npz'));mesh['v'].astype('<f4').tofile(preview/(name+'.positions.bin'));mesh['f'].astype('<u4').tofile(preview/(name+'.indices.bin'))
    artery='MMA frontal'+(' left' if side=='left' else '')
    for suffix in ['positions.bin','indices.bin']:shutil.copyfile(OUT/(artery+'.'+suffix),preview/(artery+'.'+suffix))
    for col,extent in enumerate([44.,12.]):
        x=20+col*660;y=108+row*700
        draw.text((x,y),side.capitalize()+' | '+('receiver and paired channels' if col==0 else 'shared wall at the receiver'),font=small,fill='#172335')
        centre=[sign*43,-25,91] if col==0 else [sign*42.5,-25.5,82.5]
        out.paste(mod.render(preview,[name,artery],centre,extent,az=55 if side=='right' else 125,el=10),(x,y+30))
draw.text((20,1510),'Blue: common venous exterior. Red: frontal MMA. The native medial collector openings are retained.',font=small,fill='#354354')
out.save(WORK/'MMA_shared_receiver_junctions.png');print(WORK/'MMA_shared_receiver_junctions.png',flush=True)
