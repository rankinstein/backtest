
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
from pprint import pprint
import pandas as pd
import backtrader as bt

class Hodl(bt.SignalStrategy):
    def __init__(self):
        self.inposition = False
        self.sma50 = bt.ind.SimpleMovingAverage(period=50)
        self.sma200 = bt.ind.SimpleMovingAverage(period=200)
        self.stoch = bt.ind.Stochastic()
        
        self.cross = bt.ind.CrossOver(self.sma50, self.sma200)
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        pass

    def stop(self):
        pass

    def next(self):
        if not self.inposition:
            self.inposition = True
            self.buy()
        
        if len(self.data) == self.data.buflen() - 1:
            self.sell()
