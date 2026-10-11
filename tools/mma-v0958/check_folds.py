"""Exact existing VTK triangle test, batched without Python call overhead."""
import sys,ast,ctypes
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
import vtkmodules
lib=ctypes.CDLL(str(Path(__file__).parent/'triangle_batch.so'));fn=lib.vtk_triangle_batch
array=np.ctypeslib.ndpointer;fn.argtypes=[ctypes.c_char_p,array(np.float64,flags='C_CONTIGUOUS'),array(np.int64,flags='C_CONTIGUOUS'),array(np.int64,flags='C_CONTIGUOUS'),ctypes.c_int64,array(np.uint8,flags='C_CONTIGUOUS')];fn.restype=ctypes.c_int
vtk_lib=str(Path(vtkmodules.__file__).parent/'libvtkCommonDataModel-9.3.so').encode()
def batch(t,a,b):
 t=np.ascontiguousarray(t,dtype=np.float64);a=np.ascontiguousarray(a,dtype=np.int64);b=np.ascontiguousarray(b,dtype=np.int64);out=np.zeros(len(a),np.uint8)
 assert fn(vtk_lib,t,a,b,len(a),out)==0
 return out.astype(bool)
source=(Path(__file__).parents[1]/'mma-v0952/self_check.py').read_text()
source=source.replace("from common import *","")
source=source.replace("  for a,b in zip(aa,bb):\n   if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append((int(a),int(b)))", "  keep=batch(t,aa,bb)\n  pairs.extend((int(a),int(b))for a,b in zip(aa[keep],bb[keep]))")
assert 'for a,b in zip(aa,bb):'not in source
# Compare the native batch with the original wrapped method before any check.
rng=np.random.default_rng(518);t=rng.normal(size=(40,3,3));a=rng.integers(0,40,100);b=rng.integers(0,40,100)
assert np.array_equal(batch(t,a,b),[bool(vtk.vtkTriangle.TrianglesIntersect(*t[i],*t[j]))for i,j in zip(a,b)])
exec(compile(source,'self_check_batched','exec'))
