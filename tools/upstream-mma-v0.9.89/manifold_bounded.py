from embedded_union import *
sys.path.insert(0,str(D.parent/'deps'));import manifold3d as manifold

def solid(polydata,original_id):
 v,f=arrays(polydata);u,ix=np.unique(v,axis=0,return_inverse=True);g=ix[f].astype(np.uint32);mesh64=manifold.Mesh64(vert_properties=np.ascontiguousarray(u,dtype=np.float64),tri_verts=np.ascontiguousarray(g,dtype=np.uint64),run_index=np.array([0,3*len(g)],np.uint64),run_original_id=np.array([original_id],np.uint32),face_id=np.arange(len(g),dtype=np.uint64));result=manifold.Manifold(mesh64);return result
if __name__=='__main__':
 reports=[]
 for side in ['left','right']:
  names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];p,f,r,d=modified_child(names[1],names[0]);inputs=[closed(names[0]),closed_modified(names[1],p,f,r)];inputs.append(closed(names[1]));start=manifold.Manifold.reserve_ids(3);solids=[solid(x,start+i)for i,x in enumerate(inputs)];print('solid',side,[x.status()for x in solids],flush=True);baseline=solids[0]+solids[2];union=solids[0]+(solids[1]^baseline);print('union',union.status(),union.num_tri(),flush=True);out=union.to_mesh64();v=np.asarray(out.vert_properties)[:,:3].astype('<f4').astype(float);f=np.asarray(out.tri_verts).astype(np.uint32);face_ids=np.asarray(out.face_id);runs=np.asarray(out.run_index)//3;original=np.asarray(out.run_original_id);parts={};rows=[]
  for i,n in enumerate(names):
   selected=np.zeros(len(f),bool)
   for k,oid in enumerate(original):
    if (i==0 and oid==start)or(i==1 and oid in [start+1,start+2]):selected[runs[k]:runs[k+1]]=True
   nativeFlags=np.zeros(len(f),bool)
   for k,oid in enumerate(original):
    if not selected[runs[k]:runs[k+1]].any():continue
    native=vtk_to_numpy(inputs[int(oid-start)].GetCellData().GetArray('Native')).astype(bool);segment=slice(runs[k],runs[k+1]);nativeFlags[segment]=native[face_ids[segment]]
   centre=mesh(names[1])[0][r].mean(0);nativeFlags|=np.linalg.norm(v[f].mean(1)-centre,axis=1)<1.5;selected &=nativeFlags;p,g=compact(v,f[selected]);parts[n]=(p,g);p.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.tofile(OUT/(n+'.indices.bin'));ov,of=mesh(n);oldcoords=set(map(tuple,ov));oldfaces={tuple(sorted(map(tuple,ov[t])))for t in of};newfaces={tuple(sorted(map(tuple,p[t])))for t in g};newcoords=set(map(tuple,p));rows.append({'node':n,'vertices':len(p),'triangles':len(g),'baselineVertices':len(ov),'retainedOriginalVertices':sum(tuple(x)in newcoords for x in ov),'retainedOriginalFaces':len(oldfaces&newfaces),'removedOriginalFaces':len(oldfaces-newfaces),'newFaces':len(newfaces-oldfaces),'selfIntersections':len(intersections(p,g))});print(rows[-1],flush=True)
  p,h=parts[names[0]];q,g=parts[names[1]];vv=np.vstack([p,q]);ff=np.vstack([h,g+len(p)]);u,e,c=boundary(vv,ff);row={'side':side,'deformation':d,'sharedCoordinates':len(set(map(tuple,p))&set(map(tuple,q))),'boundaryEdges':int(np.sum(c==1)),'nonManifoldEdges':int(np.sum(c>2)),'combinedSelfIntersections':len(intersections(vv,ff)),'changes':rows};print(row,flush=True);reports.append(row)
 (D.parent/'manifold-union.json').write_text(json.dumps(reports,indent=2)+'\n')
