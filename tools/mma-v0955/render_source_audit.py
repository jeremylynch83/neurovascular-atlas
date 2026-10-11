"""Render exact sections of the recovered source and retained reference."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'mma-v0952'))
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
report = json.loads((WORK / 'source-reference-comparison.json').read_text())
source = {p.name[:-len('.positions.bin')]: load(p.name[:-len('.positions.bin')], WORK / 'source-registered')
          for p in (WORK / 'source-registered').glob('*.positions.bin')}
atlas = {n: load(n) for n in source}

def segments(v, f, z):
    if not v[:, 2].min() <= z <= v[:, 2].max():
        return []
    plane = vtk.vtkPlane(); plane.SetOrigin(0, 0, z); plane.SetNormal(0, 0, 1)
    cutter = vtk.vtkCutter(); cutter.SetInputData(poly(v, f)); cutter.SetCutFunction(plane); cutter.Update()
    mesh = cutter.GetOutput()
    if not mesh.GetNumberOfPoints():
        return []
    points = vtk_to_numpy(mesh.GetPoints().GetData())[:, :2]
    raw = vtk_to_numpy(mesh.GetLines().GetData()); result = []; k = 0
    while k < len(raw):
        count = int(raw[k]); indices = raw[k+1:k+1+count]
        result.extend(points[np.c_[indices[:-1], indices[1:]]]); k += count+1
    return result

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for row, z in enumerate([82., 110.]):
    for col, meshes in enumerate([source, atlas]):
        ax = axes[row, col]
        for name, (v, f) in meshes.items():
            if name.startswith(('brain.falx', 'brain.tentorium')):
                continue
            bone = name.startswith('bone.')
            ss = segments(v, f, z)
            if ss:
                ax.add_collection(LineCollection(ss, colors='#686c76' if bone else '#248487',
                                                 linewidths=.85 if bone else .55,
                                                 alpha=1. if bone else .7))
        rows = report['sourcePairs' if col==0 else 'atlasPairs']
        points = np.asarray([p for r in rows for p in r['sampleContactPoints']])
        take = np.abs(points[:, 2]-z)<1.5
        if take.any():
            ax.scatter(points[take, 0], points[take, 1], s=15, c='#bf3335', zorder=5)
        ax.set_xlim(-75, 75); ax.set_ylim(-155, 32); ax.set_aspect('equal')
        ax.set_xlabel('RAS X (mm), +X right'); ax.set_ylabel('RAS Y (mm), +Y anterior')
        ax.grid(alpha=.15)
        ax.set_title(('Original skull + brain, shared source frame' if col==0 else 'Retained atlas reference, v0.9.51')+
                     ' | Z = '+str(int(z))+' mm', fontsize=10)
fig.suptitle('Neurovascular Atlas | verified source reference audit', fontsize=16)
fig.text(.5, .045, 'Grey: skull section. Teal: neural surfaces. Red: sampled near-guide contact points within 1.5 mm of the section.',
         ha='center', fontsize=9)
fig.text(.5, .023, f"Source: {report['sourcePairCount']} skull/neural pairs. Retained atlas: {report['atlasPairCount']} pairs near the full MMA guides. No source anatomy was deformed.",
         ha='center', fontsize=10, color='#9c2b2b')
fig.tight_layout(rect=[0, .065, 1, .95])
fig.savefig(WORK / 'Verified_source_reference_audit.png', dpi=150)
plt.close(fig)
print(WORK / 'Verified_source_reference_audit.png')
