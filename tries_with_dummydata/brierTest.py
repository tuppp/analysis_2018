from sklearn.metrics import brier_score_loss
import pandas as pd
import numpy as np
import random as rand

#predictions = (np.random.rand(1000000000))

#act = np.random.binomial(1, predictions)    

#brier = ((act - predictions)**2).mean()
#brier_sk = brier_score_loss(act,predictions )
#print(brier)
#print(brier_sk)


data =  pd.read_csv("/home/paavo/ProgrammierPraktikum/accuFor.txt")
dwd_data = pd.read_csv("/home/paavo/ProgrammierPraktikum/dwd_new.txt")

preds = data.as_matrix()[:, [1,15]]
weather_data = dwd_data.as_matrix()[:,[4,18]]

dev = (preds[1] - weather_data[1]).mean() 
print(dev)

#print(preds)
#print(weather_data)
#brier = brier_score_loss(data.)





'''
ytrue = np.array([0, 1, 1, 0])
ytrue_categorical = np.array(["spam", "ham", "ham", "spam"])
yprob = np.array([0.1, 0.9, 0.8, 0.3])
print(brier_score_loss(ytrue, yprob))  
print(brier_score_loss(ytrue, 1-yprob, pos_label=0))
print(brier_score_loss(ytrue_categorical, yprob,pos_label="ham") )
print(brier_score_loss(ytrue, np.array(yprob) > 0.5))
''' 