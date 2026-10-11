"""Compare native FBX skull/brain relationships with the supplied atlas.

Same verified source coordinate system, same recorded similarity transform.
No reference deformation and no application assets changed.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
import hashlib
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
src=WORK/'source';registered=WORK/'source-registered';registered.mkdir(exist_ok=True)
T=np.asarray(json.loads(Path('anatomy/source/brain/registration.json').read_text())['matrix'])
source={};alignment=[]
for p in src.glob('*.positions.f64'):
    n=p.name[:-len('.positions.f64')];v=np.fromfile(p,'<f8').reshape(-1,3)@T[:3,:3].T+T[:3,3];f=np.fromfile(src/(n+'.indices.bin'),'<u4').reshape(-1,3)
    source[n]=(v,f);v.astype('<f4').tofile(registered/(n+'.positions.bin'));f.tofile(registered/(n+'.indices.bin'))
    w,g=load(n);d=cKDTree(w).query(v)[0]
    alignment.append(dict(node=n,sourceVertices=len(v),atlasVertices=len(w),medianNativeVertexDistanceMm=float(np.median(d)),p95NativeVertexDistanceMm=float(np.percentile(d,95)),maximumNativeVertexDistanceMm=float(d.max())))
guides=json.loads((WORK/'tree-guides.json').read_text());tree=cKDTree(np.vstack([g['points'] for g in guides]))
def crop(v,f):
    tri=v[f];centre=tri.mean(1);radius=np.linalg.norm(tri-centre[:,None],axis=2).max(1)
    return f[tree.query(centre)[0]<radius+4]
def check(bones,brain):
    rows=[]
    for bn,(v,f) in bones.items():
        tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);cent=tri.mean(1)
        f=crop(v,f[np.einsum('ij,ij->i',normal,cent-[0,-60,95])<0])
        for n,(w,g) in brain.items():
            if n.startswith(('brain.falx','brain.tentorium')):continue
            g=crop(w,g)
            if not len(g) or not len(f):continue
            c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));tr=vtk.vtkTransform();c.SetTransform(0,tr);c.SetTransform(1,tr);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
            pts=c.GetContactsOutput().GetPoints()
            if pts is None:continue
            pts=vtk_to_numpy(pts.GetData());distance=tree.query(pts)[0];pts=pts[distance<3.5]
            if len(pts):rows.append(dict(bone=bn,brain=n,triangleContacts=int(c.GetNumberOfContacts()),nearGuideContactPoints=len(pts),minDistanceToGuideMm=float(distance.min()),sampleContactPoints=pts[::max(1,len(pts)//5)].tolist()))
    return rows
bones={n:g for n,g in source.items() if n.startswith('bone.')};brain={n:g for n,g in source.items() if n.startswith('brain.')}
sourcepairs=check(bones,brain);atlaspairs=check({n:load(n) for n in bones},{n:load(n) for n in brain})
report=dict(method='Identical source FBX frame and recorded skull-correspondence similarity transform. Pairs retained only when an exact triangle contact point is within 3.5 mm of the full MMA guides. Contact counts are point samples, not unique triangle-pair counts. No anatomical deformation or app asset change.',sourcePairs=sourcepairs,sourcePairCount=len(sourcepairs),sourceNearGuideContactPoints=sum(r['nearGuideContactPoints'] for r in sourcepairs),atlasPairs=atlaspairs,atlasPairCount=len(atlaspairs),atlasNearGuideContactPoints=sum(r['nearGuideContactPoints'] for r in atlaspairs),sourceAlignment=alignment)
(WORK/'source-reference-comparison.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='sourceAlignment'},indent=2),flush=True)
