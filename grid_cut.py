import numpy as np
import h5py
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from cal_grid_size import *

# make grids
def gridCut(nx,ny,nz,x,y,z,comoving_min,comoving_max):
    PI = math.pi
    ls_cut = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                comovingDist = math.sqrt(x[i]**2.+y[j]**2.+z[k]**2.)
                eta = np.arcsin(y[j]/comovingDist)
                lamb = np.arccos(z[k]/(comovingDist*np.cos(eta*PI/180.0)))
                if  (comoving_min<=comovingDist<=comoving_max) & (-33.5 < eta*180.0/PI < 36.5) & (-48.0 < lamb*180.0/PI < 51.0): 
                    ls_cut.append([x[i],y[j],z[k]])
    ls_cut = np.array(ls_cut)
    return ls_cut


# if you want check the grid, plot_3d grids
def plot_3d(sizex,sizey,x,y,z,gal_x,gal_y,gal_z):
    fig = plt.figure()
    fig.set_size_inches(sizex,sizey)
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(x,y,z,c='b',marker='.')
    ax.scatter(gal_x,gal_y,gal_z,c = 'r',marker='.')
    plt.show()

if __name__=="__main__":
  
  f200 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.0.hdf5','r')
  f205 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.5.hdf5','r')
  f210 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr21.0.hdf5','r')

  # galaxies position
  pos200 = first.pos(f200)
  pos205 = first.pos(f205)
  pos210 = first.pos(f210)

  # read the file you calculated  
  f = h5py.File("cal_distance.h5py",'r')

  dist200 = f['cal_dist200'][:]
  dist205 = f['cal_dist205'][:]
  dist210 = f['cal_dist210'][:]

  # A grid size is mean_distance + 1.5*standard deviation 
  STEP200 = dist200.mean()+ 1.5*dist200.std()
  STEP205 = dist205.mean()+ 1.5*dist205.std()
  STEP210 = dist210.mean()+ 1.5*dist210.std()

  PI = math.pi

  #Comoving distance : 59.84 Mpc/h <= d <= 388.48 Mpc/h
  gridcut205 = gridCut(81,61,47,
                       np.linspace(-40*STEP205,40*STEP205,81),np.linspace(-30*STEP205,30*STEP205,61),np.linspace(6*STEP205,52*STEP205,47),
                       59.85,388.48)
  #Comoving distance : 59.84 Mpc/h <= d <= 477.52 Mpc/h
  gridcut210 = gridCut(90,71,43,
                       np.linspace(-40*STEP210,50*STEP210,91),np.linspace(-35*STEP210,35*STEP210,71),np.linspace(3*STEP210,45*STEP210,43),
                       59.85,477.52)
  #Comoving distance : 59.84 Mpc/h <= d <= 314.23 Mpc/h
  gridcut200 = gridCut(81,63,48,
                       np.linspace(-40*STEP200,40*STEP200,81),np.linspace(-31*STEP200,31*STEP200,63),np.linspace(6*STEP200,53*STEP200,48),
                       59.85,314.23)

  plot_3d(5,5,gridcut210[:,0],gridcut210[:,1],gridcut210[:,2],pos210[:,0],pos210[:,1],pos210[:,2])
