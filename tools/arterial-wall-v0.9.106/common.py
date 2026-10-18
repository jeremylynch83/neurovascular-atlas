from pathlib import Path
import sys,json,numpy as np,hashlib
A=Path(__file__).resolve().parents[2];R=A.parents[1];W=Path(sys.argv[1]).resolve();CACHE=Path(sys.argv[2]).resolve();sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table
D=W/'decoded';overrides={}
for p in D.glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=D/(n+'.indices.bin');overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,CACHE,overrides)
