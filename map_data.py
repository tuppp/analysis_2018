import pandas as pd
import numpy as np
import scipy as sc
from scipy import stats


#postcodescities = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/city_to_zipcode.dat")
postcodescities = pd.read_csv("city_to_zipcode.dat")
#dwd_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_data_max_temp = pd.read_csv("dwd_data_max_temp.csv")
dwd_data_min_temp = pd.read_csv("dwd_data_min_temp.csv")
dwd_data_coverage_amount = pd.read_csv("dwd_data_coverage_amount.csv")
dwd_data_average_wind_speed = pd.read_csv("dwd_data_average_wind_speed.csv")



'''
Accuwaether Analysation for max_temp, min_temp, clouds, wind_speed
'''
#acc_data = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/acc_data.csv")
acc_data_max_temp = pd.read_csv("acc_data_max_temp.csv")
acc_data_min_temp = pd.read_csv("acc_data_min_temp.csv")
acc_data_clouds = pd.read_csv("acc_data_clouds.csv")
acc_data_wind_speed =pd.read_csv("acc_data_wind_speed.csv")



mapped_max_temp = pd.merge(dwd_data_max_temp, postcodescities, on="postcode")
doublemap_max_temp = pd.merge(mapped_max_temp, acc_data_max_temp, on=("city", "date"))
acc_mapped_max_temp = pd.merge(acc_data_max_temp, postcodescities, on="city")

mapped_min_temp = pd.merge(dwd_data_min_temp, postcodescities, on="postcode")
doublemap_min_temp = pd.merge(mapped_min_temp, acc_data_min_temp, on=("city", "date"))
acc_mapped_min_temp = pd.merge(acc_data_min_temp, postcodescities, on="city")


mapped_clouds = pd.merge(dwd_data_coverage_amount, postcodescities, on="postcode")
doublemap_clouds = pd.merge(mapped_clouds, acc_data_clouds, on=("city", "date"))
acc_mapped_clouds = pd.merge(acc_data_clouds, postcodescities, on="city")

mapped_wind_speed = pd.merge(dwd_data_average_wind_speed, postcodescities, on="postcode")
doublemap_wind_speed = pd.merge(mapped_wind_speed, acc_data_wind_speed, on=("city", "date"))
acc_mapped_wind_speed = pd.merge(acc_data_wind_speed, postcodescities, on="city")

print('max:',doublemap_max_temp)
print('min_',doublemap_min_temp)
#print(acc_mapped)
#print(mapped)
#print(doublemap)
#doublemap.to_csv("mapped_data_accuweather.csv")

#for index, row in doublemap_max_temp.iterrows():
#    print(row["max_temp_x"], row["max_temp_y"])

max_temp = doublemap_max_temp["max_temp_x"]
max_temp_prediction = doublemap_max_temp["max_temp_y"]
means_squared_error_max_temp = ((max_temp - max_temp_prediction)**2).mean()
systematic_error = (abs(max_temp - max_temp_prediction)).mean()
unsystematic_error = ((max_temp - max_temp_prediction) ** 2).mean()
print("mse_max_temp: " + str(means_squared_error_max_temp))


min_temp = doublemap_min_temp["min_temp_x"]
min_temp_prediction = doublemap_min_temp["min_temp_y"]
means_squared_error_min_temp = ((min_temp - min_temp_prediction)**2).mean()
systematic_error_min_temp = (abs(min_temp - min_temp_prediction)).mean()
unsystematic_error_min_temp = ((min_temp - min_temp_prediction) ** 2).mean()
print("mse_min_temp: " + str(means_squared_error_min_temp))

clouds = doublemap_clouds["coverage_amount"]
clouds_prediction = doublemap_clouds["clouds"]
cloud_korr, cloud_perc = sc.stats.spearmanr(clouds, clouds_prediction)
print("Spearman_clouds: " + str(cloud_korr))


wind_speed = doublemap_wind_speed["average_wind_speed"]
wind_speed_prediction = doublemap_wind_speed["wind_speed"]
means_squared_error_wind_speed = ((wind_speed - wind_speed_prediction)**2).mean()
systematic_error_wind_speed = (abs(wind_speed - wind_speed_prediction)).mean()
unsystematic_error_wind_speed = ((wind_speed - wind_speed_prediction) ** 2).mean()
print("mse_wind_speed: " + str(means_squared_error_wind_speed))

#print(acc_mapped)

'''for index, row in acc_mapped.iterrows():
    for i, r in dwd_data.iterrows():
        #print(abs(row["postcode"] - r["postcode"]))
        if abs(row["postcode"] - r["postcode"]) < 100:
            print(str(row["postcode"]) +" and " +str(r["postcode"]))'''





