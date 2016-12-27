'''
Created on 8Dec.,2016

@author: U6028300
'''
import unittest
import numpy as np
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
from matplotlib import dates
from pygments.lexer import using

from trade4k.state.config import Config

envUri = "C:/temp/py/k/3/"
envSave = "epochs_12-23"

#config = Config()
    
# for now cut to get quotes then plot
data = np.loadtxt(open(envUri + envSave+ '.csv', 'rb'), delimiter=',')
        
loss = data[0:,0:1]
wins = data[0:,1:2]
avg = data[0:,2:3]
                
y1 = loss
y2 = wins 
y3 = avg
        
# http://stackoverflow.com/questions/5498510/creating-graph-with-date-and-time-in-axis-labels-with-matplotlib
 

fig = plt.figure()

ax1 = fig.add_subplot(311)
ax1.plot(y1)
ax1.set_title('loss')        

ax2 = fig.add_subplot(313, sharex=ax1)
ax2.plot(y2)
ax2.set_title('Win')        
        
ax3 = fig.add_subplot(312, sharex=ax1)
ax3.plot(y3)
ax3.set_title('Loss Avg')  
        
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.6)
        
#format the tics
plt.sca(ax1)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off

plt.show()
pass