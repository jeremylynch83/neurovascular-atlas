"""Replace oscillating receiver stems with direct endpoint-preserving courses."""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
from scipy.ndimage import gaussian_filter
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/build_paired_veins.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef) and x.name=='solid'],type_ignores=[]),'solid','exec'))
rev=json.loads((OUT/'revision.json').read_text());rows=json.loads((OUT/'paired-channel-candidates.json').read_text())['channels'];reports=[]
for side in ['right','left']:
 n='vein.middle_meningeal.posterior.'+side;x=np.load(OUT/(n+'.curve.npz'));q=x['q'];r=x['r'];old=x['stem'];s=np.linspace(0,1,max(12,int(np.linalg.norm(old[-1]-old[0])/.1)+1));stem=(1-s[:,None])*old[0]+s[:,None]*old[-1]
 v,f=solid([(q,r),(stem,np.full(len(stem),.23))]);write(n,v,f);np.savez(OUT/(n+'.curve.npz'),q=q,r=r,stem=stem)
 for row in rows:
  if row['node']==n:row.update(vertices=len(v),triangles=len(f),receiverStemMethod='Direct endpoint-preserving course')
 for row in rev['changed']:
  if row['node']==n:row.update(vertices=len(v),triangles=len(f),field='direct-companion-receiver-stem')
 reports.append(dict(node=n,oldStemLengthMm=float(np.linalg.norm(np.diff(old,axis=0),axis=1).sum()),newStemLengthMm=float(np.linalg.norm(np.diff(stem,axis=0),axis=1).sum()),endpointMismatchMm=0.))
 print(reports[-1],flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'paired-channel-candidates.json').write_text(json.dumps(dict(status='provisional-not-exported',channels=rows,duplicatedLesserWingChannel=False,receiverExteriorMerged=False),indent=2))
(OUT/'receiver-stem-rebuild.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
