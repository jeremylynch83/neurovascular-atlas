from model import *
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree
def fast_sample(mesh,lo,hi,dims):
 from scipy.ndimage import distance_transform_edt
 spacing=(hi-lo)/(dims-1)
 st=vtk.vtkPolyDataToImageStencil();st.SetInputData(mesh);st.SetOutputOrigin(*lo);st.SetOutputSpacing(*spacing);st.SetOutputWholeExtent(0,int(dims[0]-1),0,int(dims[1]-1),0,int(dims[2]-1));st.Update()
 image=vtk.vtkImageStencilToImage();image.SetInputConnection(st.GetOutputPort());image.SetInsideValue(1);image.SetOutsideValue(0);image.SetOutputScalarTypeToUnsignedChar();image.Update()
 inside=vtk_to_numpy(image.GetOutput().GetPointData().GetScalars()).reshape(dims,order='F').astype(bool)
 return (distance_transform_edt(~inside,sampling=spacing)-distance_transform_edt(inside,sampling=spacing)).astype(np.float32)
sample=fast_sample
STEMS=['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary']
NAMES=['vein.cavernous.'+s for s in ['right','left']]+['vein.'+n+'.'+s for s in ['right','left'] for n in STEMS]+['vein.anterior_intercavernous','vein.posterior_intercavernous','vein.basilar_plexus']
lo=np.array([-28.,-78.,41.]);hi=np.array([29.,-22.,83.]);dims=np.ceil((hi-lo)/.3).astype(int)+1;sp=(hi-lo)/(dims-1)
cache=OUT/'base-sdf.npy'
if cache.exists():base=np.load(cache)
else:
 print('Sampling joined native venous wall',flush=True);base=sample(closed(combine(NAMES)),lo,hi,dims).astype(np.float32);np.save(cache,base)
x,y,z=np.meshgrid(*[np.linspace(a,b,n) for a,b,n in zip(lo,hi,dims)],indexing='ij');union=base.copy()
bcache=OUT/'bone-sdf.npy'
if bcache.exists():bd=np.load(bcache)
else:
 print('Sampling fixed bone',flush=True);bd=sample(combine(['bone.sphenoid','bone.temporal.right','bone.temporal.left']),lo,hi,dims).astype(np.float32);np.save(bcache,bd)
for side in ['right','left']:
 lat=x if side=='right' else -x+1.3
 # Compact outer chamber. Reduce the posterior roof without moving the artery.
 roof=1.8*(1-smooth((y+48)/11))*smooth((z-62)/4)*(1-smooth((z-79)/3))
 zz=z+roof;cx=11.5-.3*(y+45);cz=68.4+.3*(y+45)
 outer=(np.sqrt(((lat-cx)/5.5)**2+((y+45)/12.8)**2+((zz-cz)/9)**2)-1)*5.5
 posterior=(np.sqrt(((lat-13.3)/4.8)**2+((y+50)/6.8)**2+((zz-62.3)/6.8)**2)-1)*4.8
 h=np.maximum(1-np.abs(outer-posterior)/1.2,0);outer=np.minimum(outer,posterior)-h*h*1.2/4
 outer=np.maximum(outer,(57.2 if side=='right' else 57.1)-z);outer=np.maximum(outer,.55-bd)
 union=np.minimum(union,outer)
 print('Restored outer chamber',side,flush=True)
acache=OUT/'ica-sdf.npy'
if acache.exists():ad=np.load(acache)
else:
 ad=np.full(dims,100.,np.float32)
 for side in ['right','left']:
  print('Sampling primary ICA space',side,flush=True)
  artery=closed(combine(['ICA cavernous '+side,'ICA paraophthalmic '+side,'ICA petrous '+side]))
  ad=np.minimum(ad,sample(artery,lo,hi,dims))
 np.save(acache,ad)
