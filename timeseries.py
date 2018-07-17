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
	engine = create_engine('mysql+pymysql://dwdtestuser:<password>@weather.service.tu-berlin.de/dwdtest?use_unicode=1&charset=utf8&ssl_cipher=AES128-SHA')
	Base.metadata.create_all(engine)
	Session = sqla.orm.sessionmaker()
	Session.configure(bind=engine)
	se = Session()
   	# connect to database
	metadata = MetaData(engine, reflect=True)
    # Get Table
	table = metadata.tables[table]
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

	# TODO: vectorize
	model_95 = LinearRegression().fit(plot_data_index_array, quantiles_95)
	m_95 = model_95.coef_[0]
	temp_pred_95 = model_95.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_95, color='green', linewidth=1, label=round(m_95, 5))

	model_75 = LinearRegression().fit(plot_data_index_array, quantiles_75)
	m_75 = model_75.coef_[0]
	temp_pred_75 = model_75.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_75, color='yellow', linewidth=1, label=round(m_75, 5))

	model_50 = LinearRegression().fit(plot_data_index_array, quantiles_50)
	m_50 = model_50.coef_[0]
	temp_pred_50 = model_50.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_50, color='blue', linewidth=1, label=round(m_50, 5))

	model_25 = LinearRegression().fit(plot_data_index_array, quantiles_25)
	m_25 = model_25.coef_[0]
	temp_pred_25 = model_25.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_25, color='red', linewidth=1, label=round(m_25, 5))

	model_05 = LinearRegression().fit(plot_data_index_array, quantiles_05)
	m_05 = model_05.coef_[0]
	temp_pred_05 = model_05.predict(plot_data_index_array)
	plt.plot(plot_data_index_array, temp_pred_05, color='black', linewidth=1, label=round(m_05, 5))

	plt.xticks()
	plt.yticks()
	plt.xlabel("Year")
	plt.ylabel("Quantiles of annual average temperature/˚C")
	# plt.legend()
	plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
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

