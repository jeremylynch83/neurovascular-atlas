"""Independent combined review, including basilar anterior-wall exclusion."""
import argparse,json
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from fit_vessels import APP,curve_from_mesh
from build_targets import poly
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha
from verify_fitting import collisions,inside,distances,stats
from verify_central_rebuild import self_contacts,outside_join_contacts,material_section

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-family27');p.add_argument('--brain-directory',default='.authoring/posterior-context27');a=p.parse_args()
    w=APP/a.directory
    brains=[trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False),trimesh.load(w/'brain-trial.glb',process=False)]
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    scenes={kind:[trimesh.load(w/f'{kind}-source.glb',process=False),trimesh.load(w/f'{kind}-trial.glb',process=False)] for kind in ['veins','arteries']}
    report={'brainSha256':sha(w/'brain-trial.glb'),'veinsSha256':sha(w/'veins-trial.glb'),'arteriesSha256':sha(w/'arteries-trial.glb'),'geometry':[],'contacts':[],'containment':[],'joins':[],'sections':[],'anteriorSurface':[],'lateralGaps':[],'failures':[],'appliedToApp':False}
    def save(): (w/'combined-progress.json').write_text(json.dumps(report,indent=2)+'\n')
    stem=[trimesh.util.concatenate([m for k,m in b.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]) for b in brains]
    locs=[]
    for m in stem:
        l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(m));l.BuildLocator();locs.append(l)
    for kind,ss in scenes.items():
        changed=[]
        for key,old in ss[0].geometry.items():
            new=ss[1].geometry[key]
            assert np.array_equal(old.faces,new.faces)
            if np.array_equal(old.vertices,new.vertices) and key!='Basilar':continue
            changed.append(key);robust=old.area_faces>1e-6;ratios=new.area_faces[robust]/old.area_faces[robust]
            self_count=[self_contacts(m) for m in [old,new]]
            report['geometry'].append([kind,key,float(ratios.min()),*self_count])
            if ratios.min()<.12:report['failures'].append([kind,key,'collapsed-wall',float(ratios.min())])
            if self_count[1]>self_count[0]:report['failures'].append([kind,key,'self',*self_count])
            primary=(kind=='veins' and key in set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal'])) or key=='Basilar'
            for domain,target_scene in [('tissue',brains[1]),('bone',bones)]:
                for tk,m in target_scene.geometry.items():
                    if domain=='tissue' and any(t in tk for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
                    before=brains[0].geometry[tk] if domain=='tissue' else m
                    counts=[collisions(old,before),collisions(new,m)]
                    if any(counts):report['contacts'].append([kind,key,domain,tk,*counts])
                    if counts[1]>counts[0]:report['failures'].append([kind,key,domain,tk,*counts])
                    if primary and domain=='tissue' and counts[1] and any(t in tk for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):report['failures'].append([kind,key,'primary-wall-crosses-stem',tk,counts[1]])
                    if domain=='tissue' and m.is_watertight and np.all(new.bounds[1]>=m.bounds[0]) and np.all(new.bounds[0]<=m.bounds[1]):
                        count=[int(inside(old.vertices,before).sum()) if before.is_watertight else None,int(inside(new.vertices,m).sum())]
                        report['containment'].append([kind,key,tk,*count])
                        if count[0] is not None and count[1]>count[0]:report['failures'].append([kind,key,'increased-tissue-containment',tk,*count])
                        if primary and count[1] and any(t in tk for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle']):report['failures'].append([kind,key,'primary-wall-inside-stem',tk,count[1]])
            if key in ANTERIOR or key=='Basilar':
                rows=[]
                for mesh,l in zip([old,new],locs):
                    values=[]
                    for pt in mesh.vertices:
                        t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
                        if l.IntersectWithLine([pt[0],5,pt[2]],[pt[0],-145,pt[2]],1e-8,t,q,pc,sub,cell):values.append(pt[1]-q[1])
                    values=np.array(values);rows.append({'sampledWallVertices':len(values),'wallVerticesBehindAnteriorStemSurface':int((values<-.05).sum()),'minimumSignedClearanceMm':float(values.min()),'medianSignedClearanceMm':float(np.median(values))})
                report['anteriorSurface'].append({'node':key,'before':rows[0],'after':rows[1]})
                if rows[1]['wallVerticesBehindAnteriorStemSurface']:report['failures'].append([kind,key,'wall-behind-exposed-stem-surface',rows[1]['wallVerticesBehindAnteriorStemSurface']])
            if key in LATERAL:
                c0=curve_from_mesh(old,axis=2,n=100);c1=curve_from_mesh(new,axis=2,n=100)
                report['lateralGaps'].append({'node':key,'before':stats(distances(c0[15:85],stem[0])),'after':stats(distances(c1[15:85],stem[1]))})
            if primary:
                axis=0 if key in TRANSVERSE else 2;c=curve_from_mesh(old,axis=axis,n=80);ratio=[]
                for j in range(8,72,4):
                    areas,_=material_section(old,new,c[j],c[j+1]-c[j-1],radius=5. if key=='Basilar' else 1.5);ratio.append(areas[1]/areas[0])
                row=[kind,key,float(min(ratio)),float(np.median(ratio)),float(max(ratio))];report['sections'].append(row)
                if min(ratio)<.5 or max(ratio)>2:report['failures'].append([kind,key,'section-distortion',*row[2:]])
            print('Combined wall checked',kind,key,flush=True);save()
        # Boundary equality is checked across every label of each asset.
        pp=np.concatenate([m.vertices for m in ss[0].geometry.values()]);qq=np.concatenate([m.vertices for m in ss[1].geometry.values()])
        _,inverse=np.unique(np.round(pp,5),axis=0,return_inverse=True);order=np.argsort(inverse);same=np.diff(inverse[order])==0
        gap=float(np.linalg.norm(np.diff(qq[order],axis=0)[same],axis=1).max(initial=0));report[f'{kind}MaximumSharedBoundaryGapMm']=gap
        if gap>2e-4:report['failures'].append([kind,'opened-boundary',gap])
        for k in changed:
            for other in ss[1].geometry:
                if k==other or (other in changed and other<k):continue
                counts=[outside_join_contacts(s.geometry[k],s.geometry[other],ss[0].geometry[k],ss[0].geometry[other]) for s in ss]
                if any(counts):report['joins'].append([kind,k,other,*counts])
                if counts[1]>counts[0]:report['failures'].append([kind,k,'outside-join',other,*counts])
        save()
    for k in [r[1] for r in report['geometry'] if r[0]=='arteries']:
        for other,m in scenes['veins'][1].geometry.items():
            counts=[collisions(scenes['arteries'][i].geometry[k],scenes['veins'][i].geometry[other]) for i in [0,1]]
            if any(counts):report['contacts'].append(['artery-vein',k,other,*counts])
            if counts[1]>counts[0]:report['failures'].append(['artery-vein',k,other,*counts])
    report['passed']=not report['failures'];report['limitations']=['Open atlas cut surfaces require visual anatomical review.','Perforator entry and all brain-to-brain interfaces require separate anatomical acceptance.','No production asset is changed by this check.']
    (w/'combined-acceptance.json').write_text(json.dumps(report,indent=2)+'\n');print('Combined passed',report['passed'],'failures',len(report['failures']),flush=True)

if __name__=='__main__':main()
