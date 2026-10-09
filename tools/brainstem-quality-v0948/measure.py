from common import *
from extract_curves import extract
from types import SimpleNamespace
names=['vein.anterior_pontine','vein.transverse_pontine.left','vein.transverse_pontine.right','vein.prepontine_bridge.right']
cache={n:load(n) for n in names}
for n,(v,f) in cache.items():
 print(n,'bounds',v.min(0),v.max(0),'triangles',len(f),flush=True)
 q,r,param,tt=extract(SimpleNamespace(v=v,f=f));np.savez(WORK/(n+'.curve.npz'),q=q,r=r,param=param,tt=tt)
 print('radius',np.percentile(r,[0,10,50,90,100]),'ends',q[[0,-1]],flush=True)
for n in names:
 v,f=cache[n]
 for row in META:
  if row['file']!='venous.glb' or row['name']==n:continue
  a,b=load(row['name'])
  if np.any(a.min(0)>v.max(0)) or np.any(v.min(0)>a.max(0)):continue
  keys=lambda p:np.ascontiguousarray(p).view('V12').ravel()
  shared=v[np.isin(keys(v),keys(a))]
  if len(shared):print('interface',n,row['name'],len(shared),shared.mean(0),flush=True)
