"""Independent optic bore, native-envelope and vessel-clearance checks."""
from pathlib import Path
import sys,json,numpy as np,trimesh,vtk,fcl
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
from revision143_surface_qa import crossing,check
bones=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=bones.mesh('bone.sphenoid');t=trimesh.Trimesh(p,f,process=False);spec=json.loads((A/'anatomy/source/foramina/revision145-optic.json').read_text());report={'release':'0.9.145','optic':{},'orbitalClearances':{}}
assert t.is_watertight and t.is_winding_consistent
qa=check(p,f[p[f].max(1)[:,2]>66]);assert qa['materialCrossings']==0;report['superiorSphenoidSelfIntersection']=qa
for side,r in spec.items():
 a,b,u,v,axis=[np.array(r[k])for k in ['a','b','u','v','axis']];mid=(a+b)/2;th=np.arange(96)*2*np.pi/96;dirs=np.cos(th)[:,None]*u+np.sin(th)[:,None]*v;expected=1/np.sqrt((np.cos(th)/2.25)**2+(np.sin(th)/1.85)**2);sections=[]
 for s in np.linspace(-1.25,.5,8):
  c=mid+s*axis;origins=np.tile(c,(96,1));loc,ri,ti=t.ray.intersects_location(origins,dirs,multiple_hits=True);dist=np.linalg.norm(loc-origins[ri],axis=1);nearest=np.full(96,100.);np.minimum.at(nearest,ri,dist);err=float(max(abs(nearest-expected)));assert err<.025,(side,s,err);sections.append({'axisOffsetMm':float(s),'wallRays':96,'majorDiameterMm':float(nearest[0]+nearest[48]),'minorDiameterMm':float(nearest[24]+nearest[72]),'maxRadialErrorMm':err})
 assert not t.contains(np.linspace(a,b,33)).any();report['optic'][side]={'enclosedSections':sections,'centerlineClear':True,'note':'Oblique source mouths have unequal wall lengths. Diameter tests refer to the fully enclosed isthmus, rather than the projected mouth.'};print(side,'enclosed',len(sections),'sections, dimensions verified',flush=True)
# A subtraction-only superior construction must stay within the retained native source.
src=np.load(A/'anatomy/source/foramina/revision145-native-sources.npz');op=src['sphenoid_positions'];of=src['sphenoid_faces'];pd=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(np.ascontiguousarray(op),deep=True));pd.SetPoints(vp);cells=vtk.vtkCellArray();cells.SetCells(len(of),numpy_to_vtkIdTypeArray(np.column_stack([np.full(len(of),3),of]).astype('int64').ravel(),deep=True));pd.SetPolys(cells);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(pd);test=p[p[:,2]>66.01];dist=np.array([sdf.EvaluateFunction(x)for x in test]);outward=float(max(dist,default=0));assert outward<.004,outward;report['nativeEnvelope']={'sampledVertices':len(test),'maximumSignedOutsideDistanceMm':outward,'toleranceMm':.004,'addedSuperiorBoneVolume':False};print('native contour maximum outward distance',outward,flush=True)
def obj(q,tri):
 b=fcl.BVHModel();b.beginModel();b.addSubModel(q,tri);b.endModel();return fcl.CollisionObject(b)
def clip(q,tri,lo,hi):
 a=q[tri];return tri[((a.max(1)>=lo)&(a.min(1)<=hi)).all(1)]
rows={s['id']:s for s in json.loads((A/'anatomy/generated/complete_manifest.json').read_text())['structures']};cache={}
for side in ['right','left']:
 lo=np.array([7.,-38,65.8]);hi=np.array([29.,-15,85])
 if side=='left':lo[0],hi[0]=-hi[0],-lo[0]
 bf=clip(p,f,lo,hi);bo=obj(p,bf)
 for sid in ['artery.anterior.ophthalmic_'+side,'artery.amendment.deep_recurrent_ophthalmic.'+side,'artery.amendment.superficial_recurrent_meningeal.'+side,'vein.superior_ophthalmic.'+side]:
  a=rows[sid]['asset'];file=a['file']
  if file not in cache:cache[file]=Glb(A/'public/anatomy'/file)
  q,tri,_=cache[file].mesh(a['node']);tri=clip(q,tri,lo,hi);res=fcl.CollisionResult();count=fcl.collide(bo,obj(q,tri),fcl.CollisionRequest(num_max_contacts=20000,enable_contact=True),res)if len(tri)else 0;assert count<20000;pairs=np.array([(c.b1,c.b2)for c in res.contacts],int).reshape(-1,2);bad=[];depth=[]
  if len(pairs):bad,depth=crossing(p[bf[pairs[:,0]]],q[tri[pairs[:,1]]])
  rec={'candidateContacts':count,'materialCrossingsAbove002Mm':len(bad),'maximumCrossingBoundMm':float(max(depth,default=0))};report['orbitalClearances'][sid]=rec;print(sid,rec,flush=True);assert not len(bad),sid
(A/'docs/revision145-optic-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Optic calibre, enclosure, native contour and orbital clearances passed.')
