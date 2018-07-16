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

for x in ("accuweathercom", "openweathermaporg", "wettercom", "wetterdienstde"):
    download("min_temp_" + x + "_diff3.csv", 3, x, "min_temp")





