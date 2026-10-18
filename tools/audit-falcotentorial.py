"""Read-only current-mesh review of the falcotentorial/Galenic complex."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'mma-v0952'));from common import *
sys.path.insert(0,str(Path(__file__).parent/'mma-v0958'));from fold_engine import intersections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
APP=Path(__file__).resolve().parents[1];mf=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());cat={s['asset']['node']:s for s in mf['structures'] if s.get('asset')};cache={}
def mesh(n):
 if n not in cache:cache[n]=load(n)
 return cache[n]
def crop(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 a=v[f];f=f[np.all(a.max(1)>=lo,1)&np.all(a.min(1)<=hi,1)];a=w[g];g=g[np.all(a.max(1)>=lo,1)&np.all(a.min(1)<=hi,1)]
 return contacts(v,f,w,g) if len(f) and len(g) else 0
def boundary(v,f):
 v,inv=np.unique(v,axis=0,return_inverse=True);f=inv[f];e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1);e,c=np.unique(e,axis=0,return_counts=True);return v,e[c==1],int((c>2).sum())
names=['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence','brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']
rows=[]
for n in names:
 v,f=mesh(n);vv,inv=np.unique(v,axis=0,return_inverse=True);ff=inv[f];_,e,nm=boundary(v,f);all_e=np.vstack([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);graph=coo_matrix((np.ones(len(all_e)),(all_e[:,0],all_e[:,1])),shape=(len(vv),len(vv))).tocsr();area=np.linalg.norm(np.cross(vv[ff[:,1]]-vv[ff[:,0]],vv[ff[:,2]]-vv[ff[:,0]]),axis=1)/2
 row={'id':n,'vertices':len(v),'faces':len(f),'topology':{'boundaryEdges':len(e),'nonManifoldEdges':nm,'degenerateFaces':int((area<1e-10).sum()),'components':int(connected_components(graph,directed=False,return_labels=False)),'nonAdjacentSelfIntersections':len(intersections(vv,ff))},'contacts':[]}
 for other,s in cat.items():
  if other==n:continue
  b=s.get('anatomy',{}).get('bounds')
  if b and (np.any(np.array(b[1])+.01<v.min(0)) or np.any(np.array(b[0])-.01>v.max(0))):continue
  w,g=mesh(other)
  if np.any(w.max(0)<v.min(0)) or np.any(w.min(0)>v.max(0)):continue
  c=crop(v,f,w,g)
  if c:row['contacts'].append({'other':other,'system':s['system'],'triangleContacts':c})
 rows.append(row);print(json.dumps(row),flush=True)
# Native interfaces are assessed on welded edges, not contacts alone.
pairs=[]
for i,n in enumerate(names[:4]):
 v,f=mesh(n);vv,e,_=boundary(v,f);vk={p.astype('<f4').tobytes() for p in v};ek={tuple(sorted((vv[a].astype('<f4').tobytes(),vv[b].astype('<f4').tobytes()))) for a,b in e}
 for other in names[i+1:4]:
  w,g=mesh(other);ww,ee,_=boundary(w,g);wk={p.astype('<f4').tobytes() for p in w};we={tuple(sorted((ww[a].astype('<f4').tobytes(),ww[b].astype('<f4').tobytes()))) for a,b in ee};pairs.append({'one':n,'two':other,'sharedCoordinates':len(vk&wk),'sharedBoundaryEdges':len(ek&we),'minimumVertexDistanceMm':float(cKDTree(w).query(v)[0].min())})
report={'release':'0.9.86','sourceAssets':json.loads((DATA/'source-assets.json').read_text()),'structures':rows,'nativeInterfaces':pairs};(WORK/'regional-audit.json').write_text(json.dumps(report,indent=2)+'\n')
