"""Recover the left posterior guide from its actual construction inputs.

The saved checkpoint accidentally contains the left anterior curve twice,
although its original posterior mesh is distinct. Validate regenerated curves
against the original mesh before routing or remeshing them.
"""
from smooth_fields import *
from vein_geometry import resample
from scipy.ndimage import gaussian_filter1d
import shutil
n='vein.middle_meningeal.posterior.left';side='left';suffix=' left'
guides=json.loads((WORK/'tree-guides.json').read_text());parts=[];radii=[];norms=[]
for base in ['Middle meningeal','MMA frontal']:
    g=next(g for g in guides if g['node']==base+suffix)
    q=np.asarray(g['oldPoints']);r=np.asarray(g['radiusMm']);normal=np.asarray(g['innerTableNormals'])
    if q[0,2]>q[-1,2]:q=q[::-1];r=r[::-1];normal=normal[::-1]
    take=q[:,2]>=49
    if parts:take&=q[:,2]>parts[-1][-1,2]+.25
    parts.append(q[take]);radii.append(r[take]);norms.append(normal[take])
raw=np.concatenate(parts);rr=np.concatenate(radii);nn=np.concatenate(norms)
original=resample(raw,.15);k=cKDTree(raw).query(original)[1]
artery=arterial_field()(original);r=rr[k];normal=gaussian_filter1d(nn[k],12,axis=0);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
tangent=np.gradient(artery,axis=0);tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-12)
transverse=np.cross(tangent,normal);transverse/=np.maximum(np.linalg.norm(transverse,axis=1)[:,None],1e-12);transverse=gaussian_filter1d(transverse,8,axis=0);transverse/=np.maximum(np.linalg.norm(transverse,axis=1)[:,None],1e-12)
if np.median(transverse[:,1])<0:transverse=-transverse
q=gaussian_filter1d(artery-transverse*(r+.5)[:,None]-normal*.15,2,axis=0);radius=.24-.045*smooth((q[:,2]-110)/35)
receiver='vein.sphenoparietal.left';rv,rf=load(receiver);j=np.argmin(abs(q[:,2]-79));cp,d=closest(locator(rv,rf),q[j:j+1]);cp=cp[0];direction=cp-q[j];direction/=max(np.linalg.norm(direction),1e-8);end=cp+direction*.35;stem=resample(np.vstack([q[j],q[j]+(end-q[j])*.3,end]),.12)
reference=WORK.parent/'work-mma-rebuild/candidate';v,f=load(n,reference);dist=closest(locator(v,f),q)[1]
assert float(np.median(dist))<.25 and float(dist.max())<.3,'Recovered curve does not follow the saved posterior mesh'
np.savez(OUT/(n+'.curve.npz'),q=q,r=radius,stem=stem)
for ext in ['positions','indices','normals']:shutil.copy2(reference/(n+'.'+ext+'.bin'),OUT/(n+'.'+ext+'.bin'))
report=dict(node=n,sourceCurveDuplicated=True,sourceMeshesDistinct=True,regeneratedCurveMedianWallDistanceMm=float(np.median(dist)),regeneratedCurveMaximumWallDistanceMm=float(dist.max()))
(OUT/'recovered-posterior-guide.json').write_text(json.dumps(report,indent=2));print(report,flush=True)

