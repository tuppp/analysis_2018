import pandas as pd
import numpy as np
import sys

#sys.path.append("C:/Users/Lukas Tilmann/mkp_database")
sys.path.append('/Users/kyrak/PycharmProjects/MKP/')


import FunctionLibraryExtended as fl

dwd, se = fl.getConnectionDWD()

acc, se_acc = fl.getConnectionAccuweathercom()

op, se_op = fl.getConnectionOpenWeatherMaporg()

wc, se_wc = fl.getConnectionWettercom()

wd, se_wd  = fl.getConnectionWetterdienstde()





'''
Data available - copied from Slack:
1 - es gibt einen Eintrag
0 - Null
				        accuweather	openweathermapporg	wettercom	wetterdienstde

measure_date			        1		    1			        1		1
measure_date_hour		        1		    1			        1		1
measure_date_prediction		    1		    1			        1		1
measure_date_prediction_hour	1		    1			        1		1
postcode			            0		    1                   1		1
city				            1		    1			        0		0
temp				            0		    1			        0		0
humidity_prob			        1		    0			        1		0
precipitation_amount		    1		    0			        1		0
precipitation_type		        0		    0			        0		0
wind_speed			            1		    1			        0		0
air_pressure_ground		        0		    1			        0		0
air_pressure_sea		        0		    0			        0		0
max_temp			            1		    1			        1		1
min_temp			            1		    1			        1		1
sun_hours			            1		    0			        1		0
clouds				            1		    0			        0		0
'''






