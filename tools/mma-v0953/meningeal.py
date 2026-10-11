"""Paired anterior MMA channels, a common extracranial outlet and one
communication to the existing lesser-sphenoid-wing sinus.
"""
from geometry import *
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter,gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
revision=json.loads((OUT/'revision.json').read_text());routes=[]
revision['newLabels']=[n for n in revision['newLabels'] if not n.startswith('vein.middle_meningeal.')]
revision['changed']=[r for r in revision['changed'] if not r['node'].startswith('vein.middle_meningeal.')]
def resample(q,step=.22):
 keep=np.r_[True,np.linalg.norm(np.diff(q,axis=0),axis=1)>1e-5];q=q[keep];s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];return PchipInterpolator(s,q)(np.linspace(0,s[-1],max(12,int(s[-1]/step))))
def attachment(q,receiver):
 v,f=load(receiver,OUT) if (OUT/(receiver+'.positions.bin')).exists() else load(receiver);cp,d=closest(locator(v,f),q[-1:]);cp=cp[0];direction=cp-q[-1];direction/=np.linalg.norm(direction);end=cp+direction*.20;stem=resample(np.vstack([q[-min(6,len(q))],q[-1],q[-1]+(end-q[-1])*.4,end]));k=cKDTree(stem).query(q[-1])[1];return np.vstack([q,stem[k+1:]]),dict(receiver=receiver,surfaceEntryPoint=cp.tolist(),terminalCentre=end.tolist(),attachment='joined solid overlap at native receiver; exterior receiving surfaces retained')
def repel(q,r,receivers,lock_start=False):
 original=q.copy();lo=q.min(0)-2;hi=q.max(0)+2;obs=[]
 for n,file in FILES.items():
  if n in receivers or not (file in ['complete-circulation.glb','complete-anastomoses.glb'] or n.startswith(('brain.','vein.'))):continue
  v,f=load(n,OUT) if (OUT/(n+'.positions.bin')).exists() else load(n)
  if np.any(v.max(0)<lo) or np.any(v.min(0)>hi):continue
  fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f));obs.append((n,fn,v.min(0),v.max(0)))
 for _ in range(70):
  delta=np.zeros_like(q)
  for n,fn,lo,hi in obs:
   for k in np.flatnonzero(np.all(q>=lo-r-.4,axis=1)&np.all(q<=hi+r+.4,axis=1)):
    cp=[0.,0.,0.];dist=fn.EvaluateFunctionAndGetClosestPoint(q[k],cp);inside=FILES.get(n) in ['complete-circulation.glb','complete-anastomoses.glb'] or n.startswith('brain.');value=dist if inside else abs(dist)
    if value>=r+.17:continue
    normal=q[k]-cp
    if inside and dist<0:normal=-normal
    normal/=max(np.linalg.norm(normal),1e-12);delta[k]+=normal*min(r+.17-value,.20)
  delta=gaussian_filter1d(delta,1.2,axis=0);delta[-1]=0
  if lock_start:delta[0]=0
  if np.linalg.norm(delta,axis=1).max()<1e-5:break
  q+=delta*.65
 return q,float(np.linalg.norm(q-original,axis=1).max())
