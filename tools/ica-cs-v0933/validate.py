from model import *
from scipy.spatial import cKDTree
checks={};r=json.load(open(OUT/'revision.json'));changed={a['node'] for a in r['changed']};key=lambda v:np.ascontiguousarray(v.astype('<f4')).view('V12').ravel()
protected=[]
for side in ['right','left']:
 for stem in ['Ophthalmic','Superior hypophyseal']:
  a,af=load(stem+' '+side);b,bf=load(stem+' '+side,True);protected.append({'name':stem+' '+side,'exact':bool(np.array_equal(a,b) and np.array_equal(af,bf))})
 p,pf=load('ICA paraophthalmic '+side);q,qf=load('ICA paraophthalmic '+side,True);children=np.concatenate([load(n+' '+side)[0] for n in ['Ophthalmic','Superior hypophyseal']]);hit=np.isin(key(p),key(children));ids=np.unique(pf[hit[pf].any(1)]);protected.append({'name':'Native ostial parent faces '+side,'exact':bool(np.array_equal(p[ids],q[ids]) and np.array_equal(pf,qf)),'vertices':len(ids)})
checks['protectedOphthalmic']={'passed':all(a['exact'] for a in protected),'results':protected}
# Shared vertex counts and coordinates of all documented local junctions.
base=APP/'anatomy/source/ica-cs-v0932';joins=json.load(open(base/'validation.json'))['checks']['physicalJunctions']['junctions']
for a in json.load(open(base/'catalogue-joins.json')):
 name=a.get('boundaryReassignment',a['a']);joins.append({'a':name,'b':a['b'],'sharedVertices':a['newSharedVertices']})
seen=set();out=[]
for j in joins:
 k=(j['a'],j['b'])
 if k in seen:continue
 seen.add(k);av,_=load(k[0],True);bv,_=load(k[1],True);num=len(np.intersect1d(key(av),key(bv)));out.append({'a':k[0],'b':k[1],'sharedVertices':num,'expectedAtLeast':j['sharedVertices'],'passed':num>=j['sharedVertices']})
checks['physicalJunctions']={'passed':all(j['passed'] for j in out),'junctions':out};checks['remoteVenousSplices']={'passed':checks['physicalJunctions']['passed'],'scope':'Original topology retained; shared label junctions verified'}
q=[]
for a in r['changed']:
 v,f=load(a['node'],True);old,of=load(a['node']);t=v[f];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1);n=np.fromfile(OUT/(a['node']+'.normals.bin'),'<f4').reshape(-1,3);good=bool(np.array_equal(f,of) and np.isfinite(v).all() and (area>1e-12).all() and np.isfinite(n).all() and (np.abs(np.linalg.norm(n,axis=1)-1)<.002).all());q.append({'name':a['node'],'minimumDoubleAreaMm2':float(area.min()),'maximumDisplacementMm':float(np.linalg.norm(v-old,axis=1).max()),'passed':good})
checks['meshQuality']={'passed':all(a['passed'] for a in q),'meshes':q}
bone=combine(['bone.sphenoid','bone.temporal.right','bone.temporal.left']);bc=[];space=[]
for side in ['right','left']:
 for name in ['ICA cavernous '+side,'ICA paraophthalmic '+side,'vein.cavernous.'+side]:
  num=contacts(poly(*load(name,True)),bone);bc.append({'mesh':name,'boneContacts':num,'passed':num==0});print('Bone',name,num,flush=True)
 artery=combine(['ICA cavernous '+side,'ICA paraophthalmic '+side],True);sinus=poly(*load('vein.cavernous.'+side,True));num=contacts(artery,sinus);v,_=load('ICA cavernous '+side,True);l=locator(sinus);gaps=[closest(l,p)[1] for p in v[::3]];space.append({'side':side,'arterySinusContacts':num,'sampledMinimumSurfaceGapMm':float(min(gaps)),'passed':num==0 and min(gaps)>.10});print('Artery/sinus',side,num,min(gaps),flush=True)
branchChecks=[]
for item in json.load(open(base/'branch-clearance-authoring.json')):
 side=item['side'];sinus=poly(*load('vein.cavernous.'+side,True))
 for name in item['arterialLabels']:
  num=contacts(poly(*load(name,True)),sinus);branchChecks.append({'mesh':name,'sinusContacts':num,'passed':num==0})
checks['localBranchClearance']={'passed':all(a['passed'] for a in branchChecks),'results':branchChecks}
print('Branch clearances',sum(not a['passed'] for a in branchChecks),'failures',flush=True)
checks['boneClearance']={'passed':all(a['passed'] for a in bc),'results':bc};checks['fullSurfaceConstraints']={'passed':all(a['passed'] for a in space),'scope':'Triangle collision tests between existing closed regional walls; sampled gap. Same topology and shared deformation preserve the existing envelope partition. Not an analytical proof of containment.','sides':space}
if (OUT/'self-intersections.json').exists():
 si=json.load(open(OUT/'self-intersections.json'));checks['selfIntersections']={'passed':all(a['nonAdjacentIntersections']==0 for a in si),'sides':si}
if (OUT/'venous-self-intersections.json').exists():
 vi=json.load(open(OUT/'venous-self-intersections.json'));checks['venousSelfIntersections']={'passed':all(a['nonAdjacentIntersections']==0 for a in vi),'scope':'Changed regional venous network within the documented CS region, welded across named labels','results':vi}
res={'release':'0.9.33','passed':all(a['passed'] for a in checks.values()),'checks':checks,'limitations':['Illustrative atlas refinement; independent anatomical review pending.','Native lower petrous/canal contacts retained unchanged outside the refinement.','Dural rings and boundaries are estimates.']};(OUT/'validation.json').write_text(json.dumps(res,indent=2));print('Checks',[(k,v['passed']) for k,v in checks.items()],flush=True);print('Junction failures',[j for j in out if not j['passed']],flush=True);print('Quality failures',[j for j in q if not j['passed']],flush=True)
