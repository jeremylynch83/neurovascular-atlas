"""Direct tributary attachment, end-to-end label paths and cavity dimensions."""
import json
import numpy as np
import vtk
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from vtk.util.numpy_support import vtk_to_numpy
from refine_cavernous import read_glb,accessor,closed_artery
from reference import APP,ROOT,poly

v=np.load(ROOT/'venous-mesh.npz');p,f,l=v['positions'],v['faces'],v['labels']
ids=[r['id'] for r in json.loads((ROOT/'cavernous-local-build.json').read_text())['parts']]
e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
tri=np.tile(np.arange(len(f)),3);order=np.lexsort((e[:,1],e[:,0]));se=e[order];st=tri[order]
same=np.all(se[1:]==se[:-1],axis=1);a,b=st[:-1][same],st[1:][same]
lo=np.array([-24.6,-57,45.3]);hi=np.array([26.1,-28.2,80.7])
exterior=np.any((p<lo-.1)|(p>hi+.1),axis=1)
names=['superior_ophthalmic','ovale_emissary','superior_petrosal','inferior_petrosal','sphenoparietal','superficial_middle_cerebral']
joins={};paths={}
def components(ff):
    used,inv=np.unique(ff,return_inverse=True);a=inv.reshape(-1,3)
    edges=np.r_[a[:,[0,1]],a[:,[1,2]],a[:,[2,0]]]
    graph=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(used),len(used))).tocsr()
    count,labels=connected_components(graph,directed=False)
    return [used[labels==k] for k in range(count)]
csvertices={side:np.unique(f[l==ids.index('vein.cavernous.'+side)]) for side in ['right','left']}
for side in ['right','left']:
    cs=ids.index('vein.cavernous.'+side)
    targets=['vein.'+name+'.'+side for name in names]+['vein.basilar_plexus','vein.anterior_intercavernous','vein.posterior_intercavernous']
    joins[side]={}
    for sid in targets:
        vi=ids.index(sid);mask=((l[a]==cs)&(l[b]==vi))|((l[b]==cs)&(l[a]==vi))
        count=int(mask.sum());assert count>=12,(side,sid,count)
        joins[side][sid]={'direct_shared_edges':count}
    for name in names:
        sid='vein.'+name+'.'+side;cc=components(f[l==ids.index(sid)])
        routes=[{'vertices':len(ix),'direct_cs_vertices':int(np.isin(ix,csvertices[side]).sum()),'retained_exterior_vertices':int(exterior[ix].sum())} for ix in cc]
        through=[r for r in routes if r['direct_cs_vertices']>=10 and r['retained_exterior_vertices']>=20]
        assert through,(sid,routes)
        paths[sid]={'continuous_to_retained_course':True,'qualifying_components':through}
for name in ['anterior_intercavernous','posterior_intercavernous']:
    sid='vein.'+name;cc=components(f[l==ids.index(sid)])
    routes=[{side:int(np.isin(ix,csvertices[side]).sum()) for side in ['right','left']} for ix in cc]
    assert any(r['right']>=10 and r['left']>=10 for r in routes),(sid,routes)
    paths[sid]={'continuous_between_both_cavernous_sinuses':True,'components':routes}

def span(pd,y,z):
    plane=vtk.vtkPlane();plane.SetOrigin(0,y,0);plane.SetNormal(0,1,0)
    cut=vtk.vtkCutter();cut.SetInputData(pd);cut.SetCutFunction(plane);cut.Update();sec=cut.GetOutput()
    if not sec.GetNumberOfPoints():return None
    points=vtk_to_numpy(sec.GetPoints().GetData());lines=vtk_to_numpy(sec.GetLines().GetData());i=0;xs=[]
    while i<len(lines):
        n=lines[i];chain=points[lines[i+1:i+n+1]];i+=n+1
        for aa,bb in zip(chain[:-1],chain[1:]):
            if (aa[2]-z)*(bb[2]-z)<=0 and abs(bb[2]-aa[2])>1e-9:
                xs.append(float((aa+(bb-aa)*(z-aa[2])/(bb[2]-aa[2]))[0]))
    return max(xs)-min(xs) if len(xs)>1 else None
dimensions={};stations=[[-48,58],[-46,61]]
for release,path in [('0.9.12',ROOT/'baseline-v0.9.12/venous-raw.glb'),('0.9.13',ROOT/'venous-raw.glb')]:
    d,raw=read_glb(path);dimensions[release]={}
    for node in d['nodes']:
        if node['name'] not in ['vein.cavernous.right','vein.cavernous.left']:continue
        q=d['meshes'][node['mesh']]['primitives'][0];pp=accessor(d,raw,q['attributes']['POSITION']);ff=accessor(d,raw,q['indices']).reshape(-1,3)
        pd=poly(pp,ff);mass=vtk.vtkMassProperties();mass.SetInputData(closed_artery(pp,ff));mass.Update()
        dimensions[release][node['name']]={'temporarily_capped_label_volume_mm3':mass.GetVolume(),'sample_yz_mm':stations,'transverse_surface_spans_mm':[span(pd,y,z) for y,z in stations]}
for side in ['right','left']:
    sid='vein.cavernous.'+side;old=dimensions['0.9.12'][sid];new=dimensions['0.9.13'][sid]
result={'release':'0.9.13','direct_attachments':joins,'end_to_end_paths':paths,'model_dimensions':dimensions,
        'scope':'Direct common mesh edges, with separate same-label paths to the retained peripheral course or opposite cavernous sinus. Whole-network connectivity alone does not establish these attachments. Width samples are transverse surface spans at named model coordinates; capped volumes are authoring estimates, not patient morphometry.'}
(APP/'docs/validation/cavernous-direct-connections-v0.9.13.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
