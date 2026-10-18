"""Analytic plane fixtures distinguish clear, crossing and touching triangles."""
import unittest
import numpy as np
from clearance import certify

class ClearanceTests(unittest.TestCase):
    def test_near_parallel_triangle_needs_refinement_and_is_fully_covered(self):
        t=np.array([[[0,0,.05],[1,0,.05],[0,1,.05]]])
        r=certify(t,lambda p:np.abs(p[:,2]),max_depth=6)
        self.assertTrue(r['passed']);self.assertGreater(r['maximumSubdivisionDepth'],0)
        self.assertAlmostEqual(r['certifiedAreaMm2'],.5)
    def test_crossing_triangle_cannot_be_certified(self):
        t=np.array([[[0,0,-.05],[1,0,.05],[0,1,.05]]])
        self.assertFalse(certify(t,lambda p:np.abs(p[:,2]),max_depth=5)['passed'])
    def test_touching_triangle_cannot_be_certified(self):
        t=np.array([[[0,0,0],[1,0,.05],[0,1,.05]]])
        self.assertFalse(certify(t,lambda p:np.abs(p[:,2]),max_depth=5)['passed'])

if __name__=='__main__':unittest.main(verbosity=2)
