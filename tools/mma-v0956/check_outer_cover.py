"""Probe skull ray exits. Diagnostic only: not a segmented bone canal."""
from clear_neural import *
trees=[]
for name in ['bone.sphenoid','bone.frontal','bone.occipital','bone.parietal.right','bone.parietal.left','bone.temporal.right','bone.temporal.left']:
    v,f=load(name);tree=vtk.vtkOBBTree();tree.SetDataSet(poly(v,f));tree.BuildLocator();trees.append(tree)
data=np.load(WORK/'outward-flow.npz');q=data['final'];r=data['radii']
guides=json.loads((WORK/'tree-guides.json').read_text());rows=[];start=0
for g in guides:
    normal=-np.asarray(g['innerTableNormals'])[::3];normal/=np.linalg.norm(normal,axis=1)[:,None]
    covers=[]
    for i,n in enumerate(normal):
        p=q[start+i];dist=[]
        for tree in trees:
            pts=vtk.vtkPoints();ids=vtk.vtkIdList();tree.IntersectWithLine(p-15*n,p+30*n,pts,ids)
            if pts.GetNumberOfPoints():dist.extend((vtk_to_numpy(pts.GetData())-p)@n)
        covers.append(float(max(dist)-r[start+i]) if dist else None)
    finite=[x for x in covers if x is not None]
    row=dict(node=g['node'],minimumCoverMm=min(finite) if finite else None,negativeCoverStations=sum(x<0 for x in finite),missingRayIntersections=sum(x is None for x in covers),cover=covers)
    print({k:v for k,v in row.items() if k!='cover'},flush=True);rows.append(row);start+=len(normal)
(WORK/'outward-cover.json').write_text(json.dumps(dict(method=__doc__,results=rows),indent=2))
