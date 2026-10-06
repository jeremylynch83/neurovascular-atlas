"""Continue the recovered trial with complete protected tissue/vein cells.

Uses the recovered exact material subdivision. No production writes. The
positive ordered map is retained, rather than accepting triangle-count changes
as evidence of intact tissue interfaces.
"""
import json,numpy as np,trimesh
from pathlib import Path
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap
from reconcile_brainstem import sha
from refine_context_skin import save_replaced
from fit_brainstem_shear import SELECTED
WORK=APP/'.authoring/brainstem20'
PREVIOUS=APP/'.authoring/brainstem19-coordinated'
PROTECTED=('posterior-quadrangular','semilunar','gracile','biventral','tuber-of-vermis','pyramis-of-vermis')

def freeze(mask,origin,scene,keys):
 shape=np.array(mask.shape)
 for k in keys:
  m=scene.geometry[k];tri=m.vertices[m.faces];lo=tri.min(1)-origin;hi=tri.max(1)-origin
  keep=np.all(hi>=0,axis=1)&np.all(lo<shape-1,axis=1)
  for a,b in zip(lo[keep],hi[keep]):
   low=np.maximum(0,np.floor(a).astype(int));high=np.minimum(shape-1,np.floor(b).astype(int)+1)
   mask[low[0]:high[0]+1,low[1]:high[1]+1,low[2]:high[2]+1]=True

def main():
 WORK.mkdir(exist_ok=True)
 brain=trimesh.load(PREVIOUS/'brain-baseline.glb',process=False);veins=trimesh.load(PREVIOUS/'veins-baseline.glb',process=False)
 z=np.load(PREVIOUS/'volume-map.npz');mapping=VolumeMap.__new__(VolumeMap);mapping.origin=z['origin'];mapping.shape=np.array(z['delta'].shape);mapping.mask=z['mask'].copy()
 protected={k for k in brain.geometry if any(t in k for t in PROTECTED)}
 freeze(mapping.mask,mapping.origin,brain,protected)
 # Clival/dural sinuses stay fixed. Anterior and lateral surface-vein
 # collectors are fitted separately using their genuine interface collars.
 vein_selected=SELECTED|{'vein.lateral_mesencephalic.left','vein.lateral_mesencephalic.right'}
 freeze(mapping.mask,mapping.origin,veins,set(veins.geometry)-vein_selected)
 mapping.delta=z['delta'].copy();mapping.delta[mapping.mask]=0
 for j in range(1,mapping.shape[1]):mapping.delta[:,j,:]=np.minimum(mapping.delta[:,j,:],mapping.delta[:,j-1,:]+.7)
 mapping.minimumYDerivative=float(1-np.diff(mapping.delta,axis=1).max())
 doc,data=read_glb(PREVIOUS/'brain-baseline.glb');sd,sb=read_glb(PREVIOUS/'brain-source-refined.glb');records=mesh_records(sd,sb)
 source={};target={};changes=[]
 for k,r in records.items():
  if k in protected:continue
  p,f=r['old'],r['faces'];q=mapping.apply(p);maximum=float(np.linalg.norm(q-p,axis=1).max())
  if maximum<1e-5:continue
  a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
  changes.append({'node':k,'maximumDisplacementMm':maximum,'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None,'closedSource':bool(a.is_watertight),'closedCandidate':bool(b.is_watertight)})
 save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target)
 np.savez_compressed(WORK/'volume-map.npz',origin=mapping.origin,delta=mapping.delta,mask=mapping.mask)
 (WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 (WORK/'map.json').write_text(json.dumps({'method':'recovered exact tetrahedral field with complete posterior-label and retained venous-cell protection','minimumYDerivative':mapping.minimumYDerivative,'brainSha256':sha(WORK/'brain-trial.glb'),'maximumDisplacementMm':float(mapping.delta.max()),'protectedPosteriorLabels':sorted(protected),'changes':changes},indent=2)+'\n')
 print(json.dumps(changes,indent=2),flush=True)
if __name__=='__main__':main()
