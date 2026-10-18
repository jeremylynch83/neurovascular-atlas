"""Recheck the staged regional meshes against the retained baseline and atlas."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'repair'))
from cache import Scene
from regional_validation import validate_regional
W,A,C=map(Path,sys.argv[1:4]);overrides={}
for p in (W/'decoded').glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=W/'decoded'/(n+'.indices.bin');overrides[n]={'positions':str(p.resolve()),'indices':str(q.resolve()),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,C,overrides);parts={}
for n in ['Occipital left','Occipital mastoid left','ILT posterior branch left']:
 parts[n]=(np.fromfile(W/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(W/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3))
nets=[{'id':'occipital-root','nodes':['Occipital left','Occipital mastoid left']},{'id':'ilt-complete','nodes':['ILT posterior branch left','ILT anterior branch left','Inferolateral trunk left','ILT posteromedial ramus left']}]
report=validate_regional(scene,parts,nets);(W/'rechecked-regional-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:report[k]for k in ['passed','issues','nativeNetworks','trianglePairsChecked']});sys.exit(0 if report['passed']else 1)
