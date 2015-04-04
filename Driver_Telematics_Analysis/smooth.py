import numpy as np
from pykalman import KalmanFilter
from mpi4py import MPI
import os

def smooth(dr):    
    '''Smoothing with Kalman Filter'''
    kf = KalmanFilter()
    for t in range(1,201):
        if not os.path.exists('drivers/%d/%d_smooth.csv'%(dr,t)):
            d = np.genfromtxt('drivers/%d/%d.csv'%(dr,t), delimiter=',', skip_header=True)
            d[:,0] = kf.smooth(d[:,0])[0].T[0]
            d[:,1] = kf.smooth(d[:,1])[0].T[0]
            np.savetxt('drivers/%d/%d_smooth.csv'%(dr,t), d, delimiter=',', header='x,y', fmt='%.1f')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0: print 'Running on', size, 'cores'


drivers = list(np.loadtxt('drivers.txt', dtype=np.int16))#[:500]
Ndrivers = len(drivers)
np.random.seed(0)
np.random.shuffle(drivers) 

step = Ndrivers//size + 1
start = rank * step 
end = start + step

output =  []
for d in drivers[start:end]:
  smooth(d)
