import pandas as pd
import numpy as np
import scipy as sc
from scipy import stats

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



def map(forecast_app):
    postcodescities = pd.read_csv("city_to_zipcode.dat")
    dwd_data_max_temp = pd.read_csv("dwd_data_max_temp.csv")
    dwd_data_min_temp = pd.read_csv("dwd_data_min_temp.csv")
    dwd_data_coverage_amount = pd.read_csv("dwd_data_coverage_amount.csv")
    dwd_data_average_wind_speed = pd.read_csv("dwd_data_average_wind_speed.csv")
    dwd_data_precipitation_amount = pd.read_csv("dwd_data_precipitation_amount.csv")
    dwd_data_sun_hours = pd.read_csv("dwd_data_sun_hours.csv")
    dwd_data_relative_himidity = pd.read_csv("dwd_data_relative_himidity.csv")


    if forecast_app == 'accuweathercom':
        '''
        Accuwaether Analysation for:
        1.max_temp
        2.min_temp
        3.coverage_amount
        4.wind_speed
        5.precipitation_amount
        6.sun_hours
        7.humidity_prob
        '''

        acc_data_max_temp = pd.read_csv("acc_data_max_temp.csv")
        acc_data_min_temp = pd.read_csv("acc_data_min_temp.csv")
        acc_data_clouds = pd.read_csv("acc_data_clouds.csv")
        acc_data_wind_speed =pd.read_csv("acc_data_wind_speed.csv")
        acc_data_precipitation_amount =pd.read_csv("acc_data_precipitation_amount.csv")
        acc_data_sun_hours =pd.read_csv("acc_data_sun_hours.csv")
        acc_data_humidity_prob =pd.read_csv("acc_data_humidity_prob.csv")



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

        mapped_precipitation_amount = pd.merge(dwd_data_precipitation_amount, postcodescities, on="postcode")
        doublemap_precipitation_amount = pd.merge(mapped_precipitation_amount, acc_data_precipitation_amount, on=("city", "date"))
        acc_mapped_precipitation_amount = pd.merge(acc_data_precipitation_amount, postcodescities, on="city")

        mapped_sun_hours = pd.merge(dwd_data_sun_hours, postcodescities, on="postcode")
        doublemap_sun_hours = pd.merge(mapped_sun_hours, acc_data_sun_hours, on=("city", "date"))
        acc_mapped_sun_hours = pd.merge(acc_data_sun_hours, postcodescities, on="city")

        mapped_humiditiy_prob = pd.merge(dwd_data_relative_himidity, postcodescities, on="postcode")
        doublemap_humidity_prob= pd.merge(mapped_humiditiy_prob, acc_data_humidity_prob, on=("city", "date"))
        acc_mapped_humiditiy_prob = pd.merge(acc_data_humidity_prob, postcodescities, on="city")

        rms_min_temp, diff_min_temp = min_temp_func(doublemap_min_temp)
        rms_max_temp, rms_min_temp = max_temp_func(doublemap_max_temp)
        korr, perc = cloud_func(doublemap_clouds)
        rms_wind, diff_wind =wind_func(doublemap_wind_speed)
        rms_preci, diff_preci =precipitation_func(doublemap_precipitation_amount)
        rms_sun, diff_sun = sun_hours(doublemap_sun_hours)

        return rms_min_temp, diff_min_temp, rms_max_temp, korr, perc, rms_wind, diff_wind, rms_preci, diff_preci, rms_sun, diff_sun


    '''Queries: Openweathermaporg (owmo)
    1.max_temp
    2.min_temp
    3.air_pressure_ground
    4.wind_speed
    '''
    if forecast_app == 'openweathermaporg':
        openweathermaporg_data_max_temp = pd.read_csv("owmo_data_max_temp.csv")
        openweathermaporg_data_min_temp = pd.read_csv("owmo_data_min_temp.csv")
        openweathermaporg_data_wind_speed = pd.read_csv("owmwo_data_wind_speed.csv")
        openweathermaporg_data_air_pressure = pd.read_csv("owmo_data_air_pressure.csv")

        mapped_max_temp = pd.merge(dwd_data_max_temp, postcodescities, on="postcode")
        doublemap_max_temp = pd.merge(mapped_max_temp, openweathermaporg_data_max_temp, on=("city", "date"))
        openweathermaporg_mapped_max_temp = pd.merge(openweathermaporg_data_max_temp, postcodescities, on="city")

        mapped_min_temp = pd.merge(dwd_data_min_temp, postcodescities, on="postcode")
        doublemap_min_temp = pd.merge(mapped_min_temp, openweathermaporg_data_min_temp, on=("city", "date"))
        openweathermaporg_mapped_min_temp = pd.merge(openweathermaporg_data_min_temp, postcodescities, on="city")

        mapped_wind_speed = pd.merge(dwd_data_average_wind_speed, postcodescities, on="postcode")
        doublemap_wind_speed = pd.merge(mapped_wind_speed, openweathermaporg_data_wind_speed, on=("city", "date"))
        openweathermaporg_mapped_wind_speed = pd.merge(openweathermaporg_data_wind_speed, postcodescities, on="city")

        mapped_precipitation_amount = pd.merge(dwd_data_precipitation_amount, postcodescities, on="postcode")
        doublemap_precipitation_amount = pd.merge(mapped_precipitation_amount, openweathermaporg_data_air_pressure,                                        on=("city", "date"))
        openweathermaporg_mapped_air_pressure = pd.merge(openweathermaporg_data_air_pressure, postcodescities, on="city")

        rms_min_temp, diff_min_temp = min_temp_func(doublemap_min_temp)
        rms_max_temp, diff_max_temp = max_temp_func(doublemap_max_temp)
        rms_wind, diff_wind = wind_func(doublemap_wind_speed)
        rms_pressure, diff_pressure = air_pressure_func(doublemap_precipitation_amount)

        return rms_min_temp, diff_min_temp, rms_max_temp, diff_max_temp,rms_pressure, diff_pressure, rms_wind, diff_wind

    '''Queries: wettercom 
    1.max_temp
    2.min_temp
    3.sun_hours
    4.precipitation_amount
    5.humidity_prob
    '''
    if forecast_app == 'wettercom':
        openweathermaporg_data_max_temp = pd.read_csv("openweathermaporg_data_max_temp.csv")
        openweathermaporg_data_min_temp = pd.read_csv("openweathermaporg_data_min_temp.csv")
        openweathermaporg_data_precipitation_amount = pd.read_csv("openweathermaporg_data_precipitation_amount.csv")
        openweathermaporg_data_sun_hours = pd.read_csv("openweathermaporg_data_sun_hours.csv")

        mapped_max_temp = pd.merge(dwd_data_max_temp, postcodescities, on="postcode")
        doublemap_max_temp = pd.merge(mapped_max_temp, openweathermaporg_data_max_temp, on=("city", "date"))
        openweathermaporg_mapped_max_temp = pd.merge(openweathermaporg_data_max_temp, postcodescities, on="city")

        mapped_min_temp = pd.merge(dwd_data_min_temp, postcodescities, on="postcode")
        doublemap_min_temp = pd.merge(mapped_min_temp, openweathermaporg_data_min_temp, on=("city", "date"))
        openweathermaporg_mapped_min_temp = pd.merge(openweathermaporg_data_min_temp, postcodescities, on="city")


        mapped_precipitation_amount = pd.merge(dwd_data_precipitation_amount, postcodescities, on="postcode")
        doublemap_precipitation_amount = pd.merge(mapped_precipitation_amount, openweathermaporg_data_precipitation_amount,on=("city", "date"))
        acc_mapped_precipitation_amount = pd.merge(openweathermaporg_data_precipitation_amount, postcodescities, on="city")

        mapped_sun_hours = pd.merge(dwd_data_sun_hours, postcodescities, on="postcode")
        doublemap_sun_hours = pd.merge(mapped_sun_hours, openweathermaporg_data_sun_hours, on=("city", "date"))
        openweathermaporg_mapped_sun_hours = pd.merge(openweathermaporg_data_sun_hours, postcodescities, on="city")

        #mapped_humiditiy_prob = pd.merge(dwd_data_relative_himidity, postcodescities, on="postcode")
        #doublemap_humidity_prob = pd.merge(mapped_humiditiy_prob, openweathermaporg_data_humidity_prob, on=("city", "date"))
        #openweathermaporg_mapped_humiditiy_prob = pd.merge(openweathermaporg_data_humidity_prob, postcodescities, on="city")

        rms_min_temp, diff_min_temp = min_temp_func(doublemap_min_temp)
        rms_max_temp, diff_max_temp = max_temp_func(doublemap_max_temp)
        rms_precipitation, diff_precipitation = precipitation_func(doublemap_precipitation_amount)
        rms_sun_hours, diff_sun_hours = sun_hours(doublemap_sun_hours)

        return rms_min_temp, diff_min_temp, rms_max_temp, diff_max_temp, rms_precipitation, diff_precipitation, rms_sun_hours, diff_sun_hours

    if forecast_app == 'wetterdienstde':
        acc_data_max_temp = pd.read_csv("acc_data_max_temp.csv")
        acc_data_min_temp = pd.read_csv("acc_data_min_temp.csv")


        mapped_max_temp = pd.merge(dwd_data_max_temp, postcodescities, on="postcode")
        doublemap_max_temp = pd.merge(mapped_max_temp, acc_data_max_temp, on=("city", "date"))
        acc_mapped_max_temp = pd.merge(acc_data_max_temp, postcodescities, on="city")

        mapped_min_temp = pd.merge(dwd_data_min_temp, postcodescities, on="postcode")
        doublemap_min_temp = pd.merge(mapped_min_temp, acc_data_min_temp, on=("city", "date"))
        acc_mapped_min_temp = pd.merge(acc_data_min_temp, postcodescities, on="city")

        rms_min_temp, diff_min_temp = min_temp_func(doublemap_min_temp)
        rms_max_temp, diff_max_temp=  max_temp_func(doublemap_max_temp)

        return rms_min_temp, diff_min_temp, rms_max_temp, diff_max_temp



