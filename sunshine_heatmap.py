import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calmap

import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import sys
sys.path.append('/Users/michaelstenzel/Documents/MKP/mkp_database/')
import FunctionLibraryExtended as fle

'''
Generate a heatmap of the deviation between measured and predicted sunshine
'''

def main():

	# get real data

	#try:
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

	result = engine.execute("SELECT station_name, measure_date, sun_hours FROM dwd WHERE station_name LIKE 'Berlin%%'")

	for row in result:
		print(row)

	print(type(result))

	### generate test data
	num_days = 700
	start_date = '1/1/2014'

	np.random.seed(sum(map(ord, 'calmap')))

	mu_meas, sig_meas = 5, 0.3
	mu_pred, sig_pred = 1, 0.1
	meas = np.random.normal(mu_meas, sig_meas, num_days)
	predicted = meas + np.random.normal(mu_pred, sig_pred, num_days)
	deviation = meas - predicted
	###

	# test
	data_range = (pd.date_range(start_date, periods=num_days, freq='D'))
	plot_data = pd.Series(meas, index=data_range) - pd.Series(predicted, index=data_range)

	matplotlib.rcParams.update({'font.size': 8})

	# plot data from a single year
	plt.figure()
	ax = calmap.yearplot(plot_data, year=2014, linecolor = 'white')		# must set linecolor, due to calmaps's use of depreacted matplotlib methods
	plt.title("Sunshine prediction deviation")
	ax.plot()
	plt.show()

	# plot data from multiple years
	plt.figure()
	fig2, ax2 = calmap.calendarplot(plot_data, linecolor = 'white')		# must set linecolor, due to calmaps's use of depreacted matplotlib methods
	plt.title("Sunshine prediction deviation")
	#fig2.title("Sunshine prediction deviation")
	#ax2.plot()
	#fig2.add_axes(ax2)
	#fig2.show()
	plt.show()

if __name__ == "__main__":
    main()