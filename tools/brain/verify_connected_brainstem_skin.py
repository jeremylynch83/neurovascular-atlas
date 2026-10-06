"""Independent complete-skin checks for the resumed connected venous trial."""
import json
import argparse
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP, curve_from_mesh
from refit_connected_brainstem_skin import WORK, PRIMARY, KEYS
from reconcile_brainstem import sha
from verify_fitting import collisions, distances, inside
from verify_central_rebuild import self_contacts, outside_join_contacts, material_section

def main():
    global WORK,PRIMARY,KEYS
    parser=argparse.ArgumentParser();parser.add_argument('--section',action='store_true');parser.add_argument('--directory');args=parser.parse_args()
    if args.section:
        from refit_brainstem_sections import W,KEYS as section_keys
        if args.directory:W=APP/args.directory
        WORK=W;PRIMARY=section_keys;KEYS=section_keys
        solver=json.loads((WORK/'solver.json').read_text())
        assert solver['success'], 'No successful current solver output'
        assert solver['brainSha256']==sha(WORK/'brain-trial.glb')
        assert solver['sourceSha256']==sha(WORK/'veins-source.glb')
        assert solver['candidateSha256']==sha(WORK/'veins-trial.glb')
    before = trimesh.load(WORK/'veins-source.glb',process=False)
    after = trimesh.load(WORK/'veins-trial.glb',process=False)
    brain_path = WORK/'brain-trial.glb' if (WORK/'brain-trial.glb').exists() else APP/'public/anatomy/models/brain-context.glb'
    brain = trimesh.load(brain_path,process=False)
    bone = trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    report = {'candidateSha256':sha(WORK/'veins-trial.glb'),
              'sourceSha256':sha(WORK/'veins-source.glb'),
              'brainSha256':sha(brain_path),
              'geometry':[], 'tissue':[], 'containment':[], 'bone':[], 'joins':[], 'sections':[],
              'failures':[], 'appliedToApp':False}
    changed=[]
    for key in after.geometry:
        a,b=before.geometry[key],after.geometry[key]
        assert np.array_equal(a.faces,b.faces)
        if np.array_equal(a.vertices,b.vertices):continue
        changed.append(key)
        robust=a.area_faces>5e-5
        ratio=b.area_faces[robust]/a.area_faces[robust]
        counts=[self_contacts(m) for m in [a,b]]
        report['geometry'].append({'node':key,'minimumAreaRatio':float(ratio.min()),
                                  'medianAreaRatio':float(np.median(ratio)),
                                  'selfContacts':counts})
        if counts[1]>counts[0]:report['failures'].append([key,'self',*counts])
        if ratio.min()<.12:report['failures'].append([key,'collapsed-wall',float(ratio.min())])
        for target,m in brain.geometry.items():
            if any(t in target for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
            counts=[collisions(w,m) for w in [a,b]]
            if any(counts):report['tissue'].append([key,target,*counts])
            if counts[1]>counts[0]:report['failures'].append([key,target,*counts])
            if key in PRIMARY and counts[1] and any(t in target for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):
                report['failures'].append([key,'primary-wall-remains-in-brainstem',target,counts[1]])
            # A tube can sit wholly inside a closed tissue label without
            # intersecting its surface. Triangle contacts alone miss this.
            if m.is_watertight and np.all(b.bounds[1]>=m.bounds[0]) and np.all(b.bounds[0]<=m.bounds[1]):
                contained=[int(inside(w.vertices,m).sum()) for w in [a,b]]
                report['containment'].append([key,target,*contained])
                if contained[1]>contained[0]:report['failures'].append([key,'increased-closed-tissue-containment',target,*contained])
                if key in PRIMARY and contained[1] and any(t in target for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):
                    report['failures'].append([key,'primary-wall-inside-closed-brainstem',target,contained[1]])
        for target,m in bone.geometry.items():
            counts=[collisions(w,m) for w in [a,b]]
            if any(counts):report['bone'].append([key,target,*counts])
            if counts[1]>counts[0]:report['failures'].append([key,target,*counts])
        print('Checked complete wall',key,flush=True)
        (WORK/'acceptance-progress.json').write_text(json.dumps(report,indent=2)+'\n')
    for i,key in enumerate(changed):
        for other in after.geometry:
            if other==key or (other in changed and other<key):continue
            counts=[outside_join_contacts(s.geometry[key],s.geometry[other],
                                         before.geometry[key],before.geometry[other])
                    for s in [before,after]]
            if any(counts):report['joins'].append([key,other,*counts])
            if counts[1]>counts[0]:report['failures'].append([key,'outside-join',other,*counts])
        print('Checked joins',key,flush=True)
    p=np.concatenate([m.vertices for m in before.geometry.values()])
    q=np.concatenate([m.vertices for m in after.geometry.values()])
    _,inv=np.unique(np.round(p,5),axis=0,return_inverse=True)
    order=np.argsort(inv);same=np.diff(inv[order])==0
    gaps=np.linalg.norm(np.diff(q[order],axis=0)[same],axis=1)
    report['maximumSharedBoundaryGapMm']=float(gaps.max(initial=0))
    if gaps.max(initial=0)>2e-4:report['failures'].append(['opened-shared-boundary',float(gaps.max())])
    for key in sorted(PRIMARY):
        axis=0 if ('transverse' in key or 'pontomedullary.' in key or key=='vein.posterior_communicating') else 2
        curve=curve_from_mesh(before.geometry[key],axis=axis,n=80)
        ratios=[];warps=[]
        for j in range(8,72,3):
            tangent=curve[min(j+1,79)]-curve[max(j-1,0)]
            areas,w=material_section(before.geometry[key],after.geometry[key],curve[j],tangent)
            ratios.append(areas[1]/areas[0]);warps.append(w[1])
        row={'node':key,'minimumSkinSectionAreaRatio':float(min(ratios)),
             'medianSkinSectionAreaRatio':float(np.median(ratios)),
             'maximumSkinSectionAreaRatio':float(max(ratios)),
             'maximumSectionWarpMm':float(max(warps))}
        report['sections'].append(row)
        if min(ratios)<.5 or max(ratios)>2:report['failures'].append([key,'section-distortion',row])
    report['passed']=not report['failures']
    report['limitations']=['Triangle contacts do not prove exclusion from open atlas cut surfaces.',
                          'Skin envelope sections are not a separately segmented vessel lumen.',
                          'Composite atlas anatomy requires visual anatomical review.']
    (WORK/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'failures':report['failures']},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':main()
