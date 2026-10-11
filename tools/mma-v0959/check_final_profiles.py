"""Independently measure installed transverse profiles after float32 export."""
from route_tools import *
rows=[]
installed={r['node'] for r in json.loads((OUT/'continuation-geometry-validation.json').read_text())['results']}
for path in sorted(WORK.glob('*.v0959-curve.npz')):
 n=path.name[:-len('.v0959-curve.npz')]
 if n not in installed:continue
 a=np.load(WORK/(n+'.continuation-curve.npz'));b=np.load(path);v,f=load(n,WORK.parent/'work-v0958/candidate');w,_=current(n);param=b['param'];tt=b['tt'];old=np.column_stack([np.interp(param,tt,a['q'][:,k]) for k in range(3)]);new=np.column_stack([np.interp(param,tt,b['q'][:,k]) for k in range(3)]);pin=pins(n);error=abs(np.linalg.norm(v-old,axis=1)-np.linalg.norm(w-new,axis=1));row=dict(node=n,verticesChecked=int((~pin).sum()),constrainedNativeCapVertices=int(pin.sum()),maximumFreeRadialProfileErrorMm=float(error[~pin].max()),maximumConstrainedCapProfileErrorMm=float(error[pin].max()) if pin.any() else 0.,passed=bool(error[~pin].max()<1e-4));rows.append(row);print(row,flush=True)
(OUT/'installed-transverse-profile-validation.json').write_text(json.dumps(dict(method=__doc__,toleranceMm=.0001,results=rows,passed=len(rows)==len(installed) and all(r['passed'] for r in rows),fullLumenAndCalibreValidated=False,parentCollarCalibreReviewed=False,limitations=['Preserves the delivered, estimated radial profiles on the retained reconstructed bodies.','Native cap constraints are reported separately.','This does not test lumen connectivity or clinical calibre.']),indent=2))
