"""Optional authoring QA. Requires NumPy, VTK and python-fcl; not used by app builds."""
from pathlib import Path
import json,hashlib,numpy as np,vtk,fcl
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk,numpy_to_vtkIdTypeArray
from geometry import Glb
APP=Path(__file__).resolve().parents[2]
M=json.load(open(APP/'public/anatomy/manifest.json'));rows={s['id']:s for s in M['structures']};changes=json.load(open(APP/'anatomy/source/foramina/petrous-changes.json'))
modified=[k for k,v in changes.items()if not v.get('guideOnly')]
wanted=set(modified+['bone.temporal.right','bone.temporal.left','bone.sphenoid','bone.occipital']+['artery.anterior.internal_carotid_'+side+'.segment.'+part for side in ['right','left']for part in ['cervical','petrous']]);D={};hashes={}
for file in set(rows[k]['asset']['file']for k in wanted):
 path=APP/'public/anatomy'/file;g=Glb(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
 for k in wanted:
  if rows[k]['asset']['file']==file:
   p,f,_=g.mesh(rows[k]['asset']['node']);D[k]={'p':p,'index':f.ravel()}
V={k:D[k]for k in modified};out=[]
def pd(p,f):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.column_stack([np.full(len(f),3),f]).ravel().astype(np.int64),deep=True));o=vtk.vtkPolyData();o.SetPoints(pts);o.SetPolys(cells);return o

def intersections(p,f):
 cc=p[f].mean(1);selected=(cc[:,2]>35)&(cc[:,2]<55)&(np.abs(cc[:,0])>28);f=f[selected];o=pd(p,f);c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,o);c.SetInputData(1,o);t=vtk.vtkTransform();t.Identity();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToAllContacts();c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetNumberOfCellsPerNode(2);c.Update();a=vtk_to_numpy(c.GetContactCells(0));b=vtk_to_numpy(c.GetContactCells(1));sel=a<b;a=a[sel];b=b[sel];_,ix=np.unique(np.round(p,5),axis=0,return_inverse=True);uf=ix[f];sel=~(uf[a,:,None]==uf[b,None,:]).any((1,2));a=a[sel];b=b[sel];bounds=[]
 for start in range(0,len(a),20000):
  aa=p[f[a[start:start+20000]]];bb=p[f[b[start:start+20000]]];nn=np.cross(aa[:,1]-aa[:,0],aa[:,2]-aa[:,0]);mm=np.cross(bb[:,1]-bb[:,0],bb[:,2]-bb[:,0]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20);mm/=np.maximum(np.linalg.norm(mm,axis=1)[:,None],1e-20);d=np.sum((aa-bb[:,0,None])*mm[:,None],axis=2);e=np.sum((bb-aa[:,0,None])*nn[:,None],axis=2);bounds.extend(np.minimum(np.maximum(0,np.minimum(d.max(1),-d.min(1))),np.maximum(0,np.minimum(e.max(1),-e.min(1)))))
 bounds=np.array(bounds);return {'testedTriangles':len(f),'nonAdjacentContacts':len(bounds),'materialContacts':int(sum(bounds>.001)),'maxPenetrationBoundMm':float(max(bounds,default=0))}
controlP=np.array([[35,-55,45],[36,-55,45],[35.5,-54,45],[35.5,-54.8,44],[35.5,-54.8,46],[35.5,-55.5,45]],float);controlF=np.array([[0,1,2],[3,4,5]],int)
assert intersections(controlP,controlF)['nonAdjacentContacts']==1,'Self-intersection positive control failed'
for side in ['right','left']:
 bp=[];bf=[];offset=0
 lo=np.array([18,-69,28]) if side=='right'else np.array([-46,-69,28]);hi=np.array([46,-43,57])if side=='right'else np.array([-18,-43,57])
 for key in ['bone.temporal.'+side,'bone.sphenoid','bone.occipital']:
  r=D[key];p=np.array(r['p']);f=np.array(r['index']).reshape(-1,3);tri=p[f];sel=((tri.min(1)<hi)&(tri.max(1)>lo)).all(1);bp.append(p);bf.append(f[sel]+offset);offset+=len(p)
 model=fcl.BVHModel();model.beginModel();model.addSubModel(np.vstack(bp),np.vstack(bf));model.endModel();bone=fcl.CollisionObject(model)
 ids=[k for k in V if not k.startswith('artery.connection.')and (k.endswith('left')== (side=='left'))]
 ids+=['artery.anterior.internal_carotid_'+side+'.segment.'+p for p in ['cervical','petrous']]
 for sid in ids:
  if sid not in D:continue
  r=D[sid];p=np.array(r['p']);f=np.array(r['index']).reshape(-1,3);tri=p[f];windowLo=lo.copy();
  if 'anterior_tympanic' in sid:windowLo[2]=43 # Corrected fissure window; proximal approach is B2-AT-01.
  sel=((tri.min(1)<hi)&(tri.max(1)>windowLo)).all(1);f=f[sel];model=fcl.BVHModel();model.beginModel();model.addSubModel(p,f);model.endModel();obj=fcl.CollisionObject(model);result=fcl.CollisionResult();num=fcl.collide(bone,obj,fcl.CollisionRequest(num_max_contacts=10000,enable_contact=True),result);row={'id':sid,'testedTriangles':len(f),'windowMm':[windowLo.tolist(),hi.tolist()],'boneContacts':num,'method':'FCL double-precision BVH triangle collision'};out.append(row);print(row,flush=True);assert num==0,sid

report={'release':M['release'],'sourceHashes':hashes,'boneContacts':out,'selfIntersections':[],'deferredIssueIds':['B2-AT-01'],'scope':'Temporal, sphenoid and occipital passage windows. Jaw surfaces and complete neural/auditory canals are excluded.'}
for k in modified:
 p=D[k]['p'];f=D[k]['index'].reshape(-1,3);row={'id':k,**intersections(p,f)};report['selfIntersections'].append(row);print(k,'self contacts',row['nonAdjacentContacts'],flush=True);assert row['nonAdjacentContacts']==0,k
report['overlapChecks']=[]
for side in ['right','left']:
 ct='artery.anterior.caroticotympanic_'+side
 for other in ['artery.anterior.internal_carotid_'+side+'.segment.petrous','artery.connection.inferior_tympanic_caroticotympanic.'+side]:
  objects=[]
  for key in [ct,other]:
   r=D[key];model=fcl.BVHModel();model.beginModel();model.addSubModel(r['p'],r['index'].reshape(-1,3));model.endModel();objects.append(fcl.CollisionObject(model))
  result=fcl.CollisionResult();contacts=fcl.collide(objects[0],objects[1],fcl.CollisionRequest(num_max_contacts=10000,enable_contact=True),result);assert contacts>0,(ct,other,'lost overlap');report['overlapChecks'].append({'from':ct,'to':other,'surfaceContactPairs':contacts,'joinType':'overlapping exteriors; not a welded ostium'})
(APP/'docs/foramina-batch2-geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Passed',len(out),'regional bone tests and',len(report['selfIntersections']),'self-contact tests.')
