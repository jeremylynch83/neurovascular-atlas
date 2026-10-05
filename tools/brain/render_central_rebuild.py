"""Matched close views of the central branch reconstruction and atlas surfaces."""
import numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
from fit_vessels import APP
from render_advanced_trial import actor,render

def main():
 brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False)
 scenes=[trimesh.load(APP/'.authoring/arteries-baseline.glb',process=False),trimesh.load(APP/'.authoring/central-rebuilt-trial.glb',process=False)]
 dest=APP/'docs/validation';font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
 views=[('left',(-1,.1,.2),'Left oblique'),('right',(1,.1,.2),'Right oblique'),('left',(0,0,1),'Left superior'),('right',(0,0,1),'Right superior')]
 canvas=Image.new('RGB',(1500,640*len(views)),'white');draw=ImageDraw.Draw(canvas)
 for vi,(side,view,title) in enumerate(views):
  sign=-1 if side=='left' else 1;centre=(sign*35,-89,139);scale=30
  for si,scene in enumerate(scenes):
   items=[actor(brain.geometry[f'brain.{label}.{side}'],(.72,.7,.65),.28 if vi<2 else .85) for label in ['precentral-gyrus','postcentral-gyrus','superior-parietal-lobule','supramarginal-gyrus','superior-frontal-gyrus']]
   items+=[actor(scene.geometry[f'{label} {side}'],(.82,.12,.14)) for label in ['Central','Central cortical branch','Central distal ramus','MCA superior division']]
   path=dest/f'central-rebuilt-{side}-{vi}-{si}-v0.9.18.png';render(items,path,view,centre,scale)
   x,y=si*750,vi*640;draw.text((x+15,y+10),title+': '+('Baseline v0.9.15' if si==0 else 'Applied atlas fit v0.9.18'),font=font,fill='#30343a');canvas.paste(Image.open(path).convert('RGB'),(x,y+38))
 canvas.save(dest/'central-rebuilt-comparison-v0.9.18.png')
 print('Rendered matched central-family views.',flush=True)
if __name__=='__main__':main()
