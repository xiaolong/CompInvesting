import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep


import datetime as dt
import matplotlib.pyplot as plt
import pandas
from pylab import *
import copy


def find_events(ls_symbols, d_data):
    df_bollinger = d_data['bollinger'] 

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_bollinger)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_bollinger.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
        
            f_sym_today = df_bollinger[s_sym].ix[ldt_timestamps[i]]
            f_sym_yest = df_bollinger[s_sym].ix[ldt_timestamps[i - 1]]
            
            f_SPY_today = df_bollinger['SPY'].ix[ldt_timestamps[i]]

            # Event is found if the symbol is down below $5
            if f_sym_today < -2.0 and f_sym_yest >= -2.0 and f_SPY_today>=1.1:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

#
# Prepare to read the data
#
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
timestamps = du.getNYSEdays(startday,endday,dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo')
ls_symbols = dataobj.get_symbols_from_list('sp5002012')
ls_symbols.append('SPY')

ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
for s_key in ls_keys:
	d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
	d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
	d_data[s_key] = d_data[s_key].fillna(1.0)


# calculation goes here
means = pandas.rolling_mean(d_data['close'],20,min_periods=20)
stds = pandas.rolling_std(d_data['close'], 20,min_periods=20)
bollinger_val= (d_data['close']-means)/stds

d_data['bollinger']= bollinger_val

#print bollinger_val.values

df_events = find_events(ls_symbols, d_data)
print "Creating Study"

ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='BollingerEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')





