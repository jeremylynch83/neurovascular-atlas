"""Stage a common anterior brainstem/vessel shape map with fixed dural outlets."""
import argparse,json
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt,gaussian_filter
from scipy.spatial import cKDTree
from geometry import *
a=argparse.ArgumentParser();a.add_argument('--pons',type=float,default=2.5);a.add_argument('--midbrain',type=float,default=1.0);args=a.parse_args()
OUT=ROOT/'candidate';OUT.mkdir(exist_ok=True)
for old in list(OUT.glob('*.positions.bin'))+list(OUT.glob('*.gradient.bin')):old.unlink()
previous=json.loads((OUT/'revision.json').read_text())
fixed=set(previous['protectedLabels'])
f=np.load(OUT/'field.npz');xx=f['x'];zz=f['z'];front=f['front'];anchors=f['anchors']
F=RegularGridInterpolator((xx,zz),front,bounds_error=False,fill_value=None)
anchor_tree=cKDTree(anchors) if len(anchors) else None

def delta(v):
 x,y,z=v.T;dx=abs(x-.65)
 p=args.pons*np.sin(np.pi*np.clip((z-43)/29,0,1))**2
 mb=args.midbrain*np.sin(np.pi*np.clip((z-67)/23,0,1))**2
 amp=(p+mb)*(1-smooth((dx-10)/14))
 f=F(np.c_[np.clip(x,xx[0],xx[-1]),np.clip(z,zz[0],zz[-1])])
 # Plateau across the tissue surface and attached vessel walls preserves their
 # AP separation and avoids reducing lumen calibre near the stationary plexus.
 weight=smooth((y-(f-10))/9)*(1-smooth((y-(f+5))/7))
 d=amp*weight
 if anchor_tree is not None:d*=smooth(anchor_tree.query(v)[0]/6)
 return d

np.savez_compressed(OUT/'field.npz',x=xx,z=zz,front=front,anchors=anchors,pons=args.pons,midbrain=args.midbrain,anteriorPlateauOffsetMm=5)
report={'release':'0.9.22','baseline':'0.9.21','additionalPonsAmplitudeMm':args.pons,'additionalMidbrainAmplitudeMm':args.midbrain,'method':'Common smooth +Y map with rounded pontine prominence, smaller midbrain adjustment, fixed posterior tissue, and constant anterior shift across attached vessel walls. Dural collectors and clival plexus remain stationary.','fixedSharedCollarPoints':len(anchors),'changed':[],'protectedLabels':sorted(fixed),'appliedToApp':False,'anteriorPlateauOffsetMm':5}
minimum_jac=1.;max_rounding=0
for k,m in meshes.items():
 if m.file=='craniofacial.glb' or k in fixed:continue
 d=delta(m.v)
 if d.max(initial=0)<1e-5:continue
 q=m.v.copy();q[:,1]+=d;rounded=np.round(q*65536)/65536
 max_rounding=max(max_rounding,float(np.linalg.norm(q-rounded,axis=1).max()))
 m.new=rounded
 grad=[];eps=.025
 for j in range(3):
  step=np.zeros(3);step[j]=eps;grad.append((delta(m.v+step)-delta(m.v-step))/(2*eps))
 grad=np.array(grad).T;minimum_jac=min(minimum_jac,float((1+grad[:,1]).min()))
 old_tri=m.v[m.f];new_tri=m.new[m.f]
 old_area=np.linalg.norm(np.cross(old_tri[:,1]-old_tri[:,0],old_tri[:,2]-old_tri[:,0]),axis=1);new_area=np.linalg.norm(np.cross(new_tri[:,1]-new_tri[:,0],new_tri[:,2]-new_tri[:,0]),axis=1)
 robust=old_area>1e-5;ratios=new_area[robust]/old_area[robust]
 m.new.astype('<f4').tofile(OUT/(k+'.positions.bin'));grad.astype('<f4').tofile(OUT/(k+'.gradient.bin'))
 row={'node':k,'file':m.file,'maximumAdvanceMm':float(d.max()),'movedVertices':int((d>1e-5).sum()),'minimumJacobianDeterminant':float((1+grad[:,1]).min()),'minimumRobustTriangleAreaRatio':float(ratios.min()) if len(ratios) else None,'maximumRobustTriangleAreaRatio':float(ratios.max()) if len(ratios) else None}
 report['changed'].append(row);print(k,round(row['maximumAdvanceMm'],3),flush=True)
report.update(minimumSampledJacobianDeterminant=minimum_jac,maximumDeliveryRoundingMm=max_rounding,topologyUnchanged=True,plexusMeshRetained=True)
(OUT/'revision-incomplete.json').write_text(json.dumps(report,indent=2)+'\n')
assert minimum_jac>.1,minimum_jac
assert all(r['minimumRobustTriangleAreaRatio'] is None or r['minimumRobustTriangleAreaRatio']>.15 for r in report['changed'])
# Independent grid check for folding, not just mesh vertex derivatives.
pts=np.stack(np.meshgrid(np.arange(-24,26,2.),np.arange(-90,-39,1.),np.arange(42,92,1.),indexing='ij'),-1).reshape(-1,3);h=np.array([0,.025,0]);j=1+(delta(pts+h)-delta(pts-h))/.05;report['minimumGridJacobianDeterminant']=float(j.min());assert j.min()>.1,j.min()
(OUT/'revision.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged',len(report['changed']),'labels; minimum Jacobian',minimum_jac,flush=True)
