"""Continuous shared fields fit the full connected MMA tree, with a coordinated
local cerebral reference correction. No nearest-guide section rotations.
"""
from common import *
from diagnose import inner
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import cdist
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
sigma=9.
controls=[];shifts=[];brain_controls=[];brain_vectors=[];guides=[]
for side in ['right','left']:
 suffix=' left' if side=='left' else '';qs=[];rs=[]
 for base in ['Middle meningeal','MMA frontal']:
  x=np.load(WORK/(base+suffix+'.curve.npz'));q=x['q'];r=x['r']
  if q[0,2]>q[-1,2]:q=q[::-1];r=r[::-1]
  if qs:take=q[:,2]>qs[-1][-1,2]+.15;q=q[take];r=r[take]
  qs.append(q);rs.append(r)
 q=np.concatenate(qs);r=np.concatenate(rs);bv,bf,ns=inner(side);l=locator(bv,bf)
 cp=[];nn=[];point=[0.,0.,0.];cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.)
 def skull_point(p):
  origin=np.array([0.,-60.,95.]);direction=p-origin;direction/=np.linalg.norm(direction);t=vtk.reference(0.);pcs=[0.,0.,0.]
  hit=l.IntersectWithLine(origin,origin+direction*220,1e-6,t,point,pcs,sub,cid)
  if not hit or p[2]<54:l.FindClosestPoint(p,point,cid,sub,d2)
  return point.copy(),ns[int(cid)]
 for p in q:point0,normal0=skull_point(p);cp.append(point0);nn.append(normal0)
 cp=np.array(cp);nn=gaussian_filter1d(np.array(nn),10,axis=0);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
 delta=gaussian_filter1d(cp+nn*(r+.25)[:,None]-q,12,axis=0)*smooth((q[:,2]-45)/13)[:,None]
 # Smooth global Gaussian basis with exact coordinate sharing across branches.
 pick=np.arange(0,len(q),10);controls.append(q[pick]);shifts.append(delta[pick])
 target=q+delta;mask=q[:,2]>49
 radial=np.array([0.,-60.,95.])-cp[mask][::10];radial/=np.linalg.norm(radial,axis=1)[:,None]
 brain_controls.append(cp[mask][::10]);brain_vectors.append(radial*float(sys.argv[2] if len(sys.argv)>2 else 5.5))
 guides.append(dict(side=side,oldPoints=q.tolist(),points=target.tolist(),radiusMm=r.tolist(),innerTablePoints=cp.tolist(),innerTableNormals=nn.tolist()))
 for base in ['MMA frontal anterior division','MMA frontal posterior division','MMA posterior convexity','MMA parietal ascending','MMA posterior terminal']:
  x=np.load(WORK/(base+suffix+'.curve.npz'));bq=x['q'];br=x['r'];bp=[];bn=[]
  for p in bq:point0,normal0=skull_point(p);bp.append(point0);bn.append(normal0)
  bp=np.array(bp);bn=gaussian_filter1d(bn,9,axis=0);bn/=np.maximum(np.linalg.norm(bn,axis=1)[:,None],1e-12)
  dd=gaussian_filter1d(bp+bn*(br+.25)[:,None]-bq,9,axis=0);pick=np.arange(0,len(bq),12)
  controls.append(bq[pick]);shifts.append(dd[pick]);radial=np.array([0.,-60.,95.])-bp[pick];radial/=np.linalg.norm(radial,axis=1)[:,None];brain_controls.append(bp[pick]);brain_vectors.append(radial*float(sys.argv[2] if len(sys.argv)>2 else 5.5))
  guides.append(dict(side=side,node=base+suffix,oldPoints=bq.tolist(),points=(bq+dd).tolist(),radiusMm=br.tolist(),innerTablePoints=bp.tolist(),innerTableNormals=bn.tolist()))
