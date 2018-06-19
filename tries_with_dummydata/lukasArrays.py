import pandas as pd
import numpy as np
import random as rand
import pdb
import scipy.stats as stat

#Calculates the  probablities of rain for a given bin size
def bin_packing_error_rain(preds, ac, nbin=4.0):
    ress = []
    res = []
    for x in range(nbin):
        #xpdb.set_trace()
        lower = x/float(nbin)
        upper = (x+1)/float(nbin)
        #ress =ress + [ac[(preds < lower) & (preds> upper)]] 
        ress.append(ac[(preds < upper) & (preds> lower)])
        #print(ress[x])
        #print(((np.sum(ress[x]==1))))
        res.append(((np.sum(ress[x]==1))*nbin)/float(len(ac)) )
        #print(res)
    return res


def create_bins(nbin=5, sbin=10):
    bins = []
    for x in range(nbin):
        bins.append(np.random.rand(10)/10 + (x/nbin))
        #print(((x/nbin) + (1/(nbin*2)))
        print(bins)
    raindata = np.random.binomial(1, bins)
    #print(raindata)
    summed = raindata.sum(axis=1)
    print(raindata.shape, summed.shape)
    print(summed)
    binpercentiles = []
    for x in range(nbin):
        binpercentiles.append(stat.binom.ppf(0.95, 10, p= (x/nbin) + (1/(nbin*2))))
        #print(x)
        #print((x/nbin) + (1/(nbin*2)))
    print(binpercentiles)

    error = 0
    
    for i in range(5):
        print("summed i", summed[i], " binperc ", binpercentiles[i])
        if (summed[i] > binpercentiles[i] or summed[i] < (10 - binpercentiles[4-i])):
            error+=1
    print(error)

preds2 = np.random.uniform(size=10000000)
ac2 =  np.random.binomial(1, preds2)


#print(bin_packing_error_rain(preds2, ac2, 5))
print(create_bins())



def tilmann_formel(act, nbin=4):
    if(act.shape != nbin):
        raise Exception
    anybinmean[i] =1/2 *nbin + i/nbin
    (np.sum(abs( anybinmean[i]- act[i])) ) / np.sum(2* anybinmean[i] - 1)

