"""Replay bounded source-coordinate corrections; never install a model."""
from common import *
rows=[];normals=[];O=W/'replayed';O.mkdir(exist_ok=True)
for spec in json.load(open(W/'spec.json'))['changes']:
 n=spec['node'];v,f=scene.mesh(n);p=np.array(v,dtype='<f4');raw=np.fromfile(W/'decoded'/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4);encoded=raw.copy()
 for correction in spec['corrections']:
  ids=np.flatnonzero(np.all(v==np.array(correction['sourceCoordinate'],dtype='<f4'),axis=1));assert ids.tolist()==correction['indices'];p[ids]=np.array(correction['candidateCoordinate'],dtype='<f4')
 moved=np.any(p!=v,axis=1);changed=np.flatnonzero(np.any(moved[f],axis=1));displacements=np.linalg.norm(p.astype(float)-v.astype(float),axis=1);assert displacements.max()<=spec['maximumDisplacementLimitMm']
 a=v[f].astype(float);b=p[f].astype(float);oldcross=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);newcross=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);assert np.all(np.einsum('ij,ij->i',oldcross,newcross)>0)
 u,inv=np.unique(v,axis=0,return_inverse=True);assert len(np.unique(p,axis=0))==len(u)
 for i in range(len(u)):assert len(np.unique(p[inv==i],axis=0))==1
 u0,e0,c0,b0,_,_=edge_table(v,f);u1,e1,c1,b1,_,_=edge_table(p,f);assert np.array_equal(c0,c1)and np.array_equal(b0,b1)
 boundary=set(map(tuple,u0[np.unique(e0[c0==1])]))
 boundaryMask=np.array([tuple(x)in boundary for x in v]);assert np.array_equal(p[boundaryMask],v[boundaryMask]);keys=set(map(tuple,v));attachments=[]
 for other in scene.nearby(v.min(0),v.max(0)):
  if other==n:continue
  q,g=scene.mesh(other);shared=keys&set(map(tuple,q))
  if not shared:continue
  mask=np.array([tuple(x)in shared for x in v]);assert np.array_equal(v[mask],p[mask]);attachments.append({'other':other,'sharedCoordinates':len(shared),'positionsAndStoredNormalsFixed':True})
 dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=np.unique(p[moved],axis=0).view(dt).reshape(-1);checked=0
 for other in scene.rows:
  checked+=1
  if other==n:continue
  q,g=scene.mesh(other);assert not np.isin(np.asarray(q).view(dt).reshape(-1),match).any(),('new-coordinate-weld',other)
 angles=[]
 for i in np.flatnonzero(moved):
  ids=np.flatnonzero(np.any(f==i,axis=1));s=oldcross[ids].sum(0);t=newcross[ids].sum(0);assert np.linalg.norm(s)>0 and np.linalg.norm(t)>0;s/=np.linalg.norm(s);t/=np.linalg.norm(t);axis=np.cross(s,t);cos=float(np.clip(s@t,-1,1));assert cos>0
  K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]]);R=np.eye(3)+K+K@K/(1+cos);assert np.allclose(R.T@R,np.eye(3),atol=1e-12)
  decoded=np.maximum(raw[i,:3].astype(float)/32767.,-1);encoded[i,:3]=np.rint(np.clip(R@decoded,-1,1)*32767).astype('<i2');angles.append(float(np.degrees(np.arctan2(np.linalg.norm(axis),cos))))
 assert max(angles)<.01 and np.array_equal(encoded[~moved],raw[~moved]);assert np.array_equal(encoded[boundaryMask],raw[boundaryMask])
 for other in attachments:
  q,g=scene.mesh(other['other']);shared=keys&set(map(tuple,q));mask=np.array([tuple(x)in shared for x in v]);assert np.array_equal(encoded[mask],raw[mask])
 for name,data in [('positions',p),('indices',f),('normal-snorm16',encoded)]:
  data.tofile(O/(n+'.'+name+'.bin'))
  if(W/'accepted'/(n+'.'+name+'.bin')).exists():assert(O/(n+'.'+name+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+name+'.bin')).read_bytes()
 retained=~np.any(moved[f],axis=1);normals.append({'node':n,'sourceTriangles':len(f),'retainedSourceTrianglesWithExactCornerNormals':int(retained.sum()),'indicesByteExact':True,'unchangedVertexNormalsExact':True,'movingVertexNormalTransport':'Minimal rotation between source/candidate area-weighted incident-face normals. Source split-normal offset retained; one SNORM16 encoding.','maximumNormalTransportAngleDegrees':max(angles),'changedStoredNormalVertices':int(np.any(encoded!=raw,axis=1).sum())})
 rows.append({'node':n,'sourceVertices':len(v),'sourceTriangles':len(f),'changedVertices':int(moved.sum()),'changedFaces':len(changed),'maximumDisplacementMm':float(displacements.max()),'indicesByteExact':True,'sourceNormalOppositeFaces':0,'sourceBoundaryEdges':int((c0==1).sum()),'candidateBoundaryEdges':int((c1==1).sum()),'sourceBadEdges':int(((c0>2)|((c0==2)&(b0!=0))).sum()),'candidateBadEdges':int(((c1>2)|((c1==2)&(b1!=0))).sum()),'allBoundaryVerticesAndNormalsFixed':True,'allSourceWeldPartitionsRetained':True,'reviewedNamedMeshesForNewWelds':checked,'newCoordinateWelds':0,'attachments':attachments,'maximumNormalTransportAngleDegrees':max(angles),'replayedBuffersByteExact':(W/'accepted').is_dir()})
(W/'normal-provenance.json').write_text(json.dumps(normals,indent=2)+'\n');(W/'reconstruction-validation.json').write_text(json.dumps({'release':'0.9.115','passed':True,'changes':rows},indent=2)+'\n');print(rows)
