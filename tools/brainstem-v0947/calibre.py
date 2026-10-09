"""Estimate changes in wall radius using original geodesic sections."""
from common import *
from extract_curves import extract
from types import SimpleNamespace
from scipy.ndimage import gaussian_filter1d
checks=[]
for name in json.loads((WORK/'connected-nodes.json').read_text()):
    if name.startswith('brain.'):continue
    v,f=load(name);after,_=load(name,OUT)
    q,rad,param,tt=extract(SimpleNamespace(v=v,f=f))
    centres=[]
    for t in tt:
        ix=abs(param-t)<.3
        centres.append((after[ix]-v[ix]).mean(0) if ix.any() else (after-v)[np.argsort(abs(param-t))[:16]].mean(0))
    qn=q+gaussian_filter1d(np.array(centres),2.,axis=0)
    def radius(vertices,line):
        p=np.column_stack([np.interp(param,tt,line[:,j]) for j in range(3)])
        tang=np.gradient(line,tt,axis=0);tang/=np.maximum(np.linalg.norm(tang,axis=1)[:,None],1e-9)
        tangent=np.column_stack([np.interp(param,tt,tang[:,j]) for j in range(3)])
        tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-9)
        d=vertices-p
        return np.sqrt(np.maximum(0,(d*d).sum(1)-(d*tangent).sum(1)**2))
    before_radius=radius(v,q);after_radius=radius(after,qn)
    keep=(before_radius>.1)&(param>tt[0]+1)&(param<tt[-1]-1)
    ratio=after_radius[keep]/before_radius[keep]
    check=dict(node=name,method='Section-mean displacement and tangent with original geodesic stations; cap-adjacent points excluded. Illustrative calibre estimate, unreliable at bifurcations.',
               ratioP05MedianP95=np.percentile(ratio,[5,50,95]).tolist(),
               p95AbsoluteFractionalRadiusChange=float(np.percentile(abs(ratio-1),95)))
    checks.append(check);print(json.dumps(check),flush=True)
(OUT/'calibre.json').write_text(json.dumps(checks,indent=2)+'\n')
