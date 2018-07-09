import pandas as pd
import numpy as np

#postcodescities = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/city_to_zipcode.dat")
postcodescities = pd.read_csv("city_to_zipcode.dat")
#dwd_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_data = pd.read_csv("dwd_data.csv")

#acc_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/acc_data.csv")
acc_data = pd.read_csv("acc_data.csv")



mapped = pd.merge(dwd_data, postcodescities, on="postcode")

doublemap = pd.merge(mapped, acc_data, on=("city", "date"))

acc_mapped = pd.merge(acc_data, postcodescities, on="city")


#print(acc_mapped)
#print(mapped)
#print(doublemap)
#doublemap.to_csv("mapped_data_accuweather.csv")

#for index, row in doublemap.iterrows():
    #print(row["max_temp_x"], row["max_temp_y"])

max_temp = doublemap["max_temp_x"]

max_temp_prediction = doublemap["max_temp_y"]

means_squared_error = ((max_temp - max_temp_prediction)**2).mean()

systematic_error = (abs(max_temp - max_temp_prediction)).mean()

unsystematic_error = ((max_temp - max_temp_prediction) ** 2).mean()

print("mse: " + str(means_squared_error))




#print(acc_mapped)

'''for index, row in acc_mapped.iterrows():
    for i, r in dwd_data.iterrows():
        #print(abs(row["postcode"] - r["postcode"]))
        if abs(row["postcode"] - r["postcode"]) < 100:
            print(str(row["postcode"]) +" and " +str(r["postcode"]))'''





