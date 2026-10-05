"""Authoring only: explicit anatomical course rules for delivered vascular labels.

Relationships remain catalogue assertions until actual joined geometry is audited.
No vessel surface is moved by this step.
"""
import hashlib, json
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
PUB = APP / 'public/anatomy'

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
    manifest = json.loads((APP / 'anatomy/generated/complete_manifest.json').read_text())
    rows = {r['id']: r for r in manifest['structures']}
    guides = [r for r in rows.values() if r.get('vesselGuide')]
    targets = [r for r in rows.values() if r.get('anatomy')]
    # modes, surfaces, description, explicitly ordered station references, missing targets
    def rule(modes, names, summary, stations=(), missing=()):
        return modes, names, summary, stations, missing

    def classify(identifier):
        key = identifier.replace('_left', '').replace('_right', '').replace('.left', '').replace('.right', '')
        if key.startswith('vein.'):
            key = key[5:]
            if key == 'straight':
                return rule(['dural-attachment'], ['Falx cerebri', 'Tentorium cerebelli'],
                    'Runs along the attachment of the falx to the tentorium, between the anterior Galenic junction and the confluence.', ['brain.landmark.falcotentorial'])
            if key == 'galen':
                return rule(['cisternal'], ['Corpus callosum', 'Third ventricle', 'Falx cerebri', 'Tentorium cerebelli'],
                    'Collects deep venous drainage beneath the splenium and approaches the anterior end of the straight sinus.', ['brain.landmark.callosal-splenium', 'brain.landmark.falcotentorial'])
            if key == 'inferior_sagittal':
                return rule(['dural-free-edge'], ['Falx cerebri', 'Corpus callosum'],
                    'Follows the free inferior edge of the falx and joins the anterior straight sinus.', ['brain.landmark.falx-inferior', 'brain.landmark.falcotentorial'])
            if key in ['superior_sagittal', 'confluence', 'transverse', 'sigmoid', 'superior_petrosal', 'inferior_petrosal', 'occipital', 'marginal']:
                names = ['Falx cerebri'] if key == 'superior_sagittal' else ['Tentorium cerebelli'] if key in ['confluence', 'transverse', 'superior_petrosal'] else []
                return rule(['dural-attachment', 'bony-groove'], names,
                    'Follows its named dural attachment or skull groove, retaining tributary and outlet connections.')
            if key == 'internal_cerebral':
                return rule(['deep-venous', 'cisternal'], ['Third ventricle', 'Fornix', 'Thalamus', 'Choroid plexus', 'Corpus callosum'],
                    'Courses through the roof region of the third ventricle and converges posteriorly towards Galen.', ['brain.landmark.fornix.{side}', 'brain.landmark.third-ventricle-roof', 'brain.landmark.callosal-splenium'])
            if key == 'basal':
                return rule(['cisternal'], ['Hypothalamus', 'Base of peduncle', 'Midbrain', 'Thalamus', 'Hippocampus'],
                    'Courses through basal and perimesencephalic cisternal regions towards its retained deep venous outlet.', ['brain.landmark.hypothalamic', 'brain.landmark.cerebral-peduncle.{side}', 'brain.landmark.thalamic-posterior.{side}'])
            if key in ['thalamostriate', 'anterior_septal', 'superior_choroidal']:
                names = {'thalamostriate':['Caudate nucleus', 'Thalamus', 'Lateral ventricle'], 'anterior_septal':['Septum pellucidum', 'Fornix', 'Lateral ventricle'], 'superior_choroidal':['Choroid plexus', 'Lateral ventricle']}[key]
                return rule(['subependymal'], names, 'Follows the appropriate ventricular-wall or choroidal relationship and joins its existing internal cerebral collector.')
            if key in ['anterior_cerebral', 'deep_middle_cerebral', 'anterior_communicating', 'posterior_communicating']:
                return rule(['cisternal'], ['Hypothalamus', 'Base of peduncle', 'Insula (Subcentral gyrus and ant. and post. sulci*)'],
                    'Follows its basal or deep Sylvian cisternal course while preserving the modelled communicating connections.')
            if key in ['superficial_middle_cerebral', 'trolard', 'labbe', 'frontal_cortical', 'parietal_cortical']:
                names = ['Lat_Fis-post'] if key == 'superficial_middle_cerebral' else ['Precentral gyrus', 'Postcentral gyrus'] if key in ['trolard', 'parietal_cortical'] else ['Superior temporal gyrus', 'Middle temporal gyrus'] if key == 'labbe' else ['Superior frontal gyrus', 'Middle frontal gyrus']
                return rule(['pial', 'bridging'], names, 'Runs on the relevant cortical surface or fissure before bridging to its existing venous collector.')
            if key in ['anterior_pontomesencephalic', 'anterior_pontine', 'anterior_medullary', 'lateral_mesencephalic', 'transverse_pontine', 'pontomedullary']:
                name = 'Midbrain' if key in ['anterior_pontomesencephalic', 'lateral_mesencephalic'] else 'Medulla oblongata' if key == 'anterior_medullary' else 'Pons'
                stations = {'anterior_pontomesencephalic':['brain.landmark.pontomesencephalic.{side}'],
                    'anterior_pontine':['brain.landmark.pontomesencephalic.left', 'brain.landmark.anterior-pons', 'brain.landmark.pontomedullary.left'],
                    'anterior_medullary':['brain.landmark.anterior-medulla'],
                    'lateral_mesencephalic':['brain.landmark.lateral-midbrain.{side}'],
                    'transverse_pontine':['brain.landmark.lateral-pons.left', 'brain.landmark.anterior-pons', 'brain.landmark.lateral-pons.right'],
                    'pontomedullary':['brain.landmark.pontomedullary.left', 'brain.landmark.pontomedullary.right']}[key]
                return rule(['surface-vein', 'bridging'], [name],
                    'Follows the named exposed brainstem surface or transverse groove; any bridging outlet is fitted separately.', stations)
            if key == 'precentral_cerebellar':
                return rule(['cisternal', 'surface-vein'], ['Lingula of cerebellum', 'Superior cerebellar peduncle', 'Fourth ventricle', 'Midbrain'],
                    'Courses behind the brainstem in the precentral cerebellar cisternal region, approaching the superior vermian or Galenic outlet.', ['brain.landmark.precentral-cerebellar', 'brain.landmark.callosal-splenium'])
            if key in ['superior_vermian', 'inferior_vermian', 'inferior_hemispheric', 'superior_petrosal_vein', 'cerebellopontine_fissure']:
                names = ['Culmen', 'Declive', 'Lingula of cerebellum'] if key == 'superior_vermian' else ['Pyramis of vermis', 'Uvula of vermis', 'Tonsil of cerebellum'] if key == 'inferior_vermian' else ['Inferior semilunar lobule', 'Biventral lobule'] if key == 'inferior_hemispheric' else ['Pons', 'Flocculus', 'Wing of central lobule']
                return rule(['surface-vein', 'bridging'], names, 'Follows the appropriate vermian, hemispheric or petrosal surface and then its retained bridging drainage route.')
            if key == 'anterior_spinal':
                return rule(['surface-vein'], ['Medulla oblongata'], 'Continues along the ventral medullary and spinal venous axis.', missing=['Cervical spinal cord surface'])
            return None
        if key.startswith('artery.connection.'):
            return None
        if not key.startswith(('artery.anterior.', 'artery.posterior.', 'artery.amendment.')):
            return None
        if key.endswith(('anterior_communicating', 'posterior_communicating')):
            return rule(['cisternal'], ['Optic chiasm', 'Hypothalamus', 'Base of peduncle'],
                'Follows its basal cisternal communicating course, preserving branch ostia and both retained parent connections.')
        if any(x in key for x in ['ophthalmic', 'retinal', 'ciliary', 'ethmoidal', 'lacrimal', 'supraorbital', 'supratrochlear', 'dorsal_nasal', 'labyrinthine', 'meningeal', 'hypophyseal', 'vidian', 'ilt_', 'caroticotympanic', 'subarcuate', 'wollschlaeger', 'davidoff', 'marginal']):
            return None
        if 'internal_carotid' in key:
            if key.endswith(('.cervical', '.petrous', '.cavernous')): return None
            return rule(['cisternal'], ['Optic chiasm', 'Optic tract', 'Hypothalamus'], 'Follows the retained supraclinoid approach and branch ostia within the basal cisternal region.')
        if any(x in key for x in ['perforat', 'lenticulostriate', 'heubner', 'thalamogeniculate', 'tuberothalamic']):
            names = ['Caudate nucleus', 'Putamen', 'Globus pallidus'] if any(x in key for x in ['lenticulostriate', 'heubner']) else ['Thalamus', 'Hypothalamus', 'Midbrain', 'Pons', 'Medulla oblongata']
            return rule(['cisternal', 'penetrating'], names, 'Leaves its parent in the cisternal space, then enters tissue through an individually reviewed entry site.', missing=['Reviewed perforator entry sites and intraparenchymal course boundaries'])
        if 'choroidal' in key:
            return rule(['cisternal', 'choroidal'], ['Optic tract', 'Hippocampus', 'Thalamus', 'Choroid plexus', 'Lateral ventricle'], 'Follows its named cisternal approach before reaching the appropriate choroidal or ventricular region.', missing=['Reviewed choroidal fissure entry and plexal attachment'])
        if key.endswith('central') and not key.endswith('precentral'):
            return rule(['cisternal', 'opercular', 'sulcal'], ['Lat_Fis-post', 'Precentral gyrus', 'Postcentral gyrus', 'Central sulcus'],
                'Approaches through the Sylvian and opercular region, then follows the central sulcus between the precentral and postcentral gyri.', ['brain.landmark.central-sulcus.{side}'])
        if 'mca_m1' in key:
            return rule(['cisternal'], ['Circular sulcus of insula', 'Insula (Subcentral gyrus and ant. and post. sulci*)'], 'Courses laterally through the Sylvian cisternal region, retaining its bifurcation and perforator origins.')
        if 'mca_' in key and 'division' in key:
            return rule(['insular', 'opercular', 'pial'], ['Circular sulcus of insula', 'Lat_Fis-post', 'Insula (Subcentral gyrus and ant. and post. sulci*)'], 'Courses over the insular region and through the opercular approach to its cortical branches.')
        if any(x in key for x in ['aca_', 'internal_frontal', 'callosomarginal', 'paracentral', 'precuneal', 'internal_parietal']):
            if 'aca_a1' in key:
                return rule(['cisternal'], ['Optic chiasm', 'Hypothalamus'], 'Courses medially through the basal cisternal region towards the anterior communicating complex.')
            names = ['Corpus callosum'] if 'pericallosal' in key else ['Cingulate gyrus and sulcus (Middle anterior part)', 'Cingulate gyrus and sulcus (Middle posterior part)'] if 'callosomarginal' in key else ['Paracentral gyrus and sulcus*'] if 'paracentral' in key else ['Superior frontal gyrus', 'Precuneus', 'Corpus callosum']
            return rule(['sulcal', 'pial'], names, 'Follows its medial cerebral sulcal or pial course, preserving the named callosal, cingulate or cortical relationship.')
        if any(x in key for x in ['pca_', 'parieto_occipital_cuneal']):
            if 'pca_p1' in key or 'pca_p2_p3' in key:
                return rule(['cisternal'], ['Base of peduncle', 'Midbrain', 'Thalamus'], 'Courses around the cerebral peduncle through the perimesencephalic cisternal region.')
            names = ['Calcarine sulcus'] if 'calcarine' in key else ['Parieto-occipital sulcus'] if 'parieto_occipital' in key else ['Corpus callosum'] if 'splenial' in key else ['Hippocampus'] if 'hippocampal' in key else ['Inferior temporal gyrus', 'Lingual gyrus', 'Cuneus']
            return rule(['cisternal', 'sulcal', 'pial'], names, 'Follows the named posterior cerebral cortical or medial temporal course after its cisternal approach.')
        if any(x in key for x in ['sca', 'aica', 'pica']):
            names = ['Tonsil of cerebellum', 'Medulla oblongata', 'Uvula of vermis', 'Inferior semilunar lobule'] if 'pica' in key else ['Pons', 'Flocculus', 'Wing of central lobule'] if 'aica' in key else ['Midbrain', 'Superior cerebellar peduncle', 'Culmen', 'Superior semilunar lobule']
            return rule(['cisternal', 'pial'], names, 'Follows its brainstem cisternal approach and named cerebellar surface distribution, preserving the existing branches.')
        if 'basilar' in key or key.endswith('.v4') or 'anterior_spinal' in key or 'circumflex' in key or 'collicular' in key or 'tectal' in key:
            return rule(['cisternal', 'pial'], ['Pons', 'Medulla oblongata', 'Midbrain', 'Superior colliculus'], 'Follows the appropriate ventral or circumferential brainstem course and existing branch attachments.')
        if key.startswith('artery.anterior.') and not any(x in key for x in ['common_carotid', 'carotid_external']):
            names = ['Precentral gyrus'] if 'precentral' in key else ['Postcentral gyrus', 'Superior parietal lobule'] if 'parietal' in key else ['Middle temporal gyrus', 'Superior temporal gyrus'] if any(x in key for x in ['temporal', 'angular', 'occipital']) else ['Middle frontal gyrus', 'Inferior frontal gyrus']
            return rule(['opercular', 'sulcal', 'pial'], names, 'Follows its opercular approach and named cortical distribution while retaining the parent and distal rami.')
        return None

    asset_files = {r['asset']['file'] for r in manifest['structures'] if r.get('asset') and r['system'] in ['artery', 'vein']}
    asset_hashes = {file: hashlib.sha256((PUB / file).read_bytes()).hexdigest() for file in asset_files}
    courses = []
    for row in manifest['structures']:
        if row['system'] not in ['artery', 'vein'] or not row.get('asset'):
            continue
        identifier = row['id']
        # Distal rami inherit the regional route of their named parent; keep
        # their individual geometry, attachment graph and rule record.
        root = row
        ancestry = set()
        while any(k in root['id'] for k in ['_cortical_branch', '_distal_ramus']) and root.get('parent') in rows and root['id'] not in ancestry:
            ancestry.add(root['id'])
            root = rows[root['parent']]
        selected_rule = classify(root['id'])
        side = row['side']
        outgoing = [r for r in manifest['relationships'] if r['from'] == identifier and r['type'] in ['drains_to', 'branches_to']]
        incoming = [r for r in manifest['relationships'] if r['to'] == identifier and r['type'] in ['drains_to', 'branches_to']]
        attachments = {'parentId': row.get('parent'), 'incoming': incoming, 'outgoing': outgoing,
                       'status': 'catalogue-relationships-not-yet-verified-as-physical-junctions'}
        scope = 'intracranial' if selected_rule else 'potential-anastomosis' if row.get('displayGroup') == 'anastomoses' else 'protected-baseline'
        spec = {'vesselId': identifier, 'side': side, 'scope': scope, 'geometry': row['asset'],
                'geometrySha256': asset_hashes[row['asset']['file']],
                'registrationId': manifest['brainRegistration']['id'],
                'brainAssetSha256': manifest['brainRegistration']['registeredAssetSha256'],
                'attachments': attachments, 'radiusPolicy': 'preserve-delivered-profile',
                'reviewStatus': 'requires-anatomical-review' if selected_rule else 'protected-baseline',
                'segments': [], 'missingTargets': []}
        if selected_rule:
            modes, names, summary, explicit, missing = selected_rule
            available, absent = [], []
            for name in names:
                matches = [t['id'] for t in targets if (t['anatomy']['sourceLabel'].removesuffix('.l').removesuffix('.r') == name
                           or t['anatomy']['sourceLabel'].removesuffix('.l').removesuffix('.r').startswith(name + ' (')
                           or (name == 'Inferior frontal gyrus' and 'part of inferior frontal gyrus' in ' '.join(t['anatomy']['sourceLabel'].lower().split())))
                           and (side == 'midline' or t['side'] in [side, 'midline'])]
                available.extend(matches)
                if not matches: absent.append(name)
            station_ids = []
            for ref in explicit:
                ref = ref.replace('{side}', side if side != 'midline' else 'left')
                if ref in rows:
                    refs = rows[ref].get('vesselGuide', {}).get('anchorIds', [ref])
                    station_ids.extend(refs[:1] if ref == 'brain.landmark.falcotentorial' and identifier != 'vein.straight' else refs)
            if not station_ids:
                station_ids = [g['id'] for g in guides if identifier in g['vesselGuide']['vesselIds'] and g.get('surfaceAnchor')]
            spec.update(summary=summary, targetStructureIds=list(dict.fromkeys(available)),
                stationIds=list(dict.fromkeys(station_ids)), stationOrder='anatomical-sequence' if explicit else 'regional-references-only',
                missingTargets=list(missing) + absent,
                segments=[{'order': i, 'mode': mode, 'targetStructureIds': list(dict.fromkeys(available)),
                    'stationIds': list(dict.fromkeys(station_ids)), 'stationRole': 'whole-course-reference',
                    'constraints': {'wallClearance': 'radius-aware', 'allowTissueEntry': mode == 'penetrating',
                                    'avoidAtlasCutFaces': True, 'preserveJoinedAttachments': True},
                    'reviewStatus': 'requires-individual-segment-boundaries'} for i, mode in enumerate(modes)])
            if spec['missingTargets']: spec['reviewStatus'] = 'requires-anatomical-target'
        else:
            spec.update(summary='Retain the existing bony, orbital or extracranial course and connections during brain fitting.',
                        targetStructureIds=[], stationIds=[], stationOrder='not-applicable')
        row['vesselCourse'] = spec
        courses.append(spec)
    manifest['vesselCourseSchemaVersion'] = '1.0'
    manifest['vesselCourseState'] = 'specified-not-fitted'
    write(APP / 'anatomy/generated/complete_manifest.json', manifest)
    write(PUB / 'vessel-courses.json', {'schemaVersion': '1.0', 'coordinateSystem': 'RAS', 'units': 'mm',
        'brainRegistration': manifest['brainRegistration'], 'state': 'specified-not-fitted',
        'segmentBoundaryPolicy': 'Modes are ordered anatomical phases; individual geometric start/end stations require review before fitting.',
        'brainAdjustmentPolicy': manifest['brainAdjustmentPolicy'], 'courses': courses})
    print(json.dumps({'vascularLabels': len(courses), 'intracranialSpecifications': sum(c['scope']=='intracranial' for c in courses),
                      'targetGaps': sum(c['reviewStatus']=='requires-anatomical-target' for c in courses)}))

if __name__ == '__main__':
    main()
