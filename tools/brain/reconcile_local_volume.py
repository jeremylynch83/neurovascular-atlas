"""Exact local brainstem deformation on a fixed-interface tetrahedral grid."""
import itertools,json,shutil
import numpy as np,trimesh
from scipy.ndimage import distance_transform_edt
from fit_vessels import APP,read_glb,smoothstep
from refine_context_skin import save_replaced
from reconcile_anterior_brainstem import clip,STEM
from reconcile_brainstem import sha
WORK=APP/'.authoring/brainstem19-coordinated'
PERMUTATIONS=list(itertools.permutations(range(3)))
def arterial_movable(k):
 return k.startswith(('Basilar','PCA ','SCA ','AICA ','PICA ','Pontine ','Anterior spinal','Posterior spinal','Vertebral V3','Vertebral V4','VA medullary','Medial posterior choroidal','Thalamoperforator','Peduncular perforator','PCom perforator','Posterior communicating','Anterior choroidal','AChA optic tract','AChA peduncular','AChA capsular','Tuberothalamic','Anterior thalamoperforating'))
class VolumeMap:
 def __init__(self,brain,lock_carotid_cells=True,lock_vascular_cells=False):
  self.origin=np.array([-25.,-154.,7.]);self.shape=np.array([52,116,86]);mask=np.zeros(self.shape,bool)
  catalogue=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
  self.selected=STEM|{r['id'] for r in catalogue['structures'] if r.get('anatomy',{}).get('category')=='cerebellum'}|{'brain.fourth-ventricle'}
  self.selected -= {'brain.folium-of-vermis'}
  protected=[(k,m) for k,m in brain.geometry.items() if k not in self.selected and not any(t in k for t in ['ventricle','sulc','lat-fis','aqueduct'])]
  arteries=trimesh.load(APP/'.authoring/brainstem19/arteries-baseline.glb',process=False)
  veins=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
  if lock_vascular_cells:
   protected += [(k,m) for k,m in arteries.geometry.items() if k.startswith(('MCA ','Central')) or (lock_carotid_cells and k.startswith('ICA '))]
   protected += [(k,m) for k,m in veins.geometry.items() if k.startswith('vein.cavernous.')]
  bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
  for k,m in bones.geometry.items():
   keep=np.all(m.vertices[m.faces,1]<-95,axis=1)
   protected.append((k,trimesh.Trimesh(m.vertices,m.faces[keep],process=False)))
  for k,m in protected:
   if not len(m.faces):continue
   tri=m.vertices[m.faces];lo=tri.min(1)-self.origin;hi=tri.max(1)-self.origin
   keep=np.all(hi>=0,axis=1)&np.all(lo<self.shape-1,axis=1)
   for a,b in zip(lo[keep],hi[keep]):
    low=np.maximum(0,np.floor(a).astype(int));high=np.minimum(self.shape-1,np.floor(b).astype(int)+1)
    mask[low[0]:high[0]+1,low[1]:high[1]+1,low[2]:high[2]+1]=True
  from scipy.spatial import cKDTree
  outside=np.concatenate([m.vertices for k,m in arteries.geometry.items() if not arterial_movable(k)])
  tree=cKDTree(outside)
  def freeze_box(a,b):
   low=np.maximum(0,np.floor(a-self.origin).astype(int));high=np.minimum(self.shape-1,np.floor(b-self.origin).astype(int)+1)
   if np.all(high>=low):mask[low[0]:high[0]+1,low[1]:high[1]+1,low[2]:high[2]+1]=True
  for k,m in (arteries.geometry.items() if lock_vascular_cells else []):
   if not arterial_movable(k):continue
   shared=tree.query(m.vertices)[0]<1e-5
   for p in m.vertices[shared]:freeze_box(p,p)
   edges=np.vstack([m.faces[:,[0,1]],m.faces[:,[1,2]],m.faces[:,[2,0]]]);edges=edges[shared[edges].all(1)]
   for edge in edges:
    p=m.vertices[edge];freeze_box(p.min(0),p.max(0))
  for d in range(3):
   sl=[slice(None)]*3;sl[d]=0;mask[tuple(sl)]=True;sl[d]=-1;mask[tuple(sl)]=True
  x,y,z=np.meshgrid(*[np.arange(n)+o for n,o in zip(self.shape,self.origin)],indexing='ij')
  lower=smoothstep((z-20)/10)*(1-smoothstep((z-63)/4))
  anterior=smoothstep((z-20)/10)*(1-smoothstep((z-67)/15))*smoothstep((y+85)/25)
  delta=8*np.maximum(lower,anterior)*(1-smoothstep((np.abs(x-.65)-18)/6))
  delta[mask]=0
  # Bound only the slope that could reverse posterior/anterior order.
  # A steep fall towards fixed anterior tissue stretches the intervening gap.
  for j in range(1,self.shape[1]):delta[:,j,:]=np.minimum(delta[:,j,:],delta[:,j-1,:]+.7)
  self.delta=delta;self.mask=mask
  self.minimumYDerivative=float(1-np.diff(self.delta,axis=1).max())
  assert self.minimumYDerivative>.2
 def amount(self,p):
  xyz=p-self.origin;i=np.floor(xyz).astype(int);v=xyz-i;out=np.zeros(len(p));valid=np.all(i>=0,axis=1)&np.all(i<self.shape-1,axis=1)
  indices=np.flatnonzero(valid);a=i[valid].copy();fraction=v[valid];order=np.argsort(-fraction,axis=1);current=self.delta[tuple(a.T)];value=current.copy()
  for k in range(3):
   ax=order[:,k];a[np.arange(len(a)),ax]+=1;following=self.delta[tuple(a.T)];value+=fraction[np.arange(len(a)),ax]*(following-current);current=following
  out[indices]=value;return out
 def apply(self,p):
  q=p.copy();q[:,1]-=self.amount(p);return q

