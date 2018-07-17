import numpy as np
# import scipy.fftpack
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib
import matplotlib.pyplot as plt
import calmap

import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import FunctionLibraryExtended as fle

# get data from the database
def get_data(query, table='dwd'):
	Base = declarative_base()
	# TODO: ask user to enter username and password
	engine = create_engine('mysql+pymysql://dwdtestuser:tuBnewD3_PW@weather.service.tu-berlin.de/dwdtest?use_unicode=1&charset=utf8&ssl_cipher=AES128-SHA')
	Base.metadata.create_all(engine)
	Session = sqla.orm.sessionmaker()
	Session.configure(bind=engine)
	se = Session()
   	# connect to database
	metadata = MetaData(engine, reflect=True)
    # Get Table
	table = metadata.tables[table]
	# NOT CONTAINS(sun_hours, None)
	result = engine.execute(query)
	#result = engine.execute("SELECT station_name, measure_date, sun_hours FROM dwd WHERE station_name LIKE 'Berlin%%' AND NOT CONTAINS(sun_hours, None)")
	return np.vstack(result)

# plot pandas timeseries of plot_data
def plot_timeseries(plot_data, title):
	matplotlib.rcParams.update({'font.size': 8})
	plt.figure()
	plt.title(title)
	plot_data.plot()
	plt.show()

# plot 0.05, 0.25, 0.5, 0.75, 0.95 quantiles of daily temperatures, grouped by year
def plot_temp_quantiles(city=None):
	if city == None:
		stack = get_data("SELECT t.md, t.avgtemp FROM (select measure_date as md, AVG(average_temp) as avgtemp, COUNT(station_name) as num from dwd GROUP BY measure_date) as t WHERE t.num >= 100;")
	else:
		stack = get_data("SELECT t.md, t.avgtemp FROM (select station_name as name, measure_date as md, AVG(average_temp) as avgtemp from dwd WHERE station_name LIKE '"+city+"%%' GROUP BY measure_date) as t;")
	# find start date of stack (remove trailing '.0' and convert to date format)
	start_date = str(int(stack[0,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])
	# find end date of stack
	end_date = str(int(stack[stack.shape[0]-1,0]))
	# compute date range from the start_date and length of the time series
	data_range = pd.date_range(start_date, periods=stack.shape[0], freq='D')
	# create time series from date_range and data
	plot_data = pd.Series(stack[:,1], index=data_range)
	# calculate 0.05, 0.25, 0.5, 0.75, 0.95 quantiles of daily temperatures, grouped by year
	quantile_data = plot_data.groupby(plot_data.index.year)
	quantiles_05 = quantile_data.quantile(0.05)
	quantiles_25 = quantile_data.quantile(0.25)
	quantiles_50 = quantile_data.quantile(0.5)
	quantiles_75 = quantile_data.quantile(0.75)
	quantiles_95 = quantile_data.quantile(0.95)


	# plot quantiles and linear regression
	matplotlib.rcParams.update({'font.size': 8})
	plt.figure()

	plot_data_index_array = np.arange(int(start_date[:4]), int(end_date[:4])+1).reshape(-1, 1)

	plt.scatter(plot_data_index_array, quantiles_05, s=1, color='black')
	plt.scatter(plot_data_index_array, quantiles_25, s=1, color='red')
	plt.scatter(plot_data_index_array, quantiles_50, s=1, color='blue')
	plt.scatter(plot_data_index_array, quantiles_75, s=1, color='yellow')
	plt.scatter(plot_data_index_array, quantiles_95, s=1, color='green')

	# TODO: vectorize, add slopes to plot
	model_05 = LinearRegression().fit(plot_data_index_array, quantiles_05)
	m_05 = model_05.coef_[0]
	temp_pred_05 = model_05.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_05, color='black', linewidth=1)

	model_25 = LinearRegression().fit(plot_data_index_array, quantiles_25)
	m_25 = model_25.coef_[0]
	temp_pred_25 = model_25.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_25, color='red', linewidth=1)

	model_50 = LinearRegression().fit(plot_data_index_array, quantiles_50)
	m_50 = model_50.coef_[0]
	temp_pred_50 = model_50.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_50, color='blue', linewidth=1)

	model_75 = LinearRegression().fit(plot_data_index_array, quantiles_75)
	m_75 = model_75.coef_[0]
	temp_pred_75 = model_75.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_75, color='yellow', linewidth=1)

	model_95 = LinearRegression().fit(plot_data_index_array, quantiles_95)
	m_95 = model_95.coef_[0]
	temp_pred_95 = model_95.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_95, color='green', linewidth=1)

	plt.xticks()
	plt.yticks()
	plt.xlabel("Year")
	plt.ylabel("Quantiles of annual average temperature/˚C")
	plt.show()

# plot annual average temperatures (for all years with a minimum of 100 weather stations)
def plot_temp():
	# plot average annual temperatures (where there are at least 100 weather stations)
	stack = get_data("SELECT LEFT(t.md, 4), AVG(t.avgtemp) FROM (select measure_date as md, AVG(average_temp) as avgtemp, COUNT(station_name) as num from dwd GROUP BY measure_date) as t WHERE t.num >= 100 GROUP BY LEFT(t.md, 4);")
	plot_data = pd.Series(stack[:,1], index=pd.date_range(stack[0][0], periods=stack.shape[0], freq='Y'))
	plot_data = plot_data.astype(float)
	# plot_timeseries(plot_data, "Measured average annual temperatures/˚C")

	# plot regression (TODO: labels, module parameters to plot)
	plot_data_arrary = plot_data.values.reshape(-1, 1)
	plot_data_index_array = plot_data.index.year.values.reshape(-1, 1)
	model = LinearRegression().fit(plot_data_index_array, plot_data_arrary)
	m = model.coef_[0]
	b = model.intercept_
	print("m: ", m, " b: ", b)
	# compute regression line:
	temp_pred = model.predict(plot_data_index_array)
	# create plot:
	plt.scatter(plot_data_index_array, plot_data_arrary, s=1, color='black')
	plt.plot(plot_data_index_array, temp_pred, color='blue', linewidth=1)
	plt.xticks()
	plt.yticks()
	plt.xlabel("Year")
	plt.ylabel("Annual average temperature/˚C")
	plt.title("Change in average temperature: %s ˚C per annum"%(m))
	plt.show()

def forecast_deviation(feature=None, forecast_provider="accuweathercom"):
	forecast_data = get_data("SELECT measure_date, AVG(min_temp), AVG(max_temp) FROM accuweathercom GROUP BY measure_date;", 'accuweathercom')
	start_date = str(int(forecast_data[0,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])
	dwd_data = get_data("SELECT measure_date, AVG(average_temp) FROM dwd WHERE (measure_date >= "+start_date+") GROUP BY measure_date;", 'dwd')
	
	# TODO pd.date_range()
	# TODO pd.Series()

	return forecast_data, dwd_data

def main():
	# plot average annual temperatures (where there are at least 100 weather stations)
	plot_temp()

	# plot quantiles of annual average temperatures
	plot_temp_quantiles("Berlin")

	# plot deviation between forecast data and dwd data
	# forecast_data, dwd_data = forecast_deviation()
	# plot_timeseries([forecast_data, dwd_data], "Measured + predicted max/min temp (daily)")

if __name__ == "__main__":
    main()
