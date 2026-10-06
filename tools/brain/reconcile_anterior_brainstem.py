"""Local anterior brainstem correction with an exact piecewise affine map.

Protected tissue occupies complete Y/Z grid cells. Its coordinates remain
fixed throughout each occupied cell. Original facets are split on all cell
boundaries and diagonals before mapping, so interpolation is affine on every
resulting material facet. The map is strictly ordered in Y for each Z.
"""
import json,shutil
import numpy as np,trimesh
from scipy.ndimage import distance_transform_edt
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
WORK=APP/'.authoring/brainstem19-local'
STEM={f'brain.{k}.{s}' for k in ['pons','medulla-oblongata','midbrain','base-of-peduncle'] for s in ['left','right']}

class InterfaceMap:
 def __init__(self,brain):
  self.y=np.arange(-96.,-39.,1.);self.z=np.arange(9.,92.,1.);self.dy=1.;self.dz=1.
  mask=np.zeros((len(self.y),len(self.z)),bool)
  for k,m in brain.geometry.items():
   if k in STEM or any(t in k for t in ['ventricle','sulc','lat-fis','aqueduct']):continue
   tri=m.vertices[m.faces];tri=tri[(tri[:,:,0].min(1)<22)&(tri[:,:,0].max(1)>-21)]
   lo=tri.min(1);hi=tri.max(1)
   for a,b in zip(lo,hi):
    iy0=max(0,int(np.floor(a[1]-self.y[0])));iy1=min(len(self.y)-2,int(np.floor(b[1]-self.y[0])))
    iz0=max(0,int(np.floor(a[2]-self.z[0])));iz1=min(len(self.z)-2,int(np.floor(b[2]-self.z[0])))
    if iy1>=iy0 and iz1>=iz0:mask[iy0:iy1+2,iz0:iz1+2]=True
  mask[[0,-1],:]=True;mask[:,[0,-1]]=True
  y,z=np.meshgrid(self.y,self.z,indexing='ij')
  requested=8*smoothstep((y+70)/16)*smoothstep((z-20)/10)*(1-smoothstep((z-63)/12))
  self.delta=np.minimum(requested,.7*distance_transform_edt(~mask))
  self.mask=mask
  # In each right grid triangle, the Y derivative is a row difference.
  self.minimumYDerivative=float(1-np.diff(self.delta,axis=0).max())
  assert self.minimumYDerivative>.2,'Coordinate order would fold'
 def amount(self,p):
  y=p[:,1]-self.y[0];z=p[:,2]-self.z[0];iy=np.floor(y).astype(int);iz=np.floor(z).astype(int)
  valid=(iy>=0)&(iy<len(self.y)-1)&(iz>=0)&(iz<len(self.z)-1);out=np.zeros(len(p))
  i,j=iy[valid],iz[valid];u,v=y[valid]-i,z[valid]-j;a=self.delta[i,j];b=self.delta[i+1,j];c=self.delta[i,j+1];d=self.delta[i+1,j+1]
  out[valid]=np.where(u>=v,a+(b-a)*u+(d-b)*v,a+(d-c)*u+(c-a)*v)
  return out
 def apply(self,p):
  q=p.copy();q[:,1]-=self.amount(p);return q

def clip(poly,normal,offset):
 if not len(poly):return poly
 result=[];a=poly[-1];da=float(a@normal-offset)
 for b in poly:
  db=float(b@normal-offset)
  if (da>=-1e-9)!=(db>=-1e-9):result.append(a+(b-a)*da/(da-db))
  if db>=-1e-9:result.append(b)
  a,da=b,db
 return np.array(result).reshape(-1,3)

def split_mesh(mesh,mapping):
 triangles=[]
 for t in mesh.vertices[mesh.faces]:
  lo,hi=t.min(0),t.max(0)
  # Include outside cells as well, preserving entire source facets.
  for i in range(int(np.floor(lo[1])),int(np.floor(hi[1]))+1):
   p=clip(clip(t,np.array([0,1,0]),i),np.array([0,-1,0]),-i-1)
   if len(p)<3:continue
   for j in range(int(np.floor(lo[2])),int(np.floor(hi[2]))+1):
    q=clip(clip(p,np.array([0,0,1]),j),np.array([0,0,-1]),-j-1)
    if len(q)<3:continue
    # u=v diagonal. Each side has its own affine coordinate map.
    for r in [clip(q,np.array([0,1,-1]),i-j),clip(q,np.array([0,-1,1]),j-i)]:
     for n in range(1,len(r)-1):
      tri=np.array([r[0],r[n],r[n+1]])
      if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))>1e-9:triangles.append(tri)
 p=np.array(triangles).reshape(-1,3)
 _,ids,inverse=np.unique(np.round(p,7),axis=0,return_index=True,return_inverse=True)
 return p[ids],inverse.reshape(-1,3)

def main():
 WORK.mkdir(exist_ok=True)
 for name in ['brain-baseline.glb','veins-baseline.glb','manifest-baseline.json','courses-baseline.json','landmarks-baseline.json']:
  shutil.copyfile(APP/'.authoring/brainstem19'/name,WORK/name)
 brain=trimesh.load(WORK/'brain-baseline.glb',process=False);mapping=InterfaceMap(brain)
 doc,data=read_glb(WORK/'brain-baseline.glb');records=mesh_records(doc,data);source={};target={};changes=[]
 for k in sorted(STEM):
  old=brain.geometry[k]
  if mapping.amount(old.vertices).max()<1e-5:continue
  p,f=split_mesh(old,mapping);q=mapping.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
  source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
  changes.append({'node':k,'maximumDisplacementMm':float(mapping.amount(p).max()),'sourceVertices':len(old.vertices),'refinedVertices':len(p),'sourceTriangles':len(old.faces),'refinedTriangles':len(f),'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None})
  print('Staged',k,len(p),len(f),flush=True)
 save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target)
 (WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 np.savez_compressed(WORK/'interface-map.npz',y=mapping.y,z=mapping.z,delta=mapping.delta,protectedMask=mapping.mask)
 (WORK/'map.json').write_text(json.dumps({'method':'posterior motion of anterior brainstem contour, protected tissue interfaces fixed, exact piecewise affine material facets','minimumYDerivative':mapping.minimumYDerivative,'changedContextLabels':len(changes),'brainSha256':sha(WORK/'brain-trial.glb'),'protectedStructuresExact':len(brain.geometry)-len(changes)},indent=2)+'\n')
 import reconcile_brainstem as fitting
 fitting.WORK=WORK
 changes,batches,curves=fitting.stage_shear_veins(clearance=2.2)
 (WORK/'trial.json').write_text(json.dumps({'status':'unreleased-trial','appliedToApp':False,'brainSha256':sha(WORK/'brain-trial.glb'),'veinsSha256':sha(WORK/'veins-trial.glb'),'brainChanges':json.loads((WORK/'brain-changes.json').read_text()),'veinChanges':changes,'curves':curves},indent=2)+'\n')
 print('Staged local brainstem and anterior veins',flush=True)
if __name__=='__main__':main()
