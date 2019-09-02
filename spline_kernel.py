import numpy as np
import h5py
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.cluster import DBSCAN
from cal_grid_size import *
from grid_cut import *

def Wspl(distance,hspl):
  result = np.minimum(1. -1.5*(distance/hspl)**2 + 0.75*(distance/hspl)**3, 0.25*(2.-distance/hspl)**3)
  return result/(np.pi*hspl**3)

def Spline(gridcut,STEP,pos):
  arr_Dens = []
  for i in gridcut:
    dist = np.sqrt(np.sum((pos[:]-i)**2,axis=-1))
    dist = np.sort(dist)[:20]
    hspl = dist[-1]*0.5
    arr_Dens.append([i/STEP,np.sum(Wspl(dist,hspl))])
  return arr_Dens

if __name__=="__main__":

  f200 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.0.hdf5','r')
  f205 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr20.5.hdf5','r')
  f210 = h5py.File('SDSS_KIAS_VAGC/kias_vagc_Mr21.0.hdf5','r')

  # galaxies position
  pos200 = pos(f200)
  pos205 = pos(f205)
  pos210 = pos(f210)

  # read the file you calculated  
  cal_dist_f = h5py.File("output/cal_distance.hdf5",'r')

  dist200 = cal_dist_f['cal_dist200'][:]
  dist205 = cal_dist_f['cal_dist205'][:]
  dist210 = cal_dist_f['cal_dist210'][:]

  # A grid size is mean_distance + 1.5*standard deviation 
  STEP200 = dist200.mean()+ 1.5*dist200.std()
  STEP205 = dist205.mean()+ 1.5*dist205.std()
  STEP210 = dist210.mean()+ 1.5*dist210.std()

  PI = math.pi

  # Comoving distance : 59.84 Mpc/h <= d <= 388.48 Mpc/h
  gridcut205 = gridCut(81,61,47,
                       np.linspace(-40*STEP205,40*STEP205,81),np.linspace(-30*STEP205,30*STEP205,61),np.linspace(6*STEP205,52*STEP205,47),
                       59.85,388.48)
  # Comoving distance : 59.84 Mpc/h <= d <= 477.52 Mpc/h
  gridcut210 = gridCut(90,71,43,
                       np.linspace(-40*STEP210,50*STEP210,91),np.linspace(-35*STEP210,35*STEP210,71),np.linspace(3*STEP210,45*STEP210,43),
                       59.85,477.52)
  # Comoving distance : 59.84 Mpc/h <= d <= 314.23 Mpc/h
  gridcut200 = gridCut(81,63,48,
                       np.linspace(-40*STEP200,40*STEP200,81),np.linspace(-31*STEP200,31*STEP200,63),np.linspace(6*STEP200,53*STEP200,48),
                       59.85,314.23)

  # calculate the spline kernel 
  sp205 = Spline(gridcut205,STEP205,pos205)
  sp210 = Spline(gridcut210,STEP210,pos210)
  sp200 = Spline(gridcut200,STEP200,pos200)

  sp205_grid = [grid[0] for grid in sp205[:]]
  sp205_density = [dens[1] for dens in sp205[:]]

  sp210_grid = [grid[0] for grid in sp210[:]]
  sp210_density = [dens[1] for dens in sp210[:]]

  sp200_grid = [grid[0] for grid in sp200[:]]
  sp200_density = [dens[1] for dens in sp200[:]]

  # wrote the spline kernel density
  sp_f = h5py.File("output/spline_kernel.hdf5",'w')
  dataset = sp_f.create_dataset("sp_density200",data = sp200_density,dtype='f')
  dataset = sp_f.create_dataset("sp_density205",data = sp205_density,dtype='f')
  dataset = sp_f.create_dataset("sp_density210",data = sp210_density,dtype='f')
  dataset = sp_f.create_dataset("sp_pos200",data = sp200_grid,dtype='f')
  dataset = sp_f.create_dataset("sp_pos205",data = sp205_grid,dtype='f')
  dataset = sp_f.create_dataset("sp_pos210",data = sp210_grid,dtype='f')
  sp_f.close()

