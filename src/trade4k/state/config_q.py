'''
    Contains static variables like paths
'''

class Config(object):

    f_agent = 'agent_stats'
    f_data = 'test_4_rio_rv_rg.csv'
    save_uri = "C:/temp/py/k/3/"
    data_uri = "C:/temp/py/k/test_4_rio_rv_rg.csv"

    #f_model = '_model_2h_2'

    funds = 10000
    units = 0
    policy_funds = 1    # 1=100% funds used per order
    policy_stocks = 1   # 1=100% units sold per order

    lr=0.1
    horizon=2
    batch_size=75
    epoch = 1500

    f_model = 'kmodel_' + str(horizon) +'_'
    
    start_session = 750
    start_vary = 300

    floor_coef = .5
    coef_win= 1.15       # beat buy and hold by 15%
    coef_lose = 0.75    # lost 1/4 of wealth compared to buy and hold
    
    
    gamma = .95        # Discount factor
    epsilon = .3       # Exploration factor. Can be an integer or a tuple/list of integers with 2 integers. If tuple/list, exploration factor will drop from the first value to the second during traing. 
    epsilon_rate = .8  # Rate that epsilon should drop. If its 0.4 for example, epsilon will reach the lower value by the time 40 % of the training is complete.
    
    def __init__(self, params):
        pass