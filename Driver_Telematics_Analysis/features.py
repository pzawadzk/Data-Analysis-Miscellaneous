import numpy as np

def get_all_features(d, ts, features, smooth_type='', masking=False):
    """Calculates features for a list of trips and a driver

          d (int): driver identifier
          t (array): list of trip identifiers
          features (dict): dictionary of features to include
          smoot_type (string): indicates type of smoothing, empty string if None
          masking (bool): remove low velocities from data
    """
    FS = []
    for t in ts:
        FS.append(get_feature(d, t, features, smooth_type, masking))
    return np.array(FS)


def get_distance(d):
    """Calculates distance from coordinates
          d (2D array): X,Y GPS coordinates
    """

    delta_d = d[1:]-d[:-1]
    return np.cumsum(np.sum(delta_d**2, axis =1)**0.5)

def get_aod(d,v):
    """Calculates centrifugal acceleration
          d (2D array): X,Y GPS coordinates
          v (1D array): velocity
    """
    x = d[:,0]
    y = d[:,1]
    
    yp = np.gradient(y)
    ypp = np.gradient(yp)
    xp = np.gradient(x)
    xpp = np.gradient(xp)
    
    kappa_inv = ((xp**2 + yp**2)**(3/2.))/abs(ypp*xp - xpp*yp)
    a_od = kappa_inv * v**2
    a_od = a_od[~np.isnan(a_od)]
    a_od = a_od[~np.isinf(a_od)]
    
    
    a_od = a_od[a_od > 1.]
    a_od = a_od[a_od < 1e9]
    
    kappa_inv = kappa_inv[~np.isnan(kappa_inv)]
    kappa_inv = kappa_inv[~np.isinf(kappa_inv)]
    
    return a_od, x, y, kappa_inv

def get_feature(d, t, features, smooth_type, masking):
    """Calculates features for a given trip and driver

          d (int): driver identifier
          t (int): trip identifier
          features (dict): dictionary of features to include
          smoot_type (string): indicates type of smoothing, empty string if None
          masking (bool): remove low velocities from data
    """
    fs = []
    d = np.genfromtxt('drivers/%d/%d%s.csv'%(d,t,smooth_type), delimiter=',', skip_header=True)
    cum_dist = get_distance(d)
    velocity = np.gradient(cum_dist)
    velocity[velocity>50] = np.percentile(velocity, 95) 

    velocity_no_mask = velocity[:]
    if masking:
      velocity = velocity[mask]
      mask= 1*(velocity<2.0)
      mask_f = mask[4:]*mask[:-4]
      mask[2:-2]= mask_f


    if len(velocity) < 10:
      velocity = np.zeros(10)

    acceler  = np.gradient(velocity)

    if features['max_dist']: fs.append(cum_dist[-1])

    if features['mean_acc']: fs.append(np.mean(acceler))
    if features['max_acc']: fs.append(np.max(acceler))
    if features['min_acc']: fs.append(np.max(acceler))
    if features['std_acc']: fs.append(np.std(acceler))

    if features['Q1_acc']: fs.append(np.percentile(acceler, 25))
    if features['Q2_acc']: fs.append(np.percentile(acceler, 50))
    if features['Q3_acc']: fs.append(np.percentile(acceler, 75))
    if features['Q13_acc']: fs.append(np.percentile(acceler, 75) - np.percentile(acceler, 25))

    if features['mean_vel']: fs.append(np.mean(velocity))
    if features['max_vel']: fs.append(np.max(velocity))
    if features['std_vel']: fs.append(np.std(velocity))

    if features['Q1_vel']: fs.append(np.percentile(velocity, 25))
    if features['Q2_vel']: fs.append(np.percentile(velocity, 50))
    if features['Q3_vel']: fs.append(np.percentile(velocity, 75))
    if features['Q13_vel']: fs.append(np.percentile(velocity, 75) - np.percentile(velocity, 25))

    sa = np.sign(acceler)
    sign_change = np.sum(1*(sa[:-1] != sa[1:]))
    if features['nstops']: fs.append(sign_change)
    if features['nstops_per_dist']: fs.append(sign_change/cum_dist[-1])

    a_od, x, y, kappa_inv = get_aod(d[1:], velocity_no_mask)

    try:
      if features['Q1_aod']: fs.append(np.log(np.percentile(a_od, 25)))
      if features['Q2_aod']: fs.append(np.log(np.percentile(a_od, 50)))
      if features['Q3_aod']: fs.append(np.log(np.percentile(a_od, 75)))
      if features['Q13_aod']: fs.append(np.log(np.percentile(a_od, 75)) -np.log(np.percentile(a_od, 25)))
    except:
      if features['Q1_aod']: fs.append(0)
      if features['Q2_aod']: fs.append(0)
      if features['Q3_aod']: fs.append(0)
      if features['Q13_aod']: fs.append(0)

    try:
      if features['Q1_kinv']: fs.append(np.log(np.percentile(kappa_inv, 25)))
      if features['Q2_kinv']: fs.append(np.log(np.percentile(kappa_inv, 50)))
      if features['Q3_kinv']: fs.append(np.log(np.percentile(kappa_inv, 75)))
      if features['Q13_kinv']: fs.append(np.log(np.percentile(kappa_inv, 75)) -np.log(np.percentile(kappa_inv, 25)))
    except:
      if features['Q1_kinv']: fs.append(0)
      if features['Q2_kinv']: fs.append(0)
      if features['Q3_kinv']: fs.append(0)
      if features['Q13_kinv']: fs.append(0)

    if features['nacc']: fs.append(np.sum(1*(acceler>1)))
    if features['ndcc']: fs.append(np.sum(1*(acceler<-1)))

    if features['nacc_d']: fs.append(np.sum(1*(acceler>1))/cum_dist[-1])
    if features['ndcc_d']: fs.append(np.sum(1*(acceler<-1))/cum_dist[-1])

    if features['deff']: fs.append(np.dot(d[-1], d[-1])**0.5/cum_dist[-1])

    if features['l']: fs.append(len(d))

    nstamp = 14
    dist = [100, 500,] + [1000*i for i in range(1,nstamp-1)]
    time = np.zeros(nstamp)-1
    velo = np.zeros(nstamp)-1
    j = 0
    for i, d in enumerate(cum_dist):
        if d > dist[j]:
            time[j] = i
            velo[j] = velocity[i]
            j += 1
        if j>=len(dist):
            break
    fs += list(time) 
    fs += list(velo)

    return fs
