from common import *
from scipy.spatial import cKDTree
names=json.loads((WORK/'connected-nodes.json').read_text());x=np.load(OUT/'network.npz');v,f=x['v'],x['f'];fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f));source=np.concatenate([load(n)[0] for n in names]);keys=lambda p:np.ascontiguousarray(p.astype('<f4')).view('V12').ravel();sk=keys(source);checks=[]
for row in META:
 if row['file']!='venous.glb' or row['name'] in names:continue
 a,b=load(row['name']);shared=a[np.isin(keys(a),sk)]
 if not len(shared):continue
 distances=np.array([fn.EvaluateFunction(p.astype(float)) for p in shared]);r=dict(node=row['name'],baselineSharedVertices=len(shared),minimumSignedDistanceMm=float(distances.min()),medianSignedDistanceMm=float(np.median(distances)),verticesInsideRebuiltSolid=int(np.sum(distances<0)),connected=bool(np.any(distances<=0)));checks.append(r);print(r,flush=True)
report=dict(release='0.9.48',checks=checks,passed=all(c['connected'] for c in checks),method='Exact baseline shared attachment vertices tested against the signed distance of the rebuilt closed solid. Native endpoint collars must enter the rebuilt solid. Endpoint topology of neighbouring labels is retained; whole-atlas manifoldness is outside scope.')
(OUT/'attachments.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['passed']:sys.exit(1)
