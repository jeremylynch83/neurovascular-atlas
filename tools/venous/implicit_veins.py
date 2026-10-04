"""Union venous envelopes on a local authoring grid, then partition the skin.
This is geometric meshing, not an imaging segmentation or measured voxel data.
"""
import json,struct
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from reference import ROOT,poly,records,arrays
APP=ROOT.parents[1];spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text());ids=[s['id'] for s in spec['structures']]
paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
spacing=.4
allq=[];allr=[];owners=[]
for path in paths:
 q=np.array(path['points']);r=np.array(path['radii']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];t=np.linspace(0,arc[-1],max(3,int(arc[-1]/.28)+1));dense=np.column_stack([np.interp(t,arc,q[:,i]) for i in range(3)]);rr=np.interp(t,arc,r)
 allq.append(dense);allr.append(rr);owners.append(np.full(len(t),ids.index(path['id']),np.int32))
q=np.concatenate(allq);r=np.concatenate(allr);owners=np.concatenate(owners)
lo=np.floor((q-r[:,None]-spacing*3).min(0)/spacing)*spacing;hi=np.ceil((q+r[:,None]+spacing*3).max(0)/spacing)*spacing
shape=np.ceil((hi-lo)/spacing).astype(int)+1;field=np.full(shape[::-1],50,np.float32)
print('Grid',shape.tolist(),field.nbytes,'samples',len(q),flush=True)
for p,rad in zip(q,r):
 a=np.maximum(0,np.floor((p-rad-spacing*2-lo)/spacing).astype(int));b=np.minimum(shape,np.ceil((p+rad+spacing*2-lo)/spacing).astype(int)+1)
 xx=lo[0]+np.arange(a[0],b[0])*spacing-p[0];yy=lo[1]+np.arange(a[1],b[1])*spacing-p[1];zz=lo[2]+np.arange(a[2],b[2])*spacing-p[2]
 d=np.sqrt(zz[:,None,None]**2+yy[None,:,None]**2+xx[None,None,:]**2)-rad
 block=field[a[2]:b[2],a[1]:b[1],a[0]:b[0]];np.minimum(block,d,out=block)
print('Envelope union',flush=True)
# Hollow the cavernous spaces around the retained ICA and bound their walls by
# the local sphenoid/temporal surface. These local reference masks are geometric.
for name in ['ica-cavity-right','ica-cavity-left','cavernous-bone-right','cavernous-bone-left']:
 data=np.load(ROOT/(name+'.npz'));cp=data['positions'];cf=data['faces'];sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(cp,cf))
 a=np.maximum(0,np.floor((cp.min(0)-spacing*2-lo)/spacing).astype(int));b=np.minimum(shape,np.ceil((cp.max(0)+spacing*2-lo)/spacing).astype(int)+1)
 sampler=vtk.vtkSampleFunction();sampler.SetImplicitFunction(sdf);lower=lo+a*spacing;upper=lo+(b-1)*spacing;sampler.SetModelBounds(*np.column_stack([lower,upper]).ravel());sampler.SetSampleDimensions(*(b-a));sampler.ComputeNormalsOff();sampler.Update();cut=vtk_to_numpy(sampler.GetOutput().GetPointData().GetScalars()).reshape(tuple((b-a)[::-1]))
 block=field[a[2]:b[2],a[1]:b[1],a[0]:b[0]];np.maximum(block,-cut,out=block);print('Cavity',name,flush=True)
