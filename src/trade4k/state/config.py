'''
    Contains static variables like paths
'''

class Config(object):

    f_agent = 'agent_stats'
    f_data = 'test_4_rio_rv_rg.csv'
    save_uri = "C:/temp/py/k/"
    data_uri = "C:/temp/py/k/test_4_rio_rv_rg.csv"

    funds = 10000
    units = 0
    policy_funds = 1    # 1=100% funds used per order
    policy_stocks = 1   # 1=100% units sold per order

    floor_coef = .5

    def __init__(self, params):
        pass