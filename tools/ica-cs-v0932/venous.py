from model import *
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from scipy.ndimage import map_coordinates
PATHS=json.load(open(APP/'anatomy/source/venous/cavernous-junction-paths-v0.9.13.json'));PATHS={p['id']:p for p in PATHS}
STEMS=['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary'];MID=['anterior_intercavernous','posterior_intercavernous','basilar_plexus'];NAMES=['vein.'+n+'.'+s for s in ['right','left'] for n in STEMS]+['vein.'+n for n in MID]
PORTS=dict(zip(STEMS+MID,[[15.8,-54,64],[12.7,-55.5,61.8],[14,-36,75.2],[13,-40,76],[16.5,-43,70.5],[16.5,-47,63.5],[6.5,-37,72.8],[7,-51,71.5],[8.4,-54,64]]))
def keys(v):return np.ascontiguousarray(v.astype('<f4')).view('V12').ravel()
def clean(v,f):
 c=vtk.vtkCleanPolyData();c.SetInputData(poly(v,f));c.ToleranceIsAbsoluteOn();c.SetAbsoluteTolerance(1e-5);c.ConvertPolysToLinesOff();c.ConvertLinesToPointsOff();c.Update();return arrays(c.GetOutput())
def plane_clip(v,f,c,n,offset=0,positive=True,local=False):
 value=(v-c)@n-offset
 if local:value=np.minimum(value,25-np.linalg.norm(v-c,axis=1))
 return clean(*clip(v,f,value,positive))
def plane_rings(v,f,c,n,offset=0):return rings(v,f,np.flatnonzero(np.abs((v-c)@n-offset)<.001))
def phi(d):r=np.clip(d/8,0,1);return (1-r)**4*(4*r+1)
def setup():
 centres=[];delta=[];ports={};seams={}
 for side in ['right','left']:
  cv,cf=load('vein.cavernous.'+side);ck=keys(cv);loc=locator(poly(*load('outer-body.'+side,True)))
  for stem in STEMS+MID:
   name='vein.'+stem+('.'+side if stem in STEMS else '');v,f=load(name);ids=np.flatnonzero(np.isin(keys(v),ck));c=v[ids].mean(0);p=np.array(PORTS[stem],float)
   if side=='left':p[0]=-p[0]+1.3
   dest,_=closest(loc,p);centres.append(c);delta.append(dest-c);ports[name+'@'+side]=dest.tolist();seams[name+'@'+side]=c.tolist()
 centres=np.array(centres);coef=np.linalg.solve(phi(np.linalg.norm(centres[:,None]-centres[None,:],axis=2))+np.eye(len(centres))*1e-8,np.array(delta));np.savez_compressed(OUT/'venous-field.npz',centres=centres,coef=coef);(OUT/'venous-ports.json').write_text(json.dumps({'ports':ports,'seams':seams},indent=2))
def field(v):
 g=np.load(OUT/'venous-field.npz');out=np.zeros_like(v)
 for start in range(0,len(v),20000):out[start:start+20000]=phi(np.linalg.norm(v[start:start+20000,None]-g['centres'][None,:],axis=2))@g['coef']
 return out
LO=np.array([-27,-77,42.]);HI=np.array([28,-23,82.]);DIMS=np.ceil((HI-LO)/.30).astype(int)+1;SP=(HI-LO)/(DIMS-1)
def tube(q,width,depth):
 q=np.array(q);a=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];good=np.r_[True,np.diff(a)>1e-5];q=q[good];a=a[good];u=np.linspace(0,a[-1],max(4,int(a[-1]/.045)));cs=CubicSpline(a,q);qq=cs(u);t=cs(u,1);t/=np.linalg.norm(t,axis=1)[:,None];w=np.interp(u,a,np.broadcast_to(width,len(good))[good]);dep=np.interp(u,a,np.broadcast_to(depth,len(good))[good]);e=np.cross(t,[0,0,1]);k=np.linalg.norm(e,axis=1)<.05;e[k]=np.cross(t[k],[1,0,0]);e/=np.linalg.norm(e,axis=1)[:,None];b=np.cross(t,e);pad=max(w.max(),dep.max())+.8;il=np.maximum(0,np.floor((qq.min(0)-pad-LO)/SP).astype(int));ih=np.minimum(DIMS,np.ceil((qq.max(0)+pad-LO)/SP).astype(int)+1);out=np.full(DIMS,100,np.float32)
 if np.any(ih<=il):return out
 pp=np.stack(np.meshgrid(*[LO[j]+np.arange(il[j],ih[j])*SP[j] for j in range(3)],indexing='ij'),axis=-1).reshape(-1,3);dist,i=cKDTree(qq).query(pp);off=pp-qq[i];md=np.minimum(w[i],dep[i]);dd=(np.sqrt((np.sum(off*e[i],axis=1)/w[i])**2+(np.sum(off*b[i],axis=1)/dep[i])**2+(np.sum(off*t[i],axis=1)/md)**2)-1)*md;out[tuple(slice(a,b) for a,b in zip(il,ih))]=dd.reshape(ih-il);return out

