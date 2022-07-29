import numpy as np

def discrete_uniform_distribution_weights(n,d,l_max):
    weights = np.random.randint(0,l_max+1,size=(d,n))        
    sum_column = [np.sum(i, axis=0) for i in np.transpose(weights)]
    for i in range(len(sum_column)):
        if sum_column[i] == 0:
            rand_dim = np.random.randint(0,d)
            # minmum weight is 1 if sum equals to 0
            weights[rand_dim,i] = np.random.randint(1,l_max+1)
    wei = np.array(weights)
    return wei


def discrete_uniform_distribution_values(n,d,v_min,v_max):
    values = np.random.randint(v_min,v_max+1,n)
    val = np.array(values)
    alphas = np.ones(d).astype(int)
    alp = np.array(alphas)
    return val, alp


def normal_distribution_values(n,d,weights,sigma):
    normal_factor = np.around(np.random.normal(0,sigma,n),decimals=2)
    new_sum_column = np.around([np.sum(i, axis=0) for i in np.transpose(weights)],decimals=2)
    values = new_sum_column + normal_factor
    for i in range(len(values)):
        if values[i]<=0:
            values[i]=0.01

    val = np.array(values)
    alphas = np.ones(d).astype(int)
    alp = np.array(alphas)
    return val, alp


def sum_values(n,d,weights):
    values = [np.sum(i, axis=0) for i in np.transpose(weights)]
    val = np.array(values)
    alphas = np.ones(d).astype(int)
    alp = np.array(alphas)
    return val, alp 
