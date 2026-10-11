"""Set skull-facing controls for each convexity shaft and retain basal anchors."""
from vein_geometry import *

def inner_table(side):
    vv=[];ff=[]
    for name in ['bone.sphenoid','bone.temporal.'+side,'bone.parietal.'+side,'bone.frontal','bone.occipital']:
        v,f=load(name);tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
        centre=tri.mean(1)
        keep=np.einsum('ij,ij->i',normal,centre-[0,-60,95])<0
        ff.append(f[keep]+sum(len(x) for x in vv));vv.append(v)
    v=np.concatenate(vv);f=np.concatenate(ff)
    n=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12)
    return locator(v,f),n

bases=['Middle meningeal','MMA frontal','MMA frontal anterior division','MMA frontal posterior division','MMA posterior convexity','MMA parietal ascending','MMA posterior terminal','MMA petrosquamosal']
rows=[]
for side in ['right','left']:
    loc,ns=inner_table(side)
    suffix=' left' if side=='left' else ''
    for base in bases:
        name=base+suffix;x=np.load(WORK/(name+'.curve.npz'))
        q=x['q'];r=x['r'];cp=[];nn=[]
        cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.);point=[0.,0.,0.]
        for p in q:
            loc.FindClosestPoint(p,point,cid,sub,d2);cp.append(point.copy());nn.append(ns[int(cid)])
        cp=np.asarray(cp);nn=gaussian_filter1d(np.asarray(nn),12,axis=0)
        nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
        target=cp+nn*(r+.25)[:,None]
        delta=gaussian_filter1d(target-q,10,axis=0)
        if base=='Middle meningeal':delta*=smooth((q[:,2]-44)/12)[:,None]
        # No calvarial projection for the low petrous portion.
        if base=='MMA petrosquamosal':delta*=smooth((q[:,2]-47)/15)[:,None]
        target=q+delta
        rows.append(dict(node=name,side=side,oldPoints=q.tolist(),points=target.tolist(),radiusMm=r.tolist(),innerTablePoints=cp.tolist(),innerTableNormals=nn.tolist(),maxGuideShiftMm=float(np.linalg.norm(delta,axis=1).max())))
        print(name,round(rows[-1]['maxGuideShiftMm'],3),flush=True)
(WORK/'tree-guides.json').write_text(json.dumps(rows,indent=2))
