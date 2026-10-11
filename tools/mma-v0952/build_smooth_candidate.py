"""Reconstruct skull-facing courses with continuous native-interface transport.

Candidate output only. Export requires separate geometry acceptance.
"""
from smooth_fields import *
import hashlib
manifest=json.loads(Path('public/anatomy/manifest.json').read_text())
catalogue={s['asset']['node']:s for s in manifest['structures'] if s.get('asset')}
assignments=catalogue_fields(manifest)
a=arterial_field();b=cerebral_field(8.)
revision=dict(release='0.9.52',baseline='0.9.51',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),changed=[],newLabels=[],method='Skull-facing complete convexity guides with a continuous ambient translation field across native joined arterial surfaces. Common cortical reference and pial vessel field. Public assets retained until acceptance.',guides=json.loads((WORK/'tree-guides.json').read_text()))
for name,file in sorted(FILES.items()):
    assignment=assignments.get(name,'fixed')
    if assignment=='fixed':continue
    field=b if assignment=='cortical' else a
    v,f=load(name);q=field(v);shift=np.linalg.norm(q-v,axis=1)
    if shift.max()<1e-6:continue
    write(name,q,f)
    revision['changed'].append(dict(node=name,file=file,vertices=len(v),triangles=len(f),maxShiftMm=float(shift.max()),topologyExact=True,field='cortical-reference' if field==b else 'skull-facing-arterial'))
    print(name,round(float(shift.max()),3),flush=True)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2))
print('Changed',len(revision['changed']),flush=True)
