from model import *
bone=combine(['bone.sphenoid','bone.temporal.right','bone.temporal.left']);out=[]
for s in ['right','left']:
 cs=poly(*load('vein.cavernous.'+s,True));ica=combine(['ICA cavernous '+s,'ICA paraophthalmic '+s]);b=contacts(cs,bone);a=contacts(cs,ica);out.append({'side':s,'boneContacts':b,'mainIcaContacts':a});print(out[-1],flush=True)
(OUT/'clearance.json').write_text(json.dumps(out,indent=2))
