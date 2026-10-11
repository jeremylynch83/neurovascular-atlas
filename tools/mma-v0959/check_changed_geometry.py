"""Recheck every label modified since the immutable v0.9.58 checkpoint."""
from route_tools import *
baseline=WORK.parent/'work-v0958/candidate';rows=[]
for n in FILES:
 v,f=current(n)
 if not (baseline/(n+'.positions.bin')).exists():continue
 bv,bf=load(n,baseline)
 if np.array_equal(v,bv) and np.array_equal(f,bf):continue
 sv,sf=load(n);source=intersections(sv,sf);candidate=intersections(v,f);new=candidate-source
 edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);oldlen=np.linalg.norm(sv[edges[:,1]]-sv[edges[:,0]],axis=1);newlen=np.linalg.norm(v[edges[:,1]]-v[edges[:,0]],axis=1);ratios=newlen[oldlen>.05]/oldlen[oldlen>.05]
 row=dict(node=n,baseline=len(source),candidate=len(candidate),newIntersections=len(new),newPairs=[list(p) for p in sorted(new)],maximumAdditionalShiftMm=float(np.linalg.norm(v-bv,axis=1).max()),edgeLengthRatioPercentiles=np.percentile(ratios,[0,1,5,50,95,99,100]).tolist(),edgeRatioOutsideHalfToDouble=int(((ratios<.5)|(ratios>2)).sum()));rows.append(row);print(row,flush=True)
(OUT/'continuation-geometry-validation.json').write_text(json.dumps(dict(results=rows,passed=all(r['newIntersections']==0 for r in rows)),indent=2))
