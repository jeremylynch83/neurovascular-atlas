from model import *
names=json.load(open(OUT/'repair.json'))['changed'];joined=normals(combine(names,True));v,f=arrays(joined);nn=vtk_to_numpy(joined.GetPointData().GetNormals());keys=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();order=np.argsort(keys(v));kk=keys(v)[order]
for n in names:
 nv,_=load(n,True);i=np.searchsorted(kk,keys(nv));assert np.all(kk[i]==keys(nv));target=nn[order[i]];assert np.all(np.linalg.norm(target,axis=1)>.5);target.astype('<f4').tofile(OUT/(n+'.normals.bin'))
(OUT/'joined-normals.json').write_text(json.dumps({'release':'0.9.35','sharedNormals':'computed on welded joined network before label export','labels':len(names)},indent=2))
