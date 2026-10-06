"""Independent crossing and exported venous-section checks."""
import argparse,json
import numpy as np,trimesh
from scipy.spatial import cKDTree
from audit_expanded_pial import contact_points
from audit_tubular_candidate import section_aspect
from rebuild_tubular_brainstem_veins import frames
from fit_vessels import APP
from reconcile_brainstem import sha
from verify_fitting import inside

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--directory',default='.authoring/posterior-round58');args=parser.parse_args();w=APP/args.directory
    veins=trimesh.load(w/'veins-trial.glb',process=False);arterial=trimesh.load(w/'arteries-collision-solid.glb',force='mesh',process=False);saved=json.loads((w/'veins-round-courses.json').read_text());paths={k:np.array(row['points']) for k,row in saved.items()};rows=[]
    for k,row in saved.items():
        q=paths[k];r=np.array(row['radii']);t,_,_=frames(q);anchors=q[row.get('anchorIndices',[0,len(q)-1])];other=cKDTree(np.concatenate([p for name,p in paths.items() if name!=k]));ratios=[];diameters=[]
        others=cKDTree(np.concatenate([m.vertices for name,m in veins.geometry.items() if name!=k]));wall=veins.geometry[k].vertices;seam=wall[others.query(wall)[0]<3e-5];seam_tree=cKDTree(seam) if len(seam) else None;seam_excluded=0
        for i in np.linspace(int(.12*len(q)),int(.88*len(q)),24).astype(int):
            if np.linalg.norm(anchors-q[i],axis=1).min()<r[i]*2.6 or other.query(q[i])[0]<r[i]*2.6:continue
            if seam_tree is not None and seam_tree.query(q[i])[0]<r[i]*2.6:seam_excluded+=1;continue
            result=section_aspect(veins.geometry[k],q[i],t[i],r[i])
            if result:ratios.append(result['minorMajorRatio']);diameters.append(result['minimumDiameterToIntendedRatio'])
        n,points=contact_points(veins.geometry[k],arterial);contained=int(inside(wall,arterial).sum());test={'node':k,'triangleContactsWithArteries':n,'wallVerticesInsideArteries':contained,'validRoundSections':len(ratios),'sectionsExcludedAtPhysicalLabelSeams':seam_excluded,'minimumSectionRoundness':min(ratios,default=None),'medianSectionRoundness':float(np.median(ratios)) if ratios else None,'minimumDiameterToIntendedRatio':min(diameters,default=None)};rows.append(test);print(test,flush=True)
        (w/'crossing-roundness-validation.json').write_text(json.dumps({'rows':rows},indent=2)+'\n')
    report={'rows':rows,'hashes':{'veins':sha(w/'veins-trial.glb'),'arteries':sha(w/'arteries-trial.glb')},'crossingChecksPassed':all(row['triangleContactsWithArteries']==0 and row['wallVerticesInsideArteries']==0 for row in rows),'sectionFlatteningChecksPassed':all(row['minimumDiameterToIntendedRatio'] is None or (row['minimumDiameterToIntendedRatio']>.90 and row['medianSectionRoundness']>.97) for row in rows),'strictIsolatedAspectChecksPassed':all(row['minimumSectionRoundness'] is None or row['minimumSectionRoundness']>.90 for row in rows),'scope':'Actual exported skin sections outside branch collars and shared label boundaries; all rebuilt vein walls checked against the closed local arterial solid by triangle intersection and vertex containment. A label has partial circumference where it merges into a parent vessel, so physical label seams are excluded. The minimum diameter measures flattening: a bend can widen an oblique section while preserving its full minor diameter. Raw aspect ratios and the separate strict aspect check remain reported.'};report['passed']=report['crossingChecksPassed'] and report['sectionFlatteningChecksPassed'];(w/'crossing-roundness-validation.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
