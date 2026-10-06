"""Exact ordered AP-size registration confined to the lower posterior fossa.

Upper midbrain/optic interfaces stay fixed. AP size changes are intentional and
bounded by the ordered map. Material source facets use the recovered exact grid.
"""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,smoothstep,accessor
from reconcile_local_volume import VolumeMap
from refine_context_skin import save_replaced
from constrain_reconciliation import freeze
from reconcile_brainstem import sha
P=APP/'.authoring/brainstem19-coordinated';W=APP/'.authoring/brainstem20-space'
W.mkdir(exist_ok=True);v=np.load(P/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.shape=np.array(v['delta'].shape);m.mask=v['mask'].copy()
veins=trimesh.load(P/'veins-baseline.glb',process=False)
freeze(m.mask,m.origin,veins,{'vein.occipital_sinus','vein.inferior_vermian.left','vein.inferior_vermian.right','vein.inferior_hemispheric.left','vein.inferior_hemispheric.right'})
# Keep posterior marginal sinus relations stationary, while allowing the
# anterior medullary/clival overlap to be corrected by motion away from it.
a=veins.geometry['vein.marginal'];f=a.faces[np.all(a.triangles[:,:,1]<-90,axis=1)]
if len(f):freeze(m.mask,m.origin,trimesh.Scene({'marginal':trimesh.Trimesh(a.vertices,f,process=False)}),{'marginal'})
x,y,z=np.meshgrid(*[np.arange(n)+o for n,o in zip(m.shape,m.origin)],indexing='ij')
w=smoothstep((z-8)/16)*(1-smoothstep((z-67)/15))*(1-smoothstep((np.abs(x-.65)-18)/10))
# Six percent AP reduction around a posterior reference, with the AP component
# of a two-degree sagittal rotation. No transverse or vertical resizing.
a=np.deg2rad(-2);desired=y-(-110+.88*((y+110)*np.cos(a)-(z-65)*np.sin(a)))
m.delta=desired*w;m.delta[m.mask]=0
# Enforce .85 <= dY'/dY <= 1.15 in every exact tetrahedron. Projection also
# respects every stationary interface cell.
for iteration in range(60):
 before=m.delta.copy()
 for j in range(1,m.shape[1]):m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j-1,:]-.25,m.delta[:,j-1,:]+.25);m.delta[:,j,:][m.mask[:,j,:]]=0
 for j in range(m.shape[1]-2,-1,-1):m.delta[:,j,:]=np.clip(m.delta[:,j,:],m.delta[:,j+1,:]-.25,m.delta[:,j+1,:]+.25);m.delta[:,j,:][m.mask[:,j,:]]=0
 if np.max(abs(m.delta-before))<1e-9:break
m.minimumYDerivative=float(1-np.diff(m.delta,axis=1).max());print('Derivative',m.minimumYDerivative,'max',m.delta.max(),'min',m.delta.min(),flush=True)
doc,data=read_glb(P/'brain-baseline.glb');sd,sb=read_glb(P/'brain-source-refined.glb');records=mesh_records(sd,sb);source={};target={};changes=[]
for k,r in records.items():
 p,f=r['old'],r['faces'];q=m.apply(p);maximum=float(np.linalg.norm(q-p,axis=1).max())
 if maximum<1e-5:continue
 aa,bb=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
 # Area-weighted normal accumulation avoids roundoff amplification on tiny
 # material clipping facets. The geometry itself remains independently checked.
 fn=np.cross(q[f[:,1]]-q[f[:,0]],q[f[:,2]]-q[f[:,0]]);norm=np.zeros_like(q)
 for j in range(3):np.add.at(norm,f[:,j],fn)
 norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-15)
 source[k]=(p,f,aa.vertex_normals);target[k]=(q,f,norm)
 changes.append({'node':k,'maximumDisplacementMm':maximum,'volumeChangeFraction':float(abs(bb.volume)/abs(aa.volume)-1) if aa.is_watertight else None})
save_replaced(W/'brain-source-refined.glb',doc,data,source);save_replaced(W/'brain-trial.glb',doc,data,target);np.savez_compressed(W/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
(W/'registration.json').write_text(json.dumps({'method':'lower-fossa ordered AP resizing, fixed upper midbrain, exact recovered material facets','requestedAPScale':.88,'requestedSagittalRotationDegrees':-2,'minimumYDerivative':m.minimumYDerivative,'maximumDisplacementMm':float(m.delta.max()),'brainSha256':sha(W/'brain-trial.glb'),'changes':changes},indent=2)+'\n');print('Staged lower fossa registration',flush=True)
