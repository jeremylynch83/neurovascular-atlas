"""One-off mesh authoring: smooth swept profiles, union, common normals/labels."""
import json,sys,struct,hashlib
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicHermiteSpline, PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
import manifold3d as mf
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from reference import *
from morphology import fit_sinus, oriented_frames, continue_tangent
APP=ROOT.parents[1]
spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text())
lookup={s['id']:s for s in spec['structures']}; curves={};paths=[]
skull=bone_surface();loc=locator(skull);centre=np.array([.65,-65,105])
skull_sdf=vtk.vtkImplicitPolyDataDistance();skull_sdf.SetInput(skull)
bone_fields=[]
regional_fields={}
for rec in records:
 if rec['file']!='craniofacial' or 'tooth' in rec['name'] or rec['name']=='mandibular-alveolar-process':continue
 sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)))
 bone_fields.append((rec['name'],sdf,np.array(rec['bounds'])))
def profile_reference(profile):
 names=tuple(sorted(profile.get('bone_names',[])))
 if not names:return skull_sdf,loc
 if names not in regional_fields:
  app=vtk.vtkAppendPolyData()
  for rec in records:
   if rec['name'] in names:app.AddInputData(poly(*arrays(rec)))
  app.Update();pd=app.GetOutput();field=vtk.vtkImplicitPolyDataDistance();field.SetInput(pd)
  regional_fields[names]=(field,locator(pd))
 return regional_fields[names]
artery_append=vtk.vtkAppendPolyData()
for rec in records:
 if rec['file']=='complete-circulation':artery_append.AddInputData(poly(*arrays(rec)))
artery_append.Update();artery_sdf=vtk.vtkImplicitPolyDataDistance();artery_sdf.SetInput(artery_append.GetOutput())
print('Prepared retained arterial clearance reference',flush=True)
def clearance(q,r,sid):
 # The hypoglossal lumen is not resolved in this skull: preserve its explicitly
 # documented regional route rather than relocate the vein outside its canal.
 if 'anterior_condylar' in sid or 'vein.cavernous.' in sid or 'superior_ophthalmic' in sid:return q
 s=lookup[sid];mode=s['group'];target=q.copy()
 for _ in range(7):
  changes=np.zeros_like(target)
  for i,(p,rad) in enumerate(zip(target,r)):
   fields=[(name,f) for name,f,(lo,hi) in bone_fields if np.all(p>=lo-rad-1) and np.all(p<=hi+rad+1)]
   if not any(k in sid for k in ['superior_ophthalmic','sphenoparietal']):fields.append(('arteries',artery_sdf))
   near=[(name,f,f.EvaluateFunction(p)) for name,f in fields]; worst=min(near,key=lambda a:a[2])
   margin=rad*(1.14 if s['shape']=='sinus' else 1)+.35
   if worst[2]>=margin:continue
   grad=[0.,0.,0.];worst[1].EvaluateGradient(p,grad);direction=np.array(grad);direction/=max(np.linalg.norm(direction),1e-8)
   if s['side']=='midline' and sid not in ['vein.marginal','vein.basilar_plexus','vein.anterior_communicating','vein.posterior_communicating','vein.anterior_intercavernous','vein.posterior_intercavernous']:
    direction[0]=0;direction/=max(np.linalg.norm(direction),1e-8)
   if worst[2]<-.1 and worst[0]!='arteries':
    if mode in ['dural','superficial','deep','posterior'] or sid=='vein.basilar_plexus':
     c=np.array([.65,-105,63]) if 'sigmoid' in sid or 'occipital' in sid or 'inferior_hemispheric' in sid else centre
     inward=c-p;inward/=np.linalg.norm(inward)
     if np.dot(direction,inward)<.05:direction=inward
   # Short directional search stays on the chosen side of bone.
   for distance in np.arange(.4,13,.4):
    cand=p+direction*distance
    if min(f.EvaluateFunction(cand) for _,f in fields)>=margin:
     changes[i]=cand-p;break
  # Smoothed displacement avoids creating tube kinks at a collision boundary.
  target+=gaussian_filter1d(changes,1.4,axis=0,mode='nearest')
 return target
