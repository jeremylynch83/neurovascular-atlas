"""Smooth only new local arterial folds while holding all native ports exact."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.sparse import coo_matrix
rev=json.loads((OUT/'revision.json').read_text());oldreport=json.loads((OUT/'arterial-self-intersections.json').read_text());interfaces=json.loads((OUT/'field-interface-check.json').read_text())['exactSharedInterfaces'];reports=[]
for row in oldreport['results']:
 if not row['newIntersections']:continue
 n=row['node'];sv,sf=load(n);v,f=load(n,OUT);initial=v.copy();before=intersections(sv,sf);native=np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel()
 partners={r['a']if r['b']==n else r['b']for r in interfaces if n in [r['a'],r['b']]};foreign=set()
 for k in partners:foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
 pin=np.array([bytes(k)in foreign for k in native]);edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);a=np.r_[edges[:,0],edges[:,1]];b=np.r_[edges[:,1],edges[:,0]];graph=coo_matrix((np.ones(len(a)),(a,b)),shape=(len(v),len(v))).tocsr();degree=np.asarray(graph.sum(1)).ravel();steps=[]
 for it in range(24):
  new=intersections(v,f)-before
  if not new:break
  vertices=np.unique(f[np.unique(np.array(list(new)).ravel())]);distance=cKDTree(v[vertices]).query(v)[0];weight=(1-smooth(distance/1.2))*.12;weight[pin]=0
  mean=(graph@v)/np.maximum(degree[:,None],1);v+=(mean-v)*weight[:,None];steps.append(dict(iteration=it,newPairs=len(new)));print(n,it,len(new),flush=True)
 new=intersections(v,f)-before;write(n,v,f)
 for r in rev['changed']:
  if r['node']==n:r.update(maxShiftMm=float(np.linalg.norm(v-sv,axis=1).max()),localFoldRepairMm=float(np.linalg.norm(v-initial,axis=1).max()))
 reports.append(dict(node=n,passed=not new,remainingNewPairs=len(new),maximumRepairMm=float(np.linalg.norm(v-initial,axis=1).max()),nativePinnedVertices=int(pin.sum()),steps=steps))
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'arterial-fold-repair.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2));print(json.dumps(reports,indent=2))
