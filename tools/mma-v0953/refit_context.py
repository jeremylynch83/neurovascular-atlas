"""Apply the cerebral correction only to brain and its pial vessels.
Extracranial arteries, dural sinuses and orbital structures stay fixed.
"""
from common import *
from scipy.spatial.distance import cdist
x=np.load(WORK/'coordinate-fields.npz');bc=x['bc'];bd=x['bd'];gain=float(sys.argv[2] if len(sys.argv)>2 else 1.)
def field(v):
 out=np.zeros_like(v)
 for start in range(0,len(v),12000):
  p=v[start:start+12000];ds=cdist(p,bc);k=np.exp(-ds**2/(2*12.**2));total=k.sum(1);out[start:start+len(p)]=(k@bd)/np.maximum(total[:,None],1e-15)*smooth((35-ds.min(1))/15)[:,None]*gain
 # Keep the medial temporal surface and skull-base neurovascular compartment
 # fixed while correcting the outer cerebral mantle and higher convexity.
 peripheral=np.maximum(smooth((v[:,2]-72)/18),smooth((np.abs(v[:,0])-28)/16))
 return out*peripheral[:,None]
m=json.loads((WORK.parents[0]/'public/anatomy/manifest.json').read_text());ss={s['id']:s for s in m['structures']};eligible=set()
for s in m['structures']:
 chain=[];p=s['id']
 while p in ss:chain.append(p);p=ss[p].get('parent')
 if any(p.endswith('.segment.terminus') or '.pca_' in p for p in chain) or s.get('asset',{}).get('node','').startswith(('ACA–MCA','MCA–PCA')):eligible.add(s.get('asset',{}).get('node'))
eligible.discard(None)
vein_families=['superficial_middle_cerebral','trolard','labbe','frontal_cortical','parietal_cortical','insular','posterior_orbitofrontal']
b=json.loads((WORK.parents[0]/'public/anatomy/brain-landmarks.json').read_text());cerebral={s['asset']['node'] for s in b['surfaces'] if s['anatomy']['category'] in ['cerebral_cortex','deep_landmarks']}
eligible.update(n for n in FILES if n in cerebral or any(n.startswith('vein.'+s+'.') for s in vein_families))
r=json.loads((OUT/'revision.json').read_text());oldcontext={x['node'] for x in r['changed'] if x.get('field')=='local cerebral reference'};r['changed']=[x for x in r['changed'] if x.get('field')!='local cerebral reference']
for n in oldcontext-eligible:
 for ext in ['positions','indices','normals']:(OUT/(n+'.'+ext+'.bin')).unlink(missing_ok=True)
for n in sorted(eligible):
 if n not in FILES:continue
 v,f=load(n);shift=field(v)
 if np.linalg.norm(shift,axis=1).max()<.002:continue
 q=v+shift;write(n,q,f);r['changed'].append(dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),maxShiftMm=float(np.linalg.norm(shift,axis=1).max()),field='local cerebral reference',topologyExact=True));print(n,round(r['changed'][-1]['maxShiftMm'],3),flush=True)
r['cerebralReferenceGain']=gain;(OUT/'revision.json').write_text(json.dumps(r,indent=2)+'\n')
