import pickle
from mpi4py import MPI
import numpy as np
import pandas as pd

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
from sklearn.tree import DecisionTreeClassifier

def get_X_y(X, y, df, features_touples, indexes=None, get_y=True):
    """Converts data frame to np.array using desired features """

    if get_y: y[:] = df['click'].values

    X[:,0] = df['hour'].values % 10000
    #X[:,1] = (df['hour'].values - (df['hour'].values % 10000))/10000

    count = 1
    count_tot = 2
    for key, f in features_touples:
        if count_tot in indexes:
            X[:, count] = np.array(df[key]==f)
            count +=1
        count_tot += 1
    del df

def get_clfs(rank, Nfeatures=20, Nscores=10):
    """ Traning decision tree on a chank of data and returns predictions"""

    df = pd.read_csv('data/train_%d.csv'%rank, names=headers)
    print rank, df.shape
    np.random.seed(rank)
    fselect = np.random.choice(range(2, Nscores), Nfeatures, replace = False)
    print rank, fselect

    indexes = np.array(scores_indexes)[fselect]

    Nr, Nc  = df.shape
    Nf = len(indexes)
    X = np.zeros([Nr,Nf+1]) 
    y = np.zeros([Nr]) 

    get_X_y(X, y, df, features_touples, indexes)
    print rank, 'Xy read'
    del df
    
    if rank == 0: print 'Size of numpy array in GB:', X.nbytes/1.e9
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X, y)
    y_pred = clf.predict_proba(X)
    etmp = log_loss(y, y_pred)

    del X, y
    print 'IN error on rank:', rank, 'is', etmp
    return (clf, rank, etmp)

def predict_proba(clf, df, rank=0, get_y=True, Nfeatures=20, Nscores=10):

    np.random.seed(rank)
    fselect = np.random.choice(range(2, Nscores), Nfeatures, replace = False)

    print rank, fselect

    indexes = np.array(scores_indexes)[fselect]

    Nr, Nc  = df.shape
    Nf = len(indexes)
    X = np.zeros([Nr,Nf+1]) 
    y = np.zeros([Nr]) 

    get_X_y(X, y, df, features_touples, indexes, get_y=get_y)

    if rank == 0: print 'Size of numpy array in GB:', X.nbytes/1.e9

    y_pred = clf.predict_proba(X)
    del X

    if get_y: return y_pred, y
    else: return y_pred


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0: print 'Running on', size, 'cores'

#Feature selection
f = open('data/train', 'r')
line = f.readline()
f.close()
headers = line.strip().split(',')

f = open('features_05.pckl', 'r')
features = pickle.load(f)
f.close()

features_touples = []
for key in features.keys():
    for f in features[key]:
        features_touples.append((key,f))

f = open('scores_05.pckl', 'r')
scores = pickle.load(f)
f.close()

scores_indexes = [i for i in range(len(scores)) if scores[i]>1e-3]

Nscores = len(scores_indexes)
Nfeatures = (Nscores-2) #number of features

if rank == 0:
  fdata = open('runs/setup_%d_%d.txt' %(Nfeatures, Nscores), 'w')
  print >>fdata, 'Nscores:', Nscores
  print >>fdata, 'Nfeatures:', Nfeatures
  fdata.close()