def sample(points,radius,entry_tangent=None):
 p=np.array(points,float); d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
 assert np.all(np.diff(d)>1e-5),(p,d)
 tang=np.gradient(p,d,axis=0)
 if np.linalg.norm(p[0]-p[-1])<1e-5:tang[0]=tang[-1]=(p[1]-p[-2])/(d[1]+d[-1]-d[-2])
 if entry_tangent is not None:
  direction=np.asarray(entry_tangent,float);tang[0]=direction/np.linalg.norm(direction)
 cs=CubicHermiteSpline(d,p,tang);t=np.linspace(0,d[-1],max(6,int(d[-1]/.6)+1));q=cs(t)
 arcs=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
 t2=np.linspace(0,arcs[-1],max(6,int(arcs[-1]/.65)+1));q=np.column_stack([np.interp(t2,arcs,q[:,i]) for i in range(3)])
 rr=[radius,radius] if np.isscalar(radius) else radius
 r=PchipInterpolator(np.linspace(0,1,len(rr)),rr)(np.linspace(0,1,len(q)))
 return q,r
def point(a):
 if isinstance(a,dict):
  q=curves[a['structure']][0];x=a['fraction']*(len(q)-1);i=min(int(x),len(q)-2);return q[i]*(1-(x-i))+q[i+1]*(x-i)
 return np.array(a)
def fit(q,r,mode,start_fixed,end_fixed):
 if not mode:return q
 target=q.copy()
 for i,(p,rad) in enumerate(zip(q,r)):
  v=p-centre;h=hits(loc,centre,centre+v*4)
  if not len(h):continue
  distances=np.linalg.norm(h-centre,axis=1); j=np.argmin(distances);unit=v/np.linalg.norm(v)
  # Dural channels lie along the inner table. Cortical channels sit deeper.
  margin=rad+.65+(3 if mode=='cortical' else 0)
  target[i]=centre+unit*(distances[j]-margin)
 delta=gaussian_filter1d(target-q,3,axis=0,mode='nearest')
 weights=np.ones(len(q));ramp=np.minimum(1,np.arange(len(q))/10)
 if start_fixed:weights*=ramp
 if end_fixed:weights*=ramp[::-1]
 return q+delta*weights[:,None]
