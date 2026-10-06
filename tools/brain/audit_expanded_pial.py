"""Check original tissue triangle witnesses, seams, and spinal round sections."""
import json,argparse,numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from vtk.util.numpy_support import vtk_to_numpy
from fit_vessels import APP
from build_targets import poly
from verify_fitting import inside,stats
from audit_tubular_candidate import section_aspect
from rebuild_tubular_brainstem_veins import frames
from reconcile_brainstem import sha

W=APP/'.authoring/posterior-pial56'

def contact_points(m,target):
    if np.any(m.bounds[1]<target.bounds[0]) or np.any(target.bounds[1]<m.bounds[0]):return 0,np.empty((0,3))
    tri=target.triangles;lo,hi=m.bounds;keep=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
    if not keep.any():return 0,np.empty((0,3))
    tt=trimesh.Trimesh(target.vertices,target.faces[keep],process=False);test=vtk.vtkCollisionDetectionFilter();test.SetInputData(0,poly(m));test.SetInputData(1,poly(tt));test.SetTransform(0,vtk.vtkTransform());test.SetTransform(1,vtk.vtkTransform());test.SetCollisionModeToAllContacts();test.SetBoxTolerance(0);test.SetCellTolerance(0);test.Update();count=int(test.GetNumberOfContacts())
    ids=vtk_to_numpy(test.GetContactCells(0)) if count else np.array([],int)
    return count,m.triangles[np.unique(ids)].mean(1) if len(ids) else np.empty((0,3))

def main():
    global W
    parser=argparse.ArgumentParser();parser.add_argument('--directory',default='.authoring/posterior-pial56');parser.add_argument('--kind',choices=['all','arteries','veins'],default='all');args=parser.parse_args();W=APP/args.directory
    brain=trimesh.load(W/'brain-trial.glb',process=False);metadata=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text());target_keys=metadata['groups']['brain']+['brain.upper-cervical-cord'];target=trimesh.util.concatenate([brain.geometry[k] for k in target_keys]);closed=[brain.geometry[k] for k in target_keys if brain.geometry[k].is_watertight]
    report={'hashes':{k:sha(W/f'{k}-trial.glb') for k in ['brain','arteries','veins'] if (W/f'{k}-trial.glb').exists()},'rows':[],'posteriorSpinal':[],'closedTissueSurfacesForContainment':len(closed),'scope':'Original brainstem/cerebellar tissue skins and illustrative closed cord. Intentional arterial entry is reported separately. Containment is checked for all closed tissue parts; open atlas parts permit triangle-contact checks only.','accepted':False,'appliedToApp':False};seeds=[];names=[]
    if args.kind=='veins' and (W/'surface-validation.json').exists():report['rows']=[r for r in json.loads((W/'surface-validation.json').read_text())['rows'] if r['kind']=='arteries']
    for kind,groups in [('arteries',['arteries']),('veins',['veins','deep-veins'])]:
        if args.kind=='arteries' and kind=='veins':continue
        if args.kind=='veins' and kind=='arteries':
            arteries=trimesh.load(W/'arteries-trial.glb',process=False);continue
        scene=trimesh.load(W/f'{kind}-trial.glb',process=False)
        for k in sum([metadata['groups'][g] for g in groups],[]):
            entry=kind=='arteries' and any(t in k.lower() for t in ['perforator','paramedian'])
            m=scene.geometry[k];n,points=contact_points(m,target);contained=np.zeros(len(m.vertices),bool)
            for part in closed:
                mask=np.all((m.vertices>part.bounds[0])&(m.vertices<part.bounds[1]),axis=1)
                if mask.any():contained[mask]|=inside(m.vertices[mask],part)
            row={'kind':kind,'node':k,'intentionalPenetratingBranch':entry,'triangleContacts':n,'wallVerticesInsideClosedTissue':int(contained.sum())};report['rows'].append(row)
            if n and not entry:seeds.extend(points);names.extend([kind+'|'+k]*len(points));print(row,flush=True)
            (W/'surface-validation.json').write_text(json.dumps(report,indent=2)+'\n')
        if kind=='arteries':arteries=scene
    for row in json.loads((W/'posterior-spinal-courses.json').read_text()):
        side=row['side'];m=arteries.geometry['Posterior spinal '+side];q=np.array(row['points']);r=np.array(row['radii']);t,_,_=frames(q);ratios=[]
        for i in np.linspace(30,len(q)-20,20).astype(int):
            result=section_aspect(m,q[i],t[i],r[i])
            if result:ratios.append(result['minorMajorRatio'])
        d=cKDTree(arteries.geometry['PICA '+side].vertices).query(m.vertices)[0]
        report['posteriorSpinal'].append({'side':side,'sharedPicaSkinVertices':int((d<3e-5).sum()),'minimumSectionRoundness':min(ratios,default=None),'newOriginFromPica':True,'oldV3OstiumClosed':row['oldV3OstiumClosed']})
    report['surfaceContactCount']=sum(r['triangleContacts'] for r in report['rows'] if not r['intentionalPenetratingBranch']);report['surfaceContainedWallVertices']=sum(r.get('wallVerticesInsideClosedTissue',0) for r in report['rows'] if not r['intentionalPenetratingBranch']);report['surfaceChecksPassed']=report['surfaceContactCount']==0 and report['surfaceContainedWallVertices']==0
    report['spinalJoinChecksPassed']=all(r['sharedPicaSkinVertices']>=20 and r['minimumSectionRoundness']>.95 for r in report['posteriorSpinal'])
    report['passed']=report['surfaceChecksPassed'] and report['spinalJoinChecksPassed'];np.savez_compressed(W/'contact-seeds.npz',points=np.array(seeds).reshape(-1,3),names=np.array(names));(W/'surface-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['surfaceContactCount'],report['posteriorSpinal'],flush=True)

if __name__=='__main__':main()
