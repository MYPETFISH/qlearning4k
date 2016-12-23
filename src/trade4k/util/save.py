'''
Created on 16Dec.,2016

@author: u6028300
'''
import csv

from trade4k.state.config import Config
from datetime import datetime

class Save(object):

    def __init__(self):
        '''
        Constructor
        '''

    def save_model(self, model, name):

        # serialize model to JSON
        model_json = model.to_json()
        with open(Config.save_uri + name + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(Config.save_uri+ name + '.h5')
        print("Saved model to disk")           
 
    '''
    def log(self, game, S, q, a, r, e):
        # units funds pval
        # wealth
        
        row = game.portfolio.getVals()  
        w = game.portfolio.benchmark()
        p = game.portfolio.lastClose
        row.append(w)
        row.append(p)
         
        with open(Config.save_uri + '_agent' + str(e) + '.csv', 'a') as to_f:
            wr = csv.writer(to_f, quoting=csv.QUOTE_NONE)
            wr.writerow(row)
    '''
    def log(self, game, e):
        # units funds pval
        # wealth
        
        row = game.portfolio.getVals()  
        w = game.portfolio.benchmark()
        p = game.portfolio.lastClose
        row.append(w)
        row.append(p)
         
        if (game.trained): f_name  = 'run'
        else: f_name = 'train' 
         
        with open(Config.save_uri + f_name + str(e) + '.csv', 'a') as to_f:
            wr = csv.writer(to_f, quoting=csv.QUOTE_NONE)
            wr.writerow(row)
 
        
    def log_epoch(self, loss, win, loss_avg):
        # units funds pval
        # wealth
        
        row = [loss, win, loss_avg]
         
        #tag = "{:%m-%d_%H_%M_%S}"
        tag = "{:%m-%d}"

        with open(Config.save_uri + 'epochs_' + tag.format(datetime.now()) + '.csv', 'a') as to_f:
            wr = csv.writer(to_f, quoting=csv.QUOTE_NONE)
            wr.writerow(row)
