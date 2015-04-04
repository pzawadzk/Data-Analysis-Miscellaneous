from setup_MPI import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0: print 'Running on', size, 'cores'

cv='learn'
N = 400
M = 0
k = 17
Ndrivers = len(drivers)
p = 0.8

step = Ndrivers//size + 1
start = rank * step 
end = start + step

features = [31, 10, 5, 30, 28, 24, 11, 20, 29, 4, 7, 25, 14, 21, 8, 12, 0, 1, 16, 6, 23, 26, 3, 17, 2, 22, 19, 18, 27, 15, 13, 9][:k]
#features = [0, 20, 30, 23, 24, 18, 25, 5]
#k=0

output =  []
for d in drivers[start:end]:
  output.append(predict_top(d, N, p=p, features=features))

comm.Barrier()


All_output = comm.gather(output, root=0)

if rank == 0:
  data = {}
  for output in All_output:
    for d, y in output:
        data[d] = y
  print len(data.keys())
  f = open('topk_%d_%.3f_%d_%d_%d_fs_%d_p_%.2f.csv'%(nest, lr, md, N, M, k, p), 'w')
  print >>f, 'driver_trip,prob'
  for d in drivers:
      #data[d] -= min(data[d])
      #data[d] /= max(data[d])
      for i in range(200):
          print >>f, '%d_%d,%.3f'%(d, i+1, data[d][i])
  f.close()
