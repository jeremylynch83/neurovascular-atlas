import sys,json,numpy as np
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from repair import *
def directed(v,f,ring):
 seq=order(v,f,ring);edges={tuple(map(int,t[[k,(k+1)%3]]))for t in f for k in range(3)}
 # Exact index identities may differ at duplicate seam points, so inspect all edges.
 for k in range(len(seq)):
  a,b=seq[k],seq[(k+1)%len(seq)]
  if (int(a),int(b))in edges:return seq
  if (int(b),int(a))in edges:return seq[::-1]
 raise ValueError('No native orientation')
def loft(n,parent,bow=(0,0,0),override=None):
 v,f=override if override is not None else mesh(n);w,g=mesh(parent);rs=rims(v,f);rp=rims(w,g)
 i,j=min(((i,j)for i in range(len(rs))for j in range(len(rp))),key=lambda ij:np.linalg.norm(v[rs[ij[0]]].mean(0)-w[rp[ij[1]]].mean(0)))
 src=directed(v,f,rs[i]);target=directed(w,g,rp[j])[::-1]
 # Match cyclic perimeter positions while preserving each native boundary edge.
 a=v[src];b=w[target];ka=np.linspace(0,1,len(a),endpoint=False)
 best=None
 for k in range(len(target)):
  dst=np.roll(target,k);bb=w[dst];kb=np.linspace(0,1,len(bb),endpoint=False)
  sample=np.column_stack([np.interp(ka,np.r_[kb,1],np.r_[bb[:,q],bb[0,q]])for q in range(3)])
  err=np.sum((a-a.mean(0)-(sample-sample.mean(0)))**2)
  if best is None or err<best[0]:best=(err,dst,sample)
 dst=best[1];sample=best[2];q=v.copy();faces=f.tolist();rings=[src]
 # Intermediate collars keep the source rim fixed and distribute the bridge.
 for t in [.25,.5,.75]:
  ring=(1-t)*a+t*sample+np.sin(np.pi*t)*np.array(bow);ix=np.arange(len(q),len(q)+len(ring));q=np.vstack([q,ring]);rings.append(ix)
 endpoint=np.arange(len(q),len(q)+len(dst));q=np.vstack([q,w[dst]]);rings.append(endpoint)
 for r,s in zip(rings[:-1],rings[1:]):
  ii=jj=0
  while ii<len(r)or jj<len(s):
   # Unequal rings use a monotonic zipper rather than collapsing a rim vertex.
   if ii<len(r)and (jj==len(s)or (ii+1)/len(r)<=(jj+1)/len(s)):
    faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(r[(ii+1)%len(r)])]);ii+=1
   else:
    faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(s[(jj+1)%len(s)])]);jj+=1
 p=q.astype('<f4').astype(float);ff=np.array(faces,dtype=np.uint32)
 # Assess reports compare original face IDs and all surrounding objects.
 d={'sourceRim':endpoint.tolist(),'parentRim':dst.tolist(),'originalVertexCount':len(v),'transitionLengthMm':float(np.linalg.norm(a.mean(0)-w[dst].mean(0))),'rimShapeRmsMismatchMm':float(np.sqrt(best[0]/len(src))),'maxShiftMm':0.,'fixedDistalRimVertices':len(v),'distalRimExact':np.array_equal(p[:len(v)],v),'method':'append-native-rim-connector-no-original-vertex-displacement'}
 return q,ff,p,d
if __name__=='__main__':
 report=[];accepted=[]
 for side in ['left','right']:
  for stem,parent in [('MMA falcine terminal','MMA paramedian'),('ACA falcine branch','ACA A5')]:
   n=stem+' '+side;pn=parent+' '+side;v,f,p,d=loft(n,pn);r=assess(n,pn,v,f,p,d);report.append(r);print(json.dumps(r),flush=True)
   if r['passed']:
    p.astype('<f4').tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(n+'.normals.bin'));accepted.append(r)
 (D.parent/'loft-trials.json').write_text(json.dumps({'accepted':accepted,'trials':report},indent=2)+'\n')
