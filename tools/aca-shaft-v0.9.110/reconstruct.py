"""Replay bounded bilateral anterior A4 shaft shears with every native port fixed."""
from common import *

def reconstruct(r):
 n=r['node'];v,f=scene.mesh(n);D=W/'decoded';D.mkdir(exist_ok=True);O=W/'replayed';O.mkdir(exist_ok=True)
 def smooth(x):
  x=np.clip(x,0,1);return x*x*x*(10+x*(-15+6*x))
 def derivative(x):return np.where((x>0)&(x<1),30*x*x*(x-1)**2,0.)
 y=v[:,1].astype(float);L=r['posteriorPlateauY']-r['posteriorSupportY'];R=r['anteriorSupportY']-r['anteriorPlateauY'];a=(y-r['posteriorSupportY'])/L;b=(r['anteriorSupportY']-y)/R;w=smooth(a)*smooth(b);dw=derivative(a)/L*smooth(b)-smooth(a)*derivative(b)/R;p=v.astype(float);p[:,0]+=r['medialDisplacementMm']*w;p[:,2]+=r['superiorDisplacementMm']*w;p=p.astype('<f4');moved=np.any(p!=v,axis=1);assert float(np.linalg.norm(p-v,axis=1).max())<=r['maximumDisplacementLimitMm']
 a=v[f].astype(float);b=p[f].astype(float);oldcross=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);newcross=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);assert np.all(np.einsum('ij,ij->i',oldcross,newcross)>0)
 # One invertible shear per Y plane: y is fixed and the analytical Jacobian determinant is exactly one.
 assert np.array_equal(p[:,1],v[:,1]);attachments=[];keys=set(map(tuple,v))
 for other in scene.nearby(v.min(0),v.max(0)):
  if other==n:continue
  q,g=scene.mesh(other);shared=keys&set(map(tuple,q))
  if not shared:continue
  mask=np.array([tuple(x)in shared for x in v]);assert np.array_equal(p[mask],v[mask]),('moved-native-interface',other)
  attachments.append({'other':other,'sharedCoordinates':len(shared),'allPositionsFixed':True})
 # No new coordinate welds may be created within this mesh or with any other arterial label.
 u,inv=np.unique(v,axis=0,return_inverse=True);pu=np.array([p[np.flatnonzero(inv==i)[0]]for i in range(len(u))]);assert len(np.unique(pu,axis=0))==len(u)
 changedcoords=np.unique(p[moved],axis=0);dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=changedcoords.view(dt).reshape(-1);reviewed=0
 for other in scene.rows:
  if scene.systems[other]!='artery':continue
  reviewed+=1
  if other==n:continue
  q,g=scene.mesh(other);assert not np.isin(np.asarray(q).view(dt).reshape(-1),match).any(),('new-coordinate-weld',other)
 assert reviewed==766
 u0,e0,c0,b0,_,_=edge_table(v,f);u1,e1,c1,b1,_,_=edge_table(p,f)
 assert int((c0==1).sum())==int((c1==1).sum())
 assert int(((c0>2)|((c0==2)&(b0!=0))).sum())==int(((c1>2)|((c1==2)&(b1!=0))).sum())
 boundaryKeys=set(map(tuple,u0[np.unique(e0[c0==1])]))
 mask=np.array([tuple(x)in boundaryKeys for x in v]);assert np.array_equal(p[mask],v[mask])
 raw=np.fromfile(D/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4);norm=raw[:,:3].astype(float)/32767.;norm=np.maximum(norm,-1);new=norm.copy();new[:,1]-=r['medialDisplacementMm']*dw*norm[:,0]+r['superiorDisplacementMm']*dw*norm[:,2];new/=np.maximum(np.linalg.norm(new,axis=1)[:,None],1e-30);encoded=raw.copy();change=moved&(dw!=0);encoded[change,:3]=np.rint(np.clip(new[change],-1,1)*32767).astype('<i2');assert np.array_equal(encoded[~change],raw[~change]);retained=~np.any(moved[f],axis=1)
 for k,data in [('positions',p),('indices',f),('normal-snorm16',encoded)]:
  data.tofile(O/(n+'.'+k+'.bin'))
  if(W/'accepted'/(n+'.'+k+'.bin')).exists():assert(O/(n+'.'+k+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+k+'.bin')).read_bytes()
 provenance=[{'node':n,'retainedSourceTrianglesWithExactCornerNormals':int(retained.sum()),'sourceTriangles':len(f),'indicesByteExact':True,'unchangedVertexNormalsExact':True,'plateauNormalsExact':True,'normalTransform':'Inverse transpose of the analytical unit-determinant shear; transformed flanks quantised once to SNORM16.'}]
 row={'node':n,'sourceVertices':len(v),'sourceTriangles':len(f),'changedVertices':int(moved.sum()),'changedFaces':int((~retained).sum()),'maximumDisplacementMm':float(np.linalg.norm(p-v,axis=1).max()),'sourceNormalOppositeFaces':0,'analyticalJacobianDeterminant':1,'indicesByteExact':True,'allSourceCoordinatesWeldPartitionsRetained':True,'allBoundaryVerticesFixed':True,'sourceBoundaryEdges':int((c0==1).sum()),'sourceBadEdges':int(((c0>2)|((c0==2)&(b0!=0))).sum()),'candidateBoundaryEdges':int((c1==1).sum()),'candidateBadEdges':int(((c1>2)|((c1==2)&(b1!=0))).sum()),'newCoordinateWelds':0,'reviewedArterialMeshesForWelds':766,'attachments':attachments,'replayedBuffersByteExact':(W/'accepted').exists()}
 return row,provenance[0]

rows=[];provenance=[]
for spec in json.load(open(W/'spec.json'))['changes']:
 row,normal=reconstruct(spec);rows.append(row);provenance.append(normal);print(row,flush=True)

# Compare final candidate coordinates with every other final arterial mesh.
O=W/'replayed'
C={r['node']:np.fromfile(O/(r['node']+'.positions.bin'),'<f4').reshape(-1,3)for r in rows}
for n,p in C.items():
 v,_=scene.mesh(n);match=set(map(tuple,p[np.any(p!=v,axis=1)]))
 # Unchanged labels were already checked against all 766 source meshes above.
 # Only the other changed label needs another check against its final coordinates.
 for other,q in C.items():
  if other==n:continue
  assert not match.intersection(map(tuple,q)),('new-final-coordinate-weld',n,other)
(W/'normal-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
(W/'reconstruction-validation.json').write_text(json.dumps({'release':'0.9.110','passed':True,'changes':rows,'allFinalArterialCoordinateWeldsChecked':True},indent=2)+'\n')
