"""Build the overview image and portable package after rendering."""
from pathlib import Path
import shutil,zipfile,json,argparse
from PIL import Image,ImageDraw,ImageFont

APP=Path(__file__).resolve().parents[2]
OUT=APP/'deliverables/posterior-fossa-expanded-review'
PANELS=['combined-anterior','combined-right','combined-posterior','combined-superior','venous-oblique','venous-superior']

def main():
    global OUT,PANELS
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='deliverables/posterior-fossa-expanded-review');parser.add_argument('--candidate',type=int,default=55);parser.add_argument('--overview',default='posterior-fossa-expanded-views.png');args=parser.parse_args();OUT=APP/args.output
    if args.candidate>=56:PANELS=['surface-anterior','surface-right','surface-posterior','spinal-surface-posterior','spinal-surface-right','venous-oblique']
    width=2400;panel_w=800;panel_h=613;top=126;bottom=65
    image=Image.new('RGB',(width,top+2*panel_h+bottom),'#f8fafc');draw=ImageDraw.Draw(image)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font.replace('.ttf','-Bold.ttf'),32)
    text=ImageFont.truetype(font,23)
    draw.text((30,18),'Posterior fossa: surface vessels and PSAs arising from PICA' if args.candidate>=56 else 'Brainstem and cerebellum: expanded vascular views',font=title,fill='#263343')
    for x,label,colour in [(30,'Arteries','#bc403e'),(280,'Posterior-fossa veins','#21649b'),(710,'Basal veins, Galen and internal cerebral veins','#078e94')]:
        draw.rectangle((x,79,x+24,103),fill=colour);draw.text((x+35,76),label,font=text,fill='#263343')
    draw.text((1770,76),'Clival plexus omitted',font=text,fill='#596c7d')
    for i,name in enumerate(PANELS):
        view=Image.open(OUT/'views'/f'{name}.png').convert('RGB').resize((panel_w,panel_h),Image.Resampling.LANCZOS)
        image.paste(view,((i%3)*panel_w,top+(i//3)*panel_h))
    draw.line((0,top+panel_h,width,top+panel_h),fill='#dce2e8',width=2)
    for x in [800,1600]:draw.line((x,top,x,top+2*panel_h),fill='#dce2e8',width=2)
    draw.text((30,top+2*panel_h+18),f'Candidate {args.candidate}. Perforators enter tissue intentionally. The cord is an illustrative continuation.' if args.candidate>=56 else 'Candidate 55: existing placement and joins remain under review. Individual views and sinus outlets are included in the viewer.',font=text,fill='#596c7d')
    image.save(OUT.parent/args.overview)
    shutil.copyfile(OUT.parent/args.overview,OUT/'overview.png')
    (OUT/'authoring').mkdir(exist_ok=True)
    for path in ['tools/brain/package_expanded_review.py','tools/brain/finish_expanded_review.py','tools/render-expanded-review.mjs']:
        shutil.copyfile(APP/path,OUT/'authoring'/Path(path).name)
    assert json.loads((OUT/'geometry-validation.json').read_text())['passed']
    assert json.loads((OUT/'browser-validation.json').read_text())['passed']
    archive=OUT.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(OUT.parent))
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(archive,archive.stat().st_size,flush=True)

if __name__=='__main__':main()
