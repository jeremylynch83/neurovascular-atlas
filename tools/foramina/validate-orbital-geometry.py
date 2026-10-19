from pathlib import Path
import sys,json,numpy as np,trimesh,fcl,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];B=A/'docs';sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));rows={s['id']:s for s in M['structures']};D={};C={}
for file in ['models/craniofacial.glb','models/complete-circulation.glb','models/venous.glb']:
 g=Glb(A/'public/anatomy'/file)
 for ss in M['structures']:
  if ss.get('asset',{}).get('file')==file:
   k=ss['id']
   if ss['system']=='bone' or any(t in k for t in ['ophthalmic','ethmoidal','orbital','infraorbital','recurrent_meningeal']):D[k]=g.mesh(ss['asset']['node'])
bones={k:(p,f)for k,(p,f,n)in D.items()if k.startswith('bone.')}
def ob(p,f):
 m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
def poly(p,f):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].ravel().astype(np.int64),deep=True));o=vtk.vtkPolyData();o.SetPoints(pts);o.SetPolys(cells);return o
report={'vessels':[],'struts':[],'failures':[]};names=[]
for side in ['right','left']:
 bo={};
 for family,lo,hi in [('apex',[7,-38,62],[29,-18,85]),('ethmoid',[2,-20,65],[24,18,84]),('sof',[12,-39,44],[29,-16,76]),('iof',[15,-28,38],[38,-15,67])]:
  lo=np.array(lo,float);hi=np.array(hi,float)
  if side=='left':lo[0],hi[0]=-hi[0],-lo[0]
  pp=[];ff=[];off=0
  for k,(p,f)in bones.items():
   tri=p[f];sel=((tri.min(1)<hi)&(tri.max(1)>lo)).all(1)
   if sel.any():pp.append(p);ff.append(f[sel]+off);off+=len(p)
  bo[family]=(ob(np.vstack(pp),np.vstack(ff)),lo,hi)
 tail='right'if side=='right'else'right.left'
 ids=[('artery.anterior.ophthalmic_'+side,'apex'),('artery.anterior.anterior_ethmoidal_'+side,'ethmoid'),('artery.anterior.posterior_ethmoidal_'+side,'ethmoid'),('artery.amendment.artery_of_superior_orbital_fissure.'+side,'sof'),('artery.amendment.deep_recurrent_ophthalmic.'+side,'sof'),('artery.amendment.superficial_recurrent_meningeal.'+side,'sof'),('vein.superior_ophthalmic.'+side,'apex'),('vein.inferior_ophthalmic.'+side,'iof'),('artery.eca.maxillary.infraorbital.'+tail,'iof'),('vein.infraorbital.'+side,'iof')]
 for sid,region in ids:
  p,f,n=C.get(sid,D[sid]);bone,lo,hi=bo[region];tri=p[f];sel=((tri.min(1)<hi)&(tri.max(1)>lo)).all(1);res=fcl.CollisionResult();num=fcl.collide(bone,ob(p,f[sel]),fcl.CollisionRequest(num_max_contacts=10000,enable_contact=True),res);r={'id':sid,'region':region,'triangles':int(sum(sel)),'contacts':num}
  if num:
   pts=np.array([c.pos for c in res.contacts]);r['bounds']=[pts.min(0).tolist(),pts.max(0).tolist()];report['failures'].append(sid)
  report['vessels'].append(r);print(r,flush=True)
# Independently fitted controls from the delivered v0.9.136 strut surfaces.
p,f,n=D['bone.sphenoid'];implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(p,f))
for r in json.load(open(A/'anatomy/source/foramina/orbital-strut-controls.json')):
 q=r['retainedControls'];ds=[float(implicit.EvaluateFunction(x))for x in q];assert len(q)>=3
 report['struts'].append({'id':r['id'],'controls':len(q),'signedDistancesMm':ds})
 if any(d>=-.1 for d in ds):report['failures'].append(r['id'])
report['boneTopology']={}
for key in ['bone.sphenoid','bone.frontal','bone.maxilla.right']:
 p,f=bones[key];t=trimesh.Trimesh(p,f,process=False);bad=int(sum(np.bincount(t.edges_unique_inverse)>2));assert not bad and t.is_winding_consistent,key;report['boneTopology'][key]={'triangles':len(f),'nonManifoldEdges':bad,'watertight':t.is_watertight,'windingConsistent':t.is_winding_consistent}
(B/'foramina-batch4-geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('FAILURES',report['failures']);assert not report['failures'],report['failures']
