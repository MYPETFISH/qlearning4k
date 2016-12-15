'''
Created on 13Dec.,2016

@author: u6028300
'''
import unittest

from trade4k.games.trade import Trade

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_trade_buy(self):
        print ('test_trade')
        trade = Trade(sessions=2000)
        trade.play(2)

    def test_trade_sell(self):
        print ('test_trade')
        trade = Trade(sessions=2000)
        trade.portfolio.units=200
        trade.portfolio.price_delta(0)
        trade.play(0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()