"""Measure actual vessel-wall apposition rather than centreline distance."""
import argparse,json
import numpy as np,trimesh
from fit_vessels import APP,curve_from_mesh
from verify_fitting import distances,stats,collisions

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-surface52');a=p.parse_args();w=APP/a.directory
    b=trimesh.load(w/'brain-trial.glb',process=False);s=trimesh.util.concatenate([m for k,m in b.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);v=trimesh.load(w/'veins-trial.glb',process=False);art=trimesh.load(w/'arteries-trial.glb',process=False);rows=[]
    for k in ['vein.anterior_pontine','vein.anterior_pontomesencephalic','vein.anterior_medullary','vein.lateral_mesencephalic.left','vein.lateral_mesencephalic.right','Basilar']:
        m=art.geometry[k] if k=='Basilar' else v.geometry[k];d=distances(m.vertices,s);c=curve_from_mesh(m,axis=2,n=100)
        c=c[(c[:,2]>48)&(c[:,2]<74)] if 'lateral' in k else c[15:85];gap=[]
        for cp in c:
            mask=abs(m.vertices[:,2]-cp[2])<.5
            if mask.any():gap.append(d[mask].min())
        row={'node':k,'surfaceCourseWallGap':stats(np.array(gap)),'triangleContactsIncludingTangency':collisions(m,s)};rows.append(row);print(row,flush=True)
    report={'rows':rows,'limitations':['Contact includes intended tangent apposition and must be distinguished from wall crossing.','The minimum skin distance per sampled course station measures the near wall, not the entire vessel circumference.','Collector outlet portions are excluded from these apposition summaries.'],'accepted':False};(w/'surface-apposition.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
