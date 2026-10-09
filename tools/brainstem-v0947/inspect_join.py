from common import *
from scipy.spatial import cKDTree
av,af=load('vein.anterior_pontine',OUT);bv,bf=load('vein.transverse_pontine.right',OUT)
c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(av,af));c.SetInputData(1,poly(bv,bf));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update()
p=vtk_to_numpy(c.GetContactsOutput().GetPoints().GetData());a,_=load('vein.anterior_pontine');b,_=load('vein.transverse_pontine.right');d,ix=cKDTree(b).query(a);seam=a[d<1e-5];q,_=load('vein.anterior_pontine',OUT);newseam=q[d<1e-5];ds=cKDTree(newseam).query(p)[0]
print('contacts',len(p),'maxseamdistance',ds.max());print(np.c_[p[ds>.05],ds[ds>.05]])
