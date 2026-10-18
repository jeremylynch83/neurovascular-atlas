import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/repair'))
from bridge_loops import bridge,combine,rim_normal
from collar import clip_keep
from geometry import edge_table,cycles
class RegionalAuthoringTests(unittest.TestCase):
 def test_zero_area_native_rim_rejected(self):
  with self.assertRaises(ValueError):rim_normal(np.zeros((3,3)))
 def test_unequal_native_rim_loft_is_oriented(self):
  def ring(n,z):
   a=np.arange(n)*2*np.pi/n;return np.c_[np.cos(a),np.sin(a),np.full(n,z)].astype('<f4')
  p,g,_=bridge(ring(11,0)[::-1],ring(17,3)[::-1],steps=7);p,g=combine([(p,g)]);u,e,c,b,d,_=edge_table(p,g)
  self.assertEqual(sum(c==1),28);self.assertFalse(np.any(c>2));self.assertTrue(np.all(b[c==2]==0));self.assertEqual(sorted(map(len,cycles(d[c==1]))),[11,17])
 def test_clip_cleans_float32_collapsed_intersections(self):
  v=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],dtype='<f4');f=np.array([[0,2,1],[0,1,3],[0,3,2],[1,2,3]],dtype='<u4')
  # A tiny offset rounds cut intersections onto translated source corners.
  v+=np.array([10,10,10],dtype='<f4')
  p,g=clip_keep(v,f,[0,0,10+1e-9],[0,0,1]);u,e,c,b,d,_=edge_table(p,g)
  self.assertFalse(np.any(c>2));self.assertTrue(np.all(b[c==2]==0));self.assertEqual(len(cycles(d[c==1])),1);self.assertTrue(np.all(p[:,2]>=10));self.assertEqual(len(np.unique(g)),len(p));self.assertEqual(len(g),3)
if __name__=='__main__':unittest.main()
