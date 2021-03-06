
## HW1 solution
import qstkutil.qsdateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from pylab import *
import pandas

import numpy as np


def simulate(start, end, tickers, allocations):
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(start,end,timeofday)	
	dataobj = da.DataAccess('Yahoo')
	close = dataobj.get_data(timestamps, tickers, "close",verbose=True)
	rets = close.values.copy()
	rets = rets/rets[0,:] #normalize
	portrets = sum(rets*allocations, axis=1) #now we got the CORRECT portfolio cum return
	
	port_daily_ret=[(portrets[i]-portrets[i-1])/portrets[i-1] for i in range(1,len(portrets)) ] 

	port_daily_ret.insert(0,0) #now we get the portfolio daily return
	
	volatility = np.std(port_daily_ret)
	
	sharpe = np.sqrt(252)* np.average(port_daily_ret) / volatility
	return (volatility, port_daily_ret, sharpe, portrets[-1])



## Brute-Force here, not elegant. Recursion could be better
def getAllAlloc():
	x= [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	alloc=[]
	for i in range(0,11):
		a= x[i]
		for j in range(0,11):
			b=x[j]
			for m in range(0,11):
				c=x[m]
				for n in range(0,11):
					d= x[n]
					if a+b+c+d==1:
						alloc.append([a,b,c,d])
	return alloc
	
#vol, daily_ret, sharpe, cum_ret= simulate(startday, endday, symbols, portalloc)


def OptimalSolution(startday, endday, symbols, allocs):
	global best_vol, best_daily_ret, best_sharpe, best_cum_ret, best_alloc
	best_sharpe=-100
	
	## test agains each allocation possible
	for alloc in allocs:
		vol, daily_ret, sharpe, cum_ret= simulate(startday, endday, symbols, alloc)
		if sharpe>best_sharpe:
			best_vol= vol
			best_sharpe=sharpe
			best_daily_ret=daily_ret
			best_cum_ret= cum_ret
			best_alloc=alloc
			
	## at this point, we already get the optimal solution
	print '#'*20
	print 'Start Date: ', startday
	print 'End Date: ',endday
	print 'Symbols" ', symbols
	print 'Optimal Allocations', best_alloc
	print 'Sharpe Ratio: ', best_sharpe
	print 'Voltatility(stdev of daily rets):', best_vol
	print 'Average Daily Return:',  np.average(best_daily_ret)
	print 'Cumulative Return: ', best_cum_ret
	print '#'*20


allocs= getAllAlloc()  ## store all possible allocations first

'''
symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
startday = dt.datetime(2010,1,1)
endday = dt.datetime(2010,12,31)
OptimalSolution(startday, endday, symbols, allocs)
'''
'''
portalloc=[0.4, 0.4, 0.0, 0.2]
'''
symbols = ['BRCM', 'ADBE', 'AMD', 'ADI'] 
startday = dt.datetime(2011,1,1)
endday = dt.datetime(2011,12,31)


OptimalSolution(startday, endday, symbols, allocs)
