from keras.models import Sequential
from keras.layers import Flatten, Dense

from keras.optimizers import *
from keras.models import model_from_json

from trade4k.agent import Agent
from trade4k.state.config import Config
from trade4k.games.trade import Trade

grid_size = 10
hidden_size = 100
nb_frames = 1

#load

json_file = open(Config.save_uri + Config.f_model + '.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights(Config.save_uri + Config.f_model + '.h5')
print("model loaded")
         
# evaluate
model.compile(sgd(lr=Config.lr), "mse")
print("model compiled")

trade = Trade(horizon=Config.horizon, sessions=2000)
trade.trained=True
agent = Agent(model=model)
agent.play(trade)
