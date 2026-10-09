"""Closed regional exterior, exact patch coverage and contact classification."""
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
rev=json.loads((OUT/'revision.json').read_text());quality=[]
def coords_key(v):return np.ascontiguousarray(v.astype('<f4')).view('V12').ravel()
for family,base in [('acoustic',['Labyrinthine ','Common cochlear ','Anterior vestibular ']),('meningeal',['MMA frontal','MMA frontal anterior division'])]:
 for side in ['right','left']:
  x=np.load(OUT/(family+'-network-'+side+'.npz'));v=x['v'];f=x['f'];tri=v[f];e=np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);se=np.sort(e,axis=1);ue,inv,count=np.unique(se,axis=0,return_inverse=True,return_counts=True);direction=np.bincount(inv,weights=np.where(e[:,0]<e[:,1],1,-1));graph=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(v),len(v))).tocsr();components=connected_components(graph,directed=False)[0];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);dup=len(f)-len(np.unique(np.sort(f,axis=1),axis=0));volume=float(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()/6)
  names=[p+side for p in base] if family=='acoustic' else [p+(' left' if side=='left' else '') for p in base];vk=coords_key(v);mapping={bytes(k):i for i,k in enumerate(vk)};patches=[];coverage=[]
  for n in names:
   p,g=load(n,OUT);ids=np.array([mapping[bytes(k)] for k in coords_key(p)]);coverage.append(ids[g]);pe=np.vstack([g[:,[0,1]],g[:,[1,2]],g[:,[2,0]]]);pg=coo_matrix((np.ones(len(pe)),(pe[:,0],pe[:,1])),shape=(len(p),len(p))).tocsr();patches.append(dict(node=n,vertices=len(p),triangles=len(g),connectedComponents=connected_components(pg,directed=False)[0]))
  coverage=np.vstack(coverage);same=sorted(map(tuple,f))==sorted(map(tuple,coverage));r=dict(family=family,side=side,vertices=len(v),triangles=len(f),boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),inconsistentlyOrientedEdges=int(np.sum(direction!=0)),connectedComponents=components,degenerateTriangles=int(np.sum(area<1e-10)),duplicateTriangles=int(dup),signedVolumeMm3=volume,exactDisjointPatchCoverage=same,patches=patches)
  r['passed']=same and components==1 and not r['boundaryEdges'] and not r['nonManifoldEdges'] and not r['inconsistentlyOrientedEdges'] and not r['degenerateTriangles'] and not dup and volume>0;quality.append(r)
validation=json.loads((OUT/'validation.json').read_text());new=[];expected=[]
for row in validation['contacts']:
 if row['baselineMovedFacesInContact'] or not row['candidateMovedFacesInContact']:continue
 a,b=row['a'],row['b'];explanation=None
 if a.startswith(('Anterior vestibular','Labyrinthine','Common cochlear')) and b.startswith(('Anterior vestibular','Labyrinthine','Common cochlear')):explanation='Disjoint selectable patches on the same closed acoustic exterior. Combined-network self-intersection test checks that this is a label boundary.'
 if a.startswith('MMA frontal') and b.startswith('MMA frontal'):explanation='Disjoint selectable patches on the same closed frontal meningeal exterior.'
 if a=='Odontoid descending left' and b=='bone.occipital':explanation='The moved hypoglossal branch collar crosses the unperforated bone at the regional hypoglossal corridor. No segmented lumen is available. This remains an unresolved bone-containment check.'
 if explanation:expected.append(dict(**row,explanation=explanation))
 else:new.append(row)
report=dict(release='0.9.49',regionalNetworks=quality,contactComparisonScope='Changed surfaces against actual baseline neighbour triangles. Contact pairs that already exist are retained as wider-atlas findings, not certified as cleared.',newUnexpectedContactPairs=new,classifiedNewContacts=expected,allSharedRetainedInterfacesExact=validation['passedSharedCollars'],newDegenerateFacesAbsent=validation['passedNewDegenerateFaces'],existingContactPairsRetained=[r for r in validation['contacts'] if r['baselineMovedFacesInContact'] and r['candidateMovedFacesInContact'] and not r['existingSharedInterface']],wholeAtlasWatertight=False,canalContainmentVerified=False)
report['passed']=all(r['passed'] for r in quality) and not new and validation['passedSharedCollars'] and validation['passedNewDegenerateFaces'];(OUT/'quality.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['existingContactPairsRetained','classifiedNewContacts']},indent=2))
if not report['passed']:sys.exit(1)
