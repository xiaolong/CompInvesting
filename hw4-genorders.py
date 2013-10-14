import os

import pandas as pd
import numpy as np
import math
import copy
import datetime as dt


import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""



## for HW4: output to external file, when an event is found
def output_action(s_sym, ldt_timestamps, i, f):
	timestamp=ldt_timestamps[i]
	f.write(','.join([str(timestamp.year),str(timestamp.month),str(timestamp.day) , s_sym, 'BUY,100']) )
	f.write("\n")

	# sell out in 5 trading days!! if not enough days available, sell in the last day.
	newtime= ldt_timestamps[min(i+5, len(ldt_timestamps)-1 )]
	f.write(','.join([str(newtime.year),str(newtime.month),str(newtime.day) , s_sym, 'SELL,100']) )
	f.write("\n")



def find_events(ls_symbols, d_data, output):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close'] #here use actual close for HW2

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):

            # Scan through to get prices
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]

            # Event is found if the symbol is down below $5
            if f_symprice_today < 10.0 and f_symprice_yest >= 10.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

		# HW4: instead of put into a matrix, output to a file
		output_action(s_sym, ldt_timestamps, i, output)

    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # remove NAN from price data, specially for the S&P 500 from 2008
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    output= open('orders-hw4.csv', 'w')
    df_events = find_events(ls_symbols, d_data, output)
    output.close()

'''
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
'''

