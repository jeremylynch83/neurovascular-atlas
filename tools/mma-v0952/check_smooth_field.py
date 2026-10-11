from smooth_fields import *
import hashlib
rev=json.loads((OUT/'revision.json').read_text())
changed={r['node'] for r in rev['changed']}
old=[];new=[];owners=[];names=sorted(FILES)
for j,n in enumerate(names):
    v,f=load(n);q,g=load(n,OUT) if n in changed else (v,f)
    # Remeshed surfaces do not retain source vertex numbering. Keep source
    # slots only for exact surviving native coordinates. Missing coordinates
    # propagate NaN and fail the shared-interface check.
    if q.shape!=v.shape or not np.array_equal(f,g):
        distance,index=cKDTree(q).query(v);q=q[index].copy();q[distance>1e-7]=np.nan
    old.append(v.astype('<f4'));new.append(q.astype('<f4'));owners.append(np.full(len(v),j,np.int32))
v=np.concatenate(old);q=np.concatenate(new);ids=np.concatenate(owners)
keys=np.ascontiguousarray(v).view(np.dtype((np.void,12))).ravel()
order=np.argsort(keys);kk=keys[order]
same=kk[1:]==kk[:-1];a=order[:-1][same];bb=order[1:][same]
take=ids[a]!=ids[bb];a=a[take];bb=bb[take]
gap=np.linalg.norm(q[a]-q[bb],axis=1)
rows=[]
for ia,ib in sorted(set(zip(ids[a],ids[bb]))):
    take=(ids[a]==ia)&(ids[bb]==ib)
    rows.append(dict(a=names[ia],b=names[ib],sharedVertexPairs=int(take.sum()),missingNativeCoordinates=int(np.isnan(gap[take]).sum()),maxMismatchMm=float(np.max(gap[take][np.isfinite(gap[take])])) if np.isfinite(gap[take]).any() else None))
report=dict(exactSharedInterfaces=rows,maxMismatchMm=float(gap[np.isfinite(gap)].max()) if np.isfinite(gap).any() else 0.,missingNativeCoordinatePairs=int(np.isnan(gap).sum()),passedSharedCollars=bool(np.isfinite(gap).all() and np.all(gap<1e-4)),scope='Exact native coincident coordinates across every source mesh, including unchanged neighbours.')
del old,new,v,q,keys,order,kk,ids
fields=[]
points=np.stack(np.meshgrid(np.arange(-76,77,4),np.arange(-145,-5,4),np.arange(35,170,4),indexing='ij'),axis=-1).reshape(-1,3)
for label,field in ([] if '--interfaces-only' in sys.argv else [('arterial',arterial_field()),('cortical',cerebral_field(8.))]):
    jac=np.zeros((len(points),3,3));eps=.02
    for axis in range(3):
        off=np.zeros(3);off[axis]=eps
        jac[:,:,axis]=(field(points+off)-field(points-off))/(2*eps)
    det=np.linalg.det(jac)
    strain=np.linalg.svd(jac-np.eye(3),compute_uv=False)[:,0]
    fields.append(dict(field=label,sampleCount=len(points),minimumJacobianDeterminant=float(det.min()),maximumSampledDisplacementGradient=float(strain.max()),positiveJacobianSamples=bool(np.all(det>0)),largestSampledDisplacementMm=float(np.linalg.norm(field.displacement(points),axis=1).max())))
report['coordinateFields']=fields
if '--interfaces-only' in sys.argv:
    report['fieldSamplingStatus']='Not evaluated. Checks actual candidate native interfaces only; does not assume an active cortical deformation.'
(OUT/'field-interface-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='exactSharedInterfaces'},indent=2),flush=True)