def prepare():
 setup();pp=json.load(open(OUT/'venous-ports.json'));cuts={};primarykeys=[]
 for name in NAMES:
  v,f=load(name);vv=v+field(v);save(name,vv,f);primarykeys.append(v)
  if name.endswith(('right','left')):
   side=name.split('.')[-1];old=np.array(pp['seams'][name+'@'+side]);q=np.array(PATHS[name]['points']);n=old-q[0];n/=np.linalg.norm(n);choices=[]
   for ext in [9,11,13,15,18,7,5,3]:
    c=old-ext*n;rv,rf=plane_clip(vv,f,c,n,positive=False,local=True)
    try:rr=plane_rings(rv,rf,c,n)
    except RuntimeError:continue
    if len(rr)==1:choices=[c,rv,rf,rr];break
   if not choices:raise RuntimeError('No clean native vein cut '+name)
   c,rv,rf,rr=choices;save('remote.'+name,rv,rf);cuts[name]={'point':c.tolist(),'normal':n.tolist(),'rings':[rv[x].mean(0).tolist() for x in rr]};print('Cut',name,ext,len(rr),flush=True)
  elif 'basilar' in name:
   c=np.array([0,0,44.]);n=np.array([0,0,1.]);rv,rf=plane_clip(vv,f,c,n,positive=False);rr=plane_rings(rv,rf,c,n);save('remote.'+name,rv,rf);cuts[name]={'point':c.tolist(),'normal':n.tolist(),'rings':[rv[x].mean(0).tolist() for x in rr]};print('Cut basilar',len(rr),flush=True)
 # Carry only directly shared neighbour collars, keeping remote cerebral veins fixed.
 keysv=keys(np.concatenate(primarykeys));tree=cKDTree(np.concatenate(primarykeys));neighbours=[]
 for row in META:
  name=row['name']
  if row['file']!='venous.glb' or name in NAMES or 'vein.cavernous.' in name:continue
  v,f=load(name);hit=np.isin(keys(v),keysv)
  if not hit.any():continue
  d,_=cKDTree(v[hit]).query(v);weight=1-smooth(d/2);vv=v+field(v)*weight[:,None]
  if np.linalg.norm(vv-v,axis=1).max()<1e-6:continue
  save(name,vv,f);neighbours.append(name)
 (OUT/'venous-cuts.json').write_text(json.dumps(cuts,indent=2));(OUT/'venous-neighbours.json').write_text(json.dumps(neighbours,indent=2))