def max_temp_func(doublemap_max_temp):
    max_temp = doublemap_max_temp["max_temp_x"]
    max_temp_prediction = doublemap_max_temp["max_temp_y"]
    means_squared_error_max_temp = ((max_temp - max_temp_prediction) ** 2).mean()
    diff_max_temp = abs(max_temp - max_temp_prediction)
    print("mse_max_temp: " + str(means_squared_error_max_temp))
    print("diff_max_temp: " + str(diff_max_temp))

    return diff_max_temp, means_squared_error_max_temp

def min_temp_func(doublemap_min_temp):
    min_temp = doublemap_min_temp["min_temp_x"]
    min_temp_prediction = doublemap_min_temp["min_temp_y"]
    means_squared_error_min_temp = ((min_temp - min_temp_prediction) ** 2).mean()
    diff_min_temp = abs(min_temp - min_temp_prediction)
    print("mse_min_temp: " + str(means_squared_error_min_temp))
    print("diff_min_temp: " + str(diff_min_temp))

    return means_squared_error_min_temp, diff_min_temp

def cloud_func(doublemap_clouds):
    clouds = doublemap_clouds["coverage_amount"]
    clouds_prediction = doublemap_clouds["clouds"]
    cloud_korr, cloud_perc = sc.stats.spearmanr(clouds, clouds_prediction)
    print("Spearman_clouds: " + str(cloud_korr))

    return cloud_korr, cloud_perc

