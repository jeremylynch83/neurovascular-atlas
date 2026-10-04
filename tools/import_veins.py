#!/usr/bin/env python3
"""Import authored venous catalogue; optional editing tool, not a build step."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=json.loads((ROOT/'anatomy/source/venous/courses.json').read_text())
path=ROOT/'anatomy/generated/complete_manifest.json'
m=json.loads(path.read_text())
m['structures']=[s for s in m['structures'] if s['system']!='vein']
m['relationships']=[r for r in m['relationships'] if not r['from'].startswith('vein') and not r['to'].startswith('vein')]
provenance={'sourceType':'teaching-reconstruction','confidence':'Note-guided courses fitted to existing bone and arterial landmarks; depth and calibre estimated','reviewStatus':'unreviewed','sourceRefs':['ref.lynch.neurovascular-notes','ref.venous-authoring-2026']}
def group(id,name,parent):return {'id':id,'name':name,'parent':parent,'children':[],'kind':'group','system':'vein','side':'midline','aliases':[],'geometryStatus':'web-optimised','provenance':provenance.copy()}
m['structures'].append(group('vein','Veins',None))
for key,name in spec['groups'].items():m['structures'].append(group('vein.'+key,name,'vein'))
for s in spec['structures']:
 row={k:s[k] for k in ['id','name','parent','side','aliases','color']}
 row.update(system='vein',kind='structure',children=[],geometryStatus='web-optimised',provenance=provenance.copy(),asset={'file':'models/venous.glb','node':s['id']})
 row['notes']=f"Lynch Neurovascular anatomy, printed p{s['page']}. Reference teaching reconstruction, not patient-derived anatomy. Selected bilateral reference pattern; small tributaries and variants are not exhaustive. Calibre is illustrative."
 if s['description']:row['description']=s['description']
 if 'anterior_condylar' in s['id']:row['notes']+=' Hypoglossal canal region follows the existing landmark; its lumen is unresolved in this bone mesh.'
 if 'jugular' in s['id'] or 'vertebral.' in s['id'] or 'deep_cervical' in s['id']:row['notes']+=' Lower cervical end is truncated to the current field of view; thoracic termination is not modelled.'
 m['structures'].append(row)
byid={s['id']:s for s in m['structures']}
for s in m['structures']:
 if s['system']=='vein':s['children']=[r['id'] for r in m['structures'] if r.get('parent')==s['id']]
m['relationships']+=spec['relationships'];m['roots']=[s['id'] for s in m['structures'] if s['parent'] is None]
source={'id':'ref.venous-authoring-2026','title':'Main venous reconstruction, 4 October 2026','year':2026,'role':'Lynch pp62-76 and Figs2.16-2.19: principal courses, drainage relationships and descriptions; fitted to retained atlas bone and arterial landmarks.','notes':'docs/VENOUS_v0.9.0.md records variant choices, source discrepancy resolution and limitations. Neuroangio original angiographic cases were used as a spatial cross-check, not as measured geometry: https://neuroangio.org/venous-brain-anatomy/'}
m['sources']=[s for s in m['sources'] if s['id']!=source['id']]+[source]
m['release']=spec['release']
for asset in {s['asset']['file'] for s in m['structures'] if s.get('asset')}:
 p=ROOT/'public/anatomy'/asset
 if p.exists():m['assetByteSizes'][asset]=p.stat().st_size;m['assetRevisions'][asset]=hashlib.sha256(p.read_bytes()).hexdigest()[:20]
for s in m['structures']:
 for target in re.findall(r'\]\(#structure-([^\)]+)\)',s.get('description','')):assert target in byid,(s['id'],target)
path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
# Extend the established editable description catalogue without altering old text.
md=ROOT/'docs/STRUCTURE_DESCRIPTIONS.md';text=md.read_text();marker='\n## Venous structures added in v0.9.0\n';text=text.split(marker)[0]+marker
for s in m['structures']:
 if s['system']!='vein':continue
 text+=f'\n<a id="structure-{s["id"]}"></a>\n\n### {s["name"]}\n\n'
 if s.get('description'):text+='**Description**\n\n'+s['description']+'\n\n'
 src=next((x for x in spec['structures'] if x['id']==s['id']),None)
 text+='**Source:** '+(f'Lynch, supplied nv(2).pdf, printed p{src["page"]}.' if src else 'Display group.')+'\n'
md.write_text(text)
print(f'Imported {len(spec["structures"])} venous meshes; {sum(bool(s["description"]) for s in spec["structures"])} descriptions.')
