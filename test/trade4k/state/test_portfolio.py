'''
Created on 13Dec.,2016

@author: u6028300
'''
import unittest

from trade4k.state.feed import Feed
from trade4k.state.portfolio import Portfolio

import numpy as np

class Test_Portfolio(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_price(self):
        print ('test_price')
        
        feed = Feed()
        portfolio = Portfolio(feed)
        portfolio.units = 1000
        
        origin = feed.getOrigin()
        last_close = origin[0][Feed.closeIdx]
        
        p, c = portfolio.price(last_close)
        self.assertNotEqual(p, c)
        #print(p)
        #print(c)

    def test_price_horizon(self):
        print ('test_price_horizon')
        horizon = 3
        
        feed = Feed()
        portfolio = Portfolio(feed)
        portfolio.units = 1000

        S_feed = feed.getSession(-horizon, horizon)
        last_session = S_feed[horizon-1]
        last_close = last_session[Feed.closeIdx]

        p, c = portfolio.price_delta(last_close)
        print(p,c)
        self.assertTrue(c>p)

    def test_price_delta(self):
        print ('test_price_delta')
        horizon = 3
        
        feed = Feed()
        portfolio = Portfolio(feed)
        portfolio.units = 1000

        p, c = portfolio.price_delta(1.5)
        print(p,c)
        self.assertTrue(c>p)

    def test_price_transform(self):
        print ('test_price_transform')
        feed = Feed()
        portfolio = Portfolio(feed)

        c=np.array([100,10000,19000])
        print(portfolio.transform(c))

if __name__ == "__main__":
    '''import sys
    sys.argv = ['', 'Test_Portfolio.test_price']
    sys.argv = ['', 'Test_Portfolio.test_price_delta']
    sys.argv = ['', 'Test_Portfolio.test_price_transform']
    sys.argv = ['', 'Test_Portfolio.test_price_horizon']
    '''
    unittest.main()