"""Render exact atlas and delivered vessel geometry for target review."""
from pathlib import Path
import json
import numpy as np
import trimesh, vtk
from PIL import Image, ImageDraw, ImageFont
from build_targets import poly

APP=Path(__file__).resolve().parents[2]
dest=APP/'docs/validation'
brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',force='scene',process=False)
veins=trimesh.load(APP/'.authoring/veins-v0.9.14.glb',force='scene',process=False)
arteries=trimesh.load(APP/'.authoring/arteries-v0.9.14.glb',force='scene',process=False)
rows={s['id']:s for s in json.loads((APP/'anatomy/generated/complete_manifest.json').read_text())['structures']}

def mesh_actor(mesh,colour,opacity=1):
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly(mesh));mapper.ScalarVisibilityOff()
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*colour);actor.GetProperty().SetOpacity(opacity)
    return actor

def vascular(scene,name):
    t,k=scene.graph[name];m=scene.geometry[k].copy();m.apply_transform(t);return m

def line_actor(identifier):
    points=np.array(rows[identifier]['landmark']['course'])
    p=vtk.vtkPoints()
    for v in points:p.InsertNextPoint(*v)
    line=vtk.vtkPolyLine();line.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):line.GetPointIds().SetId(i,i)
    cells=vtk.vtkCellArray();cells.InsertNextCell(line);data=vtk.vtkPolyData();data.SetPoints(p);data.SetLines(cells)
    tube=vtk.vtkTubeFilter();tube.SetInputData(data);tube.SetRadius(.35);tube.SetNumberOfSides(8);tube.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(tube.GetOutputPort());actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(.88,.58,.04)
    return actor

def render(actors,name,view,centre,scale):
    ren=vtk.vtkRenderer();ren.SetBackground(.97,.97,.97)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(800,650);window.SetMultiSamples(0);window.AddRenderer(ren)
    for actor in actors:ren.AddActor(actor)
    camera=ren.GetActiveCamera();camera.SetPosition(*(np.array(centre)+np.array(view)*600));camera.SetFocalPoint(*centre)
    camera.SetViewUp(*( (0,1,0) if abs(view[2])>.9 else (0,0,1)));camera.ParallelProjectionOn();camera.SetParallelScale(scale)
    ren.ResetCameraClippingRange();window.Render();read=vtk.vtkWindowToImageFilter();read.SetInput(window);read.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(dest/name));writer.SetInputConnection(read.GetOutputPort());writer.Write();window.Finalize()

def dural_actors():
    result=[mesh_actor(brain.geometry[k],(.6,.53,.7),.28) for k in ['brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']]
    result += [mesh_actor(vascular(veins,k),(.08,.34,.75)) for k in ['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence']]
    result.append(line_actor('brain.landmark.falcotentorial'));return result

def central_actors(sides):
    result=[]
    for side in sides:
        for k,s in rows.items():
            if s.get('anatomy') and s['side']==side and any(x in s['anatomy']['sourceLabel'].lower() for x in ['precentral gyrus','postcentral gyrus']):
                result.append(mesh_actor(brain.geometry[k],(.68,.67,.64),.6))
        result += [mesh_actor(brain.geometry['brain.central-sulcus.'+side],(.48,.52,.66),.5),
                   mesh_actor(vascular(arteries,'Central '+side),(.78,.12,.15)),
                   line_actor('brain.landmark.central-sulcus.'+side)]
    return result

render(dural_actors(),'target-falcotentorial-sagittal-v0.9.15.png',(-1,0,0),(0,-112,95),65)
render(dural_actors(),'target-falcotentorial-oblique-v0.9.15.png',(.8,1,.5),(0,-105,100),65)
render(central_actors(['right']),'target-central-right-v0.9.15.png',(1,0,0),(35,-78,128),40)
render(central_actors(['left','right']),'target-central-superior-v0.9.15.png',(0,0,1),(0,-77,125),65)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
canvas=Image.new('RGB',(1600,1460),'white');draw=ImageDraw.Draw(canvas)
draw.text((25,18),'Anatomical targets and retained vessel courses v0.9.15',font=font,fill='#20252b')
panels=[('target-falcotentorial-sagittal-v0.9.15.png','Falcotentorial attachment, sagittal'),
        ('target-falcotentorial-oblique-v0.9.15.png','Falcotentorial attachment, oblique'),
        ('target-central-right-v0.9.15.png','Right central sulcus, lateral'),
        ('target-central-superior-v0.9.15.png','Central sulci, superior')]
for i,(file,title) in enumerate(panels):
    x=(i%2)*800;y=65+(i//2)*690
    draw.text((x+18,y),title,font=small,fill='#30343a');canvas.paste(Image.open(dest/file).convert('RGB'),(x,y+28))
draw.text((25,1410),'Blue: retained veins. Red: retained arteries. Gold: atlas course guides. Vessel fitting has not been applied.',font=small,fill='#30343a')
canvas.save(dest/'anatomical-target-review-v0.9.15.png')
print(dest/'anatomical-target-review-v0.9.15.png')
