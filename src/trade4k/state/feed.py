'''
Created on 29Sep.,2016
'''
import numpy as np
from trade4k.util.loader import Loader
from trade4k.state.config import Config

from sklearn import preprocessing
import time, os
import datetime
import random

class Feed(object):

    #@property
    #def closeIdx(self):
    #    return 4
    
    closeIdx = 4
 
    def __init__(self, sessions=2000):  #

        self.sessions = sessions
        s = (6, sessions)                    # does 6 mean 7 columns?!
        self.data = np.empty(s)
        self.data = self.loadData(sessions) # floats

        # scale for NN
        self.scaler = preprocessing.MinMaxScaler()
             
        #self.scaled = # rather convert in realtime?
        self.scaler.fit_transform(self.data[1:,])

        self.start = Config.start_session   # to target specific regions    
        self.reset()
        
    
    def reset(self):
        self.t = 1 + self.start + random.randint(-Config.start_vary, Config.start_vary)
        print ('reset t to {} : '.format(self.t)), 
    
    def incrementTime(self, delta=1):
        self.t = self.t + delta
    
    def loadData(self, sessions=2000):
        uri = Config.data_uri

        # load training data
        loader = Loader()
        loader.load(uri)
                
        rawData = loader.sessions(sessions, 0) # '2006-09-15', '9.08', '9.11', '9.05', '9.05', '4418700', '4.97838'
               
        # unelegent way of converting data - surely numpy has matrix approach to converting dates?
        for i in range(len(rawData)):
            date = (rawData[i][0])
            rawData[i][0] = self.toEpoch(date)    # convert existing array
                
        #now as all values are numbers, convert to numpy array as float
        return np.array(rawData).astype(float)
    
    # could either look forward (self.t,horizon) 
    # or back (self.t-horizon, horizon)
    def getState(self, horizon):
        return self.getSession(0, horizon)
    
    def getSession(self, t_delta, range):   # t_delta is forwards or back in time from t
        t = self.t + t_delta
        return self.data[t:t+range,:]        
    
    def getOrigin(self):    # get first set of values, i.e. not +/-
        return self.data[0:1,:] 
    
    def inverse(self, X):
        X = np.array(X).reshape((1, -1))
        inv3 = self.scaler.inverse_transform(X)
        return inv3

    def transform(self, X):
        #x = X.reshape(-1, 1)
        return self.scaler.transform(X)

    # replaced by getSession, and using transform(getSession...) for scaled vars
    '''
    def getHistory(self, t, range):
        # for qlearn_viz will return scaled
        if (self.scaleOn==True): return self.getScaled(t, range)
        else: return self.data[t:t+range,:]

    def getRealHistory(self, t, range):
        # for qlearn_viz will return scaled
        return self.data[t:t+range,:]
    
    # n.b. each column will have one zero value as its scaled
    def getScaled(self, t, range):
        scaled = self.scaled[t:t+range,:]
        return scaled
    '''
    
    # TODO use this to convert date value in csv to epoch 
    def toEpoch(self, d):
        p = '%d/%m/%Y'        # yahoo data
        os.environ['TZ']='UTC'
        epoch = int(time.mktime(time.strptime(d,p)))
        return epoch

    def epochToDateTime(self,e):
        dt = datetime.datetime.fromtimestamp(e).strftime('%Y-%m-%d')
        return dt
    
    def isEod(self, horizon):
        if (self.t + horizon < self.sessions): return False
        else: return True