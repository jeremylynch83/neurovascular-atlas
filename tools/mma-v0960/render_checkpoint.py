"""Compare exact prior and current posterior cerebral/dural mesh surfaces."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0959'))
from route_tools import *
from PIL import Image,ImageDraw,ImageFont
src=(Path(__file__).parents[1]/'relationships-v0949/render.py').read_text()
start=src.index('base=np.array(');end=src.index('\n  for tri,face',start)
src=src[:start]+"base=np.array([93,140,224] if name.startswith('vein') else [181,151,85] if name.startswith(('brain.tentorium','brain.falx')) else [188,198,207] if name.startswith(('brain.','bone.')) else [222,61,58],float)"+src[end:]
ns={'__name__':'mesh_renderer'};exec(compile(src,'exact_mesh_renderer','exec'),ns)
canvas=Image.new('RGB',(1340,1550),(20,25,34));draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
draw.text((20,18),'Neurovascular Atlas: constrained reference fit v0.9.60',font=font,fill='white')
draw.text((20,57),'Exact mesh comparison. Candidate remains unreleased; unresolved contacts are recorded.',font=small,fill=(202,210,218))
for row,(side,az) in enumerate([('left',180),('right',0)]):
 y=100+row*710;draw.text((20,y),'Posterior cerebral / tentorial reference, '+side,font=font,fill='white')
 names=['brain.occipital-pole.'+side,'brain.lingual-gyrus.'+side,'brain.lateral-occipitotemporal-gyrus.'+side,'brain.inferior-temporal-gyrus.'+side,'brain.tentorium-cerebelli.'+side,'Occipital mastoid–MMA petrosquamosal '+side]
 for col,directory in enumerate([WORK.parent/'work-v0959/candidate',OUT]):
  im=ns['render'](directory,names,[-30 if side=='left' else 31,-119,70],72,az=az,el=0)
  canvas.paste(im,(20+670*col,y+40));draw.text((35+670*col,y+51),'Prior v0.9.59' if col==0 else 'Candidate v0.9.60',font=small,fill='white')
draw.text((20,1520),'Grey: brain. Gold: tentorium. Red: arteries. These views do not establish full anatomical clearance.',font=small,fill=(202,210,218))
dest=Path(sys.argv[2]);dest.parent.mkdir(parents=True,exist_ok=True);canvas.save(dest)
