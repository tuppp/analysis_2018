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
#	dwd_avgTemp = fl.getAllTempAvg(data_dwd, dwd_ se)
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
	plt.show()

def plot_maxtemp(tuplelist = None, measure_date = None, x_day_forecast = None): 

	datalist = []
	lgnd = []

	for (table, se) in tuplelist:

		if str(table) == 'openweathermaporg' : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT max_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)
		else : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT min_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)

		lgnd.append(str(table))
	
	plot(datalist, lgnd, title = 'MaxTemp')


def plot_mintemp(tuplelist = None, measure_date = None, x_day_forecast = None): 

	datalist = []
	lgnd = [] 

	for (table, se) in tuplelist:

		if str(table) == 'openweathermaporg' : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT min_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)
		else : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT max_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)
		
		lgnd.append(str(table))
		
	plot(datalist, lgnd, title = 'MinTemp')


def boxPlot_maxtemp(tuplelist = None, measure_date = None, x_day_forecast = None):
	'''
	dimension represents data values (columns of service provider) which will be plotted
	Plots compare dwd data with each service provider of weather data
	Not recommended to plot "cloud" because of its natural appearance (x/8)'''

	datalist = []
	lgnd = []

	for (table, se) in tuplelist:

		if str(table) == 'openweathermaporg' : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT max_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast}'), se)
			datalist.append(wetterdienst_maxTemp)
		else : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT min_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)

		lgnd.append(str(table))


	boxplot(datalist, lgnd, title = 'MaxTemp')


def boxplot_mintemp(tuplelist = None, measure_date = None, x_day_forecast = None):

	'''
	dimension represents data values (columns of service provider) which will be plotted
	Plots compare dwd data with each service provider of weather data
	Not recommended to plot "cloud" because of its natural appearance (x/8)'''

	datalist = []
	lgnd = []

	for (table, se) in tuplelist:

		if str(table) == 'openweathermaporg' : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT min_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)
		else : 
			wetterdienst_maxTemp = fl.getResult(se.execute(f'SELECT max_temp FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_maxTemp)
		
		lgnd.append(str(table))

	boxplot(datalist, lgnd, title = 'MinTemp')


def boxplot_sunhours(tuplelist = None, measure_date = None, x_day_forecast = None) :

	datalist = []
	lgnd = []

	for (table, se) in tuplelist:

			wetterdienst_sunhours = fl.getResult(se.execute(f'SELECT sun_hours FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_sunhours[wetterdienst_sunhours != np.array(None)])
			lgnd.append(str(table))

	boxplot(datalist, lgnd, title = 'SunHours')


def boxplot_windspeed(tuplelist = None, measure_date = None, x_day_forecast = None) :

	datalist = []
	lgnd = []

	for (table, se) in tuplelist:

			wetterdienst_sunhours = fl.getResult(se.execute(f'SELECT wind_speed FROM {str(table)} WHERE measure_date > {str(measure_date)} and measure_date_prediction - measure_date = {x_day_forecast} '), se)
			datalist.append(wetterdienst_sunhours[wetterdienst_sunhours != np.array(None)])
			lgnd.append(str(table))

	boxplot(datalist, lgnd, title = 'WindSpeed')


def boxplot (datalist = None, lgnd = None, title = None):

	plt.figure(figsize = (10,10))
	plt.boxplot(datalist)
	plt.xlabel('Services')
	plt.xticks(np.arange(1,len(lgnd)+1), lgnd)	
	plt.title(title)		


def plot(datalist = None, lgnd = None, title = None):

	plt.figure(figsize = (10,10))
	
	for table in datalist:
		plt.plot(table)
	
	plt.legend(lgnd, loc = 'upper center')
	plt.xlabel('Services')	
	plt.title(title)		
	plt.show()


def main():

	data_dwd, dwd_se = fl.getConnectionDWD()
	data_wetterdienst, wd_se = fl.getConnectionWetterdienstde()
	data_wetterde, we_se = fl.getConnectionWetterde()
	data_wettercom, wc_se = fl.getConnectionWettercom()
	data_openweather, ow_se = fl.getConnectionOpenWeatherMaporg()
	data_accuweather, aw_se = fl.getConnectionAccuweathercom()

	measure_date = 20180604 #
	x_day_forecast = 1 #Attention: 20180630 - 2018071 != 1 ...
	
	tuple_without_dwd = [(data_openweather, ow_se),(data_accuweather, aw_se), (data_wetterdienst, wd_se), (data_wettercom, wc_se)]
	boxPlot_maxtemp(tuple_without_dwd, measure_date, x_day_forecast)
	boxplot_mintemp(tuple_without_dwd, measure_date, x_day_forecast)
	boxplot_sunhours(tuple_without_dwd, measure_date, x_day_forecast)
	boxplot_windspeed(tuple_without_dwd, measure_date, x_day_forecast)

	plot_mintemp(tuple_without_dwd, measure_date, x_day_forecast)
	plot_maxtemp(tuple_without_dwd, measure_date, x_day_forecast)
	plt.show()

if __name__ == "__main__":
	main()

