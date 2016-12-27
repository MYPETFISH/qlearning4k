from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, LSTM
from keras.optimizers import *
from keras.models import model_from_json


from trade4k.games.trade import Trade
from trade4k.agent import Agent
from trade4k.state.config import Config

#indicators = 7
#vals = 3

#in_dim = (Config.horizon * indicators) + vals
#hidden_size = in_dim/2 - 2

out_size = 3
#lr = 0.01
'''
model = Sequential()
model.add(Flatten(input_shape=(nb_frames, grid_size, grid_size)))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(3))
model.compile(sgd(lr=.2), "mse")
'''

# to work with game, need following shape
input_shape =(Config.nb_frames, Config.in_dim)

print('test_trade')
loading=False

if (loading):
    json_file = open(Config.save_uri + Config.f_model + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    
    # load weights into new model
    model.load_weights(Config.save_uri + Config.f_model + '.h5')
    print("Loaded model from disk")
         
    #compile here with lr=0.2         
    model.compile(sgd(lr=Config.lr), "mse")     #mean squared error
    # evaluate loaded model on qlearn_viz data
else:
    model = Sequential()
    # input = 24, hidden = 12, out = 3
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(Config.hidden_size, activation='relu'))
    #model.add(Dropout(0.5)) - backend doesnt like dropout
    model.add(Dense(out_size, activation='softmax'))        # Q_sa tends to 1
    model.compile(sgd(lr=Config.lr), "mse")     #mean squared error
    
    
trade = Trade(horizon=Config.horizon, sessions=Config.sessions)
agent = Agent(model=model, memory_size=Config.memory_size)          # roll own Agent?
# 200 is slow when sorting. Try 75
agent.train(trade, batch_size=Config.batch_size, nb_epoch=Config.epoch, epsilon=Config.epsilon)
#agent.play(trade)
