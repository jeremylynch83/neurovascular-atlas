from model import *
from scipy.spatial import cKDTree

def keys(a):
 return np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()

report=[]
revision=json.loads((OUT/'revision.json').read_text())
for side in ['right','left']:
 names=[r['node'] for r in revision['changed'] if r['node'].endswith(side)]
 joined=combine(names,True);v,f=arrays(joined)
 edges,count=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0,return_counts=True)
 boundary=np.unique(edges[count==1]);locked=np.zeros(len(v),bool);locked[boundary]=True
 source=v.copy()
 # Round the short petrous transition collar without changing remote rings.
 fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputData(joined);fair.SetNumberOfIterations(35);fair.SetPassBand(.08);fair.BoundarySmoothingOff();fair.NormalizeCoordinatesOn();fair.Update();target,_=arrays(fair.GetOutput())
 weight=np.exp(-((v[:,2]-56.65)/.70)**2);weight*=smooth((v[:,2]-55.65)/.3)*(1-smooth((v[:,2]-58.0)/.3));weight[locked]=0
 v+=(target-v)*weight[:,None]
 parent='ICA paraophthalmic '+side;child='Ophthalmic '+side
 p,_=load(parent);q,_=load(child);old=p[np.isin(keys(p),keys(q))].mean(0)
 p,_=load(parent,True);q,_=load(child,True);ring=p[np.isin(keys(p),keys(q))]
 ids=cKDTree(source).query(ring)[1];centre=v[ids].mean(0)
 field=np.exp(-np.sum((v-centre)**2,axis=1)/(2*1.4**2));field*=smooth((field-.0001)/.001);field[locked]=0
 delta=(old-centre)/field[ids].mean();v+=field[:,None]*delta
 v=v.astype('<f4');norm=vtk_to_numpy(normals(poly(v,f)).GetPointData().GetNormals())
 tree=cKDTree(source)
 for name in names:
  nv,nf=load(name,True);idx=tree.query(nv)[1];save(name,v[idx],nf)
  norm[idx].astype('<f4').tofile(OUT/(name+'.normals.bin'))
 p,_=load(parent,True);q,_=load(child,True);now=p[np.isin(keys(p),keys(q))].mean(0)
 result={'side':side,'ophthalmicOstiumCentroidBefore':old.tolist(),'ophthalmicOstiumCentroidAfter':now.tolist(),'centroidDisplacementMm':float(np.linalg.norm(old-now)),'maximumLocalCorrectionMm':float(np.max(np.linalg.norm(v-source,axis=1))),'nativeExternalBoundaryVerticesExact':bool(np.array_equal(v[locked],source[locked].astype('<f4')))}
 report.append(result);print(result)
(OUT/'origin-restoration.json').write_text(json.dumps(report,indent=2)+'\n')
