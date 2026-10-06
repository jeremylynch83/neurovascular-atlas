"""Audit material-matched source label boundaries in a staged brain."""
import argparse,json
import numpy as np,trimesh
from fit_vessels import APP
from reconcile_brainstem import sha
def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-context39');a=p.parse_args();w=APP/a.directory
    old=trimesh.load(w/'brain-source.glb',process=False);new=trimesh.load(w/'brain-trial.glb',process=False);names=sorted(old.geometry)
    pp=[];qq=[];tags=[];geometry=[]
    for i,k in enumerate(names):
        x,y=old.geometry[k],new.geometry[k];assert np.array_equal(x.faces,y.faces)
        pp.append(x.vertices);qq.append(y.vertices);tags.append(np.full(len(x.vertices),i))
        if np.array_equal(x.vertices,y.vertices):continue
        robust=x.area_faces>5e-5;ratio=y.area_faces[robust]/x.area_faces[robust]
        geometry.append({'node':k,'minimumRobustTriangleAreaRatio':float(ratio.min()),'sourceClosed':bool(x.is_watertight),'candidateClosed':bool(y.is_watertight)})
    pp=np.concatenate(pp);qq=np.concatenate(qq);tags=np.concatenate(tags)
    _,rep,inv=np.unique(np.round(pp,5),axis=0,return_index=True,return_inverse=True);lo=np.full(len(rep),len(names));hi=np.full(len(rep),-1)
    np.minimum.at(lo,inv,tags);np.maximum.at(hi,inv,tags);joined=lo!=hi
    lower=np.full((len(rep),3),np.inf);upper=np.full((len(rep),3),-np.inf)
    np.minimum.at(lower,inv,qq);np.maximum.at(upper,inv,qq);gap=np.linalg.norm(upper-lower,axis=1);largest=np.argsort(-np.where(joined,gap,0))[:20]
    report={'brainSha256':sha(w/'brain-trial.glb'),'sourceSha256':sha(w/'brain-source.glb'),'geometry':geometry,'maximumSharedLabelPointGapMm':float(gap[joined].max(initial=0)),'largestBoundaryGaps':[{'sourcePointMm':pp[rep[i]].tolist(),'boundingGapMm':float(gap[i]),'sourceLabels':[names[j] for j in np.unique(tags[inv==i])]} for i in largest if joined[i] and gap[i]>2e-4],'limitations':['This checks coincident source material points, not every cut-surface attachment or tissue overlap.','Full brain self-intersection and anatomical interface acceptance remain separate checks.'],'appliedToApp':False}
    report['passed']=not report['largestBoundaryGaps'] and all(r['minimumRobustTriangleAreaRatio']>=.1 for r in geometry)
    (w/'brain-interface-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Material boundary gap',report['maximumSharedLabelPointGapMm'],'passed',report['passed'],flush=True)
if __name__=='__main__':main()
