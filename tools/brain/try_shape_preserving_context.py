"""Shape-first alternative: common Y shear, preserving all closed volumes."""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from reconcile_local_volume import VolumeMap
from refine_context_skin import save_replaced
from verify_fitting import collisions
P=APP/'.authoring/brainstem19-coordinated';W=APP/'.authoring/brainstem20-shape'
W.mkdir(exist_ok=True);z=np.load(P/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=z['origin'];m.shape=np.array(z['delta'].shape)
x,y,zz=np.meshgrid(*[np.arange(n)+o for n,o in zip(m.shape,m.origin)],indexing='ij')
w=smoothstep((zz-10)/18)*(1-smoothstep((zz-67)/20))*(1-smoothstep((np.abs(x-.65)-17)/12))*(1-smoothstep((y+50)/15))
doc,data=read_glb(P/'brain-baseline.glb');sd,sb=read_glb(P/'brain-source-refined.glb');records=mesh_records(sd,sb);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(P/'veins-baseline.glb',process=False)
for amount in [8,6,4,2]:
 m.delta=w*amount;m.mask=np.zeros(m.shape,bool);source={};target={};volumes=[];contacts=[];clival=[0,0]
 for k,r in records.items():
  if any(t in k for t in ['sulc','ventricle','aqueduct','lat-fis']):continue
  p,f=r['old'],r['faces'];q=m.apply(p)
  if np.max(np.linalg.norm(q-p,axis=1))<1e-5:continue
  a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
  if a.is_watertight:volumes.append([k,float(abs(b.volume)/abs(a.volume)-1)])
  for bk,bm in bones.geometry.items():
   n=collisions(b,bm)
   if n:contacts.append([k,bk,collisions(a,bm),n])
  if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):
   clival[0]+=collisions(veins.geometry['vein.basilar_plexus'],a);clival[1]+=collisions(veins.geometry['vein.basilar_plexus'],b)
 failures=[r for r in contacts if r[-1]>r[-2]]
 report={'amountMm':amount,'volumes':volumes,'boneContacts':contacts,'boneFailures':failures,'clival':clival};(W/f'test-{amount}.json').write_text(json.dumps(report,indent=2));print(amount,'clival',clival,'bone failures',len(failures),'volume',volumes,flush=True)
 if not failures:
  save_replaced(W/'brain-source-refined.glb',doc,data,source);save_replaced(W/'brain-trial.glb',doc,data,target);np.savez_compressed(W/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask);break
