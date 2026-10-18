from common import *
import hashlib
from regional_validation import validate_regional
T=W/'accepted';overrides={}
for n in ['ACA A5 right','Precuneal right']:
 p=T/(n+'.positions.bin');q=T/(n+'.indices.bin');overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
s=Scene(A,CACHE,{**baseline_overrides,**overrides});n='ACA falcine branch right';C={n:(np.fromfile(T/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(T/(n+'.indices.bin'),'<u4').reshape(-1,3))};report=validate_regional(s,C,[{'id':'right-aca-falcine','nodes':['ACA A5 right','ACA falcine branch right','Precuneal right']}]);(T/'collar-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:report[k]for k in ['passed','issues','nativeNetworks','trianglePairsChecked']},flush=True)

sys.exit(0 if report['passed'] else 1)
