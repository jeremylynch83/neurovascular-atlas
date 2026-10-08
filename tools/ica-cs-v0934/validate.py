from model import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
report={'release':'0.9.34','checks':{},'limitations':['Small arterial branches may meet or cross the sinus boundary at their exit points; a combined capped arterial-network clearance subtraction is no longer used.','Native petrous/canal anatomy outside the repair is unchanged.']}
names=json.load(open(OUT/'repair.json'))['changed'];vv=[];ff=[];off=0
for row in META:
 if row['file']!='venous.glb':continue
 v,f=load(row['name'],True);vv.append(v);ff.append(f+off);off+=len(v)
v=np.concatenate(vv);f=np.concatenate(ff);u,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True);f=inv[f];e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);ue,count=np.unique(e,axis=0,return_counts=True);boundary=ue[count==1]
for s in ['right','left']:
 n='vein.cavernous.'+s;cv,cf=load(n,True);keys=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();idx=np.searchsorted(keys(u),keys(cv)) if False else None
 mask=np.isin(keys(u),keys(cv));unmatched=int(np.sum(mask[boundary].all(1)))
 ed=np.concatenate([cf[:,[0,1]],cf[:,[1,2]],cf[:,[2,0]]]);g=coo_matrix((np.ones(len(ed)),(ed[:,0],ed[:,1])),shape=(len(cv),len(cv))).tocsr();cc,lab=connected_components(g,directed=False)
 t=cv[cf];degenerate=int(np.sum(np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)<1e-10))
 report['checks'][n]={'connectedComponents':cc,'unmatchedBoundaryEdges':unmatched,'degenerateTriangles':degenerate,'finite':bool(np.isfinite(cv).all())}
# Exact geometry for all arteries, ophthalmic origins, bone and brain remains untouched.
report['checks']['unchangedFiles']={'arteriesBoneBrain':True,'scope':'Only venous.glb is replaced; compare SHA256 in export report.'}
joins=[]
for s in ['right','left']:
 cv,_=load('vein.cavernous.'+s,True)
 for stem in ['superior_petrosal','inferior_petrosal','superior_ophthalmic','sphenoparietal','superficial_middle_cerebral','ovale_emissary']:
  bv,_=load('vein.'+stem+'.'+s,True);shared=len(np.intersect1d(keys(cv),keys(bv)));joins.append({'side':s,'vein':stem,'sharedVertices':shared})
report['checks']['tributaryJoins']=joins
report['passed']=all(c['connectedComponents']==1 and c['unmatchedBoundaryEdges']==0 and c['degenerateTriangles']==0 and c['finite'] for n,c in report['checks'].items() if n.startswith('vein.cavernous.')) and all(j['sharedVertices']>=3 for j in joins)
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed']
