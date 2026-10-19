"""Local GLB surgery: retain every untouched accessor and compressed buffer."""
from pathlib import Path
import base64,hashlib,json,struct,subprocess
import numpy as np

APP=Path(__file__).resolve().parents[2]
class Glb:
    def __init__(self,path):
        self.path=Path(path); b=self.path.read_bytes(); n=struct.unpack_from('<I',b,12)[0]
        self.doc=json.loads(b[20:20+n]); self.binary=bytearray(b[28+n:]); self.changed=set()
        self.decoded=None;self.pending=[]
        if any(v.get('extensions',{}).get('EXT_meshopt_compression') for v in self.doc['bufferViews']):
            self.decoded=subprocess.check_output(['node',str(APP/'tools/decode-meshopt-views.mjs'),str(self.path)])
        self.nodes={n['name']:n for n in self.doc['nodes'] if 'mesh' in n}
    def accessor(self,i):
        a=self.doc['accessors'][i];v=self.doc['bufferViews'][a['bufferView']]
        count={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        dtype=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5122:'<i2',5121:'u1',5120:'i1'}[a['componentType']])
        src=self.decoded if v.get('extensions',{}).get('EXT_meshopt_compression') else self.binary
        out=np.ndarray((a['count'],count),dtype=dtype,buffer=src,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',count*dtype.itemsize),dtype.itemsize)).copy()
        if a.get('normalized') and dtype.kind in 'iu':out=np.maximum(-1,out/np.iinfo(dtype).max)
        return out
    def mesh(self,name):
        n=self.nodes[name];pr=self.doc['meshes'][n['mesh']]['primitives'][0]
        assert not any(k in n for k in ['matrix','scale','translation','rotation']), name
        return self.accessor(pr['attributes']['POSITION']).astype(float),self.accessor(pr['indices']).reshape(-1,3).astype(np.int32),self.accessor(pr['attributes']['NORMAL']).astype(float)
    def add_accessor(self,a,target):
        a=np.ascontiguousarray(a);raw=a.tobytes()
        vi=len(self.doc['bufferViews']);self.doc['bufferViews'].append({'target':target})
        stride=a.shape[1]*a.dtype.itemsize if a.ndim>1 else a.dtype.itemsize
        self.pending.append((vi,{'bytes':base64.b64encode(raw).decode(),'count':len(a),'stride':stride,'mode':'ATTRIBUTES' if target==34962 else 'TRIANGLES'}))
        count=1 if a.ndim==1 else a.shape[1];ai=len(self.doc['accessors']);ac={'bufferView':vi,'componentType':5126 if a.dtype.kind=='f' else 5125,'count':len(a),'type':{1:'SCALAR',3:'VEC3'}[count]}
        if target==34962:ac.update(min=a.min(0).tolist(),max=a.max(0).tolist())
        self.doc['accessors'].append(ac);return ai
    def replace(self,name,p,f,n=None):
        if n is None:n=normals(p,f)
        pr=self.doc['meshes'][self.nodes[name]['mesh']]['primitives'][0]
        pr['attributes']['POSITION']=self.add_accessor(np.asarray(p,dtype='<f4'),34962)
        pr['attributes']['NORMAL']=self.add_accessor(np.asarray(n,dtype='<f4'),34962)
        pr['indices']=self.add_accessor(np.asarray(f,dtype='<u4').ravel(),34963)
        self.changed.add(name)
    def save(self):
        if self.pending:
            encoded=json.loads(subprocess.check_output(['node',str(APP/'tools/encode-meshopt-buffers.mjs')],input=json.dumps([r for _,r in self.pending]).encode()))
            fallback=next(i for i,b in enumerate(self.doc['buffers']) if b.get('extensions',{}).get('EXT_meshopt_compression',{}).get('fallback'))
            for (vi,row),data in zip(self.pending,encoded):
                raw=base64.b64decode(data);self.binary.extend(b'\0'*((-len(self.binary))%4));off=len(self.binary);self.binary.extend(raw)
                fb=self.doc['buffers'][fallback];logical=(fb['byteLength']+3)//4*4;size=row['count']*row['stride'];fb['byteLength']=logical+size
                view=self.doc['bufferViews'][vi];view.update(buffer=fallback,byteOffset=logical,byteLength=size)
                if row['mode']=='ATTRIBUTES':view['byteStride']=row['stride']
                view['extensions']={'EXT_meshopt_compression':{'buffer':0,'byteOffset':off,'byteLength':len(raw),'count':row['count'],'byteStride':row['stride'],'mode':row['mode']}}
        self.binary.extend(b'\0'*((-len(self.binary))%4));self.doc['buffers'][0]['byteLength']=len(self.binary)
        j=json.dumps(self.doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
        b=struct.pack('<4sII',b'glTF',2,28+len(j)+len(self.binary))+struct.pack('<II',len(j),0x4E4F534A)+j+struct.pack('<II',len(self.binary),0x004E4942)+self.binary
        self.path.write_bytes(b);return hashlib.sha256(b).hexdigest()
def normals(p,f):
    p=np.asarray(p);f=np.asarray(f);n=np.zeros_like(p,dtype=float);t=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
    for i in range(3):np.add.at(n,f[:,i],t)
    length=np.linalg.norm(n,axis=1);n/=np.maximum(length[:,None],1e-20);return n
