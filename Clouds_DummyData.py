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

"""
def main(argv):
    pass

    Base = declarative_base()
    engine = create_engine('mysql+pymysql://dwdtestuser:asdassaj14123@weather.service.tu-berlin.de/dwdtest?use_unicode=1&charset=utf8&ssl_cipher=AES128-SHA')
    Base.metadata.create_all(engine)
    Session = sqla.orm.sessionmaker()
    Session.configure(bind=engine)
    se = Session()
    # connect to database
    metadata = MetaData(engine, reflect=True)

    # Get Table
    table = metadata.tables['dwd']

    result = engine.execute("SELECT coverage_amount FROM dwd WHERE station_name LIKE 'Berlin%%'")

    for row in result:
        print('result:', row)

    print(type(result))
"""

dwd,se1 = fle.getConnectionDWD()
acc, se2  = fle.getConnectionAccuweathercom()
openW, se3 =fle.getConnectionOpenWeatherMaporg()
wetter_com , se4 = fle.getConnectionWettercom()
wetter_de, se5 = fle.getConnectionWetterde()

#shiny = fle.getPostcode(11111, dwd, se, query = "")

#tabler = se1.query(dwd).filter(dwqd.c.postcode = se2.query(acc).filter(acc.c.postcode))

#ganze_tabelle = se1.query(dwd).filter(dwd.c.postcode = acc.c.postcode)

#Test
"""
DWD - Columns
0 station_id
1 station_name
2 postcode
3 measure_date
4 quality_1
5 max_wind_speed
6 average_wind_speed
7 quality_2
8 precipitation_amount
9 precipitation_type
10 sun_hours
11 snow_height
12 coverage_amount
13 vapor_pressure
14 air_pressure
15 average_temp
16 relative_humidity
17 max_temp
18 min_temp
19 ground_min_temp
"""

dwd_info = fle.getResult(se1.query(dwd),se1)
print('dwd_clouds:', fle.getResult(se1.query(dwd),se1))

def cloud_convert_dwd(dwd_cloud):
    dwd_cloud_list = dwd_info.copy()
    for dwd_cloud in dwd_cloud_list:
        dwd_cloud[12] = np.round(dwd_cloud[12])
    return dwd_cloud_list




"""
Accuweathercom - Columns
0 measure_date                 | int(11)     | NO   | PRI | NULL    |       |
1 measure_date_hour            | int(11)     | YES  |     | NULL    |       |
2 measure_date_prediction      | int(11)     | NO   | PRI | NULL    |       |
3 measure_date_prediction_hour | int(11)     | NO   | PRI | NULL    |       |
4 postcode                     | int(11)     | NO   | PRI | NULL    |       |
5 city                         | varchar(50) | NO   | PRI | NULL    |       |
6 temp                         | float       | YES  |     | NULL    |       |
7 humidity_prob                | float       | YES  |     | NULL    |       |
8 precipitation_amount         | float       | YES  |     | NULL    |       |
9 precipitation_type           | varchar(50) | YES  |     | NULL    |       |
10 wind_speed                   | float       | YES  |     | NULL    |       | 
11 air_pressure_ground          | float       | YES  |     | NULL    |       |
12 air_pressure_sea             | float       | YES  |     | NULL    |       |
13 max_temp                     | float       | YES  |     | NULL    |       |
14 min_temp                     | float       | YES  |     | NULL    |       |
15 sun_hours                    | float       | YES  |     | NULL    |       |
16 clouds                       | varchar(50) | YES  |     | NULL    |
"""

weather_app_info = fle.getResult(se2.query(acc),se2)
print('dwd_clouds:', fle.getResult(se1.query(dwd),se1))

