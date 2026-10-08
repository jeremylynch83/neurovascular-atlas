from model import *
from venous import LO,HI,DIMS,SP
from scipy.ndimage import map_coordinates
cache=OUT/'artery-network-sdf.npy';ad=np.load(cache);checks=[]
for side in ['right','left']:
 names=[n+' '+side for n in ['Meningohypophyseal trunk','Inferolateral trunk','Inferior hypophyseal','Dorsal meningeal','Tentorial marginal','Basal tentorial MHT branch','Medial clival MHT branch','Lateral clival MHT branch','ILT superior ramus','ILT anterolateral ramus','ILT recurrent lacerum ramus','Ophthalmic','Superior hypophyseal','Posterior communicating','Anterior choroidal'] if any(m['name']==n+' '+side for m in META)]
 artery=closed(combine(names,True));bounds=np.array(artery.GetBounds()).reshape(3,2);il=np.maximum(0,np.floor((bounds[:,0]-.7-LO)/SP).astype(int));ih=np.minimum(DIMS,np.ceil((bounds[:,1]+.7-LO)/SP).astype(int)+1);slices=tuple(slice(a,b) for a,b in zip(il,ih));sublo=LO+il*SP;subhi=LO+(ih-1)*SP
 dd=sample(artery,sublo,subhi,ih-il);g=np.load(OUT/('cavity-'+side+'.npz'));xx=np.stack(np.meshgrid(*[LO[j]+np.arange(il[j],ih[j])*SP[j] for j in range(3)],indexing='ij'),axis=0).reshape(3,-1);body=map_coordinates(g['outer'],(xx-g['lo'][:,None])/g['spacing'][:,None],order=1,mode='constant',cval=100).reshape(ih-il);dd[body>1]=100;ad[slices]=np.minimum(ad[slices],dd);checks.append({'side':side,'arterialLabels':names,'scope':'Independent sinus envelope and a 1 mm collar beyond its outer boundary; remote courses remain fixed.','branchVenousGapRequestedMm':.30});print(side,'branch spaces carved',len(names),flush=True)
np.save(cache,ad);(OUT/'branch-clearance-authoring.json').write_text(json.dumps(checks,indent=2))
