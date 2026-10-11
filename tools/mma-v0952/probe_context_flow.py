"""Compare a time-integrated field with the rejected direct brain displacement."""
from smooth_fields import *
import ast
module=ast.parse((Path(__file__).parent/'self_check.py').read_text());fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='intersections');exec(compile(ast.Module(body=[fn],type_ignores=[]),'self_check','exec'))
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rows=[]
for name in ['brain.superior-frontal-sulcus.right','brain.orbital-gyri.right','brain.precentral-sulcus-inferior-part.left']:
    v,f=load(name);base=intersections(v,f)
    for amp in [4.,6.,8.]:
        field=cerebral_field(amp);q=v.copy();steps=24
        for _ in range(steps):
            k=field.displacement(q)/steps;q+=field.displacement(q+k*.5)/steps
        q=q.astype('<f4').astype(float);after=intersections(q,f)
        row=dict(node=name,amplitudeMm=amp,baseline=len(base),candidate=len(after),new=len(after-base),maximumShiftMm=float(np.linalg.norm(q-v,axis=1).max()));rows.append(row);print(row,flush=True)
(WORK/'context-flow-probe.json').write_text(json.dumps(rows,indent=2))

