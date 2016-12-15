import csv
import numpy as np
import os

from keras.models import model_from_json

''' D, O, H, L, C, V, AD'''
class Loader(object):
    
    def __init__(self):
        self.modelFile = "model.h5"
        self.modelUri = "C:/temp/py/"    

    ''' date, o,h,l,c,vol,adj 
    
        is NOT a numpy array on load, so that data can be munged
    '''
    def load(self, uri):
        with open(uri, 'rU') as from_f:     # U universal newline to avoid \n errors
            data_iter = csv.reader(from_f, 
                           delimiter = ',',
                           dialect=csv.excel_tab)
            data = [data for data in data_iter]

            self.data = data
            self.records = data.__len__()
            print ('{0} records'.format(self.records))
            
    def sessions(self, length, start=0):
        if (self.data.__sizeof__() < (length+start)):
            print ('insufficient data {0} present, require {1}'.format(self.periods, length))
        else:
            return self.data[start:start+length]     #for numpy
        
    '''        
    def loadModel(self):
        # load json and create model
        json_file = open(self.modelUri + self.modelFile  + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(self.modelUri + self.modelFile + '.h5')
        print("Loaded model from disk")
         
        compile here with lr=0.2         
        # evaluate loaded model on qlearn_viz data
        return loaded_model
    
    def saveModel(self, model):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(self.modelUri + self.modelFile + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(self.modelUri + self.modelFile + '.h5')
        print("Saved model to disk")


    def modelExists(self):
        return os.path.isfile(self.modelUri + self.modelFile + ".json")
    '''