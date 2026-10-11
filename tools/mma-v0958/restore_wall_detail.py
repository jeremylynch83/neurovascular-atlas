"""Reject failed coordinate smoothing and restore source calibre/detail.

Harmonic displacement collars preserve every native interface. Unlike
coordinate Laplacian smoothing, displacement smoothing does not shrink the
original tube wall. Pial bodies replay the saved anatomical reference fields.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.spatial.distance import cdist
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
m=ast.parse((Path(__file__).parent/'complete_pial_fit.py').read_text());exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='field'],type_ignores=[]),'field','exec'))
rev=json.loads((OUT/'revision.json').read_text());old=json.loads((OUT/'arterial-fold-repair.json').read_text());interfaces=json.loads((OUT/'field-interface-check.json').read_text())['exactSharedInterfaces'];fields=[(np.load(WORK/'reference-fit-field-pass1.npz'),.2),(np.load(WORK/'reference-fit-field.npz'),.02)];reports=[]
for r in old['results']:
 if r['passed']:continue
 n=r['node'];sv,sf=load(n);v,f=load(n,OUT);base=WORK.parent/'work-v0957/candidate';b,_=load(n,base)if(base/(n+'.positions.bin')).exists()else load(n);native=np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel();partners={r['a']if r['b']==n else r['b']for r in interfaces if n in [r['a'],r['b']]};foreign=set()
 for k in partners:foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
 pin=np.array([bytes(k)in foreign for k in native])
 if n.startswith('MMA posterior cavernous'):
  x=np.load(WORK.parent/'work-v0956-outward'/(n+'.curve.npz'));par=x['param'];tt=x['tt'];delta=v-b;shift=np.array([np.average(delta,weights=np.exp(-((par-t)/.5)**2)+1e-30,axis=0)for t in tt]);b+=np.column_stack([np.interp(par,tt,shift[:,k])for k in range(3)])
 elif not n.startswith(('MMA ','Middle meningeal')):
  for x,width in fields:b+=field(b,x,width)
 ids=np.flatnonzero(pin);dd=cKDTree(b[ids]).query(b)[0];boundary=pin|(dd>8.);free=np.flatnonzero(~boundary);fixed=np.flatnonzero(boundary);d=np.zeros_like(v);d[ids]=v[ids]-b[ids]
 edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]];ww=1/np.maximum(np.linalg.norm(b[aa]-b[bb],axis=1),.025);g=coo_matrix((ww,(aa,bb)),shape=(len(v),len(v))).tocsr();lap=diags(np.asarray(g.sum(1)).ravel())-g
 if len(free):d[free]=spsolve((lap[free][:,free]+diags(np.full(len(free),1e-5))).tocsc(),-(lap[free][:,fixed]@d[fixed]))
 q=b+d;q[ids]=v[ids]
 # Weld displacement copies of a physical source point, including isolated
 # hard-normal patches. A small zero-displacement regulariser anchors any
 # detached component with no constrained port.
 _,inv,cnt=np.unique(sv,axis=0,return_inverse=True,return_counts=True);val=np.zeros((len(cnt),3));np.add.at(val,inv,q);val/=cnt[:,None]
 for j in ids:val[inv[j]]=v[j]
 q=val[inv];assert np.isfinite(q).all();before=intersections(sv,sf);oldnew=intersections(v,f)-before;new=intersections(q,f)-before
 write(n,q,f)
 for row in rev['changed']:
  if row['node']==n:row.update(maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()),field='harmonic-displacement-wall-restoration',failedLaplacianTrialRejected=True)
 reports.append(dict(node=n,newPairsBeforeRestoration=len(oldnew),newPairsAfterRestoration=len(new),nativePinnedVertices=len(ids),maximumWallRestorationMm=float(np.linalg.norm(q-v,axis=1).max()),passed=not new));print(reports[-1],flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'wall-detail-restoration.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
