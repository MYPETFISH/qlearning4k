from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from qlearning4k.games import Catch
from keras.optimizers import *
from trade4k import Agent

grid_size = 10
hidden_size = 100
nb_frames = 1

horizon = 3
indicators = 7
vals = 3

in_shape = (horizon * indicators + vals,)   # need ,?
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

model = Sequential()
# input = 24, hidden = 12, out = 3
model.add(Dense(hidden_size, input_shape=in_shape, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(out_size, activation='softmax'))        # Q_sa tends to 1
model.compile(sgd(lr=lr), "mse")     #mean squared error

catch = Catch(grid_size)
trade = Trade(horizon=horizon, sessions=1000)
agent = Agent(model=model)          # roll own Agent?
agent.train(trade, batch_size=10, nb_epoch=1000, epsilon=.1)
agent.play(catch)
