"""Transport retained arterial relationships with the accepted local map."""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import WORK,VolumeMap,split_mesh
from refine_context_skin import save_replaced

def load_map():
 a=np.load(WORK/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=a['origin'];m.delta=a['delta'];m.mask=a['mask'];m.shape=np.array(m.delta.shape);m.minimumYDerivative=float(1-np.diff(m.delta,axis=1).max());return m

def main():
 m=load_map();d,b=read_glb(APP/'.authoring/brainstem19/arteries-baseline.glb');records=mesh_records(d,b);source={};target={};changes=[]
 for k,r in records.items():
  amount=m.amount(r['old']);maximum=float(amount.max())
  if k.startswith(('ICA ','MCA ','Central')):
   print('Protected maximum',k,maximum,flush=True)
   assert maximum<1e-7,'Local map reaches protected anterior arterial geometry'
  allowed=k.startswith(('Basilar','PCA ','SCA ','AICA ','PICA ','Pontine ','Anterior spinal','Posterior spinal','Vertebral V3','Vertebral V4','VA medullary','Medial posterior choroidal','Thalamoperforator','Peduncular perforator','PCom perforator','Posterior communicating','Anterior choroidal','AChA optic tract','AChA peduncular','AChA capsular','Tuberothalamic','Anterior thalamoperforating'))
  if maximum<1e-5 or not allowed:continue
  print('Transporting',k,maximum,flush=True);p,f=split_mesh(trimesh.Trimesh(r['old'],r['faces'],process=False));q=m.apply(p);a,bm=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,bm.vertex_normals);changes.append({'node':k,'role':'retained-regional-relationship-transport','maximumDisplacementMm':float(m.amount(p).max()),'sourceTriangles':len(r['faces']),'refinedTriangles':len(f)})
 save_replaced(WORK/'arteries-source-refined.glb',d,b,source);save_replaced(WORK/'arteries-trial.glb',d,b,target);(WORK/'artery-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 print('Transported arterial labels',len(changes),flush=True)
if __name__=='__main__':main()
