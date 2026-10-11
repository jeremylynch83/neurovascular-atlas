from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
for a,b in [('MMA frontal','brain.orbital-gyri.right'),('MMA frontal left','brain.orbital-part-of-inferior-frontal-gyrus.left')]:
 v,f=load(a,OUT);w,g=load(b,OUT);c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.Update();p=c.GetContactsOutput().GetPoints();pp=vtk_to_numpy(p.GetData())
 print(a,b,c.GetNumberOfContacts(),np.round(pp[::max(1,len(pp)//15)],2).tolist(),flush=True)
