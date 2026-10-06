"""Authorised posterior-fossa size registration, with smooth fixed transitions.

Brainstem/cerebellar context shares one map. AP size is reduced around the
posterior fossa centre before translation, giving room without pushing the
cerebellum through the posterior skull. This deliberately changes regional
size; it does not assert tissue volume preservation or patient-specific anatomy.
"""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
from verify_fitting import collisions
P=APP/'.authoring/brainstem19-coordinated';W=APP/'.authoring/brainstem20-resized'
class ResizeMap:
 def __init__(self,ap_scale=.9,posterior_mm=4):self.ap_scale=ap_scale;self.posterior_mm=posterior_mm
 def apply(self,p):
  w=smoothstep((p[:,2]-8)/14)*(1-smoothstep((p[:,2]-68)/22))
  w*=1-smoothstep((p[:,1]+48)/15)
  w*=1-smoothstep((np.abs(p[:,0]-.65)-55)/20)
  d=np.zeros_like(p);d[:,1]=(self.ap_scale-1)*(p[:,1]+110)-self.posterior_mm
  d[:,0]=-.02*(p[:,0]-.65);d[:,2]=-.02*(p[:,2]-55)
  return p+d*w[:,None]

def main():
 W.mkdir(exist_ok=True);doc,data=read_glb(P/'brain-baseline.glb');sd,sb=read_glb(P/'brain-source-refined.glb');records=mesh_records(sd,sb)
 bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(P/'veins-baseline.glb',process=False)
 for scale,amount in [(.94,2),(.92,3),(.90,4)]:
  m=ResizeMap(scale,amount);source={};target={};changes=[];bone_rows=[];clival=[0,0]
  for k,r in records.items():
   p,f=r['old'],r['faces'];q=m.apply(p);maximum=float(np.linalg.norm(q-p,axis=1).max())
   if maximum<1e-5:continue
   a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
   changes.append({'node':k,'maximumDisplacementMm':maximum,'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None})
   if any(t in k for t in ['sulc','ventricle','aqueduct','lat-fis']):continue
   for bk,bm in bones.geometry.items():
    n=collisions(b,bm)
    if n:bone_rows.append([k,bk,collisions(a,bm),n])
   if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):
    clival[0]+=collisions(veins.geometry['vein.basilar_plexus'],a);clival[1]+=collisions(veins.geometry['vein.basilar_plexus'],b)
  failures=[r for r in bone_rows if r[-1]>r[-2]]
  report={'apScale':scale,'posteriorTranslationMm':amount,'transverseAndVerticalScale':.98,'changes':changes,'brainBoneContacts':bone_rows,'boneFailures':failures,'clival':clival,'status':'unreleased-resizing-trial','appliedToApp':False}
  (W/f'candidate-{scale:.2f}.json').write_text(json.dumps(report,indent=2)+'\n');print('Scale',scale,'clival',clival,'bone failures',failures,flush=True)
  save_replaced(W/f'brain-trial-{scale:.2f}.glb',doc,data,target)
  if not failures and clival[1]==0:
   save_replaced(W/'brain-source-refined.glb',doc,data,source);save_replaced(W/'brain-trial.glb',doc,data,target);(W/'resize-map.json').write_text(json.dumps(report,indent=2)+'\n');print('Resized brain candidate passes initial skull/clival checks',flush=True);break
if __name__=='__main__':main()
