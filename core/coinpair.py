import urllib
import urllib2
import json
import time
import hmac,hashlib
from poloniex import poloniex
import coin
import pandas as pd
import numpy as np
import datetime

class CoinPair:
    def __init__(self, conn=None):
        self.name=''
        self.currPrice=-1
        self.currVolume=-1
        self.high24hr=-1
        self.low24hr=-1
        self.conn=conn

    def add_coin(self, name,conn):
        self.name=name
        if conn:
            self.conn=conn
            value=conn.api_query("returnTicker")[name]
            self.currPrice=float(value['last'])
            self.currValue=float(value['baseVolume'])
            self.high24hr=float(value['high24hr'])
            self.low24hr=float(value['low24hr'])
        else:
            print 'Warning: missing the latest data'

    def reset(self):
        self.__init__()

    def get_current_status(self):
        status={
                'name':self.name, 
                'price':self.currPrice,
                'volue':self.currVolume,
                'high24hr':self.high24hr,
                'low24hr':self.low24hr
                }
        return status


    def get_historical_data(self, startTime, endTime, period, save=False):
        # conn: connection to Poloniex API
        # startTime/endTime: datetime
        # period: time intervals, available paras 300, 900, 1800, 7200, 14400, and 86400
        startTime=startTime.strftime('%s')
        endTime=endTime.strftime('%s')
        historicalData = self.conn.api_query("returnChartData",{"currencyPair":self.name,"start":startTime,"end":endTime,"period":period})
        if save:
            filename='dataset/'+self.name+'.txt'
            d=np.array([l.values() for l in historicalData]) # get the array of all values
            dateTime=[datetime.datetime.utcfromtimestamp(l['date']) for l in historicalData] # get the datetime of timestamp
            columns=[key if key!='date' else 'timestamp' for key in historicalData[1].keys()] # get the column names from the dataframe
            pd.DataFrame(data=d, columns=columns, index=dateTime).to_csv(filename, index_label='utcdatetime')
        return historicalData

