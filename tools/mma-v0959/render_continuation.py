"""Render exact prior and installed mesh buffers for the three retained repairs."""
from route_tools import *
import importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('mesh_render',Path(__file__).parents[1]/'relationships-v0949/render.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
canvas=Image.new('RGB',(1340,2200),(20,25,34));draw=ImageDraw.Draw(canvas);draw.text((20,16),'Neurovascular Atlas: retained v0.9.59 repairs',font=font,fill='white');draw.text((20,53),'Exact mesh renders. Candidate remains unaccepted; six routes remain unresolved.',font=small,fill=(203,210,220))
cases=[('Anterior falcine connection, left',['Anterior falcine–MMA paramedian left','Anterior falcine left','MMA paramedian left','brain.falx-cerebri'],[0,-23,137],60,180,0),('Anterior falcine connection, right',['Anterior falcine–MMA paramedian right','Anterior falcine right','MMA paramedian right','brain.falx-cerebri'],[0,-23,137],60,0,0),('Mastoid to petrosquamosal connection, right',['Occipital mastoid–MMA petrosquamosal right','Occipital mastoid dural branch right','MMA petrosquamosal','brain.tentorium-cerebelli.right'],[47,-105,64],40,30,-65)]
for row,(title,names,centre,extent,az,el) in enumerate(cases):
 y=105+row*685;draw.text((20,y),title,font=font,fill='white')
 for col,directory in enumerate([WORK.parent/'work-v0958/candidate',OUT]):
  im=renderer.render(directory,names,centre,extent,az=az,el=el);canvas.paste(im,(20+col*670,y+32));draw.text((35+col*670,y+45),'Prior v0.9.58' if col==0 else 'Installed v0.9.59',font=small,fill='white')
draw.text((20,2165),'Red: arterial labels. Grey: falx or tentorium. No brain or skull clearance is implied by these views.',font=small,fill=(203,210,220));dest=Path(sys.argv[2]);dest.parent.mkdir(parents=True,exist_ok=True);canvas.save(dest)
