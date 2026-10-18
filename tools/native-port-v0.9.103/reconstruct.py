from common import *
from geometry import cycles,triangle_crosses
from regional_validation import validate_regional
from fractions import Fraction as Q
from collections import defaultdict
import shutil
D=W/'decoded';D.mkdir(exist_ok=True);O=W/'replayed';O.mkdir(exist_ok=True);rows=[]
for n,removed in [('vein.anterior_spinal',[22489,22490]),('vein.pterygoid_plexus.left',[5749,5750,5751])]:
 v,f=scene.mesh(n)
 zero_ids=[22489,22490]if 'anterior_spinal'in n else [5751]
 for i in zero_ids:
  ta,tb,tc=[[Q(float(x))for x in q]for q in v[f[i]]];ab=[y-x for x,y in zip(ta,tb)];ac=[z-x for x,z in zip(ta,tc)];assert ab[1]*ac[2]==ab[2]*ac[1]and ab[2]*ac[0]==ab[0]*ac[2]and ab[0]*ac[1]==ab[1]*ac[0]
 v.tofile(D/(n+'.positions.bin'));f.tofile(D/(n+'.indices.bin'));keep=np.ones(len(f),bool);keep[removed]=False;g=np.array(f[keep],dtype='<u4');new=[]
 if 'pterygoid'in n:
  new=[[2991,2990,2993]];g=np.vstack([g,np.array(new,dtype='<u4')]);a,b,c=v[[2990,2992,2993]].astype(float);assert np.array_equal(b,(a+c)/2);assert np.array_equal(v[f[5749]][0],v[f[5750]][0]);assert np.array_equal(f[5749],np.array([2991,2990,2992]));assert np.array_equal(f[5750],np.array([2991,2992,2993]));oldcross=sum(np.cross(v[f[i]][1].astype(float)-v[f[i]][0],v[f[i]][2].astype(float)-v[f[i]][0])for i in [5749,5750]);t=v[new[0]].astype(float);assert np.array_equal(oldcross,np.cross(t[1]-t[0],t[2]-t[0]))
 v.tofile(O/(n+'.positions.bin'));g.tofile(O/(n+'.indices.bin'));u,e,c,b,bd,_=edge_table(v,f);uu,ee,cc,bb,dd,_=edge_table(v,g)
 def edges(u,e,mask):return {tuple(map(tuple,u[x]))for x in e[mask]}
 before=edges(u,e,c==1);after=edges(uu,ee,cc==1);prebad=edges(u,e,(c>2)|((c==2)&(b!=0)));postbad=edges(uu,ee,(cc>2)|((cc==2)&(bb!=0)));assert postbad<=prebad
 row={'node':n,'removedFaces':removed,'newTriangles':new,'retainedSourceFaceIds':np.flatnonzero(keep).tolist(),'vertices':len(v),'boundaryBefore':len(before),'boundaryAfter':len(after),'newBoundaryEdges':[[list(x),list(y)]for x,y in sorted(after-before)],'badBefore':len(prebad),'badAfter':len(postbad),'newBadEdges':0,'sourceVerticesAndNormalsRetained':True}
 if 'anterior_spinal'in n:
  loops=cycles(dd[cc==1]);row['candidateBoundaryLoopSizes']=list(map(len,loops));assert sorted(map(len,loops))==[6,82]
  # Both newly visible edges are exactly the non-zero sides of deleted
  # zero-area faces. They close the existing proximal boundary path.
  expected={tuple(sorted([tuple(v[f[removed[0]][0]]),tuple(v[f[removed[0]][1]])])),tuple(sorted([tuple(v[f[removed[1]][1]]),tuple(v[f[removed[1]][2]])]))};assert after-before==expected;row['portBoundaryProof']='Only two previously masked edges of the existing proximal port; no cap or positive-area face removed/added.'
 else:
  report=validate_regional(scene,{n:(v,g)},[]);assert report['passed'],report['issues'];row['newFaceValidation']=report;assert not(after-before)
 row['replayedBuffersByteExact']=all((O/(n+'.'+kind+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+kind+'.bin')).read_bytes()for kind in ['positions','indices']);assert row['replayedBuffersByteExact'];rows.append(row)
(D/'source-assets.json').write_text(json.dumps({Path(k).name:v for k,v in scene.source_hashes.items()},indent=2)+'\n');(W/'replay-reconstruction.json').write_text(json.dumps({'release':'0.9.103','changes':rows,'allWorldCoordinatesAndOriginalNormalsRetained':True,'pterygoidWallUnionExact':True},indent=2)+'\n');print([{k:v for k,v in r.items()if k not in ['retainedSourceFaceIds','newFaceValidation']}for r in rows],flush=True)

import subprocess
subprocess.run(['python3',str(A/'tools/native-port-v0.9.103/global_validate.py'),str(W),str(CACHE)],check=True)
report={'passed':True,'release':'0.9.103','changes':rows,'global':json.load(open(W/'global-edge-validation.json')),'removedExactZeroAreaFaces':3,'retainedSourceVertexAndNormalStreams':True,'pterygoidWallUnionExact':True,'newGlobalBoundaryEdges':0}
(W/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n')
