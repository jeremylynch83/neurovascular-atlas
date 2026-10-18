"""Independent geometry, invalidation and rejection regressions for authoring."""
import json,struct,sys,tempfile,unittest,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/repair'))
from cache import BVH,Scene,atomic_json
from geometry import triangle_crosses,triangle_crosses_exact,scan_network,patch_mesh,snap_seam
from validation import validate,ray_inside
from repair import LIMITS,execute

class ArrayScene:
    def __init__(self,meshes,systems=None):
        self.data=meshes;self.systems=systems or {k:'artery'for k in meshes};self.rows={n:{'bounds':[v.min(0).tolist(),v.max(0).tolist()]}for n,(v,f)in meshes.items()};self.indexes={}
    def mesh(self,n):return self.data[n]
    def nearby(self,lo,hi):return [n for n,r in self.rows.items()if np.all(np.array(r['bounds'][1])>=lo)and np.all(np.array(r['bounds'][0])<=hi)]
    def bvh(self,n):
        if n not in self.indexes:self.indexes[n]=BVH.build(*self.data[n])
        return self.indexes[n]

def tetra(scale=.1):
    v=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],dtype='<f4')*scale
    return v,np.array([[0,2,1],[0,1,3],[0,3,2],[1,2,3]],dtype='<u4')
def tube(low,high):
    a=np.arange(8)*np.pi/4;ring=np.c_[np.cos(a),np.sin(a),np.zeros(8)];v=np.vstack([ring+[0,0,z]for z in [low,(low+high)/2,high]]).astype('<f4');f=[]
    for k in range(2):
        for j in range(8):
            a=k*8+j;b=k*8+(j+1)%8;c=(k+1)*8+j;d=(k+1)*8+(j+1)%8;f.extend([[a,b,d],[a,d,c]])
    return v,np.array(f,dtype='<u4')
def fixture_glb(path,meshes):
    binary=bytearray();views=[];accessors=[];nodes=[];gmeshes=[]
    for name,(v,f)in meshes.items():
        ids=[]
        for data,kind,component in [(v.astype('<f4'),'VEC3',5126),(f.astype('<u4').ravel(),'SCALAR',5125)]:
            view=len(views);views.append({'buffer':0,'byteOffset':len(binary),'byteLength':data.nbytes});binary.extend(data.tobytes());a={'bufferView':view,'componentType':component,'count':len(data),'type':kind}
            if kind=='VEC3':a.update(min=v.min(0).tolist(),max=v.max(0).tolist())
            ids.append(len(accessors));accessors.append(a)
        nodes.append({'name':name,'mesh':len(gmeshes)});gmeshes.append({'primitives':[{'attributes':{'POSITION':ids[0]},'indices':ids[1]}]})
    doc={'asset':{'version':'2.0'},'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors,'nodes':nodes,'meshes':gmeshes,'scenes':[{'nodes':list(range(len(nodes)))}],'scene':0};j=json.dumps(doc).encode();j+=b' '*((-len(j))%4)
    path.write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary)
def fixture_app(root,meshes):
    p=root/'public/anatomy/models';p.mkdir(parents=True);(root/'tools/repair').mkdir(parents=True);(root/'tools/repair/decode.mjs').symlink_to(ROOT/'tools/repair/decode.mjs')
    fixture_glb(p/'fixture.glb',meshes);atomic_json(root/'public/anatomy/manifest.json',{'structures':[{'id':n,'system':'artery','asset':{'file':'models/fixture.glb','node':n}}for n in meshes]})