def cloud_convert_weather_app(weather_cloud):
    weather_cloud_list = weather_app_info.copy()

    intervall_length = 100/9
    intervall_ends = 100/9/2

    for weather_cloud in weather_cloud_list:
        if weather_cloud[16] == 'NULL':
            continue
        weather_cloud[16] = weather_cloud[16]/9
        if weather_cloud[16] <= intervall_ends:
            weather_cloud[16] = 0
        elif intervall_ends  < weather_cloud[16] <= intervall_ends + intervall_length:
            weather_cloud[16] = 1
        elif intervall_ends + intervall_length < weather_cloud[16] <= intervall_ends + intervall_length*2:
            weather_cloud[16] = 2
        elif intervall_ends + intervall_length*2 < weather_cloud[16] <= intervall_ends + intervall_length*3:
            weather_cloud[16] = 3
        elif intervall_ends + intervall_length*3 < weather_cloud[16] <= intervall_ends + intervall_length * 4:
            weather_cloud[16] = 4
        elif intervall_ends + intervall_length * 4 < weather_cloud[16] <= intervall_ends + intervall_length * 5:
            weather_cloud[16] = 5
        elif intervall_ends + intervall_length * 5 < weather_cloud[16] <= intervall_ends + intervall_length * 6:
            weather_cloud[16] = 6
        elif intervall_ends + intervall_length * 6 < weather_cloud[16] <= intervall_ends + intervall_length * 7:
            weather_cloud[16] = 7
        elif intervall_ends + intervall_length * 7 < weather_cloud[16] <= intervall_ends*2 + intervall_length * 8:
            weather_cloud[16] = 8


    return weather_cloud_list


def convert_wetterdienst(x):
    wetter_cloud_list = []
    for cloud_wetter in x:
            if cloud_wetter <= 1:
                wetter_cloud_list.append(1)
            elif cloud_wetter > 1 and cloud_wetter <= 2:
                wetter_cloud_list.append(2)
            elif cloud_wetter > 2 and cloud_wetter <= 3:
                wetter_cloud_list.append(3)
            elif cloud_wetter > 3 and cloud_wetter <= 4:
                wetter_cloud_list.append(4)
            elif cloud_wetter > 4 and cloud_wetter <= 5:
                wetter_cloud_list.append(5)
            elif cloud_wetter > 5 and cloud_wetter <= 6:
                wetter_cloud_list.append(6)
            elif cloud_wetter > 6 and cloud_wetter <= 7:
                wetter_cloud_list.append(7)
            else:
                wetter_cloud_list.append(8)
    return wetter_cloud_list

listi = []
#listi.append('a')
print(listi)

temperature_diff = []
def Temp_difference(x,y):

    for i in range(len(x)):
        temp_diff = x(i) - y(i)
        abs(temp_diff)
    return temp_diff


def mean_square(x,y):

    x_ms = np.sum(((x-y)**2))

    x_ms = np.sqrt(x_ms / len(x))

    return x_ms




mock_data_wetter = [['sonnig', 'heiter', 'wolkig', 'fast_bedeckt'],
                ['wolkig','fast_bedeckt','sonnig','heiter']]


Dahlem_dwd = np.array([6.2,5.6,6.1,6.1,6.3,5.3,5.7,7.2,8,3.4])
Dahlem_waether = np.array([29,21,49,46,47,16,54,57,54,88])



#cloudy_list = cloudy_convert_accuwaehter (Dahlem_dwd)
#print(cloudy_list)
#cloudy_list = [[0.25, 0.375, 0.625, 0.875], [0.625, 0.875, 0.25, 0.375]]


mock_data_dbd = [[6/8, 1/8, 7/8, 2/8],
                 [6/8, 1/8, 7/8, 3/8]]

#def spearman(mock_data,cloudlist):
 #   korrel = []
  #  pvall = []
   # for i in range(len(mock_data)):
    #        korr, pval = sc.stats.spearmanr(mock_data[i], cloudy_list[i])
     #       korrel.append(korr)
      #      pvall.append(pvall)
    #return korrel, pvall

#print(cloudy_spearman(mock_data_dbd, cloudy_list))
#print(sc.stats.spearmanr(mock_data_dbd, cloudy_list))

#print(spearman(mock_data_dbd,cloudy_list))


def rms(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())
###########################







#if __name__ == "__main__":
 #   main(sys.argv)
