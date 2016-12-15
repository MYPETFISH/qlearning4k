from keras.models import Sequential
from keras.layers import Flatten, Dense
from qlearning4k.games import Catch
from keras.optimizers import *
from keras.models import model_from_json

from qlearning4k import Agent

grid_size = 10
hidden_size = 100
nb_frames = 1

#load

json_file = open('C:/temp/py/fariz/catch' + '.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights('C:/temp/py/fariz/catch' + '.h5')
print("Loaded model")
         
# evaluate
model.compile(sgd(lr=.2), "mse")

catch = Catch(grid_size)
agent = Agent(model=model)
agent.play(catch)
