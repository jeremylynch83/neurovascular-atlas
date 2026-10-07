"""Recover circular shaft offsets after a non-uniform placement field."""
import sys,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from extract_curves import extract
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
from vtk.util.numpy_support import vtk_to_numpy
OUT=ROOT.parent/'corrections-work';C=OUT/'candidate';R=OUT/'candidate-round';R.mkdir(exist_ok=True);revision=json.loads((C/'revision.json').read_text());quality=json.loads((C/'validation.json').read_text());changed={r['node'] for r in revision['changed']};values={n:np.fromfile(C/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float) for n in changed}
vv=[];label=[];names=[n for n,m in meshes.items() if m.file=='venous.glb']
for i,n in enumerate(names):
 v=np.unique(meshes[n].v.astype('<f4'),axis=0);vv.append(v);label.extend([i]*len(v))
allv=np.vstack(vv);_,inverse,count=np.unique(allv,axis=0,return_inverse=True,return_counts=True);shared=allv[count[inverse]>1];sharedtree=cKDTree(shared)
results=[]
for metric in quality['calibreChanges']:
 n=metric['node']
 if metric['p95AbsoluteFractionalRadiusChange']<.25:continue
 m=meshes[n];q,rad,param,tt=extract(m);stage=values[n]
 # Derive the transported centre from actual staged cross-sections, not a mapped point approximation.
 centres=[]
 for t in tt:
  mask=abs(param-t)<.3
  centres.append(stage[mask].mean(0) if mask.any() else stage[np.argsort(abs(param-t))[:16]].mean(0))
 qn=gaussian_filter1d(np.array(centres),2.,axis=0);oldtan=np.gradient(q,tt,axis=0);newtan=np.gradient(qn,tt,axis=0);oldtan/=np.maximum(np.linalg.norm(oldtan,axis=1)[:,None],1e-9);newtan/=np.maximum(np.linalg.norm(newtan,axis=1)[:,None],1e-9)
 def interp(a):return np.column_stack([np.interp(param,tt,a[:,j]) for j in range(3)])
 a=interp(oldtan);b=interp(newtan);a/=np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-9);b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-9);cross=np.cross(a,b);dot=(a*b).sum(1);offset=m.v-interp(q);rot=offset+np.cross(cross,offset)+np.cross(cross,np.cross(cross,offset))/np.maximum(1+dot,1e-6)[:,None];target=interp(qn)+rot
 distance=sharedtree.query(m.v)[0]
 # Preserve the original folded ostial neighbourhoods instead of re-sweeping them.
 col=vtk.vtkCollisionDetectionFilter();pd0=poly(stage,m.f);col.SetInputData(0,pd0);col.SetInputData(1,pd0);tr=vtk.vtkTransform();col.SetTransform(0,tr);col.SetTransform(1,tr);col.SetCollisionModeToAllContacts();col.Update()
 left=vtk_to_numpy(col.GetContactCells(0));right=vtk_to_numpy(col.GetContactCells(1));_,ids=np.unique(stage.astype('<f4'),axis=0,return_inverse=True);faces=ids[m.f];nonadjacent=~np.any(faces[left,:,None]==faces[right,None,:],axis=(1,2));fold_faces=np.unique(np.r_[left[nonadjacent],right[nonadjacent]])
 fold_vertices=np.unique(m.f[fold_faces]);fold_distance=cKDTree(m.v[fold_vertices]).query(m.v)[0] if len(fold_vertices) else np.full(len(m.v),np.inf)
 w=smooth((np.minimum(param-tt[0],tt[-1]-param)-1)/2)*smooth(distance/1.3)*smooth((fold_distance-2)/2);v=stage+(target-stage)*w[:,None];values[n]=v
 results.append({'node':n,'maximumRoundRecoveryMm':float(np.linalg.norm(v-stage,axis=1).max()),'protectedFoldVertices':int((fold_distance<=2).sum()),'sharedBoundaryVerticesRetained':bool(np.all(v[distance<1e-7]==stage[distance<1e-7]))});print('ROUND',results[-1],flush=True)
pd={n:poly(v,meshes[n].f) for n,v in values.items()};bounds={n:np.array(p.GetBounds()).reshape(3,2).T for n,p in pd.items()};new=[]
for n in [r['node'] for r in results]:
 for o,m in meshes.items():
  if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
  b=bounds.get(o,m.bounds)
  if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
  if contacts(pd[n],pd.get(o,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,o])
for n,v in values.items():v.astype('<f4').tofile(R/(n+'.positions.bin'))
r={'rounding':results,'newContacts':new};(R/'rounding.json').write_text(json.dumps(r,indent=2)+'\n');print('ROUND RESULT',r,flush=True)
