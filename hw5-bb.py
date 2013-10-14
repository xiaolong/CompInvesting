import qstkutil.qsdateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas
from pylab import *

#
# Prepare to read the data
#
symbols = ["AAPL","GOOG","IBM","MSFT","$SPX"]
startday = dt.datetime(2010,1,1)
endday = dt.datetime(2010,12,31)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess('Yahoo')
voldata = dataobj.get_data(timestamps, symbols, "volume")
adjcloses = dataobj.get_data(timestamps, symbols, "close")
actualclose = dataobj.get_data(timestamps, symbols, "actual_close")

#adjcloses = adjcloses.fillna()
#adjcloses = adjcloses.fillna(method='backfill')
adjcloses = (adjcloses.fillna(method='ffill')).fillna(method='backfill')

# calculation goes here
means = pandas.rolling_mean(adjcloses,20,min_periods=20)
stds = pandas.rolling_std(adjcloses, 20,min_periods=20)
bollinger_val= (adjcloses-means)/stds

#print bollinger_val.values

bollinger_val.to_csv("bollinger_values.csv",sep=',')

exit()
# Plot the prices
plt.clf()

symtoplot = 'AAPL'
plot(adjcloses.index,adjcloses[symtoplot].values,label=symtoplot)
plot(adjcloses.index,means[symtoplot].values)
plt.legend([symtoplot,'Moving Avg.'])
plt.ylabel('Adjusted Close')

savefig("movingavg-ex.png", format='png')
