import sys
sys.path.append('/Users/kyrak/PycharmProjects/MKP/')
import pandas as pd
import scipy as sc
from scipy import stats
import FunctionLibraryExtended as fle
import MySql
from sqlalchemy import create_engine
import FunctionLibraryExtended as fle
import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


dwd,se1 = fle.getConnectionDWD()
acc, se2  = fle.getConnectionAccuweathercom()
openW, se3 =fle.getConnectionOpenWeatherMaporg()
wetter_com , se4 = fle.getConnectionWettercom()
wetter_de, se5 = fle.getConnectionWetterde()
wetter_dienst, se6 = fle.getConnectionWetterdienstde()




"""
Queries:
1. Min_Temp
2. Max_Temp
3. Clouds
4. Wind_Speed
5. Precipitation

Functions:
1. Difference
2. RMSE
3. Spearman
"""

dwd_porperty_index = 2
app_property_index = 3

def min_temp_select(weatherapp):

    if weatherapp == 'accuweathercom':
        accuweather_compare_query = se2.execute('select dwd.postcode, dwd.measure_date, dwd.min_temp, app.min_temp from (select dwd.postcode, dwd.min_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.min_temp <> NULL) as dwd join (select sum(app.min_temp)/count(app.min_temp) as min_temp, measure_date, postcode from accuweathercom as app where app.min_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        min_temp_compare = fle.getResult(se2, accuweather_compare_query)
    elif weatherapp == 'openweathermaporg':
        openweather_compare_query = se3.execute('select dwd.postcode, dwd.measure_date, dwd.min_temp, app.min_temp from (select dwd.postcode, dwd.min_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.min_temp <> NULL) as dwd join (select sum(app.min_temp)/count(app.min_temp) as min_temp, measure_date, postcode from openweathermaporg as app where app.min_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        min_temp_compare = fle.getResult(se3, openweather_compare_query)
    elif weatherapp == 'wettercom':
        wettercom_compare_query = se4.execute('select dwd.postcode, dwd.measure_date, dwd.min_temp, app.min_temp from (select dwd.postcode, dwd.min_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.min_temp <> NULL) as dwd join (select sum(app.min_temp)/count(app.min_temp) as min_temp, measure_date, postcode from wettercom as app where app.min_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        min_temp_compare = fle.getResult(se4, wettercom_compare_query)
    elif weatherapp == 'wetterde':
        wetterde_compare_query = se5.execute('select dwd.postcode, dwd.measure_date, dwd.min_temp, app.min_temp from (select dwd.postcode, dwd.min_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.min_temp <> NULL) as dwd join (select sum(app.min_temp)/count(app.min_temp) as min_temp, measure_date, postcode from wetterde as app where app.min_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        min_temp_compare = fle.getResult(se5, wetterde_compare_query)
    else:
        wetterdienstde_compare_query = se6.execute('select dwd.postcode, dwd.measure_date, dwd.min_temp, app.min_temp from (select dwd.postcode, dwd.min_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.min_temp <> NULL) as dwd join (select sum(app.min_temp)/count(app.min_temp) as min_temp, measure_date, postcode from wetterdienstse as app where app.min_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        min_temp_compare = fle.getResult(se6, wetterdienstde_compare_query)

    if not min_temp_compare:
        diff(min_temp_compare)
        mean_square_error(min_temp_compare)
        return min_temp_compare
    else:
        print("not data to compare")

def max_temp_select(weatherapp):

    if weatherapp == 'accuweathercom':
        accuweather_compare_query = se2.execute('select dwd.postcode, dwd.measure_date, dwd.max_temp, app.max_temp from (select dwd.postcode, dwd.max_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.max_temp <> NULL) as dwd join (select sum(app.max_temp)/count(app.max_temp) as max_temp, measure_date, postcode from accuweathermaporg as app where app.max_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        max_temp_compare = fle.getResult(se2, accuweather_compare_query)
    elif weatherapp == 'openweathermaporg':
        openweather_compare_query = se3.execute('select dwd.postcode, dwd.measure_date, dwd.max_temp, app.max_temp from (select dwd.postcode, dwd.max_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.max_temp <> NULL) as dwd join (select sum(app.max_temp)/count(app.max_temp) as max_temp, measure_date, postcode from openweathermaporg as app where app.max_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        max_temp_compare = fle.getResult(se3, openweather_compare_query)
    elif weatherapp == 'wettercom':
        wettercom_compare_query = se4.execute('select dwd.postcode, dwd.measure_date, dwd.max_temp, app.max_temp from (select dwd.postcode, dwd.max_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.max_temp <> NULL) as dwd join (select sum(app.max_temp)/count(app.max_temp) as max_temp, measure_date, postcode from wettercom as app where app.max_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        max_temp_compare = fle.getResult(se4, wettercom_compare_query)
    elif weatherapp == 'wetterde':
        wetterde_compare_query = se5.execute('select dwd.postcode, dwd.measure_date, dwd.max_temp, app.max_temp from (select dwd.postcode, dwd.max_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.max_temp <> NULL) as dwd join (select sum(app.max_temp)/count(app.max_temp) as max_temp, measure_date, postcode from wetterde as app where app.max_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        max_temp_compare = fle.getResult(se5, wetterde_compare_query)
    else:
        wetterdienstde_compare_query = se6.execute(
            'select dwd.postcode, dwd.measure_date, dwd.max_temp, app.max_temp from (select dwd.postcode, dwd.max_temp, dwd.measure_date from dwd where measure_date > 20180522 and dwd.max_temp <> NULL) as dwd join (select sum(app.max_temp)/count(app.max_temp) as max_temp, measure_date, postcode from wetterdienstde as app where app.max_temp <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        max_temp_compare = fle.getResult(se6, wetterdienstde_compare_query)

    diff(max_temp_compare)
    mean_square_error(max_temp_compare)
    return max_temp_compare



def cloud_select(weatherapp):

    if weatherapp == 'accuweathercom':
        accuweather_compare_query = se2.execute('select dwd.postcode, dwd.measure_date,coverage_amount, clouds_temp from (select dwd.postcode, coverage_amount, dwd.measure_date from dwd where measure_date > 20180522 and coverage_amount <> NULL) as dwd join (select sum(app.clouds)/count(app.clouds) as clouds, measure_date, postcode from accuweathercom as app where clouds <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        cloud_compare = fle.getResult(se2, accuweather_compare_query)
    elif weatherapp == 'openweathermaporg':
        openweather_compare_query = se3.execute('select dwd.postcode, dwd.measure_date,coverage_amount, clouds_temp from (select dwd.postcode, coverage_amount, dwd.measure_date from dwd where measure_date > 20180522 and coverage_amount <> NULL) as dwd join (select sum(app.clouds)/count(app.clouds) as clouds, measure_date, postcode from openweathermaporg, as app where clouds <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        cloud_compare = fle.getResult(se3, openweather_compare_query)
    elif weatherapp == 'wettercom':
        wettercom_compare_query = se4.execute('select dwd.postcode, dwd.measure_date,coverage_amount, clouds_temp from (select dwd.postcode, coverage_amount, dwd.measure_date from dwd where measure_date > 20180522 and coverage_amount <> NULL) as dwd join (select sum(app.clouds)/count(app.clouds) as clouds, measure_date, postcode from wettercom as app where clouds <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        cloud_compare = fle.getResult(se4, wettercom_compare_query)
    elif weatherapp == 'wetterde':
        wetterde_compare_query = se5.execute('select dwd.postcode, dwd.measure_date,coverage_amount, clouds_temp from (select dwd.postcode, coverage_amount, dwd.measure_date from dwd where measure_date > 20180522 and coverage_amount <> NULL) as dwd join (select sum(app.clouds)/count(app.clouds) as clouds, measure_date, postcode from wetterde as app where clouds <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        cloud_compare = fle.getResult(se5, wetterde_compare_query)
    else:
        wetterdienstde_compare_query = se6.execute('select dwd.postcode, dwd.measure_date,coverage_amount, clouds_temp from (select dwd.postcode, coverage_amount, dwd.measure_date from dwd where measure_date > 20180522 and coverage_amount <> NULL) as dwd join (select sum(app.clouds)/count(app.clouds) as clouds, measure_date, postcode from wetterdienstde as app where clouds <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        cloud_compare = fle.getResult(se6, wetterdienstde_compare_query)

    if not cloud_compare:
        diff(cloud_compare)
        spearman(cloud_compare)
        mean_square_error(cloud_compare)
        return cloud_compare
    else:
        print("no data to compare")


def wind_speed_select(weatherapp):

    if weatherapp == 'accuweathercom':
        accuweather_compare_query = se2.execute('select dwd.postcode, dwd.measure_date, average_wind_speed, wind_speed from (select dwd.postcode, dwd.average_wind_speed, dwd.measure_date from dwd where measure_date > 20180522 and average_wind_speed <> NULL) as dwd join (select sum(wind_speed)/count(wind_speed) as wind_speed, measure_date, postcode from accuweathercom as app where wind_speed <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        wind_speed_compare = fle.getResult(se2, accuweather_compare_query)
    elif weatherapp == 'openweathermaporg':
        openweather_compare_query = se3.execute('select dwd.postcode, dwd.measure_date, average_wind_speed, wind_speed from (select dwd.postcode, dwd.average_wind_speed, dwd.measure_date from dwd where measure_date > 20180522 and average_wind_speed <> NULL) as dwd join (select sum(wind_speed)/count(wind_speed) as wind_speed, measure_date, postcode from openweathermaporg as app where wind_speed <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        wind_speed_compare = fle.getResult(se3, openweather_compare_query)
    elif weatherapp == 'wettercom':
        wettercom_compare_query = se4.execute('select dwd.postcode, dwd.measure_date, average_wind_speed, wind_speed from (select dwd.postcode, dwd.average_wind_speed, dwd.measure_date from dwd where measure_date > 20180522 and average_wind_speed <> NULL) as dwd join (select sum(wind_speed)/count(wind_speed) as wind_speed, measure_date, postcode from wettercom as app where wind_speed <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        wind_speed_compare = fle.getResult(se4, wettercom_compare_query)
    elif weatherapp == 'wetterde':
        wetterde_compare_query = se5.execute('select dwd.postcode, dwd.measure_date, average_wind_speed, wind_speed from (select dwd.postcode, dwd.average_wind_speed, dwd.measure_date from dwd where measure_date > 20180522 and average_wind_speed <> NULL) as dwd join (select sum(wind_speed)/count(wind_speed) as wind_speed, measure_date, postcode from wetterde as app where wind_speed <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        wind_speed_compare = fle.getResult(se5, wetterde_compare_query)
    else:
        wetterdienstde_compare_query = se6.execute('select dwd.postcode, dwd.measure_date, average_wind_speed, wind_speed from (select dwd.postcode, dwd.average_wind_speed, dwd.measure_date from dwd where measure_date > 20180522 and average_wind_speed <> NULL) as dwd join (select sum(wind_speed)/count(wind_speed) as wind_speed, measure_date, postcode from wetterdienstde as app where wind_speed <> NULL group by measure_date, postcode) as app on dwd.measure_date = app.measure_date')
        wind_speed_compare = fle.getResult(se6, wetterdienstde_compare_query)
    if not wind_speed_compare:
        diff(wind_speed_compare)
        mean_square_error(wind_speed_compare)
        return wind_speed_compare
    else:
        return print("not data to compare")


def cloud_convert_dwd(dwd_waetherapp_query_result):
    for object in dwd_waetherapp_query_result:
        object[dwd_porperty_index] = np.round(dwd_porperty_index)


def cloud_convert_weather_app(dwd_waetherapp_query_result):

    intervall_length = 100/9
    intervall_ends = 100/9/2

    for weather_cloud in dwd_waetherapp_query_result:
        if weather_cloud[app_property_index] == 'NULL':
            continue
        weather_cloud[app_property_index] = weather_cloud[16]/9
        if weather_cloud[app_property_index] <= intervall_ends:
            weather_cloud[app_property_index] = 0
        elif intervall_ends  < weather_cloud[16] <= intervall_ends + intervall_length:
            weather_cloud[app_property_index] = 1
        elif intervall_ends + intervall_length < weather_cloud[16] <= intervall_ends + intervall_length*2:
            weather_cloud[app_property_index] = 2
        elif intervall_ends + intervall_length*2 < weather_cloud[16] <= intervall_ends + intervall_length*3:
            weather_cloud[app_property_index] = 3
        elif intervall_ends + intervall_length*3 < weather_cloud[16] <= intervall_ends + intervall_length * 4:
            weather_cloud[app_property_index] = 4
        elif intervall_ends + intervall_length * 4 < weather_cloud[16] <= intervall_ends + intervall_length * 5:
            weather_cloud[app_property_index] = 5
        elif intervall_ends + intervall_length * 5 < weather_cloud[16] <= intervall_ends + intervall_length * 6:
            weather_cloud[app_property_index] = 6
        elif intervall_ends + intervall_length * 6 < weather_cloud[16] <= intervall_ends + intervall_length * 7:
            weather_cloud[app_property_index] = 7
        elif intervall_ends + intervall_length * 7 < weather_cloud[16] <= intervall_ends*2 + intervall_length * 8:
            weather_cloud[app_property_index] = 8


def diff(dwd_waetherapp_query_result):
    for object in dwd_waetherapp_query_result:
        cloud_diff = object[dwd_porperty_index]- object[app_property_index]
        dwd_waetherapp_query_result.append(cloud_diff)


def mean_square_error(dwd_waetherapp_query_result):
    clouds_rmse = 0
    for object in dwd_waetherapp_query_result:
        coverage_amount = object[dwd_porperty_index]
        clouds = object[app_property_index]
        clouds_rmse = clouds_rmse+(((coverage_amount-clouds)**2))
    clouds_rmse = np.sqrt(clouds_rmse / len(dwd_waetherapp_query_result))
    dwd_waetherapp_query_result.append(clouds_rmse)



def spearman(dwd_waetherapp_query_result):
    cloud_list = dwd_waetherapp_query_result[:, app_property_index]
    coverage_amount_list  =dwd_waetherapp_query_result[:, dwd_porperty_index]
    korr, pval = sc.stats.spearmanr(cloud_list, coverage_amount_list)
    dwd_waetherapp_query_result.append(korr)
    dwd_waetherapp_query_result.append(pval)




#shiny = fle.getPostcode(11111, dwd, se, query = "")
#tabler = se1.query(dwd).filter(dwqd.c.postcode = se2.query(acc).filter(acc.c.postcode))
#ganze_tabelle = se1.query(dwd).filter(dwd.c.postcode = acc.c.postcode)
#table_postcode_acc = se1.query(dwd, acc).filter(dwd.c.station_name ==  acc.c.city).filter(dwd.c.measure_date == acc.c.measure_date)
#table_postcode_opmap = se3.query(dwd, openW).filter(dwd.c.postcode ==  openW.c.postcode)
#acc_postcode = se2.query(acc).filter(acc.c.postcode != -1)
#print(acc_postcode)
#print('acc_post:', fle.getResult(table_postcode_opmap,se3))
#print('join:', fle.getResult(table_postcode,se1))
