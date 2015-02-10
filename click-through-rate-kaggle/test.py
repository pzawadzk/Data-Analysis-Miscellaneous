from setup import *

if rank == 0: fdat = open('runs/test_%d_%d.txt' % (Nfeatures, Nscores), 'w')

f = open('runs/clfs_%d_%d_rank_%d.pckl' % (Nfeatures, Nscores, rank), 'r')
clf = pickle.load(f)
f.close()

#Testing
if rank == 0: print >>fdat, 'TESTING'
df = pd.read_csv('data/train_0.csv', names=headers)
Nr, Nc = df.shape
y_pred, y = predict_proba(clf, df, rank=rank, Nfeatures=Nfeatures, Nscores=Nscores)
comm.Barrier()
Y_pred = comm.gather(y_pred, root=0)
if rank == 0:
  Y_pred = np.sum(Y_pred, axis=0)/size
  print >>fdat, 'YPRED', np.shape(Y_pred), Y_pred
  etmp = log_loss(y, Y_pred)
  print >>fdat, 'OUT OF SAMPLE ERROR', etmp


if rank == 0: fdat.close()
