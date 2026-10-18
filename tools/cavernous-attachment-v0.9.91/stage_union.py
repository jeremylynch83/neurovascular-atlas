from transport_collar import *
x=np.load(D.parent/'fitted-parent.npz');CACHE['MMA cavernous left']=(x['v'],x['f']);p,f,d=transport_collar(54.,.8,1.,parent_exit=(0,0,1));assert not intersections(p,f)
for n,v,g in [('MMA posterior cavernous left',p,f),('MMA cavernous left',x['v'],x['f'])]:
 v.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.astype('<u4').tofile(OUT/(n+'.indices.bin'));np.savez(D.parent/('screened-'+n+'.npz'),v=v,f=g)
(D.parent/'route-input.json').write_text(json.dumps(d,indent=2)+'\n')
