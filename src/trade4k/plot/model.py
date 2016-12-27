'''
Created on 24Dec.,2016

@author: U6028300
'''
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import *

from keras.utils.visualize_util import plot

from keras.models import model_from_json

from trade4k.state.config import Config

json_file = open(Config.save_uri + Config.f_model + '.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
    
# load weights into new model
model.load_weights(Config.save_uri + Config.f_model + '.h5')
print("Loaded model from disk")
         
model.compile(sgd(lr=Config.lr), "mse")     #mean squared error

plot(model, to_file=Config.save_uri + 'fig/' + Config.f_model + '.png')
