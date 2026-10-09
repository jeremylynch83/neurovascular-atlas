"""Compare local surface contacts, welded joins and self intersections."""
from common import *
from scipy.spatial import cKDTree
from itertools import combinations
names=json.loads((WORK/'connected-nodes.json').read_text())
cache={r['name']:load(r['name']) for r in META}
after={n:load(n,OUT)[0] for n in names}
checks=[];failures=[]
def pair_contacts(av,af,bv,bf,seam=None):
    if not len(af) or not len(bf):return set()
    c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(av,af));c.SetInputData(1,poly(bv,bf))
    t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCellTolerance(1e-7)
    c.SetCollisionModeToHalfContacts();c.Update()
    pairs=list(zip(vtk_to_numpy(c.GetContactCells(0)).tolist(),vtk_to_numpy(c.GetContactCells(1)).tolist()))
    if seam is not None and len(seam):
        points=vtk_to_numpy(c.GetContactsOutput().GetPoints().GetData()) if pairs else np.empty((0,3))
        assert len(points)==len(pairs)
        # The mesh labels have coincident collars. Half-contact output can report
        # adjacent facets within tens of microns of those shared vertices.
        keep=cKDTree(seam).query(points)[0]>.05
        pairs=[p for p,k in zip(pairs,keep) if k]
    return set(pairs)
for n in names:
    v,f=cache[n];q=after[n];moving=np.any(np.any(v[f]!=q[f],axis=2),axis=1)
    if not moving.any():continue
    lo=np.minimum(v[f[moving]].min((0,1)),q[f[moving]].min((0,1)))-1e-5
    hi=np.maximum(v[f[moving]].max((0,1)),q[f[moving]].max((0,1)))+1e-5
    for row in META:
        target=row['name']
        if target==n:continue
        a,b=cache[target];aq=after.get(target,a)
        if np.any(np.minimum(a.min(0),aq.min(0))>hi) or np.any(np.maximum(a.max(0),aq.max(0))<lo):continue
        ta=a[b];tq=aq[b]
        relevant=np.all(np.minimum(ta.min(1),tq.min(1))<=hi,axis=1)&np.all(np.maximum(ta.max(1),tq.max(1))>=lo,axis=1)
        # Include both labels' moving faces in this pair's review box.
        fa=f[moving];fb=b[relevant]
        seam=None
        if row['file']=='venous.glb':
            dist,idx=cKDTree(a).query(v)
            seam=dist<1e-5
        before=pair_contacts(v,fa,a,fb,v[seam] if seam is not None else None)
        current=pair_contacts(q,fa,aq,fb,q[seam] if seam is not None else None)
        new=current-before
        if row['file']=='venous.glb' and (before or current):
            # Interface faces are expected to meet at shared vertices. Identify
            # them in the baseline, then ignore only those specific adjacent pairs.
            dist,idx=cKDTree(a).query(v)
            shared={i:int(idx[i]) for i in np.flatnonzero(dist<1e-5)}
            def adjacent(pair):
                i,j=pair
                return any(shared.get(int(k),-1) in fb[j] for k in fa[i])
            before={p for p in before if not adjacent(p)}
            current={p for p in current if not adjacent(p)}
            new=current-before
        if before or current:
            r=dict(node=n,target=target,asset=row['file'],contactTrianglePairsBefore=len(before),
                   contactTrianglePairsAfter=len(current),newContactTrianglePairs=len(new))
            checks.append(r);print(json.dumps(r),flush=True)
            if new:failures.append(r)
    print('Audited '+n,flush=True)
report=dict(release='0.9.46',scope='All moved triangles against every intersecting anatomical label, including arteries, brain, bone and other veins. Shared venous interface adjacency and contacts within 0.05 mm of shared collar vertices excluded.',
            changedNodes=len(names),checks=checks,newContacts=failures,passed=not failures)
(OUT/'contacts.json').write_text(json.dumps(report,indent=2)+'\n')
if failures:sys.exit(1)
