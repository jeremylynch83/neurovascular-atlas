"""Matched views of the resumed context solve, with fixed clival veins."""
import numpy as np,trimesh,vtk
from PIL import Image,ImageDraw,ImageFont
from fit_vessels import APP
from render_advanced_trial import actor,render
W=APP/'.authoring/brainstem20-optimised'
bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
canvas=Image.new('RGB',(1500,1920),'white');draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
for j,view in enumerate([(1,0,0),(0,1,0),(.8,.7,.35)]):
 for i,state in enumerate(['baseline','trial']):
  brain=trimesh.load(APP/'.authoring/brainstem19/brain-baseline.glb' if state=='baseline' else W/'brain-trial.glb',process=False)
  labels=[k for k in brain.geometry if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle','tonsil-of-cerebellum','uvula','pyramis','tuber-of'])]
  items=[actor(brain.geometry[k],(.75,.7,.6),.9 if 'pons' in k or 'midbrain' in k else .6) for k in labels]
  items += [actor(m,(.4,.65,.8),.2) for k,m in bones.geometry.items() if k in ['bone.occipital','bone.sphenoid']]
  items += [actor(veins.geometry['vein.basilar_plexus'],(.05,.25,.75))]
  path=W/f'context-{state}-{j}.png';render(items,path,view,(0,-80,52),50);canvas.paste(Image.open(path),(i*750,j*640+45));draw.text((i*750+15,j*640+10),'v0.9.18 baseline' if i==0 else 'Continued trial: volume constrained',fill='black',font=font)
canvas.save(W/'context-comparison.png')
