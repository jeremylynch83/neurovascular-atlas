"""Offline posterior fossa reconciliation, with review-only staged outputs.

Brain correction uses one continuous posterior coordinate map on the brainstem
and neighbouring cerebellar surfaces. Distance caps retain the registered dura,
supratentorial tissue and posterior skull boundary. A trial venous shear follows the resulting anterior surfaces. These outputs
remain unreleased unless complete surface and relationship validation passes.
"""
import argparse,json,hashlib
from pathlib import Path
import numpy as np,trimesh
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from fit_vessels import (APP,read_glb,write_glb,mesh_records,accessor,
    smoothstep,curve_from_mesh,ray_tree,front)
from rebuild_central_branches import implicit

WORK=APP/'.authoring/brainstem19'
ANTERIOR=['vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']
TRANSVERSE=[f'vein.{k}.{s}' for k in ['transverse_pontine','pontomedullary'] for s in ['left','right']]
LATERAL=['vein.lateral_mesencephalic.'+s for s in ['left','right']]
PRIMARY=ANTERIOR+TRANSVERSE+LATERAL

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def update_normals(doc,data,records):
    all_old=np.concatenate([r['old'] for r in records.values()])
    _,inverse=np.unique(np.round(all_old,5),axis=0,return_inverse=True)
    normals=np.zeros((inverse.max()+1,3));offset=0
    for r in records.values():
        p=r['positions'].astype(float);f=r['faces'];ids=inverse[offset:offset+len(p)];offset+=len(p)
        fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
        for k in range(3):np.add.at(normals,ids[f[:,k]],fn)
    normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
    offset=0;changed=[]
    for key,r in records.items():
        p=r['positions'];ids=inverse[offset:offset+len(p)];offset+=len(p)
        if np.array_equal(p,r['old']):continue
        accessor(doc,data,r['primitive']['attributes']['NORMAL'])[:]=normals[ids]
        doc['accessors'][r['primitive']['attributes']['POSITION']].update(min=p.min(0).tolist(),max=p.max(0).tolist())
        changed.append({'node':key,'maximumDisplacementMm':float(np.linalg.norm(p-r['old'],axis=1).max()),'movedVertices':int((np.linalg.norm(p-r['old'],axis=1)>1e-5).sum())})
    return changed

class ContextMap:
    def __init__(self,brain,bones,selected):
        fixed=[m for k,m in brain.geometry.items() if k not in selected and not any(t in k for t in ['ventricle','sulc','lat-fis','aqueduct'])]
        mesh=trimesh.util.concatenate(fixed);tri=mesh.vertices[mesh.faces]
        lo=np.array([-28.35,-155,10]);hi=np.array([29.65,-38,77])
        keep=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
        self.fixed=implicit(trimesh.Trimesh(mesh.vertices,mesh.faces[keep],process=False))
        bb=trimesh.util.concatenate(list(bones.geometry.values()))
        keep=np.all(bb.vertices[bb.faces,1]<-95,axis=1)
        self.posterior=implicit(trimesh.Trimesh(bb.vertices,bb.faces[keep],process=False))
    def apply(self,p,amount=8):
        q=p.copy();active=(p[:,2]>20)&(p[:,2]<90)&(np.abs(p[:,0]-.65)<40)&(p[:,1]<-48)&(p[:,1]>-145)
        a=p[active]
        w=smoothstep((a[:,2]-20)/10)*(1-smoothstep((a[:,2]-72)/18))
        w*=1-smoothstep((np.abs(a[:,0]-.65)-14)/5)
        w*=smoothstep((-a[:,1]-48)/6)*(1-smoothstep((-a[:,1]-120)/25))
        delta=amount*w
        for function in [self.fixed,self.posterior]:
            distance=np.array([abs(function.EvaluateFunction(x)) for x in a])
            delta=np.minimum(delta,.8*np.maximum(0,distance-1))
        q[active,1]-=delta
        return q

def selected_context(manifest):
    return {s['id'] for s in manifest['structures'] if s.get('anatomy',{}).get('category') in ['cerebellum','brainstem'] and not any(t in s['id'] for t in ['colliculus'])}|{'brain.fourth-ventricle'}

