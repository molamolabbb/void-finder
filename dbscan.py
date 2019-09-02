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

#%matplotlib inline
def DBscan(STEP,dfData):
  model = DBSCAN(eps=np.sqrt(3.)*STEP,min_samples=1) # np.sqrt(3) is the key!!!!!

  arrCutVal,arrNvoid = dfData['density'].median()*np.logspace(-3,3,61),[]
  for cut_val in arrCutVal:
    dfCutGrid = dfData[dfData['density'] < cut_val]
    #print(cut_val)

    dbCluster = model.fit(dfCutGrid.drop(['density'],axis=1))
    grpLabel = pd.Series(dbCluster.labels_,index=dfCutGrid.index)
    grpLabel[grpLabel == -1] = np.nan

    arrNvoid.append(len(grpLabel.value_counts() >= 5))

  #fig = plt.figure( figsize=(20,15))
  plt.clf()
  plt.plot(arrCutVal,arrNvoid,'C0-')
  plt.xscale("log")
  plt.xlabel(r"Density Threshold")
  plt.ylabel("Number of Voids (>= 5 cells)")
  plt.axvline(x=dfData['density'].median(),c='k',ls='--')
  plt.title("Number of Voids")
  plt.savefig("Number_of_Voids.pdf")


if __name__=="__main__":
  f = h5py.File("output/spline_kernel.h5py",'r')

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

  cal_dist_f = h5py.File("output/cal_distance.h5py",'r')
  
  dist200 = cal_dist_f['cal_dist200'][:]
  dist205 = cal_dist_f['cal_dist205'][:]
  dist210 = cal_dist_f['cal_dist210'][:]

  STEP200 = dist200.mean()+ 1.5*dist200.std()
  STEP205 = dist205.mean()+ 1.5*dist205.std()
  STEP210 = dist210.mean()+ 1.5*dist210.std()

  DBscan(STEP200,dfData200)
  DBscan(STEP205,dfData205)
  DBscan(STEP210,dfData210)

