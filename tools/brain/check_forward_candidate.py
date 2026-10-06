"""Check the incremental forward/pontine edit against its review parent.

This is a focused comparison, not full anatomical acceptance of the parent.
"""
import argparse,json
import numpy as np,trimesh,vtk
from fit_vessels import APP,curve_from_mesh
from build_targets import poly
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha
from verify_fitting import collisions,distances,stats,inside

def locator(m):
    l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(m));l.BuildLocator();return l

def anterior_values(m,loc):
    values=[]
    for pt in m.vertices:
        t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
        if loc.IntersectWithLine([pt[0],5,pt[2]],[pt[0],-145,pt[2]],1e-8,t,q,pc,sub,cell):values.append(pt[1]-q[1])
    v=np.array(values);return {'sampledWallVertices':len(v),'wallVerticesBehindAnteriorSurface':int((v<-.05).sum()),'minimumMm':float(v.min()),'medianMm':float(np.median(v))}

def gap(o,n):
    pp=np.concatenate([m.vertices for m in o.geometry.values()]);qq=np.concatenate([n.geometry[k].vertices for k in o.geometry])
    _,inv=np.unique(np.round(pp,5),axis=0,return_inverse=True);ix=np.argsort(inv);same=np.diff(inv[ix])==0
    return float(np.linalg.norm(np.diff(qq[ix],axis=0)[same],axis=1).max(initial=0))

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-forward41');a=p.parse_args();w=APP/a.directory
    ss={k:[trimesh.load(w/f'{k}-{s}.glb',process=False) for s in ['source','trial']] for k in ['brain','arteries','veins']}
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    brain=ss['brain'];stems=[trimesh.util.concatenate([m for k,m in b.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]) for b in brain]
    locs=[locator(m) for m in stems]
    report={'scope':'incremental forward-shift check against candidate40, not full anatomical acceptance','hashes':{k:sha(w/f'{k}-trial.glb') for k in ss},'appliedToApp':False,'accepted':False,'geometry':[],'boneContacts':[],'anteriorSurface':[],'lateralGaps':[],'failures':[]}
    def save(): (w/'forward-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    for kind,(o,n) in ss.items():
        boundary=gap(o,n);report[kind+'MaximumSharedMaterialPointGapMm']=boundary
        if boundary>2e-4:report['failures'].append([kind,'opened-existing-boundary',boundary])
        for key,old in o.geometry.items():
            new=n.geometry[key];assert np.array_equal(old.faces,new.faces)
            if np.array_equal(old.vertices,new.vertices):continue
            robust=old.area_faces>5e-5;ratio=new.area_faces[robust]/old.area_faces[robust];r=float(ratio.min())
            report['geometry'].append([kind,key,r]);
            if r<.25:report['failures'].append([kind,key,'incremental-facet-distortion',r])
            for bk,b in bones.geometry.items():
                if bk not in ['bone.occipital','bone.sphenoid','bone.temporal.right','bone.temporal.left']:continue
                counts=[collisions(old,b),collisions(new,b)]
                if any(counts):report['boneContacts'].append([kind,key,bk,*counts])
                if counts[1]>counts[0]:report['failures'].append([kind,key,'increased-bone-contacts',bk,*counts])
            if key=='Basilar' or key in ANTERIOR:
                values=[anterior_values(m,l) for m,l in zip([old,new],locs)];report['anteriorSurface'].append({'node':key,'before':values[0],'after':values[1]})
                if values[1]['wallVerticesBehindAnteriorSurface']>values[0]['wallVerticesBehindAnteriorSurface']:report['failures'].append([kind,key,'increased-anterior-wall-penetration',values])
            if key in LATERAL:
                cs=[curve_from_mesh(m,axis=2,n=100)[15:85] for m in [old,new]]
                report['lateralGaps'].append({'node':key,'before':stats(distances(cs[0],stems[0])),'after':stats(distances(cs[1],stems[1]))})
        print(kind,'geometry / bone checks completed',flush=True);save()
    plex=ss['veins'][1].geometry['vein.basilar_plexus'];assert np.array_equal(plex.vertices,ss['veins'][0].geometry['vein.basilar_plexus'].vertices)
    report['basilarPlexusRetainedExactly']=True;report['basilarClearance']=[]
    wholebone=trimesh.util.concatenate(list(bones.geometry.values()))
    for i in [0,1]:
        ba=ss['arteries'][i].geometry['Basilar'];contacts=collisions(ba,stems[i]);pc=collisions(ba,plex)
        row={'state':['parent','candidate'][i],'brainstemTriangleContacts':contacts,'plexusTriangleContacts':pc,'boneWallDistance':stats(distances(ba.vertices,wholebone)),'plexusWallDistance':stats(distances(ba.vertices,plex))};report['basilarClearance'].append(row)
        if i and contacts:report['failures'].append(['Basilar','brainstem-contacts',contacts])
        if i and pc>report['basilarClearance'][0]['plexusTriangleContacts']:report['failures'].append(['Basilar','increased-plexus-contacts',pc])
        # Open atlas label cuts are unsuitable for individual containment.
        # Weld the two sides before checking whether the complete skin closes.
        welded=stems[i].copy();welded.merge_vertices();row['completeStemClosed']=bool(welded.is_watertight)
        if welded.is_watertight:
            row['basilarWallVerticesInsideStem']=int(inside(ba.vertices,welded).sum())
            if i and row['basilarWallVerticesInsideStem']:report['failures'].append(['Basilar','inside-stem',row['basilarWallVerticesInsideStem']])
    report['pontineProfiles']=[]
    for z in [50,55,60,65]:
        vals=[]
        for i in [0,1]:
            m=trimesh.util.concatenate([m for k,m in brain[i].geometry.items() if 'pons.' in k]);l=locator(m);pts=vtk.vtkPoints();ids=vtk.vtkIdList();l.IntersectWithLine([.8,-145,z],[.8,-30,z],1e-8,pts,ids);ys=[pts.GetPoint(j)[1] for j in range(pts.GetNumberOfPoints())]
            vals.append({'backY':min(ys),'frontY':max(ys),'APThicknessMm':max(ys)-min(ys)})
        report['pontineProfiles'].append({'zMm':z,'before':vals[0],'after':vals[1]})
    report['incrementalChecksPassed']=not report['failures'];report['limitations']=['Parent candidate40 remains unaccepted with existing vessel joins and tissue-shape issues.','The focused checks do not establish complete brain self-intersection, all arterial perforator entries or full surrounding anatomy acceptance.','Coincident material point checks do not establish continuous attachment across every cut surface.']
    save();print('incremental checks',report['incrementalChecksPassed'],'failures',report['failures'],flush=True)

if __name__=='__main__':main()
