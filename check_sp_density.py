import numpy as np
import h5py
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.cluster import DBSCAN
from cal_grid_size import *
from grid_cut import *
from spline_kernel import *

if __name__=="__main__":
  f = h5py.File("output/spline_kernel.hdf5",'r')

  dfData200 = pd.DataFrame({'x' : f['sp_pos200'][:,0],
                            'y' : f['sp_pos200'][:,1],
                            'z' : f['sp_pos200'][:,2],
                            'density': f['sp_density200'][:]})

  dfData205 = pd.DataFrame({'x' : f['sp_pos205'][:,0],
                            'y' : f['sp_pos205'][:,1],
                            'z' : f['sp_pos205'][:,2],
                            'density': f['sp_density205'][:]})

  dfData210 = pd.DataFrame({'x' : f['sp_pos210'][:,0],
                            'y' : f['sp_pos210'][:,1],
                            'z' : f['sp_pos210'][:,2],
                            'density': f['sp_density210'][:]})

  fig = plt.figure()
  fig.set_size_inches(20,7)
  
  ax = fig.add_subplot(1,3,1)
  log_dens = np.log(dfData200['density'])
  plt.hist(log_dens,1000)
 
  ax = fig.add_subplot(1,3,2)  
  log_dens = np.log(dfData205['density'])
  plt.hist(log_dens,1000)
  
  ax = fig.add_subplot(1,3,3)
  log_dens = np.log(dfData210['density'])
  plt.hist(log_dens,1000)


  plt.xlabel("log(density)")
  plt.ylabel("# of x")
  ax.set_xlim([-15,0])
  #ax.set_ylim([0,10000])
  plt.show()
