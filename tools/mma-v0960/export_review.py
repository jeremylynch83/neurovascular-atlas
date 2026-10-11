"""Embed source and final candidate meshes with independent topology per mode."""
import sys,base64,gzip,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
mf=json.loads(Path('public/anatomy/manifest.json').read_text());cat={s.get('asset',{}).get('node'):s for s in mf['structures']};by={s['id']:s for s in mf['structures']}
names={n for n in FILES if 'MMA' in n or n.startswith(('Middle meningeal','brain.','ICA cavernous'))}
names.update(['bone.sphenoid','bone.frontal','bone.occipital','bone.parietal.right','bone.parietal.left','bone.temporal.right','bone.temporal.left','vein.sphenoparietal.right','vein.sphenoparietal.left'])
for n in list(names):
    for id in cat.get(n,{}).get('endpoints',[]):
        k=by.get(id,{}).get('asset',{}).get('node')
        if k in FILES:names.add(k)
names.update(rev['newLabels'])
reference=json.loads((OUT/'tentorial-reference-correction-v0960.json').read_text())
if reference['installed']:names.update(r['node'] for r in reference['results'])
names=sorted(names)
chunks=[];offset=0;rows=[];buffer_checks=[]
def append(a):
    global offset
    raw=a.tobytes();at=offset;chunks.append(raw);offset+=len(raw);return at
sha=lambda b:hashlib.sha256(b).hexdigest()
for n in names:
    new=n not in FILES
    sv,sf=load(n,OUT)if new else load(n)
    v,f=load(n,OUT)if n in changed else(sv,sf)
    sv=sv.astype('<f4');sf=sf.astype('<u4');v=v.astype('<f4');f=f.astype('<u4')
    kind='brain'if n.startswith('brain.')else'bone'if n.startswith('bone.')else'vein'if n.startswith('vein.')else'artery'
    row=dict(name=n,label=cat.get(n,{}).get('name',n.replace('vein.middle_meningeal.anterior.','Anterior middle meningeal vein ').replace('vein.middle_meningeal.posterior.','Posterior middle meningeal vein ')),kind=kind,vertices=len(sv),triangles=len(sf),positionOffset=append(sv),indexOffset=append(sf),candidateOffset=None,candidateIndexOffset=None,candidateOnly=new)
    if n in changed:
        row.update(candidateOffset=append(v),candidateIndexOffset=append(f),candidateVertices=len(v),candidateTriangles=len(f))
    row['side']='left'if n.endswith(('.left',' left'))else'right'if n.endswith(('.right',' right'))or n.startswith(('MMA ','Middle meningeal'))else'both'
    rows.append(row)
    for mode,a,g in [('source',sv,sf),('candidate',v,f)]:buffer_checks.append(dict(node=n,mode=mode,positionSha256=sha(a.tobytes()),indicesSha256=sha(g.tobytes())))
acceptance=json.loads((OUT/'acceptance-continuation.json').read_text())
validation=dict(neuralPairs=acceptance['mmaNeuralContactPairs'],baselineNeuralPairs='Not assessed',newFolds=acceptance['newPerLabelArterialFolds']+acceptance['newPerLabelBrainFolds'],interfaceGapMm=acceptance['nativeInterfaceMismatchMm'],veinNeuralPairs=acceptance['receiverNeuralContactPairs'],containmentPairs=acceptance['strictContainmentPairCount'],excludedBrainParcels=acceptance['excludedContainmentBrainParcels'],referenceContactPairs=acceptance['cortexTentoriumContactPairs'],remainingRoutes=sorted({r['artery']for r in acceptance['mmaNeuralContacts']}))
data=b''.join(chunks)
for row in rows:
    for mode in ['source','candidate']:
        use=mode=='candidate'and row['candidateOffset']is not None
        po=row['candidateOffset']if use else row['positionOffset'];io=row['candidateIndexOffset']if use else row['indexOffset'];nv=row['candidateVertices']if use else row['vertices'];nf=row['candidateTriangles']if use else row['triangles']
        check=next(r for r in buffer_checks if r['node']==row['name']and r['mode']==mode)
        assert sha(data[po:po+nv*12])==check['positionSha256']
        assert sha(data[io:io+nf*12])==check['indicesSha256']
meta=json.dumps(dict(meshes=rows,validation=validation,licenceText=Path('public/anatomy/licenses/Z_Anatomy_Source_Licence.txt').read_text()),separators=(',',':'))
packed=base64.b64encode(gzip.compress(data,mtime=0)).decode();js=next(Path('review-v0960/bundle/assets').glob('*.js')).read_text()
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neurovascular Atlas v0.9.60 review</title><body><div id="app"></div><script type="application/json" id="mesh-meta">'+meta.replace('</','<\\/')+'</script><script type="application/octet-stream" id="mesh-data">'+packed+'</script><script type="module">'+js.replace('</script','<\\/script')+'</script></body></html>'
destination=Path(sys.argv[2])if len(sys.argv)>2 else Path('deliverables');destination.mkdir(parents=True,exist_ok=True);path=destination/'Neurovascular_Atlas_MMA_review_v0.9.60.html';path.write_text(html)
report=dict(file=str(path),bytes=path.stat().st_size,sha256=sha(path.read_bytes()),meshCount=len(rows),exactBufferComparisons=len(buffer_checks)*2,topologyPerModeSupported=True,brainAndVeinComparisonSupported=True,validation=validation,bufferChecks=buffer_checks)
(WORK/'review-export-continuation.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items()if k!='bufferChecks'})
