"""Exact orthographic triangle renders, same camera before and after."""
from common import *
import importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('software_renderer',Path(__file__).resolve().parents[1]/'relationships-v0949/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rev=json.loads((OUT/'revision.json').read_text());new=set(rev['newLabels']);right=lambda f:'vein.'+f+'.right'
scenes=[('Petrosal shafts', [right('superior_petrosal'),right('inferior_petrosal'),right('cavernous'),right('superior_petrosal_vein')],[23,-61,54],38,5,10),('Mandibular and infraorbital drainage',['Inferior alveolar','Infraorbital',right('pterygoid_plexus'),right('inferior_alveolar'),right('infraorbital')],[30,-22,18],76,10,0),('Vertebral venous plexus',['Vertebral V2 right',right('vertebral'),right('vertebral_periarterial_plexus')],[21,-83,-39],58,90,0),('Paired anterior meningeal veins',['Middle meningeal','MMA frontal',right('middle_meningeal'),right('pterygoid_plexus')],[40,-34,89],145,0,0),('Retinal reference course',['Central retinal right',right('central_retinal'),right('superior_ophthalmic')],[24,-8,67],35,90,18),('Selected internal auditory CPA route',['Labyrinthine right',right('internal_auditory'),right('superior_petrosal_vein'),right('cerebellopontine_fissure')],[27,-72,53],28,90,20)]
scenes=[s for s in scenes if all(n in FILES or n in new for n in s[1])]
W=1340;H=160+len(scenes)*708+92;out=Image.new('RGB',(W,H),'#f4f4ef');d=ImageDraw.Draw(out);font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,26);small=ImageFont.truetype(font,18);title=ImageFont.truetype(font,33)
d.text((20,18),'Neurovascular Atlas | Audit continuation v0.9.50',font=title,fill='#172335');d.text((20,66),'Exact mesh renders. Blue: veins. Red: arteries. Matched cameras and scale.',font=small,fill='#354354');d.text((20,105),'v0.9.49',font=f,fill='#172335');d.text((680,105),'v0.9.50',font=f,fill='#172335')
for i,(label,names,centre,extent,az,el) in enumerate(scenes):
 y=150+i*708;d.text((20,y),label,font=f,fill='#172335')
 for col,directory in enumerate([DATA,OUT]):
  ns=[n for n in names if directory==OUT or n not in new];im=mod.render(directory,ns,centre,extent,az=az,el=el);out.paste(im,(20+col*660,y+42))
d.text((20,H-72),'Reference reconstructions. Canal containment, nerves and cervical bone fit remain unverified.',font=small,fill='#354354');d.text((20,H-43),'Views isolate the regional vessels for inspection; they do not demonstrate full bone containment.',font=small,fill='#354354');out.save(WORK/'Vessel_changes_v0.9.50.png');print('Saved comparison',out.size)
