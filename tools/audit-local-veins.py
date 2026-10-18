"""Current-surface local venous audit; no geometry is changed by this script."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'mma-v0952'))
from common import *
sys.path.insert(0,str(Path(__file__).parent/'mma-v0958'))
from fold_engine import intersections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
APP=Path(__file__).resolve().parents[1];mf=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());catalogue={s.get('asset',{}).get('node'):s for s in mf['structures'] if s.get('asset')}
names=['vein.'+n+'.'+s for s in ['left','right'] for n in ['superior_petrosal','inferior_petrosal','vertebral','vertebral_periarterial_plexus','inferior_alveolar','infraorbital','central_retinal','internal_auditory','middle_meningeal.anterior','middle_meningeal.posterior']]
cache={}
def mesh(n):
 if n not in cache:cache[n]=load(n)
 return cache[n]
def boundary(v,f):
 e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);e,c=np.unique(e,axis=0,return_counts=True);return e[c==1],int((c>2).sum())
def keys(v,e):return {tuple(sorted((v[a].astype('<f4').tobytes(),v[b].astype('<f4').tobytes()))) for a,b in e}
def cropped_contacts(v,f,w,g):
 lo=np.maximum(v.min(0),w.min(0));hi=np.minimum(v.max(0),w.max(0))
 if np.any(lo>hi):return 0
 t=w[g];g=g[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
 t=v[f];f=f[np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)]
 return contacts(v,f,w,g) if len(f) and len(g) else 0
bones=[n for n in FILES if n.startswith('bone.') and n not in ['bone.mandible','bone.hyoid']];loc={n:locator(*mesh(n)) for n in bones}
def screen(n,axis,stations):
 v,f=mesh(n);rows=[]
 for z in stations:
  p=section(v,f,axis,z)
  if not len(p):continue
  centre=(p.min(0)+p.max(0))/2;hits=[]
  for bone,l in loc.items():
   cp,d=closest(l,centre[None]);_,wd=closest(l,p);hits.append((float(wd.min()),bone,cp[0],float(d[0])))
  gap,bone,cp,d=min(hits,key=lambda x:x[0]);rows.append({'coordinate':float(z),'centre':centre.tolist(),'bone':bone,'closest':cp.tolist(),'minimumWallGapMm':gap,'centreGapMm':d})
 return rows
report={'release':'0.9.85','units':'mm','assetHashes':json.loads((DATA/'source-assets.json').read_text()),'structures':[],'petrosalSections':[],'scope':'20 local venous labels; contacts/topology do not establish full anatomical acceptance. Canal/nerve/cervical targets absent from this scene are not inferred.'}
for side,sign in [('left',-1),('right',1)]:
 for family,axis,stations in [('superior_petrosal',0,sign*np.arange(16.5,27,.5)),('inferior_petrosal',2,np.arange(49,63,.5))]:report['petrosalSections'].append({'id':'vein.'+family+'.'+side,'axis':axis,'sections':screen('vein.'+family+'.'+side,axis,stations)})
(WORK/'petrosal-sections.json').write_text(json.dumps(report['petrosalSections'],indent=2)+'\n')
for n in names:
 v,f=mesh(n);vv,inv=np.unique(v,axis=0,return_inverse=True);ff=inv[f];e,nm=boundary(vv,ff);tri=vv[ff];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2;all_edges=np.vstack([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);graph=coo_matrix((np.ones(len(all_edges)),(all_edges[:,0],all_edges[:,1])),shape=(len(vv),len(vv))).tocsr()
 row={'id':n,'topology':{'boundaryEdges':len(e),'nonManifoldEdges':nm,'degenerateFaces':int((area<1e-10).sum()),'components':int(connected_components(graph,directed=False,return_labels=False)),'nonAdjacentSelfIntersections':len(intersections(vv,ff))},'contacts':[]}
 for other,s in catalogue.items():
  if other==n:continue
  b=s.get('anatomy',{}).get('bounds')
  if b and (np.any(np.array(b[1])+.01<v.min(0)) or np.any(np.array(b[0])-.01>v.max(0))):continue
  w,g=mesh(other)
  if np.any(w.max(0)<v.min(0)) or np.any(w.min(0)>v.max(0)):continue
  c=cropped_contacts(v,f,w,g)
  if c:row['contacts'].append({'other':other,'system':s['system'],'triangleContacts':c,'declaredReceiver':any(r['type']=='drains_to' and r['from']==n and r['to']==s['id'] for r in mf['relationships'])})
 report['structures'].append(row);print(json.dumps(row),flush=True)
(WORK/'local-veins-baseline.json').write_text(json.dumps(report,indent=2)+'\n')
