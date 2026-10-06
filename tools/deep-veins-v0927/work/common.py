from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT
sys.path.insert(0,str(BASE/'work'))
from geometry import meshes,poly,locator,close,contacts,smooth,vtk,vtk_to_numpy
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d
OUT=ROOT/'candidate';MAN=json.loads((ROOT.parents[1]/'public/anatomy/manifest.json').read_text());ROWS={r['id']:r for r in MAN['structures']}
locs={}
def surface(k,seed,offset=.2):
 node=ROWS[k]['asset']['node'];m=meshes[node]
 if node not in locs:locs[node]=locator(m.pd)
 q,dist=close(locs[node],seed)
 # Use nearest oriented triangle normal for a small radius-aware offset.
 p=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);dd=vtk.reference(0.);locs[node].FindClosestPoint(seed,p,ci,sub,dd);tri=m.v[m.f[int(ci)]];n=np.cross(tri[1]-tri[0],tri[2]-tri[0]);n/=max(np.linalg.norm(n),1e-12)
 return q+n*offset

def centreline(k):
 cache=OUT/(k+'.baseline-course.npz')
 if cache.exists():return np.load(cache)['q']
 namespace={};exec((BASE/'work/extract_curves.py').read_text().split('courses={}')[0],namespace);q,_,_,_=namespace['extract'](meshes[k]);np.savez_compressed(cache,q=q);return q

def inlet(k,seed):
 q=centreline(k);return q[np.argmin(np.linalg.norm(q-seed,axis=1))].copy()
def curve(points):
 q=np.asarray(points,float);q=q[np.r_[True,np.linalg.norm(np.diff(q,axis=0),axis=1)>.01]];t=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];n=max(24,int(t[-1]/.25)+1)
 return CubicSpline(t,q,axis=0,bc_type='natural')(np.linspace(0,t[-1],n))
