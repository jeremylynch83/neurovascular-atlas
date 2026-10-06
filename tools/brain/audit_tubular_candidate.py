"""Independent exported-wall, section and crossing checks for rebuilt tubes."""
import argparse,json
import numpy as np,trimesh,vtk
from scipy.spatial import ConvexHull,cKDTree
from vtk.util.numpy_support import vtk_to_numpy
from fit_vessels import APP
from build_targets import poly,cut
from seat_posterior_candidate import locator,front_fn
from verify_fitting import collisions,distances,stats
from rebuild_tubular_brainstem_veins import frames

def section_aspect(mesh,q,tangent,radius):
    data=cut(poly(mesh),q,tangent);points=data.GetPoints()
    if points is None:return None
    v=vtk_to_numpy(points.GetData());v=v[np.linalg.norm(v-q,axis=1)<radius*1.6]
    if len(v)<8:return None
    n=np.cross(tangent,[0,0,1])
    if np.linalg.norm(n)<.1:n=np.cross(tangent,[0,1,0])
    n/=np.linalg.norm(n);b=np.cross(tangent,n);xy=np.column_stack([(v-q)@n,(v-q)@b])
    hull=ConvexHull(xy);xy=xy[hull.vertices];theta=np.linspace(0,np.pi,128);support=xy@np.array([np.cos(theta),np.sin(theta)]);width=np.ptp(support,axis=0)
    return {'minorMajorRatio':float(width.min()/width.max()),'minorDiameterMm':float(width.min()),'majorDiameterMm':float(width.max()),'minimumDiameterToIntendedRatio':float(width.min()/(2*radius)),'areaEquivalentRadiusMm':float(np.sqrt(hull.volume/np.pi))}

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-tubular54');a=p.parse_args();w=APP/a.directory
    current=trimesh.load(w/'veins-source.glb',process=False);veins=trimesh.load(w/'veins-trial.glb',process=False);brain=trimesh.load(w/'brain-trial.glb',process=False);arteries=trimesh.load(w/'arteries-trial.glb',process=False);courses=json.loads((w/'tubular-courses.json').read_text());stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);front=front_fn(locator(stem));ba=arteries.geometry['Basilar'];network=trimesh.util.concatenate(list(veins.geometry.values()));network.merge_vertices(digits_vertex=5)
    report={'scope':'rebuilt vein sections, exported wall crossings and near-wall apposition','accepted':False,'appliedToApp':False,'networkWatertight':bool(network.is_watertight),'networkWindingConsistent':bool(network.is_winding_consistent),'rows':[],'limitations':['Roundness is measured in actual exported skin sections, excluding nearby branch centres.','Tissue-ray checks cover anterior exposed skin; an open composite brainstem prevents complete closed-solid containment validation.','Collector collars and anatomical joints require review; this is not complete anatomical acceptance.']}
    all_curves={k:np.array(r['points']) for k,r in courses.items()}
    for k,row in courses.items():
        q=np.array(row['points']);r=np.array(row['radii']);t,_,_=frames(q);other=cKDTree(np.concatenate([v for kk,v in all_curves.items() if kk!=k]));after=[];before=[]
        for i in np.linspace(int(.15*len(q)),int(.85*len(q)),24).astype(int):
            if other.query(q[i])[0]<r[i]*2.6:continue
            test=section_aspect(veins.geometry[k],q[i],t[i],r[i])
            if test:after.append(test)
        m=veins.geometry[k];v=np.vstack([m.vertices,m.triangles.mean(1)]);signed=[]
        if row['mode']=='front':
            for point in v:
                if k=='vein.anterior_spinal' and point[2]<20:continue
                y=front(point[0],point[2])
                if y is not None:signed.append(point[1]-y)
        d=distances(m.vertices,stem);gap=[]
        for i in np.linspace(int(.15*len(q)),int(.85*len(q)),50).astype(int):
            if k=='vein.anterior_spinal' and q[i,2]<20:continue
            if 'lateral_mesencephalic' in k and q[i,2]>75:continue
            if 'superior_petrosal_vein' in k and abs(q[i,0]-.65)>24:continue
            mask=np.linalg.norm(m.vertices-q[i],axis=1)<r[i]*1.8
            if mask.any():gap.append(float(d[mask].min()))
        item={'node':k,'validRoundSections':len(after),'roundSectionRatioMin':min([x['minorMajorRatio'] for x in after],default=None),'roundSectionRatioMedian':float(np.median([x['minorMajorRatio'] for x in after])) if after else None,'roundSectionRadiusMedianMm':float(np.median([x['areaEquivalentRadiusMm'] for x in after])) if after else None,'wallGap':stats(np.array(gap)) if gap else None,'basilarTriangleCrossings':collisions(m,ba),'sampledAnteriorWallPenetrationCount':int((np.array(signed)<-.05).sum()),'minimumAnteriorSignedGapMm':min(signed,default=None)}
        report['rows'].append(item);(w/'tubular-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(item,flush=True)
    relevant=[m for k,m in arteries.geometry.items() if any(k.startswith(x) for x in ['Basilar','PCA ','SCA ','Pontine ','Vertebral V4','AICA ','Anterior spinal'])];arterial=trimesh.util.concatenate(relevant)
    rebuilt=trimesh.util.concatenate([veins.geometry[k] for k in courses]);report['rebuiltVeinsPosteriorArterialCrossings']=collisions(rebuilt,arterial);report['rebuiltVeinsStemTriangleContacts']=collisions(rebuilt,stem);report['networkComponents']=len(network.split(only_watertight=False));report['sectionRoundnessPassed']=all(row['roundSectionRatioMin'] is None or row['roundSectionRatioMin']>.85 for row in report['rows']);report['basilarCrossingChecksPassed']=all(row['basilarTriangleCrossings']==0 for row in report['rows']);report['collectorPortionsExcludedFromWallGapSummaries']=True;(w/'tubular-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Network summary', {k:v for k,v in report.items() if k not in ['rows','limitations']},flush=True)

if __name__=='__main__':main()
