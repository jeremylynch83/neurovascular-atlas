from model import *
from fit import artery_field
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d,map_coordinates
from scipy.spatial import cKDTree
def shared(parent,child):
 v,f=load(parent);b,bf=load(child);keys=np.ascontiguousarray(b.astype('<f4')).view('V12').ravel();pk=np.ascontiguousarray(v.astype('<f4')).view('V12').ravel();ids=np.flatnonzero(np.isin(keys,pk));rr=rings(b,bf,ids)
 if len(rr)!=1:raise RuntimeError('Expected one ostial ring '+child)
 return b[rr[0]],keys[ids]
def rebuild():
 result=[]
 for side in ['right','left']:
  sv,sf=load('ICA cavernous '+side);sv=(sv+artery_field(sv,side)).astype('<f4');tv,tf=clip(sv,sf,sv[:,2]-(57.5 if side=='right' else 57.4),False);pv,pf=load('ICA petrous '+side);save('ICA petrous '+side,np.concatenate([pv,tv]),np.concatenate([pf,tf+len(pv)]))
  q=np.load(OUT/'target-course.npz')[side];ss=np.linspace(0,1,3000);q=CubicSpline(np.linspace(0,1,len(q)),q)(ss);r=np.load(ROOT/('centreline-'+side+'.npz'))['radius'];r=np.interp(ss,np.linspace(0,1,len(r)),gaussian_filter1d(np.clip(r,2.15,2.65),4))
  lo=np.array([3 if side=='right' else -20,-56,56.5]);hi=np.array([21 if side=='right' else -2,-30,83]);dims=np.ceil((hi-lo)/.2).astype(int)+1;spacing=(hi-lo)/(dims-1);pp=np.stack(np.meshgrid(*[np.linspace(a,b,n) for a,b,n in zip(lo,hi,dims)],indexing='ij'),axis=-1).reshape(-1,3);d,i=cKDTree(q).query(pp);v,f=iso((d-r[i]).reshape(dims),lo,spacing);v,f=clip(v,f,v[:,2]-(58.15 if side=='right' else 58.05))
  lowv,lowf=load('ICA petrous '+side,True);lr=max(rings(lowv,lowf),key=lambda a:lowv[a,2].mean());br=min(rings(v,f),key=lambda a:v[a,2].mean());o=len(v);v=np.concatenate([v,lowv[lr]]);f=np.concatenate([f,bridge(v,br,np.arange(o,len(v)))])
  ov,of=load('ICA paraophthalmic '+side);oa,oash=shared('ICA paraophthalmic '+side,'Ophthalmic '+side);sha,shash=shared('ICA paraophthalmic '+side,'Superior hypophyseal '+side);oc=oa.mean(0);sc=sha.mean(0);dist,_=cKDTree(np.concatenate([oa,sha])).query(ov);value=np.maximum.reduce([ov[:,2]-77.6,1.35-np.linalg.norm(ov-oc,axis=1),1.15-np.linalg.norm(ov-sc,axis=1),.35-dist]);ov,of=clip(ov,of,value);keys=np.ascontiguousarray(ov.astype('<f4')).view('V12').ravel();rr=rings(ov,of);outer=min([a for a in rr if not np.any(np.isin(keys[a],np.r_[oash,shash]))],key=lambda a:ov[a,2].mean())
  dist,_=cKDTree(np.concatenate([oa,sha])).query(v);value=np.maximum.reduce([v[:,2]-77.35,1.55-np.linalg.norm(v-oc,axis=1),1.35-np.linalg.norm(v-sc,axis=1),.65-dist]);v,f=clip(v,f,value,False);br=max(rings(v,f),key=lambda a:v[a,2].mean());o=len(v);v=np.concatenate([v,ov]);f=np.concatenate([f,of+o,bridge(v,br,outer+o)])
  allroots=[]
  for child in ['Meningohypophyseal trunk','Inferolateral trunk']:
   rr,_=shared('ICA cavernous '+side,child+' '+side);rr=(rr+artery_field(rr,side)).astype('<f4');allroots.append(rr);c=rr.mean(0);v,f=clip(v,f,np.linalg.norm(v-c,axis=1)-1.6);br=min(rings(v,f),key=lambda a:np.linalg.norm(v[a].mean(0)-c));o=len(v);v=np.concatenate([v,rr]);f=np.concatenate([f,bridge(v,br,np.arange(o,len(v)))])
  original,_=load('ICA paraophthalmic '+side);protected=np.concatenate([original,lowv[lr]]+allroots).astype('<f4');v=v.astype('<f4');keys=np.ascontiguousarray(v).view('V12').ravel();locked=np.isin(keys,np.ascontiguousarray(protected).view('V12').ravel());parent=np.arange(len(v))
  def root(i):
   while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
   return i
  for aa,bb in cKDTree(v).query_pairs(.035):
   if np.linalg.norm(v[aa]-v[bb])>.005 and not(side=='left' and np.linalg.norm(v[aa]-[-9.84,-35.25,76.9])<.15):continue
   aa=root(aa);bb=root(bb)
   if aa==bb or (locked[aa] and locked[bb]):continue
   if locked[bb] or (not locked[aa] and bb<aa):aa,bb=bb,aa
   parent[bb]=aa
  f=np.array([root(i) for i in range(len(v))])[f];save('ICA rebuilt '+side,v,f);result.append({'side':side,'ophthalmicRingVertices':len(oa),'SHAvertices':len(sha)});print('Rebuilt',side,flush=True)
 (OUT/'arterial-rebuild.json').write_text(json.dumps(result,indent=2))
