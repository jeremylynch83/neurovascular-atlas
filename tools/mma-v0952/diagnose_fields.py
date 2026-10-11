from smooth_fields import *
points=np.stack(np.meshgrid(np.arange(-76,77,3),np.arange(-145,-5,3),np.arange(35,170,3),indexing='ij'),axis=-1).reshape(-1,3)
rows=[]
for label,field in [('arterial',arterial_field()),('cortical',cerebral_field(8.))]:
    jac=np.zeros((len(points),3,3));eps=.02
    for axis in range(3):
        off=np.zeros(3);off[axis]=eps
        jac[:,:,axis]=(field(points+off)-field(points-off))/(2*eps)
    det=np.linalg.det(jac);gradient=np.linalg.svd(jac-np.eye(3),compute_uv=False)[:,0]
    row=dict(field=label,sampleCount=len(points),minimumJacobianDeterminant=float(det.min()),maximumSampledDisplacementGradient=float(gradient.max()),positiveJacobianSamples=bool(np.all(det>0)),largestSampledDisplacementMm=float(np.linalg.norm(field.displacement(points),axis=1).max()))
    rows.append(row);print(row,flush=True)
(WORK/'continuous-field-diagnostic.json').write_text(json.dumps(rows,indent=2))
