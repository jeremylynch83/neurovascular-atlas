"""Preserve source coincident vertices across normal/UV seams.

Surface graph solves must not give two copies of one physical point different
coordinates. Geometry coordinates are reconciled without merging labels or
changing triangle topology, and every correction is measured.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
rev=json.loads((OUT/'revision.json').read_text());reports=[]
for row in rev['changed']:
 n=row['node']
 if n not in FILES:continue
 sv,sf=load(n);v,f=load(n,OUT)
 if len(sv)!=len(v)or not np.array_equal(sf,f):continue
 _,inv,count=np.unique(sv,axis=0,return_inverse=True,return_counts=True);values=np.zeros((len(count),3));np.add.at(values,inv,v);values/=count[:,None];q=values[inv];correction=np.linalg.norm(q-v,axis=1)
 if correction.max()<1e-9:continue
 write(n,q,f);row.update(maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()),coincidentSourceVerticesPreserved=True)
 reports.append(dict(node=n,maximumCorrectionMm=float(correction.max()),correctedVertexCopies=int((correction>1e-9).sum())));print(reports[-1],flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'coincident-vertex-preservation.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
