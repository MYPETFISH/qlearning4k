__author__ = "Alex Johnston"

import numpy as np
import math

from trade4k.state.config import Config
from trade4k.state.feed import Feed
from trade4k.state.portfolio import Portfolio

from .game import Game

#actions = {0:'sell', 1:'hold', 2:'buy'}

class Trade(Game):

	# No grid, unless is 7x3 + 3 (8x3)
	def __init__(self, sessions=2000, horizon = 3):
		self.horizon = horizon
		self.won = False
		self.feed = Feed(sessions)
		self.portfolio = Portfolio(self.feed, funds=Config.funds)
		self.reset()

	def reset(self):
		self.t = 0

		# reset & get initial portfolio state & feed state, scaled
		self.portfolio.reset()
		self.feed.reset()

		'''
		S_port = self.portfolio.getState()
		S_feed = self.feed.getState(self.horizon)
		
		re_port = np.reshape(S_feed, (self.horizon*7,1))
		re_feed = np.reshape(S_port, (3,1))
		self.state = np.append(np.reshape(S_feed, (self.horizon*7,1)), np.reshape(S_port, (3,1)))
		'''
		self.state = self.get_state()
		
	@property
	def name(self):
		return "Trade"

	@property
	def nb_actions(self):
		return 3

	def play(self, action):
		assert action in range(3), "Invalid action."
		# local copy of state to work with
		state = self.state

		# buy/sell at close +/- zero, not tp1 open
		self.update_portfolio(action)
		
		# move to tp1
		self.feed.incrementTime()

		# get historical prices to horizon
		S_feed = self.feed.getState(self.horizon)
		
		# price on latest close
		last_session = S_feed[self.horizon-1]
		last_close = last_session[Feed.closeIdx]
		self.portfolio.price_delta(last_close)
		
		'''
		re_feed = np.reshape(S_feed, (self.horizon*7,1))
		re_port = np.reshape(S_port, (3,1))

		# store new state for next round
		self.state = np.append(np.reshape(S_feed, (self.horizon*7,1)), np.reshape(S_port, (3,1)))
		'''
		self.state = self.get_state()

	def update_portfolio(self, action):		# sell|hold|buy
		order = 0		
		if (action==1):		# hold=1
			return
		elif (action==2):	   # buy=2

			available = self.portfolio.funds*Config.policy_funds

			order = math.floor(available/self.portfolio.lastClose)
			
			# dont understand the 10
			#if (available > 10.0 and order > 0):  
			if (order > 0):  
				#self.portfolio.funds -= order*self.portfolio.lastClose
				#self.portfolio.units += order

				self.portfolio.update(order)
				#print('buy order: {0}'.format(order))
		elif (action==0):	  # sell=0
			if (self.portfolio.units > 0):
				order = Config.policy_stocks * self.portfolio.units
				#self.portfolio.funds += order * self.portfolio.lastClose
				#self.portfolio.units -= order
				self.portfolio.update(-order)

				#print('sell order: {0}'.format(order))

	# state is both portfolio and market data
	# is returned by game.get_data as S
	# since feed and port use different scalars, scaling should occur here
	def get_state(self):
		S_port = self.portfolio.getState()
		S_feed = self.feed.getState(self.horizon)

		sc_port = self.portfolio.transform(S_port)
		sc_feed = self.feed.transform(S_feed)
		
		s_feed = np.reshape(sc_feed, (self.horizon*7,))
		s_port = np.reshape(sc_port, (3,))
		
		#scaled_feed = self.feed.transform(re_feed)	# reshape to avoid warning
		#scaled_port = self.portfolio.transform(re_port)
		
		S = np.append(s_feed, s_port)
		return S	# scaled

	# this is the reward. 
	# need -ve as value decreases
	# in future should also add cost of trading
	def get_score(self):
		profit = self.portfolio.getProfit()
		return profit

	def is_over(self):
		if (self.portfolio.cValue <= self.portfolio.floor): 
			return True
		else: return False

	# !
	def is_won(self):
		return True		
		# change to multiple of initial investment: e.g. pval > (20 x closing * initial funds)
