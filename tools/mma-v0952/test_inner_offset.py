from vein_geometry import *
from scipy.spatial.transform import Rotation
guides=json.loads((WORK/'mma-guides.json').read_text())
brain={n:load(n) for n in FILES if n.startswith('brain.')}
results=[]
for sigma,offset in [(3,.15),(3,-.15),(3,-.45)]:
 rows=[]
 for info in guides:
  side=info['side'];suffix=' left' if side=='left' else ''
  old=np.array(info['oldPoints']);cp=np.array(info['innerTablePoints']);nn=np.array(info['innerTableNormals']);r=np.array(info['radiusMm'])
  delta=gaussian_filter1d(cp+nn*(r+offset)[:,None]-old,sigma,axis=0)*smooth((old[:,2]-44)/10)[:,None];target=old+delta
  ta=np.gradient(old,axis=0);tb=np.gradient(target,axis=0);ta/=np.linalg.norm(ta,axis=1)[:,None];tb/=np.linalg.norm(tb,axis=1)[:,None];axis=np.cross(ta,tb);length=np.linalg.norm(axis,axis=1);angle=np.arctan2(length,np.einsum('ij,ij->i',ta,tb));rv=axis/np.maximum(length[:,None],1e-12)*angle[:,None]
  tree=cKDTree(old)
  for base in ['Middle meningeal','MMA frontal']:
   name=base+suffix;v,f=load(name);_,k=tree.query(v);a=np.clip(k-1,0,len(old)-2);b=np.clip(k,0,len(old)-2)
   def project(j):
    seg=old[j+1]-old[j];t=np.clip(np.einsum('ij,ij->i',v-old[j],seg)/np.maximum(np.einsum('ij,ij->i',seg,seg),1e-12),0,1);p=old[j]+seg*t[:,None];return t,p,np.linalg.norm(v-p,axis=1)
   t0,p0,d0=project(a);t1,p1,d1=project(b);take=d1<d0;j=np.where(take,b,a);t=np.where(take,t1,t0);p=np.where(take[:,None],p1,p0);weight=smooth((12-np.minimum(d0,d1))/10)
   centre=target[j]*(1-t[:,None])+target[j+1]*t[:,None];rot=rv[j]*(1-t[:,None])+rv[j+1]*t[:,None];q=v+(centre+Rotation.from_rotvec(rot).apply(v-p)-v)*weight[:,None]
   total=0
   for bn,(w,g) in brain.items():
    if np.any(w.max(0)<q.min(0)) or np.any(w.min(0)>q.max(0)):continue
    nc=contacts(q,f,w,g)
    if nc:rows.append(dict(artery=name,brain=bn,contacts=nc));total+=nc
   print(sigma,offset,name,total,flush=True)
 results.append(dict(smoothingSigmaStations=sigma,innerOffsetBeyondRadiusMm=offset,contacts=rows))
 (WORK/'inner-offset-test.json').write_text(json.dumps(results,indent=2))
