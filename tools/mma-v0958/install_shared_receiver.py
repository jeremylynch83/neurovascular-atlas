"""Partition a validated common exterior without duplicating internal walls.

Each triangle has one label owner. Labels meet at exact shared coordinates;
the combined surface preserves the native cavernous openings and topology.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from fold_engine import intersections
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());validation=json.loads((OUT/'receiver-common-wall-fit-spatial-validation.json').read_text());assert all(x['passed']for x in validation['results']);reports=[]
for side in ['right','left']:
 receiver='vein.sphenoparietal.'+side;labels=[receiver,'vein.middle_meningeal.anterior.'+side,'vein.middle_meningeal.posterior.'+side]
 x=np.load(OUT/('receiver-common-wall-fit-spatial-'+side+'.npz'));v=x['v'].astype(float);f=x['f'];base=np.load(OUT/('receiver-seam-completed-'+side+'.npz'))['v'].astype(float);cent=base[f].mean(1)
 sv,sf=load(receiver);cp,dr=closest(locator(sv,sf),cent);distances=[dr]
 for n in labels[1:]:
  curve=np.load(OUT/(n+'.curve.npz'));q=np.vstack([curve['q'],curve['stem']]);r=np.r_[curve['r'],np.full(len(curve['stem']),.23)];dd,ix=cKDTree(q).query(cent);distances.append(abs(dd-r[ix]))
 owner=np.argmin(np.array(distances),axis=0);owner[(dr<.30)&(cent[:,2]<85.8)]=0
 edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);faces=np.tile(np.arange(len(f)),3);order=np.lexsort((edges[:,1],edges[:,0]));ee=edges[order];fi=faces[order];take=np.all(ee[1:]==ee[:-1],axis=1);a=fi[:-1][take];b=fi[1:][take];graph=coo_matrix((np.ones(2*len(a)),(np.r_[a,b],np.r_[b,a])),shape=(len(f),len(f))).tocsr()
 # Absorb tiny ownership islands into their neighbouring label.
 for iteration in range(4):
  changed=False
  for label in range(3):
   ids=np.flatnonzero(owner==label);nc,cc=connected_components(graph[ids][:,ids],directed=False);counts=np.bincount(cc);largest=int(counts.argmax())
   for comp in range(nc):
    if comp==largest:continue
    members=ids[cc==comp];neighbour=np.unique(graph[members].indices);other=owner[neighbour];other=other[other!=label]
    if len(other):owner[members]=np.bincount(other,minlength=3).argmax();changed=True
  if not changed:break
 nn=normals(v,f);combined=[];parts=[]
 for i,n in enumerate(labels):
  faces=f[owner==i];indices=np.unique(faces);vv=v[indices];ff=np.searchsorted(indices,faces);write(n,vv,ff);nn[indices].astype('<f4').tofile(OUT/(n+'.normals.bin'));parts.append(dict(node=n,triangles=len(ff),vertices=len(vv),faceComponents=int(connected_components(graph[owner==i][:,owner==i],directed=False,return_labels=False))))
  row=dict(node=n,file='venous.glb',vertices=len(vv),triangles=len(ff),topologyExact=False,topology='common-exterior-partition',field='shared-receiver-cortex-fit',maxShiftMm=float(validation['results'][0 if side=='right'else 1]['maximumDisplacementMm']))
  for k,r in enumerate(rev['changed']):
   if r['node']==n:rev['changed'][k]=row;break
  else:rev['changed'].append(row)
  if i:
   old=np.load(OUT/(n+'.curve.npz'));curves={key:old[key]for key in old.files};tree=cKDTree(base);delta=v-base
   for key in ['q','stem']:
    dd,jj=tree.query(curves[key],k=8);ww=1/np.maximum(dd,.05)**2;curves[key]=curves[key]+np.sum(ww[:,:,None]*delta[jj],axis=1)/ww.sum(1)[:,None]
   np.savez_compressed(OUT/(n+'.curve.npz'),**curves)
  combined.append((vv,ff))
 # Validate exact ownership and reassembly, independently of partition logic.
 restored=set()
 for vv,ff in combined:
  for t in vv[ff].astype('<f4'):
   key=tuple(sorted(map(bytes,np.ascontiguousarray(t).view('V12').ravel())))
   assert key not in restored,'Duplicate external triangle ownership';restored.add(key)
 assert len(restored)==len(f)
 _,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True);wf=inv[f];ed=np.sort(np.vstack([wf[:,[0,1]],wf[:,[1,2]],wf[:,[2,0]]]),axis=1);ue,count=np.unique(ed,axis=0,return_counts=True);bound=ue[count==1];sourcev,sourcef=load(receiver);_,si=np.unique(sourcev.astype('<f4'),axis=0,return_inverse=True);sourcef=si[sourcef];sourcev=np.unique(sourcev.astype('<f4'),axis=0);se=np.sort(np.vstack([sourcef[:,[0,1]],sourcef[:,[1,2]],sourcef[:,[2,0]]]),axis=1);se,sc=np.unique(se,axis=0,return_counts=True)
 def keys(verts,edges):return {tuple(sorted((verts[a].tobytes(),verts[b].tobytes())))for a,b in edges}
 weldedv=np.unique(v.astype('<f4'),axis=0);exact=keys(weldedv,bound)==keys(sourcev,se[sc==1]);folds=intersections(v,f)
 report=dict(side=side,installed=True,parts=parts,triangles=len(f),uniqueOwnedTriangles=len(restored),nativeBoundaryEdgesExact=exact,boundaryEdges=len(bound),nonManifoldEdges=int((count>2).sum()),newSelfIntersections=len(folds),passed=exact and not folds and not(count>2).any()and all(p['faceComponents']==1 for p in parts))
 assert report['passed'],report;reports.append(report);np.savez_compressed(OUT/('receiver-network-installed-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'),owner=owner);print(report,flush=True)
rev['receiverExteriorInstalled']=True;(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'receiver-network-installation.json').write_text(json.dumps(dict(method=__doc__,results=reports,passed=all(r['passed']for r in reports)),indent=2))
