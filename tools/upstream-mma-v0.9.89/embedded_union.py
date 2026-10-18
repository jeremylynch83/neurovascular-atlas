from union_candidate import *
from common import section
from weld import weld_parts

def modified_child(n,parent,scale=.7,length=1.5):
 v,f=mesh(n);r=max(rims(v,f),key=lambda r:abs(v[r,0].mean()));c=v[r].mean(0);q=section(*mesh(parent),2,c[2]);target=q.mean(0);delta=target-c;d=np.linalg.norm(v-c,axis=1);weight=1-smooth(d/length);p=v+weight[:,None]*delta
 # Radial shrink is limited to the first native ring and fades smoothly.
 ringv=v[r]-c;_,_,axes=np.linalg.svd(ringv);axis=axes[-1];rad=v-c-np.outer((v-c)@axis,axis);p-=weight[:,None]*(1-scale)*rad
 p=p.astype('<f4').astype(float);return p,f,r,{'node':n,'shift':delta.tolist(),'scale':scale,'length':length,'maxDisplacement':float(np.linalg.norm(p-v,axis=1).max())}
def closed_modified(n,p,f,rim):
 recipe=surfaces['entries'][ids[n]];extra=np.array(recipe['extra']);oldv,_=mesh(n);c=oldv[rim].mean(0);j=np.argmin(np.linalg.norm(extra-c,axis=1));extra[j]=p[rim].mean(0);verts=np.vstack([p,extra]);faces=np.vstack([f,np.array(recipe['caps']).reshape(-1,3)]);o=poly(verts,faces);a=numpy_to_vtk(np.r_[np.ones(len(f),np.int32),np.zeros(len(faces)-len(f),np.int32)],deep=True);a.SetName('Native');o.GetCellData().AddArray(a);clean=vtk.vtkCleanPolyData();clean.SetInputData(o);clean.SetTolerance(0.);clean.Update();return clean.GetOutput()
if __name__=='__main__':
 reports=[]
 for side in ['left','right']:
  names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];accepted=False
  for scale in [.7,.5]:
   p,f,r,d=modified_child(names[1],names[0],scale);cp=closed(names[0]);cc=closed_modified(names[1],p,f,r);print('inlet inside',side,scale,inside(p[r],cp).sum(),len(r),flush=True)
   op=vtk.vtkBooleanOperationPolyDataFilter();op.SetOperationToUnion();op.SetInputData(0,cp);op.SetInputData(1,cc);op.Update();o=op.GetOutput();print('union',side,scale,o.GetNumberOfCells(),flush=True)
   if not o.GetNumberOfCells():continue
   v,f=arrays(o);native=vtk_to_numpy(o.GetCellData().GetArray('Native')).astype(bool);source=vtk_to_numpy(o.GetCellData().GetArray('CellSource'));parts={};cr=[]
   for i,n in enumerate(names):
    q,g=compact(v,f[native&(source==i)]);parts[n]=(q,g);cr.append({'node':n,'vertices':len(q),'triangles':len(g),'selfIntersections':len(intersections(q,g))})
   parts,weld_report=weld_parts(parts);p,h=parts[names[0]];q,g=parts[names[1]];vv=np.vstack([p,q]);ff=np.vstack([h,g+len(p)]);u,e,c=boundary(vv,ff);baseline=sum(len(r)for n in names for r in rims(*mesh(n)))-len(r);row={'side':side,**d,'weld':weld_report,'changes':cr,'shared':len(set(map(tuple,p))&set(map(tuple,q))),'boundaryEdges':int(np.sum(c==1)),'nonManifoldEdges':int(np.sum(c>2)),'combinedSelfIntersections':len(intersections(vv,ff))};print(row,flush=True);reports.append(row)
   # Expected only the unchanged parent proximal rim and child distal rim remain.
   expected=len(rims(*mesh(names[0]))[0])+50
   if row['nonManifoldEdges']==0 and row['boundaryEdges']==expected and row['combinedSelfIntersections']==0:
    for n,(q,g)in parts.items():q.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.astype('<u4').tofile(OUT/(n+'.indices.bin'))
    row['acceptedTopology']=True;accepted=True;break
  print('accepted',side,accepted,flush=True)
 (D.parent/'embedded-union-trials.json').write_text(json.dumps(reports,indent=2)+'\n')
