"""Persist exact checks and an audit register without claiming full closure."""
from common import *
import hashlib
import shutil
rev=json.loads((OUT/'revision.json').read_text());val=json.loads((OUT/'validation.json').read_text());selfs=json.loads((OUT/'self-intersections.json').read_text());new=set(rev['newLabels']);paths=json.loads((OUT/'new-vein-paths.json').read_text());routes={r['node']:r for r in paths};classified=[]
for c in val['contacts']:
 if c['a'] not in new and c['b'] not in new:category='retained regional baseline relationship; compare face counts'
 else:
  n=c['a'] if c['a'] in new else c['b'];other=c['b'] if n==c['a'] else c['a'];receiver=routes[n]['attachment']['receiver']
  category='intended receiver volume attachment' if other==receiver else ('unsegmented bony canal corridor, containment unresolved' if other.startswith('bone.') else 'unexpected contact requiring correction')
 classified.append(dict(**c,classification=category))
preserved={fn:hashlib.sha256((Path('public/anatomy/models')/fn).read_bytes()).hexdigest()==sha for fn,sha in rev['baselineAssetHashes'].items() if fn!='venous.glb'}
report=dict(preservedAssetChecks=preserved,release='0.9.50',baseline='0.9.49',newSelectableVenousLabels=len(new),checks=dict(preservedAssetsExact=all(preserved.values()),actualLoaderExact=json.loads((OUT/'loader.json').read_text())['passed'],noNewDegenerateFaces=val['passedNewDegenerateFaces'],fixedNativeCollars=val['passedSharedCollars'],noNewSelfIntersections=selfs['passed'],newSurfacesConnected=json.loads((OUT/'new-surface-components.json').read_text())['passed'],newSurfacesClosed=all(r['boundaryEdges']==0 and r['nonManifoldEdges']==0 for r in val['meshChecks'] if r['node'] in new)),contacts=classified,unresolvedCanalContacts=[c for c in classified if c['classification'].startswith('unsegmented')],unexpectedNewContacts=[c for c in classified if c['classification'].startswith('unexpected')],wholeAtlasCertified=False)
(OUT/'release-checks.json').write_text(json.dumps(report,indent=2)+'\n');dest=Path('docs/validation');dest.mkdir(exist_ok=True)
for src,name in [('revision.json','relationships-revision'),('validation.json','relationships-geometry'),('self-intersections.json','relationships-self-intersections'),('release-checks.json','relationships'),('sinus-screens.json','sinus-stations'),('deformation-trials.json','sinus-deformation-trials'),('export.json','relationships-export'),('loader.json','relationships-loader'),('rejected-trial-summary.json','rejected-meningeal-trial'),('new-surface-components.json','new-surface-components')]:
 if (OUT/src).exists():shutil.copyfile(OUT/src,dest/(name+'-v0.9.50.json'))
