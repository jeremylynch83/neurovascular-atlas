"""Conforming source triangle refinement before non-affine atlas deformation.

Long decimated faces cannot follow a curved coordinate map from their endpoints
alone. Split long edges across all edited labels together, retaining material
face labels and shared boundary coordinates. Source surfaces are unchanged.
"""
import copy,json
import numpy as np
from fit_vessels import read_glb,write_glb,mesh_records,accessor

def subdivide(records,keys,max_edge):
    points=[];faces=[];labels=[];offset=0;names=sorted(keys)
    for i,key in enumerate(names):
        r=records[key];p=r['old'];points.append(p);faces.append(r['faces']+offset);labels.extend([i]*len(r['faces']));offset+=len(p)
    p=np.concatenate(points);f=np.concatenate(faces);labels=np.array(labels)
    _,indices,inverse=np.unique(np.round(p,5),axis=0,return_index=True,return_inverse=True);p=p[indices];f=inverse[f]
    for iteration in range(10):
        edges=np.stack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]],axis=1)
        unique,inv=np.unique(np.sort(edges,axis=2).reshape(-1,2),axis=0,return_inverse=True);inv=inv.reshape(-1,3)
        split=np.linalg.norm(p[unique[:,0]]-p[unique[:,1]],axis=1)>max_edge
        if not split.any():break
        middle=np.full(len(unique),-1,int);middle[split]=np.arange(len(p),len(p)+split.sum());p=np.vstack([p,p[unique[split]].mean(1)])
        mids=middle[inv];codes=(split[inv]*[1,2,4]).sum(1);new=[];tags=[]
        patterns={0:[['a','b','c']],1:[['a','u','c'],['u','b','c']],2:[['b','v','a'],['v','c','a']],4:[['c','w','b'],['w','a','b']],3:[['b','v','u'],['a','u','c'],['u','v','c']],6:[['c','w','v'],['b','v','a'],['v','w','a']],5:[['a','u','w'],['c','w','b'],['w','u','b']],7:[['a','u','w'],['u','b','v'],['w','v','c'],['u','v','w']]}
        for code,pattern in patterns.items():
            keep=codes==code
            if not keep.any():continue
            values={k:v for k,v in zip(['a','b','c','u','v','w'],np.column_stack([f[keep],mids[keep]]).T)}
            for tri in pattern:new.append(np.column_stack([values[k] for k in tri]));tags.append(labels[keep])
        f=np.concatenate(new);labels=np.concatenate(tags)
        print('Source refinement',iteration+1,len(p),len(f),flush=True)
    result={}
    for i,key in enumerate(names):
        indices,inverse=np.unique(f[labels==i],return_inverse=True);result[key]=(p[indices],inverse.reshape(-1,3))
    return result

def save_replaced(path,source_doc,source_data,replacements):
    doc={'asset':copy.deepcopy(source_doc['asset']),'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'materials':copy.deepcopy(source_doc.get('materials',[])),'accessors':[],'bufferViews':[],'buffers':[{}]};data=bytearray()
    def put(values,template,target):
        values=np.ascontiguousarray(values);a=copy.deepcopy(template);a.pop('byteOffset',None);a['bufferView']=len(doc['bufferViews']);a['count']=len(values)
        if values.dtype==np.dtype('<u4'):a['componentType']=5125
        if 'min' in a:a['min']=values.min(0).tolist();a['max']=values.max(0).tolist()
        i=len(doc['accessors']);doc['accessors'].append(a);data.extend(b'\0'*(-len(data)%4));doc['bufferViews'].append({'buffer':0,'byteOffset':len(data),'byteLength':values.nbytes,'target':target});data.extend(values.tobytes());return i
    for node in source_doc['nodes']:
        if 'mesh' not in node:continue
        n=copy.deepcopy(node);n['mesh']=len(doc['meshes']);mesh=copy.deepcopy(source_doc['meshes'][node['mesh']]);key=node['name']
        assert len(mesh['primitives'])==1
        primitive=mesh['primitives'][0]
        rep=replacements.get(key)
        attributes={}
        for attr,index in primitive['attributes'].items():
            value=rep[0].astype('<f4') if rep and attr=='POSITION' else rep[2].astype('<f4') if rep and attr=='NORMAL' else accessor(source_doc,source_data,index).copy()
            attributes[attr]=put(value,source_doc['accessors'][index],34962)
        primitive['attributes']=attributes;index=primitive['indices'];value=rep[1].astype('<u4').reshape(-1,1) if rep else accessor(source_doc,source_data,index).copy();primitive['indices']=put(value,source_doc['accessors'][index],34963)
        doc['scenes'][0]['nodes'].append(len(doc['nodes']));doc['nodes'].append(n);doc['meshes'].append(mesh)
    doc['buffers'][0]['byteLength']=len(data);write_glb(path,doc,data)
