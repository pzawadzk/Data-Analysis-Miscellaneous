from setup import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0: print 'Running on', size, 'cores'

cv='learn'
N = 400
Ndrivers = len(drivers)
features = range(18)

step = Ndrivers//size + 1
start = rank * step 
end = start + step

output =  []
for d in drivers[start:end]:
  output.append(predict(d, N, features, cv=cv))

comm.Barrier()


All_output = comm.gather(output, root=0)

if rank == 0:
  data = {}
  for output in All_output:
    for d, y in output:
        data[d] = y
  print len(data.keys())
  f = open('result_%d_%d_%d_%d_mask.csv'%(nest, lr, md, N), 'w')
  print >>f, 'driver_trip,prob'
  for d in drivers:
      for i in range(200):
          print >>f, '%d_%d,%.3f'%(d, i+1, data[d][i])
  f.close()