register=[dict(item='Incorrect left incisive and orbital MMA passage associations',status='resolved in v0.9.49; retained',evidence='Previous relationship release and unchanged catalogue associations'),dict(item='Facial/deep facial and superficial temporal pairing',status='regional correction retained from v0.9.49; anatomical variants remain',evidence='Existing meshes unchanged in v0.9.50'),dict(item='Frontal MMA surface support',status='regional tubular rebuild retained from v0.9.49',evidence='Arterial asset unchanged'),dict(item='Lateral transverse sinus skull apposition',status='screen reconciled; no displacement needed',evidence='Corrected local bone set includes adjacent parietal bone, omitted by original screen'),dict(item='Superior and inferior petrosal shaft support',status='partially implemented',evidence='Constrained shaft fitting; all native shared collar coordinates fixed; medial free outlets retained'),dict(item='Inferior alveolar and infraorbital venous companions',status='selected bilateral proximal/reference courses implemented',evidence='Separate selectable meshes and represented pterygoid drainage; intrabony containment unresolved'),dict(item='Central retinal venous companion',status='selected bilateral ophthalmic drainage reference implemented',evidence='Optic nerve, globe and alternative drainage patterns absent'),dict(item='Paired anterior middle meningeal veins',status='open; trial rejected',evidence='Trial introduced neural/arterial contacts and converging stem crossings; excluded from release'),dict(item='Internal auditory veins',status='selected bilateral CPA drainage reference implemented',evidence='Other intrabony and aqueduct venous routes omitted'),dict(item='Vertebral venous system',status='regional plexiform component implemented; full fit open',evidence='Cervical vertebrae and exact foraminal levels absent'),dict(item='Hypoglossal and internal acoustic canal containment',status='open; requires detailed canal segmentation',evidence='Coarse bone surface overlaps cannot establish lumen containment'),dict(item='Supraorbital, ethmoidal, stylomastoid and Vidian guides',status='open; requires independent route/foramen definition',evidence='Approximate point references do not define canal centrelines; no forced point fitting'),dict(item='Mastoid emissary and posterior condylar veins',status='open; requires variant selection and reliable bony aperture definitions',evidence='No separately segmented canal geometry suitable for safe placement')]
(dest/'audit-register-v0.9.50.json').write_text(json.dumps(dict(release='0.9.50',wholeAuditClosed=False,items=register),indent=2)+'\n')
text='''# Audit continuation v0.9.50

This release continues the v0.9.48 relationship audit on the validated v0.9.49 baseline. It is a reference teaching reconstruction. The complete audit is not closed.

## Implemented

- Constrained local petrosal shaft fitting, with every native shared collar coordinate fixed and nearby arterial courses protected.
- Bilateral selectable inferior alveolar, infraorbital, central retinal, selected CPA internal auditory and regional vertebral periarterial venous surfaces.
- Named drainage relationships, authored reference paths, source citations and explicit review status for every new label.
- Correction of the transverse sinus support screen: the original bone set omitted adjacent parietal bone. The existing lateral course is retained.

All new calibres are illustrative. The inferior alveolar representation stops before dental terminal branches. Retinal courses represent a selected superior ophthalmic drainage variant. The anterior meningeal trial was rejected for collisions and is not included. Internal auditory courses show a selected CPA route, not the entire intrabony labyrinthine venous system. The vertebral addition is a selected connected regional plexiform component, not a claim of complete microscopic anatomy.

## Still open

Fine orbital/skull-base guides need independent bony route definitions. Hypoglossal, internal acoustic, inferior alveolar and infraorbital canal containment cannot be certified by this coarse skull. Cervical vertebrae, exact foraminal levels, nerves and optic nerve/globe anatomy are absent. Mastoid emissary and posterior condylar routes need reliable aperture definitions and a selected variant. Medial petrosal free outlet transitions remain under anatomical review.

Existing baseline self-intersections and contacts are retained where outside the accepted corrections. Numerical checks do not establish clinical accuracy, lumen patency, exhaustive venous coverage or whole-atlas watertightness.

## Verification

'''
text+='The production build and actual Three.js/Meshopt loader are checked after export. Full reports are in `docs/validation/relationships-*-v0.9.50.json`. New surfaces are checked for closed manifold edges, degenerate faces and non-adjacent triangle intersections. Existing surfaces are compared against exact original face IDs, and native shared collars against original coordinates. Skull, brain and arterial assets are retained byte for byte.\n\n'
text+='Bone contacts along unsegmented canal corridors remain open findings, explicitly separated from intended venous receiver attachments. See `relationships-v0.9.50.json` and `audit-register-v0.9.50.json`.\n\n'
text+='The before-and-after PNG renders exact mesh triangles with matched cameras and scale. Vessels are isolated for inspection; the image does not prove bone containment.\n\n## Audit register\n\n| Item | Status |\n| --- | --- |\n'
for r in register:text+='| '+r['item']+' | '+r['status']+' |\n'
text+='\n## Reproduction\n\nDecode the exact v0.9.49 model assets using `tools/decode-posterior-baseline.mjs` into a work directory `decoded/`. Then run the scripts under `tools/audit-finish-v0950/` with that work directory as the first argument: `fit_sinuses.py`, `limit_deformation.py`, `extract_companions.py`, `add_veins.py`, `add_vertebral_plexus.py`, `add_retinal.py`, `repair_infraorbital.py`, `validate.py`, `self_check.py`, `check_components.py`, `export.mjs`, `catalogue.py`, production build, `check_export.mjs`, `report.py`, and `render_comparison.py`. Run from the app directory. Python scripts take the work directory as their first argument. The Node exporter takes `work/candidate` and the exact v0.9.49 GLB directory; the Node loader check takes `work/candidate` and `work/decoded`. Evidence and reference paths are included; transient decoded buffers are excluded from delivery.\n'
Path('docs/AUDIT_CONTINUATION_v0.9.50.md').write_text(text);print(json.dumps(report['checks']));print('Unexpected contacts',len(report['unexpectedNewContacts']))
assert all(report['checks'].values()),'Failed geometric release check'
assert not report['unexpectedNewContacts'],'Unexpected new contacts'
