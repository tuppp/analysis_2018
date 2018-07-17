import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import rain_analysis as rain
import analysis_functions as an




def mse(data, provider, days):

    #means_squared_error = np.mean((data["max_temp_x"] - data["max_temp_y"]) ** 2)
    #print("Means Squared Error bei " + provider +" " +str(days) + " Tage im Vorraus: " + str(means_squared_error))
    means_squared_error = (data["max_temp_x"] - data["max_temp_y"])
    return means_squared_error


postcodescities = pd.read_csv("city_to_zipcode.dat", encoding="latin1")
dwd_data = pd.read_csv("dwd_data.csv", encoding="latin1")
dwd_rain_data = pd.read_csv("dwd_rain.csv", encoding="latin1")


#op_data_1 = pd.read_csv("min_temp_openweathermaporg_diff1.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
acc_data_1 = pd.read_csv("min_temp_accuweathercom_diff1.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wcom_data_1 = pd.read_csv("min_temp_wettercom_diff1.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wdde_data_1 = pd.read_csv("min_temp_wetterdienstde_diff1.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
acc_data_2 = pd.read_csv("min_temp_accuweathercom_diff2.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wcom_data_2 = pd.read_csv("min_temp_wettercom_diff2.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wdde_data_2 = pd.read_csv("min_temp_wetterdienstde_diff2.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
acc_data_3 = pd.read_csv("min_temp_accuweathercom_diff3.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wcom_data_3 = pd.read_csv("min_temp_wettercom_diff3.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
wdde_data_3 = pd.read_csv("min_temp_wetterdienstde_diff3.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
acc_data_4 = pd.read_csv("min_temp_accuweathercom_diff4.csv", encoding="latin1").rename(columns={"min_temp":"max_temp"})
acc_data_rain = pd.read_csv("accuweather_rain.csv", encoding="latin1")


#mapped_op_1 = pd.merge(op_data_1, postcodescities, on="city")
mapped_acc_1 = pd.merge(acc_data_1, postcodescities, on="city")
mapped_wcom_1 = pd.merge(wcom_data_1, postcodescities, on="city")
mapped_acc_2 = pd.merge(acc_data_2, postcodescities, on="city")
mapped_wcom_2 = pd.merge(wcom_data_2, postcodescities, on="city")
mapped_acc_3 = pd.merge(acc_data_3, postcodescities, on="city")
mapped_wcom_3 = pd.merge(wcom_data_3, postcodescities, on="city")
mapped_acc_4 = pd.merge(acc_data_4, postcodescities, on="city")
mapped_acc_rain = pd.merge(acc_data_rain, postcodescities, on="city")

#mapped_op_1 = mapped_op_1.rename(columns={'postcode_y': 'postcode'})
mapped_acc_1 = mapped_acc_1.rename(columns= {'postcode_y': 'postcode'})
mapped_wcom_1 = mapped_wcom_1.rename(columns={'postcode_y': 'postcode'})
mapped_acc_2 = mapped_acc_2.rename(columns= {'postcode_y': 'postcode'})
mapped_wcom_2 = mapped_wcom_2.rename(columns={'postcode_y': 'postcode'})
mapped_acc_3 = mapped_acc_3.rename(columns= {'postcode_y': 'postcode'})
mapped_wcom_3 = mapped_wcom_3.rename(columns={'postcode_y': 'postcode'})
mapped_acc_4 = mapped_acc_4.rename(columns= {'postcode_y': 'postcode'})
mapped_acc_rain = mapped_acc_rain.rename(columns= {'postcode_y': 'postcode'})

#doublemap_op = pd.merge(dwd_data, mapped_op, on=("postcode", "date"))
doublemap_acc_1 = pd.merge(dwd_data, mapped_acc_1, on=("postcode", "date"))
mapped_wde_1 = pd.merge(dwd_data, wdde_data_1, on=("postcode", "date"))
doublemap_wcom_1 = pd.merge(dwd_data, mapped_wcom_1, on=("postcode", "date"))
doublemap_acc_2 = pd.merge(dwd_data, mapped_acc_2, on=("postcode", "date"))
mapped_wde_2 = pd.merge(dwd_data, wdde_data_2, on=("postcode", "date"))
doublemap_wcom_2 = pd.merge(dwd_data, mapped_wcom_2, on=("postcode", "date"))
doublemap_acc_3 = pd.merge(dwd_data, mapped_acc_3, on=("postcode", "date"))
mapped_wde_3 = pd.merge(dwd_data, wdde_data_3, on=("postcode", "date"))
doublemap_wcom_3 = pd.merge(dwd_data, mapped_wcom_3, on=("postcode", "date"))
doublemap_acc_4 = pd.merge(dwd_data, mapped_acc_4, on=("postcode", "date"))
doublemap_acc_rain = pd.merge(dwd_rain_data, mapped_acc_rain, on=("postcode", "date"))

#plt.hist(
mse_acc_diff1 = mse(doublemap_acc_1, "accuweather", 1)
mse_acc_diff2 = mse(doublemap_acc_2, "accuweather", 2)
mse_acc_diff3 = mse(doublemap_acc_3, "accu", 3)
#n = float(len(mse_acc_diff1))
plt.hist(mse_acc_diff1, bins=20, normed=True, color=(0.2, 0.4, 0.6, 0.3))
plt.hist(mse_acc_diff2, bins=20, normed=True, color=(0.4, 0.2, 0.6, 0.3))
plt.hist(mse_acc_diff3, bins=20, normed=True, color=(0.2, 0.6, 0.4, 0.3))
plt.show()
mse(doublemap_wcom_1, "wetter.com", 1)
mse(mapped_wde_1, "wetterde", 1)

mse(doublemap_acc_2, "accuweather", 2)
mse(doublemap_wcom_2, "wetter.com", 2)
mse(mapped_wde_2, "wetterde", 2)

mse(doublemap_acc_3, "accuweather", 3)
mse(doublemap_wcom_3, "wetter.com", 3)
mse(mapped_wde_3, "wetterde", 3)

#bin_val = rain.bin_packing_error_rain(doublemap_acc_rain['rain_amount_x'], doublemap_acc_rain['rain_amount_y'], 10 )


#brier = an.brier(doublemap_acc_rain['rain_amount_x'], doublemap_acc_rain['rain_amount_y'])

#print(brier)
#print(bin_val)

#for index, row in doublemap_acc_1.iterrows():
#    print(row)



#plt.boxplot(labels=["1 Tag vorher", "2 Tage vorher", "3 Tage", "4 Tage"], x=[mse(doublemap_acc_1, "accuweather", 1),mse(doublemap_acc_2, "accuweather", 2), mse(doublemap_acc_3, "accuweather", 3), mse(doublemap_acc_4, "accuweather", 4)])



#plt.savefig('plot.png')







#print(acc_mapped)

'''for index, row in acc_mapped.iterrows():
    for i, r in dwd_data.iterrows():
        #print(abs(row["postcode"] - r["postcode"]))
        if abs(row["postcode"] - r["postcode"]) < 100:
            print(str(row["postcode"]) +" and " +str(r["postcode"]))'''





