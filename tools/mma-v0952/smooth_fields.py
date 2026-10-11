"""Continuous ambient fields, shared by every vertex at a native interface.

Experiments stay outside public assets until independent acceptance passes.
"""
from common import *
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import cdist

class GuideField:
    def __init__(self, points, vectors, sigma, support):
        self.points=np.asarray(points)[::12]
        self.vectors=np.asarray(vectors)[::12]
        self.tree=cKDTree(self.points)
        self.sigma=sigma;self.support=support;self.cortical=False
    def displacement(self, v):
        out=np.zeros_like(v,dtype=float)
        for start in range(0,len(v),5000):
            p=v[start:start+5000]
            nearest=self.tree.query(p)[0]
            # Every control contributes. Truncating to k neighbours introduced
            # discontinuities when the neighbour set changed between branches.
            d2=cdist(p,self.points,'sqeuclidean')
            d2-=d2.min(1)[:,None]
            w=np.exp(-d2/(2*self.sigma**2))
            vec=(w@self.vectors)/np.maximum(w.sum(1)[:,None],1e-30)
            # Constant weight around the tube, smoothly zero outside support.
            taper=smooth((self.support-nearest)/(self.support-self.sigma))
            if self.cortical:
                # Keep the medial skull base and posterior-fossa entrances fixed.
                lateral_start=np.maximum(20,45-.6*(p[:,2]-40))
                taper*=smooth((np.abs(p[:,0])-lateral_start)/15)
            out[start:start+len(p)]=vec*taper[:,None]
        return out
    def __call__(self,v):return v+self.displacement(v)

def arterial_field():
    guides=json.loads((WORK/('tree-guides.json' if '--tree' in sys.argv else 'mma-guides.json')).read_text())
    points=[];vectors=[]
    for g in guides:
        old=np.asarray(g['oldPoints']);target=np.asarray(g['points'])
        delta=gaussian_filter1d(target-old,10,axis=0)
        if 'node' not in g:delta*=smooth((old[:,2]-44)/12)[:,None]
        points.append(old);vectors.append(delta)
    return GuideField(np.concatenate(points),np.concatenate(vectors),4.5,18)

def cerebral_field(amplitude):
    guides=json.loads((WORK/('tree-guides.json' if '--tree' in sys.argv else 'mma-guides.json')).read_text())
    points=[];vectors=[]
    for g in guides:
        q=np.asarray(g['points']);n=np.asarray(g['innerTableNormals'])
        n=gaussian_filter1d(n,18,axis=0)
        n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12)
        # The endocranial normal points towards the cerebral compartment.
        weight=smooth((q[:,2]-45)/15)
        points.append(q);vectors.append(amplitude*n*weight[:,None])
    field=GuideField(np.concatenate(points),np.concatenate(vectors),10,35)
    field.cortical='--cortical' in sys.argv
    return field

def catalogue_fields(manifest):
    nodes={s['id']:s for s in manifest['structures']}
    pial_roots=('artery.anterior.mca_m1_', 'artery.anterior.aca_a1_', 'artery.anterior.aca_pericallosal_', 'artery.posterior.pca_p1_', 'artery.posterior.basilar', 'artery.posterior.pica_', 'artery.anterior.posterior_communicating_', 'artery.anterior.anterior_choroidal_')
    def arterial(s):
        seen=set()
        while s and s['id'] not in seen:
            sid=s['id'];name=s.get('name','').lower();seen.add(sid)
            if any(x in name for x in ['dural','meningeal','tentorial','inferolateral','ilt ','meningohypophyseal']):return 'arterial'
            if sid.startswith(pial_roots):return 'cortical'
            s=nodes.get(s.get('parent'))
        return 'arterial'
    assignments={}
    for s in nodes.values():
        if not s.get('asset'):continue
        n=s['asset']['node'];system=s.get('system')
        if n.startswith('brain.'):assignment='cortical'
        elif system=='artery':assignment=arterial(s)
        elif system=='vein':
            dural=any(x in n for x in ['cavernous','sphenoparietal','sagittal','transverse.','sigmoid.','petrosal.','straight','torcular','marginal','occipital_sinus','basilar_plexus'])
            assignment='cortical' if s.get('vesselCourse',{}).get('scope')=='intracranial' and not dural else 'fixed'
        else:assignment='fixed'
        assignments[n]=assignment
    return assignments

if __name__=='__main__':
    import time
    a=arterial_field()
    names=['Middle meningeal','Middle meningeal left','MMA frontal','MMA frontal left','MMA orbital','MMA orbital left','MMA posterior convexity','MMA posterior convexity left']
    if '--tree' in sys.argv:names=[r['node'] for r in json.loads((WORK/'tree-guides.json').read_text())]+['MMA orbital','MMA orbital left']
    arterial={n:(a(load(n)[0]),load(n)[1]) for n in names}
    brain={n:load(n) for n in FILES if n.startswith('brain.')}
    report=[]
    for amp in ([8.] if '--only-eight' in sys.argv else ([6.,8.] if '--tree' in sys.argv else [4.,6.,8.])):
        b=cerebral_field(amp);rows=[]
        for bn,(v,f) in brain.items():
            bv=b(v)
            for name,(av,af) in arterial.items():
                if np.any(bv.max(0)<av.min(0)) or np.any(bv.min(0)>av.max(0)):continue
                nc=contacts(av,af,bv,f)
                if nc:rows.append(dict(artery=name,brain=bn,triangleContacts=nc))
        print('amplitude',amp,'pairs',len(rows),'contacts',sum(r['triangleContacts'] for r in rows),flush=True)
        report.append(dict(amplitudeMm=amp,contacts=rows))
        (WORK/('smooth-tree-test.json' if '--tree' in sys.argv else 'smooth-field-test.json')).write_text(json.dumps(report,indent=2))
