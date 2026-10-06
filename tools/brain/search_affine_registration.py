"""Search a small, shape-preserving posterior fossa registration family."""
import itertools,json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,accessor
from verify_fitting import collisions
from refine_context_skin import save_replaced
P=APP/'.authoring/brainstem19';W=APP/'.authoring/brainstem20-affine'
brain=trimesh.load(P/'brain-baseline.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(P/'veins-baseline.glb',process=False)
base=json.loads((W/'candidate-0.94.json').read_text());selected={c['node'] for c in base['changes']}
constraints={}
for domain,key,targets in [('bone','brainBone',bones.geometry),('tissue','brainTissue',brain.geometry),('veins','fixedDuralVeins',veins.geometry)]:
 for k,target,o,n in base[key]:constraints[(domain,k,target)]=(targets[target],o)
# Additional zero-contact pairs are verified after this inexpensive search.
stem=[k for k in selected if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]
results=[];best=None
for scale,angle,posterior in itertools.product([.94,.92,.90],[-2,-3,-4,-5],[0,1,2]):
 a=np.deg2rad(angle);rot=np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]]);centre=np.array([.65,-110,65.]);offset=np.array([0,-posterior,0]);new={k:trimesh.Trimesh(centre+(brain.geometry[k].vertices-centre)@rot.T*scale+offset,brain.geometry[k].faces,process=False) for k in selected}
 failed=[]
 for (domain,k,label),(target,o) in constraints.items():
  n=collisions(new[k],target)
  if n>o:failed.append([domain,k,label,o,n])
 clival=sum(collisions(new[k],veins.geometry['vein.basilar_plexus']) for k in stem)
 score=sum((r[-1]-r[-2])/(r[-2]+10) for r in failed)+clival
 row={'scale':scale,'rotationDegrees':angle,'posteriorTranslationMm':posterior,'centreMm':centre.tolist(),'failures':failed,'clival':clival,'score':score};results.append(row)
 if best is None or score<best['score']:best=row;print('Best',best,flush=True)
 if score==0:break
(W/'affine-search.json').write_text(json.dumps({'candidates':results,'best':best},indent=2)+'\n')
doc,data=read_glb(P/'brain-baseline.glb');records=mesh_records(doc,data);a=np.deg2rad(best['rotationDegrees']);rot=np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]]);centre=np.array(best['centreMm']);offset=np.array([0,-best['posteriorTranslationMm'],0]);target={}
for k in selected:
 r=records[k];q=centre+(r['old']-centre)@rot.T*best['scale']+offset;normal=accessor(doc,data,r['primitive']['attributes']['NORMAL']).copy()@rot.T;target[k]=(q,r['faces'],normal)
save_replaced(W/'brain-best.glb',doc,data,target);print('Search completed',best,flush=True)