def network():
 pp=json.load(open(OUT/'venous-ports.json'));cuts=json.load(open(OUT/'venous-cuts.json'));labels=['vein.cavernous.right','vein.cavernous.left']+NAMES;union=np.full(DIMS,100,np.float32)
 for name in labels:
  if '--reuse' in __import__('sys').argv and 'vein.cavernous.' not in name and (OUT/(name+'.sdf.npy')).exists():
   sdf=np.load(OUT/(name+'.sdf.npy'));union=np.minimum(union,sdf);continue
  if 'vein.cavernous.' in name:
   g=np.load(OUT/('cavity-'+name.split('.')[-1]+'.npz'));xx=np.stack(np.meshgrid(*[LO[j]+np.arange(DIMS[j])*SP[j] for j in range(3)],indexing='ij'),axis=0).reshape(3,-1);sdf=map_coordinates(g['outer'],(xx-g['lo'][:,None])/g['spacing'][:,None],order=1,mode='constant',cval=100).reshape(DIMS).astype(np.float32);del xx
  elif 'basilar' in name:
   sdf=np.full(DIMS,100,np.float32);paths=[a for a in json.load(open(APP/'anatomy/source/venous/fitted-paths.json')) if a['id']==name]
   for i,a in enumerate(paths):
    q=np.array(a['points']);rr=np.array(a['radii']);qq=q+field(q)
    if i in [1,2]:
     side='right' if i==1 else 'left';dest=np.array(pp['ports'][name+'@'+side]);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];qq+=(dest-qq[0])*(1-smooth(arc/8))[:,None]
    keep=qq[:,2]>43.5
    if keep.sum()<3:continue
    sdf=np.minimum(sdf,tube(qq[keep],rr[keep]*1.35,rr[keep]*.7))
  elif name.endswith(('right','left')):
   side=name.split('.')[-1];a=PATHS[name];q=np.array(a['points']);q=q+field(q);c=np.array(cuts[name]['point']);n=np.array(cuts[name]['normal']);q=q[(q-c)@n>.8];start=np.array(cuts[name]['rings'][0]);dest=np.array(pp['ports'][name+'@'+side]);centre=np.array([11 if side=='right' else -9.7,-45,68.5]);inward=(centre-dest);inward/=np.linalg.norm(inward);q=np.concatenate([[start],q,[dest+inward*1.0]]);sdf=tube(q,a['width_radius_mm'],a['depth_radius_mm'])
  else:
   a=PATHS[name];q=np.array(a['points']);q=q+field(q);sdf=tube(q,a['width_radius_mm'],a['depth_radius_mm'])
  np.save(OUT/(name+'.sdf.npy'),sdf);union=np.minimum(union,sdf);print('Volume',name,flush=True)
 cache=OUT/'artery-network-sdf.npy'
 if cache.exists():ad=np.load(cache)
 else:
  ad=np.full(DIMS,100,np.float32)
  for side in ['right','left']:
   artery=closed(combine(['ICA rebuilt '+side,'ICA petrous '+side],True));bounds=np.array(artery.GetBounds()).reshape(3,2);il=np.maximum(0,np.floor((bounds[:,0]-.7-LO)/SP).astype(int));ih=np.minimum(DIMS,np.ceil((bounds[:,1]+.7-LO)/SP).astype(int)+1);slices=tuple(slice(a,b) for a,b in zip(il,ih));ad[slices]=np.minimum(ad[slices],sample(artery,LO+il*SP,LO+(ih-1)*SP,ih-il));print('Arterial space',side,flush=True)
  np.save(cache,ad)
 union=np.maximum(union,.30-ad);v,f=iso(union,LO,SP);fc=v[f].mean(1);best=np.full(len(f),np.inf);owner=np.zeros(len(f),int)
 for j,name in enumerate(labels):
  sdf=np.load(OUT/(name+'.sdf.npy'),mmap_mode='r');val=map_coordinates(sdf,((fc-LO)/SP).T,order=1,mode='constant',cval=100);k=val<best;best[k]=val[k];owner[k]=j
 stats=[]
 for j,name in enumerate(labels):
  ff=f[owner==j];vv=v
  if name in cuts:
   cut=cuts[name];c=np.array(cut['point']);n=np.array(cut['normal']);vv,ff=plane_clip(vv,ff,c,n,.65);lr=plane_rings(vv,ff,c,n,.65);rv,rf=load('remote.'+name,True);rr=plane_rings(rv,rf,c,n);o=len(vv);vv=np.concatenate([vv,rv]);ff=np.concatenate([ff,rf+o]);available=list(range(len(rr)));joined=0
   for a in lr:
    if not available:break
    b=min(available,key=lambda j:np.linalg.norm(vv[a].mean(0)-vv[rr[j]+o].mean(0)));available.remove(b);ff=np.concatenate([ff,bridge(vv,a,rr[b]+o)]);joined+=1
   stats.append({'name':name,'localRings':len(lr),'remoteRings':len(rr),'joined':joined,'passed':joined==len(lr)==len(rr)})
  save(name,vv,ff)
 (OUT/'venous-splices.json').write_text(json.dumps(stats,indent=2));print(stats,flush=True)
if __name__=='__main__':
 import sys
 for stage in sys.argv[1:]:
  if not stage.startswith('--'):{'prepare':prepare,'network':network}[stage]()
