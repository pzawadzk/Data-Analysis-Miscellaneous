from setup import *

part = 'c'

#Submission
if rank == 0: fdat = open('runs/submission_%d_%d_%s.txt' % (Nfeatures, Nscores, part), 'a')

f = open('runs/clfs_%d_%d_rank_%d.pckl' % (Nfeatures, Nscores, rank), 'r')
clf = pickle.load(f)
f.close()

if rank == 0: print >>fdat, 'SUBMISSION'
headers_no_click = headers[:]
headers_no_click.remove('click')
df = pd.read_csv('data/single_line')#, names=headers_no_click)
dtypes = df.dtypes



df = pd.read_csv('data/xa%s'%part, dtype=dtypes)
df['hour'] = df['hour'].astype('int64') 

Nr, Nc = df.shape
prob = predict_proba(clf, df, rank=rank, get_y=False, Nfeatures=Nfeatures, Nscores=Nscores)
print rank, prob
comm.Barrier()
Prob = comm.gather(prob, root=0)
if rank == 0:
  Prob = np.sum(Prob, axis=0)/size
  print >>fdat, rank, 'PROB_gatherd', Prob
  df_final = pd.read_csv('data/xa%s'%part, usecols =[0], dtype=dtypes)
  df_final['click'] = np.nan
  df_final['click'] = Prob[:,1]
  df_final.to_csv('runs/PRED_%d_%d_%s.csv'%(Nfeatures, Nscores, part), float_format='%.3f', index=False)


if rank == 0: fdat.close()
