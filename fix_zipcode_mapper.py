import pandas as pd
import numpy as np


postcodescities = pd.read_csv("city_to_zipcode.dat")
#dwd_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_data = pd.read_csv("dwd_data.csv")

#acc_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/acc_data.csv")
#acc_data = pd.read_csv("acc_data.csv")



mapped = pd.merge(dwd_data, postcodescities, on="postcode")

print(mapped)