'''
Queries: DWD
1.max_temp
2.min_temp
3.coverage_amount
4.average_wind_speed
5.precipitation_amount
6.sun_hours
7. relative_himidity 
8.air_pressure

'''
dwd_data_query_max_temp = se.execute("SELECT measure_date, max_temp, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_min_temp = se.execute("SELECT measure_date, min_temp, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_coverage_amount = se.execute("SELECT measure_date, coverage_amount, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_average_wind_speed = se.execute("SELECT measure_date, average_wind_speed, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_precipitation_amount = se.execute("SELECT measure_date, precipitation_amount, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_sun_hours = se.execute("SELECT measure_date, sun_hours, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_relative_himidity = se.execute("SELECT measure_date, relative_himidity, postcode FROM dwd WHERE measure_date > 20180522")
dwd_data_query_air_pressure = se.execute("SELECT measure_date, air_pressure, postcode FROM dwd WHERE measure_date > 20180522 and air_pressure")



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




'''Queries: Openweathermaporg (owmo)
1.max_temp
2.min_temp
3.air_pressure_ground
4.wind_speed
'''

omwo_data_query_max_temp = se.execute("SELECT measure_date_prediction, min_temp as max_temp, postcode FROM openweathermaporg WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))
omwo_data_query_min_temp = se.execute("SELECT measure_date_prediction, max_temp as  min_temp, postcode FROM openweathermaporg WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))
omwo_data_query_air_pressure_ground = se.execute("SELECT measure_date_prediction, air_pressure_ground, postcode FROM openweathermaporg WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))
omwo_data_query_wind_speed = se.execute("SELECT measure_date_prediction, wind_speed, postcode FROM openweathermaporg WHERE measure_date_prediction > 20180522   and postcode <> -1 AND measure_date_prediction - measure_date = " + str(diff))


'''Queries: wettercom 
1.max_temp
2.min_temp
4.sun_hours
5.precipitation_amount
6.humidity_prob
'''

wettercom_data_query_max_temp = se.execute("SELECT measure_date_prediction, min_temp as max_temp, postcode FROM wettercom WHERE measure_date_prediction > 20180522 and postcode <> -1 AND measure_date_prediction - measure_date = " + str(diff))
wettercom_data_query_min_temp = se.execute("SELECT measure_date_prediction, max_temp as min_temp,postcode FROM wettercom WHERE measure_date_prediction > 20180522  and postcode <> -1 AND measure_date_prediction - measure_date = " + str(diff))
wettercom_data_query_sun_hours = se.execute("SELECT measure_date_prediction, sun_hours, postcode FROM wettercom WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))
wettercom_data_precipitation_amount = se.execute("SELECT measure_date_prediction, precipitation_amount, postcode FROM wettercom WHERE measure_date_prediction > 20180522   and postcode <> -1 AND measure_date_prediction - measure_date = " + str(diff))
wettercom_data_humidity_prob = se.execute("SELECT measure_date_prediction, humidity_prob, postcode FROM wettercom WHERE measure_date_prediction > 20180522   and postcode <> -1 AND measure_date_prediction - measure_date = " + str(diff))

'''
Queries: wetterdienstde
1.max_temp
2.min_temp
'''
wetterdienstde_data_query_max_temp = se.execute("SELECT measure_date_prediction, min_temp as max_temp , postcode FROM wetterdienstde   WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))
wetterdienstde_data_query_min_temp = se.execute("SELECT measure_date_prediction, max_temp as min_temp , postcode FROM wetterdienstde   WHERE measure_date_prediction > 20180522  and postcode <> -1  AND measure_date_prediction - measure_date = " + str(diff))




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
dwd_data_max_temp = fl.getResult(dwd_data_query_max_temp, se)
dwd_df_max_temp = pd.DataFrame(dwd_data_max_temp, columns=("date", "max_temp", "postcode"))
dwd_df_max_temp.to_csv("dwd_data_max_temp.csv", columns=("date", "max_temp", "postcode"), header=True)

'''
2.min_temp
'''

dwd_data_min_temp = fl.getResult(dwd_data_query_min_temp, se)
dwd_df_min_temp = pd.DataFrame(dwd_data_min_temp, columns=("date", "min_temp", "postcode"))
dwd_df_min_temp.to_csv("dwd_data_min_temp.csv", columns=("date", "min_temp", "postcode"), header=True)


'''
3.coverage_amount
'''

dwd_data_coverage_amount = fl.getResult(dwd_data_query_coverage_amount, se)
dwd_df_coverage_amount = pd.DataFrame(dwd_data_coverage_amount, columns=("date", "coverage_amount", "postcode"))
dwd_df_coverage_amount.to_csv("dwd_data_coverage_amount.csv", columns=("date", "coverage_amount", "postcode"), header=True)

'''
4.average_wind_speed
'''

dwd_data_average_wind_speed = fl.getResult(dwd_data_query_average_wind_speed, se)
dwd_df_average_wind_speed = pd.DataFrame(dwd_data_average_wind_speed, columns=("date", "average_wind_speed", "postcode"))
dwd_df_average_wind_speed.to_csv("dwd_data_average_wind_speed.csv", columns=("date", "average_wind_speed", "postcode"), header=True)

'''
5.precipitation_amount
'''

dwd_data_precipitation_amount = fl.getResult(dwd_data_query_precipitation_amount, se)
dwd_df_precipitation_amount = pd.DataFrame(dwd_data_precipitation_amount, columns=("date", "precipitation_amount", "postcode"))
dwd_df_precipitation_amount.to_csv("dwd_data_precipitation_amount.csv", columns=("date", "precipitation_amount", "postcode"), header=True)

'''
6.sun_hours
'''

dwd_data_sun_hours = fl.getResult(dwd_data_query_sun_hours, se)
dwd_df_sun_hours = pd.DataFrame(dwd_data_sun_hours, columns=("date", "sun_hours", "postcode"))
dwd_df_sun_hours.to_csv("dwd_data_sun_hours.csv", columns=("date", "sun_hours", "postcode"), header=True)

'''
7.relative_himidity
'''

dwd_data_relative_himidity = fl.getResult(dwd_data_query_relative_himidity, se)
dwd_df_relative_himidity = pd.DataFrame(dwd_data_relative_himidity, columns=("date", "relative_himidity", "postcode"))
dwd_df_relative_himidity.to_csv("dwd_data_relative_himidity.csv", columns=("date", "relative_himidity", "postcode"), header=True)

'''air_pressure
'''

dwd_data_relative_air_pressure = fl.getResult(dwd_data_query_air_pressure, se)
dwd_df_relative_air_pressure = pd.DataFrame(dwd_data_relative_air_pressure, columns=("date", "air_pressure", "postcode"))
dwd_df_relative_air_pressure.to_csv("dwd_data_air_pressure.csv", columns=("date", "air_pressure", "postcode"), header=True)


'''
Accuweathercom Query Results
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




'''Queries: Openweathermaporg (owmo) Results
1.max_temp
2.min_temp
3.air_pressure_ground
4.wind_speed
5.humidity_prob
'''
owmo_data_max_temp = fl.getResult(omwo_data_query_max_temp, se)
owmo_df_max_temp = pd.DataFrame(owmo_data_max_temp)
owmo_df_max_temp.columns = ("date", "max_temp", "postcode")
owmo_df_max_temp.to_csv("owmo_data_max_temp.csv", columns=("date", "max_temp", "postcode"))



owmo_data_min_temp = fl.getResult(omwo_data_query_min_temp, se)
owmo_df_min_temp = pd.DataFrame(owmo_data_min_temp)
owmo_df_min_temp.columns = ("date", "min_temp", "postcode")
owmo_df_min_temp.to_csv("owmo_data_min_temp.csv", columns=("date", "min_temp", "postcode"))


owmo_data_air_pressure_ground = fl.getResult(omwo_data_query_air_pressure_ground, se)
owmo_df_air_pressure_ground = pd.DataFrame(owmo_data_air_pressure_ground)
owmo_df_air_pressure_ground.columns = ("date", "air_pressure", "postcode")
owmo_df_air_pressure_ground.to_csv("owmo_data_air_pressure_ground.csv", columns=("date", "air_pressure", "postcode"))


owmo_data_wind_speed = fl.getResult(omwo_data_query_wind_speed, se)
owmo_df_air_wind_speed = pd.DataFrame(owmo_data_wind_speed)
owmo_df_air_wind_speed.columns = ("date", "wind_speed", "postcode")
owmo_df_air_wind_speed.to_csv("owmo_data_wind_speed.csv", columns=("date", "wind_speed", "postcode"))




'''Queries: wettercom 
1.max_temp
2.min_temp
4.sun_hours
5.precipitation_amount
6.humidity_prob
'''

wettercom_data_max_temp = fl.getResult(wettercom_data_query_max_temp, se)
wettercom_df_max_temp = pd.DataFrame(wettercom_data_max_temp)
wettercom_df_max_temp.columns = ("date", "max_temp", "postcode")
wettercom_df_max_temp.to_csv("wettercom_data_max_temp.csv", columns=("date", "max_temp", "postcode"))



wettercom_data_min_temp = fl.getResult(wettercom_data_query_min_temp, se)
wettercom_df_min_temp = pd.DataFrame(wettercom_data_min_temp)
wettercom_df_min_temp.columns = ("date", "min_temp", "postcode")
wettercom_df_min_temp.to_csv("wettercom_data_min_temp.csv", columns=("date", "min_temp", "postcode"))


wettercom_data_sun_hours = fl.getResult(wettercom_data_query_sun_hours, se)
wettercom_df_sun_hours = pd.DataFrame(wettercom_data_sun_hours)
wettercom_df_sun_hours.columns = ("date", "sun_hours", "postcode")
wettercom_df_sun_hours.to_csv("wettercom_data_sun_hours.csv", columns=("date", "sun_hours", "postcode"))


wettercom_data_precipitation_amount = fl.getResult(wettercom_data_precipitation_amount, se)
wettercom_df_precipitation_amount = pd.DataFrame(wettercom_data_precipitation_amount)
wettercom_df_precipitation_amount.columns = ("date", "precipitation_amount", "postcode")
wettercom_df_precipitation_amount.to_csv("wettercom_data_precipitation_amount.csv", columns=("date", "precipitation_amount", "postcode"))

'''
Queries: wetterdienstde
1.max_temp
2.min_temp
'''

wetterdienstde_data_max_temp = fl.getResult(wetterdienstde_data_query_max_temp, se)
wetterdienstde_df_max_temp = pd.DataFrame(wetterdienstde_data_max_temp)

wetterdienstde_df_max_temp.columns = ("date", "max_temp", "postcode")
wetterdienstde_df_max_temp.to_csv("wetterdienstde_data_max_temp.csv", columns=("date", "max_temp", "postcode"))



wetterdienstde_data_min_temp = fl.getResult(wetterdienstde_data_query_min_temp, se)
wetterdienstde_df_min_temp = pd.DataFrame(wetterdienstde_data_min_temp)
wetterdienstde_df_min_temp.columns = ("date", "min_temp", "postcode")
wetterdienstde_df_min_temp.to_csv("wetterdienstde_data_min_temp.csv", columns=("date", "min_temp", "postcode"))


