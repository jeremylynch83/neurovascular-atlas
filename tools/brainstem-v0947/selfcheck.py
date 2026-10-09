"""Check non-adjacent triangle intersections before and after the deformation."""
from common import *
from scipy.spatial import cKDTree
names=json.loads((WORK/'connected-nodes.json').read_text())
def intersections(v,f,welded,moved):
    t=v[f].astype(float);c=t.mean(1);r=np.linalg.norm(t-c[:,None],axis=2).max(1)
    lo=t.min(1);hi=t.max(1);tree=cKDTree(c);pairs=set()
    areas=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)
    locator=vtk.vtkStaticCellLocator();locator.SetDataSet(poly(v,f));locator.BuildLocator()
    ids=vtk.vtkIdList()
    for a in np.flatnonzero(moved):
        if areas[a]<=1e-10:continue
        bounds=[lo[a,0]-1e-8,hi[a,0]+1e-8,lo[a,1]-1e-8,hi[a,1]+1e-8,lo[a,2]-1e-8,hi[a,2]+1e-8]
        locator.FindCellsWithinBounds(bounds,ids)
        for j in range(ids.GetNumberOfIds()):
            b=ids.GetId(j)
            if b==a or (b<a and moved[b]) or areas[b]<=1e-10:continue
            if np.any(lo[a]>hi[b]+1e-8) or np.any(lo[b]>hi[a]+1e-8):continue
            if np.any(welded[a,:,None]==welded[b,None,:]):continue
            if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.add(tuple(sorted((int(a),int(b)))))
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
    cap_pairs=[]
    if n.startswith('brain.pons.'):
        # Artificial medial closures are almost planar in x; retain them as explicit evidence.
        for a,b in new:
            points=v[f[[a,b]]].reshape(-1,3)
            if np.ptp(points[:,0])<.04 and .5<points[:,0].mean()<.8:cap_pairs.append((a,b))
    check=dict(artificialMedialClosurePairs=sorted(cap_pairs),node=n,nonAdjacentPairsBefore=len(before),nonAdjacentPairsAfter=len(current),
               changedRawPairs=sorted(new),maximumNewPairDistanceFromExistingSiteMm=float(distances.max()) if len(distances) else 0.,
               pairsOutsideExistingJunctionSites=[p for p,d in zip(sorted(new),distances) if d>.15 and p not in cap_pairs])
    checks.append(check);print(json.dumps(check),flush=True)
report=dict(release='0.9.47',passed=all(not r['pairsOutsideExistingJunctionSites'] for r in checks),checks=checks,
            strictRawPairIdentityPassed=all(not r['changedRawPairs'] for r in checks),
            existingJunctionSiteToleranceMm=.15,
            scope='All triangle pairs involving a moved face; exact coincident vertices welded for adjacency; pre-existing zero-area faces excluded. Pair changes within 0.15 mm of existing self-contact sites are reported separately. This is not a watertight mesh certificate.')
(OUT/'self-intersections.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['passed']:sys.exit(1)
