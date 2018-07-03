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



coverage_amount_index = 2
cloud_index = 3

def cloud_select(weatherapp):

    if weatherapp == 'accuweathercom':
        accuweather_compare_query = se2.execute('select dwd.postcode, dwd.measure_date, coverage_amount, clouds from dwd, openweathermaporg where clouds <> NULL and coverage_amount <> NULL and dwd.measure_date = openweathermaporg.measure_date and dwd.postcode <> openweathermaporg.postcode');
        cloud_compare = fle.getResult(se2, accuweather_compare_query)
    elif weatherapp == 'openweathermaporg':
        openweather_compare_query = se3.execute(
        'select dwd.postcode, dwd.measure_date, coverage_amount, clouds from dwd, openweathermaporg where clouds <> NULL and coverage_amount <> NULL and dwd.measure_date = openweathermaporg.measure_date and dwd.postcode <> openweathermaporg.postcode');
        cloud_compare = fle.getResult(se3, openweather_compare_query)
    elif weatherapp == 'wettercom':
        wettercom_compare_query = se4.execute(
        'select dwd.postcode, dwd.measure_date, coverage_amount, clouds from dwd, openweathermaporg where clouds <> NULL and coverage_amount <> NULL and dwd.measure_date = openweathermaporg.measure_date and dwd.postcode <> openweathermaporg.postcode');
        cloud_compare = fle.getResult(se4, wettercom_compare_query)
    elif weatherapp == 'wetterde':
        wetterde_compare_query = se5.execute(
        'select dwd.postcode, dwd.measure_date, coverage_amount, clouds from dwd, openweathermaporg where clouds <> NULL and coverage_amount <> NULL and dwd.measure_date = openweathermaporg.measure_date and dwd.postcode <> openweathermaporg.postcode');
        cloud_compare = fle.getResult(se5, wetterde_compare_query)
    else:
        wetterdienstde_compare_query = se6.execute(
        'select dwd.postcode, dwd.measure_date, coverage_amount, clouds from dwd, openweathermaporg where clouds <> NULL and coverage_amount <> NULL and dwd.measure_date = openweathermaporg.measure_date and dwd.postcode <> openweathermaporg.postcode');
        cloud_compare = fle.getResult(se6, wetterdienstde_compare_query)

    cloud_diff(cloud_compare)
    cloud_spearman(cloud_compare)
    clouds_mean_square_error(cloud_compare)
    return cloud_compare






def cloud_convert_dwd(dwd_waetherapp_query_result):
    for object in dwd_waetherapp_query_result:
        object[coverage_amount_index] = np.round(coverage_amount_index)


def cloud_convert_weather_app(dwd_waetherapp_query_result):

    intervall_length = 100/9
    intervall_ends = 100/9/2

    for weather_cloud in dwd_waetherapp_query_result:
        if weather_cloud[cloud_index] == 'NULL':
            continue
        weather_cloud[cloud_index] = weather_cloud[16]/9
        if weather_cloud[cloud_index] <= intervall_ends:
            weather_cloud[cloud_index] = 0
        elif intervall_ends  < weather_cloud[16] <= intervall_ends + intervall_length:
            weather_cloud[cloud_index] = 1
        elif intervall_ends + intervall_length < weather_cloud[16] <= intervall_ends + intervall_length*2:
            weather_cloud[cloud_index] = 2
        elif intervall_ends + intervall_length*2 < weather_cloud[16] <= intervall_ends + intervall_length*3:
            weather_cloud[cloud_index] = 3
        elif intervall_ends + intervall_length*3 < weather_cloud[16] <= intervall_ends + intervall_length * 4:
            weather_cloud[cloud_index] = 4
        elif intervall_ends + intervall_length * 4 < weather_cloud[16] <= intervall_ends + intervall_length * 5:
            weather_cloud[cloud_index] = 5
        elif intervall_ends + intervall_length * 5 < weather_cloud[16] <= intervall_ends + intervall_length * 6:
            weather_cloud[cloud_index] = 6
        elif intervall_ends + intervall_length * 6 < weather_cloud[16] <= intervall_ends + intervall_length * 7:
            weather_cloud[cloud_index] = 7
        elif intervall_ends + intervall_length * 7 < weather_cloud[16] <= intervall_ends*2 + intervall_length * 8:
            weather_cloud[cloud_index] = 8


def cloud_diff(dwd_waetherapp_query_result):
    for object in dwd_waetherapp_query_result:
        cloud_diff = object[coverage_amount_index]- object[cloud_index]
        dwd_waetherapp_query_result.append(cloud_diff)


def clouds_mean_square_error(dwd_waetherapp_query_result):
    clouds_rmse = 0
    for object in dwd_waetherapp_query_result:
        coverage_amount = object[coverage_amount_index]
        clouds = object[cloud_index]
        clouds_rmse = clouds_rmse+(((coverage_amount-clouds)**2))
    clouds_rmse = np.sqrt(clouds_rmse / len(dwd_waetherapp_query_result))
    dwd_waetherapp_query_result.append(clouds_rmse)



def cloud_spearman(dwd_waetherapp_query_result):
    cloud_list = dwd_waetherapp_query_result[:, cloud_index]
    coverage_amount_list  =dwd_waetherapp_query_result[:, coverage_amount_index]
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
