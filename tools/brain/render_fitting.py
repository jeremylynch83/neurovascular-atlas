"""Matched views of exported first-batch vessel fitting and registered context."""
from pathlib import Path
import json,argparse
import numpy as np,trimesh,vtk
from PIL import Image,ImageDraw,ImageFont
from build_targets import poly
APP=Path(__file__).resolve().parents[2];DEST=APP/'docs/validation';brains={state:trimesh.load(path,process=False) for state,path in [('baseline',APP/'.authoring/brain-baseline.glb'),('fitted',APP/'public/anatomy/models/brain-context.glb')]}

def actor(m,colour,opacity=1):
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly(m));mapper.ScalarVisibilityOff();a=vtk.vtkActor();a.SetMapper(mapper);a.GetProperty().SetColor(*colour);a.GetProperty().SetOpacity(opacity);return a

def render(items,path,view,centre,scale):
 ren=vtk.vtkRenderer();ren.SetBackground(.98,.98,.98);win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(750,560);win.SetMultiSamples(0);win.AddRenderer(ren)
 for item in items:ren.AddActor(item)
 c=ren.GetActiveCamera();c.SetPosition(*(np.array(centre)+np.array(view)*500));c.SetFocalPoint(*centre);c.SetViewUp(*( (0,1,0) if abs(view[2])>.9 else (0,0,1)));c.ParallelProjectionOn();c.SetParallelScale(scale);ren.ResetCameraClippingRange();win.Render();im=vtk.vtkWindowToImageFilter();im.SetInput(win);im.Update();w=vtk.vtkPNGWriter();w.SetInputConnection(im.GetOutputPort());w.SetFileName(str(path));w.Write();win.Finalize()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--rejected-trial',action='store_true');args=parser.parse_args();prefix='trial' if args.rejected_trial else 'fitting'
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
 for region in (['central'] if args.rejected_trial else ['dural','stem','central']):
  if region=='dural':
   targets=['brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right','brain.corpus-callosum'];labels=['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence','vein.internal_cerebral.left','vein.internal_cerebral.right','vein.basal.left','vein.basal.right','vein.precentral_cerebellar'];asset='veins';centre=(0,-105,98);scale=65;views=[(-1,0,0),(.8,1,.4)]
  elif region=='stem':
   targets=[f'brain.{k}.{s}' for k in ['pons','midbrain','medulla-oblongata','base-of-peduncle','superior-cerebellar-peduncle'] for s in ['left','right']];labels=['vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']+[f'vein.{k}.{s}' for k in ['lateral_mesencephalic','transverse_pontine','pontomedullary','superior_petrosal_vein','basal'] for s in ['left','right']];asset='veins';centre=(0,-70,57);scale=46;views=[(0,1,0),(1,0,0)]
  else:
   targets=[f'brain.{k}.{s}' for k in ['central-sulcus','precentral-gyrus','postcentral-gyrus'] for s in ['left','right']];labels=['Central right','Central left','MCA superior division right','MCA superior division left','Central cortical branch right','Central cortical branch left','Central distal ramus right','Central distal ramus left'];asset='arteries';centre=(0,-74,133);scale=64;views=[(1,0,0),(-1,0,0),(0,0,1),(.8,1,.7)]
  canvas=Image.new('RGB',(1500,640*len(views)),'white');draw=ImageDraw.Draw(canvas)
  for vi,view in enumerate(views):
   for si,state in enumerate(['baseline','fitted']):
    scene=trimesh.load(APP/(f'.authoring/{asset}-rejected.glb' if args.rejected_trial and state=='fitted' else f'.authoring/{asset}-{state}.glb'),process=False)
    items=[actor(brains[state].geometry[k],(.3,.55,.35) if 'central-sulcus' in k else (.7,.67,.6),.25 if 'central-sulcus' in k else (.32 if region=='dural' else (1 if region=='central' and vi==3 else .6))) for k in targets]
    items += [actor(scene.geometry[k],(.08,.32,.72) if asset=='veins' else ((.5,.45,.45) if k.endswith('right') else (.8,.1,.12))) for k in labels if k in scene.geometry]
    path=DEST/f'{prefix}-{region}-{state}-{vi}-v0.9.17.png';render(items,path,view,centre,scale)
    x=si*750;y=vi*640
    view_label=['Right lateral','Left lateral','Superior','Oblique, opaque'][vi] if region=='central' else ['View 1','View 2'][vi]
    draw.text((x+15,y+10),('Baseline v0.9.15' if si==0 else ('Rejected left trial' if args.rejected_trial else 'Checkpoint v0.9.17'))+' | '+view_label,font=font,fill='#30343a')
    caption='Red: left trial | Grey: right retained | Green: sulcal reference' if region=='central' else region.capitalize()+': geometry retained'
    draw.text((x+15,y+36),caption,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18),fill='#515861')
    canvas.paste(Image.open(path).convert('RGB'),(x,y+70))
  canvas.save(DEST/f'{prefix}-{region}-comparison-v0.9.17.png');print(region,flush=True)
if __name__=='__main__':main()
