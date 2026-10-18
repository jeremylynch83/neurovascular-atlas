"""Independent dense surface samples and topology checks for a brain trial.

Nearest triangles are selected by centroid. Distances therefore conservatively
overestimate each sampled point's true distance. This is not a continuous
Hausdorff bound between all possible points on the two surfaces.
"""
from pathlib import Path
import argparse, json, time, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from repair.cache import BVH


def topology(p, f):
    # Exact coordinate welding is for analysis only, never an output mutation.
    t=p[f].astype(float)
    area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
    positive=f[area>0]
    _, inverse = np.unique(p, axis=0, return_inverse=True)
    w = inverse[positive]
    edges = np.sort(np.concatenate([w[:, [0,1]], w[:, [1,2]], w[:, [2,0]]]),axis=1)
    edges, counts = np.unique(edges,axis=0,return_counts=True)
    used=np.unique(w); graph=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(inverse.max()+1,inverse.max()+1)).tocsr()
    graph=graph[used][:,used]
    components=connected_components(graph,directed=False,return_labels=False)
    boundary=edges[counts==1]
    vertices=p[np.unique(f)]
    return {'components':int(components),'euler':int(len(used)-len(edges)+len(positive)),
            'nonManifoldEdges':int(np.sum(counts>2)), 'zeroAreaFaces':int(np.sum(area==0)),
            'areaMm2':float(area.sum()),'signedVolumeMm3':float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6)}, boundary, inverse


def distances(points, vertices, faces):
    triangles=vertices[faces].astype(float);centres=triangles.mean(axis=1);tree=cKDTree(centres)
    vertex_tree=cKDTree(vertices[np.unique(faces)])
    values=[]
    for start in range(0,len(points),2048):
        x=np.asarray(points[start:start+2048],dtype=float)
        _, near=tree.query(x,k=min(16,len(faces)),workers=1)
        if near.ndim==1:near=near[:,None]
        t=triangles[near]; q=x[:,None,:];a=t[:,:,0];b=t[:,:,1];c=t[:,:,2]
        candidates=[]
        for first,second in [(a,b),(b,c),(c,a)]:
            edge=second-first;den=(edge*edge).sum(2)
            u=((q-first)*edge).sum(2)/np.maximum(den,1e-40)
            closest=first+np.clip(u,0,1)[:,:,None]*edge
            candidates.append(((q-closest)**2).sum(2))
        ab=b-a;ac=c-a;v=q-a
        aa=(ab*ab).sum(2);cc=(ac*ac).sum(2);bc=(ab*ac).sum(2)
        av=(ab*v).sum(2);cv=(ac*v).sum(2);det=aa*cc-bc*bc
        safe=np.where(abs(det)>1e-30,det,1)
        u=(cc*av-bc*cv)/safe;w=(aa*cv-bc*av)/safe
        projected=a+u[:,:,None]*ab+w[:,:,None]*ac
        inside=(abs(det)>1e-30)&(u>=0)&(w>=0)&(u+w<=1)
        candidates.append(np.where(inside,((q-projected)**2).sum(2),np.inf))
        nearest_vertex,_=vertex_tree.query(x,k=1,workers=1)
        values.append(np.minimum(np.sqrt(np.minimum.reduce(candidates).min(1)),nearest_vertex))
    values=np.concatenate(values)
    # Thin, elongated triangles can be missed by a centroid shortlist. Refine
    # every value near or beyond the error budget against the full triangle BVH.
    uncertain=np.flatnonzero(values>.008)
    if len(uncertain):
        bvh=BVH.build(vertices,faces)
        for i in uncertain:values[i]=min(values[i],bvh.nearest(points[i],vertices,faces))
    return values


def sample(p,f):
    # Every vertex, plus face centres and edge midpoints at a deterministic
    # stride of 16 faces. This covers all meshes, including narrow folia.
    t=p[f[::16]]
    return np.concatenate([p,t.mean(1),(t[:,0]+t[:,1])/2,(t[:,1]+t[:,2])/2,(t[:,2]+t[:,0])/2])


