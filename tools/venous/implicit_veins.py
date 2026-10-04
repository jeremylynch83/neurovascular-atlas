"""Union venous envelopes on a local authoring grid, then partition the skin.
This is geometric meshing, not an imaging segmentation or measured voxel data.
"""
import json,struct
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy
from scipy.spatial import cKDTree
from reference import ROOT,poly,records,arrays,bone_surface
from morphology import unit
APP=ROOT.parents[1];spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text());ids=[s['id'] for s in spec['structures']]
paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
spacing=.28
allq=[];allr=[];owners=[];allt=[];alln=[];allb=[];alla=[];alld=[];allc=[];alltriangle=[]
for path in paths:
 q=np.array(path['points']);r=np.array(path['radii']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];t=np.linspace(0,arc[-1],max(3,int(arc[-1]/.22)+1));dense=np.column_stack([np.interp(t,arc,q[:,i]) for i in range(3)]);rr=np.interp(t,arc,r)
 tangent=unit(np.gradient(dense,axis=0));normal=np.zeros_like(dense);normal[:,2]=1
 profile=path.get('profile',{})
 if profile:
  raw=np.array(path['wallNormals']);normal=unit(np.column_stack([np.interp(t,arc,raw[:,i]) for i in range(3)]))
 normal=unit(normal-tangent*np.sum(normal*tangent,axis=1)[:,None]);lateral=unit(np.cross(tangent,normal))
 # Round paths use an ordinary sphere, so their frame is immaterial.
 if not profile:tangent=np.tile([0.,0.,1.],(len(t),1));normal=np.tile([0.,1.,0.],(len(t),1));lateral=np.tile([1.,0.,0.],(len(t),1))
 a=rr*profile.get('width',1);d=rr*profile.get('depth',1);c=np.maximum(.7,rr*.6) if profile else rr
 allt.append(tangent);alln.append(normal);allb.append(lateral);alla.append(a);alld.append(d);allc.append(c);alltriangle.append(np.full(len(t),profile.get('kind')=='rounded_triangle'))
 allq.append(dense);allr.append(rr);owners.append(np.full(len(t),ids.index(path['id']),np.int32))
q=np.concatenate(allq);r=np.concatenate(allr);owners=np.concatenate(owners)
tangents=np.concatenate(allt);norms=np.concatenate(alln);bins=np.concatenate(allb);widths=np.concatenate(alla);depths=np.concatenate(alld);lengths=np.concatenate(allc);triangles=np.concatenate(alltriangle)
extent=np.maximum.reduce([widths,depths,lengths])*(1+.13*triangles)
lo=np.floor((q-extent[:,None]-spacing*3).min(0)/spacing)*spacing;hi=np.ceil((q+extent[:,None]+spacing*3).max(0)/spacing)*spacing
shape=np.ceil((hi-lo)/spacing).astype(int)+1;field=np.full(shape[::-1],50,np.float32)
major_mask=np.zeros(shape[::-1],bool)
major_owners={i for i,row in enumerate(spec['structures']) if row.get('profile')}
print('Grid',shape.tolist(),field.nbytes,'samples',len(q),flush=True)
for index,(p,rad) in enumerate(zip(q,extent)):
 a=np.maximum(0,np.floor((p-rad-spacing*2-lo)/spacing).astype(int));b=np.minimum(shape,np.ceil((p+rad+spacing*2-lo)/spacing).astype(int)+1)
 xx=lo[0]+np.arange(a[0],b[0])*spacing-p[0];yy=lo[1]+np.arange(a[1],b[1])*spacing-p[1];zz=lo[2]+np.arange(a[2],b[2])*spacing-p[2]
 def dot(axis):return zz[:,None,None]*axis[2]+yy[None,:,None]*axis[1]+xx[None,None,:]*axis[0]
 u=dot(bins[index])/widths[index];v=dot(norms[index])/depths[index];w=dot(tangents[index])/lengths[index]
 rho2=u*u+v*v
 if triangles[index]:rho2/=(1-.13*np.cos(3*np.arctan2(u,v)))**2
 d=(np.sqrt(rho2+w*w)-1)*min(widths[index],depths[index],lengths[index])
 block=field[a[2]:b[2],a[1]:b[1],a[0]:b[0]];np.minimum(block,d,out=block)
 if int(owners[index]) in major_owners:major_mask[a[2]:b[2],a[1]:b[1],a[0]:b[0]]|=d<spacing*2
