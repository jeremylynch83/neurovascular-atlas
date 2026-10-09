"""Refresh exact asset hashes and barycentric brain bindings after the crossing correction."""
from common import *
import hashlib
revision=json.loads((OUT/'revision.json').read_text())
hashes={r['file']:r['sha256'] for r in json.loads((OUT/'export.json').read_text())['checks']}
changes={r['node']:r for r in revision['changed']}
calibre={r['node']:r for r in json.loads((OUT/'calibre.json').read_text())}
p=Path('anatomy/generated/complete_manifest.json');m=json.loads(p.read_text());rows={s['id']:s for s in m['structures']}
brainhash=hashes['brain-context.glb']
def anchor(a):
    n=rows[a['structureId']]['asset']['node'];v,f=load(n,OUT if n in changes else DATA)
    a['position']=(v[f[a['triangleIndex']]]*np.array(a['barycentric'])[:,None]).sum(0).tolist();a['assetSha256']=brainhash
for s in rows.values():
    n=s.get('asset',{}).get('node')
    if s.get('surfaceAnchor'):
        anchor(s['surfaceAnchor']);s['landmark']['point']=s['surfaceAnchor']['position']
    for a in s.get('secondarySurfaceAnchors',[]):anchor(a)
    if n in changes and s.get('asset',{}).get('file')=='models/brain-context.glb':
        v,f=load(n,OUT);s['anatomy']['bounds']=[v.min(0).tolist(),v.max(0).tolist()];s['anatomy']['centroid']=v.mean(0).tolist();s['anatomy']['regionalAdjustmentRelease']='0.9.47'
    c=s.get('vesselCourse')
    if c:
        c['brainAssetSha256']=brainhash
        fn=s['asset']['file'].removeprefix('models/')
        if fn in hashes:c['geometrySha256']=hashes[fn]
        if n in changes:
            if c.get('fitting',{}).get('release')!='0.9.47':c['fittingPrevious']=c.get('fitting')
            c['fitting']=dict(release='0.9.47',baseline='0.9.46',status='crossing-corrected-junction-mesh-review-pending',maximumDisplacementMm=changes[n]['maximumDisplacementMm'],validation='docs/validation/transverse-pontine-v0.9.47.json',calibreCheck=calibre[n])
            c['reviewStatus']='requires-anatomical-review';c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation'
            c['summary']='The transverse pontine midline crossing passes posterior to the basilar artery, between artery and pons. Connected junctions follow the correction; small arterial branches are checked individually.'
for s in rows.values():
    ids=s.get('vesselGuide',{}).get('anchorIds',[])
    if ids:s['landmark']['course']=[rows[k]['surfaceAnchor']['position'] for k in ids]
for s in rows.values():
    if s['id'].startswith('vein.transverse_pontine.'):
        if 'At the midline' not in s.get('description',''):s['description']=s.get('description','')+' At the midline, transverse pontine venous anastomoses normally pass posterior to the basilar artery, between the artery and pons.'
        refs=s.setdefault('provenance',{}).setdefault('sourceRefs',[])
        if 'ref.teksam2003.pmv' not in refs:refs.append('ref.teksam2003.pmv')
m['release']='0.9.47';m['brainRegistration']['registeredAssetSha256']=brainhash
adj=dict(release='0.9.47',brainSha256=brainhash,method='Local pontine groove recess, maximum 3.5 mm; arteries fixed.',evidence='docs/validation/transverse-pontine-v0.9.47.json')
m['brainRegistration']['regionalAdjustments']=[r for r in m['brainRegistration'].get('regionalAdjustments',[]) if r.get('release')!='0.9.47']
m['brainRegistration']['regionalAdjustments'].append(adj)
m['brainAdjustmentPolicy']['appliedAdjustments']=[r for r in m['brainAdjustmentPolicy'].get('appliedAdjustments',[]) if r.get('release')!='0.9.47']
m['brainAdjustmentPolicy']['appliedAdjustments'].append(dict(release='0.9.47',status='crossing-context-adjustment-awaiting-anatomical-review',geometry=[r for r in revision['changed'] if r['file']=='brain-context.glb'],completeVenousRefitApplied=False,evidence=adj['evidence']))
p.write_text(json.dumps(m,indent=2)+'\n')
p=Path('public/anatomy/vessel-courses.json');e=json.loads(p.read_text());e.update(release=m['release'],brainRegistration=m['brainRegistration'],brainAdjustmentPolicy=m['brainAdjustmentPolicy'])
def refresh(o):
 if isinstance(o,list):
  for x in o:refresh(x)
 elif isinstance(o,dict):
  if o.get('structureId') in rows and 'geometrySha256' in o:o.update(rows[o['structureId']]['vesselCourse'])
  if 'brainAssetSha256' in o:o['brainAssetSha256']=brainhash
  g=o.get('geometry',{})
  if isinstance(g,dict) and 'geometrySha256' in o and g.get('file','').removeprefix('models/') in hashes:o['geometrySha256']=hashes[g['file'].removeprefix('models/')]
  for x in list(o.values()):refresh(x)
refresh(e)
# Course export uses id as its structure key.
for c in e.get('courses',[]):
 key=c.get('vesselId',c.get('id',c.get('structureId')))
 if key in rows and rows[key].get('vesselCourse'):c.update(rows[key]['vesselCourse'])
p.write_text(json.dumps(e,indent=2)+'\n')
print('Asset hashes, brain anchors and course evidence refreshed.')
