from model import *
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
paths={};targets={}
for side in ['right','left']:
 d=np.load(ROOT/('centreline-'+side+'.npz'));old=CubicSpline(np.linspace(0,1,len(d['points'])),gaussian_filter1d(d['points'],4,axis=0,mode='nearest'))
 u=np.array([0,.18,.27,.36,.44,.53,.59,.67,.75,.82,.88,1]);q=old(u);q[3:9]=[[13.6,-50,63.5],[13,-49.3,68.5],[10.2,-43.5,71.2],[8.5,-38.3,72.2],[8.8,-35.6,73.4],[10.4,-35.2,74.8]]
 if side=='left':q[3:9,0]=-(q[3:9,0]-1.3)
 q[9]=[12,-35.2,75.4] if side=='right' else [-10.7,-35.2,75.4];spl=CubicSpline(u,q-old(u),bc_type='clamped');ss=np.linspace(0,1,2500);paths[side]=(old,cKDTree(old(ss)),ss,spl);su=np.linspace(0,1,250);base=old(su)+spl(su)*((1-smooth((su-.855)/.025))*smooth((su-.16)/.10))[:,None];targets[side]=CubicSpline(su,gaussian_filter1d(base,20,axis=0,mode='nearest'))
def artery_field(v,side):
 old,tree,ss,spl=paths[side];d,i=tree.query(v);s=ss[i]
 for _ in range(4):
  q=old(s);t=old(s,1);den=(t*t).sum(1)+((q-v)*old(s,2)).sum(1);step=np.clip(((q-v)*t).sum(1)/np.maximum(den,1e-5),-.002,.002);s=np.clip(s-step,np.maximum(0,ss[i]-.008),np.minimum(1,ss[i]+.008))
 def target(s):return targets[side](s)
 q=old(s);nq=target(s);a=old(s,1);a/=np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-9);b=target(np.clip(s+.0001,0,1))-target(np.clip(s-.0001,0,1));b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-9);k=np.cross(a,b);c=(a*b).sum(1);r=v-q;rot=r+np.cross(k,r)+np.cross(k,np.cross(k,r))/np.maximum((1+c)[:,None],1e-7);w=(1-smooth((d-3)/7))*(1-smooth((s-.855)/.025))*smooth((s-.16)/.10)
 ov,_=load('Ophthalmic '+side);pv,_=load('ICA paraophthalmic '+side);sh=np.intersect1d(np.ascontiguousarray(ov.astype('<f4')).view('V12').ravel(),np.ascontiguousarray(pv.astype('<f4')).view('V12').ravel()).view('<f4').reshape(-1,3);dist,_=cKDTree(sh).query(v);w*=smooth((dist-.6)/1.1)*smooth((v[:,2]-(57.5 if side=='right' else 57.4))/1.5);return (nq+rot-v)*w[:,None]
if __name__=='__main__':
 changed=[]
 for row in META:
  n=row['name']
  if row['file']!='complete-circulation.glb' or n.startswith(('Ophthalmic ','Superior hypophyseal ','Posterior communicating ','Anterior choroidal ','PCom ','AChA ','Tuberothalamic ')):continue
  v,f=load(n);nv=v.copy()
  for side in paths:nv+=artery_field(v,side)
  if np.array_equal(nv.astype('<f4'),v.astype('<f4')):
   for suffix in ['positions','indices','normals']:(OUT/(n+'.'+suffix+'.bin')).unlink(missing_ok=True)
   continue
  save(n,nv,f);changed.append({'node':n,'file':row['file']})
 np.savez(OUT/'target-course.npz',**{s:targets[s](np.linspace(0,1,250)) for s in paths})
 (OUT/'revision.json').write_text(json.dumps({'baseVersion':'0.9.31','release':'0.9.32','changed':changed,'newLabels':[],'baselineAssetHashes':json.loads((DATA/'source-assets.json').read_text())},indent=2));print('Fitted',len(changed),'arterial labels',flush=True)
