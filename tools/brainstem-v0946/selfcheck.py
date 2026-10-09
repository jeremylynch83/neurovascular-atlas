"""Check non-adjacent triangle intersections before and after the deformation."""
from common import *
from scipy.spatial import cKDTree
names=json.loads((WORK/'connected-nodes.json').read_text())
def intersections(v,f,welded,moved):
    t=v[f].astype(float);c=t.mean(1);r=np.linalg.norm(t-c[:,None],axis=2).max(1)
    lo=t.min(1);hi=t.max(1);tree=cKDTree(c);pairs=set()
    areas=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)
    for start in range(0,len(f),64):
        ids=np.arange(start,min(start+64,len(f)));ns=tree.query_ball_point(c[ids],r[ids]+r.max())
        aa=np.repeat(ids,[len(n) for n in ns]);bb=np.concatenate(ns)
        keep=(aa<bb)&(moved[aa]|moved[bb])&(areas[aa]>1e-10)&(areas[bb]>1e-10)
        aa=aa[keep];bb=bb[keep]
        keep=np.all(lo[aa]<=hi[bb]+1e-8,axis=1)&np.all(lo[bb]<=hi[aa]+1e-8,axis=1)&(np.linalg.norm(c[aa]-c[bb],axis=1)<=r[aa]+r[bb])
        aa=aa[keep];bb=bb[keep]
        keep=~np.any(welded[aa,:,None]==welded[bb,None,:],axis=(1,2));aa=aa[keep];bb=bb[keep]
        for a,b in zip(aa,bb):
            if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.add((int(a),int(b)))
    return pairs
checks=[]
for n in names:
    v,f=load(n);q,_=load(n,OUT);_,inv=np.unique(v,axis=0,return_inverse=True)
    moved=np.any(np.any(v[f]!=q[f],axis=2),axis=1)
    before=intersections(v,f,inv[f],moved);current=intersections(q,f,inv[f],moved)
    new=current-before
    distances=np.empty(0)
    if before and new:
        tri=v[f]; centres=tri.mean(1)
        old_centres=np.array([(centres[a]+centres[b])/2 for a,b in before])
        new_centres=np.array([(centres[a]+centres[b])/2 for a,b in sorted(new)])
        distances=cKDTree(old_centres).query(new_centres)[0]
    elif new:distances=np.full(len(new),np.inf)
    check=dict(node=n,nonAdjacentPairsBefore=len(before),nonAdjacentPairsAfter=len(current),
               changedRawPairs=sorted(new),maximumNewPairDistanceFromExistingSiteMm=float(distances.max()) if len(distances) else 0.,
               pairsOutsideExistingJunctionSites=[p for p,d in zip(sorted(new),distances) if d>.15])
    checks.append(check);print(json.dumps(check),flush=True)
report=dict(release='0.9.46',passed=all(not r['pairsOutsideExistingJunctionSites'] for r in checks),checks=checks,
            strictRawPairIdentityPassed=all(not r['changedRawPairs'] for r in checks),
            existingJunctionSiteToleranceMm=.15,
            scope='All triangle pairs involving a moved face; exact coincident vertices welded for adjacency; pre-existing zero-area faces excluded. Pair changes within 0.15 mm of existing self-contact sites are reported separately. This is not a watertight mesh certificate.')
(OUT/'self-intersections.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['passed']:sys.exit(1)
