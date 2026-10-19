import numpy as np

def subdivide(p,f,surface,fields,max_edge=.38):
 n0=len(p);extra=np.array(surface.get('extra',[]),float).reshape(-1,3);p=np.r_[p,extra];nf=len(f);caps=np.array(surface.get('caps',[]),int).reshape(-1,3);faces=np.r_[f,caps];labels=np.r_[np.arange(nf),np.full(len(caps),-1)]
 lo=np.array([r['old'] for r in []]) if False else None
 boxes=[(np.array(r['old']).min(0)-r['outer']-1,np.array(r['old']).max(0)+r['outer']+1) for r in fields]
 for it in range(12):
  edges=np.sort(np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]),axis=1);edges=np.unique(edges,axis=0);a=p[edges[:,0]];b=p[edges[:,1]];active=np.zeros(len(edges),bool)
  for lo,hi in boxes:active|=((np.minimum(a,b)<=hi)&(np.maximum(a,b)>=lo)).all(1)
  active&=np.linalg.norm(a-b,axis=1)>max_edge
  split=edges[active]
  if not len(split):break
  mids={tuple(e):len(p)+i for i,e in enumerate(split)};p=np.r_[p,(p[split[:,0]]+p[split[:,1]])/2];new=[];labs=[]
  for (a,b,c),lab in zip(faces,labels):
   ab=mids.get(tuple(sorted([a,b])));bc=mids.get(tuple(sorted([b,c])));ca=mids.get(tuple(sorted([c,a])));mask=(ab is not None)*1+(bc is not None)*2+(ca is not None)*4
   if mask==0:parts=[[a,b,c]]
   elif mask==1:parts=[[a,ab,c],[ab,b,c]]
   elif mask==2:parts=[[b,bc,a],[bc,c,a]]
   elif mask==4:parts=[[c,ca,b],[ca,a,b]]
   elif mask==3:parts=[[b,bc,ab],[a,ab,c],[ab,bc,c]]
   elif mask==6:parts=[[c,ca,bc],[b,bc,a],[bc,ca,a]]
   elif mask==5:parts=[[a,ab,ca],[c,ca,b],[ca,ab,b]]
   else:parts=[[a,ab,ca],[ab,b,bc],[ca,bc,c],[ab,bc,ca]]
   new.extend(parts);labs.extend([lab]*len(parts))
  faces=np.array(new,int);labels=np.array(labs,int)
 actual=faces[labels>=0];used=np.unique(actual);order=np.r_[np.arange(n0),used[used>=n0]];capused=np.setdiff1d(np.unique(faces[labels<0]),order);order=np.r_[order,capused];na=len(order)-len(capused);remap=np.full(len(p),-1,int);remap[order]=np.arange(len(order));fnew=remap[actual];oldlabels=labels[labels>=0];entry={**surface,'vertexCount':na,'extra':p[order[na:]].tolist(),'caps':remap[faces[labels<0]].ravel().tolist(),'removed':np.where(np.isin(oldlabels,surface.get('removed',[])))[0].tolist(),'flips':np.where(np.isin(oldlabels,surface.get('flips',[])))[0].tolist()}
 entry['_sourceFaces']=oldlabels.tolist()
 return p[order[:na]],fnew,entry
