"""Exact axial triangle intersections for skull/brain registration review."""
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
source={n:load(n) for n in FILES};candidate={n:load(n,OUT) if n in changed else vf for n,vf in source.items()}
for n in rev['newLabels']:candidate[n]=load(n,OUT)
def segments(v,f,z):
    if not (v[:,2].min()<=z<=v[:,2].max()):return []
    plane=vtk.vtkPlane();plane.SetOrigin(0,0,z);plane.SetNormal(0,0,1);c=vtk.vtkCutter();c.SetInputData(poly(v,f));c.SetCutFunction(plane);c.Update();pd=c.GetOutput()
    if not pd.GetNumberOfPoints():return []
    points=vtk_to_numpy(pd.GetPoints().GetData())[:,:2];raw=vtk_to_numpy(pd.GetLines().GetData());out=[];k=0
    while k<len(raw):
        count=int(raw[k]);ids=raw[k+1:k+1+count];out.extend(points[np.c_[ids[:-1],ids[1:]]]);k+=count+1
    return out
fig,axes=plt.subplots(2,2,figsize=(12,11));colours={'bone.':'#777777','brain.':'#267f83','artery':'#d53034','vein.':'#2266d3'}
for row,z in enumerate([82.,110.]):
    for col,mesh in enumerate([source,candidate]):
        ax=axes[row,col]
        for n,(v,f) in mesh.items():
            category='bone.' if n.startswith('bone.') else ('brain.' if n.startswith('brain.') and not any(s in n for s in ['falx','tentorium']) else ('vein.' if n.startswith('vein.middle_meningeal.') else ('artery' if n.startswith(('MMA ','Middle meningeal')) else None)))
            if category is None:continue
            ss=segments(v,f,z)
            if ss:ax.add_collection(LineCollection(ss,colors=colours[category],linewidths=.45 if category in ['bone.','brain.'] else 1.7,alpha=.6 if category=='brain.' else 1.))
        ax.set_xlim(-63,63);ax.set_ylim(-96,14);ax.set_aspect('equal');ax.set_xlabel('RAS X (mm), +X = right');ax.set_ylabel('RAS Y (mm), +Y = anterior');ax.grid(alpha=.15);ax.set_title(('Accepted reference 0.9.51' if col==0 else 'Rejected reconstruction reference')+' | Z = '+str(int(z))+' mm',fontsize=11)
fig.suptitle('Neurovascular Atlas: skull and brain registration review',fontsize=16)
fig.text(.5,.032,'Grey: skull. Teal: neural surfaces. Red: MMA. Blue: new paired meningeal veins.',ha='center',fontsize=10)
fig.text(.5,.012,'Failed candidate: 270 new brain triangle-pair intersections. No trial anatomy has been installed.',ha='center',fontsize=10,color='#9c2b2b')
fig.tight_layout(rect=[0,.055,1,.95]);fig.savefig(WORK/'Skull_brain_registration_review_v0.9.54.png',dpi=150);plt.close(fig)