def stage_brain():
    doc,data=read_glb(WORK/'brain-baseline.glb');records=mesh_records(doc,data)
    brain=trimesh.load(WORK/'brain-baseline.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    selected=selected_context(json.loads((WORK/'manifest-baseline.json').read_text()))
    mapping=ContextMap(brain,bones,selected)
    from refine_context_skin import subdivide,save_replaced
    selected={k for k in selected if k in records and np.max(np.linalg.norm(mapping.apply(records[k]['old'])-records[k]['old'],axis=1))>1e-5}
    refined=subdivide(records,selected,1.0);source={};replacements={};changes=[]
    for key,(p,f) in refined.items():
        q=mapping.apply(p);a=trimesh.Trimesh(p,f,process=False);b=trimesh.Trimesh(q,f,process=False)
        source[key]=(p,f,a.vertex_normals);replacements[key]=(q,f,b.vertex_normals)
        changes.append({'node':key,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'movedVertices':int((np.linalg.norm(q-p,axis=1)>1e-5).sum()),'sourceVertices':len(records[key]['old']),'refinedVertices':len(p),'sourceTriangles':len(records[key]['faces']),'refinedTriangles':len(f),'sourceSurfacePreservedBeforeDeformation':True})
    save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,replacements)
    return changes

def stage_shear_veins():
    """One Z-ordered translation field retains primary transverse sections."""
    from fit_vessels import neighbours
    doc,data=read_glb(WORK/'veins-baseline.glb');records=mesh_records(doc,data)
    from refine_context_skin import subdivide,save_replaced
    selected=neighbours(records,set(ANTERIOR+TRANSVERSE))
    selected-={'vein.superior_petrosal.left','vein.superior_petrosal.right'}
    refined=subdivide(records,selected,.6)
    replacements={k:(p,f,trimesh.Trimesh(p,f,process=False).vertex_normals) for k,(p,f) in refined.items()}
    save_replaced(WORK/'veins-source-refined.glb',doc,data,replacements)
    doc,data=read_glb(WORK/'veins-source-refined.glb');records=mesh_records(doc,data)
    brain=trimesh.load(WORK/'brain-trial.glb',process=False)
    stem=ray_tree(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]))
    source=np.concatenate([curve_from_mesh(trimesh.Trimesh(records[k]['old'],records[k]['faces'],process=False),n=120) for k in ANTERIOR])
    source=source[np.argsort(source[:,2])];keep=np.r_[True,np.diff(source[:,2])>1e-4];source=source[keep]
    stations=np.arange(source[0,2],source[-1,2]+.15,.2)
    source_y=[]
    for z in stations:
        d=np.abs(source[:,2]-z);ids=np.argsort(d)[:8];w=np.exp(-d[ids]**2/.4**2)
        source_y.append(np.average(source[ids,1],weights=w))
    delta=np.array([front(stem,3.0,z)[1]+1.75-y for z,y in zip(stations,source_y)])
    shift=PchipInterpolator(stations,gaussian_filter1d(delta,3))
    outside=np.concatenate([r['old'] for k,r in records.items() if k not in selected]);tree=cKDTree(outside)
    selected_wall=np.concatenate([r['old'] for k,r in records.items() if k in selected]);shared=selected_wall[tree.query(selected_wall)[0]<1e-5];fixed=cKDTree(shared[:,[0,2]])
    for key in selected:
        r=records[key];p=r['old'];z=np.clip(p[:,2],source[0,2],source[-1,2])
        weight=smoothstep((p[:,2]-17)/9)*(1-smoothstep((p[:,2]-79)/10))
        weight*=1-smoothstep((np.abs(p[:,0]-.65)-7)/17)
        weight*=smoothstep(fixed.query(p[:,[0,2]])[0]/6)
        delta=shift(z)
        r['positions'][:,1]+=delta*weight
    changes=update_normals(doc,data,records);write_glb(WORK/'veins-trial.glb',doc,data)
    return changes,[],[{'id':'brainstem-anterior-shear','stationsZ':stations.tolist(),'sourceCentreY':source_y,'shiftAtStationsMm':shift(stations).tolist(),'rule':'common-Z-ordered-translation-with-shared-collector-collars'}]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--brain-only',action='store_true');parser.add_argument('--veins-only',action='store_true');parser.add_argument('--shear-veins',action='store_true');parser.add_argument('--iterations',type=int,default=12);args=parser.parse_args()
    if not args.veins_only:
        changes=stage_brain();(WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2));print('Staged brain',len(changes),flush=True)
    if not args.brain_only:
        changes,batches,curves=stage_shear_veins()
        report={'release':'0.9.19','baseline':'0.9.18','status':'review-only','appliedToApp':False,'brainSha256':sha(WORK/'brain-trial.glb'),'veinsSha256':sha(WORK/'veins-trial.glb'),'brainChanges':json.loads((WORK/'brain-changes.json').read_text()),'veinChanges':changes,'batches':batches,'curves':curves}
        (WORK/'trial.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged veins',len(changes),flush=True)

if __name__=='__main__':main()