def split_mesh(mesh):
 triangles=[]
 for face_number,t in enumerate(mesh.vertices[mesh.faces]):
  lo,hi=np.floor(t.min(0)).astype(int),np.floor(t.max(0)).astype(int)
  for i in range(lo[0],hi[0]+1):
   px=clip(clip(t,np.array([1,0,0]),i),np.array([-1,0,0]),-i-1)
   if len(px)<3:continue
   for j in range(lo[1],hi[1]+1):
    py=clip(clip(px,np.array([0,1,0]),j),np.array([0,-1,0]),-j-1)
    if len(py)<3:continue
    for k in range(lo[2],hi[2]+1):
     pz=clip(clip(py,np.array([0,0,1]),k),np.array([0,0,-1]),-k-1)
     if len(pz)<3:continue
     cell=np.array([i,j,k])
     for order in PERMUTATIONS:
      r=pz
      for a,b in zip(order[:-1],order[1:]):
       normal=np.zeros(3);normal[a]=1;normal[b]=-1;r=clip(r,normal,cell[a]-cell[b])
       if len(r)<3:break
      for n in range(1,len(r)-1):
       tri=np.array([r[0],r[n],r[n+1]])
       if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))>1e-9:triangles.append(tri)
  if face_number and face_number%2500==0:print('Material facets',face_number,'to',len(triangles),flush=True)
 p=np.array(triangles).reshape(-1,3);_,ids,inv=np.unique(np.round(p,6),axis=0,return_index=True,return_inverse=True)
 return p[ids],inv.reshape(-1,3)

def close_roundoff_holes(p,f):
 """Close only sub-micrometre clipping holes in originally closed surfaces."""
 edges=np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);unique,inv,count=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
 boundary=edges[count[inv]==1];outgoing={};incoming={}
 for a,b in boundary:outgoing.setdefault(int(a),[]).append(int(b));incoming.setdefault(int(b),[]).append(int(a))
 used=set();added=[];sizes=[]
 for start in outgoing:
  if start in used:continue
  loop=[];a=start
  for step in range(100):
   if a in loop:break
   if len(outgoing.get(a,[]))!=1 or len(incoming.get(a,[]))!=1:break
   loop.append(a);a=outgoing[a][0]
  used.update(loop)
  if a!=start or len(loop)<3:continue
  diameter=float(np.linalg.norm(np.ptp(p[loop],axis=0)))
  if diameter>1e-3:continue
  for i in range(1,len(loop)-1):added.append([loop[0],loop[i+1],loop[i]])
  sizes.append(diameter)
 return np.vstack([f,np.array(added).reshape(-1,3)]) if added else f,sizes

def main():
 WORK.mkdir(exist_ok=True)
 for name in ['brain-baseline.glb','veins-baseline.glb','manifest-baseline.json','courses-baseline.json','landmarks-baseline.json']:shutil.copyfile(APP/'.authoring/brainstem19'/name,WORK/name)
 brain=trimesh.load(WORK/'brain-baseline.glb',process=False);mapping=VolumeMap(brain);doc,data=read_glb(WORK/'brain-baseline.glb');source={};target={};changes=[]
 for k in sorted(mapping.selected):
  old=brain.geometry[k]
  if mapping.amount(old.vertices).max()<1e-5:continue
  print('Splitting',k,flush=True);p,f=split_mesh(old);closure=[]
  if old.is_watertight:f,closure=close_roundoff_holes(p,f)
  q=mapping.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
  source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
  changes.append({'node':k,'maximumDisplacementMm':float(mapping.amount(p).max()),'sourceVertices':len(old.vertices),'refinedVertices':len(p),'sourceTriangles':len(old.faces),'refinedTriangles':len(f),'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1),'roundoffHoleDiametersMm':closure,'closedSource':bool(a.is_watertight),'closedCandidate':bool(b.is_watertight)})
  print('Staged',k,len(p),len(f),flush=True)
 save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target)
 (WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n');np.savez_compressed(WORK/'volume-map.npz',origin=mapping.origin,delta=mapping.delta,mask=mapping.mask)
 (WORK/'map.json').write_text(json.dumps({'method':'fixed-interface tetrahedral map, exact source facet subdivision','minimumYDerivative':mapping.minimumYDerivative,'brainSha256':sha(WORK/'brain-trial.glb'),'changes':changes},indent=2)+'\n')
 import reconcile_brainstem as fitting;fitting.WORK=WORK;changes,batches,curves=fitting.stage_shear_veins(clearance=2.2)
 (WORK/'trial.json').write_text(json.dumps({'status':'unreleased-trial','appliedToApp':False,'brainSha256':sha(WORK/'brain-trial.glb'),'veinsSha256':sha(WORK/'veins-trial.glb'),'brainChanges':json.loads((WORK/'brain-changes.json').read_text()),'veinChanges':changes,'curves':curves},indent=2)+'\n')
 print('Staged volume trial',flush=True)
if __name__=='__main__':main()
