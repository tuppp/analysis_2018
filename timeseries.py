import numpy as np
import scipy.fftpack
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calmap

import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

# remove this!
import sys
sys.path.append('/Users/michaelstenzel/Documents/MKP/mkp_database/')

import FunctionLibraryExtended as fle

# get data from the database
def get_data():
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
	table = metadata.tables['dwd']
	# NOT CONTAINS(sun_hours, None)
	result = engine.execute("SELECT measure_date, AVG(average_temp) FROM dwd GROUP BY measure_date;")
	#result = engine.execute("SELECT station_name, measure_date, sun_hours FROM dwd WHERE station_name LIKE 'Berlin%%' AND NOT CONTAINS(sun_hours, None)")
	return np.vstack(result)

# plot timeseries of plot_data
def plot_timeseries(plot_data, title):
	matplotlib.rcParams.update({'font.size': 8})
	plt.figure()
	plt.title(title)
	plot_data.plot()
	plt.show()

def main():
	stack = get_data()
	# find start date of stack (remove trailing '.0' and convert to date format)
	start_date = str(int(stack[0,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])
	# compute date range from the start_date and length of the time series
	data_range = pd.date_range(start_date, periods=stack.shape[0], freq='D')
	# compute difference of the two time series
	plot_data = pd.Series(stack[:,1], index=data_range)
	# print(plot_data)
	plot_timeseries(plot_data, "Measured average daily temperatures/˚C")

	fft = scipy.fftpack.fft(plot_data)
	fft_series = pd.Series(fft)
	fft_series.plot()
	plt.show()
	# print(fft)
	# plot_timeseries(fft, "FFT of average daily temperatures")


if __name__ == "__main__":
    main()
