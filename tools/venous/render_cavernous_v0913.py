"""Matched-camera renders of the delivered GLBs, plus sectional verification."""
import sys,json,io,os
from pathlib import Path
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk
from PIL import Image,ImageDraw,ImageFont,ImageOps
from refine_cavernous import read_glb,accessor,whole_veins
from reference import APP,ROOT,poly,records,arrays
OUT=ROOT/'review-v0.9.13';OUT.mkdir(exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(F,n)
def atomic_png_bytes(data,path):
 temp=path.with_suffix('.tmp')
 with temp.open('wb') as stream:
  for start in range(0,len(data),1024*1024):stream.write(data[start:start+1024*1024])
  stream.flush();os.fsync(stream.fileno())
 temp.replace(path)
 with Image.open(path) as check:check.load()
def atomic_save(im,path):
 data=io.BytesIO();im.save(data,format='PNG');atomic_png_bytes(data.getvalue(),path)

def glbparts(path):
 doc,b=read_glb(path);out=[]
 for node in doc['nodes']:
  if 'mesh' not in node:continue
  prim=doc['meshes'][node['mesh']]['primitives'][0]
  p=accessor(doc,b,prim['attributes']['POSITION']).copy()
  f=accessor(doc,b,prim['indices']).reshape(-1,3).copy()
  nn=accessor(doc,b,prim['attributes']['NORMAL']).copy();out.append((node['name'],p,f,nn))
 return out
bones=[(r['name'],poly(*arrays(r))) for r in records if r['name'] in ['bone.sphenoid','bone.temporal.right','bone.temporal.left']]
models={}
for label,v,a in [('before','.authoring/venous/baseline-v0.9.12/venous-raw.glb','.authoring/venous/baseline-v0.9.12/circulation-refined.glb'),('after','.authoring/venous/venous-raw.glb','.authoring/circulation-refined.glb')]:
 vp=glbparts(APP/v);ap=glbparts(APP/a)
 ven=[]
 for name,p,f,nn in vp:
  main=name in ['vein.cavernous.right','vein.cavernous.left','vein.anterior_intercavernous','vein.posterior_intercavernous','vein.sphenoparietal.right','vein.sphenoparietal.left','vein.superficial_middle_cerebral.right','vein.superficial_middle_cerebral.left','vein.superior_ophthalmic.right','vein.superior_ophthalmic.left','vein.ovale_emissary.right','vein.ovale_emissary.left']
  if not main:
   c=p[f].mean(1);keep=(abs(c[:,0]-.65)<25)&(c[:,1]>-59)&(c[:,1]<-28)&(c[:,2]>46)&(c[:,2]<81)
   f=f[keep]
   if not len(f):continue
  pd=poly(p,f);pd.GetPointData().SetNormals(numpy_to_vtk(nn,deep=True));ven.append((name,pd,main))
 art=[(name,poly(p,f)) for name,p,f,nn in ap if name.startswith('ICA ') and any(w in name for w in ['cavernous','petrous','paraophthalmic'])]
 models[label]=(ven,art)
views=[('01-frontal','Frontal',(0,1,0)),('02-lateral','Left lateral',(-1,0,0)),('03-superior','Superior',(0,0,1)),('04-oblique','Right anterior oblique',(1,1,.55)),('05-posterior','Posterior',(0,-1,0)),('06-inferior','Inferior',(0,0,-1))]
def render(label,name,view,opaque=False):
 cached=OUT/f'{name}-{label}{"-opaque" if opaque else "-raw"}.png'
 if cached.exists():
  try:
   with Image.open(cached) as check:check.load()
   return cached
  except OSError:pass
 ren=vtk.vtkRenderer();ren.SetBackground(1,1,1)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(True);win.SetSize(1000,1000);win.SetMultiSamples(0);win.SetAlphaBitPlanes(1);win.AddRenderer(ren)
 ren.SetUseDepthPeeling(1);ren.SetMaximumNumberOfPeels(80);ren.SetOcclusionRatio(.05)
 def add(pd,colour,opacity):
  mapper=vtk.vtkPolyDataMapper()
  if pd.GetPointData().GetNormals() is not None:mapper.SetInputData(pd)
  else:
   normal=vtk.vtkPolyDataNormals();normal.SetInputData(pd);normal.SplittingOff();normal.ConsistencyOn();normal.Update();mapper.SetInputConnection(normal.GetOutputPort())
  mapper.ScalarVisibilityOff()
  actor=vtk.vtkActor();actor.SetMapper(mapper);pr=actor.GetProperty();pr.SetColor(*colour);pr.SetOpacity(opacity);pr.SetAmbient(.25);pr.SetDiffuse(.7);pr.SetInterpolationToPhong();ren.AddActor(actor)
 for _,pd in bones:add(pd,(.57,.57,.54),.10)
 ven,art=models[label]
 for sid,pd,main in ven:
  if 'roof-closeup' in name and sid!='vein.cavernous.left':continue
  if 'closeup' in name and sid.endswith('.right'):continue
  add(pd,(.63,.28,.68) if 'superior_ophthalmic' in sid else (.92,.48,.12) if 'ovale_emissary' in sid else (.20,.64,.77) if 'superficial_middle' in sid else (.12,.36,.82) if main else (.43,.50,.61),(1 if opaque else .25) if main else .4)
 if not opaque or 'roof-closeup' in name:
  for artery_name,pd in art:
   if 'roof-closeup' in name and not artery_name.endswith('left'):continue
   add(pd,(.83,.11,.1) if 'cavernous' in artery_name else (.9,.59,.55),1 if 'cavernous' in artery_name else .45)
 center=np.array([.65,-44,63.0]);v=np.array(view,dtype=float);v/=np.linalg.norm(v)
 if 'roof-closeup' in name:center=np.array([-12,-43,67.0])
 cam=ren.GetActiveCamera();cam.SetPosition(*(center+v*600));cam.SetFocalPoint(*center);cam.SetViewUp(*((0,0,1) if abs(v[2])<.9 else (0,1,0)));cam.ParallelProjectionOn();cam.SetParallelScale(30);ren.ResetCameraClippingRange();win.Render()
 if 'roof-closeup' in name:cam.SetParallelScale(16);ren.ResetCameraClippingRange();win.Render()
 grab=vtk.vtkWindowToImageFilter();grab.SetInput(win);grab.Update();p=OUT/f'{name}-{label}{"-opaque" if opaque else "-raw"}.png';w=vtk.vtkPNGWriter();w.SetWriteToMemory(True);w.SetInputConnection(grab.GetOutputPort());w.Write();atomic_png_bytes(vtk_to_numpy(w.GetResult()).tobytes(),p);win.Finalize();return p

for name,title,view in views:
 for opaque in [False,True]:
  canvas=Image.new('RGB',(1848,1140),'white');d=ImageDraw.Draw(canvas)
  d.text((28,22),'Cavernous roof correction: '+title,font=font(34),fill='#1e293b')
  for i,label in enumerate(['before','after']):
   d.text((28+i*924,82),'v0.9.12' if label=='before' else 'v0.9.13',font=font(27),fill='#475569')
   im=Image.open(render(label,name,view,opaque)).convert('RGB').resize((900,900),Image.Resampling.LANCZOS);canvas.paste(im,(24+i*924,126))
  d.text((28,1050),'Blue: CS/lesser-wing. Cyan: SMCV. Purple: SOV. Orange: ovale emissary.',font=font(20),fill='#475569')
  d.text((28,1092),'Matched camera and scale. Actual meshes. ICA locally lowered up to 0.9 mm; skull retained. Dural roof is inferred.',font=font(20),fill='#64748b')
  atomic_save(canvas,OUT/(name+('-opaque.png' if opaque else '.png')))
 print(name,flush=True)
sheet=Image.new('RGB',(1620,1240),'white');d=ImageDraw.Draw(sheet);d.text((24,18),'v0.9.13: Cavernous roof correction',font=font(32),fill='#1e293b')
for i,(name,title,_) in enumerate(views):
 x=20+(i%3)*540;y=83+(i//3)*558;d.text((x+8,y),title,font=font(24),fill='#475569');sheet.paste(Image.open(OUT/f'{name}-after-raw.png').convert('RGB').resize((518,518),Image.Resampling.LANCZOS),(x,y+35))
d.text((26,1204),'Actual final meshes. Six matched-scale views; sellar soft-tissue boundary is inferred.',font=font(22),fill='#64748b');atomic_save(sheet,OUT/'00-six-view-overview.png')

for name,title,view in [('07-entry-closeup','Left anterior oblique close-up',(-1,.55,.2))]:
 canvas=Image.new('RGB',(1848,1140),'white');d=ImageDraw.Draw(canvas);d.text((28,22),title,font=font(34),fill='#1e293b')
 for i,label in enumerate(['before','after']):
  d.text((28+924*i,82),'v0.9.12' if label=='before' else 'v0.9.13',font=font(27),fill='#475569')
  im=Image.open(render(label,name,view,True)).convert('RGB');im=im.crop((160,130,730,820)).resize((740,896),Image.Resampling.LANCZOS);canvas.paste(im,(104+924*i,126))
 d.text((28,1050),'Blue: CS/lesser-wing. Cyan: SMCV. Purple: SOV. Orange: ovale emissary.',font=font(22),fill='#475569')
 d.text((28,1092),'Actual delivered surface normals; identical camera and crop. ICA locally lowered up to 0.9 mm; skull retained.',font=font(20),fill='#64748b');atomic_save(canvas,OUT/(name+'.png'))

canvas=Image.new('RGB',(1848,1140),'white');d=ImageDraw.Draw(canvas)
d.text((28,22),'One cavernous cavity; ICA emerges above the roof',font=font(34),fill='#1e293b')
for i,label in enumerate(['before','after']):
 d.text((28+924*i,82),'v0.9.12' if label=='before' else 'v0.9.13',font=font(27),fill='#475569')
 im=Image.open(render(label,'08-roof-closeup',(-1,.45,.22),True)).convert('RGB').resize((900,900),Image.Resampling.LANCZOS);canvas.paste(im,(24+924*i,126))
d.text((28,1050),'Blue: actual cavernous surface. Red: ICA. Grey: sphenoid and temporal bone.',font=font(22),fill='#475569')
d.text((28,1092),'Same camera and scale. Roof inferred from clinoid landmarks; no external arterial sleeve.',font=font(22),fill='#64748b')
atomic_save(canvas,OUT/'08-roof-closeup.png')
