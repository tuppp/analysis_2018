import pandas as pd
import numpy as np
import sys

sys.path.append("C:/Users/Lukas Tilmann/mkp_database")

import FunctionLibraryExtended as fl

dwd, se = fl.getConnectionDWD()

def download(file, diff, provider, data_type):
    query = se.execute("SELECT measure_date_prediction, postcode, city, {data_type} FROM {provider} WHERE measure_date_prediction - measure_date = {difference}".format(provider=provider, difference=diff, data_type=data_type))
    result = fl.getResult(query, se)
    print(provider)
    dataframe = pd.DataFrame(result, columns=("date", "postcode", "city", data_type))
    dataframe.to_csv(file,columns=("date", "postcode", "city", data_type), header=True)

#example of downloading and joining from a certain forecast provider

#query1 = se.execute("SELECT measure_date_prediction, city, max_temp, max_temp_prediction FROM (((SELECT measure_date, postcode, max_temp_actual FROM dwd WHERE measure_date > MIN((SELECT measure_date FROM accuweathercom) AS acc_dates)) AS dwd_data) JOIN ((((SELECT measure_date_prediction, postcode, city, max_temp_prediction FROM accuweathercom WHERE measure_date_prediction - measure_date = 1 ) AS acc) JOIN city_to_postcode ON city_to_postcode.city = acc.city) AS mapped) ON mapped.postcode =dwd_data.postcode)")

#accuweather_data_query = se.execute("SELECT measure_date_prediction, min_temp AS max_temp, city FROM accuweathercom WHERE measure_date_prediction > 20180522  AND measure_date_prediction - measure_date = " + str(diff))

print("start download")

'''for x in ("accuweathercom", "openweathermaporg", "wettercom", "wetterdienstde"):
    download("min_temp_" + x + "_diff1.csv", 1, x, "min_temp")

for x in ("accuweathercom", "openweathermaporg", "wettercom", "wetterdienstde"):
    download("min_temp_" + x + "_diff2.csv", 2, x, "min_temp")


for x in ("accuweathercom", "openweathermaporg", "wettercom", "wetterdienstde"):
    download("min_temp_" + x + "_diff5.csv",5 , x, "min_temp")
 '''

#download("min_temp_accuweathercom_diff5.csv",5 , "accuweathercom", "min_temp")
#download("accuweather_rain.csv",1 , "accuweathercom", "rain_amount")


#query = se.execute("SELECT measure_date, postcode, station_name, precipitation_amount FROM dwd WHERE measure_date > 20180520")
query = se.execute("SELECT measure_date_prediction, postcode, city, precipitation_amount FROM accuweathercom WHERE measure_date_prediction - measure_date = 1")
result = fl.getResult(query, se)
#mapper = lambda t: 1 if t is not None and float(t)>0.1 else 0
mapper = lambda t: float(t) / 100 if t is not None else 0.0
#mapped = np.apply_along_axis(mapper, axis=3, arr=result)
#mapped = np.array([mapper(xi) for xi in result])
dataframe = pd.DataFrame(result,  columns=("date", "postcode", "city", "rain_amount"))
#dataframe['rain_amount'] = dataframe["rain_amount"].apply(mapper)
dataframe['rain_amount'] = dataframe['rain_amount'].apply(mapper)
dataframe.to_csv("accuweather_rain.csv", columns=("date", "postcode", "city", "rain_amount"), header=True)
#dataframe.to_csv("dwd_rain.csv", columns=("date", "postcode", "city", "rain_amount"), header=True)
#dataframe.to_csv("wetterdienstde_rain_chance.csv", columns=("date", "postcode", "city", "rain_amount"), header=True)




