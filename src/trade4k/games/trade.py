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
		self.trained = False

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
		
		#if (self.feed.t%10==0): print self.feed.t,
		print str(action),
		
		# local copy of state to work with
		state = self.state

		# buy/sell at close +/- zero, not tp1 open
		self.update_portfolio(action)
		
		# move to tp1
		self.feed.incrementTime(1)

		# get historical prices to horizon
		S_feed = self.feed.getState(self.horizon)
		
		# price on latest close
		last_session = S_feed[self.horizon-1] #IndexError: index 2 is out of bounds for axis 0 with size 2
		last_close_delta = last_session[Feed.closeIdx]
		self.portfolio.price_delta(last_close_delta)
		self.portfolio.last_close_delta = last_close_delta	# t plus 1 close
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
			# MINUS FEES
			order = math.floor(available/self.portfolio.lastClose)
			
			# dont understand the 10
			#if (available > 10.0 and order > 0):  
			if (order > 0):  
				#self.portfolio.funds -= order*self.portfolio.lastClose
				#self.portfolio.units += order

				self.portfolio.update(order)
				# CHARGE FEES
				
				#print('buy order: {0}'.format(order))
		elif (action==0):	  # sell=0
			if (self.portfolio.units > 0):
				order = Config.policy_stocks * self.portfolio.units
				#self.portfolio.funds += order * self.portfolio.lastClose
				#self.portfolio.units -= order
				
				self.portfolio.update(-order)
				# CHARGE FEES
				
				#print('sell order: {0}'.format(order))

		self.order = order # for calculating reward

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
	def get_score(self, action):
		#score = self.portfolio.getProfit()
		'''
		additional params: action
		# score depends on whether it chose correct buy|sell|hold
		
		# another NN can calculate size of swing or price
		# adding order may not be beneficial, since swings/changes are being looked for
		
		# if hold and stock>0
		#   reward +5 (opposed to -ve costs for trading)
		#     if price+ then reward +10
		#     else reward -10
		# if buy 
		#   if price+ then reward +15
		#   else reward -15
		# if sell 
		#   if price- then reward +15
		#   else reward -15
		if (
		'''
		score = 0
		if (action==1):	#hold 
			score +=5
			if (self.portfolio.last_close_delta >= 0): # price increased t+1		
				if (self.portfolio.units > 0): # have stock
					score +=10 					# reward holding stock
			else: 										# price decreased t+1
				if (self.portfolio.units > 0): # have stock
					score -=10					# punish holding stock
					
		elif (action==0):	# sell
			if (self.portfolio.last_close_delta >= 0): # price increased t+1			
				score -=10								# punish selling into bull
				#if (self.portfolio.units > 0): # have stock
				#	score +=10 					# reward holding stock
			else: 										# price decreased t+1
				score +=10								# reward selling into bear 
			if (self.portfolio.units > 0): # have stock
				score -=10					# punish holding stock
			
		elif (action==0):	# buy
			if (self.portfolio.last_close_delta >= 0): # price increased t+1			
				score +=10								# reward buying into bull
				#if (self.portfolio.units > 0): # have stock
				#	score +=10 					# reward holding stock
			else: 										# price decreased t+1
				score -=10								# punish buying into bear 
			if (self.portfolio.units > 0): # have stock
				score +=10					# reward holding stock
		
		return score

	def is_over(self):
		if (self.portfolio.benchmark() < Config.coef_lose):# or self.portfolio.benchmark() > 2): 
			return True
		elif (self.feed.isEod(self.horizon)): 
			return True
		else: return False

	# ! TO USE
	def is_won(self):
		if (self.portfolio.benchmark() > Config.coef_win): # doubled investment
			return True
		else: return False
				