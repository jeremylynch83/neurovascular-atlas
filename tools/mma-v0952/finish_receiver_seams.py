"""Repair only generated receiver seams, preserving every native opening.

This stays a private candidate. Source intersections are retained by exact
triangle-coordinate provenance; all newly introduced intersections are fatal.
"""
from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
m=ast.parse((Path(__file__).parents[1]/'mma-v0953/geometry.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef) and x.name in ['arrays','rings']],type_ignores=[]),'geometry','exec'))
m=ast.parse((Path(__file__).parent/'self_check.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef) and x.name=='intersections'],type_ignores=[]),'self_check','exec'))

def edge_report(f):
    e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
    e,c=np.unique(e,axis=0,return_counts=True)
    return e[c==1],int(np.sum(c>2))

def welded(v,f):
    # Exact float32 coordinate welding retains original collar coordinates.
    v,inv=np.unique(v.astype('<f4'),axis=0,return_inverse=True);f=inv[f]
    take=np.array([len(set(x))==3 for x in f]);f=f[take]
    return v.astype(float),f

def triangle_keys(v,f):
    v=v.astype('<f4');out=[]
    for face in f:
        p=v[face];p=p[np.lexsort((p[:,2],p[:,1],p[:,0]))];out.append(p.tobytes())
    return out

reports=[]
for side in ['right','left']:
    n='vein.sphenoparietal.'+side;sv,sf=load(n);sv,sf=welded(sv,sf)
    sb,_=edge_report(sf);native=sv[np.unique(sb)];tree=cKDTree(native)
    x=np.load(OUT/('receiver-implicit-union-'+side+'.npz'));v,f=welded(x['v'],x['f'])
    bd,_=edge_report(f);generated=bd[np.any(tree.query(v[bd].reshape(-1,3))[0].reshape(-1,2)>1e-5,axis=1)]
    ids=np.unique(generated);loops=rings(v,f,ids)
    caps=[]
    directed=set(map(tuple,np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]).tolist()))
    for loop in loops:
        p=v[loop];diameter=float(np.linalg.norm(np.ptp(p,axis=0)))
        assert diameter<1.5,'Refusing to cap a large or unidentified boundary'
        if diameter<.001:
            # FlyingEdges' float32 near-zero slivers are collapsed locally.
            # No native collar vertex is in these generated seam loops.
            assert tree.query(p)[0].min()>1e-5
            f[np.isin(f,loop)]=loop[0]
            f=f[np.array([len(set(face))==3 for face in f])]
            caps.append(dict(vertices=len(loop),diameterMm=diameter,centreMm=p.mean(0).tolist(),method='Generated sub-micron seam collapse'))
            continue
        # VTK triangulates this actual boundary, rather than adding an
        # unconstrained centroid fan across a non-planar receiver seam.
        points=vtk.vtkPoints();points.SetData(numpy_to_vtk(p,deep=True))
        line=vtk.vtkPolyLine();line.GetPointIds().SetNumberOfIds(len(loop)+1)
        for j in range(len(loop)+1):line.GetPointIds().SetId(j,j%len(loop))
        lines=vtk.vtkCellArray();lines.InsertNextCell(line)
        contour=vtk.vtkPolyData();contour.SetPoints(points);contour.SetLines(lines)
        tri=vtk.vtkContourTriangulator();tri.SetInputData(contour);tri.Update()
        cf=vtk_to_numpy(tri.GetOutput().GetPolys().GetData()).reshape(-1,4)[:,1:]
        assert len(cf)==len(loop)-2,'Boundary triangulation incomplete'
        cf=loop[cf]
        a,b=int(loop[0]),int(loop[1]);edge=next((tuple(face[j:j+2]) for face in cf for j in [0,1] if set(face[j:j+2])=={a,b}),None)
        if edge is None:
            edge=next(((int(face[2]),int(face[0])) for face in cf if {int(face[2]),int(face[0])}=={a,b}),None)
        assert edge is not None
        if edge in directed:cf=cf[:,[1,0,2]]
        f=np.vstack([f,cf]);caps.append(dict(vertices=len(loop),diameterMm=diameter,centreMm=p.mean(0).tolist()))
    bd,non=edge_report(f)
    gap=cKDTree(v).query(native)[0]
    # Compare boundary edges by coordinates, including the touching left collar.
    def boundary_keys(v,e):
        return {tuple(sorted((v[a].astype('<f4').tobytes(),v[b].astype('<f4').tobytes()))) for a,b in e}
    exact=boundary_keys(v,bd)==boundary_keys(sv,sb)
    con=vtk.vtkPolyDataConnectivityFilter();con.SetInputData(poly(v,f));con.SetExtractionModeToAllRegions();con.Update()
    before=intersections(sv,sf);after=intersections(v,f)
    sk=triangle_keys(sv,sf);vk=triangle_keys(v,f)
    original={tuple(sorted((sk[a],sk[b]))) for a,b in before}
    new=[(a,b) for a,b in after if tuple(sorted((vk[a],vk[b]))) not in original]
    row=dict(side=side,boundaryEdges=len(bd),baselineBoundaryEdges=len(sb),nativeBoundaryEdgesExact=exact,nativeCollarMismatchMm=float(gap.max()),nonManifoldEdges=non,components=int(con.GetNumberOfExtractedRegions()),sourceIntersectionPairs=len(before),candidateIntersectionPairs=len(after),newIntersectionPairs=len(new),newPairs=new[:30],generatedSeamCaps=caps,passed=exact and non==0 and con.GetNumberOfExtractedRegions()==1 and not new)
    np.savez(OUT/('receiver-seam-completed-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'))
    reports.append(row);print(json.dumps(row),flush=True)
(OUT/'receiver-seam-validation.json').write_text(json.dumps(reports,indent=2))
