import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import mysql.connector as sql
import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import FunctionLibraryExtended as fl


#def plotBoxPlot(avg = 'none'):
#	dwd_avgTemp = fl.getAllTempAvg(data_dwd, dwd_se)
#	wetterdienst_avgTemp = fl.getAllTempAvg(data_wetterdienst, wd_se)
#	wetterde_avgTemp = fl.getAllTempAvg(data_wetterde, we_se )

#panda data frame "translator" necessary
#spearman correlation Ordinalskala "Bewölkung"
def getSpearManCorrCloud(observation, prediction):
	print(sp.stats.spearmanr(observation, prediction))

#plots comparison of prediction and observation of DIMENSION (ylabel) in
def plotMeassuredDifferences(observation, prediction, ylbl, yscl):

	plt.plot(observation, label = 'observation', color = 'g')
	plt.plot(prediction, label = 'prediction', color = 'c')
   	#plt.figure(figsize = (5,3))
	plt.xlabel(f"time")
	plt.ylabel(f"{ylbl} in {yscl}")
	plt.grid(True)
	#fig.show()
	plt.show()

def boxPlotAvgTemp():
	'''
	dimension represents data values (columns of service provider) which will be plotted
	Plots compare dwd data with each service provider of weather data
	Not recommended to plot "cloud" because of its natural appearance (x/8)'''

	data_dwd, dwd_se = fl.getConnectionDWD()
	data_wetterdienst, wd_se = fl.getConnectionWetterdienstde()
	data_wetterde, we_se = fl.getConnectionWetterde()
	data_wettercom, wc_se = fl.getConnectionWettercom()
	data_openweather, ow_se = fl.getConnectionOpenWeatherMaporg()
	data_accuweather, aw_se = fl.getConnectionAccuweathercom()


	#session_list = [] 
	#session_list.extend([wd_se, wc_se, ow_se, aw_se])
	#table_list = []
	#table_list.extend([data_wetterdienst, data_wetterde, data_wettercom, data_openweather, data_accuweather])
	tuple_list = [(data_openweather, ow_se),(data_accuweather, aw_se), (data_wetterdienst, wd_se), (data_wetterde, we_se), (data_wettercom, wc_se)]

	dataList = []

	for (table, se) in tuple_list : 
		wetterdienst_maxTemp = fl.getResult(se.execute('SELECT max_temp FROM ' + str(table)), se)
		wetterdienst_minTemp = fl.getResult(se.execute('SELECT min_temp FROM ' + str(table)), se)
		wetterdienst_avgTemp = (wetterdienst_maxTemp*58 + wetterdienst_minTemp* 42)/100 #Juni18 überd. warm, 13 Sonnenstunden ca. => gew. Temp	
		dataList.append(wetterdienst_avgTemp)

	print(dataList[0])

	

	#data_dwd = pd.read_sql('SELECT dimension FROM dwd', con = fl.getConnectionDWD))
	#data_wetterdienst = pd.read_sql('SELECT dimension FROM wetterdienstde', con = fl.getConnectionWetterdienstde))
	#data_wetterde = pd.read_sql('SELECT dimension FROM wetterde', con = fl.getConnectionWetterde))
	#data_wettercom = pd.read_sql('SELECT dimension FROM wettercom', con = fl.getConnectionWettercom))
	#data_openweather = pd.read_sql('SELECT dimension FROM openweathermaporg', con = fl.getConnectionOpenWeatherMaporg))
	#data_accuweather = pd.read_sql('SELECT dimension FROM accuweathercom', con = fl.getConnectionAccuweathercom))
	
	dataList.append(dwd_se.execute('SELECT average_temp FROM dwd'))
	sample_query = dwd_se.execute('SELECT average_temp FROM dwd')

	FunctionLibraryExtended.getResult(sample_query, dwd_se)
#	dataList.append(pd.read_sql('SELECT average_temp FROM dwd', con = fl.getConnectionDWD()))
#	dataList.append(pd.read_sql('SELECT maxTemp FROM getConnectionWetterdienstde', con = fl.getConnectionWetterdienstde()))
#	dataList.append(pd.read_sql('SELECT maxTemp+minTemp FROM wetterde', con = fl.getConnectionWetterde()))
#	dataList.append(pd.read_sql('SELECT (maxTemp+minTemp)/2 FROM wettercom', con = fl.getConnectionWettercom()))
#	dataList.append(pd.read_sql('SELECT (maxTemp+minTemp)/2 FROM openweathermaporg', con = fl.getConnectionOpenWeatherMaporg()))
#	dataList.append(pd.read_sql('SELECT (maxTemp+minTemp)/2 FROM accuweathercom', con = fl.getConnectionAccuweathercom()))

	
	fig = plt.figure(figsize = (5,8))
	for data in dataList:
		data.plot(kind = 'box')
		fig.add_subplot(111)
		df.data.plot()


    #ax = fig.add_subplot(111)
    #bp = ax.boxplot(dataPlot)
    #ax.set_xticklabels(labels)
	fig.show()
	plt.show()

def main():
	#try:
	Base = declarative_base()
	engine = create_engine('mysql+pymysql://dwdtestuser:asdassaj14123@weather.service.tu-berlin.de/dwdtest?use_unicode=1&charset=utf8&ssl_cipher=AES128-SHA')
	Base.metadata.create_all(engine)
	Session = sqla.orm.sessionmaker()
	Session.configure(bind=engine)
	se = Session()
    	   # connect to database
	metadata = MetaData(engine, reflect=True)
	#plotMeassuredDifferences(np.arange(11), np.arange(5,14), "range", "lange")
	boxPlotAvgTemp()
	#data_wetterdienst, wd_se = fl.getConnectionWetterdienstde()
	



#data_dwd, dwd_se = fl.getConnectionDWD()
#data_wetterdienst, wd_se = fl.getConnectionWetterdienstde()
#data_wetterde, we_se = fl.getConnectionWetterde()
#data_wettercom, wc_se = fl.getConnectionWettercom()
#data_openweather, ow_se = fl.getConnectionOpenWeatherMaporg()
#data_accuweather, aw_se = fl.getConnectionAccuweathercom()

#df = pd.read_sql('SELECT * FROM table_name', con=db_connection)
#print("Postcode on Rain")
#print(fl.getResult(fl.getRain(data_wetterdienst,wd_se,fl.getPostcode(26197,data_wetterdienst,wd_se)), wd_se))


if __name__ == "__main__":
	main()
