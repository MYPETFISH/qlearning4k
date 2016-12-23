'''
Created on 8Dec.,2016

@author: U6028300
'''
import numpy as np

import matplotlib.pyplot as plt

from trade4k.state.config import Config

#config = Config()

uri = "C:/temp/py/k/3/"

#f_fig = '3/fig/train'
f_fig = 'fig/train'
    
i=0
while (i<2):
    data = np.loadtxt(open(uri + 'train' + str(i) + '.csv', 'rb'), delimiter=',')
    #data = np.loadtxt(open(Config.save_uri + '_run' + '.csv', 'rb'), delimiter=',')
                     
    fig = plt.figure()
    
    # units funds pval
    # wealth
    #sell = data[0:,0:1]
    
    pval = data[0:, 2:3]
    funds = data[0:, 1:2]
    units = data[0:, 0:1]
    wealth = data[0:, 3:4]
    price = data[0:, 4:5]
    
    ax1 = fig.add_subplot(511)
    ax1.plot(wealth)
    ax1.axhline(y=1.0,linewidth=1, color='r')
    ax1.set_title('wealth generated | epoch {}'.format(str(i)))        
    
    ax2 = fig.add_subplot(512, sharex=ax1)
    ax2.plot(pval)
    ax2.set_title('pval')             
    
    ax5 = fig.add_subplot(513, sharex=ax1)
    ax5.plot(price)
    ax5.set_title('price')             
    
    ax3 = fig.add_subplot(514)
    ax3.plot(funds)
    ax3.set_title('funds')        
    
    ax4 = fig.add_subplot(515)
    ax4.plot(units)
    ax4.set_title('units')             
    
    plt.subplots_adjust(hspace = .3)
    
    #format the tics
    plt.sca(ax1)
    plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off

    #format the tics
    plt.sca(ax5)
    plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off

    #format the tics
    plt.sca(ax2)
    plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off

    #format the tics
    plt.sca(ax3)
    plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off

    
    #plt.show()
    save_uri = uri + f_fig + str(i) + '.png'
    plt.savefig(save_uri, bbox_inches='tight')
    #plt.savefig(save_uri)
    #plt.show()
    i = i+1
    plt.close()
