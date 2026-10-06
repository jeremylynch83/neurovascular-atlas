"""Move paired posterior spinal origins to PICA with actual ostium surgery."""
import json,numpy as np,trimesh,vtk,manifold3d as mf
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.interpolate import PchipInterpolator
from fit_vessels import APP,read_glb,mesh_records,resample
from refine_context_skin import save_replaced
from rebuild_tubular_brainstem_veins import tube
from fit_expanded_pial_vessels import OUT,SRC,ExposedSurface,fit_course
from reconcile_brainstem import sha

def boundary(mesh):
    f=mesh.faces;directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);e=np.sort(directed,axis=1);_,idx,count=np.unique(e,axis=0,return_index=True,return_counts=True)
    assert count.max()<=2,'Nonmanifold source edge'
    return directed[idx[count==1]]

def capped(mesh,ids):
    mesh=mesh.copy();mesh.merge_vertices(digits_vertex=5);v=mesh.vertices.copy();f=mesh.faces.copy();edges=boundary(mesh);caps=[]
    if len(edges):
        G=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False)
        for c in np.unique(cc[edges.ravel()]):
            edge=edges[cc[edges[:,0]]==c];points=np.unique(edge);centre=v[points].mean(0);ci=len(v);v=np.vstack([v,centre]);caps.append(np.column_stack([edge[:,1],edge[:,0],np.full(len(edge),ci)]))
    original_faces=len(f);f=np.vstack([f,*caps]) if caps else f
    runs=np.array([0,original_faces*3,len(f)*3],np.uint32) if caps else np.array([0,len(f)*3],np.uint32)
    solid=mf.Manifold(mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=runs,run_original_id=np.array(ids if caps else ids[:1],np.uint32)))
    assert solid.status()==mf.Error.NoError,str(solid.status())
    return solid

def close_old_root(current,source,old_psa):
    v0=source['old'];_,idx,inv=np.unique(np.round(v0,5),axis=0,return_index=True,return_inverse=True);v=current['old'][idx];f=inv[source['faces']];m=trimesh.Trimesh(v,f,process=False);edges=boundary(m)
    G=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False);near=cKDTree(old_psa['old']);count=0
    for c in np.unique(cc[edges.ravel()]):
        edge=edges[cc[edges[:,0]]==c];points=np.unique(edge);d=near.query(v0[idx[points]])[0]
        if (d<2e-5).mean()<.85:continue
        ci=len(v);centre=v[points].mean(0);v=np.vstack([v,centre]);f=np.vstack([f,np.column_stack([edge[:,1],edge[:,0],np.full(len(edge),ci)])]);count+=1
    assert count==1,('Expected one old spinal origin',count)
    return trimesh.Trimesh(v,f,process=False)

