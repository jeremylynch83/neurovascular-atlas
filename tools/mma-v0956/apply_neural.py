"""Apply measured shared flow to arterial candidate buffers only."""
from clear_neural import *
import hashlib
prior=WORK.parent/'work-v0955/candidate'
revision=json.loads((prior/'revision.json').read_text())
flow_file=WORK/('outward-flow.npz' if '--outward' in sys.argv else 'neural-flow.npz')
data=np.load(flow_file)
steps=[Step(p,d) for p,d in zip(data['points'],data['vectors'])]
manifest=json.loads(Path('public/anatomy/manifest.json').read_text())
assign=catalogue_fields(manifest)
previous={r['node'] for r in revision['changed']}
names=[n for n in FILES if assign.get(n)=='arterial']
vv=[];ff=[];sizes=[]
for name in names:
    v,f=load(name,prior if name in previous else DATA)
    vv.append(v);ff.append(f);sizes.append(len(v))
v=np.concatenate(vv)
mask=steps[0].tree.query(v)[0]<steps[0].support
q=v[mask].copy();print('Active vertices',len(q),'of',len(v),flush=True)
for i,s in enumerate(steps):
    q=s(q)
    if i%10==0:print('Flow step',i,flush=True)
v[mask]=q
revision['changed']=[];revision['newLabels']=[];start=0
for name,size,f in zip(names,sizes,ff):
    q=v[start:start+size];start+=size
    old,_=load(name);shift=np.linalg.norm(q-old,axis=1)
    if shift.max()<1e-6:continue
    write(name,q,f)
    revision['changed'].append(dict(node=name,file=FILES[name],vertices=len(q),triangles=len(f),maxShiftMm=float(shift.max()),topologyExact=True,field='shared-neural-clearance-arterial'))
revision.update(release='0.9.56',status='experimental-neural-clearance',method=__doc__)
revision['flowSource']={'filename':flow_file.name,'sha256':hashlib.sha256(flow_file.read_bytes()).hexdigest()}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2))
print('Written',len(revision['changed']),flush=True)
