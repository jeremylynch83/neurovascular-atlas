"""Regression checks for independently bounded surface and cisternal segments."""
import unittest,json,copy,hashlib
from validate_courses import validate_segments
class Segments(unittest.TestCase):
 def setUp(self):
  self.points=[[0,0,0],[1,0,0],[2,0,0],[3,0,0]]
  self.cache={'anatomy/source/test.json':{'v':{'parts':[{'points':self.points}]}}}
  self.c={'vesselId':'v','targetStructureIds':['brain.a'],'stationIds':[],
   'coursePaths':[{'source':'anatomy/source/test.json','sourceStructureId':'v','sourcePart':0,'pointCount':4,'pointSha256':hashlib.sha256(json.dumps(self.points,separators=(',',':')).encode()).hexdigest(),'lengthMm':3}],
   'segments':[{'order':i,'mode':mode,'targetStructureIds':targets,'stationIds':[],'pathIndex':0,'pointRange':r,'arcRangeMm':r,'constraints':{'allowTissueEntry':False,'avoidAtlasCutFaces':True,'preserveJoinedAttachments':True,'wallClearance':'radius-aware'}} for i,mode,targets,r in [(0,'pial',['brain.a'],[0,1]),(1,'cisternal',[],[1,3])]]}
 def check(self):validate_segments(self.c,{},self.cache)
 def test_mixed_course_valid(self):self.check()
 def test_gap_rejected(self):
  self.c['segments'][1]['pointRange']=[2,3];self.c['segments'][1]['arcRangeMm']=[2,3]
  with self.assertRaises(AssertionError):self.check()
 def test_overlap_rejected(self):
  self.c['segments'][0]['pointRange']=[0,2];self.c['segments'][0]['arcRangeMm']=[0,2]
  with self.assertRaises(AssertionError):self.check()
 def test_out_of_range_rejected(self):
  self.c['segments'][1]['pointRange']=[1,4]
  with self.assertRaises(AssertionError):self.check()
 def test_foreign_target_rejected(self):
  self.c['segments'][1]['targetStructureIds']=['brain.b']
  with self.assertRaises(AssertionError):self.check()
 def test_lost_target_rejected(self):
  self.c['segments'][0]['targetStructureIds']=[]
  with self.assertRaises(AssertionError):self.check()
 def test_stale_path_rejected(self):
  self.cache['anatomy/source/test.json']['v']['parts'][0]['points'][1]=[1,2,0]
  with self.assertRaises(AssertionError):self.check()
 def test_false_arc_rejected(self):
  self.c['segments'][1]['arcRangeMm']=[1,2.9]
  with self.assertRaises(AssertionError):self.check()
if __name__=='__main__':unittest.main()
