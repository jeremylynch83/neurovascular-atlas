"""Paired anterior meningeal channel candidates, kept out of public assets.

The receiver stem overlaps the retained lesser-wing channel. It is not yet a
merged exterior wall; that independent acceptance condition remains explicit.
"""
from smooth_fields import *
from vein_geometry import resample
from scipy.ndimage import gaussian_filter

def solid(curves,spacing=.12):
    allq=np.concatenate([q for q,r in curves]);lo=allq.min(0)-1;hi=allq.max(0)+1
    dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1)
    field=np.full(tuple(dims),3.,np.float32)
    for q,r in curves:
        for a,b,ra,rb in zip(q[:-1],q[1:],r[:-1],r[1:]):
            pad=max(ra,rb)+.35
            low=np.maximum(np.floor((np.minimum(a,b)-pad-lo)/sp).astype(int),0)
            high=np.minimum(np.ceil((np.maximum(a,b)+pad-lo)/sp).astype(int)+1,dims)
            sl=tuple(slice(int(x),int(y)) for x,y in zip(low,high))
            pp=np.stack(np.meshgrid(*[lo[i]+np.arange(low[i],high[i])*sp[i] for i in range(3)],indexing='ij'),axis=-1)
            ab=b-a;t=np.clip(np.sum((pp-a)*ab,axis=-1)/max(np.dot(ab,ab),1e-12),0,1)
            sdf=np.linalg.norm(pp-a-t[...,None]*ab,axis=-1)-(ra*(1-t)+rb*t)
            field[sl]=np.minimum(field[sl],sdf)
    field=gaussian_filter(field,.55)
    im=vtk.vtkImageData();im.SetDimensions(*dims);im.SetOrigin(*lo);im.SetSpacing(*sp)
    im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(order='F'),deep=True))
    iso=vtk.vtkFlyingEdges3D();iso.SetInputData(im);iso.SetValue(0,0);iso.ComputeNormalsOff();iso.Update()
    fair=vtk.vtkWindowedSincPolyDataFilter();fair.SetInputConnection(iso.GetOutputPort());fair.SetNumberOfIterations(12);fair.SetPassBand(.15);fair.BoundarySmoothingOff();fair.NormalizeCoordinatesOn();fair.Update()
    pd=fair.GetOutput();v=vtk_to_numpy(pd.GetPoints().GetData()).copy();f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
    tri=v[f]
    if np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()<0:f=f[:,[0,2,1]]
    return v,f

field=arterial_field();guides=json.loads((WORK/'tree-guides.json').read_text());rows=[]
for side in ['right','left']:
    suffix=' left' if side=='left' else '';parts=[];radii=[];norms=[]
    for base in ['Middle meningeal','MMA frontal']:
        g=next(g for g in guides if g['node']==base+suffix)
        q=np.asarray(g['oldPoints']);r=np.asarray(g['radiusMm']);n=np.asarray(g['innerTableNormals'])
        if q[0,2]>q[-1,2]:q=q[::-1];r=r[::-1];n=n[::-1]
        take=q[:,2]>=49
        if parts:take&=q[:,2]>parts[-1][-1,2]+.25
        parts.append(q[take]);radii.append(r[take]);norms.append(n[take])
    raw=np.concatenate(parts);rr=np.concatenate(radii);nn=np.concatenate(norms)
    original=resample(raw,.15);k=cKDTree(raw).query(original)[1]
    artery=field(original);r=rr[k];normal=gaussian_filter1d(nn[k],12,axis=0)
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
    tangent=np.gradient(artery,axis=0);tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-12)
    transverse=np.cross(tangent,normal);transverse/=np.maximum(np.linalg.norm(transverse,axis=1)[:,None],1e-12)
    transverse=gaussian_filter1d(transverse,8,axis=0);transverse/=np.maximum(np.linalg.norm(transverse,axis=1)[:,None],1e-12)
    # RAS +Y is anterior on both sides. The cross-product sign reverses
    # between hemispheres, so normalise it before assigning channel labels.
    if np.median(transverse[:,1])<0:transverse=-transverse
    receiver='vein.sphenoparietal.'+side;rv,rf=load(receiver);loc=locator(rv,rf)
    for label,sign in [('anterior',1),('posterior',-1)]:
        name='vein.middle_meningeal.'+label+'.'+side
        q=artery+sign*transverse*(r+.5)[:,None]-normal*.15
        q=gaussian_filter1d(q,2,axis=0)
        radius=.24-.045*smooth((q[:,2]-110)/35)
        j=np.argmin(abs(q[:,2]-79))
        cp,d=closest(loc,q[j:j+1]);cp=cp[0]
        direction=cp-q[j];direction/=max(np.linalg.norm(direction),1e-8)
        end=cp+direction*.35
        stem=resample(np.vstack([q[j],q[j]+(end-q[j])*.3,end]),.12)
        v,f=solid([(q,radius),(stem,np.full(len(stem),.23))])
        write(name,v,f)
        np.savez(OUT/(name+'.curve.npz'),q=q,r=radius,stem=stem)
        edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
        con=vtk.vtkPolyDataConnectivityFilter();con.SetInputData(poly(v,f));con.SetExtractionModeToAllRegions();con.Update()
        row=dict(node=name,file='venous.glb',vertices=len(v),triangles=len(f),boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),components=con.GetNumberOfExtractedRegions(),receiver=receiver,receiverSurfaceEntryPoint=cp.tolist(),receiverStemLengthMm=float(np.linalg.norm(end-q[j])),attachment='Provisional receiver-volume overlap. A merged exterior junction remains required before release.',illustrativeRadiusMm=[float(radius.min()),float(radius.max())])
        rows.append(row);print(row,flush=True)
(OUT/'paired-channel-candidates.json').write_text(json.dumps(dict(status='provisional-not-exported',channels=rows,source='San Millan Ruiz et al. AJNR 2004;25:112-120. PMID 14729539. Figure 3 and accompanying anatomical dissection.',duplicatedLesserWingChannel=False,receiverExteriorMerged=False),indent=2))
rev=json.loads((OUT/'revision.json').read_text())
new={row['node'] for row in rows}
rev['changed']=[row for row in rev['changed'] if row['node'] not in new]
rev['newLabels']=sorted(new)
rev['changed']+=rows
(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
