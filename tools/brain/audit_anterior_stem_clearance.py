"""Signed anterior wall clearance for open as well as closed stem surfaces."""
import argparse,json
import numpy as np,trimesh,vtk
from fit_vessels import APP
from build_targets import poly
from reconcile_brainstem import sha
from verify_fitting import collisions

def main():
    p=argparse.ArgumentParser();p.add_argument('--brain',default='.authoring/posterior-anchor30/brain-trial.glb');p.add_argument('--arteries',default='.authoring/brainstem19/arteries-baseline.glb');p.add_argument('--output',default='.authoring/posterior-anchor30/basilar-clearance.json');a=p.parse_args()
    artery=trimesh.load(APP/a.arteries,process=False).geometry['Basilar']
    out={'arteriesSha256':sha(APP/a.arteries),'brainSha256':sha(APP/a.brain),'states':[]}
    for path in ['public/anatomy/models/brain-context.glb',a.brain]:
        brain=trimesh.load(APP/path,process=False)
        parts=[m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]
        loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(trimesh.util.concatenate(parts)));loc.BuildLocator();values=[];bad=[]
        for pt in artery.vertices:
            t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
            if loc.IntersectWithLine([pt[0],5,pt[2]],[pt[0],-145,pt[2]],1e-8,t,q,pc,sub,cell):
                v=pt[1]-q[1];values.append(v)
                if v<-.05:bad.append(pt.tolist())
        values=np.array(values)
        row={'path':path,'wallVerticesBehindAnteriorSurface':len(bad),'minimumMm':float(values.min()),'medianMm':float(np.median(values)),'triangleContacts':sum(collisions(artery,m) for m in parts),'badWallBoundsMm':np.array(bad).reshape(-1,3).tolist() if len(bad)<10 else [np.min(bad,axis=0).tolist(),np.max(bad,axis=0).tolist()]}
        out['states'].append(row);print({k:v for k,v in row.items() if k!='badWallBoundsMm'},flush=True)
    (APP/a.output).write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
