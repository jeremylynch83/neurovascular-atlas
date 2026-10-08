from model import *
baseline=ROOT/'baseline-models/complete_manifest.json'
if not baseline.exists():baseline=ROOT/'baseline/complete_manifest.json'
m=json.load(open(baseline));byid={r['id']:r for r in m['structures']};key=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel();cache={};changes=set(r['name'] for r in META if (OUT/(r['name']+'.positions.bin')).exists());result=[]
def get(name,after):
 k=(name,after)
 if k not in cache:cache[k]=key(load(name,after)[0])
 return cache[k]
for r in m['relationships']:
 a=byid[r['from']].get('asset',{}).get('node');b=byid[r['to']].get('asset',{}).get('node')
 if not a or not b or not(a in changes or b in changes):continue
 if byid[r['from']]['system'] not in ['artery','vein'] or byid[r['to']]['system'] not in ['artery','vein']:continue
 old=len(np.intersect1d(get(a,False),get(b,False)))
 if old<3:continue
 new=len(np.intersect1d(get(a,True),get(b,True)));out={'a':a,'b':b,'type':r['type'],'baselineSharedVertices':old,'newSharedVertices':new,'passed':new>=3}
 if not out['passed'] and a.startswith('ICA cavernous'):
  replacement='ICA petrous '+a.split()[-1];n=len(np.intersect1d(get(replacement,True),get(b,True)))
  if n>=3:out.update(passed=True,newSharedVertices=n,boundaryReassignment=replacement)
 result.append(out)
(OUT/'catalogue-joins.json').write_text(json.dumps(result,indent=2));print('Physical catalogue joins',len(result),'failed',[r for r in result if not r['passed']],flush=True)
