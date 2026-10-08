from model import *
from scipy.spatial import cKDTree

def keys(a):return np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()
def facekeys(f):return np.ascontiguousarray(np.sort(f.astype('<u4'),axis=1)).view('V12').ravel()
revision=json.loads((OUT/'revision.json').read_text());report=[]
for side in ['right','left']:
 names=[r['node'] for r in revision['changed'] if r['node'].endswith(side)]
 joined=normals(combine(names,True));v,f=arrays(joined);nn=vtk_to_numpy(joined.GetPointData().GetNormals()).copy()
 base,_=load('ICA petrous '+side);bn=np.fromfile(DATA/('ICA petrous '+side+'.normals.bin'),'<f4').reshape(-1,3)
 mask=np.isin(keys(v),keys(base));idx=cKDTree(base).query(v[mask])[1]
 reverse=np.median(np.sum(nn[mask]*bn[idx],axis=1))<0
 if reverse:f=f[:,::-1];nn=-nn
 e,c=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0,return_counts=True);boundary=np.unique(e[c==1])
 bv=[];bn=[]
 for name in names:
  ov,_=load(name);oldn=np.fromfile(DATA/(name+'.normals.bin'),'<f4').reshape(-1,3);keep=np.isin(keys(ov),keys(v[boundary]));bv.extend(ov[keep]);bn.extend(oldn[keep])
 if len(bv):
  bv=np.array(bv);bn=np.array(bn);d,i=cKDTree(bv).query(v);w=1-smooth(d/.6);nn=nn*(1-w[:,None])+bn[i]*w[:,None]
 nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
 tree=cKDTree(v);order=np.argsort(facekeys(f));fk=facekeys(f)[order]
 for name in names:
  nv,nf=load(name,True);idx=tree.query(nv)[1];fi=order[np.searchsorted(fk,facekeys(idx[nf]))];lookup=np.full(len(v),-1,dtype=int);lookup[idx]=np.arange(len(nv));nf=lookup[f[fi]];assert np.all(nf>=0)
  nf.astype('<u4').tofile(OUT/(name+'.indices.bin'));nn[idx].astype('<f4').tofile(OUT/(name+'.normals.bin'))
 report.append({'side':side,'outwardOrientationMatchedToNativePetrousSurface':True,'nativeExternalNormalsBlendedWithinMm':.6,'triangleVertexSetsUnchanged':True,'positionsUnchanged':True})
(OUT/'orientation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
