"""Rebind the exact material arterial skin to the current staged brain field."""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records
from transport_additional_brainstem_arteries import load,W
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
old=load(APP/'.authoring/brainstem20-lower-final/volume-map.npz');new=load(W/'volume-map.npz')
def inverse(p):
 lo=p[:,1]-12;hi=p[:,1]+12
 for _ in range(36):
  q=p.copy();q[:,1]=(lo+hi)/2;less=old.apply(q)[:,1]<p[:,1];lo[less]=q[less,1];hi[~less]=q[~less,1]
 q=p.copy();q[:,1]=(lo+hi)/2;return q
d,b=read_glb(W/'arteries-source.glb');records=mesh_records(d,b);replaced={};rows=[]
for k,r in records.items():
 p,f=r['old'],r['faces'];q=new.apply(inverse(p));move=float(np.linalg.norm(q-p,axis=1).max())
 if move<1e-5:continue
 m=trimesh.Trimesh(q,f,process=False);replaced[k]=(q,f,m.vertex_normals)
 error=0
 for w in [[1/3]*3,[.5,.5,0],[.5,0,.5],[0,.5,.5]]:
  a=(p[f]*np.array(w)[None,:,None]).sum(1);c=(q[f]*np.array(w)[None,:,None]).sum(1)
  error=max(error,float(np.linalg.norm(new.apply(inverse(a))-c,axis=1).max()))
 rows.append({'node':k,'mapInterpolationErrorMm':error,'maximumDisplacementMm':move})
 print(rows[-1],flush=True)
save_replaced(W/'arteries-trial.glb',d,b,replaced)
report={'brainSha256':sha(W/'brain-trial.glb'),'fieldSha256':sha(W/'volume-map.npz'),'sourceSha256':sha(W/'arteries-source.glb'),'candidateSha256':sha(W/'arteries-trial.glb'),'minimumOldMapYDerivative':float(1-np.diff(old.delta,axis=1).max()),'minimumNewMapYDerivative':float(1-np.diff(new.delta,axis=1).max()),'geometry':rows,'appliedToApp':False}
report['interpolationPassed']=all(r['mapInterpolationErrorMm']<2e-4 for r in rows)
report['protectedAnteriorLabelsRetained']=not any(r['node'].startswith(('ICA ','MCA ','Central')) for r in rows)
(W/'arterial-map-check.json').write_text(json.dumps(report,indent=2)+'\n')
