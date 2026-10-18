"""Record the exact pre-existing crossing that excludes the PICA vermian trial."""
from common import *
from geometry import triangle_crosses_exact
n='PICA vermian left';v,f=scene.mesh(n);a=v[f[7392]].astype(float);b=v[f[7390]].astype(float);tris=[[4108,4107,4110],[4108,4110,4109]]
baseline=triangle_crosses_exact(a,b);trial=[triangle_crosses_exact(v[t].astype(float),b)for t in tris];assert baseline and all(trial)
report={'release':'0.9.106','status':'open-trial-excluded','node':n,'sourceFaces':[7390,7392],'sourceFacePositions':[v[f[i]].tolist()for i in [7390,7392]],'baselineExactPositiveCrossing':bool(baseline),'trialExactPositiveCrossings':list(map(bool,trial)),'trialNewTriangles':tris,'sourcePositionsSha256':hashlib.sha256(v.tobytes()).hexdigest(),'sourceIndicesSha256':hashlib.sha256(f.tobytes()).hexdigest(),'productionMeshRetained':True,'conclusion':'The exact subdivision preserves an existing wall crossing and fails the strict changed-face gate. It is not installed. Local wall reconstruction remains open.'}
(W/'deferred-crossing-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report['conclusion'])
