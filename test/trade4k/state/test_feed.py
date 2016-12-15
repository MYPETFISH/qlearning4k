'''
Created on 13Dec.,2016

@author: u6028300
'''
import unittest
from trade4k.state.feed import Feed


class Test(unittest.TestCase):


    def setUp(self):
        self.feed = Feed()


    def tearDown(self):
        pass


    def test_getOrigin(self):
        print ('test_getOrigin')
        feed = Feed()
        origin = feed.getOrigin()
        print (origin[0][1])
        self.assertTrue(origin[0][1] > 1)

    def test_getPositionsToday(self):
        print('getPositionsToday')
        feed = Feed()
        sessions = feed.getSession(0, 1)
        print (sessions)

    def test_getPositionsTodayP1(self):
        print('getPositionsTodayP1')
        feed = Feed()
        sessions = feed.getSession(0, 2)
        print (sessions)

    def test_getPositionsTomorrow(self):
        print('getPositionsTomorrow')
        feed = Feed()
        sessions = feed.getSession(1, 1)
        print (sessions)

    def test_getPositionsTodayTransformed(self):
        print('getPositionsTodayTransformed')
        feed = Feed()
        sessions = feed.getSession(0, 1)
        transformed = feed.transform(sessions)
        print (transformed)

    def test_getPositionsTodayInversed(self):
        print('getPositionsTodayInversed')
        feed = Feed()
        sessions = feed.getSession(0, 1)
        print(sessions)
        transformed = feed.transform(sessions)        
        session2 = feed.inverse(transformed)
        print (session2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()