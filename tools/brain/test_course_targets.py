"""Dural bone references must not weaken pial/neural course constraints."""
import unittest
from validate_courses import validate_targets

class Targets(unittest.TestCase):
    def setUp(self):
        self.rows={'bone.a':{'system':'bone','asset':{}},'brain.a':{'system':'brain','asset':{'node':'a'}},'vein.a':{'system':'vein','asset':{'node':'v'}},'passage':{'landmark':{'point':[0,0,0]}}}
        self.rows['bone.a']['asset']={'node':'b'}
        self.course={'targetStructureIds':['bone.a'],'referenceStructureIds':['vein.a','passage'],'segments':[{'targetStructureIds':['bone.a'],'mode':'dural-attachment'}]}
    def test_dural_and_groove_bone_supported(self):
        for mode in ['dural-attachment','bony-groove']:
            self.course['segments'][0]['mode']=mode;validate_targets(self.course,self.rows)
    def test_pial_bone_rejected(self):
        self.course['segments'][0]['mode']='pial'
        with self.assertRaises(AssertionError):validate_targets(self.course,self.rows)
    def test_vessel_not_a_tissue_target(self):
        self.course['targetStructureIds']=['vein.a']
        with self.assertRaises(AssertionError):validate_targets(self.course,self.rows)
    def test_missing_reference_rejected(self):
        self.course['referenceStructureIds'].append('missing')
        with self.assertRaises(AssertionError):validate_targets(self.course,self.rows)
    def test_unmeshed_tissue_rejected(self):
        self.rows['bone.a'].pop('asset')
        with self.assertRaises(AssertionError):validate_targets(self.course,self.rows)
    def test_original_brain_target_supported(self):
        self.course={'targetStructureIds':['brain.a'],'segments':[{'targetStructureIds':['brain.a'],'mode':'pial'}]};validate_targets(self.course,self.rows)

if __name__=='__main__':unittest.main()
