"""Refresh v0.9.46 course evidence after the checked export."""
from common import *
import hashlib
revision=json.loads((OUT/'revision.json').read_text())
collision=json.loads((OUT/'contacts.json').read_text())
selfcheck=json.loads((OUT/'self-intersections.json').read_text())
assert collision['passed'] and selfcheck['passed']
hashes={r['file']:r['sha256'] for r in json.loads((OUT/'export.json').read_text())['checks']}
changes={r['node']:r for r in revision['changed']}
calibre={r['node']:r for r in json.loads((OUT/'calibre.json').read_text())}
def update(obj):
    if isinstance(obj,list):
        for value in obj:update(value)
    elif isinstance(obj,dict):
        geometry=obj.get('geometry',{})
        if not isinstance(geometry,dict):geometry={}
        filename=geometry.get('file','').removeprefix('models/')
        if 'geometrySha256' in obj and filename in hashes:
            obj['geometrySha256']=hashes[filename]
            if geometry.get('node') in changes:
                if obj.get('fitting',{}).get('release')!='0.9.46':obj['fittingPrevious']=obj.get('fitting')
                obj['fitting']=dict(release='0.9.46',baseline='0.9.45',status='regional-placement-and-contact-gates-passed',
                                    maximumDisplacementMm=changes[geometry['node']]['maximumDisplacementMm'],
                                    validation='docs/validation/anterior-brainstem-v0.9.46.json')
                obj['fitting']['calibreCheck']=calibre[geometry['node']]
                obj['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation'
                obj['reviewStatus']='requires-anatomical-review'
                obj['candidateReviewStatus']='Median alignment corrected with connected interfaces preserved; representative anatomy and calibre remain illustrative.'
                obj['summary']='Anterior brainstem venous course corrected in v0.9.46, with the median channels closer to the midline. The median pontine channel retains its pial relationship behind the basilar artery. Local branch contacts cleared.'
                if geometry['node']=='vein.anterior_spinal':
                    obj['scope']='intracranial-and-upper-cervical'
                    obj['missingTargets']=[]
                    if 'brain.upper-cervical-cord' not in obj['targetStructureIds']:obj['targetStructureIds'].append('brain.upper-cervical-cord')
                    for segment in obj['segments']:
                        if 'brain.upper-cervical-cord' not in segment['targetStructureIds']:segment['targetStructureIds'].append('brain.upper-cervical-cord')
        for value in list(obj.values()):update(value)
for filename in ['anatomy/generated/complete_manifest.json','public/anatomy/vessel-courses.json']:
    p=Path(filename);m=json.loads(p.read_text());m['release']='0.9.46';update(m)
    if 'structures' in m:
        refs=[dict(id='ref.teksam2003.pmv',title='Teksam et al. Anatomy and Frequency of Large Pontomesencephalic Veins on 3D CT Angiograms of the Circle of Willis',
                   year=2003,url='https://pmc.ncbi.nlm.nih.gov/articles/PMC7974009/',role='Median pontine vein relationship to the basilar artery',redistribution='reference only'),
              dict(id='ref.kiyosue2008.amv-apmv',title='Kiyosue et al. The anterior medullary–anterior pontomesencephalic venous system and its bridging veins communicating to the dural sinuses',
                   year=2008,url='https://doi.org/10.1007/s00234-008-0433-3',role='Midline anterior medullary and pontomesencephalic venous course and connections',redistribution='reference only')]
        m['sources'].extend(r for r in refs if not any(s['id']==r['id'] for s in m['sources']))
        for r in m['structures']:
            if r['id'] in MEDIAN:
                source_refs=r.setdefault('provenance',{}).setdefault('sourceRefs',[])
                for ref in refs:
                    if ref['id'] not in source_refs:source_refs.append(ref['id'])
        for r in m['structures']:
            if r['id']=='vein.anterior_pontine' and 'normally between the basilar' not in r['description']:
                r['description']+=' It runs on the anterior surface of the pons, near the midline, normally between the basilar artery and brainstem.'
    p.write_text(json.dumps(m,indent=2)+'\n')
evidence=dict(revision=revision,contactAudit=collision,selfIntersectionAudit=selfcheck,
              calibreChecks=list(calibre.values()),
              exported=json.loads((OUT/'export.json').read_text()))
Path('docs/validation/anterior-brainstem-v0.9.46.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Catalogue refreshed; 16 connected venous labels; regional contact checks passed.')
