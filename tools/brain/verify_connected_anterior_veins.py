"""Whole-wall acceptance gate for the connected anterior venous candidate."""
import argparse, json, itertools
import numpy as np, trimesh
from fit_vessels import APP, read_glb, mesh_records, accessor, curve_from_mesh
from reconcile_brainstem import sha, ANTERIOR
from verify_fitting import collisions
from verify_central_rebuild import self_contacts, outside_join_contacts, material_section
W=APP/'.authoring/connected-anterior20'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--arteries',action='store_true');args=parser.parse_args()
    path=W/'veins-trial.glb';source=APP/'.authoring/brainstem19/veins-baseline.glb'
    od,ob=read_glb(source);nd,nb=read_glb(path);oldr,newr=mesh_records(od,ob),mesh_records(nd,nb)
    old={k:trimesh.Trimesh(r['positions'],r['faces'],process=False) for k,r in oldr.items()}
    new={k:trimesh.Trimesh(r['positions'],r['faces'],process=False) for k,r in newr.items()}
    changed=[k for k in old if not np.array_equal(old[k].vertices,new[k].vertices)]
    report={'sourceSha256':sha(source),'candidateSha256':sha(path),'brainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),'changedLabels':changed,'geometry':[],'tissue':[],'bone':[],'self':[],'veinNeighbours':[],'arteries':[],'sections':[],'failures':[],'arterialChecksCompleted':args.arteries}
    def require(ok,message):
        if not ok:report['failures'].append(message)
    require(set(old)==set(new),'Changed label inventory')
    p=np.concatenate([old[k].vertices for k in old]);q=np.concatenate([new[k].vertices for k in old]);_,inverse=np.unique(np.round(p,5),axis=0,return_inverse=True);order=np.argsort(inverse);same=np.diff(inverse[order])==0;gap=np.linalg.norm(np.diff(q[order],axis=0)[same],axis=1)
    report['maximumSharedBoundaryGapMm']=float(gap.max(initial=0));require(gap.max(initial=0)<2e-4,'Opened labelled join')
    brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    for k in old:
        require(np.array_equal(old[k].faces,new[k].faces),k+': triangle indices changed')
        if k not in changed:
            require(np.array_equal(accessor(od,ob,oldr[k]['primitive']['attributes']['NORMAL']),accessor(nd,nb,newr[k]['primitive']['attributes']['NORMAL'])),k+': retained normal changed');continue
        a,b=old[k],new[k];ratio=b.area_faces/np.maximum(a.area_faces,1e-20)
        require(np.isfinite(b.vertices).all() and ratio.min()>1e-4,k+': collapsed wall')
        report['geometry'].append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(b.vertices-a.vertices,axis=1).max()),'minimumTriangleAreaRatio':float(ratio.min())})
        counts=[self_contacts(m) for m in [a,b]];report['self'].append([k,*counts]);require(counts[1]<=counts[0],k+': increased nonadjacent self contacts')
        for target,m in brain.geometry.items():
            if any(s in target for s in ['sulc','lat-fis','ventricle','aqueduct']):continue
            counts=[collisions(n,m) for n in [a,b]]
            if any(counts):report['tissue'].append([k,target,*counts])
            require(counts[1]<=counts[0],k+': increased tissue contacts '+target)
            if k in ANTERIOR and any(s in target for s in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle']):require(counts[1]==0,k+': brainstem surface not cleared '+target)
        for target,m in bones.geometry.items():
            counts=[collisions(n,m) for n in [a,b]]
            if any(counts):report['bone'].append([k,target,*counts])
            require(counts[1]<=counts[0],k+': increased bone contacts '+target)
        if k in ANTERIOR or k=='vein.anterior_spinal':
            src=curve_from_mesh(a,n=100);areas=[]
            for i in np.linspace(12,86,15).astype(int):
                pair,_=material_section(a,b,src[i],src[i+1]-src[i-1]);areas.append(pair[1]/pair[0])
            report['sections'].append({'node':k,'minimumMaterialEnvelopeAreaRatio':float(min(areas)),'medianMaterialEnvelopeAreaRatio':float(np.median(areas))});require(min(areas)>.5,k+': severe skin envelope narrowing')
        print('Wall check',k,flush=True)
    for k in changed:
        for other in old:
            if other==k or (other in changed and other<k):continue
            a=outside_join_contacts(old[k],old[other],old[k],old[other]);b=outside_join_contacts(new[k],new[other],old[k],old[other])
            if a or b:report['veinNeighbours'].append([k,other,a,b])
            require(b<=a,k+': increased outside-join venous contacts '+other)
    if args.arteries:
        arteries=trimesh.load(APP/'.authoring/brainstem19/arteries-baseline.glb',process=False)
        for k in changed:
            for target,m in arteries.geometry.items():
                counts=[collisions(n,m) for n in [old[k],new[k]]]
                if any(counts):report['arteries'].append([k,target,*counts])
                require(counts[1]<=counts[0],k+': increased retained arterial contacts '+target)
            print('Arterial neighbours',k,flush=True)
    report['passed']=not report['failures']
    report['limitations']=['Open atlas tissue surfaces do not establish complete solid containment.','Section measurements concern the skin envelope, not a separately segmented lumen.','Pre-existing contacts in uncorrected regional routes remain recorded.']
    (W/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'failures':report['failures'],'sections':report['sections']},indent=2),flush=True)
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
