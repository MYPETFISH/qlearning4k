'''
Created on 1Oct.,2016
'''
import logging

#from gym.scoreboard import game
#from bokeh.util.logconfig import level
from sklearn import preprocessing

import math
import numpy as np

from trade4k.state.feed import Feed
from trade4k.state.config import Config

class Portfolio(object):

    def __init__(self, feed, funds=1000., units=0.):        
        self.ifunds = funds
        self.iunits = units
        self.origin = feed.getOrigin()
        
        self.reset()
        
        # benchmarking
        self.units_bm = math.floor(self.ifunds/self.lastClose)
        self.funds_bm = self.ifunds - (self.units_bm * self.lastClose)
        
        # arbitrary size for this array
        xf = np.array([funds, funds*20, funds*20]).reshape(-1,1)     
        #review if funds grow x 20
        self.scaler = preprocessing.MinMaxScaler().fit(xf)
 
    def reset(self):
        self.funds, self.cValue, self.pValue = (self.ifunds,)*3
        self.units = self.iunits
        
        self.floor = self.funds * Config.floor_coef 
        
        self.lastClose = self.origin[0][Feed.closeIdx]  # initial close
        self.price(self.lastClose)
        
 
    def price_delta(self, closeDelta):       # replaces valuation
        self.lastClose = self.lastClose + closeDelta
        self.pValue = self.cValue
        self.cValue = self.funds + (self.units * self.lastClose)
        
        if (self.floor<self.cValue): 
            self.floor = self.cValue * Config.floor_coef

        return self.pValue, self.cValue

    def price(self, close):       # replaces valuation
        self.lastClose = close
        self.pValue = self.cValue
        self.cValue = self.funds + (self.units * self.lastClose)
        
        if (self.floor<self.cValue): 
            self.floor = self.cValue * Config.floor_coef

        return self.pValue, self.cValue

    # call after a price update. is fraction
    def benchmark(self):
        bm = (self.units_bm * self.lastClose) + self.funds_bm
        val =  (self.units * self.lastClose) + self.funds 
        return val/bm

    def update(self, order):
        self.funds -= order*self.lastClose
        self.units += order

    # returns S_portfolio, unscaled
    def getState(self):
        return np.array([self.units, self.funds, self.cValue]).reshape(1,3)

    def getValues(self):
        return self.pValue, self.cValue

    def getVals(self):
        vals = [self.units, self.funds, self.pValue]        
        return vals

    def getScaledVals(self):
        xg = np.array([self.units, self.funds, self.pValue]).reshape(-1,1)
        vals = self.scaler.transform(xg)
        return vals

    def unscaleVales(self, vals):
        return self.scale.inverse_transform(vals)
    '''
    def inverse(self, X):
        X = np.array(X).reshape((1, -1))
        inv3 = self.scaler.inverse_transform(X)
        return inv3
    '''
    # units funds pval
    def transform(self, X):
        xg = X.reshape(-1,1)    # avoid warning
        return self.scaler.transform(xg)

    # units funds pval
    def inverse(self, X):
        return self.scaler.inverse_transform(X)
    
    # q-learning manages discounted future reward
    def getProfit(self):
        return self.cValue - self.pValue

    # HELPER
    def actionStr(self, action):
        if (action==0): return 'buy'
        elif (action==1): return 'sell'
        elif (action==2): return 'hold'
        