print('Envelope union',flush=True)
# Hollow the cavernous spaces around the retained ICA and bound their walls by
# the local sphenoid/temporal surface. These local reference masks are geometric.
for name in ['ica-cavity-right','ica-cavity-left','cavernous-bone-right','cavernous-bone-left']:
 data=np.load(ROOT/(name+'.npz'));cp=data['positions'];cf=data['faces'];sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(cp,cf))
 a=np.maximum(0,np.floor((cp.min(0)-spacing*2-lo)/spacing).astype(int));b=np.minimum(shape,np.ceil((cp.max(0)+spacing*2-lo)/spacing).astype(int)+1)
 sampler=vtk.vtkSampleFunction();sampler.SetImplicitFunction(sdf);lower=lo+a*spacing;upper=lo+(b-1)*spacing;sampler.SetModelBounds(*np.column_stack([lower,upper]).ravel());sampler.SetSampleDimensions(*(b-a));sampler.ComputeNormalsOff();sampler.Update();cut=vtk_to_numpy(sampler.GetOutput().GetPointData().GetScalars()).reshape(tuple((b-a)[::-1]))
 block=field[a[2]:b[2],a[1]:b[1],a[0]:b[0]];np.maximum(block,-cut,out=block);print('Cavity',name,flush=True)
# Intersect the major sinus envelopes with the intracranial bone boundary
# before triangulation. This avoids folds caused by moving a reduced triangle
# mesh across a suture after meshing.
major_mask&=field<spacing*2
flat=np.flatnonzero(major_mask);del major_mask
skull_sdf=vtk.vtkImplicitPolyDataDistance();skull_sdf.SetInput(bone_surface())
for start in range(0,len(flat),40000):
 ix=flat[start:start+40000];zz,yy,xx=np.unravel_index(ix,field.shape)
 points=lo+np.column_stack([xx,yy,zz])*spacing
 distance=np.array([skull_sdf.EvaluateFunction(v) for v in points],np.float32)
 field.ravel()[ix]=np.maximum(field.ravel()[ix],.20-distance)
print('Major sinus bone boundary clipped before meshing',len(flat),flush=True)
del flat
im=vtk.vtkImageData();im.SetDimensions(*shape);im.SetOrigin(*lo);im.SetSpacing(spacing,spacing,spacing);im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(),deep=False))
contour=vtk.vtkFlyingEdges3D();contour.SetInputData(im);contour.SetValue(0,0);contour.ComputeNormalsOff();contour.Update()
connect=vtk.vtkPolyDataConnectivityFilter();connect.SetInputConnection(contour.GetOutputPort());connect.SetExtractionModeToLargestRegion();connect.Update()
smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputConnection(connect.GetOutputPort());smooth.SetNumberOfIterations(25);smooth.SetPassBand(.06);smooth.BoundarySmoothingOff();smooth.FeatureEdgeSmoothingOff();smooth.NormalizeCoordinatesOn();smooth.Update()
decimate=vtk.vtkDecimatePro();decimate.SetInputConnection(smooth.GetOutputPort());decimate.SetTargetReduction(.80);decimate.PreserveTopologyOn();decimate.SplittingOff();decimate.BoundaryVertexDeletionOff();decimate.Update()
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
 c=p[f[start:start+10000]].mean(1);distance,near=tree.query(c,k=48);ix=near*3;delta=c[:,None,:]-labelq[near]
 u=np.sum(delta*bins[ix],axis=2)/widths[ix];v=np.sum(delta*norms[ix],axis=2)/depths[ix];w=np.sum(delta*tangents[ix],axis=2)/lengths[ix]
 rho2=(u*u+v*v)/(1-.13*triangles[ix]*np.cos(3*np.arctan2(u,v)))**2
 score=(np.sqrt(rho2+w*w)-1)*np.minimum.reduce([widths[ix],depths[ix],lengths[ix]])
 lab=labelowner[near[np.arange(len(c)),score.argmin(1)]];labels.extend(lab.tolist())
labels=np.array(labels,np.int32);missing=set(range(len(ids)))-set(labels);assert not missing,[ids[i] for i in missing]
# Preserve the pre-fitting skin for authoring inspection.
np.savez_compressed(ROOT/'venous-unfitted-mesh.npz',positions=p,faces=f,labels=labels)
from fit_skin import fit_skin
p=fit_skin(p,f,labels,spec)
print('Final skin fitted to intracranial bony interfaces',flush=True)
normals=np.zeros_like(p);fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
for k in range(3):np.add.at(normals,f[:,k],fn)
normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
np.savez_compressed(ROOT/'venous-mesh.npz',positions=p,faces=f,normals=normals,labels=labels)
doc={'asset':{'version':'2.0','generator':'Neurovascular Atlas venous authoring v0.9.2'},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'accessors':[],'bufferViews':[],'buffers':[]};chunks=[];offset=0
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
(ROOT/'venous-stats.json').write_text(json.dumps({'parts':stats,'vertices':len(p),'triangles':len(f),'components':1,'authoring_grid_mm':spacing,'method':'Bone-oriented sinus profiles and round venous envelopes, common-surface smoothing and topology-preserving reduction; not imaging data'},indent=2))
print('Exported',len(ids),len(p),len(f),dest.stat().st_size,flush=True)
