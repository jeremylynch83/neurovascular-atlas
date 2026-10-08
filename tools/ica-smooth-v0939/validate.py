from model import *
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def keys(a):return np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()
def joined(names,after=False):
 vv=[];ff=[];offset=0
 for n in names:
  v,f=load(n,after);vv.append(v);ff.append(f+offset);offset+=len(v)
 v=np.concatenate(vv);_,first,iv=np.unique(keys(v),return_index=True,return_inverse=True);faces=iv[np.concatenate(ff)];keep=np.all(np.diff(np.sort(faces,axis=1),axis=1)>0,axis=1);return v[first],faces[keep]
def topology(v,f):
 e,c=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0,return_counts=True);boundary=e[c==1];G=coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(len(v),len(v))).tocsr();comps,_=connected_components(G,directed=False);return {'components':int(comps),'boundaryEdges':int(len(boundary)),'nonManifoldEdges':int((c>2).sum()),'boundaryKeys':set(tuple(x.tobytes() for x in row) for row in np.sort(keys(v)[boundary],axis=1))}
report=[]
for side in ['right','left']:
 names=[r['node'] for r in json.loads((OUT/'revision.json').read_text())['changed'] if r['node'].endswith(side)]+['ICA '+t+' '+side for t in ['posterior communicating','anterior choroidal','terminus']]
 v,f=joined(names,True);bv,bf=joined(names);before=topology(bv,bf);after=topology(v,f);same=after.pop('boundaryKeys')==before.pop('boundaryKeys');origins=[]
 for par,child in [('ICA cavernous','Meningohypophyseal trunk'),('ICA cavernous','Inferolateral trunk'),('ICA paraophthalmic','Ophthalmic'),('ICA paraophthalmic','Superior hypophyseal')]:
  p,_=load(par+' '+side);q,_=load(child+' '+side);r=p[np.isin(keys(p),keys(q))];np_,_=load(par+' '+side,True);nq,_=load(child+' '+side,True);hit=np_[np.isin(keys(np_),keys(nq))];# Original ring vertices remain identifiable in the refined surface.
  mapped=np_[cKDTree(np_).query(r)[1]];origins.append({'branch':child,'centroidDisplacementMm':float(np.linalg.norm(mapped.mean(0)-r.mean(0))),'sharedVertices':len(hit)})
 main=combine(['ICA '+t+' '+side for t in ['petrous','cavernous','paraophthalmic']],True);bones=combine(['bone.sphenoid','bone.temporal.'+side]);sinus=poly(*load('vein.cavernous.'+side));cv,cf=arrays(main);local=crop(main,[-28,-61,55],[29,-27,84]);result={'side':side,'topologyBefore':before,'topologyAfter':after,'nativeExternalBoundariesExact':same,'originChecks':origins,'mainIcaBoneContacts':contacts(local,bones),'mainIcaSinusContacts':contacts(local,sinus)}
 report.append(result);print(result,flush=True)
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
