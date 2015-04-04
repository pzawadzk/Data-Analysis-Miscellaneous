import pickle

from mpi4py import MPI
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

drivers = list(np.loadtxt('drivers.txt', dtype=np.int16))#[:500]

nest = 40
lr = 0.1
md = 3
clf = GradientBoostingClassifier(n_estimators=nest, learning_rate=lr,  max_depth=md, random_state=0, subsample =0.5)


def predict(d, N, features, p=1.0):
    """Calculates probability of a trip to belong to a driver

        d (int): driver identifier
        N (int): number of drivers avians which the probability is calculated
        features (array): list of features
        p (flot): discrimination threshold for classification
    
    """
    
    index = drivers.index(d)
    vs = np.random.choice(drivers[:index] + drivers[index+1:],N)
    
    X0 = np.genfromtxt('features/Xall_alf_%d_fs.csv'%d, delimiter=',')[:,features] 
    y_all = np.genfromtxt('result_40_0_3_2700_fs_16.csv', delimiter=',')[1:,1]

    y0 = y_all[index*200:(index+1)*200]
    mask_y0 = y0 >= p

    ypart = np.array([1,]*200 + [0,]*200)
    y_pred = np.zeros(200)

    w = 0
    for v in vs:
        Xi = np.genfromtxt('features/Xall_alf_%d_fs.csv'%v, delimiter=',')[:,features]

        index = drivers.index(v)
        yi = y_all[index*200:(index+1)*200]
        mask_yi = yi >= p

        y_outl = np.concatenate((mask_y0, mask_yi))

        Xpart = np.concatenate((X0, Xi))
    
        clf.fit(Xpart[y_outl] , ypart[y_outl])
        p = clf.predict_proba(Xpart)[:200, 1]
        y_pred +=   p 

    return (d, y_pred/N)

def predict_rand(d, N, M, features, p=1.0):
    
    np.random.seed(0)
    index = drivers.index(d)
    
    Xpart = np.genfromtxt('features/Xall_alf_%d_fs.csv'%d, delimiter=',')[:,features] 
    vs = np.random.choice(drivers[:index] + drivers[index+1:],N)
    for v in vs:
        Xi = np.genfromtxt('features/Xall_alf_%d_fs.csv'%v, delimiter=',')[:,features]
        Xpart = np.concatenate((Xpart, Xi))

    ypart = np.array([1,]*200 + [0,]*200)
    y_pred = np.zeros(200)
    for i in range(M):
      choice = np.random.random_integers(200, (N+1)*200-1, 200)
   
      mask = np.concatenate((range(200), choice)) 
      clf.fit(Xpart[mask,:], ypart)
      y_pred += clf.predict_proba(Xpart)[:200, 1]

    return (d, y_pred/M)

