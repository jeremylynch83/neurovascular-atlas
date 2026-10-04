"""Six additional model views and comparisons with attributed source images."""
import json
import io,os
from pathlib import Path
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
from scipy.spatial import cKDTree
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[3];WORK=ROOT/'comparison-v097'
OUT=ROOT/'cavernous-v0.9.7';OUT.mkdir(exist_ok=True)
TMP=WORK/'cavernous';TMP.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(s):return ImageFont.truetype(FONT,s)
def save_image(im,path):
 data=io.BytesIO();im.save(data,format='PNG');b=data.getvalue()
 temp=path.with_suffix('.tmp')
 with temp.open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 temp.replace(path)
 with Image.open(path) as check:check.load()

def geometry(label,row):
 p=np.array(np.memmap(WORK/f'{label}.bin',dtype='<f4',mode='r',offset=row['positionOffset'],shape=(row['vertices'],3)))
 f=np.array(np.memmap(WORK/f'{label}.bin',dtype='<u4',mode='r',offset=row['indexOffset'],shape=(row['indices']//3,3)))
 return p,f
def poly(p,f):
 pd=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));pd.SetPoints(pts)
 ca=vtk.vtkCellArray();ca.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));pd.SetPolys(ca)
 n=vtk.vtkPolyDataNormals();n.SetInputData(pd);n.SplittingOff();n.ConsistencyOn();n.Update();return n.GetOutput()

records={label:json.loads((WORK/f'{label}.json').read_text()) for label in ['bones','arteries','after','before','oldarteries']}
BONES=[]
for r in records['bones']:
 if r['name'] in ['bone.sphenoid','bone.temporal.left','bone.temporal.right']:
  BONES.append((r['name'],poly(*geometry('bones',r))))
def load_model(label,artery_label):
 venous=[];ica=[]
 primary=[r for r in records[label] if 'vein.cavernous.' in r['name'] or 'intercavernous' in r['name']]
 tree=cKDTree(np.concatenate([geometry(label,r)[0] for r in primary]))
 for r in records[label]:
  p,f=geometry(label,r);main=r in primary
  if not main:
   if tree.query(p)[0].min()>.025:continue
   f=f[tree.query(p[f].mean(axis=1))[0]<4]
   if not len(f):continue
  venous.append((r['name'],poly(p,f),main))
 for r in records[artery_label]:
  if 'ICA cavernous' in r['name']:ica.append((r['name'],poly(*geometry(artery_label,r))))
 return venous,ica
MODELS={'before':load_model('before','oldarteries'),'after':load_model('after','arteries')}

VIEWS=[
 ('01-frontal','Frontal',(0,1,0)),
 ('02-left-lateral','Left lateral',(-1,0,0)),
 ('03-superior','Superior',(0,0,1)),
 ('04-right-anterior-oblique','Right anterior oblique',(1,1,.55)),
 ('05-posterior','Posterior',(0,-1,0)),
 ('06-inferior','Inferior',(0,0,-1))]

def render(name,view,transparent=False,bone=True,context=False,version="after"):
 VENOUS,ICA=MODELS[version]
 ren=vtk.vtkRenderer();ren.SetBackground(1,1,1)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1000,1000);win.SetAlphaBitPlanes(1);win.SetMultiSamples(0);win.AddRenderer(ren)
 ren.SetUseDepthPeeling(1);ren.SetMaximumNumberOfPeels(100);ren.SetOcclusionRatio(.05)
 def add(pd,col,op):
  m=vtk.vtkPolyDataMapper();m.SetInputData(pd);m.ScalarVisibilityOff()
  a=vtk.vtkActor();a.SetMapper(m);pr=a.GetProperty();pr.SetColor(*col);pr.SetOpacity(op);pr.SetInterpolationToPhong();pr.SetAmbient(.25);pr.SetDiffuse(.7);ren.AddActor(a)
 if bone:
  for _,pd in BONES:add(pd,(.55,.55,.52),.13)
 for _,pd,main in VENOUS:add(pd,(.12,.38,.84) if main else (.43,.48,.6),.28 if transparent else 1)
 if transparent:
  for _,pd in ICA:add(pd,(.86,.13,.11),1)
 center=np.array([.65,-44,63]);v=np.array(view,float);v/=np.linalg.norm(v)
 cam=ren.GetActiveCamera();cam.SetPosition(*(center+v*600));cam.SetFocalPoint(*center)
 cam.SetViewUp(*((0,0,1) if abs(v[2])<.9 else (0,1,0)))
 cam.ParallelProjectionOn();cam.SetParallelScale(30);ren.ResetCameraClippingRange();win.Render()
 c=vtk.vtkWindowToImageFilter();c.SetInput(win);c.Update()
 path=TMP/f'{name}.png';w=vtk.vtkPNGWriter();w.SetFileName(str(path));w.SetInputConnection(c.GetOutputPort());w.Write();win.Finalize();return path


for name,title,view in VIEWS:
 images=[Image.open(render(name+'-'+version,view,True,version=version)).convert('RGB') for version in ['before','after']]
 canvas=Image.new('RGB',(1848,1140),'white');d=ImageDraw.Draw(canvas)
 d.text((28,20),'Cavernous ICA and sinuses: '+title,font=font(34),fill='#1e293b')
 d.text((28,83),'Before: v0.9.6',font=font(27),fill='#475569');d.text((952,83),'After: v0.9.7',font=font(27),fill='#475569')
 for i,im in enumerate(images):canvas.paste(im.resize((900,900),Image.Resampling.LANCZOS),(24+924*i,126))
 d.text((28,1050),'Matched camera and scale. Red: cavernous ICA. Blue: venous envelope. Grey: skull and venous joins.',font=font(21),fill='#475569')
 d.text((28,1093),'Actual delivered meshes. Sellar soft-tissue exclusion is inferred; detailed nerves and septa are not modelled.',font=font(20),fill='#64748b')
 save_image(canvas,OUT/f'{name}.png');print(name,flush=True)
sheet=Image.new('RGB',(1620,1240),'white');d=ImageDraw.Draw(sheet)
d.text((24,18),'v0.9.7: cavernous sinuses and corrected ICA',font=font(32),fill='#1e293b')
for i,(name,title,_) in enumerate(VIEWS):
 x=20+(i%3)*540;y=83+(i//3)*558;d.text((x+8,y),title,font=font(24),fill='#475569')
 im=Image.open(TMP/f'{name}-after.png').convert('RGB').resize((518,518),Image.Resampling.LANCZOS);sheet.paste(im,(x,y+35))
d.text((26,1204),'Six matched-scale views of the updated delivered meshes.',font=font(22),fill='#64748b')
save_image(sheet,OUT/'00-six-view-overview.png')
for name,title,view in VIEWS[:2]:
 render(name+'-opaque-after',view,False)