# Keep the ICA channel, without subtracting combined/capped small branch networks.
union=np.maximum(union,.65-ad)
# Mild field fairing removes grid-scale ripples; no detached overlay surfaces.
union=gaussian_filter(union,.65);v,f=iso(union,lo,sp)
# Smooth the newly joined network before assigning labels.
smo=vtk.vtkWindowedSincPolyDataFilter();smo.SetInputData(poly(v,f));smo.SetNumberOfIterations(12);smo.SetPassBand(.08);smo.BoundarySmoothingOff();smo.FeatureEdgeSmoothingOff();smo.NonManifoldSmoothingOff();smo.NormalizeCoordinatesOn();smo.Update();v,f=arrays(smo.GetOutput())
# Drop disconnected carving debris. The bilateral sinus network is connected.
conn=vtk.vtkPolyDataConnectivityFilter();conn.SetInputData(poly(v,f));conn.SetExtractionModeToLargestRegion();conn.Update();v,f=arrays(conn.GetOutput())
# Weld numerical slivers at final Float32 precision before partitioning.
cleaner=vtk.vtkCleanPolyData();cleaner.SetInputData(poly(v.astype('<f4').astype(float),f));cleaner.ToleranceIsAbsoluteOn();cleaner.SetAbsoluteTolerance(1e-4);cleaner.ConvertPolysToLinesOff();cleaner.ConvertLinesToPointsOff();cleaner.Update();v,f=arrays(cleaner.GetOutput())
# Assign every triangle once to its nearest original labelled surface.
fc=v[f].mean(1);centres=[];labels=[]
for j,n in enumerate(NAMES):
 ov,of=load(n);centres.append(ov[of].mean(1));labels.extend([j]*len(of))
_,nearest=cKDTree(np.concatenate(centres)).query(fc);owner=np.asarray(labels)[nearest]
# Reassign tiny label islands across shared borders instead of leaving sinus shards.
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
for iteration in range(2):
 for j in range(len(NAMES)):
  selected=np.flatnonzero(owner==j);ff=f[selected]
  ids,inv=np.unique(ff,return_inverse=True);lf=inv.reshape(-1,3)
  edge=np.concatenate([lf[:,[0,1]],lf[:,[1,2]],lf[:,[2,0]]]);graph=coo_matrix((np.ones(len(edge)),(edge[:,0],edge[:,1])),shape=(len(ids),len(ids))).tocsr()
  count,comp=connected_components(graph,directed=False)
  facecomp=comp[lf[:,0]];sizes=np.bincount(facecomp,minlength=count)
  for k in np.flatnonzero(sizes<40):
   patch=selected[facecomp==k];vertices=np.unique(f[patch]);neighbours=owner[np.any(np.isin(f,vertices),axis=1)];neighbours=neighbours[neighbours!=j]
   if len(neighbours):owner[patch]=np.bincount(neighbours,minlength=len(NAMES)).argmax()
cuts=json.load(open(APP/'anatomy/source/ica-cs-v0932/venous-cuts.json'))
splices=[]
for j,n in enumerate(NAMES):
 vv=v.copy();ff=f[owner==j]
 if n in cuts:
  cut=cuts[n];c=np.array(cut['point']);normal=np.array(cut['normal'])
  # Find a clean native tube section with matching local/remote loops.
  originalv,originalf=load(n);found=False
  for shift in [0,-1,1,-2,2,-4,4,-6,6,8,10,12,14,16]:
   cc=c+normal*shift
   lv,lf=clip(v.copy(),f[owner==j],(v-cc)@normal-.65)
   value=(originalv-cc)@normal
   if n!='vein.basilar_plexus':value=np.minimum(value,25-np.linalg.norm(originalv-cc,axis=1))
   ov,of=clip(originalv,originalf,value,False)
   try:
    lr=rings(lv,lf,np.flatnonzero(abs((lv-cc)@normal-.65)<.002))
    ids=abs((ov-cc)@normal)<.002
    if n!='vein.basilar_plexus':ids &= np.linalg.norm(ov-cc,axis=1)<24.99
    rr=rings(ov,of,np.flatnonzero(ids))
   except RuntimeError:continue
   if n=='vein.basilar_plexus':print('Basilar section',cc[2],len(lr),len(rr),flush=True)
   if len(lr)==len(rr) and len(lr)>0:
    vv,ff=lv,lf;found=True;break
  if not found:raise RuntimeError(f'{n}: no clean matching section; local={len(lr)} native={len(rr)}')
  o=len(vv);vv=np.concatenate([vv,ov]);ff=np.concatenate([ff,of+o]);avail=list(range(len(rr)))
  for a in lr:
   b=min(avail,key=lambda k:np.linalg.norm(vv[a].mean(0)-ov[rr[k]].mean(0)));avail.remove(b);ff=np.concatenate([ff,bridge(vv,a,rr[b]+o)])
  splices.append({'name':n,'localRings':len(lr),'nativeRings':len(rr)})
 save(n,vv,ff);print('Saved',n,len(ff),flush=True)
(OUT/'repair.json').write_text(json.dumps({'release':'0.9.34','changed':NAMES,'method':'Restore compact outer chamber volume; retain primary ICA channel; union and fair venous wall; repartition and graft native remote collars','splices':splices},indent=2))
