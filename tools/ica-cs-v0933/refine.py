"""Local refinement of v0.9.32. Requires decoded v0.9.32 meshes as input."""
from pathlib import Path
import json,sys,os,numpy as np,vtk
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix,diags
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
ROOT=Path(__file__).resolve().parent;APP=ROOT.parents[1]
DATA=Path(sys.argv[1]).resolve();OUT=ROOT/'candidate';OUT.mkdir(exist_ok=True)
META=json.loads((DATA/'meshes.json').read_text())
def load(n):return np.fromfile(DATA/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(DATA/(n+'.indices.bin'),'<u4').reshape(-1,3)
def poly(v,f):
 p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(v,deep=True));p.SetPoints(pts);cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(cells);return p
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
def keys(v):return np.ascontiguousarray(v.astype('<f4')).view('V12').ravel()
def joined(names):
 vs=[];fs=[];ranges=[];o=0
 for n in names:
  v,f=load(n);vs.append(v);fs.append(f+o);ranges.append((n,o,o+len(v),f));o+=len(v)
 vv=np.concatenate(vs);k,idx,inv=np.unique(keys(vv),return_index=True,return_inverse=True);return vv[idx],inv[np.concatenate(fs)],inv,ranges
# Bone is unchanged. Use its local surface to taper motion away from fixed bone.
bv=[];bf=[];o=0
for n in ['bone.sphenoid','bone.temporal.right','bone.temporal.left']:
 v,f=load(n);t=v[f];keep=np.all(t.max(1)>[-28,-64,54],axis=1)&np.all(t.min(1)<[29,-27,86],axis=1);bf.append(f[keep]+o);bv.append(v);o+=len(v)
bone=poly(np.concatenate(bv),np.concatenate(bf));loc=vtk.vtkStaticCellLocator();loc.SetDataSet(bone);loc.BuildLocator()
def bone_distance(v):
 out=np.empty(len(v));q=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);d=vtk.reference(0.)
 for i,p in enumerate(v):loc.FindClosestPoint(p,q,ci,sub,d);out[i]=float(d)**.5
 return out
# Retain complete ophthalmic and superior hypophyseal meshes and incident parent faces.
protected=[];fixednames=['Ophthalmic '+s for s in ['right','left']]+['Superior hypophyseal '+s for s in ['right','left']]
for s in ['right','left']:
 child=np.concatenate([load('Ophthalmic '+s)[0],load('Superior hypophyseal '+s)[0]]);pv,pf=load('ICA paraophthalmic '+s);shared=np.isin(keys(pv),keys(child));inc=pf[shared[pf].any(1)];protected.append(pv[np.unique(inc)]);protected.append(child)
protected=np.concatenate(protected);ptree=cKDTree(protected)
def envelope_weight(v):
 # Fixed lower course; progressively lower the posterior half above z62.
 lat=np.abs(v[:,0]-.65);wy=1-smooth((v[:,1]+48)/11);wz=smooth((v[:,2]-62)/4)*(1-smooth((v[:,2]-79)/3));wx=smooth((lat-2)/3)*(1-smooth((lat-20)/6));back=smooth((v[:,1]+65)/6)
 d,_=ptree.query(v);out=wy*wz*wx*back*smooth((d-.15)/2.5)
 return out
def spatial_weight(v):
 lat=np.abs(v[:,0]-.65);return smooth((v[:,2]-57.7)/3)*(1-smooth((v[:,2]-79)/2))*smooth((v[:,1]+64)/5)*(1-smooth((v[:,1]+34)/3))*smooth((lat-1.8)/2)*(1-smooth((lat-23)/4))
selected=[]
for row in META:
 n=row['name']
 if row['file'] not in ['complete-circulation.glb','complete-anastomoses.glb','venous.glb'] or n in fixednames:continue
 v,f=load(n)
 if spatial_weight(v).max()>.01:selected.append(row)