def forecast_deviation(feature=None, forecast_provider="accuweathercom", city="Berlin"):
	# forecast_data = get_data("SELECT measure_date_prediction, AVG(sun_hours) FROM "+forecast_provider+" WHERE city LIKE '"+city+"%%' GROUP BY measure_date_prediction;", forecast_provider)
	# forecast_data = get_data("SELECT measure_date, measure_date_prediction, sun_hours FROM accuweathercom WHERE city LIKE 'Berlin%%';", "accuweathercom")
	forecast_data = get_data("SELECT measure_date, measure_date_prediction, sun_hours FROM accuweathercom WHERE (measure_date >= '20180606' AND city LIKE 'Berlin%%');", "accuweathercom")

	# start_date = str(int(forecast_data[0,0]))
	start_date = "20180606"
	end_date = str(int(forecast_data[forecast_data.shape[0]-1,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])
	# dwd_data = get_data("SELECT measure_date, AVG(sun_hours) FROM dwd WHERE (station_name LIKE '"+city+"%%' AND measure_date >= "+start_date+") GROUP BY measure_date;", 'dwd')
	dwd_data = get_data("SELECT measure_date, AVG(sun_hours) FROM dwd WHERE (station_name LIKE '"+city+"%%' AND measure_date >= '20180606' AND measure_date <= '"+end_date+"') GROUP BY measure_date;", 'dwd')

	# compute date range from the start_date and length of the time series
	data_range = pd.date_range(start_date, periods=dwd_data.shape[0], freq='D')

	# every 5th entry, starting at 1
	predict_1_day = forecast_data[1::5]
	predict_1_day = predict_1_day[0:(dwd_data.shape[0]),2]
	# print(dwd_data[:,1])
	print(predict_1_day.shape)

	# every 5th entry, starting at 2
	predict_2_day = forecast_data[2::5]
	predict_2_day = predict_2_day[0:(dwd_data.shape[0]),2]

	# every 5th entry, starting at 3
	predict_3_day = forecast_data[3::5]
	predict_3_day = predict_3_day[0:(dwd_data.shape[0]),2]

	# every 5th entry, starting at 4
	predict_4_day = forecast_data[4::5]
	predict_4_day = predict_4_day[0:(dwd_data.shape[0]),2]

	# print(predict_1_day.shape[0]-1)
	# print(dwd_data.shape[0]-1)

	# print(dwd_data[:,1].reshape(-1,1))
	# print(dwd_data[:,1].reshape(-1,1).shape)

	# deviation_1 = abs(predict_1_day[:, 2] - dwd_data[:predict_1_day.shape[0]-1,1])

	# deviation_1 = abs(predict_1_day - dwd_data[:,1])
	# deviation_2 = abs(predict_2_day - dwd_data[:,1])
	# deviation_3 = abs(predict_3_day - dwd_data[:,1])
	# deviation_4 = abs(predict_4_day - dwd_data[:,1])

	deviation_1 = dwd_data[:,1] - predict_1_day
	deviation_2 = dwd_data[:,1] - predict_2_day
	deviation_3 = dwd_data[:,1] - predict_3_day
	deviation_4 = dwd_data[:,1] - predict_4_day

	# print(deviation_1)

	# create time series from date_range and AVG(sun_hours) (forecast)
	deviation_1_plot_data = pd.Series(deviation_1, index=data_range)
	deviation_2_plot_data = pd.Series(deviation_2, index=data_range)
	deviation_3_plot_data = pd.Series(deviation_3, index=data_range)
	deviation_4_plot_data = pd.Series(deviation_4, index=data_range)
	# print(deviation_1_plot_data)

	rms_1 = np.sqrt(np.sum(deviation_1**2)/(dwd_data[:,1]).size)
	rms_2 = np.sqrt(np.sum(deviation_2**2)/(dwd_data[:,1]).size)
	rms_3 = np.sqrt(np.sum(deviation_3**2)/(dwd_data[:,1]).size)
	rms_4 = np.sqrt(np.sum(deviation_4**2)/(dwd_data[:,1]).size)
	print("RMS 1 day forecast: ", rms_1)
	print("RMS 2 day forecast: ", rms_2)
	print("RMS 3 day forecast: ", rms_3)
	print("RMS 4 day forecast: ", rms_4)

	# plot_timeseries(deviation_1_plot_data, "test")

	# groupby weekday
	weekday_deviation_1 = deviation_1_plot_data.groupby(deviation_1_plot_data.index.weekday).mean()
	print(weekday_deviation_1)
	weekday_deviation_2 = deviation_2_plot_data.groupby(deviation_2_plot_data.index.weekday).mean()
	print(weekday_deviation_2)
	weekday_deviation_3 = deviation_3_plot_data.groupby(deviation_3_plot_data.index.weekday).mean()
	print(weekday_deviation_3)
	weekday_deviation_4 = deviation_4_plot_data.groupby(deviation_4_plot_data.index.weekday).mean()
	print(weekday_deviation_4)

	# concat = pd.concat([weekday_deviation_1, weekday_deviation_2, weekday_deviation_3, weekday_deviation_4])
	# print(concat)
	# matplotlib.rcParams.update({'font.size': 8})
	# plt.figure()
	# plt.title("comp")
	# concat.plot()
	# plt.show()
	plot_timeseries(weekday_deviation_1, "1-day deviation by weekday")
	plot_timeseries(weekday_deviation_2, "2-day deviation by weekday")
	plot_timeseries(weekday_deviation_3, "3-day deviation by weekday")
	plot_timeseries(weekday_deviation_4, "4-day deviation by weekday")

	# create time series from date_range and AVG(sun_hours) (forecast)
	# dwd_plot_data = pd.Series(dwd_data[:,1], index=data_range)

	# TODO pd.date_range()
	# TODO pd.Series()

	return forecast_data, dwd_data

def main():
	# plot average annual temperatures (where there are at least 100 weather stations)
	plot_temp()

	# plot quantiles of annual average temperatures
	plot_temp_quantiles("Berlin")

	forecast_deviation("accuweathercom", "Berlin")

	# plot deviation between forecast data and dwd data
	# forecast_data, dwd_data = forecast_deviation()
	# plot_timeseries([forecast_data, dwd_data], "Measured + predicted max/min temp (daily)")

if __name__ == "__main__":
    main()
