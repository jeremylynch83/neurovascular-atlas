"""Immutable decoded buffers and lazy, persistent triangle BVHs.

Assets are hashed on every command. Spatial data are keyed by decoded geometry,
so changing one label does not invalidate the other labels' collision indexes.
"""
from pathlib import Path
from contextlib import contextmanager
import hashlib,json,os,subprocess,uuid,fcntl,heapq
import numpy as np

SCHEMA=1
def digest(data): return hashlib.sha256(data).hexdigest()
def file_hash(path):
    h=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_text(json.dumps(value,indent=2)+'\n');os.replace(temp,path)
@contextmanager
def locked(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        try:yield
        finally:fcntl.flock(stream,fcntl.LOCK_UN)

class BVH:
    """Median-split triangle AABB hierarchy, saved as arrays rather than pickle."""
    def __init__(self,lo,hi,left,right,start,count,order):
        self.lo,self.hi,self.left,self.right,self.start,self.count,self.order=lo,hi,left,right,start,count,order
    @classmethod
    def build(cls,v,f,leaf=32):
        t=v[f];lo=t.min(1);hi=t.max(1);cent=(lo+hi)/2
        order=np.arange(len(f),dtype=np.int64);nlo=[];nhi=[];left=[];right=[];start=[];count=[]
        def node(a,b):
            i=len(left);ids=order[a:b];nlo.append(lo[ids].min(0));nhi.append(hi[ids].max(0));left.append(-1);right.append(-1);start.append(a);count.append(b-a)
            if b-a>leaf:
                axis=int(np.ptp(cent[ids],axis=0).argmax());mid=(a+b)//2
                order[a:b]=ids[np.argpartition(cent[ids,axis],mid-a)]
                left[i]=node(a,mid);right[i]=node(mid,b);count[i]=0
            return i
        node(0,len(f));return cls(np.array(nlo),np.array(nhi),np.array(left),np.array(right),np.array(start),np.array(count),order)
    def query(self,lo,hi):
        found=[];stack=[0]
        while stack:
            i=stack.pop()
            if np.any(self.hi[i]<lo)or np.any(self.lo[i]>hi):continue
            if self.count[i]:found.extend(self.order[self.start[i]:self.start[i]+self.count[i]])
            else:stack.extend([int(self.left[i]),int(self.right[i])])
        return np.array(found,dtype=np.int64)
    def nearest(self,point,v,f):
        def bound(i):return float(np.square(np.maximum(np.maximum(self.lo[i]-point,point-self.hi[i]),0)).sum())
        best=float('inf');todo=[(bound(0),0)]
        while todo:
            lower,i=heapq.heappop(todo)
            if lower>=best:continue
            if not self.count[i]:
                for child in [int(self.left[i]),int(self.right[i])]:heapq.heappush(todo,(bound(child),child))
                continue
            ids=self.order[self.start[i]:self.start[i]+self.count[i]];t=np.asarray(v[f[ids]],dtype=float)
            # Distance to the three closed edges, plus the orthogonal face
            # projection where its barycentric coordinates lie inside.
            distances=[]
            for a,b in [(0,1),(1,2),(2,0)]:
                edge=t[:,b]-t[:,a];den=np.einsum('ij,ij->i',edge,edge);u=np.einsum('ij,ij->i',point-t[:,a],edge)/np.maximum(den,1e-30);q=t[:,a]+np.clip(u,0,1)[:,None]*edge;distances.append(np.square(q-point).sum(1))
            a=t[:,1]-t[:,0];b=t[:,2]-t[:,0];x=point-t[:,0];aa=(a*a).sum(1);ab=(a*b).sum(1);bb=(b*b).sum(1);ax=(a*x).sum(1);bx=(b*x).sum(1);den=aa*bb-ab*ab;safe=np.where(np.abs(den)>1e-30,den,1);u=(bb*ax-ab*bx)/safe;w=(aa*bx-ab*ax)/safe;inside=(np.abs(den)>1e-30)&(u>=0)&(w>=0)&(u+w<=1);q=t[:,0]+u[:,None]*a+w[:,None]*b;distances.append(np.where(inside,np.square(q-point).sum(1),np.inf));best=min(best,float(np.min(distances)))
        return best**.5
    def save(self,path):
        temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
        with temp.open('wb') as f:np.savez(f,lo=self.lo,hi=self.hi,left=self.left,right=self.right,start=self.start,count=self.count,order=self.order,schema=SCHEMA)
        os.replace(temp,path)
    @classmethod
    def load(cls,path):
        with np.load(path,allow_pickle=False) as data:
            if int(data['schema'])!=SCHEMA:raise ValueError('BVH schema')
            return cls(*(data[k] for k in ['lo','hi','left','right','start','count','order']))

class Scene:
    def __init__(self,app,root,overrides=None):
        self.app=Path(app).resolve();self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
        self.stats={'assetCacheHits':0,'assetDecodes':0,'bvhCacheHits':0,'bvhBuilds':0,'namedMeshes':0}
        self.rows={};self.source_hashes={};self.loaded={};self.indexes={}
        manifest=json.loads((self.app/'public/anatomy/manifest.json').read_text())
        self.manifest_hash=digest(json.dumps([(s['id'],s['system'],s['asset'])for s in manifest['structures']if s.get('asset')],sort_keys=True).encode())
        files=sorted({s['asset']['file'] for s in manifest['structures'] if s.get('asset')})
        self.systems={s['asset']['node']:s['system'] for s in manifest['structures'] if s.get('asset')}
        for asset in files:
            source=self.app/'public/anatomy'/asset;h=file_hash(source);self.source_hashes[asset]=h
            record=self.root/'assets'/f'{SCHEMA}-{h}.json'
            with locked(record.with_suffix('.lock')):
                data=None
                if record.exists():
                    try:
                        candidate=json.loads(record.read_text())
                        if candidate['schema']==SCHEMA and candidate['sourceSha256']==h and all(self._valid_row(r) for r in candidate['meshes']):data=candidate
                    except (ValueError,KeyError,OSError):pass
                if data is None:
                    temp=record.with_name(record.name+'.'+uuid.uuid4().hex+'.tmp')
                    try:
                        subprocess.run(['node',str(self.app/'tools/repair/decode.mjs'),str(source),str(self.root),str(temp)],check=True,capture_output=True,text=True)
                        data=json.loads(temp.read_text());assert data['sourceSha256']==h and all(self._valid_row(r) for r in data['meshes']);os.replace(temp,record)
                    finally:temp.unlink(missing_ok=True)
                    self.stats['assetDecodes']+=1
                else:self.stats['assetCacheHits']+=1
            for row in data['meshes']:
                if row['name'] in self.rows:raise ValueError('Duplicate mesh name')
                self.rows[row['name']]={**row,'asset':asset}
        # Replay fixtures or explicit authoring baselines. Never modify the GLB.
        self.overrides={}
        for name,entry in (overrides or {}).items():
            if name not in self.rows:raise ValueError('Unknown override '+name)
            paths=[self.app/entry[k] for k in ['positions','indices']]
            for k,p in zip(['positionSha256','indicesSha256'],paths):
                if file_hash(p)!=entry[k]:raise ValueError('Override hash mismatch '+name)
            v=np.fromfile(paths[0],'<f4').reshape(-1,3);f=np.fromfile(paths[1],'<u4').reshape(-1,3)
            if not np.isfinite(v).all() or f.max()>=len(v):raise ValueError('Invalid override')
            key=digest(v.tobytes()+f.tobytes());folder=self.root/'geometry'/key;folder.mkdir(parents=True,exist_ok=True)
            for filename,data in [('positions.bin',v.tobytes()),('indices.bin',f.tobytes())]:
                p=folder/filename
                if not p.exists():p.write_bytes(data)
            self.rows[name]={**self.rows[name],'key':key,'vertices':len(v),'triangles':len(f),'bounds':[v.min(0).tolist(),v.max(0).tolist()]}
            self.overrides[name]=key
        self.stats['namedMeshes']=len(self.rows)
        self.names=list(self.rows);self.lo=np.array([self.rows[n]['bounds'][0] for n in self.names]);self.hi=np.array([self.rows[n]['bounds'][1] for n in self.names])
    def _valid_row(self,r):
        d=self.root/'geometry'/r['key']
        return all((d/n).is_file() and (d/n).stat().st_size==s for n,s in [('positions.bin',r['vertices']*12),('indices.bin',r['triangles']*12)])
    def mesh(self,name):
        if name not in self.loaded:
            r=self.rows[name];d=self.root/'geometry'/r['key']
            self.loaded[name]=(np.memmap(d/'positions.bin',dtype='<f4',mode='r',shape=(r['vertices'],3)),np.memmap(d/'indices.bin',dtype='<u4',mode='r',shape=(r['triangles'],3)))
        return self.loaded[name]
    def nearby(self,lo,hi):return [self.names[i] for i in np.flatnonzero(np.all(self.hi>=lo,axis=1)&np.all(self.lo<=hi,axis=1))]
    def bvh(self,name):
        if name not in self.indexes:
            path=self.root/'geometry'/self.rows[name]['key']/f'bvh-{SCHEMA}.npz'
            with locked(path.with_suffix('.lock')):
                tree=None
                if path.exists():
                    try:tree=BVH.load(path)
                    except (ValueError,KeyError,OSError):pass
                if tree is None:tree=BVH.build(*self.mesh(name));tree.save(path);self.stats['bvhBuilds']+=1
                else:self.stats['bvhCacheHits']+=1
            self.indexes[name]=tree
        return self.indexes[name]
    def volume_topology(self,name):
        from geometry import edge_table
        path=self.root/'geometry'/self.rows[name]['key']/'volume-topology-1.json'
        with locked(path.with_suffix('.lock')):
            if path.exists():return json.loads(path.read_text())
            _,_,counts,balance,_,_=edge_table(*self.mesh(name))
            result={'closedOrientedManifold':bool(np.all(counts==2)and np.all(balance==0)),
                    'boundaryEdges':int(sum(counts==1)),'nonManifoldEdges':int(sum(counts>2)),
                    'misorientedEdges':int(sum((counts==2)&(balance!=0)))}
            atomic_json(path,result);return result
    @property
    def fingerprint(self):return digest(json.dumps({'assets':self.source_hashes,'overrides':self.overrides,'manifestBindings':self.manifest_hash},sort_keys=True).encode())
