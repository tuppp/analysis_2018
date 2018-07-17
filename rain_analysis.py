import pandas as pd
import numpy as np
import random as rand
import pdb
import scipy.stats as stat

#Calculates the  probablities of rain for a given bin size
def bin_packing_error_rain(preds, ac, nbin=4.0):
    temp = []
    res = []
    #print("Predictions")
    #print(preds)
    #print("Actual")
    #print(ac)
    for x in range(nbin):
        #xpdb.set_trace()
        lower = x/nbin
        upper = (x+1)/nbin
        temp.append(ac[(preds < upper) & (preds> lower)])
        #print(ac[(preds < upper) & (preds> lower)])
        #res.append(((np.sum(temp[x]==1))*nbin)/len(ac))
        rain_day = np.sum(temp[x]==1)
        day = len(temp[x])
        npi = (((lower + upper) / 2 ) * day)
        dev = 0
        if npi != 0:
            dev = ((npi - rain_day)**2) / npi
        if day==0:
            res.append(np.nan)
        else:
            #print(day)
            #print(rain_day)
            #print(rain_day/day)
            res.append(dev)
        #res.append((0+np.sum(temp[x]==1))/(np.sum(temp[x])))
    #print(res)
    #print(temp)
    #print("Ende bin packing error")
    return stat.chi2.cdf(x=np.array(res).sum(), df=9, loc=0, scale=1)


preds2 = np.random.uniform(size=1000)
ac2 =  np.random.binomial(1, preds2)

#print(bin_packing_error_rain(preds2, ac2, 10))
#print(stat.chi2.cdf(x=bin_packing_error_rain(preds2, ac2, 10), df=9, loc=0, scale=1))
#print("Ende")
#print(create_bins())


'''
def tilmann_formel(act, nbin=4):
    if(act.shape != nbin):
        raise Exception
    anybinmean[i] =1/2 *nbin + i/nbin
    (np.sum(abs( anybinmean[i]- act[i])) ) / np.sum(2* anybinmean[i] - 1)



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
    print(error)'''