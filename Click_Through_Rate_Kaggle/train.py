from setup import *

#Train
fdat = open('runs/train_%d_%d.txt' % (Nfeatures, Nscores), 'a')

if rank == 0: print >>fdat, 'TRAIN'
clf, r, err= get_clfs(rank, Nfeatures,Nscores)
print >>fdat, 'Rank:', rank, 'In sample error:', err

f = open('runs/clfs_%d_%d_rank_%d.pckl' % (Nfeatures, Nscores, rank), 'w')
pickle.dump(clf, f)
f.close()

fdat.close()
