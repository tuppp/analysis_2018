import pandas as pd
import numpy as np
import sys

sys.path.append("C:/Users/Lukas Tilmann/mkp_database")
#sys.path.append('/Users/kyrak/PycharmProjects/MKP/')


import FunctionLibraryExtended as fl

dwd, se = fl.getConnectionDWD()

acc, se_acc = fl.getConnectionAccuweathercom()

op, se_op = fl.getConnectionOpenWeatherMaporg()

#data = fl.getResult(fl.getPostcode(26197,dwd,se),se)

#data = fl.getResult(fl.getTempAvg(Dwd,se),se)

#query_2 = se_acc.query(acc).filter(acc.c.postcode==10627)

#query = se.query(dwd).filter(dwd.c.postcode==10627)

#query = se.query(dwd).select_from(dwd.c.max_temp)

#query2 = se.query(acc, dwd).filter(dwd.c.postcode==acc.c.postcode)

#query2 = se.query(op, dwd).filter(dwd.c.station_name==op.c.city).filter(dwd.c.measure_date == op.c.measure_date)

#query4 = se.query(op, dwd).filter(dwd.c.postcode==op.c.postcode)

print("query: ")
#query5 = se.query(op.c.postcode).filter(dwd.c.measure_date > 20180601).filter(dwd.c.postcode==op.c.postcode)
    #.filter(dwd.c.measure_date == op.c.measure_date_prediction)
    #.filter(dwd.c.measure_date == op.c.measure_date_prediction)

#query6 = se.execute("SELECT measure_date FROM dwd AS d WHERE d.measure_date > 20180601 ")
                    #" AND (d.measure_date == o.measure_date_prediction)")


#query7 = se.execute("SELECT dwd_recent.max_temp FROM ((Select * FROM openweathermaporg WHERE measure_date_prediction > 20180601) AS op) JOIN (SELECT * FROM dwd WHERE measure_date > 20180601) AS dwd_recent")

#query8 = se.execute("SELECT * FROM ((SELECT * FROM openweathermaporg WHERE measure_date_prediction == 20180604) AS op) JOIN ((SELECT * FROM dwd WHERE measure_date = 20180604) AS dwd_recent)")

#query9 = se.execute("SELECT dwd.max_temp, openweathermaporg.max_temp WHERE dwd.postcode == openweathermaporg.postcode AND dwd.measure_date == 20180604 AND openweathermaporg.measure_date_prediction == 20180604")
#query1 = se.execute("SELECT * FROM dwd WHERE dwd.measure_date = 20180604 AND dwd.max_temp IS NOT NULL AND (postcode = 15837 OR postcode= 55250 OR postcode= 60323 OR postcode= 26197 )")
#predictiondatesquery = se.execute("SELECT DISTINCT measure_date_prediction FROM openweathermaporg WHERE measure_date_prediction > 20180604")
#postcodequery = se.execute("SELECT DISTINCT dwd.postcode FROM dwd WHERE EXISTS (SELECT DISTINCT postcode FROM openweathermaporg) ")

#one_day_pred_query = se.execute("SELECT op.max_temp, op.postcode, op.measure_date_prediction, d.postcode, d.measure_date, d.max_temp FROM openweathermaporg AS op, dwd AS d WHERE op.measure_date_prediction - op.measure_date = 1 AND(d.postcode = 15837 OR d.postcode= 52385 OR d.postcode= 60323 OR d.postcode= 26197 ) AND d.postcode = op.postcode  ")
#dwd_dates_query = se.execute("SELECT measure_date FROM dwd WHERE EXISTS (SELECT DISTINCT measure_date_prediction FROM openweathermaporg)")



