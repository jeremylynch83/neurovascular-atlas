#!/usr/bin/env python3
"""Import the reviewed Markdown catalogue. This is an editing tool, not a build step."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'docs/STRUCTURE_DESCRIPTIONS.md'
path = ROOT / 'anatomy/generated/complete_manifest.json'
manifest = json.loads(path.read_text())
by_id = {s['id']: s for s in manifest['structures']}
text = source.read_text()
blocks = re.split(r'<a id="structure-([^\"]+)"></a>', text)
entries = dict(zip(blocks[1::2], blocks[2::2]))
if set(entries) != set(by_id):
    raise SystemExit('The description catalogue and model structure IDs do not match.')

descriptions = {}
for id, block in entries.items():
    description = re.search(r'\*\*Description\*\*\s*\n\n(.*?)(?=\n\n\*\*Source:\*\*)', block, re.S)
    if not description:
        continue
    value = description[1].strip()
    if not value:
        raise SystemExit(f'Empty description: {id}')
    targets = re.findall(r'\]\(#structure-([^\)]+)\)', value)
    if any(target not in by_id for target in targets):
        raise SystemExit(f'Unknown description link target: {id}')
    descriptions[id] = value

renames = {
    'artery.eca.middle_temporal.right': 'Posterior deep temporal artery right',
    'artery.eca.middle_temporal.right.left': 'Posterior deep temporal artery left',
    'artery.eca.posterior_deep_temporal.right': 'Middle deep temporal artery right',
    'artery.eca.posterior_deep_temporal.right.left': 'Middle deep temporal artery left',
    'artery.eca.maxillary.foramen_rotundum.right': 'Artery of the foramen rotundum right',
    'artery.eca.maxillary.foramen_rotundum.right.left': 'Artery of the foramen rotundum left',
}
for id, name in renames.items():
    structure = by_id[id]
    old_name = structure['name']
    aliases = [old_name, re.sub(r' (?:right|left)$', '', old_name), re.sub(r' (?:right|left)$', '', name)]
    structure['aliases'] = list(dict.fromkeys(structure['aliases'] + aliases))
    structure['name'] = name
    # Keep human-readable labels in the reviewed document in step with the model.
    text = text.replace(f'### {old_name}\n', f'### {name}\n')
    text = text.replace(f'[{old_name}](#structure-{id})', f'[{name}](#structure-{id})')

# Dental/alveolar are equivalent terms in the supplied notes.
for structure in manifest['structures']:
    id = structure['id']
    if id.startswith('artery.eca.maxillary.inferior_alveolar.'):
        structure['aliases'] = list(dict.fromkeys(structure['aliases'] + ['Inferior dental artery', 'Inferior dental (or alveolar) artery']))
    elif id.startswith('artery.eca.maxillary.posterior_superior_alveolar.'):
        structure['aliases'] = list(dict.fromkeys(structure['aliases'] + ['Posterior superior dental artery']))
    if id in descriptions:
        structure['description'] = descriptions[id]
    else:
        structure.pop('description', None)

manifest['release'] = json.loads((ROOT / 'package.json').read_text())['version']
ref = {'id': 'ref.lynch.neurovascular-notes', 'title': 'Jeremy Lynch: Neurovascular anatomy, supplied nv(2).pdf',
       'role': 'Authoritative structure description text and terminology',
       'notes': 'Reviewed mapping and source pages are in docs/STRUCTURE_DESCRIPTIONS.md.'}
if not any(s['id'] == ref['id'] for s in manifest['sources']):
    manifest['sources'].append(ref)
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
source.write_text(text)
print(f'Imported {len(descriptions)} descriptions; reconciled {len(renames)} display names.')
