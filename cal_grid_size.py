import numpy as np
import h5py

f200 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.0.hdf5','r')
f205 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.5.hdf5','r')
f210 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr21.0.hdf5','r')

def pos(f):
  x_ = f['x_cartesian'][:]
  y_ = f['y_cartesian'][:]
  z_ = f['z_cartesian'][:]
  eta_ = f['eta'][:]
  lamb_ = f['lambda'][:]
  comoving_ = f['comoving_distance'][:]
  pos = np.vstack([x_,y_,z_]).T
  pos_sp = np.vstack([x_,y_,z_,eta_,lamb_,comoving_]).T
  return pos

def cal_dist(pos):
  dist3 = []
  n=0
  for i in pos : 
    dist = np.sqrt(np.sum((pos[:]-i)**2,axis=-1))
    dist.sort()
    dist3.append(dist[3])
    if n%1000 == 0:
      print('%i is done' %n)
    n+=1
  return dist3
	
if __name__=="__main__":
  pos200 = pos(f200)
  pos205 = pos(f205)
  pos210 = pos(f210)

  dist200 = cal_dist(pos200)
  dist205 = cal_dist(pos205)
  dist210 = cal_dist(pos210)

  f = h5py.File("cal_distance.h5py",'w')
  dataset = f.create_dataset("cal_dist200", data = dist200[:] ,dtype = 'f')
  dataset = f.create_dataset("cal_dist205", data = dist205[:] ,dtype = 'f')
  dataset = f.create_dataset("cal_dist210", data = dist210[:] ,dtype = 'f')
  f.close()
	

	
