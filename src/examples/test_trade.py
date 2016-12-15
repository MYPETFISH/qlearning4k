from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.optimizers import *

from trade4k.games.trade import Trade
from trade4k.agent import Agent

nb_frames = 1

horizon = 3
indicators = 7
vals = 3

in_dim = (horizon * indicators) + vals
#in_shape = (in_dim,)   
hidden_size = in_dim/2

out_size = 3
lr = 0.005
'''
model = Sequential()
model.add(Flatten(input_shape=(nb_frames, grid_size, grid_size)))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(3))
model.compile(sgd(lr=.2), "mse")
'''

# to work with game, need following shape
input_shape =(nb_frames, in_dim)

model = Sequential()
# input = 24, hidden = 12, out = 3
model.add(Dense(hidden_size, input_shape=input_shape))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(out_size, activation='softmax'))        # Q_sa tends to 1
model.compile(sgd(lr=lr), "mse")     #mean squared error

trade = Trade(horizon=horizon, sessions=1000)
agent = Agent(model=model)          # roll own Agent?
agent.train(trade, batch_size=200, nb_epoch=1000, epsilon=.1)
#agent.play(trade)
