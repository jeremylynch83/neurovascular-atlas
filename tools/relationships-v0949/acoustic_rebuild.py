"""Tubular single-wall reconstruction of each acoustic arterial network."""
from common import *
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def arrays(p):return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
revision=json.loads((OUT/'revision.json').read_text());topologies=[];profiles=[]
for side,sign in [('right',1),('left',-1)]:
 NAMES=['Labyrinthine '+side,'Common cochlear '+side,'Anterior vestibular '+side];curves=[];connectors=[]
 q=np.loadtxt(WORK/('transport-'+side+'.csv'),delimiter=',')[:,4:7];q=gaussian_filter1d(q,2.,axis=0);q[0]=np.loadtxt(WORK/('transport-'+side+'.csv'),delimiter=',')[0,4:7];r=np.linspace(.22,.14,len(q))
 # Cover the exact old AICA interface ring with a rounded volume collar.
 av,af=load('AICA '+side);vv,ff=load(NAMES[0]);shared=vv[cKDTree(av).query(vv)[0]<1e-5];root=shared.mean(0);stem=np.linspace(root,q[0],12);stem[0]=root;rr=np.linspace(.30,.22,len(stem));q=np.vstack([stem,q]);r=np.r_[rr,r];curves.append([q,r]);profiles.append(dict(node=NAMES[0],radiusRangeMm=[.14,.22],rootCollarRadiusMm=.30,policy='illustrative tube radius; distal branch scale .65; root collar contains the native AICA interface'))
 for n,axis in [(NAMES[1],1),(NAMES[2],0)]:
  vv,ff=load(n,OUT);lo0=vv[:,axis].min();hi0=vv[:,axis].max();stations=np.linspace(lo0+.06,hi0-.06,45);qq=[]
  for value in stations:
   pp=section(vv,ff,axis,value)
   if len(pp):qq.append((pp.min(0)+pp.max(0))/2)
  qq=gaussian_filter1d(np.array(qq),1,axis=0);radius=np.full(len(qq),.115);curves.append([qq,radius]);profiles.append(dict(node=n,radiusMm=.115,policy='illustrative smooth tubular branch'))
  # Connect the child to the main branch at its nearest endpoint pair.
  nearest=cKDTree(q);da,ka=nearest.query(qq[0]);db,kb=nearest.query(qq[-1]);j,k=(0,ka) if da<db else (len(qq)-1,kb);t=np.linspace(0,1,20);connectors.append((qq[j]+t[:,None]*(q[k]-qq[j]),np.full(len(t),.13),len(curves)-1))
 allq=np.concatenate([q for q,r in curves]+[q for q,r,j in connectors]);lo=allq.min(0)-.8;hi=allq.max(0)+.8;spacing=.06;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1)
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
 v=v.astype('<f4');f=f.astype('<u4');np.savez(OUT/('acoustic-network-'+side+'.npz'),v=v,f=f,normals=nn)
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
  ff=f[owner==j];ids,inv=np.unique(ff,return_inverse=True);v[ids].tofile(OUT/(n+'.positions.bin'));inv.reshape(-1,3).astype('<u4').tofile(OUT/(n+'.indices.bin'));nn[ids].astype('<f4').tofile(OUT/(n+'.normals.bin'));changed.append(dict(node=n,file='complete-circulation.glb',vertices=len(ids),triangles=len(ff),topology='exterior patch of unified tubular solid'))
 for row in changed:
  for original in revision['changed']:
   if original['node']==row['node']:original.update(row)
 # Closed combined exterior, with exact disjoint patch coverage.
 edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,count=np.unique(edges,axis=0,return_counts=True);topologies.append(dict(side=side,vertices=len(v),triangles=len(f),boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),patches=NAMES))
revision['acousticNetworkTopology']=topologies;revision['acousticRadiusProfiles']=profiles;revision['method']='Local coordinate shears for retained surfaces; acoustic centreline tubes joined by an implicit union on a 0.06 mm grid, smoothed single exterior and disjoint selectable patches.'
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');print(topologies,flush=True)
