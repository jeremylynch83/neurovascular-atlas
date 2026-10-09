"""Remove inherited frontal MMA overlapping facets using a tubular regional union."""
from common import *
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def arrays(p):return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
revision=json.loads((OUT/'revision.json').read_text());topologies=[];profiles=[]
for side,sign in [('right',1),('left',-1)]:
 suffix='' if side=='right' else ' left';NAMES=['MMA frontal'+suffix,'MMA frontal anterior division'+suffix];curves=[];connectors=[];bone_names=['bone.frontal','bone.parietal.'+side,'bone.temporal.'+side,'bone.sphenoid'];bone_loc=[];bone_signed=[]
 for bone in bone_names:
  a,b=load(bone);bone_loc.append(locator(a,b));ip=vtk.vtkImplicitPolyDataDistance();ip.SetInput(poly(a,b));bone_signed.append(ip)
 for j,n in enumerate(NAMES):
  directory=OUT if any(row['node']==n and 'topology' not in row for row in revision['changed']) else DATA;vv,ff=load(n,directory);stations=np.arange(vv[:,2].min()+.4,vv[:,2].max()-.25,.45);q=[];radius=[]
  for value in stations:
   p=section(vv,ff,2,value)
   if len(p)<3:continue
   c=(p.min(0)+p.max(0))/2;q.append(c);radius.append(np.median(np.linalg.norm(p[:,:2]-c[:2],axis=1)))
  q=gaussian_filter1d(np.array(q),1.8,axis=0);r=gaussian_filter1d(np.clip(radius,.35 if j==0 else .24,.50 if j==0 else .42),2)
  if j==0:
   # Radius-aware inner-table clearance, preserving the exact root region.
   for _ in range(2):
    pp=[];dd=[]
    for l in bone_loc:
     cp,ds=closest(l,q);pp.append(cp);dd.append(ds)
    dd=np.array(dd);which=np.argmin(dd,axis=0);cp=np.array(pp)[which,np.arange(len(q))];ds=dd[which,np.arange(len(q))];signed=np.array([bone_signed[k].EvaluateFunction(p) for k,p in zip(which,q)]);direction=(q-cp)/np.maximum(ds[:,None],1e-10);direction[signed<0]*=-1;need=(ds<r+.45)&(q[:,2]>83);q[need]=cp[need]+direction[need]*(r[need]+.45)[:,None]
    if _==0:q=gaussian_filter1d(q,.9,axis=0)
   av,af=load('Middle meningeal'+suffix);source,sf=load(n);shared=source[cKDTree(av).query(source)[0]<1e-5];assert len(shared)>10,n;root=shared.mean(0);stem=np.linspace(root,q[0],10);q=np.vstack([stem,q]);r=np.r_[np.linspace(.58,r[0],10),r]
  curves.append([q,r]);profiles.append(dict(node=n,method='Smoothed axial contour centreline with bounded illustrative median contour radius, after the local inner-table placement correction.',tubeRadiusP05MedianP95=np.percentile(r,[5,50,95]).tolist()))
  if j==1:
   parentq,parentr=curves[0];tree=cKDTree(parentq);da,ka=tree.query(q[0]);db,kb=tree.query(q[-1]);a,k=(0,ka) if da<db else (len(q)-1,kb);t=np.linspace(0,1,18);connectors.append((q[a]+t[:,None]*(parentq[k]-q[a]),np.full(len(t),min(.40,r[a])),1))
 allq=np.concatenate([q for q,r in curves]+[q for q,r,j in connectors]);lo=allq.min(0)-.8;hi=allq.max(0)+.8;spacing=.14;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1)
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
 v=v.astype('<f4');f=f.astype('<u4');np.savez(OUT/('meningeal-network-'+side+'.npz'),v=v,f=f,normals=nn)
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
  old=next((c for c in revision['changed'] if c['node']==row['node']),None)
  if old:old.update(row)
  else:revision['changed'].append(row)
 edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,count=np.unique(edges,axis=0,return_counts=True);topologies.append(dict(side=side,vertices=len(v),triangles=len(f),boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),patches=NAMES))
revision['meningealNetworkTopology']=topologies;revision['meningealRadiusProfiles']=profiles;revision['method']+=' Frontal MMA and its anterior division reconstructed as 0.14 mm implicit tubular regional networks, preserving original parent attachment locations.'
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');print(topologies,flush=True)