def wind_func(doublemap_wind_speed):
    wind_speed = doublemap_wind_speed["average_wind_speed"]
    wind_speed_prediction = doublemap_wind_speed["wind_speed"]
    means_squared_error_wind_speed = ((wind_speed - wind_speed_prediction) ** 2).mean()
    diff_wind_speed = abs(wind_speed - wind_speed_prediction)
    print("mse_wind_speed: " + str(means_squared_error_wind_speed))
    print("diff_precipitation:" + str(wind_speed))

    return means_squared_error_wind_speed, diff_wind_speed


def precipitation_func(doublemap_precipitation_amount):
    precipitation_amount = doublemap_precipitation_amount["precipitation_amount_x"]
    precipitation_amount_prediction = doublemap_precipitation_amount["precipitation_amount_y"]
    means_squared_error_precipitation_amount = ((precipitation_amount - precipitation_amount_prediction) ** 2).mean()
    diff_precipitation = abs(precipitation_amount - precipitation_amount_prediction)
    print("mse_precipitation_amount: " + str(means_squared_error_precipitation_amount))
    print("diff_precipitation:" + str(diff_precipitation))

    return means_squared_error_precipitation_amount, diff_precipitation


def sun_hours(doublemap_sun_hours):
    sun_hours = doublemap_sun_hours["sun_hours_x"]
    sun_hours_prediction = doublemap_sun_hours["sun_hours_y"]
    means_squared_error_sun_hours = ((sun_hours - sun_hours_prediction) ** 2).mean()
    diff_sun_hours = abs(sun_hours - sun_hours_prediction)
    print("mse_sun_hours: " + str(means_squared_error_sun_hours))
    print("diff_sun_hours:" + str(diff_sun_hours))

    return diff_sun_hours, means_squared_error_sun_hours

def air_pressure_func(doublemap_air_pressure):
    sun_hours = doublemap_air_pressure["air_pressure_x"]
    sun_hours_prediction = doublemap_air_pressure["air_pressure_y"]
    means_squared_error_sun_hours = ((sun_hours - sun_hours_prediction) ** 2).mean()
    diff_sun_hours = abs(sun_hours - sun_hours_prediction)
    print("mse_pressures: " + str(means_squared_error_sun_hours))
    print("diff_pressure" + str(diff_sun_hours))

    return diff_sun_hours, means_squared_error_sun_hours


a, b, c, d, e, f, g, h ,j,l ,k= map('accuweathercom')

#print('rms_min_temp:',a + 'diff_min_temp:',b +'rms_max_temp:',c + 'rmsd_pressure:',d+  'diff_pressure',e + 'rms_wind:',f+ 'diff_wind',g +'diff_max:',h)