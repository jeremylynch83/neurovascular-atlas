from pathlib import Path
import sys,json,numpy as np,trimesh,fcl
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));D={};rows={r['id']:r for r in M['structures']}
for file in ['models/craniofacial.glb','models/complete-circulation.glb','models/complete-anastomoses.glb']:
 g=Glb(A/'public/anatomy'/file)
 for r in M['structures']:
  if r.get('asset',{}).get('file')==file:D[r['id']]=g.mesh(r['asset']['node'])
def ob(p,f):
 m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
bones={k:(ob(p,f),p.min(0),p.max(0))for k,(p,f,n)in D.items()if rows[k]['system']=='bone'}
report={'vessels':[],'boneTopology':{},'failures':[]}
for sid in D:
 if not sid.startswith('artery.')or not any(t in sid for t in ['descending_palatine','greater_palatine','lesser_palatine','maxillary.sphenopalatine','maxillary.pterygoid_canal','eca.pterygovaginal','eca.posterior_septal','eca.posterior_lateral_nasal','amendment.superior_septal_subdivision','amendment.inferior_septal_subdivision']):continue
 p,f,n=D[sid];vo=ob(p,f);lo=p.min(0);hi=p.max(0);contacts=[]
 for name,(bo,bl,bh)in bones.items():
  if not ((lo<=bh)&(hi>=bl)).all():continue
  r=fcl.CollisionResult();num=fcl.collide(bo,vo,fcl.CollisionRequest(num_max_contacts=1000,enable_contact=True),r)
  if num:
   pts=np.array([c.pos for c in r.contacts]);contacts.append({'bone':name,'contacts':num,'bounds':[pts.min(0).tolist(),pts.max(0).tolist()]})
 rec={'id':sid,'contacts':contacts};report['vessels'].append(rec);print(rec,flush=True)
 if contacts:report['failures'].append(sid)
for name in ['bone.sphenoid','bone.palatine.right','bone.palatine.left','bone.maxilla.right','bone.maxilla.left','bone.maxillary-alveolar-process-left','bone.maxillary-alveolar-process-right','bone.inferior_nasal_concha.right','bone.inferior_nasal_concha.left']:
 p,f,n=D[name];t=trimesh.Trimesh(p,f,process=False);bad=int(sum(np.bincount(t.edges_unique_inverse)>2));assert not bad and t.is_winding_consistent,name
 if 'maxilla.'not in name and 'alveolar-process'not in name:assert t.is_watertight,name
 report['boneTopology'][name]={'triangles':len(f),'watertight':t.is_watertight,'nonManifoldEdges':bad,'windingConsistent':t.is_winding_consistent}
(A/'docs/foramina-batch5-geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n');assert not report['failures'],report['failures']
