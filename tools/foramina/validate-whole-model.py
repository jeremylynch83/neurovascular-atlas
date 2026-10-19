"""Whole-delivery structural inventory and vascular/bone surface screen.
This records source limitations; a surface collision alone is not an anatomical diagnosis.
"""
from pathlib import Path
import sys,json,hashlib,time,numpy as np,trimesh,fcl
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));D={};report={'release':M['release'],'assetHashes':{},'meshes':[],'vascularBoneContacts':[],'vascularMeshesScreened':0,'candidateBoneVesselPairs':0,'structuralErrors':[]};rows={s['id']:s for s in M['structures']}
for file in sorted({s['asset']['file']for s in M['structures']if s.get('asset')}):
 path=A/'public/anatomy'/file;g=Glb(path);report['assetHashes'][file]=hashlib.sha256(path.read_bytes()).hexdigest()
 for s in M['structures']:
  if s.get('asset',{}).get('file')!=file:continue
  sid=s['id'];p,f,n=g.mesh(s['asset']['node']);D[sid]=(p,f,n)
  err=[]
  if not np.isfinite(p).all()or not np.isfinite(n).all():err.append('non-finite array')
  if f.min()<0 or f.max()>=len(p):err.append('invalid index')
  area=np.linalg.norm(np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]]),axis=1)/2;deg=int(sum(area<1e-12));r={'id':sid,'system':s['system'],'vertices':len(p),'triangles':len(f),'zeroAreaTriangles':deg,'bounds':[p.min(0).tolist(),p.max(0).tolist()]}
  if s['system']=='bone':
   t=trimesh.Trimesh(p,f,process=False);r.update(watertight=t.is_watertight,windingConsistent=t.is_winding_consistent,nonManifoldEdges=int(sum(np.bincount(t.edges_unique_inverse)>2)))
  report['meshes'].append(r)
  if err:report['structuralErrors'].append({'id':sid,'errors':err})
 print('Decoded',file,flush=True)
def ob(p,f):
 m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
bones={sid:(ob(p,f),p.min(0),p.max(0))for sid,(p,f,n)in D.items()if rows[sid]['system']=='bone'}
for sid,(p,f,n)in D.items():
 s=rows[sid]
 if s['system']not in ['artery','vein']:continue
 report['vascularMeshesScreened']+=1;lo=p.min(0);hi=p.max(0);possible=[(name,bo)for name,(bo,bl,bh)in bones.items()if((lo<=bh)&(hi>=bl)).all()]
 if not possible:continue
 vo=ob(p,f)
 for name,bo in possible:
  report['candidateBoneVesselPairs']+=1;r=fcl.CollisionResult();count=fcl.collide(bo,vo,fcl.CollisionRequest(num_max_contacts=250,enable_contact=True),r)
  if count:
   pp=np.array([c.pos for c in r.contacts]);rec={'vessel':sid,'bone':name,'system':s['system'],'potentialConnection':s.get('displayGroup')=='anastomoses','sampledContacts':count,'truncatedAt':250,'bounds':[pp.min(0).tolist(),pp.max(0).tolist()],'status':'requires-anatomical-review','interpretation':'Surface crossings or apposition in the delivered teaching meshes; this screen does not establish penetration depth or an incorrect anatomical course.'};report['vascularBoneContacts'].append(rec);print('Contact',sid,name,count,flush=True)
report['scope']='Every delivered mesh array; all artery/vein meshes against all represented craniofacial bones including teeth and hyoid. This is a broad surface screen, not clinical or histological validation.'
(A/'docs/foramina-batch8-whole-model-validation.json').write_text(json.dumps(report,indent=2));print('SUMMARY',len(report['meshes']),'meshes',report['vascularMeshesScreened'],'vessels',len(report['vascularBoneContacts']),'contact pairs',flush=True);assert not report['structuralErrors']