class GeometryTests(unittest.TestCase):
    def test_transverse_crossing(self):
        a=np.array([[0,0,0],[1,0,0],[0,1,0.]])
        self.assertTrue(triangle_crosses(a,np.array([[.2,.2,-1],[.2,.2,1],[.8,.2,0]])))
    def test_shared_vertex_does_not_hide_overlap(self):
        a=np.array([[0,0,0],[1,0,0],[0,1,0.]])
        self.assertTrue(triangle_crosses(a,np.array([[0,0,0],[.8,.2,0],[.2,.8,0]])))
        self.assertTrue(triangle_crosses(a,np.array([[0,0,0],[.5,.1,1],[.5,.1,-1]])))
    def test_shared_edge_allowed_but_coplanar_fold_rejected(self):
        a=np.array([[0,0,0],[1,0,0],[0,1,0.]])
        self.assertFalse(triangle_crosses(a,np.array([[1,0,0],[0,0,0],[0,-1,0]])))
        self.assertTrue(triangle_crosses(a,np.array([[1,0,0],[0,0,0],[.2,.2,0]])))
    def test_parallel_disjoint_and_tangent(self):
        a=np.array([[0,0,0],[1,0,0],[0,1,0.]])
        self.assertFalse(triangle_crosses(a,a+[0,0,.01]))
        self.assertFalse(triangle_crosses(a,np.array([[1,0,0],[2,0,0],[1,1,1]])))
    def test_a5_near_parallel_shared_vertex_regression(self):
        # Exact exported Float32 triangles formerly reported as a wall fold.
        a=np.array([[1.3587535619735718,-79.76895141601562,119.34420013427734],[1.3501044511795044,-80.09761810302734,119.31825256347656],[1.3544288873672485,-79.7948989868164,119.42204284667969]])
        b=np.array([[1.363078236579895,-79.46622467041016,119.44799041748047],[1.3544288873672485,-79.7948989868164,119.42204284667969],[1.3587535619735718,-79.49217224121094,119.52583312988281]])
        for order_a in itertools.permutations(range(3)):
            for order_b in itertools.permutations(range(3)):
                self.assertFalse(triangle_crosses(a[list(order_a)],b[list(order_b)]))
                self.assertFalse(triangle_crosses(b[list(order_b)],a[list(order_a)]))
        for scale in [2.**-10,1.,2.**10]:
            self.assertFalse(triangle_crosses(a*scale+[1024,-1024,512],b*scale+[1024,-1024,512]))
    def test_near_parallel_true_crossings_are_not_relaxed(self):
        a=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
        for height in [2.**-20,2.**-30,2.**-40]:
            b=np.array([[.25,.25,-height],[.75,.25,height],[.25,.75,height]])
            self.assertTrue(triangle_crosses(a,b))
            self.assertTrue(triangle_crosses(b[::-1],a[::-1]))
    def test_exact_parallel_gap_and_shared_edge_contacts(self):
        a=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
        self.assertFalse(triangle_crosses(a,a+[0.,0.,2.**-40]))
        self.assertFalse(triangle_crosses(a,np.array([[1.,0.,0.],[0.,0.,0.],[.25,-1.,2.**-40]])))
        # Even an extremely thin genuine coplanar overlap must fail.
        self.assertTrue(triangle_crosses(a,np.array([[0.,0.,0.],[1.,0.,0.],[.5,2.**-40,0.]])))
    def test_petrosal_tolerance_false_positives(self):
        rows=json.loads((Path(__file__).with_name('petrosal-predicate-fixtures.json')).read_text())
        false=[r for r in rows if not r['expected']]
        self.assertEqual(len(false),11)
        for row in false:
            a=np.array(row['a']);b=np.array(row['b'])
            for ia in itertools.permutations(range(3)):
                for ib in itertools.permutations(range(3)):
                    self.assertFalse(triangle_crosses(a[list(ia)],b[list(ib)]),row['faces'])
                    self.assertFalse(triangle_crosses(b[list(ib)],a[list(ia)]),row['faces'])
    def test_petrosal_genuine_crossings_survive_predicate_fix(self):
        rows=json.loads((Path(__file__).with_name('petrosal-predicate-fixtures.json')).read_text())
        positive=[r for r in rows if r['expected']]
        self.assertEqual(len(positive),22)
        for row in positive:
            a=np.array(row['a']);b=np.array(row['b'])
            for scale in [2.**-10,1.,2.**10]:
                aa=a*scale+[1024,-1024,512];bb=b*scale+[1024,-1024,512]
                self.assertTrue(triangle_crosses(aa,bb),row['faces'])
                self.assertTrue(triangle_crosses(bb[::-1],aa[::-1]),row['faces'])
    def test_degenerate_triangle_has_no_positive_area_crossing(self):
        a=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
        for b in [np.array([[0.,0.,0.],[0.,0.,0.],[1.,0.,0.]]),np.array([[0.,0.,0.],[.5,0.,0.],[1.,0.,0.]])]:
            self.assertFalse(triangle_crosses(a,b))
            self.assertFalse(triangle_crosses(b,a))
    def test_a5_distal_retained_contact_is_not_a_crossing(self):
        row=json.loads((Path(__file__).with_name('a5-distal-contact-fixture.json')).read_text())
        a=np.array(row['a']);b=np.array(row['b'])
        for ia in itertools.permutations(range(3)):
            for ib in itertools.permutations(range(3)):
                self.assertFalse(triangle_crosses(a[list(ia)],b[list(ib)]))
                self.assertFalse(triangle_crosses(b[list(ib)],a[list(ia)]))
    def test_filtered_predicate_matches_exact_for_conditioned_cases(self):
        rng=np.random.default_rng(114)
        for i in range(128):
            a=rng.uniform(-1,1,(3,3));b=rng.uniform(-1,1,(3,3))
            if i%2==0:a[:,2]*=2.**-35;b[:,2]*=2.**-35
            if i%3==0:b[0]=a[0]
            if i%5==0:b[:2]=a[:2]
            a+=np.array([64,-128,32]);b+=np.array([64,-128,32])
            expected=triangle_crosses_exact(a,b)
            self.assertEqual(triangle_crosses(a,b),expected,i)
            self.assertEqual(triangle_crosses(b[::-1],a[::-1]),expected,i)
    def test_bvh_matches_bruteforce_after_disk_roundtrip(self):
        rng=np.random.default_rng(44);v=rng.random((300,3));f=np.arange(300).reshape(-1,3);t=v[f]
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'tree.npz';BVH.build(v,f,leaf=4).save(p);tree=BVH.load(p)
            for _ in range(30):
                lo=rng.random(3)*.8;hi=lo+.1;expected=set(np.flatnonzero(np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1)));self.assertTrue(expected<=set(tree.query(lo,hi)))
    def test_nearest_distance_has_analytic_face_edge_and_vertex_answers(self):
        v=np.array([[0,0,0],[1,0,0],[0,1,0.]]);f=np.array([[0,1,2]]);tree=BVH.build(v,f)
        self.assertAlmostEqual(tree.nearest(np.array([.2,.2,2.]),v,f),2)
        self.assertAlmostEqual(tree.nearest(np.array([.5,-1,0.]),v,f),1)
        self.assertAlmostEqual(tree.nearest(np.array([-1,-1,0.]),v,f),2**.5)
    def test_gap_closes_without_moving_source(self):
        v,f=tetra();scene=ArrayScene({'child':(v,f[:1]),'parent':(v,f[1:3])});net={'id':'fixture','target':'child','nodes':['child','parent']}
        proposals=scan_network(scene,net,LIMITS);selected=[r for r in proposals if r['eligible']];self.assertEqual(len(selected),1)
        p,g,_=patch_mesh(scene,'child',selected);self.assertTrue(np.array_equal(p[:len(v)],v));self.assertTrue(np.array_equal(g[:1],f[:1]));self.assertEqual(len(g),2)
        r=validate(scene,{'child':(p,g)},[net],LIMITS);self.assertTrue(r['passed'],r)
    def test_single_label_opening_is_preserved(self):
        v,f=tetra();scene=ArrayScene({'child':(v,f[:3])});rows=scan_network(scene,{'id':'port','target':'child','nodes':['child']},LIMITS)
        self.assertFalse(any(r['eligible']for r in rows));self.assertIn('single-label-port-not-a-junction-gap',[r['reason']for r in rows])
    def test_intersecting_obstacle_rejects_patch(self):
        v,f=tetra();b=np.array([[.025,.025,-.01],[.025,.025,.15],[.08,.025,.06]],dtype='<f4');scene=ArrayScene({'child':(v,f[:1]),'parent':(v,f[1:3]),'obstacle':(b,np.array([[0,1,2]],dtype='<u4'))});net={'id':'gap','target':'child','nodes':['child','parent']};p,g,_=patch_mesh(scene,'child',[x for x in scan_network(scene,net,LIMITS)if x['eligible']]);r=validate(scene,{'child':(p,g)},[net],LIMITS);self.assertFalse(r['passed']);self.assertTrue(r['crossings'])
    def test_enclosed_patch_detects_tissue_without_surface_crossing(self):
        v,f=tetra(2);scene=ArrayScene({'tissue':(v-0.5,f)},{'tissue':'brain'});self.assertTrue(ray_inside(scene,'tissue',np.array([0.,0.,0.])));self.assertFalse(ray_inside(scene,'tissue',np.array([5.,5.,5.])))
    def test_snap_closes_explicit_rims(self):
        scene=ArrayScene({'child':tube(.02,2),'parent':tube(-2,0)});p,g,detail=snap_seam(scene,{'target':'child','parent':'parent'},LIMITS)
        self.assertLessEqual(detail['maximumDisplacementMm'],.020001);net={'id':'join','target':'child','nodes':['child','parent']};r=validate(scene,{'child':(p,g)},[net],LIMITS);self.assertTrue(r['passed'],r)
    def test_snap_refuses_large_registration_change(self):
        scene=ArrayScene({'child':tube(.2,2),'parent':tube(-2,0)})
        with self.assertRaisesRegex(ValueError,'registration'):snap_seam(scene,{'target':'child','parent':'parent'},LIMITS)
    def test_snap_protects_other_label_attachment(self):
        v,f=tube(.02,2);scene=ArrayScene({'child':(v,f),'parent':tube(-2,0),'attached':(v[:3],np.array([[0,1,2]],dtype='<u4'))})
        with self.assertRaisesRegex(ValueError,'another-native-attachment'):snap_seam(scene,{'target':'child','parent':'parent'},LIMITS)

