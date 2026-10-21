#!/usr/bin/env python3
"""Lossless GLB packaging. Copy encoded buffer views, never decode/re-encode.
The complete source GLBs and their manifest bindings remain authoritative.
"""
import copy, hashlib, json, re, struct, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'public/anatomy'
def sha(b): return hashlib.sha256(b).hexdigest()
def compact(x): return json.dumps(x,separators=(',',':'),ensure_ascii=False).encode()
def write_changed(p,b):
    if not p.exists() or p.read_bytes()!=b: p.write_bytes(b)
def read_glb(p):
    b=p.read_bytes(); magic,version,total=struct.unpack_from('<4sII',b)
    assert magic==b'glTF' and version==2 and total==len(b),p
    n,t=struct.unpack_from('<II',b,12); assert t==0x4e4f534a
    doc=json.loads(b[20:20+n]); off=20+n
    length,kind=struct.unpack_from('<II',b,off);assert kind==0x004e4942
    return doc,b[off+8:off+8+length]
def glb(doc,blob):
    j=compact(doc);j+=b' '*((-len(j))%4);blob+=b'\0'*((-len(blob))%4)
    return struct.pack('<4sII',b'glTF',2,28+len(j)+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob

def extract(doc,blob,names):
    # Current source assets are flat geometry-only scenes. Fail explicitly if
    # authoring introduces unsupported dependencies rather than losing data.
    assert not any(k in doc for k in ['skins','animations','images','textures'])
    assert not any('children' in n or 'skin' in n for n in doc['nodes'])
    nodes=[copy.deepcopy(n) for n in doc['nodes'] if n.get('name') in names]
    assert len(nodes)==len(names),'Missing or duplicate pack nodes'
    accessors=[];views=[];meshes=[];out=bytearray();fallback=0;amap={};vmap={};mmap={}
    def view(i):
        nonlocal fallback
        if i in vmap:return vmap[i]
        v=copy.deepcopy(doc['bufferViews'][i]);ext=v.get('extensions',{}).get('EXT_meshopt_compression')
        out.extend(b'\0'*((-len(out))%4))
        if ext:
            assert ext['buffer']==0
            start=ext.get('byteOffset',0);payload=blob[start:start+ext['byteLength']]
            ext['byteOffset']=len(out);out.extend(payload)
            v['buffer']=1;v['byteOffset']=fallback;fallback+=v['byteLength'];fallback+=(-fallback)%4
        else:
            assert v['buffer']==0
            start=v.get('byteOffset',0);payload=blob[start:start+v['byteLength']]
            v['byteOffset']=len(out);out.extend(payload)
        vmap[i]=len(views);views.append(v);return vmap[i]
    def accessor(i):
        if i in amap:return amap[i]
        a=copy.deepcopy(doc['accessors'][i]);assert 'sparse' not in a
        if 'bufferView' in a:a['bufferView']=view(a['bufferView'])
        amap[i]=len(accessors);accessors.append(a);return amap[i]
    for n in nodes:
        old=n['mesh']
        if old not in mmap:
            m=copy.deepcopy(doc['meshes'][old])
            for p in m['primitives']:
                assert not p.get('extensions'),'Unsupported primitive extension'
                p['attributes']={k:accessor(v) for k,v in p['attributes'].items()}
                if 'indices' in p:p['indices']=accessor(p['indices'])
                for target in p.get('targets',[]):
                    for k,v in target.items():target[k]=accessor(v)
            mmap[old]=len(meshes);meshes.append(m)
        n['mesh']=mmap[old]
    buffers=[{'byteLength':len(out)}]
    if fallback:buffers.append({'byteLength':fallback,'extensions':{'EXT_meshopt_compression':{'fallback':True}}})
    result={k:copy.deepcopy(doc[k]) for k in ['asset','materials','extensionsUsed','extensionsRequired'] if k in doc}
    result.update(scene=0,scenes=[{'nodes':list(range(len(nodes)))}],nodes=nodes,meshes=meshes,buffers=buffers,bufferViews=views,accessors=accessors)
    return glb(result,bytes(out))

def dependency_hash(doc,blob,names):
    """Ignore unrelated buffer offsets and accessor numbering in source files."""
    cache={}
    def accessor(i):
        if i in cache:return cache[i]
        a=copy.deepcopy(doc['accessors'][i]);assert 'sparse' not in a
        if 'bufferView' in a:
            v=copy.deepcopy(doc['bufferViews'][a.pop('bufferView')]);ext=v.get('extensions',{}).get('EXT_meshopt_compression')
            storage=ext or v;assert storage['buffer']==0
            start=storage.get('byteOffset',0);payload=blob[start:start+storage['byteLength']]
            storage.pop('byteOffset',None);storage.pop('buffer',None)
            if ext:v.pop('byteOffset',None);v.pop('buffer',None)
            a['view']=v;a['payloadHash']=sha(payload)
        cache[i]=a;return a
    nodes=[]
    for n in doc['nodes']:
        if n.get('name') not in names:continue
        row=copy.deepcopy(n);mesh=copy.deepcopy(doc['meshes'][row.pop('mesh')])
        for p in mesh['primitives']:
            p['attributes']={k:accessor(v) for k,v in p['attributes'].items()}
            if 'indices' in p:p['indices']=accessor(p['indices'])
            for target in p.get('targets',[]):
                for k,v in target.items():target[k]=accessor(v)
        row['geometry']=mesh;nodes.append(row)
    return sha(compact({'generator':sha(Path(__file__).read_bytes()),'nodes':nodes,'materials':doc.get('materials'),'extensions':doc.get('extensionsRequired')}))

def group(s):
    i=s['id']
    if s.get('displayGroup')=='anastomoses':
        return 3,'anastomoses'
    if (re.search(r'(common_carotid|internal_carotid.*\.segment\.|vertebral.*\.segment\.|\.basilar$|\.aca_a1_|\.mca_m1_|\.pca_p1_|posterior_communicating_|anterior_communicating)',i)
        or i.startswith('artery.carotid.external.')):return 0,'starter'
    if re.search(r'(aca_pericallosal.*\.segment\.|mca_(superior|inferior)_division|\.pca_p[2-4]_|\.pica_.*\.segment\.|\.aica_|\.sca_|\.ophthalmic_|\.anterior_choroidal_)',i):return 1,'main-branches'
    region='external' if '.eca.' in i else 'posterior' if '.posterior.' in i else 'anterior' if '.anterior.' in i else 'other'
    return 2,region+'-'+s['side']

def main():
    started=time.perf_counter();m=json.loads((BASE/'manifest.json').read_text());directory=BASE/'packs';directory.mkdir(exist_ok=True)
    arterial=[s for s in m['structures'] if s.get('asset') and s['system']=='artery']
    files=sorted({s['asset']['file'] for s in arterial})
    source_hashes={f:sha((BASE/f).read_bytes()) for f in files}
    key=sha(compact({'generator':sha(Path(__file__).read_bytes()),'sources':source_hashes,'rows':[(s['id'],s['asset'],s['side'],s.get('displayGroup')) for s in arterial],'skull':m['assetRevisions']['models/craniofacial.glb']}))
    index_path=directory/'index.json';index=json.loads(index_path.read_text()) if index_path.exists() else {}
    reused=0;built=0;assembled=0
    if index.get('inputHash')==key and all((BASE/p['file']).exists() and sha((BASE/p['file']).read_bytes())==p['sha256'] for p in index['packs']):
        packs=index['packs'];reused=len(packs)
    else:
        sources={f:read_glb(BASE/f) for f in files};groups={}
        for s in arterial:
            stage,name=group(s);groups.setdefault((stage,name,s['asset']['file']),[]).append(s)
        packs=[]
        previous={(p['stage'],p.get('name'),p['source']):p for p in index.get('packs',[])}
        for (stage,name,source),rows in sorted(groups.items()):
            names={s['asset']['node'] for s in rows}
            dependency=dependency_hash(*sources[source],names)
            old=previous.get((stage,name,source))
            if old and old.get('dependencyHash')==dependency and (BASE/old['file']).exists() and sha((BASE/old['file']).read_bytes())==old['sha256']:
                packs.append({**old,'ids':[s['id'] for s in rows]});reused+=1;continue
            assembled+=1
            data=extract(*sources[source],{s['asset']['node'] for s in rows});h=sha(data)
            # Content addressing keeps unaffected packs stable after an edit.
            file=f'packs/{stage}-{name}-{h[:20]}.glb';p=BASE/file
            if p.exists() and sha(p.read_bytes())==h:reused+=1
            else:write_changed(p,data);built+=1
            packs.append({'file':file,'stage':stage,'ids':[s['id'] for s in rows],'sha256':h,'bytes':len(data),'source':source,'name':name,'dependencyHash':dependency})
        index={'schema':1,'inputHash':key,'sourceHashes':source_hashes,'packs':packs}
        write_changed(index_path,compact(index)+b'\n')
        keep={Path(p['file']).name for p in packs}
        for p in directory.glob('*.glb'):
            if p.name not in keep:p.unlink()
    # Prune stale generated files even when all active outputs were cached.
    keep={Path(p['file']).name for p in packs}
    for p in directory.glob('*.glb'):
        if p.name not in keep:p.unlink()
    for field in ['assetRevisions','assetByteSizes']:
        m[field]={k:v for k,v in m[field].items() if not k.startswith('packs/')}
    # Retain original asset bindings for DSA and authoring. Only the loader
    # consults this download plan, so packing never changes anatomical hashes.
    m['loadingPacks']=[{k:p[k] for k in ['file','stage','ids']} for p in packs]
    for p in packs:m['assetRevisions'][p['file']]=p['sha256'][:20];m['assetByteSizes'][p['file']]=p['bytes']
    d,_=read_glb(BASE/'models/craniofacial.glb');lo=[float('inf')]*3;hi=[-float('inf')]*3
    for n in d['nodes']:
        assert not any(k in n for k in ['matrix','translation','rotation','scale']),'Update skull bounds extraction for transformed nodes'
        if n.get('name')=='bone.hyoid':continue
        for p in d['meshes'][n['mesh']]['primitives']:
            a=d['accessors'][p['attributes']['POSITION']]
            for k in range(3):lo[k]=min(lo[k],a['min'][k]);hi[k]=max(hi[k],a['max'][k])
    m['startupBounds']=[lo,hi]
    write_changed(BASE/'manifest.json',json.dumps(m,indent=2,ensure_ascii=False).encode()+b'\n')
    report={'built':built,'assembled':assembled,'reused':reused,'packs':len(packs),'seconds':round(time.perf_counter()-started,4),'starterBytes':sum(p['bytes'] for p in packs if p['stage']==0)}
    print('Loading packs: '+json.dumps(report));return report
if __name__=='__main__':main()
