"""Shape-preserving affine registration of the connected posterior fossa.

Authorised modest size correction, evaluated against original labelled meshes.
No production write. Regional labels share exactly the same affine transform.
"""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,accessor
from reconcile_brainstem import update_normals,sha
from refine_context_skin import save_replaced
from verify_fitting import collisions
from verify_central_rebuild import outside_join_contacts
P=APP/'.authoring/brainstem19';W=APP/'.authoring/brainstem20-affine'
class FossaRegistration:
 def __init__(self,scale=.94,posterior=2):self.scale=scale;self.posterior=posterior;self.centre=np.array([.65,-110,55.])
 def apply(self,p):return self.centre+(p-self.centre)*self.scale+np.array([0,-self.posterior,0])

def main():
 W.mkdir(exist_ok=True);manifest=json.loads((P/'manifest-baseline.json').read_text());selected={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'}
 brain=trimesh.load(P/'brain-baseline.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(P/'veins-baseline.glb',process=False);doc,data=read_glb(P/'brain-baseline.glb');records=mesh_records(doc,data)
 for scale,posterior in [(.94,2),(.92,3),(.90,4)]:
  m=FossaRegistration(scale,posterior);target={};changes=[];bone_rows=[];tissue_rows=[];venous=[];clival=[0,0]
  for k in selected:
   if k not in records:continue
   r=records[k];p,f=r['old'],r['faces'];q=m.apply(p);normal=accessor(doc,data,r['primitive']['attributes']['NORMAL']).copy();target[k]=(q,f,normal);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
   changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'uniformScale':scale,'volumeRatio':float(abs(b.volume)/abs(a.volume)) if a.is_watertight else None})
   if any(t in k for t in ['ventricle','aqueduct']):continue
   for bk,bm in bones.geometry.items():
    n=collisions(b,bm);o=collisions(a,bm)
    if o or n:bone_rows.append([k,bk,o,n])
   for bk,bm in brain.geometry.items():
    if bk in selected or any(t in bk for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
    n=collisions(b,bm);o=collisions(a,bm)
    if o or n:tissue_rows.append([k,bk,o,n])
   for vk,v in veins.geometry.items():
    if vk not in ['vein.basilar_plexus','vein.occipital_sinus','vein.marginal','vein.inferior_petrosal.left','vein.inferior_petrosal.right','vein.cavernous.left','vein.cavernous.right']:continue
    n=collisions(v,b);o=collisions(v,a)
    if o or n:venous.append([k,vk,o,n])
   if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):
    clival[0]+=collisions(veins.geometry['vein.basilar_plexus'],a);clival[1]+=collisions(veins.geometry['vein.basilar_plexus'],b)
  failures=[r for r in bone_rows+tissue_rows+venous if r[-1]>r[-2]]
  report={'scale':scale,'posteriorTranslationMm':posterior,'centreMm':m.centre.tolist(),'changes':changes,'brainBone':bone_rows,'brainTissue':tissue_rows,'fixedDuralVeins':venous,'failures':failures,'clival':clival,'status':'staged-affine-size-registration','appliedToApp':False}
  save_replaced(W/f'brain-trial-{scale:.2f}.glb',doc,data,target);(W/f'candidate-{scale:.2f}.json').write_text(json.dumps(report,indent=2)+'\n');print('Affine',scale,'clival',clival,'failures',failures,flush=True)
  if not failures and not clival[1]:
   save_replaced(W/'brain-trial.glb',doc,data,target);(W/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print('Initial shape-preserving registration passed',flush=True);break
if __name__=='__main__':main()
