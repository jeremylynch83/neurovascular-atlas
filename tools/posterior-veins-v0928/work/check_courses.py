from common import *
x=json.loads((OUT/'courses.json').read_text());report=[]
for row in x['structures']:
 for i,part in enumerate(row['parts']):
  q=np.array(part['points']);d=np.diff(q,axis=0);length=np.linalg.norm(d,axis=1);tangent=d/np.maximum(length[:,None],1e-10);angle=np.arccos(np.clip((tangent[1:]*tangent[:-1]).sum(1),-1,1));bend=(angle/np.maximum((length[1:]+length[:-1])/2,.005)).max()*part['radius'];rec={'node':row['id'],'part':i,'maximumRadiusCurvatureProduct':float(bend)}
  if row['mode'] in ['pial','cisternal'] and i==0:
   k=row.get('surfaceTarget') or row['targets'][0];field=vtk.vtkImplicitPolyDataDistance();field.SetInput(meshes[k].pd);dist=np.array([field.EvaluateFunction(p) for p in q]);arc=np.r_[0,np.cumsum(length)];mask=arc<arc[-1]-6
   if part.get('startReceiver'):mask&=arc>6
   if not mask.any():continue;rec['minimumBodyTargetSignedDistanceMm']=float(dist[mask].min());rec['radiusMm']=part['radius'];rec['insideBodySamples']=int((dist[mask]<0).sum())
  report.append(rec)
(OUT/'course-checks.json').write_text(json.dumps(report,indent=2)+'\n')
for r in report:
 if r['maximumRadiusCurvatureProduct']>1 or r.get('insideBodySamples',0):print(r,flush=True)
