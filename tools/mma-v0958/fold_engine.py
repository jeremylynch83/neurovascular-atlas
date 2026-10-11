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

import ast
p=Path(__file__).parents[1]/'mma-v0952/self_check.py'
src=p.read_text();tree=ast.parse(src);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='intersections');source=ast.get_source_segment(src,node)
source=source.replace("  for a,b in zip(aa,bb):\n   if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append((int(a),int(b)))", "  keep=batch(t,aa,bb)\n  pairs.extend((int(a),int(b))for a,b in zip(aa[keep],bb[keep]))")
exec(compile(source,'intersections_batched','exec'))