todo=list(spec['structures'])
while todo:
 progressed=False
 for s in todo[:]:
  if any(isinstance(p,dict) and p['structure'] not in curves for p in s['points']):continue
  q,r=sample([point(p) for p in s['points']],s['radius'],s.get('entry_tangent'))
  if s.get('profile',{}).get('bone_apposition'):
   q=fit_sinus(q,r,s['profile'],*profile_reference(s['profile']),isinstance(s['points'][0],dict),isinstance(s['points'][-1],dict))
  else:
   q=fit(q,r,s['fit'],isinstance(s['points'][0],dict),isinstance(s['points'][-1],dict))
   q=clearance(q,r,s['id'])
  # Preserve exact collector attachments after local fitting.
  for end,step in [(0,1),(-1,-1)]:
   if isinstance(s['points'][end],dict):
    shift=point(s['points'][end])-q[end]
    for k in range(min(12,len(q)//2)):
     idx=k if step==1 else -1-k;q[idx]+=shift*(1-k/12)**2
  if s.get('continue_into'):q=continue_tangent(q,curves[s['continue_into']][0],s.get('continuation_length_mm',24))
  curves[s['id']]=(q,r);paths.append((s['id'],q,r,s['shape'],s.get('profile')));todo.remove(s);progressed=True
 if not progressed:raise ValueError('Unresolved attachments '+str([s['id'] for s in todo]))
for s in spec['structures']:
 for extra in s.get('additionalPaths',[]):
  if isinstance(extra,dict):
   p=extra['points'];radius=extra['radius'];profile=extra.get('profile')
  else:p=extra;radius=.85 if 'pterygoid' in s['id'] else .8;profile=None
  q,r=sample([point(a) for a in p],radius)
  if profile and profile.get('bone_apposition'):
   q=fit_sinus(q,r,profile,*profile_reference(profile),isinstance(p[0],dict),isinstance(p[-1],dict))
  else:q=clearance(q,r,s['id'])
  for end,step in [(0,1),(-1,-1)]:
   if isinstance(p[end],dict):
    shift=point(p[end])-q[end]
    for k in range(min(12,len(q)//2)):
     idx=k if step==1 else -1-k;q[idx]+=shift*(1-k/12)**2
  paths.append((s['id'],q,r,'round',profile))

fitted=[]
for sid,q,r,shape,profile in paths:
 row={'id':sid,'points':q.round(5).tolist(),'radii':r.round(5).tolist(),'shape':shape}
 if profile:
  row['profile']=profile;row['wallNormals']=oriented_frames(q,profile,profile_reference(profile)[0] if profile.get('bone_apposition') else None)[1].round(6).tolist()
 fitted.append(row)
(APP/'anatomy/source/venous/fitted-paths.json').write_text(json.dumps(fitted,separators=(',',':'))+'\n')
np.savez_compressed(ROOT/'venous-curves.npz',**{sid.replace('.','_'):np.c_[q,r] for sid,(q,r) in curves.items()})
if '--paths-only' in sys.argv:
 print('Exported fitted paths',len(paths),flush=True);sys.exit(0)

def tube(q,r,shape='round',n=20):
 tangent=np.gradient(q,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 norms=[];v=np.array([1.,0,0]);v-=tangent[0]*np.dot(v,tangent[0]);
 if np.linalg.norm(v)<.1:v=np.array([0.,1,0]);v-=tangent[0]*np.dot(v,tangent[0])
 v/=np.linalg.norm(v)
 for t in tangent:
  v-=t*np.dot(v,t);v/=np.linalg.norm(v);norms.append(v.copy())
 norms=np.array(norms);bins=np.cross(tangent,norms)
 theta=np.arange(n)*2*np.pi/n;profile=1+.12*np.cos(3*theta) if shape=='sinus' else np.ones(n)
 pts=q[:,None,:]+r[:,None,None]*profile[None,:,None]*(norms[:,None,:]*np.cos(theta)[None,:,None]+bins[:,None,:]*np.sin(theta)[None,:,None])
 pts=pts.reshape(-1,3);faces=[]
 for i in range(len(q)-1):
  for j in range(n):
   a=i*n+j;b=i*n+(j+1)%n;c=b+n;d=a+n;faces.extend([[a,b,d],[b,c,d]])
 # Flat terminal caps exist only at genuinely truncated/open-system ends;
 # union removes internal caps at every attached junction.
 a=len(pts);b=a+1;pts=np.vstack([pts,q[0],q[-1]])
 for j in range(n):faces.extend([[a,(j+1)%n,j],[b,(len(q)-1)*n+j,(len(q)-1)*n+(j+1)%n]])
 return pts.astype(np.float32),np.array(faces,dtype=np.uint32)

print('Curves',len(curves),'paths',len(paths),flush=True)
ids=list(lookup);original=mf.Manifold.reserve_ids(len(ids));solids=[]
for sid,q,r,shape,profile in paths:
 p,f=tube(q,r,shape)
 mesh=mf.Mesh(p,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([original+ids.index(sid)],np.uint32))
 solid=mf.Manifold(mesh)
 if solid.is_empty():raise RuntimeError(f'{sid}: {solid.status()}')
 solids.append(solid)
joined=mf.Manifold.batch_boolean(solids,mf.OpType.Add)
for side in ['right','left']:
 cavity=np.load(ROOT/f'ica-cavity-{side}.npz');cp=cavity['positions'];cf=cavity['faces']
 cut=mf.Manifold(mf.Mesh(cp,cf,run_index=np.array([0,len(cf)*3],np.uint32),run_original_id=np.array([original+ids.index('vein.cavernous.'+side)],np.uint32)))
 assert cut.status()==mf.Error.NoError
 joined=joined-cut
 bonefile=ROOT/f'cavernous-bone-{side}.npz'
 if bonefile.exists():
  cavity=np.load(bonefile);cp=cavity['positions'];cf=cavity['faces']
  cut=mf.Manifold(mf.Mesh(cp,cf,run_index=np.array([0,len(cf)*3],np.uint32),run_original_id=np.array([original+ids.index('vein.cavernous.'+side)],np.uint32)))
  assert cut.status()==mf.Error.NoError
  joined=joined-cut
print('Union',joined.num_tri(),'status',joined.status(),flush=True)
m=joined.to_mesh();p=np.array(m.vert_properties[:,:3]);f=np.array(m.tri_verts);labels=np.zeros(len(f),np.int32)
for i,oid in enumerate(m.run_original_id):labels[m.run_index[i]//3:m.run_index[i+1]//3]=int(oid)-original
# Remove isolated boolean slivers and enclosed bubbles, retaining every named
# structure on the principal connected venous surface.
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
edges=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]])
_,component=connected_components(coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(p),len(p))).tocsr(),directed=False)
counts=np.bincount(component[f[:,0]]);keep=component[f[:,0]]==counts.argmax();removed=int((~keep).sum());f=f[keep];labels=labels[keep]
used,inv=np.unique(f,return_inverse=True);p=p[used];f=inv.reshape(-1,3).astype(np.uint32)
assert len(np.unique(labels))==len(ids)
# Gentle common-surface fairing keeps endpoints and label boundaries continuous.
pd=poly(p,f);sm=vtk.vtkWindowedSincPolyDataFilter();sm.SetInputData(pd);sm.SetNumberOfIterations(8);sm.SetPassBand(.12);sm.BoundarySmoothingOff();sm.FeatureEdgeSmoothingOff();sm.NonManifoldSmoothingOff();sm.NormalizeCoordinatesOn();sm.Update();p=vtk_to_numpy(sm.GetOutput().GetPoints().GetData()).astype(np.float32)
# Smooth normals are computed globally before splitting selectable surfaces.
vnorm=np.zeros_like(p);fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
for k in range(3):np.add.at(vnorm,f[:,k],fn)
vnorm/=np.maximum(np.linalg.norm(vnorm,axis=1)[:,None],1e-12)
np.savez_compressed(ROOT/'venous-mesh.npz',positions=p,faces=f,normals=vnorm,labels=labels)
np.savez_compressed(ROOT/'venous-curves.npz',**{sid.replace('.','_'):np.c_[q,r] for sid,(q,r) in curves.items()})

# Small, self-contained GLB with one named mesh per selectable structure.
doc={'asset':{'version':'2.0','generator':'Neurovascular Atlas venous authoring v0.9.0'},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'accessors':[],'bufferViews':[],'buffers':[]}
chunks=[];offset=0
def acc(arr,typ,component,target,bounds=False):
 global offset
 arr=np.ascontiguousarray(arr);raw=arr.tobytes();pad=(-len(raw))%4
 bv=len(doc['bufferViews']);doc['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw),'target':target});chunks.append(raw+b'\0'*pad);offset+=len(raw)+pad
 a={'bufferView':bv,'componentType':component,'count':len(arr),'type':typ}
 if bounds:a.update(min=arr.min(axis=0).tolist(),max=arr.max(axis=0).tolist())
 doc['accessors'].append(a);return len(doc['accessors'])-1
stats=[]
for i,sid in enumerate(ids):
 ff=f[labels==i];assert len(ff)>0,sid
 used,inv=np.unique(ff,return_inverse=True);pp=p[used];nn=vnorm[used];ix=inv.ravel().astype(np.uint32)
 pos=acc(pp,'VEC3',5126,34962,True);nor=acc(nn,'VEC3',5126,34962);ind=acc(ix,'SCALAR',5125,34963)
 idx=len(doc['meshes']);doc['meshes'].append({'name':sid,'primitives':[{'attributes':{'POSITION':pos,'NORMAL':nor},'indices':ind}]});doc['nodes'].append({'name':sid,'mesh':idx});doc['scenes'][0]['nodes'].append(idx)
 stats.append({'id':sid,'vertices':len(pp),'triangles':len(ff)})
doc['buffers']=[{'byteLength':offset}];j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4);b=b''.join(chunks)
dest=ROOT/'venous-raw.glb'
with dest.open('wb') as out:
 out.write(struct.pack('<4sII',b'glTF',2,28+len(j)+len(b)));out.write(struct.pack('<II',len(j),0x4e4f534a));out.write(j);out.write(struct.pack('<II',len(b),0x004e4942))
 for i in range(0,len(b),4*1024*1024):out.write(b[i:i+4*1024*1024])
assert dest.stat().st_size==28+len(j)+len(b)
(ROOT/'venous-stats.json').write_text(json.dumps({'parts':stats,'vertices':len(p),'triangles':len(f),'components':1,'removed_isolated_triangles':removed,'status':str(joined.status())},indent=2))
print('Exported',len(ids),'parts',len(f),'triangles',dest.stat().st_size,'bytes',flush=True)