class CacheAndLedgerTests(unittest.TestCase):
    def test_accepted_reuse_copies_files_and_detects_tampering(self):
        with tempfile.TemporaryDirectory()as d:
            root=Path(d);v,f=tetra();fixture_app(root/'app',{'child':(v,f[:1]),'parent':(v,f[1:3])});config={'schema':1,'networks':[{'id':'gap','target':'child','nodes':['child','parent']}]}
            a=execute(root/'app',config,root/'cache',root/'one');self.assertEqual(a['status'],'accepted')
            b=execute(root/'app',config,root/'cache',root/'two');self.assertTrue(b['reusedRecordedTrial']);self.assertTrue((root/'two/accepted-corrections.json').is_file());self.assertTrue((root/'two/candidate/child.positions.bin').is_file())
            p=Path(a['candidateFiles'][0]);p.write_bytes(b'0'*p.stat().st_size)
            c=execute(root/'app',config,root/'cache',root/'three');self.assertFalse(c['reusedRecordedTrial']);self.assertEqual(c['status'],'accepted')
    def test_content_invalidation_retains_unchanged_mesh_bvh(self):
        with tempfile.TemporaryDirectory()as d:
            root=Path(d);v,f=tetra();meshes={'a':(v,f),'b':(v+[3,0,0],f)};fixture_app(root/'app',meshes);cache=root/'cache';first=Scene(root/'app',cache);first.bvh('a');first.bvh('b');key=first.rows['b']['key']
            warm=Scene(root/'app',cache);warm.bvh('a');self.assertEqual(warm.stats['assetDecodes'],0);self.assertEqual(warm.stats['bvhCacheHits'],1)
            path=root/'app/public/anatomy/models/fixture.glb';size=path.stat().st_size;stamp=path.stat().st_mtime_ns
            changed=v.copy();changed[1,0]=.09;fixture_glb(path,{'a':(changed,f),'b':meshes['b']});self.assertEqual(path.stat().st_size,size)
            import os;os.utime(path,ns=(stamp,stamp))
            after=Scene(root/'app',cache);after.bvh('a');after.bvh('b');self.assertEqual(after.stats['assetDecodes'],1);self.assertEqual(after.rows['b']['key'],key);self.assertEqual(after.stats['bvhCacheHits'],1);self.assertEqual(after.stats['bvhBuilds'],1)
            (cache/'geometry'/after.rows['a']['key']/'indices.bin').unlink();recovered=Scene(root/'app',cache);self.assertEqual(recovered.stats['assetDecodes'],1)
    def test_rejected_trial_is_recorded_and_not_repeated(self):
        with tempfile.TemporaryDirectory()as d:
            root=Path(d);v,f=tetra();fixture_app(root/'app',{'child':(v,f[:3])});config={'schema':1,'networks':[{'id':'port','target':'child','nodes':['child']}]}
            a=execute(root/'app',config,root/'cache',root/'first');self.assertEqual(a['status'],'rejected');self.assertEqual(json.loads((root/'first/accepted-corrections.json').read_text())['accepted'],[])
            b=execute(root/'app',config,root/'cache',root/'second');self.assertTrue(b['reusedRecordedTrial']);self.assertEqual(b['status'],'rejected')
            self.assertEqual(len((root/'cache/trials/journal.jsonl').read_text().splitlines()),1)

if __name__=='__main__':unittest.main()
