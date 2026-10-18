from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=True);CACHE=Path(sys.argv[2]).resolve();sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene,BVH
from geometry import triangle_crosses
scene=Scene(A,CACHE)
