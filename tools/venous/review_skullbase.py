"""Render the authored skull-base veins against retained local bones."""
import json,sys
import numpy as np
from reference import ROOT,APP,records,arrays,poly,render,numpy_to_vtk
from morphology import unit
paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
regions=['basilar_plexus','sphenoparietal','cavernous.','intercavernous','petrosal.','marginal','condylar','sigmoid.','transverse.','internal_jugular.']
colours={'basilar_plexus':(.1,.8,.95),'sphenoparietal':(.95,.7,.15),'superior_petrosal':(.9,.4,.9),'inferior_petrosal':(.3,.8,.35),'cavernous':(.25,.5,.95),'marginal':(.85,.35,.25)}
def tube(row):
 q=np.array(row['points']);r=np.array(row['radii']);t=unit(np.gradient(q,axis=0));profile=row.get('profile',{})
 n=np.array(row.get('wallNormals',np.tile([0,0,1.],(len(q),1))));n=unit(n-t*np.sum(n*t,axis=1)[:,None]);b=unit(np.cross(t,n));theta=np.linspace(0,2*np.pi,20,endpoint=False)
 p=q[:,None,:]+r[:,None,None]*(profile.get('depth',1)*n[:,None,:]*np.cos(theta)[None,:,None]+profile.get('width',1)*b[:,None,:]*np.sin(theta)[None,:,None]);f=[]
 for i in range(len(q)-1):
  for j in range(20):a=i*20+j;bb=i*20+(j+1)%20;f.extend([[a,bb,a+20],[bb,bb+20,a+20]])
 return poly(p.reshape(-1,3),np.array(f))
bones=[(poly(*arrays(r)),(.85,.8,.7),.6) for r in records if r['name'] in ['bone.sphenoid','bone.occipital','bone.temporal.left','bone.temporal.right']]
veins=[]
if '--surface' in sys.argv:
 data=np.load(ROOT/'venous-mesh.npz');spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text())
 for i,row in enumerate(spec['structures']):
  if any(k in row['id'] for k in regions):
   pd=poly(data['positions'],data['faces'][data['labels']==i]);pd.GetPointData().SetNormals(numpy_to_vtk(data['normals'],deep=True))
   veins.append((pd,next((c for k,c in colours.items() if k in row['id']),(.45,.5,.85)),1))
for row in ([] if '--surface' in sys.argv else paths):
 if any(k in row['id'] for k in regions):veins.append((tube(row),next((c for k,c in colours.items() if k in row['id']),(.45,.5,.85)),1))
prefix='skullbase-surface-' if '--surface' in sys.argv else 'skullbase-paths-'
for name,view in [('superior',(0,0,1)),('posterior',(0,-1,.55)),('right',(1,0,.25))]:render(bones+veins,ROOT/(prefix+name+'.png'),view=view,center=(.65,-76,52),scale=66)

if '--surface' in sys.argv:
 import vtk
 def section(pd,origin,normal):
  plane=vtk.vtkPlane();plane.SetOrigin(*origin);plane.SetNormal(*normal)
  cutter=vtk.vtkCutter();cutter.SetInputData(pd);cutter.SetCutFunction(plane);cutter.Update()
  tube=vtk.vtkTubeFilter();tube.SetInputConnection(cutter.GetOutputPort());tube.SetRadius(.10);tube.SetNumberOfSides(8);tube.Update();return tube.GetOutput()
 for name,origin,normal,view,scale in [
  ('clivus',(0.65,-60,47),(1,0,0),(1,0,0),22),
  ('lesser-wing',(35,-27,79),(1,0,0),(1,0,0),13),
  ('petrous-ridge',(35,-70,59),(1,0,0),(1,0,0),17),
  ('parasellar',(0.65,-46,62),(0,1,0),(0,-1,0),27),
  ('foramen-magnum',(0.65,-85,32),(0,0,1),(0,0,1),28)]:
  items=[(section(pd,origin,normal),col,1) for pd,col,_ in bones+veins]
  for rec in records:
   if rec['name'] in ['ICA cavernous right','ICA cavernous left']:items.append((section(poly(*arrays(rec)),origin,normal),(.95,.3,.2),1))
  render(items,ROOT/('skullbase-section-'+name+'.png'),view=view,center=origin,scale=scale)
