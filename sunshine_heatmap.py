import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calmap

import sqlalchemy as sqla
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import FunctionLibraryExtended as fle

# Generate a heatmap of the difference in measured sunshine between two cities
def main():	
	#try:
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
	result = engine.execute("SELECT measure_date, sun_hours FROM dwd WHERE (station_name LIKE 'Berlin%%') AND (sun_hours NOT LIKE 'None') GROUP BY measure_date")
	#result = engine.execute("SELECT station_name, measure_date, sun_hours FROM dwd WHERE station_name LIKE 'Berlin%%' AND NOT CONTAINS(sun_hours, None)")
	stack = np.vstack(result)

	# get data for second city
	result = engine.execute("SELECT measure_date, sun_hours FROM dwd WHERE (station_name LIKE 'M%%') AND (sun_hours NOT LIKE 'None') GROUP BY measure_date")
	stack_2 = np.vstack(result)

	# find start date of stack (remove trailing '.0' and convert to date format)
	start_date = str(int(stack[0,0]))
	start_date = '%s-%s-%s' % (start_date[:4], start_date[4:6], start_date[6:])

	data_range = pd.date_range(start_date, periods=stack.shape[0], freq='D')
	plot_data = pd.Series(stack_2[:550,1]-stack[:,1], index=data_range)

	print(plot_data)

	matplotlib.rcParams.update({'font.size': 8})

	# plot data from multiple years
	plt.figure()
	fig2, ax2 = calmap.calendarplot(plot_data, linecolor = 'white')		# must set linecolor, due to calmaps's use of depreacted matplotlib methods
	plt.title("Daily sunshine difference between Munich and Berlin")
	plt.show()


if __name__ == "__main__":
    main()
