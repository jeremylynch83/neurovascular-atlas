from pathlib import Path
import sys,json,numpy as np,trimesh,fcl,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];B=A/'docs';sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));rows={s['id']:s for s in M['structures']};canals=json.load(open(A/'anatomy/source/foramina/posterior-canals.json'));g=Glb(A/'public/anatomy/models/craniofacial.glb');bones={k:g.mesh(k)[:2] for k in ['bone.temporal.right','bone.temporal.left','bone.occipital','bone.sphenoid']};C={};old={};cache={}
def ob(p,f):
 m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
def clip(p,f,lo,hi):
 tri=p[f];s=((tri.min(1)<hi)&(tri.max(1)>lo)).all(1);return p,f[s]
def locator(p,f):
 o=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));o.SetPoints(pts);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.column_stack([np.full(len(f),3),f]).ravel().astype(np.int64),deep=True));o.SetPolys(c);t=vtk.vtkOBBTree();t.SetDataSet(o);t.BuildLocator();return t
report={'boneContacts':[],'passages':[],'boneTopology':{},'failures':[]}
for k,(p,f) in bones.items():
 t=trimesh.Trimesh(p,f,process=False);report['boneTopology'][k]={'triangles':len(f),'windingConsistent':t.is_winding_consistent,'watertight':t.is_watertight,'components':len(t.split(only_watertight=False)),'nonManifoldEdges':int(sum(np.bincount(t.edges_unique_inverse)>2))}
for side in ['right','left']:
 lo=np.array([8,-82,29])if side=='right'else np.array([-52,-82,29]);hi=np.array([52,-46,60])if side=='right'else np.array([-8,-46,60]);bp=[];bf=[];off=0
 for k,(p,f) in bones.items():
  pp,ff=clip(p,f,lo,hi);bp.append(pp);bf.append(ff+off);off+=len(pp)
 bone=ob(np.vstack(bp),np.vstack(bf));loc=locator(np.vstack(bp),np.vstack(bf))
 tail='right'if side=='right'else'right.left'
 ids=['artery.eca.occipital.stylomastoid.'+tail,'artery.eca.maxillary.anterior_tympanic.'+tail,'artery.eca.apa.hypoglossal.'+tail,'artery.eca.apa.jugular.'+tail,'artery.posterior.labyrinthine_'+side,'artery.amendment.jugular_ascending_iac_branch.'+side,'artery.amendment.anterior_vestibular.'+side]
 ids += [s['id'] for s in M['structures'] if s.get('asset') and s['system']=='artery' and s['side']==side and any(t in s['id'] for t in ['vestibular','cochlear','subarcuate','tympanic','facial_nerve_arcade','petrosal','stylomastoid','labyrinthine'])]
 ids=list(dict.fromkeys(ids))
 ids+=['vein.sigmoid.'+side,'vein.internal_jugular.'+side,'vein.anterior_condylar.'+side]
 for sid in ids:
  if sid in C:p,f,n=C[sid]
  elif sid in old:p,f,n=old[sid]
  else:
   s=rows[sid];file=s['asset']['file'];
   if file not in cache:cache[file]=Glb(A/'public/anatomy'/file)
   p,f,n=cache[file].mesh(s['asset']['node'])
  p,ff=clip(p,f,lo,hi)
  if not len(ff):continue
  result=fcl.CollisionResult();c=fcl.collide(bone,ob(p,ff),fcl.CollisionRequest(num_max_contacts=10000,enable_contact=True),result);r={'id':sid,'triangles':len(ff),'contacts':c}
  if c:
   pts=np.array([v.pos for v in result.contacts]);r['contactBounds']=[pts.min(0).tolist(),pts.max(0).tolist()];report['failures'].append(sid)
  report['boneContacts'].append(r);print(r,flush=True)
 for key in ['internal-acoustic','facial-canal','hypoglossal','jugular-foramen','jugular-neural','petrotympanic']:
  hits=[];course=canals[side][key]
  for a,b in zip(course,course[1:]):
   pts=vtk.vtkPoints();loc.IntersectWithLine(a,b,pts,None);hits.extend([pts.GetPoint(i)for i in range(pts.GetNumberOfPoints())])
  r={'id':key+'.'+side,'centrelineHits':len(hits),'points':hits};report['passages'].append(r)
  if hits:report['failures'].append(key+'.'+side)
(B/'foramina-batch3-geometry-validation.json').write_text(json.dumps(report,indent=2));print('FAILURES',report['failures'],flush=True)

assert not report['failures'],report['failures']
