import numpy as np
import sys

sys.path.append("C:/Users/Lukas Tilmann/mkp_database")

import FunctionLibraryExtended as fl

dwd, se = fl.getConnectionDWD()
acc, se_acc = fl.getConnectionAccuweathercom()
op, se_op = fl.getConnectionOpenWeatherMaporg()
wdde, se_wd = fl.getConnectionWetterdienstde()
wde, se_wde = fl.getConnectionWetterde()
wc, se_wc = fl.getConnectionWettercom()


#creates timespan queries
dwd_timespan_query = se.execute("SELECT MAX(measure_date), MIN(measure_date) FROM dwd")
acc_timespan_query = se.execute("SELECT MAX(measure_date_prediction), MIN(measure_date_prediction) FROM accuweathercom")
op_timespan_query = se.execute("SELECT MAX(measure_date_prediction), MIN(measure_date_prediction) FROM openweathermaporg")
wdde_timespan_query = se.execute("SELECT MAX(measure_date_prediction), MIN(measure_date_prediction) FROM wetterdienstde")
wde_timespan_query = se.execute("SELECT MAX(measure_date_prediction), MIN(measure_date_prediction) FROM wetterde")
wc_timespan_query = se.execute("SELECT MAX(measure_date_prediction), MIN(measure_date_prediction) FROM wettercom")


dwd_postcodes_query = se.execute("SELECT DISTINCT postcode FROM dwd WHERE NOT postcode = -1")
acc_postcodes_query = se.execute("SELECT DISTINCT postcode FROM accuweathercom WHERE NOT postcode = -1")
op_postcodes_query = se.execute("SELECT DISTINCT postcode FROM openweathermaporg WHERE NOT postcode = -1")
wdde_postcodes_query = se.execute("SELECT DISTINCT postcode FROM wetterdienstde WHERE postcode IS NOT Null")
wde_postcodes_query = se.execute("SELECT DISTINCT postcode FROM wetterde WHERE postcode IS NOT Null")
wc_postcodes_query = se.execute("SELECT DISTINCT postcode FROM wettercom WHERE postcode IS NOT Null")



#timespan query results
dwd_timespan = fl.getResult(dwd_timespan_query, se)
acc_timespan = fl.getResult(acc_timespan_query, se)
op_timespan = fl.getResult(op_timespan_query, se)
wdde_timespan = fl.getResult(wdde_timespan_query, se)
wde_timespan = fl.getResult(wde_timespan_query, se)
wc_timespan = fl.getResult(wc_timespan_query, se)




#prints out the results from the various queries
print("dwd timespan: " + str(dwd_timespan[0,0]) + " - " + str(dwd_timespan[0,1]))
#print("dwd postcodes: ")
#print(fl.getResult(dwd_postcodes_query, se))
print("accuweather timespan: " + str(acc_timespan[0,0]) + " - " + str(acc_timespan[0,1]))
#print("accuweather postcodes: ")
#print(fl.getResult(acc_postcodes_query, se))
print("openweathermaporg timespan: " + str(op_timespan[0,0]) + " - " + str(op_timespan[0,1]))
#print("openweathermap postcodes: ")
#print(fl.getResult(op_postcodes_query, se))
print("wdde timespan: " + str(wdde_timespan[0,0]) + " - " + str(wdde_timespan[0,1]))
#print("wetterdienstde postcodes: ")
#print(fl.getResult(wdde_postcodes_query, se))
print("wde timespan: " + str(wde_timespan[0,0]) + " - " + str(wde_timespan[0,1]))
#print("wetterde postcodes: ")
#print(fl.getResult(wde_postcodes_query, se))
print("wc timespan: " + str(wc_timespan[0,0]) + " - " + str(wc_timespan[0,1]))
#print("wettercom postcodes: ")
#print(fl.getResult(wc_postcodes_query, se))








