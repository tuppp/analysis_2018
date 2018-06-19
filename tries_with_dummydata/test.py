import numpy as np
import pandas as pd




movies = pd.read_csv('https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/imdb_1000.csv')


#print(movies.head())


#print(movies.shape)

#print(movies)





#Postleitzahl, Timestamp, Stadt, Temperatur,  Wolkendeckung(1-7), Niederschlagswahrscheinlichkeit, Luftfeuchtigkeit, Windgeschwindigkeit, Luftdruck, min und max temperatur 
leFrame = pd.DataFrame(np.array(["Postleitzahl", "Niederschlagswahrscheinlichkeit", "Luftfeuchtigkeit", "Windgeschwindigkeit", "Luftdruck", "Min und Max Temperatur"]))

#leFrame.transpose()
print(leFrame)
jeez = pd.Panel(["Postleitzahl", "Timestamp", "Stadt", "Temperatur",  "Wolkendeckung(1-7)", "Niederschlagswahrscheinlichkeit", "Luftfeuchtigkeit", "Windgeschwindigkeit", "Luftdruck", "Min und Max Temperatur"])
print(jeez)
#leFrame.append(np.random.randint(low=0,high=40, size=12))


#print(leFrame)

'''

leFrame = pd.DataFrame(["Postleitzahl", "Timestamp", "Stadt", "Temperatur",  "Wolkendeckung(1-7)", "Niederschlagswahrscheinlichkeit", "Luftfeuchtigkeit", "Windgeschwindigkeit", "Luftdruck", "Min und Max Temperatur"])
frame = leFrame.transpose
#leFrame.append(["Postleitzahl", "Timestamp", "Stadt", "Temperatur",  "Wolkendeckung(1-7)", "Niederschlagswahrscheinlichkeit", "Luftfeuchtigkeit", "Windgeschwindigkeit", "Luftdruck", "Min und Max Temperatur"])
for x in range(1,1000):
    leFrame = leFrame.append([234,234,234,23,23,234,234,234,546])

'''




df = pd.read_csv('someGapMinderData')



df.head()

type(df)

df.colums()

df.dtypes

subset = df[['country','continent', 'year']]

subset.head()

subset = df[[1,2,3]]
#==
subset = df[range[1,3]]


df.loc[99]

#Last value finding
df.loc[df.shape[0]-1]



df.iloc[0]

#df.ix[rows, colums]
df.ix[0,'continent']
df.ix[0,1]





