allowed={a['node'] for a in json.load(open(APP/'anatomy/source/ica-cs-v0932/revision.json'))['changed']}
selected=[r for r in META if r['name'] in allowed]
for p in OUT.glob('*.bin'):p.unlink()
# Freeze collars shared with unmodified neighbours, so remote vessels remain exact.
selectedkeys=np.unique(np.concatenate([keys(load(r['name'])[0]) for r in selected]));outside=[]
for row in META:
 if row['file'] not in ['complete-circulation.glb','complete-anastomoses.glb','venous.glb'] or row['name'] in allowed:continue
 v,_=load(row['name']);kk=keys(v);ii=np.searchsorted(selectedkeys,kk);hit=(ii<len(selectedkeys))&(selectedkeys[np.minimum(ii,len(selectedkeys)-1)]==kk)
 if hit.any():outside.append(v[hit])
if outside:
 protected=np.concatenate([protected]+outside);ptree=cKDTree(protected)
print('Selected',len(selected),'local labels',flush=True)
measure=[];changed=[];smoothing=[]
for group,rows in [('arterial',[r for r in selected if r['file']!='venous.glb']),('venous',[r for r in selected if r['file']=='venous.glb'])]:
 v,f,inv,ranges=joined([r['name'] for r in rows]);original=v.copy();bd=bone_distance(v);bp=smooth((bd-.58)/1.7);d,_=ptree.query(v);protect=smooth((d-.15)/2.5);w=envelope_weight(v)*bp
 if group=='venous':
  arteryverts=[];arteryfaces=[];offset=0
  arterialNames=['ICA cavernous '+side for side in ['right','left']]+['ICA paraophthalmic '+side for side in ['right','left']]
  arterialNames+=sum([d['arterialLabels'] for d in json.load(open(APP/'anatomy/source/ica-cs-v0932/branch-clearance-authoring.json'))],[])
  for name in dict.fromkeys(arterialNames):
   aa=np.fromfile(OUT/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float) if (OUT/(name+'.positions.bin')).exists() else load(name)[0];_,ff=load(name);arteryverts.append(aa);arteryfaces.append(ff+offset);offset+=len(aa)
  artery=poly(np.concatenate(arteryverts),np.concatenate(arteryfaces));aloc=vtk.vtkStaticCellLocator();aloc.SetDataSet(artery);aloc.BuildLocator()
  def artery_distance(points):
   q0=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);dd=vtk.reference(0.);out=np.empty(len(points))
   for i,pp in enumerate(points):aloc.FindClosestPoint(pp,q0,ci,sub,dd);out[i]=float(dd)**.5
   return out
  # Integrate a smooth constrained velocity field in small steps rather than
  # subtracting one large displacement, which can fold a thin venous wall.
  moving=envelope_weight(v)>.000001
  for step in range(16):
   points=v[moving];db=bone_distance(points);da=artery_distance(points)
   velocity=.43*np.maximum(points[:,2]-62,0)*envelope_weight(points)*smooth((db-.58)/1.7)*smooth((da-.65)/1.3)
   points[:,2]-=velocity/16;v[moving]=points
  print('Integrated posterior roof flow',flush=True)
 # Arterial centreline and calibre remain intact; only bounded surface fairing follows.
 # Smooth the connected surface rather than separate labels, preserving every shared join.
 e=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);ii=np.r_[e[:,0],e[:,1]];jj=np.r_[e[:,1],e[:,0]];A=coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(len(v),len(v))).tocsr();deg=np.asarray(A.sum(1)).ravel();P=diags(1/np.maximum(deg,1))@A
 _,count=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0,return_counts=True)
 # Preserve true external open boundaries; joined label borders have two incident faces.
 raw=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);ue,ec=np.unique(raw,axis=0,return_counts=True);boundary=np.zeros(len(v),bool);boundary[np.unique(ue[ec!=2])]=True
 sw=spatial_weight(v)*bp*protect;sw[boundary]=0
 if group=='arterial':
  main=np.concatenate([load('ICA cavernous '+s)[0] for s in ['right','left']]+[load('ICA paraophthalmic '+s)[0] for s in ['right','left']]);dist,_=cKDTree(main).query(original);sw*=1-smooth((dist-2)/4)
  graft=[]
  for side in ['right','left']:
   par,pfaces=load('ICA cavernous '+side)
   for child in ['Meningohypophyseal trunk','Inferolateral trunk']:
    cv,_=load(child+' '+side);hit=np.isin(keys(par),keys(cv));graft.append(par[np.unique(pfaces[hit[pfaces].any(1)])])
  gd,_=cKDTree(np.concatenate(graft)).query(original);sw*=smooth((gd-.12)/.65)
 else:
  main=np.concatenate([load('vein.cavernous.'+s)[0] for s in ['right','left']]);dist,_=cKDTree(main).query(original);sw*=1-smooth((dist-5)/7)
 if group=='venous':
  sw*=smooth((artery_distance(v)-.65)/.8)
  if (ROOT/'constraints.json').exists():
   c=json.load(open(ROOT/'constraints.json'));dd,_=cKDTree(c['venousLocalFreezeCentres']).query(original);sw*=smooth((dd-c['radiusMm'])/c['transitionMm'])
 deformed=v.copy()
 before=np.linalg.norm(P@v-v,axis=1)
 for _ in range(int(os.environ.get("SMOOTH_PAIRS","18"))):
  v+=.42*sw[:,None]*(P@v-v)
  v-=.43*sw[:,None]*(P@v-v)
 delta=v-deformed;mag=np.linalg.norm(delta,axis=1);cap=.055 if group=='arterial' else .10;delta*=np.minimum(1,cap/np.maximum(mag,1e-9))[:,None];v=deformed+delta
 after=np.linalg.norm(P@v-v,axis=1);m=sw>.2;smoothing.append({'group':group,'iterations':int(os.environ.get('SMOOTH_PAIRS','18')),'activeVertices':int(m.sum()),'meanLaplacianBeforeMm':float(before[m].mean()),'meanLaplacianAfterMm':float(after[m].mean()),'maximumDisplacementMm':float(np.linalg.norm(v-original,axis=1).max())});print(smoothing[-1],flush=True)
 # Recalculate normals on the common connected surface, then retain original per-label topology.
 vv=v.astype('<f4');nf=vtk.vtkPolyDataNormals();nf.SetInputData(poly(vv.astype(float),f));nf.SplittingOff();nf.ConsistencyOn();nf.Update();nn=vtk_to_numpy(nf.GetOutput().GetPointData().GetNormals()).astype('<f4');nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
 for n,a,b,faces in ranges:
  inds=inv[a:b];out=vv[inds];old,_=load(n)
  if np.array_equal(out,old.astype('<f4')):continue
  out.tofile(OUT/(n+'.positions.bin'));faces.astype('<u4').tofile(OUT/(n+'.indices.bin'));nn[inds].astype('<f4').tofile(OUT/(n+'.normals.bin'));row=next(r for r in rows if r['name']==n);changed.append({'node':n,'file':row['file']})
  if n.startswith('vein.cavernous.'):
   slices=[]
   for y in [-54,-50,-46,-42,-38]:
    mask=np.abs(old[:,1]-y)<.5;slices.append({'yMm':y,'roofBeforeMm':float(old[mask,2].max()),'roofAfterMm':float(out[mask,2].max()),'meanRoofReductionMm':float((old[mask,2]-out[mask,2])[old[mask,2]>np.percentile(old[mask,2],90)].mean())})
   measure.append({'side':n.split('.')[-1],'slices':slices})
revision={'baseVersion':'0.9.32','release':'0.9.33','changed':changed,'newLabels':[],'baselineAssetHashes':json.loads((DATA/'source-assets.json').read_text()),'method':'16-step bone/artery-constrained posterior sinus roof flow with native collar constraints; 18 bounded Taubin pairs on connected labelled arterial/venous surfaces; native topology and protected OA/SHA walls retained'}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2));(OUT/'refinement.json').write_text(json.dumps({'posteriorHeight':measure,'smoothing':smoothing},indent=2));print('Changed',len(changed),'labels',flush=True)
