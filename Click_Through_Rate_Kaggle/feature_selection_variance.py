import pandas as pd
import pickle
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print rank
size = comm.Get_size()



def get_features(df, cols):
    """ Select unique categorical variables and return a touple (column, variable)"""
    features = []
    for h in cols:
        unique = df[h].unique()
        for u in unique:
            features.append((h, u))
    return features

def select_variance(df, features, cut_off=0.10):
    """ Select low variance features"""
    low_variance_f = []
    N = len(features)
    for item, (h, u) in enumerate(features):
        if item % (N//10): print rank, 'Progress: %.2f'% (1.0*item/N)
        value = 1*np.array(df[h]==u)
        if value.std() > cut_off:
            low_variance_f.append((h,u))
    return low_variance_f

df = pd.read_csv('test_15AA')#, names=headers, header=0, usecols = usecols)
print df.shape
df.head()

cols_with_f = [ 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']

features = get_features(df, cols_with_f)

N = len(features)
slice = N//size
start = rank*slice
end = (rank+1)*slice + N%2

low_variance = select_variance(df, features[start:end], cut_off=0.10)
low_variance = comm.gather(low_variance, root=0)

if rank == 0:
  print low_variance
  features = {}
  for low_variance_element in low_variance:
    for (h, u) in  low_variance_element:
      if h not in features.keys(): features[h] = []
      features[h].append(u)
  f = open('features_10.pckl', 'w')
  pickle.dump(features, f)
  f.close()
