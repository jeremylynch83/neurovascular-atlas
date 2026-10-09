"""Rebuild the four connected pontine veins as a single smooth tubular solid."""
from common import *
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import hashlib
NAMES=['vein.anterior_pontine','vein.transverse_pontine.left','vein.transverse_pontine.right','vein.prepontine_bridge.right']
def arrays(p):return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
from clearance import correct
curves=[];clearance=[];profiles=[]
for n in NAMES:
 d=np.load(WORK/(n+'.curve.npz'));q=d['q'];r=d['r'];tt=d['tt']
 # Discard tiny cap sections and smooth the illustrative native radius profile.
 r=gaussian_filter1d(np.clip(r,np.percentile(r,20),np.percentile(r,70)),4)
 r=np.minimum(r,.82 if n=='vein.anterior_pontine' else (.73 if 'transverse' in n else .31))
 if n=='vein.transverse_pontine.right':
  r+=.06*np.exp(-((q[:,0]-11.1)/1.2)**2)
 q,check=correct(q,r);check['node']=n;clearance.append(check)
 profiles.append(dict(node=n,sourceEstimatedRadiusP05MedianP95=np.percentile(d['r'],[5,50,95]).tolist(),tubeRadiusP05MedianP95=np.percentile(r,[5,50,95]).tolist(),method='Smoothed and bounded illustrative radius of native geodesic sections, with a local 0.06 mm right tributary collar allowance.'))
 curves.append([q,r])
# Explicitly reunite the original common junction using short curved stems.
# The transverse crossing retains its corrected posterior centreline.
root=np.array([2.12,-62.70,55.65])
connectors=[]
for j,(q,r) in enumerate(curves):
 k=cKDTree(q).query(root)[1]
 if j in [1,2,3]:
  k=0 if np.linalg.norm(q[0]-root)<np.linalg.norm(q[-1]-root) else len(q)-1
  length=np.linalg.norm(root-q[k]);t=np.linspace(0,1,max(5,int(length/.12)+1));connectors.append((q[k]+t[:,None]*(root-q[k]),np.linspace(r[k],min(.62,r[k]),len(t)),j))
 else:
  t=np.linspace(0,1,10);connectors.append((q[k]+t[:,None]*(root-q[k]),np.full(len(t),min(r[k],.70)),j))
allq=np.concatenate([q for q,r in curves]+[q for q,r,j in connectors]);lo=allq.min(0)-2;hi=allq.max(0)+2;spacing=.12;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1)
field=np.full(dims,5.,np.float32)
print('Grid',dims.tolist(),'voxels',int(np.prod(dims)),flush=True)
def add(q,r,blend=.28):
 for a,b,ra,rb in zip(q[:-1],q[1:],r[:-1],r[1:]):
  pad=max(ra,rb)+blend+.25;low=np.maximum(np.floor((np.minimum(a,b)-pad-lo)/sp).astype(int),0);high=np.minimum(np.ceil((np.maximum(a,b)+pad-lo)/sp).astype(int)+1,dims)
  sl=tuple(slice(int(x),int(y)) for x,y in zip(low,high));pp=np.stack(np.meshgrid(*[lo[i]+np.arange(low[i],high[i])*sp[i] for i in range(3)],indexing='ij'),axis=-1);ab=b-a;den=np.dot(ab,ab)
  t=np.clip(np.sum((pp-a)*ab,axis=-1)/max(den,1e-12),0,1);tube=np.linalg.norm(pp-a-t[...,None]*ab,axis=-1)-(ra*(1-t)+rb*t)
  # Hard minimum along each shaft prevents serial radius inflation.
  field[sl]=np.minimum(field[sl],tube)
for q,r in curves:add(q,r)
for q,r,j in connectors:add(q,r)
# A mild scalar-field smoothing creates rounded branch transitions without the
# serial smooth-min expansion of every centreline station.
from scipy.ndimage import gaussian_filter
field=gaussian_filter(field,.85)
im=vtk.vtkImageData();im.SetDimensions(*dims);im.SetOrigin(*lo);im.SetSpacing(*sp);im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(order='F'),deep=True));iso=vtk.vtkFlyingEdges3D();iso.SetInputData(im);iso.SetValue(0,0);iso.ComputeNormalsOff();iso.Update()
clean=vtk.vtkCleanPolyData();clean.SetInputConnection(iso.GetOutputPort());clean.SetTolerance(0);clean.Update()
fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputConnection(clean.GetOutputPort());fair.SetNumberOfIterations(15);fair.SetPassBand(.12);fair.BoundarySmoothingOff();fair.NonManifoldSmoothingOff();fair.NormalizeCoordinatesOn();fair.Update()
norm=vtk.vtkPolyDataNormals();norm.SetInputConnection(fair.GetOutputPort());norm.SplittingOff();norm.ConsistencyOn();norm.AutoOrientNormalsOn();norm.Update();v,f=arrays(norm.GetOutput());nn=vtk_to_numpy(norm.GetOutput().GetPointData().GetNormals())
v=v.astype('<f4');f=f.astype('<u4');np.savez(OUT/'network.npz',v=v,f=f,normals=nn)
# Assign each exterior face once using its nearest original centreline tube.
c=v[f].mean(1);scores=[]
for q,r in curves:
 d,k=cKDTree(q).query(c);scores.append(d-r[k])
owner=np.argmin(scores,axis=0)
# Merge isolated label speckles into the surrounding selectable patch.
for _ in range(3):
 for j in range(len(NAMES)):
  selected=np.flatnonzero(owner==j);ff=f[selected];ids,inv=np.unique(ff,return_inverse=True);lf=inv.reshape(-1,3);edges=np.concatenate([lf[:,[0,1]],lf[:,[1,2]],lf[:,[2,0]]]);g=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(ids),len(ids))).tocsr();count,cc=connected_components(g,directed=False);fc=cc[lf[:,0]];sizes=np.bincount(fc,minlength=count)
  for k in np.flatnonzero(sizes<16):
   patch=selected[fc==k];neigh=owner[np.any(np.isin(f,np.unique(f[patch])),axis=1)];neigh=neigh[neigh!=j]
   if len(neigh):owner[patch]=np.bincount(neigh,minlength=len(NAMES)).argmax()
changed=[]
for j,n in enumerate(NAMES):
 ff=f[owner==j];ids,inv=np.unique(ff,return_inverse=True);v[ids].tofile(OUT/(n+'.positions.bin'));inv.reshape(-1,3).astype('<u4').tofile(OUT/(n+'.indices.bin'));nn[ids].astype('<f4').tofile(OUT/(n+'.normals.bin'));changed.append(dict(node=n,file='venous.glb',vertices=len(ids),triangles=len(ff),topology='exterior patch of unified tubular solid'))
revision=dict(release='0.9.48',baselineRelease='0.9.47',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),newLabels=[],changed=changed,method='Native geodesic centreline tubes with smoothed illustrative radius, explicit connected junction, implicit union, 0.12 mm grid, smooth single exterior surface and disjoint selectable patches.',gridSpacingMm=sp.tolist(),centrelineClearance=clearance,radiusProfiles=profiles,wholeAtlasWatertightClaimed=False)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(WORK/'connected-nodes.json').write_text(json.dumps(NAMES))
print('Rebuilt',len(v),len(f),flush=True)