for side in ['right','left']:
 suffix=' left' if side=='left' else '';a=np.load(WORK/('Middle meningeal'+suffix+'.rebuilt-curve.npz'));b=np.load(WORK/('MMA frontal'+suffix+'.rebuilt-curve.npz'));q=resample(np.vstack([a['q'][a['q'][:,2]>38],b['q'][b['q'][:,2]>a['q'][-1,2]+.2]]));radius=np.r_[a['r'],b['r']];guide=np.concatenate([a['q'],b['q']]);ar=radius[cKDTree(guide).query(q)[1]]
 centre=np.array([0.,-60.,95.]);normal=centre-q;normal/=np.linalg.norm(normal,axis=1)[:,None];tangent=np.gradient(q,axis=0);sidevec=np.cross(tangent,normal);sidevec/=np.maximum(np.linalg.norm(sidevec,axis=1)[:,None],1e-12);sidevec=gaussian_filter1d(sidevec,4,axis=0);sidevec/=np.linalg.norm(sidevec,axis=1)[:,None]
 merge=smooth((q[:,2]-38)/10);base=q-normal*.20;common=q[0]+normal[0]*1.2;receiver='vein.pterygoid_plexus.'+side;sinus='vein.sphenoparietal.'+side;pair=[]
 for sign in [-1,1]:
  p=base+sidevec*sign*(ar+.52)[:,None]*merge[:,None]+normal*1.4*(1-merge[:,None]);p[0]=common;p=p[::-1];p,adj=repel(p,.18,[receiver,sinus]);pair.append(p)
 # Both channels approach one common off-artery outlet, without crossing stems.
 mergepoint=(pair[0][-1]+pair[1][-1])/2;pair[0][-1]=mergepoint;pair[1][-1]=mergepoint;stem=np.vstack([mergepoint,mergepoint+normal[0]*1.0]);stem,at=attachment(stem,receiver);stem,adj=repel(stem,.24,[receiver,sinus],lock_start=True)
 # One short communication to the native lesser-wing channel, not a duplicate.
 sv,sf=load(sinus);target=sv[np.argmax(sv[:,0] if side=='right' else -sv[:,0])];dist,k=cKDTree(pair[0]).query(target);branch=np.vstack([pair[0][k],pair[0][k]+(target-pair[0][k])*.5]);branch,sa=attachment(branch,sinus);branch,adj2=repel(branch,.17,[receiver,sinus],lock_start=True)
 paths=pair+[stem,branch];rads=[.18,.18,.24,.17];allq=np.concatenate(paths);lo=allq.min(0)-.8;hi=allq.max(0)+.8;dims=np.ceil((hi-lo)/.12).astype(int)+1;sp=(hi-lo)/(dims-1);field=np.full(dims,3.,np.float32)
 for p,rad in zip(paths,rads):
  p=resample(p,.18)
  for aa,bb in zip(p[:-1],p[1:]):
   pad=rad+.35;low=np.maximum(np.floor((np.minimum(aa,bb)-pad-lo)/sp).astype(int),0);high=np.minimum(np.ceil((np.maximum(aa,bb)+pad-lo)/sp).astype(int)+1,dims);sl=tuple(slice(int(x),int(y)) for x,y in zip(low,high));points=np.stack(np.meshgrid(*[lo[j]+np.arange(low[j],high[j])*sp[j] for j in range(3)],indexing='ij'),axis=-1);ab=bb-aa;t=np.clip(np.sum((points-aa)*ab,axis=-1)/max(np.dot(ab,ab),1e-12),0,1);sdf=np.linalg.norm(points-aa-t[...,None]*ab,axis=-1)-rad;field[sl]=np.minimum(field[sl],sdf)
 field=gaussian_filter(field,.45);v,f=iso(field,lo,sp)
 clean=vtk.vtkCleanPolyData();clean.SetInputData(poly(v,f));clean.SetToleranceIsAbsolute(True);clean.SetAbsoluteTolerance(1e-5);clean.Update();fill=vtk.vtkFillHolesFilter();fill.SetInputConnection(clean.GetOutputPort());fill.SetHoleSize(.12);fill.Update();tri=vtk.vtkTriangleFilter();tri.SetInputConnection(fill.GetOutputPort());tri.Update();connected=vtk.vtkPolyDataConnectivityFilter();connected.SetInputConnection(tri.GetOutputPort());connected.SetExtractionModeToLargestRegion();connected.Update();v,f=arrays(connected.GetOutput());ids,inv=np.unique(f,return_inverse=True);v=v[ids];f=inv.reshape(-1,3);node='vein.middle_meningeal.'+side;write(node,v,f)
 revision['newLabels'].append(node);revision['changed'].append(dict(node=node,file='venous.glb',vertices=len(v),triangles=len(f),topology='closed fresh paired anterior meningeal tubular union'))
 routes.append(dict(node=node,side=side,paths=[p.tolist() for p in paths],radiiMm=rads,attachments=[at,sa],scope='Selected anterior meningeal pair and shared pterygoid drainage variant; other channels and fine canal containment remain unverified'))
 print(node,len(v),len(f),flush=True)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'new-vein-paths.json').write_text(json.dumps(routes,indent=2)+'\n')