'''
Queries: DWD
1.max_temp
2.min_temp
3.coverage_amount
4.average_wind_speed
5.precipitation_amount
6.sun_hours
7. relative_himidity (ja der rechtschreibfehler steht so im dwd)
'''
dwd_data_query_max_temp = se.execute("SELECT measure_date, max_temp, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_min_temp = se.execute("SELECT measure_date, min_temp, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_coverage_amount = se.execute("SELECT measure_date, coverage_amount, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_average_wind_speed = se.execute("SELECT measure_date, average_wind_speed, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_precipitation_amount = se.execute("SELECT measure_date, precipitation_amount, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_sun_hours = se.execute("SELECT measure_date, sun_hours, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_relative_himidity = se.execute("SELECT measure_date, relative_himidity, postcode FROM dwd WHERE measure_date > 20180522")



#difference between the date where prediction was created and the date which the prediction is for
diff = 1

'''
Queries: Accuweathercom
1.max_temp
2.min_temp
3.coverage_amount
4.wind_speed
5.precipitation_amount
6.sun_hours
7.humidity_prob
'''
accuweather_data_query_max_temp = se.execute("SELECT measure_date_prediction, min_temp AS max_temp, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_min_temp = se.execute("SELECT measure_date_prediction, max_temp AS min_temp, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_clouds = se.execute("SELECT measure_date_prediction, clouds, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_wind_speed = se.execute("SELECT measure_date_prediction, wind_speed, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_precipitation_amount = se.execute("SELECT measure_date_prediction, precipitation_amount, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_sun_hours = se.execute("SELECT measure_date_prediction, sun_hours, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))
accuweather_data_query_humidity_prob = se.execute("SELECT measure_date_prediction, humidity_prob, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))

# AND d.measure_date = op.measure_date_prediction

#result = fl.getResult(one_day_pred_query, se)
#result = fl.getResult(dwd_dates_query, se)
#result = fl.getResult(se.execute("SELECT DISTINCT measure_date FROM dwd"), se)
#result = fl.getResult(postcodequery, se)


'''
Falls doch alles in eine CVS: mode = 'a'
DWD Query Results 
1.max_temp
2.min_temp
3.clouds
4.windspeed
5.precipitation_amount
6.sun_hours
7. relative_himidity (ja der rechtschreibfehler steht so im dwd)
'''

'''
1.max_temp
'''
print("start download")
dwd_data_max_temp = fl.getResult(dwd_data_query_max_temp, se)
print("download done")
print(dwd_data_max_temp)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_max_temp = pd.DataFrame(dwd_data_max_temp, columns=("date", "max_temp", "postcode"))
print(dwd_df_max_temp)
dwd_df_max_temp.to_csv("dwd_data_max_temp.csv", columns=("date", "max_temp", "postcode"), header=True)

'''
2.min_temp
'''
#print("start download")
dwd_data_min_temp = fl.getResult(dwd_data_query_min_temp, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_min_temp = pd.DataFrame(dwd_data_min_temp, columns=("date", "min_temp", "postcode"))
#print(dwd_df)
dwd_df_min_temp.to_csv("dwd_data_min_temp.csv", columns=("date", "min_temp", "postcode"), header=True)


'''
3.coverage_amount
'''
#print("start download")
dwd_data_coverage_amount = fl.getResult(dwd_data_query_coverage_amount, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_coverage_amount = pd.DataFrame(dwd_data_coverage_amount, columns=("date", "coverage_amount", "postcode"))
#print(dwd_df)
dwd_df_coverage_amount.to_csv("dwd_data_coverage_amount.csv", columns=("date", "coverage_amount", "postcode"), header=True)

'''
4.average_wind_speed
'''
#print("start download")
dwd_data_average_wind_speed = fl.getResult(dwd_data_query_average_wind_speed, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_average_wind_speed = pd.DataFrame(dwd_data_average_wind_speed, columns=("date", "average_wind_speed", "postcode"))
#print(dwd_df)
dwd_df_average_wind_speed.to_csv("dwd_data_average_wind_speed.csv", columns=("date", "average_wind_speed", "postcode"), header=True)

'''
5.precipitation_amount
'''
#print("start download")
dwd_data_precipitation_amount = fl.getResult(dwd_data_query_precipitation_amount, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_precipitation_amount = pd.DataFrame(dwd_data_precipitation_amount, columns=("date", "precipitation_amount", "postcode"))
#print(dwd_df)
dwd_df_precipitation_amount.to_csv("dwd_data_precipitation_amount.csv", columns=("date", "precipitation_amount", "postcode"), header=True)

'''
6.sun_hours
'''
#print("start download")
dwd_data_sun_hours = fl.getResult(dwd_data_query_sun_hours, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_sun_hours = pd.DataFrame(dwd_data_sun_hours, columns=("date", "sun_hours", "postcode"))
#print(dwd_df)
dwd_df_sun_hours.to_csv("dwd_data_sun_hours.csv", columns=("date", "sun_hours", "postcode"), header=True)

'''
7.relative_himidity
'''
#print("start download")
dwd_data_relative_himidity = fl.getResult(dwd_data_query_relative_himidity, se)
#print("download done")
#print(dwd_data)
#pd.DataFrame(dwd_data).to_csv("C:/Users/Lukas Tilmann/analysis_2018/dwd_data.csv")
dwd_df_relative_himidity = pd.DataFrame(dwd_data_relative_himidity, columns=("date", "arelative_himidity", "postcode"))
#print(dwd_df)
dwd_df_relative_himidity.to_csv("dwd_data_relative_himidity.csv", columns=("date", "relative_himidity", "postcode"), header=True)

'''
Accuweathercom Query 
1.max_temp
2.min_temp
3.clouds
4.wind_speed
5.precipitation_amount
6.sun_hours
7.humidity_prob
'''

'''
1.max_temp
'''
accuweather_data_max_temp = fl.getResult(accuweather_data_query_max_temp, se)
acc_df_max_temp = pd.DataFrame(accuweather_data_max_temp)
acc_df_max_temp.columns = ("date", "max_temp", "city")
acc_df_max_temp.to_csv("acc_data_max_temp.csv", columns=("date", "max_temp", "city"))

'''
2.min_temp
'''
accuweather_data_min_temp = fl.getResult(accuweather_data_query_min_temp,se)
acc_df_min_temp = pd.DataFrame(accuweather_data_min_temp)
acc_df_min_temp.columns = ("date", "min_temp", "city")
acc_df_min_temp.to_csv("acc_data_min_temp.csv", columns=("date", "min_temp", "city"))

'''
3.clouds
'''
accuweather_data_clouds = fl.getResult(accuweather_data_query_clouds,se)
acc_df_clouds = pd.DataFrame(accuweather_data_clouds)
acc_df_clouds.columns = ("date", "clouds", "city")
acc_df_clouds.to_csv("acc_data_clouds.csv", columns=("date", "clouds", "city"))

'''
4.windspeed
'''
accuweather_data_winds_peed = fl.getResult(accuweather_data_query_wind_speed,se)
acc_df_wind_speed = pd.DataFrame(accuweather_data_winds_peed)
acc_df_wind_speed.columns = ("date", "wind_speed", "city")
acc_df_wind_speed.to_csv("acc_data_wind_speed.csv", columns=("date", "wind_speed", "city"))


'''
5.precipitation_amount
'''
accuweather_data_precipitation_amount = fl.getResult(accuweather_data_query_precipitation_amount,se)
acc_df_precipitation_amount = pd.DataFrame(accuweather_data_winds_peed)
acc_df_precipitation_amount.columns = ("date", "precipitation_amount", "city")
acc_df_precipitation_amount.to_csv("acc_data_precipitation_amount.csv", columns=("date", "precipitation_amount", "city"))

'''
6.sun_hours
'''
accuweather_data_sun_hours = fl.getResult(accuweather_data_query_sun_hours,se)
acc_df_sun_hours = pd.DataFrame(accuweather_data_winds_peed)
acc_df_sun_hours.columns = ("date", "sun_hours", "city")
acc_df_sun_hours.to_csv("acc_data_sun_hours.csv", columns=("date", "sun_hours", "city"))
'''
7.7.humidity_prob
'''
accuweather_data_humidity_prob = fl.getResult(accuweather_data_query_humidity_prob,se)
acc_df_humidity_prob = pd.DataFrame(accuweather_data_humidity_prob)
acc_df_humidity_prob.columns = ("date", "humidity_prob", "city")
acc_df_humidity_prob.to_csv("acc_data_humidity_prob.csv", columns=("date", "humidity_prob", "city"))
#postcodescities = pd.read_csv("C:/Users/Lukas Tilmann/analysis_2018/city_to_zipcode.dat")

#for x in dwd_data:
   # print(x)

#for x in accuweather_data:
   # print(x)

#print(postcodescities)

#print(fl.getResult(postcodequery, se))

'''26197, 72458, 94501, 49594, 85250, 15837, 2627, 52385, 38116, 60323
15837, 60323, 26197
'''
#query6 = se.query(op.c.measure_date_prediction, dwd.measure_date).filter(query)

#query3 = se.query(acc, dwd).filter(dwd.c.postcode == acc.c.postcode).filter(dwd.c.measure_date == acc.c.measure_date)

#query3 = se.query(dwd).filter(dwd.c.postcode!=0)



#print(query5)

#print(fl.getResult(query2, se))

#print(fl.getResult(query5, se))

#print(fl.getResult(query2, se))
#print(fl.getResult(query, se))

#print(fl.getResult(query_2, se_acc))

#print(query)


