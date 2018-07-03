import pandas as pd
import numpy as np

postcodescities = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/city_to_zipcode.dat")
dwd_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
acc_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/acc_data.csv")


mapped = pd.merge(dwd_data, postcodescities, on="postcode")

doublemap = pd.merge(mapped, acc_data, on="place")

acc_mapped = pd.merge(acc_data, postcodescities, on="place")

#print(doublemap)

#print(acc_mapped)

for index, row in acc_mapped.iterrows():
    for i, r in dwd_data.iterrows():
        #print(abs(row["postcode"] - r["postcode"]))
        if abs(row["postcode"] - r["postcode"]) < 100:
            print(str(row["postcode"]) +" and " +str(r["postcode"]) )





