"""Audit changed labels, physical joins and neighbouring context for a release."""
import argparse,json,hashlib
import numpy as np,trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP
from audit_expanded_pial import contact_points
from verify_fitting import inside

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-round59');p.add_argument('--joins-only',action='store_true');a=p.parse_args();w=APP/a.directory
    brain=trimesh.load(w/'brain-trial.glb',process=False)
    manifest=json.loads((w/'candidate-manifest.json').read_text())
    metadata=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text())
    context=set(metadata['groups']['brain'])|{'brain.upper-cervical-cord'}
    nearby=[(k,m) for k,m in brain.geometry.items() if k not in context and not any(s in k for s in ['sulcus','fissure','ventricle','aqueduct','lat-fis','falx','tentorium'])]
    report={'sourceHashes':{k:hashlib.sha256((w/f'{k}-trial.glb').read_bytes()).hexdigest() for k in ['brain','arteries','veins']},'geometry':{},'physicalJoins':[],'neighbourContacts':[],'newNeighbourContacts':[]}
    scenes={}
    for kind in ['arteries','veins']:
        old=trimesh.load(APP/f'.authoring/{kind}-baseline.glb',process=False);new=trimesh.load(w/f'{kind}-trial.glb',process=False);scenes[kind]=new
        assert set(old.geometry)==set(new.geometry),(kind,'labels changed')
        changed=[k for k in new.geometry if not (np.array_equal(old.geometry[k].vertices,new.geometry[k].vertices) and np.array_equal(old.geometry[k].faces,new.geometry[k].faces))]
        report['geometry'][kind]={'labels':len(new.geometry),'changedLabels':changed,'unchangedLabels':sorted(set(new.geometry)-set(changed))}
        for k in ([] if a.joins_only else changed):
            entry=kind=='arteries' and any(s in k.lower() for s in ['perforator','paramedian'])
            if entry:continue
            for name,m in nearby:
                if np.any(new.geometry[k].bounds[1]<m.bounds[0]) or np.any(m.bounds[1]<new.geometry[k].bounds[0]):continue
                n,_=contact_points(new.geometry[k],m)
                mask=np.all((new.geometry[k].vertices>m.bounds[0])&(new.geometry[k].vertices<m.bounds[1]),axis=1)
                contained=int(inside(new.geometry[k].vertices[mask],m).sum()) if m.is_watertight and mask.any() else 0
                if not n and not contained:continue
                o,_=contact_points(old.geometry[k],m)
                row={'kind':kind,'node':k,'tissue':name,'triangleContacts':n,'baselineTriangleContacts':o,'containedWallVertices':contained}
                report['neighbourContacts'].append(row)
                if n>o or contained:report['newNeighbourContacts'].append(row)
                print(row,flush=True)
        (w/'integration-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    for kind in ['arteries','veins']:
        source=trimesh.load(APP/'.authoring/posterior-tubular55'/f'{kind}-trial.glb',process=False)
        selected=list(json.loads((w/f'{kind}-round-courses.json').read_text()))
        keys=list(source.geometry)
        for k in selected:
            for other in keys:
                if other==k or (other in selected and other<k):continue
                one,two=source.geometry[k],source.geometry[other]
                if np.any(one.bounds[1]<two.bounds[0]) or np.any(two.bounds[1]<one.bounds[0]):continue
                before=int((cKDTree(two.vertices).query(one.vertices)[0]<3e-5).sum())
                if before<3:continue
                one,two=scenes[kind].geometry[k],scenes[kind].geometry[other]
                after=int((cKDTree(two.vertices).query(one.vertices)[0]<3e-5).sum())
                report['physicalJoins'].append({'kind':kind,'node':k,'other':other,'beforeSharedVertices':before,'afterSharedVertices':after,'passed':after>=3})
        (w/'integration-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    # The requested PSA origins replace the earlier VA joins, so exclude these
    # obsolete source joins from the pass criteria rather than asserting them.
    for row in report['physicalJoins']:
        if row['node'].startswith('Posterior spinal ') and row['other'].startswith('Vertebral '):row['intentionalOriginReplacement']=True
    report['passed']=not report['newNeighbourContacts'] and all(r['passed'] or r.get('intentionalOriginReplacement') for r in report['physicalJoins'])
    report['neighbourAuditPerformed']=not a.joins_only
    report['physicalJoinsPassed']=all(r['passed'] or r.get('intentionalOriginReplacement') for r in report['physicalJoins'])
    report['scope']='Changed exported labels against neighbouring parenchymal skins outside the separately audited posterior-fossa group. Reference sheets excluded. Existing surface contacts reported. Original exported seam pairs checked for shared positions.'
    (w/'integration-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Integration passed',report['passed'],flush=True)

if __name__=='__main__':main()
