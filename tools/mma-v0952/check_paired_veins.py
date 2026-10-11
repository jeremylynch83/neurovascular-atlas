from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
tree=ast.parse((Path(__file__).parent/'self_check.py').read_text())
definition=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='intersections')
exec(compile(ast.Module(body=[definition],type_ignores=[]),'self_check.py','exec'))
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
rows=json.loads((OUT/'paired-channel-candidates.json').read_text())['channels']
mesh={n:load(n,OUT) if n in changed else load(n) for n in FILES}
for channel in rows:
    mesh[channel['node']]=load(channel['node'],OUT)
checks=[]
for row in rows:
    name=row['node'];v,f=load(name,OUT);folds=intersections(v,f)
    tri=v[f];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
    volume=float(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()/6)
    lo=v.min(0)-.2;hi=v.max(0)+.2;contacts_found=[]
    for n,(w,g) in mesh.items():
        if n==name:continue
        if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
        t=w[g];take=np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)
        nc=contacts(v,f,w,g[take])
        if nc:contacts_found.append(dict(other=n,triangleContacts=nc,intendedReceiver=n==row['receiver'],boneCanalUnsegmented=n.startswith('bone.')))
    report=dict(node=name,selfIntersectionPairs=len(folds),degenerateTriangles=int(np.sum(area<1e-11)),signedVolumeMm3=volume,contacts=contacts_found)
    checks.append(report);print(json.dumps(report),flush=True)
distinct=[]
for side in ['left','right']:
    a=load('vein.middle_meningeal.anterior.'+side,OUT)
    b=load('vein.middle_meningeal.posterior.'+side,OUT)
    identical=np.array_equal(a[0],b[0]) and np.array_equal(a[1],b[1])
    distinct.append(dict(side=side,distinctMeshes=not identical))
(OUT/'paired-channel-validation.json').write_text(json.dumps(dict(status='provisional-not-exported',checks=checks,pairedMeshesDistinct=distinct),indent=2))
