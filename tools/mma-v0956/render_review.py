"""Exact mesh comparison with the unchanged cerebral reference."""
from clear_neural import *
import importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('exact_renderer',Path(__file__).parents[1]/'relationships-v0949/render.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
fig=Image.new('RGB',(1350,1510),'#f3f5f0');draw=ImageDraw.Draw(fig)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,28);small=ImageFont.truetype(font,17)
draw.text((24,20),'Neurovascular Atlas | MMA geometry review',font=title,fill='#163d35')
draw.text((24,65),'Unreleased reconstruction. Grey: unchanged brain. Red: exact arterial mesh surfaces.',font=small,fill='#53685e')
categories={s['asset']['node']:s['anatomy']['category'] for s in json.loads(Path('public/anatomy/brain-landmarks.json').read_text())['surfaces']}
for row,(side,az) in enumerate([('right',0),('left',180)]):
    names=[n for n in FILES if n.startswith(('MMA ','Middle meningeal')) and n.endswith(' left')==(side=='left')]
    names+=[n for n in FILES if n.endswith('.'+side) and categories.get(n)=='cerebral_cortex']
    y=105+row*690
    for col,directory in enumerate([DATA,OUT]):
        draw.text((24+col*665,y),side.capitalize()+(' | recovered v0.9.51' if col==0 else ' | current candidate'),font=small,fill='#163d35')
        im=renderer.render(directory,names,[0,-61,106],195,az=az,el=0)
        fig.paste(im,(15+col*670,y+28))
draw.text((24,1490),'Exact geometry render. Mesh clearance does not establish anatomical accuracy.',font=small,fill='#79521e')
target=Path('/workspace/scratch/687560554b74/deliverables/MMA_geometry_comparison_v0956.png');fig.save(target);print(target,flush=True)
