from model import *
from scipy.ndimage import gaussian_filter,distance_transform_edt
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import hashlib
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
for p in OUT.glob('*.bin'):p.unlink()
def sample_field(mesh,lo,sp,dims):
 st=vtk.vtkPolyDataToImageStencil();st.SetInputData(mesh);st.SetOutputOrigin(*lo);st.SetOutputSpacing(*sp);st.SetOutputWholeExtent(0,int(dims[0]-1),0,int(dims[1]-1),0,int(dims[2]-1));st.Update();im=vtk.vtkImageStencilToImage();im.SetInputConnection(st.GetOutputPort());im.SetInsideValue(1);im.SetOutsideValue(0);im.SetOutputScalarTypeToUnsignedChar();im.Update();inside=vtk_to_numpy(im.GetOutput().GetPointData().GetScalars()).reshape(dims,order='F').astype(bool);return distance_transform_edt(~inside,sampling=sp)-distance_transform_edt(inside,sampling=sp)
results=[];changed=[]
for side in ['right','left']:
 names=['ICA '+t+' '+side for t in ['petrous','cavernous','paraophthalmic']]+[t+' '+side for t in ['Ophthalmic','Superior hypophyseal','Meningohypophyseal trunk','Inferolateral trunk','Tentorial marginal','Dorsal meningeal','Inferior hypophyseal','Basal tentorial MHT branch']]
 original=combine(names);lo=np.array([0 if side=='right' else -26,-64,50.]);hi=np.array([27 if side=='right' else 1,-22,90.]);dims=np.ceil((hi-lo)/.15).astype(int)+1;sp=(hi-lo)/(dims-1)
 print('Sampling',side,flush=True);sdf=sample_field(closed(original),lo,sp,dims);sdf=gaussian_filter(sdf,1.8)
 for branch in names[3:]:
  bsdf=sample_field(closed(poly(*load(branch))),lo,sp,dims);bsdf=gaussian_filter(bsdf,.35);blend=.55;h=np.maximum(1-abs(sdf-bsdf)/blend,0);sdf=np.minimum(sdf,bsdf)-h*h*blend/4
 bone=sample_field(combine(['bone.sphenoid','bone.temporal.'+side]),lo,sp,dims);sdf=np.maximum(sdf,.15-bone);v,f=iso(sdf,lo,sp)
 fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputData(poly(v,f));fair.SetNumberOfIterations(20);fair.SetPassBand(.08);fair.NormalizeCoordinatesOn();fair.Update();v,f=arrays(fair.GetOutput())
 # A single remeshed surface is assigned once to its original selectable label.
 centres=[];labels=[]
 for j,n in enumerate(names):
  ov,of=load(n);centres.append(ov[of].mean(1));labels.extend([j]*len(of))
 owner=np.array(labels)[cKDTree(np.concatenate(centres)).query(v[f].mean(1))[1]]
 # Keep one connected region per label; tiny nearest-label islands join neighbours.
 for it in range(3):
  for j in range(len(names)):
   selected=np.flatnonzero(owner==j);ff=f[selected];ids,iv=np.unique(ff,return_inverse=True);lf=iv.reshape(-1,3);e=np.concatenate([lf[:,[0,1]],lf[:,[1,2]],lf[:,[2,0]]]);g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(ids),len(ids))).tocsr();count,c=connected_components(g,directed=False);fc=c[lf[:,0]];sz=np.bincount(fc,minlength=count)
   for k in np.flatnonzero(sz<25):
    patch=selected[fc==k];neigh=owner[np.any(np.isin(f,np.unique(f[patch])),axis=1)];neigh=neigh[neigh!=j]
    if len(neigh):owner[patch]=np.bincount(neigh,minlength=len(names)).argmax()
 cuts={names[0]:(np.array([0,0,56.5]),np.array([0,0,1]),None),names[2]:(np.array([14 if side=='right' else -12.7,-36.3,78.8]),np.array([0,.9,-.43]),None)}
 for parent,child in [('ICA cavernous','Meningohypophyseal trunk'),('ICA cavernous','Inferolateral trunk'),('ICA paraophthalmic','Ophthalmic'),('ICA paraophthalmic','Superior hypophyseal')]+[('Meningohypophyseal trunk',t) for t in ['Tentorial marginal','Dorsal meningeal','Inferior hypophyseal','Basal tentorial MHT branch']]:
  pv,_=load(parent+' '+side);cv,_=load(child+' '+side);keys=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();root=pv[np.isin(keys(pv),keys(cv))].mean(0);d=np.linalg.norm(cv-root,axis=1);near=(d>2.5)&(d<4);near=near if near.any() else d>np.percentile(d,70);point=cv[near].mean(0);direction=point-root;direction/=np.linalg.norm(direction);distance=2.8 if d.max()>4 else .85;cuts[child+' '+side]=(root+direction*distance,-direction,root)
 splices=[]
 for j,n in enumerate(names):
  lv=v.copy();lf=f[owner==j]
  if n==names[2]:
   ov,of=load(n);up,_=load('ICA posterior communicating '+side);keys=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();shared=np.flatnonzero(np.isin(keys(ov),keys(up)));ring=rings(ov,of,shared)[0];cc=ov[ring].mean(0);_,_,vh=np.linalg.svd(ov[ring]-cc,full_matrices=False);normal=vh[-1]
   if np.dot(normal,ov.mean(0)-cc)<0:normal=-normal
   for gap in [.45,.65,.85,1.05,1.3]:
    a,af=clip(v,f[owner==j],(v-cc)@normal-gap,True)
    try:ar=rings(a,af,np.flatnonzero(abs((a-cc)@normal-gap)<.002))
    except RuntimeError:continue
    if len(ar)==1:break
   else:raise RuntimeError('No proximal transition collar')
   lv=np.concatenate([a,ov[ring]]);lf=np.concatenate([af,bridge(lv,ar[0],np.arange(len(a),len(lv)))]);splices.append({'name':n,'nativeSegmentRingExact':True,'gapMm':gap});save(n,lv,lf);changed.append({'node':n,'file':'complete-circulation.glb'});continue
  if n in cuts and not n.startswith('Meningohypophyseal'):
   c,normal,root=cuts[n];ov,of=load(n);done=False
   for shift in [0,.5,-.5,1,-1,1.5,-1.5,2,-2,3]:
    cc=c+normal*shift
    value=(ov-cc)@normal;lvv=(v-cc)@normal
    if root is not None:value=np.minimum(value,7-np.linalg.norm(ov-root,axis=1));lvv=np.minimum(lvv,7-np.linalg.norm(v-root,axis=1))
    a,af=clip(v,f[owner==j],lvv-.35,True);b,bf=clip(ov,of,value,False)
    try:
     ar=rings(a,af,np.flatnonzero(abs((a-cc)@normal-.35)<.002));br=rings(b,bf,np.flatnonzero(abs((b-cc)@normal)<.002))
    except RuntimeError:continue
    print('Collar',n,shift,len(ar),len(br),flush=True)
    if len(ar)==len(br)==1:done=True;break
   if not done:raise RuntimeError('No clean collar '+n)
   lv=np.concatenate([a,b]);lf=np.concatenate([af,bf+len(a),bridge(lv,ar[0],br[0]+len(a))]);splices.append({'name':n,'cut':cc.tolist(),'localVertices':len(ar[0]),'nativeVertices':len(br[0])})
  save(n,lv,lf);changed.append({'node':n,'file':'complete-circulation.glb'})
 # Weld only microscopic new slivers; preserve all original native vertices.
 vv=[];ff=[];rows=[];offset=0
 for n in names:
  a,af=load(n,True);rows.append((n,offset,offset+len(a),af));vv.append(a);ff.append(af+offset);offset+=len(a)
 allv=np.concatenate(vv).astype('<f4');allf=np.concatenate(ff);originalkeys=np.unique(np.concatenate([np.ascontiguousarray(load(n)[0].astype('<f4')).view('V12').ravel() for n in names]));kk=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();locked=np.isin(kk(allv),originalkeys);par=np.arange(len(allv))
 def root(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for x,y in cKDTree(allv).query_pairs(.0001):
  x=root(x);y=root(y)
  if x==y or (locked[x] and locked[y] and not np.array_equal(allv[x],allv[y])):continue
  if locked[y] or (not locked[x] and y<x):x,y=y,x
  par[y]=x
 iv=np.array([root(i) for i in range(len(allv))]);allv=allv[iv]
 for n,a,b,af in rows:save(n,allv[a:b],af)
 joined=combine(names,True);jv,jf=arrays(joined);nn=vtk_to_numpy(normals(joined).GetPointData().GetNormals());order=np.argsort(kk(jv));k=kk(jv)[order]
 for n in names:
  nv,_=load(n,True);i=np.searchsorted(k,kk(nv));nn[order[i]].astype('<f4').tofile(OUT/(n+'.normals.bin'))
 results.append({'side':side,'gridSpacingMm':sp.tolist(),'fieldBlurSigmaMm':(sp*1.8).tolist(),'splices':splices});print('Remeshed',side,flush=True)
revision={'release':'0.9.39','changed':changed,'newLabels':[],'baselineAssetHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'baseline').glob('*.glb')}}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'repair.json').write_text(json.dumps(results,indent=2)+'\n')
