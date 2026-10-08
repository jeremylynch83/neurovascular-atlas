from model import *
from scipy.spatial import cKDTree
import hashlib,time
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def keys(a):return np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()
def join(names):
 vv=[];ff=[];labels=[];offset=0
 for label,n in enumerate(names):
  v,f=load(n);vv.append(v);ff.append(f+offset);labels.extend([label]*len(f));offset+=len(v)
 v=np.concatenate(vv);_,first,inv=np.unique(keys(v),return_index=True,return_inverse=True);faces=inv[np.concatenate(ff)];lab=np.array(labels,np.int32);keep=np.all(np.diff(np.sort(faces,axis=1),axis=1)>0,axis=1);return v[first],faces[keep],lab[keep]
results=[];changed=[]
for side in ['right','left']:
 names=['ICA '+t+' '+side for t in ['petrous','cavernous','paraophthalmic','posterior communicating','anterior choroidal','terminus']]+[t+' '+side for t in ['Ophthalmic','Superior hypophyseal','Meningohypophyseal trunk','Inferolateral trunk']]
 v,f,labels=join(names);oldv=v.copy();oldf=f.copy();edges,count=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0,return_counts=True);boundary=edges[count==1];collar=v[np.unique(boundary)]
 origin=[];rootRings=[]
 for parent,child in [('ICA cavernous','Meningohypophyseal trunk'),('ICA cavernous','Inferolateral trunk'),('ICA paraophthalmic','Ophthalmic'),('ICA paraophthalmic','Superior hypophyseal')]:
  a,_=load(parent+' '+side);b,_=load(child+' '+side);mask=np.isin(keys(a),keys(b));origin.extend(a[mask]);rootRings.append(a[mask])
 origin=np.array(origin);pd=poly(v,f);la=numpy_to_vtk(labels,deep=True);la.SetName('label');pd.GetCellData().AddArray(la)
 # Resolve long bridge triangles without multiplying the already fine core mesh.
 sub=vtk.vtkLinearSubdivisionFilter();sub.SetInputData(pd);sub.SetNumberOfSubdivisions(1);sub.Update();pd=sub.GetOutput();v,f=arrays(pd);labels=vtk_to_numpy(pd.GetCellData().GetArray('label')).copy()
 original=v.copy()
 # Fixed origins and all true external collars. Label borders are interior.
 # Refined points on source boundary edges must collapse back to native rings.
 mids=(oldv[boundary[:,0]]+oldv[boundary[:,1]])/2;length=np.linalg.norm(oldv[boundary[:,0]]-oldv[boundary[:,1]],axis=1);tree=cKDTree(mids);ns=tree.query_ball_point(v,length.max()/2+1e-7);onBoundary=np.zeros(len(v),bool);nearest=np.zeros(len(v),int)
 for i,ids in enumerate(ns):
  if not ids:continue
  ids=np.array(ids);a=oldv[boundary[ids,0]];b=oldv[boundary[ids,1]];ab=b-a;t=np.clip(np.einsum('ij,ij->i',v[i]-a,ab)/np.maximum(np.einsum('ij,ij->i',ab,ab),1e-16),0,1);d=np.linalg.norm(v[i]-a-ab*t[:,None],axis=1);hit=np.argmin(d)
  if d[hit]<1e-6:
   onBoundary[i]=True;edge=boundary[ids[hit]];nearest[i]=edge[0 if t[hit]<.5 else 1]
 main=np.concatenate([load('ICA '+t+' '+side)[0] for t in ['cavernous','paraophthalmic']]);d,_=cKDTree(main).query(v);w=1-smooth((d-1.4)/2.0);w*=smooth((v[:,2]-54.5)/3)*(1-smooth((v[:,2]-83)/4))
 dc,_=cKDTree(collar).query(v);do,_=cKDTree(origin).query(v);w*=smooth((dc-.2)/1.8);w[onBoundary]=0
 fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputData(pd);fair.SetNumberOfIterations(85);fair.SetPassBand(.02);fair.BoundarySmoothingOff();fair.FeatureEdgeSmoothingOff();fair.NonManifoldSmoothingOff();fair.NormalizeCoordinatesOn();fair.Update();target,_=arrays(fair.GetOutput());delta=target-v;mag=np.linalg.norm(delta,axis=1);delta*=np.minimum(1,.50/np.maximum(mag,1e-12))[:,None];v+=delta*w[:,None]
 # Allow the ostial wall to round while holding each original ostium's centroid.
 centres=np.array([r.mean(0) for r in rootRings]);field=np.exp(-np.sum((original[:,None,:]-centres[None,:,:])**2,axis=2)/(2*1.2**2))*w[:,None]
 tree=cKDTree(original);indices=[tree.query(r)[1] for r in rootRings];matrix=np.array([field[i].mean(0) for i in indices]);means=np.array([(v[i]-original[i]).mean(0) for i in indices]);correction=np.linalg.solve(matrix,means);v-=field@correction
 v[onBoundary]=oldv[nearest[onBoundary]]
 # Weld collapsed boundary points, discard only resulting zero-area triangles.
 v=v.astype('<f4');_,first,inv=np.unique(keys(v),return_index=True,return_inverse=True);v=v[first];f=inv[f];keep=np.all(np.diff(np.sort(f,axis=1),axis=1)>0,axis=1);f=f[keep];labels=labels[keep];tri=v[f];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);keep=area>1e-10;f=f[keep];labels=labels[keep]
 nn=vtk_to_numpy(normals(poly(v,f)).GetPointData().GetNormals()).copy();nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
 for label,n in enumerate(names):
  faces=f[labels==label];ids,iv=np.unique(faces,return_inverse=True);v[ids].tofile(OUT/(n+'.positions.bin'));iv.reshape(-1,3).astype('<u4').tofile(OUT/(n+'.indices.bin'));nn[ids].astype('<f4').tofile(OUT/(n+'.normals.bin'));changed.append({'node':n,'file':'complete-circulation.glb'})
 result={'side':side,'trianglesBefore':len(oldf),'trianglesAfter':len(f),'maximumSurfaceDisplacementMm':float(np.max(np.linalg.norm(delta*w[:,None],axis=1))),'fixedOriginCentroids':len(rootRings),'nativeBoundaryEdges':len(boundary),'method':'conforming linear bridge subdivision, connected surface fairing, native collar restoration and shared normals'};results.append(result);print(result,flush=True)
revision={'release':'0.9.39','changed':changed,'newLabels':[],'baselineAssetHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'baseline').glob('*.glb')}}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'repair.json').write_text(json.dumps(results,indent=2)+'\n')