def cavity():
 bone=combine(['bone.sphenoid','bone.temporal.right','bone.temporal.left'])
 for side in ['right','left']:
  lo=np.array([2 if side=='right' else -23,-59,55]);hi=np.array([24 if side=='right' else -1,-30,81]);dims=np.ceil((hi-lo)/.22).astype(int)+1;spacing=(hi-lo)/(dims-1);x,y,z=np.meshgrid(*[np.linspace(a,b,n) for a,b,n in zip(lo,hi,dims)],indexing='ij');lat=x if side=='right' else -x+1.3;cx=11.5-.3*(y+45);cz=68.4+.3*(y+45);outer=(np.sqrt(((lat-cx)/5.5)**2+((y+45)/12.8)**2+((z-cz)/9)**2)-1)*5.5;posterior=(np.sqrt(((lat-13.3)/4.8)**2+((y+50)/6.8)**2+((z-62.3)/6.8)**2)-1)*4.8;h=np.maximum(1-np.abs(outer-posterior)/1.2,0);outer=np.minimum(outer,posterior)-h*h*1.2/4;outer=np.maximum(outer,(57.2 if side=='right' else 57.1)-z)
  cache=OUT/('bone-grid-'+side+'.npz')
  if cache.exists():bd=np.load(cache)['sdf']
  else:bd=sample(bone,lo,hi,dims);np.savez_compressed(cache,sdf=bd)
  outer=np.maximum(outer,.55-bd);save('outer-body.'+side,*iso(outer,lo,spacing));artery=closed(combine(['ICA rebuilt '+side,'ICA petrous '+side],True));ad=sample(artery,lo,hi,dims);sdf=np.maximum(outer,.32-ad);save('vein.cavernous.'+side,*iso(sdf,lo,spacing));np.savez_compressed(OUT/('cavity-'+side+'.npz'),sdf=sdf,outer=outer,lo=lo,spacing=spacing);print('Sinus',side,flush=True)
def partition():
 result=[]
 for side in ['right','left']:
  v,f=load('ICA rebuilt '+side,True);g=np.load(OUT/('cavity-'+side+'.npz'));d=map_coordinates(g['outer'],((v-g['lo'])/g['spacing']).T,order=1,mode='constant',cval=100);cv,cf=clip(v,f,-d);av,af=clip(v,f,d);save('ICA cavernous '+side,cv,cf);save('ICA paraophthalmic '+side,av,af)
  old,_=load('ICA cavernous '+side);old+=artery_field(old,side);od=map_coordinates(g['outer'],((old-g['lo'])/g['spacing']).T,order=1,mode='constant',cval=100);mask=old[:,2]>=(57.5 if side=='right' else 57.4);mx=float(od[mask].max())
  if mx>.05:raise RuntimeError('Refusing boundary change to hide source C4 protrusions '+str(mx))
  result.append({'side':side,'entryZMm':57.5 if side=='right' else 57.4,'sourceC4MaximumOuterSdfMm':mx,'boundaryStatus':'Retained estimated petrolingual entry; proximal ring estimated from independent bone-fitted roof, not segmented dura'})
 (OUT/'boundaries.json').write_text(json.dumps(result,indent=2))
def revision():
 r=json.loads((OUT/'revision.json').read_text());r['changed']=[{'node':a['name'],'file':a['file']} for a in META if (OUT/(a['name']+'.positions.bin')).exists()];(OUT/'revision.json').write_text(json.dumps(r,indent=2))
if __name__=='__main__':
 import sys
 for stage in sys.argv[1:]:{'rebuild':rebuild,'cavity':cavity,'partition':partition,'revision':revision}[stage]()