im=vtk.vtkImageData();im.SetDimensions(*shape);im.SetOrigin(*lo);im.SetSpacing(spacing,spacing,spacing);im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(),deep=False))
contour=vtk.vtkFlyingEdges3D();contour.SetInputData(im);contour.SetValue(0,0);contour.ComputeNormalsOff();contour.Update()
connect=vtk.vtkPolyDataConnectivityFilter();connect.SetInputConnection(contour.GetOutputPort());connect.SetExtractionModeToLargestRegion();connect.Update()
smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputConnection(connect.GetOutputPort());smooth.SetNumberOfIterations(25);smooth.SetPassBand(.06);smooth.BoundarySmoothingOff();smooth.FeatureEdgeSmoothingOff();smooth.NormalizeCoordinatesOn();smooth.Update()
decimate=vtk.vtkDecimatePro();decimate.SetInputConnection(smooth.GetOutputPort());decimate.SetTargetReduction(.6);decimate.PreserveTopologyOn();decimate.SplittingOff();decimate.BoundaryVertexDeletionOff();decimate.Update()
clean=vtk.vtkCleanPolyData();clean.SetInputConnection(decimate.GetOutputPort());clean.Update();pd=clean.GetOutput();p=vtk_to_numpy(pd.GetPoints().GetData()).astype(np.float32);f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
# Remove a rare pinched internal bubble without retaining a four-face edge.
# Face connectivity across ordinary two-face edges identifies the outer skin.
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
edges=np.sort(f[:,[[0,1],[1,2],[2,0]]].reshape(-1,2),axis=1)
_,inverse,counts=np.unique(edges,axis=0,return_inverse=True,return_counts=True)
order=np.argsort(inverse);starts=np.r_[0,np.cumsum(counts)[:-1]][counts==2];faceowners=np.repeat(np.arange(len(f)),3);adj=faceowners[order[np.column_stack([starts,starts+1])]]
_,components=connected_components(coo_matrix((np.ones(len(adj)),(adj[:,0],adj[:,1])),shape=(len(f),len(f))).tocsr(),directed=False)
f=f[components==np.bincount(components).argmax()]
used,inv=np.unique(f,return_inverse=True);p=p[used];f=inv.reshape(-1,3).astype(np.uint32)
_,edgecounts=np.unique(np.sort(f[:,[[0,1],[1,2],[2,0]]].reshape(-1,2),axis=1),axis=0,return_counts=True);assert np.all(edgecounts==2)
volume=np.einsum('ij,ij->i',p[f[:,0]],np.cross(p[f[:,1]],p[f[:,2]])).sum()/6
if volume<0:f=f[:,[0,2,1]]
# Nearest envelope ownership; whole-surface normals remain shared across labels.
labelq=q[::3];labelr=r[::3];labelowner=owners[::3];tree=cKDTree(labelq);labels=[]
for start in range(0,len(f),10000):
 c=p[f[start:start+10000]].mean(1);distance,near=tree.query(c,k=48);score=distance-labelr[near];lab=labelowner[near[np.arange(len(c)),score.argmin(1)]];labels.extend(lab.tolist())
labels=np.array(labels,np.int32);missing=set(range(len(ids)))-set(labels);assert not missing,[ids[i] for i in missing]
# Fit the final skin at a few narrow bony interfaces. Centreline clearance alone
# does not guarantee clearance of the full radius. Preserve the unresolved
# hypoglossal passage rather than routing its vein around the occipital condyle.
protected=np.zeros(len(p),bool)
for side in ['right','left']:protected[np.unique(f[labels==ids.index('vein.anterior_condylar.'+side)])]=True
links=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);links=np.concatenate([links,links[:,::-1]])
adjacency=coo_matrix((np.ones(len(links)),(links[:,0],links[:,1])),shape=(len(p),len(p))).tocsr();degree=np.asarray(adjacency.sum(1)).ravel();degree[degree==0]=1
bone_fields=[]
for rec in records:
 if rec['name'] in ['bone.mandible','bone.temporal.left','bone.temporal.right','bone.occipital']:
  sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)));bone_fields.append((sdf,np.array(rec['bounds'])))
for iteration in range(12):
 delta=np.zeros_like(p);touched=0
 for sdf,(bmin,bmax) in bone_fields:
  candidates=np.flatnonzero(np.all((p>=bmin-.25)&(p<=bmax+.25),axis=1)&~protected)
  for i in candidates:
   distance=sdf.EvaluateFunction(p[i])
   if distance<.12:
    g=[0.,0.,0.];sdf.EvaluateGradient(p[i],g);g=np.array(g);g/=max(np.linalg.norm(g),1e-8);delta[i]+=g*min(.4,.18-distance);touched+=1
 if not touched:break
 for _ in range(2):delta=.7*delta+.3*(adjacency@delta)/degree[:,None]
 delta[protected]=0;p+=delta