def main():
    args=argparse.ArgumentParser();args.add_argument('work',type=Path);args.add_argument('error');args.add_argument('--topology-only',action='store_true');a=args.parse_args()
    report=json.loads((a.work/f'trial-{a.error}.json').read_text());results=[];all_values=[];rejected=[];begun=time.monotonic()
    for row in report['meshes']:
        if not row['changed']:continue
        name=row['name'];old=a.work/'baseline';new=a.work/a.error
        p=np.fromfile(old/(name+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(old/(name+'.indices.bin'),'<u4').reshape(-1,3)
        q=np.fromfile(new/(name+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(new/(name+'.indices.bin'),'<u4').reshape(-1,3)
        before,be,bi=topology(p,f);after,ae,ai=topology(q,g)
        reasons=[]
        for k in ['components','euler']:
            if before[k]!=after[k]:reasons.append(k+' changed')
        if after['nonManifoldEdges']>before['nonManifoldEdges']:reasons.append('new non-manifold edges')
        if after['zeroAreaFaces']>before['zeroAreaFaces']:reasons.append('new zero-area faces')
        def boundary_coords(points,inverse,edges):
            unique=np.unique(points,axis=0)
            return sorted(tuple(sorted((tuple(unique[x]),tuple(unique[y])))) for x,y in edges)
        if boundary_coords(p,bi,be)!=boundary_coords(q,ai,ae):reasons.append('boundary changed')
        for key in ['areaMm2','signedVolumeMm3']:
            if abs(after[key]-before[key])/max(abs(before[key]),1e-20)>.001:reasons.append(key+' changed by over 0.1%')
        if reasons:
            rejected.append({'name':name,'reasons':reasons,'before':before,'after':after});print(json.dumps(rejected[-1]),flush=True);continue
        if a.topology_only:
            results.append({'name':name,'before':before,'after':after});continue
        forward=distances(sample(p,f),q,g);backward=distances(sample(q,g),p,f);v=np.concatenate([forward,backward]);all_values.append(v)
        result={'name':name,'samples':len(v),'maximumSampledDistanceMm':float(v.max()),
                'p99SampledDistanceMm':float(np.percentile(v,99)),'rmsSampledDistanceMm':float(np.sqrt((v*v).mean())),
                'beforeTopology':before,'afterTopology':after,'exactBoundaryEdges':len(be)}
        results.append(result);print(json.dumps({k:v for k,v in result.items()if k not in ['beforeTopology','afterTopology']}),flush=True)
        if v.max()>.02:rejected.append({'name':name,'reasons':['maximum sampled surface distance exceeds 0.02 mm'],'maximumSampledDistanceMm':float(v.max())})
    v=np.concatenate(all_values)if all_values else np.array([])
    summary={'passed':not rejected,'errorBudgetMm':float(a.error),'sampledSurfaceLimitMm':.02,'samples':len(v),'changedMeshes':len(results),
             'maximumSampledDistanceMm':float(v.max())if len(v)else None,'p99SampledDistanceMm':float(np.percentile(v,99))if len(v)else None,
             'rmsSampledDistanceMm':float(np.sqrt((v*v).mean()))if len(v)else None,
             'boundaryEdgesComponentsAndEulerPreserved':not rejected,'newNonManifoldEdges':0 if not rejected else None,'newZeroAreaFaces':0 if not rejected else None,
             'method':'Both directions: every vertex, plus centroids and edge midpoints at stride 16 faces. Vertex and 16 nearest-centroid triangle candidates, with full triangle-BVH nearest queries for all distances over 0.008 mm. Conservative distances at sampled points; not a continuous Hausdorff guarantee. Topology is assessed after excluding existing exact zero-area faces.',
             'seconds':time.monotonic()-begun,'meshes':results,'rejectedMeshes':rejected}
    prefix='topology'if a.topology_only else'measurement'
    (a.work/f'{prefix}-{a.error}.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items()if k!='meshes'}),flush=True)

if __name__=='__main__':main()
