"""Read-only current-mesh audit and review guides for four MMA companion channels.

Run after decode-posterior-baseline.mjs, with its parent work directory as argv[1].
Uses the existing offline VTK helpers, not the app runtime. No mesh is rewritten.
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'mma-v0952'))
from common import *
sys.path.insert(0,str(Path(__file__).parent/'mma-v0958'))
from fold_engine import intersections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
APP=Path(__file__).resolve().parents[1]
manifest=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text())
catalogue={s.get('asset',{}).get('node'):s for s in manifest['structures'] if s.get('asset')}
meshes={}
def mesh(n):
 if n not in meshes:meshes[n]=load(n)
 return meshes[n]
def weld(v,f):
 v,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True);return v.astype(float),inv[f]
def edges(v,f):
 e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);e,c=np.unique(e,axis=0,return_counts=True);return e,c
def boundary_keys(v,f):
 e,c=edges(v,f)
 return {tuple(sorted((v[a].astype('<f4').tobytes(),v[b].astype('<f4').tobytes()))) for a,b in e[c==1]}
def topology(v,f,folds=True):
 v,f=weld(v,f);e,c=edges(v,f);t=v[f];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
 graph=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(v),len(v))).tocsr()
 return {'vertices':len(v),'triangles':len(f),'boundaryEdges':int((c==1).sum()),'nonManifoldEdges':int((c>2).sum()),'degenerateTriangles':int((area<1e-10).sum()),'duplicateTriangles':len(f)-len(np.unique(np.sort(f,axis=1),axis=0)),'components':int(connected_components(graph,directed=False,return_labels=False)),'nonAdjacentSelfIntersections':len(intersections(v,f)) if folds else None}
def join(a,b):
 v,f=mesh(a);w,g=mesh(b);shared=boundary_keys(v,f)&boundary_keys(w,g)
 verts={p for edge in shared for p in edge};points=np.array([np.frombuffer(p,'<f4') for p in verts])
 # Count rim components: an isolated coordinate touch is not an attachment.
 if len(verts):
  lookup={p:i for i,p in enumerate(verts)};ee=np.array([[lookup[x],lookup[y]] for x,y in shared]);graph=coo_matrix((np.ones(len(ee)),(ee[:,0],ee[:,1])),shape=(len(verts),len(verts))).tocsr();components=int(connected_components(graph,directed=False,return_labels=False))
 else:components=0
 return {'a':a,'b':b,'sharedBoundaryEdges':len(shared),'sharedBoundaryVertices':len(verts),'rimComponents':components,'rimCentroidMm':points.mean(0).tolist() if len(points) else None}
def crop_contacts(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 t=w[g];g=g[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
 if not len(g):return 0
 t=v[f];f=f[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
 return contacts(v,f,w,g) if len(f) else 0
def distribution(d):return dict(zip(['minimum','p05','median','p95','maximum'],map(float,np.percentile(d,[0,5,50,95,100]))))
def axial_guide(n):
 # Review stations are measured section centroids, not recovered authoring controls.
 v,f=mesh(n);p=poly(v,f);points=[];diagnostics=[]
 for z in np.linspace(v[:,2].max()-.35,v[:,2].min()+.35,100):
  pl=vtk.vtkPlane();pl.SetOrigin(0,0,z);pl.SetNormal(0,0,1);cut=vtk.vtkCutter();cut.SetInputData(p);cut.SetCutFunction(pl);cut.Update();c=cut.GetOutput()
  if not c.GetNumberOfPoints():continue
  q=vtk_to_numpy(c.GetPoints().GetData());raw=vtk_to_numpy(c.GetLines().GetData());es=[];i=0
  while i<len(raw):
   k=raw[i];ids=raw[i+1:i+1+k];es.extend(zip(ids[:-1],ids[1:]));i+=k+1
  es=np.array(es);graph=coo_matrix((np.ones(len(es)),(es[:,0],es[:,1])),shape=(len(q),len(q))).tocsr();nc,cc=connected_components(graph,directed=False)
  centres=[]
  for label in range(nc):
   e=es[cc[es[:,0]]==label];length=np.linalg.norm(q[e[:,1]]-q[e[:,0]],axis=1);centres.append(np.average((q[e[:,0]]+q[e[:,1]])/2,axis=0,weights=length))
  hint=points[-1] if points else v[v[:,2]>v[:,2].max()-1].mean(0)
  centre=min(centres,key=lambda t:np.linalg.norm(t[:2]-hint[:2]));points.append(centre)
  if nc>1:diagnostics.append({'zMm':float(z),'components':nc})
 return np.array(points),diagnostics
report={'release':'0.9.84','date':'2026-10-14','geometryChanged':False,'units':'mm','coordinates':'RAS','assetHashes':json.loads((DATA/'source-assets.json').read_text()),'method':{'topology':'Exact float32 coordinate welding, edge incidence, graph components and existing non-adjacent VTK triangle test. Label meshes are open at genuine shared interfaces; combined receiver walls are assessed separately.','contacts':'VTK half contacts on AABB-cropped triangles, 1e-7 tolerance. Counts are diagnostics, not defect counts.','guides':'100 axial section length-weighted centroids per shaft, tracked from cranial to caudal. Review stations measured from current surfaces, not original authoring centrelines. Receiver spur is represented by an exact shared-rim reference.','distances':'Sampled guide/wall vertices to surface triangles, not exact continuous minimum or physiological clearance.','containment':'Bone intersections are recorded. Neither coarse closed bone geometry nor an approximate foramen landmark establishes canal containment.'},'channels':[],'receiverNetworks':[]}
guides={'release':'0.9.84','coordinates':'RAS mm','method':report['method']['guides'],'structures':[]}
for side in ['left','right']:
 receiver='vein.sphenoparietal.'+side;rv,rf=mesh(receiver)
 for label in ['anterior','posterior']:
  n='vein.middle_meningeal.'+label+'.'+side;v,f=mesh(n);q,diag=axial_guide(n);rim=join(n,receiver)
  checks=[]
  for other in FILES:
   if other==n or other==receiver or other=='vein.middle_meningeal.'+('posterior' if label=='anterior' else 'anterior')+'.'+side:continue
   w,g=mesh(other)
   if np.any(w.max(0)<v.min(0)) or np.any(w.min(0)>v.max(0)):continue
   count=crop_contacts(v,f,w,g)
   if count:checks.append({'other':other,'system':catalogue.get(other,{}).get('system'),'triangleContacts':count})
  suffix=' left' if side=='left' else ''
  # Keep the two arterial meshes independently located; take nearest distance.
  a1=mesh('Middle meningeal'+suffix);a2=mesh('MMA frontal'+suffix)
  _,d1=closest(locator(*a1),q);_,d2=closest(locator(*a2),q);ad=np.minimum(d1,d2)
  skull=['bone.sphenoid','bone.frontal','bone.parietal.'+side,'bone.temporal.'+side]
  dd=[]
  for b in skull:dd.append(closest(locator(*mesh(b)),q)[1])
  wall_d=closest(locator(v,f),q)[1]
  row={'id':n,'side':side,'channelPosition':label,'topology':topology(v,f),'receiverInterface':rim,'contacts':checks,'shaftGuideToMmaSurfaceMm':distribution(ad),'shaftGuideToSkullSurfaceMm':distribution(np.min(dd,axis=0)),'shaftGuideToOwnWallMm':distribution(wall_d),'guideMultipleSectionComponents':diag,'cranialEndpointMm':q[0].tolist(),'caudalEndpointMm':q[-1].tolist()}
  report['channels'].append(row);guides['structures'].append({'id':n,'parts':[{'role':'main-shaft-review-guide','direction':'cranial-to-caudal, not a flow direction','points':q.tolist()}],'receiverRim':rim,'limitations':'Shaft guide only; common exterior receiver spur is specified by its shared boundary. Cranial and caudal caps are not drainage joins.'});print(json.dumps(row),flush=True)
 labels=[receiver]+['vein.middle_meningeal.'+p+'.'+side for p in ['anterior','posterior']];vv=[];ff=[];offset=0
 for n in labels:v,f=mesh(n);vv.append(v);ff.append(f+offset);offset+=len(v)
 v,f=weld(np.vstack(vv),np.vstack(ff));top=topology(v,f);rim=join(receiver,'vein.cavernous.'+side)
 report['receiverNetworks'].append({'side':side,'labels':labels,'topology':top,'cavernousInterface':rim,'boundaryMatchesCavernousInterface':boundary_keys(v,f)==(boundary_keys(*mesh(receiver))&boundary_keys(*mesh('vein.cavernous.'+side)))})
(WORK/'meningeal-review.json').write_text(json.dumps(report,indent=2)+'\n');(WORK/'meningeal-review-guides.json').write_text(json.dumps(guides,indent=2)+'\n');print('DONE',flush=True)
