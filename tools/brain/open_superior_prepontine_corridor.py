"""Stage a smooth, ordered local corridor correction using recovered facets."""
import json
import numpy as np
import trimesh
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from reconcile_local_volume import VolumeMap
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
W=APP/'.authoring/brainstem21-skin'
P=APP/'.authoring/brainstem20-lower-final'
W.mkdir(exist_ok=True)
v=np.load(P/'volume-map.npz');m=VolumeMap.__new__(VolumeMap)
m.origin=v['origin'];m.shape=np.array(v['delta'].shape);m.mask=v['mask'].copy();m.delta=v['delta'].copy()
x,y,z=np.meshgrid(*[np.arange(n)+o for n,o in zip(m.shape,m.origin)],indexing='ij')
extra=6.6*smoothstep((z-25)/8)*(1-smoothstep((z-69)/4))
extra*=1-smoothstep((abs(x-.65)-18)/7)
extra*=smoothstep((y+80)/15)
# The previous trial froze cells occupied by the posterior intercavernous
# sinus, including already overlapping pons. Brain motion AWAY from this
# retained sinus must not be pinned to that incorrect starting interface.
# Genuine neighbouring brain and posterior skull interface pins remain.
baseline_scene=trimesh.load(APP/'.authoring/brainstem19-coordinated/brain-baseline.glb',process=False)
# Dural sheets are retained as independent fixed obstacles. Their coarse
# occupancy cells must not prevent the adjacent brain moving away from them.
baseline_scene.geometry={k:r for k,r in baseline_scene.geometry.items() if not k.startswith('dura.')}
interface_mask=VolumeMap(baseline_scene,lock_vascular_cells=False).mask
region=(extra>0)
m.mask[region]=interface_mask[region]
extra[m.mask]=0
m.delta+=extra
# Positive AP order applies to every exact material tetrahedron.
for iteration in range(80):
 old=m.delta.copy()
 for j in range(1,m.shape[1]):
  m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j-1,:]-.3,m.delta[:,j-1,:]+.3)
  m.delta[:,j,:][m.mask[:,j,:]]=0
 for j in range(m.shape[1]-2,-1,-1):
  m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j+1,:]-.3,m.delta[:,j+1,:]+.3)
  m.delta[:,j,:][m.mask[:,j,:]]=0
 if abs(m.delta-old).max()<1e-9:break
doc,data=read_glb(APP/'.authoring/brainstem19-coordinated/brain-source-refined.glb')
records=mesh_records(doc,data)
current=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False)
replacements={};changes=[];matched={}
old_map=VolumeMap.__new__(VolumeMap);old_map.origin=v['origin'];old_map.shape=np.array(v['delta'].shape);old_map.delta=v['delta']
for k,r in records.items():
 if k.startswith('dura.'):continue
 p,f=r['old'],r['faces'];q=m.apply(p);base=current.geometry[k]
 # Copy unchanged labels from the delivered app, preserving their buffers.
 if q.shape==base.vertices.shape and abs(q-base.vertices).max()<1e-5:continue
 if not np.max(extra)>0:continue
 # Unrefined source labels outside this local field remain exact.
 if np.max(abs(q-p))<1e-5 and base.vertices.shape==p.shape:continue
 target=trimesh.Trimesh(q,f,process=False)
 fn=np.cross(q[f[:,1]]-q[f[:,0]],q[f[:,2]]-q[f[:,0]])
 normals=np.zeros_like(q)
 for j in range(3):np.add.at(normals,f[:,j],fn)
 normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-15)
 replacements[k]=(q,f,normals)
 old=old_map.apply(p);old_mesh=trimesh.Trimesh(old,f,process=False)
 matched[k]=(old,f,old_mesh.vertex_normals)
 if base.vertices.shape==q.shape:
  changes.append({'node':k,'maximumAdditionalDisplacementMm':float(np.linalg.norm(q-base.vertices,axis=1).max())})
 # The recovered source facet set is used for the staged whole asset.
base_doc,base_data=read_glb(APP/'public/anatomy/models/brain-context.glb')
save_replaced(W/'brain-trial.glb',base_doc,base_data,replacements)
save_replaced(W/'brain-matched-source.glb',base_doc,base_data,matched)
np.savez_compressed(W/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
(W/'corridor-registration.json').write_text(json.dumps({'brainSha256':sha(W/'brain-trial.glb'),
 'baselineBrainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),
 'minimumYDerivative':float(1-np.diff(m.delta,axis=1).max()),
 'changes':changes,'appliedToApp':False},indent=2)+'\n')
print(json.dumps(changes,indent=2),flush=True)
