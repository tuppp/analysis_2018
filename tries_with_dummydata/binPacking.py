import pandas as pd
import numpy as np
import random as rand
import pdb
import scipy as sp

'''
def bin_packing_error_rain(preds, ac, nbin=4.0):
    ress = []   
    res = []
    for x in range(nbin):
        #xpdb.set_trace()
        lower = x/float(nbin)
        upper = (x+1)/float(nbin)
        #ress =ress + [ac[(preds < lower) & (preds> upper)]] 
        ress.append(ac[(preds < upper) & (preds> lower)])
        print(ress[x])
        print(((np.sum(ress[x]==1))))
        res.append(((np.sum(ress[x]==1))*nbin)/float(len(ac)) )
        #print(res)
    return res


#preds2 = np.random.uniform(size=10000000)
#ac2 =  np.random.binomial(1, preds2)


print(bin_packing_error_rain(preds2, ac2, 5))


def tilmann_formel(act, nbin=4):
    if(act.shape != nbin):
        raise Exception
    anybinmean[i] =1/2 *nbin + i/nbin
    (np.sum(abs( anybinmean[i]- act[i])) ) / np.sum(2* anybinmean[i] - 1)


preds2 = np.random.uniform(size=10)
np.arange(1000).(lambda k : k = np.random.binomial(1, preds2))
ac2 =  np.random.binomial(1, preds2)
'''

array = np.random.rand(10000000,10)

act = np.random.binomial(1, array)

print((np.absolute(act.sum(axis=1)-5)).mean())