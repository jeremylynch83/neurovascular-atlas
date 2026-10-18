from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=True);scene=Scene(A,Path(sys.argv[2]).resolve())
from fractions import Fraction
from geometry import triangle_crosses,triangle_crosses_exact
import importlib.util,itertools,time,hashlib
spec=importlib.util.spec_from_file_location('historical_geometry',A/'anatomy/source/intersection-v0.9.101/previous-geometry.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
n='ACA A5 right';v,f=scene.mesh(n);a=v[f[5129]].astype(float);b=v[f[5204]].astype(float)
def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
aa=[[Fraction(float(x))for x in p]for p in a];bb=[[Fraction(float(x))for x in p]for p in b];na=cross(sub(aa[1],aa[0]),sub(aa[2],aa[0]));nb=cross(sub(bb[1],bb[0]),sub(bb[2],bb[0]));da=[dot(sub(x,aa[0]),na)for x in bb];db=[dot(sub(x,bb[0]),nb)for x in aa]
assert [(x>0)-(x<0)for x in da]==[-1,0,-1];assert [(x>0)-(x<0)for x in db]==[0,-1,0];assert bb[1]==aa[2]
# A triangle meets the other plane at exactly one vertex, and both
# non-zero signed determinants have the same sign. Their intersection
# therefore cannot contain a positive-length interval or positive area.
assert old.triangle_crosses(a,b)and not triangle_crosses(a,b)
lo=np.vstack([a,b]).min(0)-.1;hi=np.vstack([a,b]).max(0)+.1;tree=scene.bvh(n);ids=tree.query(lo,hi);tt=v[f[ids]];ids=ids[np.all(tt.max(1)>=lo,axis=1)&np.all(tt.min(1)<=hi,axis=1)];pairs=set()
for i in ids:
 q=v[f[i]];ql=q.min(0)-1e-7;qh=q.max(0)+1e-7
 for j in tree.query(ql,qh):
  if i==j:continue
  r=v[f[j]]
  if np.any(r.max(0)<ql)or np.any(r.min(0)>qh):continue
  pairs.add(tuple(sorted([int(i),int(j)])))
rows=[];changed=[];start=time.perf_counter()
for i,j in sorted(pairs):
 p,q=v[f[i]].astype(float),v[f[j]].astype(float);before=old.triangle_crosses(p,q);after=triangle_crosses(p,q);exact=triangle_crosses_exact(p,q)
 if before!=after:changed.append({'faces':[i,j],'oldCrossing':before,'newCrossing':after,'exactCrossing':exact})
 if exact:rows.append({'faces':[i,j],'newPredicateCrossing':after})
report={'release':'0.9.101','baseline':'0.9.100','geometryChanged':False,'anatomicalAcceptance':False,'sourceAssets':scene.source_hashes,'node':n,'faceIndices':[5129,5204],'coordinates':[a.tolist(),b.tolist()],'oldPredicateCrossing':old.triangle_crosses(a,b),'newPredicateCrossing':triangle_crosses(a,b),'exactPredicateCrossing':triangle_crosses_exact(a,b),'independentHalfSpaceProof':{'triangleBInPlaneA':list(map(str,da)),'triangleAInPlaneB':list(map(str,db)),'signs':[[-1,0,-1],[0,-1,0]],'commonPoint':list(map(float,aa[2])),'intersection':'single-shared-vertex-only'},'localAudit':{'bounds':[lo.tolist(),hi.tolist()],'localFaces':len(ids),'trianglePairsChecked':len(pairs),'oldNewClassificationChanges':changed,'exactPositiveCrossings':rows,'seconds':time.perf_counter()-start},'scope':'Reclassifies the single recorded right A5 self-crossing pair; local exact audit does not establish whole-course anatomical acceptance.'}
(W/'predicate-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('AUDIT',len(ids),'faces',len(pairs),'pairs','changes',len(changed),'exactCrossings',rows,flush=True)
