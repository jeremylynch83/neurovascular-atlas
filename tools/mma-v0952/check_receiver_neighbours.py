"""Audit the completed shared exterior against the actual candidate scene.

Unchanged source receiver triangles are identified exactly, so native
collector connections do not count as newly generated wall contacts.
Bone contacts are explicitly reported as unresolved, never exempted.
"""
from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
m=ast.parse((Path(__file__).parent/'finish_receiver_seams.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef) and x.name=='triangle_keys'],type_ignores=[]),'keys','exec'))
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
results=[]
for side in ['right','left']:
    receiver='vein.sphenoparietal.'+side
    x=np.load(OUT/('receiver-seam-completed-'+side+'.npz'));v=x['v'].astype(float);f=x['f']
    sv,sf=load(receiver);sourcekeys=set(triangle_keys(sv,sf))
    keys=triangle_keys(v,f);newmask=np.array([k not in sourcekeys for k in keys]);newf=f[newmask]
    lo=v[newf].min((0,1));hi=v[newf].max((0,1));rows=[]
    for n in FILES:
        if n==receiver:continue
        w,g=load(n,OUT) if n in changed else load(n)
        if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
        t=w[g];g=g[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
        if not len(g):continue
        count=contacts(v,newf,w,g)
        if count:
            r=dict(other=n,triangleContacts=count,domain='bone' if n.startswith(('bone.','tooth')) else 'neural' if n.startswith('brain.') else 'vascular',accepted=False)
            rows.append(r);print(side,r,flush=True)
    tri=v[f];areas=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)*.5
    report=dict(side=side,generatedTriangles=len(newf),retainedSourceTriangles=int((~newmask).sum()),degenerateTriangles=int(np.sum(areas<1e-10)),minimumTriangleAreaMm2=float(areas.min()),contacts=rows,noNewNeuralOrVascularContacts=not any(r['domain']!='bone' for r in rows),boneRelationsAccepted=not any(r['domain']=='bone' for r in rows))
    results.append(report)
(OUT/'receiver-neighbour-validation.json').write_text(json.dumps(results,indent=2))
print(json.dumps([{k:v for k,v in row.items() if k!='contacts'} for row in results],indent=2),flush=True)
