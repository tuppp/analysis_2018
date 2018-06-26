"""
Created on Tue May 15 15:05:35 2018

@author: michaelstenzel
"""

import numpy as np
import pandas as pd
import random as rand

def randArray():
    temp = rand.randint(-10, 35)
    rainProb = rand.random()
    wind = rand.randint(0,25)
    return [temp,rainProb,wind]

def createArray(size):
    arr = randArray()
    for x in range (0,size):
        arr = np.vstack([arr, randArray()])
    return arr

# clean a panda dataframe: remove NaN
def clean(x):
    x.dropna(axis=1, how='any')

def difference(x, y):
    return x - y

# given two pandas dataframes, calculate the root mean square error
def rms(x, y):
    return (pd.DataFrame.sum((x-y)**2)/len(x)).apply(np.sqrt)