c=np.concatenate(controls);d=np.concatenate(shifts)
K=np.exp(-cdist(c,c)**2/(2*sigma*sigma));coeff=np.linalg.solve(K+np.eye(len(c))*.015,d)
print('Arterial field solved',len(c),flush=True)
bc=np.concatenate(brain_controls);bd=np.concatenate(brain_vectors)
def artery_field(v):
 out=np.zeros_like(v)
 for start in range(0,len(v),12000):
  p=v[start:start+12000];k=np.exp(-cdist(p,c)**2/(2*sigma*sigma));out[start:start+len(p)]=k@coeff
 return out*smooth((v[:,2]-43)/10)[:,None]
def cortex_field(v):
 out=np.zeros_like(v)
 for start in range(0,len(v),12000):
  p=v[start:start+12000];ds=cdist(p,bc);k=np.exp(-ds**2/(2*8.**2));total=k.sum(1);out[start:start+len(p)]=(k@bd)/np.maximum(total[:,None],1e-15)*smooth((18-ds.min(1))/9)[:,None]
 return out
selected={n for n,filename in FILES.items() if filename in ['complete-circulation.glb','complete-anastomoses.glb'] and ('mma' in n.lower() or 'middle meningeal' in n.lower())}
vascular={n for n,file in FILES.items() if file in ['complete-circulation.glb','complete-anastomoses.glb']}
mesh={n:load(n) for n in FILES}
print('Meshes loaded',len(mesh),flush=True)
# Fixed collars at unaffected arterial neighbours constrain the outer support.
anchors=[]
trees={}
for n in selected:
 print('Collar controls',n,flush=True)
 v,f=mesh[n]
 for other in vascular-selected:
  w,g=mesh[other]
  if np.any(w.max(0)<v.min(0)) or np.any(w.min(0)>v.max(0)):continue
  if other not in trees:trees[other]=cKDTree(w)
  take=trees[other].query(v)[0]<1e-5
  if take.any():anchors.append(v[take][::max(1,int(take.sum()/8))])
if anchors:
 ac=np.concatenate(anchors);ac=np.unique(np.round(ac,4),axis=0)
 # Only receivers close enough to be displaced need fixed controls.
 ac=ac[np.linalg.norm(artery_field(ac),axis=1)>.001]
 if len(ac):
  c=np.concatenate([c,ac]);d=np.concatenate([d,np.zeros_like(ac)]);K=np.exp(-cdist(c,c)**2/(2*sigma*sigma));coeff=np.linalg.solve(K+np.eye(len(c))*.001,d)
changes=[];regions=[]
for n,(v,f) in mesh.items():
 if n in selected:shift=artery_field(v)
 elif n.startswith('brain.'):shift=cortex_field(v)
 elif n in vascular or n.startswith('vein.'):
  # Carry local pial vessels with the cerebral reference, fade dural tributaries
  # at their skull-fixed receiving surfaces. Low dural courses stay fixed.
  if n.startswith('vein.') and any(t in n for t in ['cavernous','sphenoparietal','sagittal','transverse','sigmoid','petrosal','pterygoid','middle_meningeal']):continue
  if n in vascular and any(t in n.lower() for t in ['meningeal','falcine','tentorial','tympanic','mastoid','transosseous','lacrimal','ophthalmic','ilt','hypophyseal','clival']):continue
  shift=cortex_field(v)
 else:continue
 if np.linalg.norm(shift,axis=1).max()<.002:continue
 q=(v+shift).astype('<f4').astype(float);write(n,q,f)
 changes.append(dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),maxShiftMm=float(np.linalg.norm(q-v,axis=1).max()),topologyExact=True,field='MMA shared Gaussian' if n in selected else 'local cerebral reference'))
 print(n,round(changes[-1]['maxShiftMm'],3),flush=True)
regions.append(dict(sigmaMm=sigma,brainSupportMm=18,brainPeakMm=float(np.linalg.norm(bd,axis=1).max()),fixedReceiverControlCount=len(ac) if anchors else 0))
revision=dict(release='0.9.53',baseline='0.9.51',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),changed=changes,newLabels=[],method='Continuous Gaussian coordinate fields across complete MMA branches and common local cerebral/pial correction; source indices retained',guides=guides,regions=regions)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(WORK/'mma-guides.json').write_text(json.dumps(guides,indent=2)+'\n')
np.savez(WORK/'coordinate-fields.npz',c=c,coeff=coeff,bc=bc,bd=bd)
