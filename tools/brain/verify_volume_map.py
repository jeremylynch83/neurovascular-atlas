"""Verify ordered coordinate transport and the delivered material facets."""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,accessor
from reconcile_local_volume import WORK,VolumeMap
from transport_local_volume import load_map
from reconcile_brainstem import sha
from verify_fitting import collisions

brain=trimesh.load(WORK/'brain-baseline.glb',process=False);mapping=load_map();regenerated=VolumeMap(brain)
assert np.array_equal(regenerated.delta,mapping.delta),'Stale coordinate field'
assert np.max(mapping.delta[regenerated.mask])==0
assert mapping.minimumYDerivative>=.299999999
report={'status':'coordinate-map-checks','brainCandidateSha256':sha(WORK/'brain-trial.glb'),'sourceSha256':sha(WORK/'brain-source-refined.glb'),'minimumYDerivative':mapping.minimumYDerivative,'maximumDisplacementMm':float(mapping.delta.max()),'positiveOrderedCoordinateMap':True,'exactFieldReproduction':True,'geometry':[],'unchangedLabels':[],'brainBoneChecks':[],'failures':[],'limitations':['A continuous strictly Y-ordered map with X and Z fixed is injective. Applying that same map to all moving tissue, with identity on complete protected tissue cells, preserves existing interfaces and cannot introduce new intersections before coordinate quantisation.','Refined material facets are tested at their vertices, edge midpoints and centres for agreement with this piecewise affine map.','Floating point quantisation and the original overlapping atlas cuts require separate interpretation of raw triangle contact counts.','Contact checks do not establish anatomical accuracy or valid containment in open atlas surfaces.']}
sd,sb=read_glb(WORK/'brain-source-refined.glb');td,tb=read_glb(WORK/'brain-trial.glb');bd,bb=read_glb(WORK/'brain-baseline.glb');sr,tr,br=[mesh_records(d,b) for d,b in [(sd,sb),(td,tb),(bd,bb)]]
bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
for k,r in tr.items():
 p=sr[k]['old'].astype(float);q=r['old'].astype(float);f=r['faces'];assert np.array_equal(f,sr[k]['faces'])
 changed=not np.array_equal(p,q)
 if not changed:
  for a in ['POSITION','NORMAL']:assert np.array_equal(accessor(td,tb,r['primitive']['attributes'][a]),accessor(bd,bb,br[k]['primitive']['attributes'][a])),k
  assert np.array_equal(f,br[k]['faces']);report['unchangedLabels'].append(k);continue
 errors=[np.linalg.norm(mapping.apply(p)-q,axis=1).max()]
 for weights in [[1/3,1/3,1/3],[.5,.5,0],[0,.5,.5],[.5,0,.5]]:
  source=(p[f]*np.array(weights)[None,:,None]).sum(1);actual=(q[f]*np.array(weights)[None,:,None]).sum(1);errors.append(float(np.linalg.norm(mapping.apply(source)-actual,axis=1).max()))
 error=max(errors);assert error<2e-4,(k,error)
 area0=np.linalg.norm(np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]]),axis=1);area=np.linalg.norm(np.cross(q[f[:,1]]-q[f[:,0]],q[f[:,2]]-q[f[:,0]]),axis=1);robust=area0>1e-4
 assert np.isfinite(q).all() and area[robust].min()>1e-7,k
 a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
 report['geometry'].append({'node':k,'maximumMapAgreementErrorMm':error,'minimumRobustTriangleAreaRatio':float((area[robust]/area0[robust]).min()),'sourceClosed':bool(a.is_watertight),'candidateClosed':bool(b.is_watertight),'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None})
 if a.is_watertight:assert b.is_watertight,k
 for name,bone in bones.geometry.items():
  after=collisions(b,bone)
  if not after:continue
  before=collisions(a,bone);report['brainBoneChecks'].append([k,name,before,after])
  if after>before:report['failures'].append([k,'new bone contacts',name,before,after])
 print('Verified map and skull',k,error,flush=True)
report['passed']=not report['failures'];(WORK/'coordinate-map-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failures':report['failures'],'changed':len(report['geometry']),'unchanged':len(report['unchangedLabels'])},indent=2),flush=True)
assert report['passed']
