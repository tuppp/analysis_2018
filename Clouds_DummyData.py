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
wetter_dienst, se6 = fle.getConnectionWetterdienstde()

#shiny = fle.getPostcode(11111, dwd, se, query = "")

#tabler = se1.query(dwd).filter(dwqd.c.postcode = se2.query(acc).filter(acc.c.postcode))

#ganze_tabelle = se1.query(dwd).filter(dwd.c.postcode = acc.c.postcode)


#table_postcode_acc = se1.query(dwd, acc).filter(dwd.c.station_name ==  acc.c.city).filter(dwd.c.measure_date == acc.c.measure_date)
#table_postcode_opmap = se3.query(dwd, openW).filter(dwd.c.postcode ==  openW.c.postcode)
#acc_postcode = se2.query(acc).filter(acc.c.postcode != -1)
#print(acc_postcode)
#print('acc_post:', fle.getResult(table_postcode_opmap,se3))
#print('hello')
#print('join:', fle.getResult(table_postcode,se1))
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
#print('dwd_clouds:', fle.getResult(se1.query(dwd),se1))
#

#resulti =  fle.getResult(se1.query(dwd),se1)
#print('Typ:', type(resulti.type))
# DWD ab 20180501
a = se1.execute('select * from dwd where measure_date > 20180501')
print('a:',fle.getResult(a,se1))
print(len(fle.getResult(a,se1)))


# Wetterdienst ab 20180501
b = se6.execute('select * from wetterdienstde where measure_date > 20180501')
print('b:',fle.getResult(b,se6))
print(len(fle.getResult(b,se6)))

#join both

c = se6.execute('select * from wetterdienstde, dwd where dwd.measure_date > 20180501 and wetterdienstde.measure_date > 20180501 and wetterdienstde.postcode = dwd.postcode')
print('c:',fle.getResult(c,se6))
print(len(fle.getResult(c,se6)))

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

weather_app_wetterdienstde = fle.getResult(se2.query(wetter_dienst),se6)
#print('dwd_clouds:', fle.getResult(se1.query(dwd),se1))

def cloud_convert_weather_app(weather_cloud):
    weather_cloud_list = weather_app_wetterdienstde.copy()

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

def cloud_diff(start_date):
    query1 = se1.execute('select * from (select * from dwd where measure_date > 20180601) as dwd1, (select * from wetterdienstde where measure_date > 20180601) as wetterdienstde1 where dwd1.measure_date = wetterdienstde1.measure_date and dwd1.postcode = wetterdienstde1.postcode')
    diff_list = fle.getResult(query1,se6)
    #Null bereinigen
    #join an date
    dwd_cloud_index = 1
    wetter_app_cloud_index = 2

    for object in diff_list:
        cloud_diffi = object[dwd_cloud_index]- object[wetter_app_cloud_index]
        diff_list.append(cloud_diffi)
    
    return diff_list


"""
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
"""


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


#def rms(predictions, targets):
#    return np.sqrt(((predictions - targets) ** 2).mean())
###########################







#if __name__ == "__main__":
 #   main(sys.argv)
