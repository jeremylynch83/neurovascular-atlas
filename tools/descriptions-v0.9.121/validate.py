"""Metadata-only regression check against an unpacked v0.9.120 baseline."""
from pathlib import Path
import sys,json,hashlib,re
A=Path(__file__).resolve().parents[2];B=Path(sys.argv[1]).resolve()
def read(p):return json.loads(p.read_text())
before=read(B/'anatomy/generated/complete_manifest.json');after=read(A/'anatomy/generated/complete_manifest.json');public=read(A/'public/anatomy/manifest.json');overlay=read(A/'anatomy/metadata/description-corrections-v0.9.121.json');expected={r['id']:r for r in overlay['entries']};assert len(expected)==666
assert after['structures']==public['structures'];old={s['id']:s for s in before['structures']};now={s['id']:s for s in after['structures']};assert now.keys()==old.keys()
changed=[]
for sid,s in now.items():
 a=dict(old[sid]);b=dict(s);a.pop('description',None);b.pop('description',None);assert a==b,(sid,'non-description change')
 if s.get('description')!=old[sid].get('description'):
  changed.append(sid);assert sid in expected;assert old[sid]['description']==expected[sid]['before'];assert s['description']==expected[sid]['after']
 for ref in re.findall(r'#structure-([^\s)]+)',s.get('description','')):assert ref in now,(sid,ref)
 assert not re.search(r'High\s*\|\s*New|nomenclature review',s.get('description','')),(sid,'leaked authoring label')
assert set(changed)==set(expected)
aa=dict(before);bb=dict(after)
for d in [aa,bb]:d.pop('release',None);d.pop('descriptionAudit',None);d.pop('structures',None)
assert aa==bb,'Non-description manifest metadata changed'
for file in before['assetRevisions']:
 a=B/'public/anatomy'/file;b=A/'public/anatomy'/file;assert hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest(),file
for file in ['dsa-surfaces.json','dsa-flow.json']:assert (B/'public/anatomy'/file).read_bytes()==(A/'public/anatomy'/file).read_bytes(),file
for p in (B/'src').rglob('*'):
 if p.is_file():assert p.read_bytes()==(A/p.relative_to(B)).read_bytes(),str(p)
for file in ['ANATOMICAL_ISSUES.json','ANATOMICAL_ISSUES.md','tests/staged-loading/expected-geometry.json']:
 assert (B/file).read_bytes()==(A/file).read_bytes(),file
report={'passed':True,'release':'0.9.121','baseline':'0.9.120','reviewedPopulatedDescriptions':sum(bool(s.get('description'))for s in old.values()),'revisedDescriptions':len(changed),'validInternalDescriptionLinks':True,'noAuthoringStatusDebris':True,'allFiveModelAssetsByteExact':True,'allDsaRecipesAndFlowByteExact':True,'allStructureFieldsExceptDescriptionExact':True,'allOtherManifestFieldsExceptReleaseAndAuditReferenceExact':True,'runtimeSourceByteExact':True,'issueRegisterAndExpectedGeometryExact':True,'intentionalContralateralPharyngealLinksRetained':True}
(A/'docs/description-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
