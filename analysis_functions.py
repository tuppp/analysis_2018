import pandas as pd
import numpy as np
import random as rand

def brier(predictions, actual):
    ((actual - predictions) ** 2).mean()

def mse(predictions, actual):
    np.absolute((actual - predictions).mean()) + ((actual - predictions) ** 2 ).mean()

def create_mockdata(size):
    preds = np.random.rand(size)
    acts = np.random.binomial(1, preds)
    return (preds, acts)
