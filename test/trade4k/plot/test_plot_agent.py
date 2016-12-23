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
from boto.ec2.buyreservation import BuyReservation

from trade4k.state.config import Config

class TestPlotAgent(unittest.TestCase):

    def __init__(self): 
        pass

    def setUp(self):
        pass

    def test_plot_vals(self):           
        
        data = np.loadtxt(open(Config.data_uri + '_agent1' + '.csv', 'rb'), delimiter=',')
                 
        fig = plt.figure()

        # units funds pval
        # wealth
        #sell = data[0:,0:1]

        wealth = data[0:, -1]
        pval = data[0:, -2:-1]
        funds = data[0:, -3:-2]
        #units = data[0:, -4:-3]

        self.y1 = wealth
        self.y2 = pval
        self.y3 = funds
        #self.y4 = units
        
        ax1 = fig.add_subplot(111)
        ax1.plot(self.y1, 'r')      #wealth
        ax1.plot(self.y2, 'k')      #pval
        ax1.plot(self.y3, 'b')      #funds
        #ax1.plot(self.y4, 'g')      #units
        ax1.set_title('Valuation')      
        
        plt.show()
        
    def tearDown(self):
        pass
