from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent;A=W/'inr-anatomy-atlas-v0.9.121';B=W.parent/'ophthalmic-work/inr-anatomy-atlas-v0.9.120';rows=json.loads((W/'changes.json').read_text());refs=json.loads((W/'references.json').read_text())
def read(p):return json.loads(p.read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
m=read(B/'anatomy/generated/complete_manifest.json');byid={s['id']:s for s in m['structures']}
for r in rows:
 assert byid[r['id']]['description']==r['before'],r['id'];byid[r['id']]['description']=r['after']
m['release']='0.9.121';m['descriptionAudit']={'release':'0.9.121','baseline':'0.9.120','reviewedPopulatedDescriptions':1295,'revisedDescriptions':len(rows),'correctionList':'docs/Description_Audit_v0.9.121.html','overrides':'anatomy/metadata/description-corrections-v0.9.121.json','scope':'Descriptions only. Structure names, geometry, parentage, anatomical relationships, segment boundaries and DSA data retained.'}
write(A/'anatomy/generated/complete_manifest.json',m);write(A/'public/anatomy/manifest.json',m)
write(A/m['descriptionAudit']['overrides'],{'schema':1,'release':'0.9.121','references':refs,'entries':rows})
for name in ['package.json','package-lock.json']:
 d=read(A/name);d['version']='0.9.121'
 if name=='package-lock.json':d['packages']['']['version']='0.9.121'
 write(A/name,d)
c=read(B/'public/anatomy/vessel-courses.json');c['release']='0.9.121';write(A/'public/anatomy/vessel-courses.json',c)
for file in ['Description_Audit_v0.9.121.html','inventory.json','references.json']:
 target=A/'docs'/file;shutil.copy2(W/file,target)
for target in [A/'public/docs/Description_Audit_v0.9.121.html']:shutil.copy2(W/'Description_Audit_v0.9.121.html',target)
T=A/'tools/descriptions-v0.9.121';T.mkdir(exist_ok=True)
for file in ['prepare.py','brain_bone.py','report.py','apply.py']:shutil.copy2(W/file,T/file)
p=A/'README.md';s=p.read_text().replace('# Neurovascular Atlas v0.9.120','# Neurovascular Atlas v0.9.121',1).replace('inr-anatomy-atlas-v0.9.120.zip','inr-anatomy-atlas-v0.9.121.zip').replace('verifies v0.9.120','verifies v0.9.121');s=s.replace('\n\n','\n\nDescription audit: 666 entries revised to focus on the selected structure, with targeted anatomical corrections. The searchable before/after list is docs/Description_Audit_v0.9.121.html. Geometry and DSA data are unchanged.\n\n',1);p.write_text(s)
p=A/'CHANGELOG.md';p.write_text('# v0.9.121\n\nAudit all 1,295 populated descriptions. Revise 666 entries: 361 arteries, 57 veins, 193 brain structures and 55 bony landmarks. Replace copied parent/sibling passages with structure-specific course, location, territory or endpoint descriptions. Correct targeted anatomical claims and leaked authoring link labels. Retain intentional contralateral links and normal variation. Include the complete before/after correction list and a build-time description overlay. Preserve all geometry, graph relationships, model labels, segment bounds, DSA recipes and flow data.\n\n'+p.read_text())
print('Applied',len(rows),'description corrections')