def main():
    d,b=read_glb(OUT/'arteries-trial.glb');rr=mesh_records(d,b);sd,sb=read_glb(SRC/'arteries-trial.glb');old=mesh_records(sd,sb)
    brain=trimesh.load(OUT/'brain-trial.glb',process=False);med=trimesh.util.concatenate([brain.geometry['brain.medulla-oblongata.'+s] for s in ['left','right']]+[brain.geometry['brain.upper-cervical-cord']]);posterior=ExposedSurface(med)
    rows=json.loads((OUT/'arteries-pial-courses.json').read_text());replacements={};report=[]
    for side,sign in [('left',-1),('right',1)]:
        pk='PICA '+side;sk='Posterior spinal '+side;vk='Vertebral V3 '+side
        source=np.array(rows[pk]['sourcePoints']);course=np.array(rows[pk]['points']);va=cKDTree(old['Vertebral V4 '+side]['old']);ends=va.query(source[[0,-1]])[0];from_start=ends[0]<ends[1];i=int(.16*(len(course)-1)) if from_start else int(.84*(len(course)-1));origin=course[i].copy()
        radius=.235;z0=min(32.,origin[2]-3.);xlat=.65+sign*max(11.5,abs(origin[0]-.65));rear=posterior.hit(np.array([xlat,origin[1],z0]),1,-1)
        if rear is None:rear=posterior.hit(np.array([.65+sign*4.,origin[1],z0]),1,-1)
        assert rear is not None,'Missing dorsal medullary witness'
        knots=[origin,origin+np.array([sign*1.2,-1.5,-1.5]),np.array([xlat,rear-radius-.03,z0])]
        for z in np.linspace(z0-1.,-30.,140):
            x=.65+sign*(4.+7.5*np.exp(-(z0-z)/4.));query=np.array([x,-85.,z]);y=posterior.hit(query,1,-1)
            if y is None:y=-91.
            knots.append(np.array([x,y-radius-.025,z]))
        q=resample(np.array(knots),210);r=np.linspace(.235,.175,len(q))
        # Keep the route on the posterior skin after smoothing, including the
        # side-to-dorsal approach around the medulla.
        q=fit_course(q,r,posterior,iterations=4);q[0]=origin
        for j in range(12):q[j]+= (origin-q[0])*(1-j/12)**2
        for j in range(25,len(q)):
            y=posterior.hit(q[j],1,-1)
            if y is not None:q[j,1]=y-r[j]-.025
        v,f=tube(q,r,sides=40);psa=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([102],np.uint32)))
        assert psa.status()==mf.Error.NoError
        parent=capped(trimesh.Trimesh(rr[pk]['old'],rr[pk]['faces'],process=False),[100,101]);joined=parent+psa;assert joined.status()==mf.Error.NoError
        mesh=joined.to_mesh();vv=np.array(mesh.vert_properties[:,:3]);ff=np.array(mesh.tri_verts);labels=np.zeros(len(ff),int)
        for j,oid in enumerate(mesh.run_original_id):labels[mesh.run_index[j]//3:mesh.run_index[j+1]//3]=oid
        for key,tag in [(pk,100),(sk,102)]:
            faces=ff[labels==tag];used,inv=np.unique(faces,return_inverse=True);m=trimesh.Trimesh(vv[used],inv.reshape(-1,3),process=False);replacements[key]=(m.vertices,m.faces,m.vertex_normals)
        sealed=close_old_root(rr[vk],old[vk],old[sk]);replacements[vk]=(sealed.vertices,sealed.faces,sealed.vertex_normals)
        report.append({'side':side,'parent':pk,'proximalFractionFromPicaOrigin':.16,'origin':origin.tolist(),'points':q.tolist(),'radii':r.tolist(),'oldV3OstiumClosed':True,'newPicaOstiumBooleanUnion':'NoError','calibreMm':[.47,.35]});print('Rebuilt PICA origin and posterior course',side,flush=True)
    save_replaced(OUT/'arteries-spinal.glb',d,b,replacements);(OUT/'arteries-spinal.glb').replace(OUT/'arteries-trial.glb')
    (OUT/'posterior-spinal-courses.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest=json.loads((APP/'public/anatomy/manifest.json').read_text());lookup={r['name']:r for r in manifest['structures']}
    for side in ['left','right']:
        row=lookup['Posterior spinal '+side];parent=lookup['PICA '+side];old_parent=next(r for r in manifest['structures'] if r['id']==row['parent']);old_parent['children']=[k for k in old_parent['children'] if k!=row['id']];parent['children']=list(dict.fromkeys(parent['children']+[row['id']]));row['parent']=parent['id']
        for rel in manifest['relationships']:
            if rel.get('to')==row['id'] and rel.get('type')=='branches_to':rel['from']=parent['id']
        row['notes']='Representative PICA-origin variant. Posterolateral medullary and upper-cervical surface course.'
        vc=row['vesselCourse'];vc['scope']='intracranial-and-upper-cervical';vc['attachments']['parentId']=parent['id'];vc['attachments']['incoming']=[{'from':parent['id'],'to':row['id'],'type':'branches_to'}];vc['reviewStatus']='candidate-geometry-verified';vc['targetStructureIds']=['brain.medulla-oblongata.'+side,'brain.upper-cervical-cord'];vc['geometrySha256']=sha(OUT/'arteries-trial.glb')
        vc['summary']='Arises from proximal PICA, curves around the lateral medulla, then descends on the posterior medullary and upper-cervical pial contour.'
    template=copy_row=next(r for r in manifest['structures'] if r['id']=='brain.medulla-oblongata.right')
    import copy
    cord=copy.deepcopy(template);cord.update(id='brain.upper-cervical-cord',name='Upper cervical cord',side='midline',children=[],description='Illustrative continuation of the registered caudal medullary contour for spinal arterial orientation.');cord['asset']['node']=cord['id'];cord.pop('vesselCourse',None);manifest['structures'].append(cord)
    manifest['candidateDirectory']='posterior-pial56';(OUT/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    trial=json.loads((OUT/'trial.json').read_text());trial['posteriorSpinalOrigins']='proximal PICA bilaterally';trial['hashes']={k:sha(OUT/f'{k}-trial.glb') for k in ['brain','arteries','veins']};(OUT/'trial.json').write_text(json.dumps(trial,indent=2)+'\n')

if __name__=='__main__':main()