print('Final skin fitted to bony interfaces',flush=True)
# A long reduced triangle can cross a concavity even when all three vertices
# clear it. Resolve the remaining local centroid contacts as well.
for sid,bone in [('vein.deep_facial.left','bone.mandible'),('vein.sigmoid.left','bone.temporal.left')]:
 rec=next(a for a in records if a['name']==bone);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)));ff=f[labels==ids.index(sid)]
 for _ in range(16):
  centres=p[ff].mean(1);delta=np.zeros_like(p);weights=np.zeros(len(p));bad=0
  for face,c in zip(ff,centres):
   distance=sdf.EvaluateFunction(c)
   if distance<.04:
    grad=[0.,0.,0.];sdf.EvaluateGradient(c,grad);grad=np.array(grad);grad/=max(np.linalg.norm(grad),1e-8)
    for v in face:delta[v]+=grad*min(.35,.1-distance);weights[v]+=1
    bad+=1
  if not bad:break
  weights[weights==0]=1;delta/=weights[:,None];delta=.8*delta+.2*(adjacency@delta)/degree[:,None];p+=delta
normals=np.zeros_like(p);fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
for k in range(3):np.add.at(normals,f[:,k],fn)
normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
np.savez_compressed(ROOT/'venous-mesh.npz',positions=p,faces=f,normals=normals,labels=labels)
doc={'asset':{'version':'2.0','generator':'Neurovascular Atlas venous authoring v0.9.0'},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'accessors':[],'bufferViews':[],'buffers':[]};chunks=[];offset=0
def acc(arr,typ,component,target,bounds=False):
 global offset
 arr=np.ascontiguousarray(arr);raw=arr.tobytes();pad=(-len(raw))%4;bv=len(doc['bufferViews']);doc['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw),'target':target});chunks.append(raw+b'\0'*pad);offset+=len(raw)+pad
 a={'bufferView':bv,'componentType':component,'count':len(arr),'type':typ}
 if bounds:a.update(min=arr.min(0).tolist(),max=arr.max(0).tolist())
 doc['accessors'].append(a);return len(doc['accessors'])-1
stats=[]
for i,sid in enumerate(ids):
 ff=f[labels==i];used,inv=np.unique(ff,return_inverse=True);pp=p[used];nn=normals[used];ix=inv.ravel().astype(np.uint32)
 pos=acc(pp,'VEC3',5126,34962,True);nor=acc(nn,'VEC3',5126,34962);ind=acc(ix,'SCALAR',5125,34963);idx=len(doc['meshes']);doc['meshes'].append({'name':sid,'primitives':[{'attributes':{'POSITION':pos,'NORMAL':nor},'indices':ind}]});doc['nodes'].append({'name':sid,'mesh':idx});doc['scenes'][0]['nodes'].append(idx);stats.append({'id':sid,'vertices':len(pp),'triangles':len(ff)})
doc['buffers']=[{'byteLength':offset}];j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4);b=b''.join(chunks);dest=ROOT/'venous-raw.glb'
with dest.open('wb') as out:
 out.write(struct.pack('<4sII',b'glTF',2,28+len(j)+len(b)));out.write(struct.pack('<II',len(j),0x4e4f534a));out.write(j);out.write(struct.pack('<II',len(b),0x004e4942))
 for i in range(0,len(b),4*1024*1024):out.write(b[i:i+4*1024*1024])
assert dest.stat().st_size==28+len(j)+len(b)
(ROOT/'venous-stats.json').write_text(json.dumps({'parts':stats,'vertices':len(p),'triangles':len(f),'components':1,'authoring_grid_mm':spacing,'method':'Implicit envelope union, common-surface smoothing and topology-preserving reduction; not imaging data'},indent=2))
print('Exported',len(ids),len(p),len(f),dest.stat().st_size,flush=True)
