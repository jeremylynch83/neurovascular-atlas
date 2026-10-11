"""Package exact candidate buffers into a self-contained, unreleased viewer."""
from clear_neural import *
import base64,gzip,hashlib,re
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
contact=json.loads((OUT/'full-mma-brain-check.json').read_text())
fold=json.loads((OUT/'arterial-self-intersections.json').read_text())
interface=json.loads((OUT/'field-interface-check.json').read_text())
prior=json.loads((WORK.parent/'work-v0955/candidate/acceptance.json').read_text())
categories={s['asset']['node']:s['anatomy']['category'] for s in json.loads(Path('public/anatomy/brain-landmarks.json').read_text())['surfaces']}
neural=[r for r in contact['contacts'] if categories.get(r['brain'])!='dural_reflections']
names=[n for n in FILES if n.startswith(('MMA ','Middle meningeal','brain.')) or n in ['bone.sphenoid','bone.frontal','bone.occipital','bone.parietal.right','bone.parietal.left','bone.temporal.right','bone.temporal.left']]
chunks=[];offset=0;rows=[]
def append(a):
    global offset
    raw=a.tobytes();at=offset;chunks.append(raw);offset+=len(raw);return at
for name in names:
    v,f=load(name);kind='brain' if name.startswith('brain.') else 'bone' if name.startswith('bone.') else 'artery'
    row=dict(name=name,vertices=len(v),triangles=len(f),kind=kind,positionOffset=append(v.astype('<f4')),indexOffset=append(f.astype('<u4')),candidateOffset=None)
    if name in changed:
        q,g=load(name,OUT);assert np.array_equal(f,g);row['candidateOffset']=append(q.astype('<f4'))
    row['side']='left' if name.endswith(('.left',' left')) else 'right' if name.endswith(('.right',' right')) or name.startswith(('MMA ','Middle meningeal')) else 'both'
    rows.append(row)
validation=dict(neuralPairs=len(neural),baselineNeuralPairs=None,newFolds=sum(r['newIntersections'] for r in fold['results']),interfaceGapMm=interface['maxMismatchMm'])
# Baseline display must compare with actual recovered geometry, not the previous
# unreleased checkpoint's differently positioned arteries.
baseline_report=WORK/'baseline-mma-contacts.json'
if baseline_report.exists():validation['baselineNeuralPairs']=json.loads(baseline_report.read_text())['neuralPairs']
else:validation['baselineNeuralPairs']='Not measured'
licence=Path('public/anatomy/licenses/Z_Anatomy_Source_Licence.txt').read_text()
meta=json.dumps(dict(meshes=rows,validation=validation,licenceText=licence),separators=(',',':'))
packed=base64.b64encode(gzip.compress(b''.join(chunks),mtime=0)).decode()
js=next(Path('review-v0956/bundle/assets').glob('*.js')).read_text()
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neurovascular Atlas · MMA review</title><body><div id="app"></div><script type="application/json" id="mesh-meta">'+meta.replace('</','<\\/')+'</script><script type="application/octet-stream" id="mesh-data">'+packed+'</script><script type="module">'+js.replace('</script','<\\/script')+'</script></body></html>'
path=Path('/workspace/scratch/687560554b74/deliverables/Neurovascular_Atlas_MMA_review_v0.9.56.html');path.write_text(html)
(WORK/'review-export.json').write_text(json.dumps(dict(file=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),meshCount=len(rows),validation=validation),indent=2))
print(path,path.stat().st_size,validation,flush=True)
