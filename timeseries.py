import numpy as np
import scipy.fftpack
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calmap

import sys
sys.path.append('/Users/michaelstenzel/Documents/MKP/mkp_database/')

import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import FunctionLibraryExtended as fle

# get data from the database
def get_data(query, table='dwd'):
	Base = declarative_base()
	# ask user to enter username and password
	engine = create_engine('mysql+pymysql://dwdtestuser:asdassaj14123@weather.service.tu-berlin.de/dwdtest?use_unicode=1&charset=utf8&ssl_cipher=AES128-SHA')
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

# plot timeseries of plot_data
def plot_timeseries(plot_data, title):
	matplotlib.rcParams.update({'font.size': 8})
	plt.figure()
	plt.title(title)
	# for x in plot_data:
	# 	x.plot()
	plot_data.plot()
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
	# plot daily average temperatures (where there are at least 100 weather stations)
	stack = get_data("SELECT t.md, t.avgtemp FROM (select measure_date as md, AVG(average_temp) as avgtemp, COUNT(station_name) as num from dwd GROUP BY measure_date) as t WHERE t.num >= 100;")

	# find start date of stack (remove trailing '.0' and convert to date format)
	start_date = str(int(stack[0,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])
	# compute date range from the start_date and length of the time series
	data_range = pd.date_range(start_date, periods=stack.shape[0], freq='D')
	# compute difference of the two time series
	plot_data = pd.Series(stack[:,1], index=data_range)
	plot_timeseries(plot_data, "Measured average daily temperatures/˚C")

	# calculate 0.05, 0.25, 0.5, 0.75, 0.95 quantiles of daily temperatures, grouped by year
	quantile_data = plot_data.groupby(plot_data.index.year)
	quantiles_05 = quantile_data.quantile(0.05)
	quantiles_25 = quantile_data.quantile(0.25)
	quantiles_50 = quantile_data.quantile(0.5)
	quantiles_75 = quantile_data.quantile(0.75)
	quantiles_95 = quantile_data.quantile(0.95)

	# plot the FFT
	# fft = scipy.fftpack.fft(plot_data)
	# fft_series = pd.Series(fft)
	# fft_series.plot()
	# plt.show()

	# plot average annual temperatures (where there are at least 100 weather stations)
	stack = get_data("SELECT LEFT(t.md, 4), AVG(t.avgtemp) FROM (select measure_date as md, AVG(average_temp) as avgtemp, COUNT(station_name) as num from dwd GROUP BY measure_date) as t WHERE t.num >= 100 GROUP BY LEFT(t.md, 4);")
	print(stack)
	plot_data = pd.Series(stack[:,1], index=pd.date_range(stack[0][0], periods=stack.shape[0], freq='Y'))
	plot_data = plot_data.astype(float)
	print(plot_data)
	plot_timeseries(plot_data, "Measured average annual temperatures/˚C")

	# plot quantiles
	matplotlib.rcParams.update({'font.size': 8})
	plt.figure()
	plt.title("TEST")
	d = pd.concat([quantiles_05, quantiles_25, quantiles_50, quantiles_75, quantiles_95], axis=1)
	# d = d.rename(columns={"0": "05", "1": "95"})
	print(d)
	d.plot()
	plt.show()

	# plot deviation between forecast data and dwd data
	# forecast_data, dwd_data = forecast_deviation()
	# plot_timeseries([forecast_data, dwd_data], "Measured + predicted max/min temp (daily)")

if __name__ == "__main__":
    main()
