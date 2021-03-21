
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
from pprint import pprint
import pandas as pd
import backtrader as bt

from pdb import set_trace

class SMA(bt.Strategy):
    params = dict(
      stop_loss=0
    )

    def __init__(self):
        self.sma50 = bt.ind.SimpleMovingAverage(period=50)
        self.sma200 = bt.ind.SimpleMovingAverage(period=200)
        self.stoch = bt.ind.Stochastic()
        
        self.cross = bt.ind.CrossOver(self.sma50, self.sma200)
        self.dataclose = self.datas[0].close

        self.conditions = {
          'price_above_50_sma': False,
          'price_above_200_sma': False,
          '50_above_200_sma': False,
          '50_slope_is_up': False,
          '50_curved_up': False
        }

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        pass

    def stop(self):
        pass
    
    def evaluate_long_position(self):
       return (
          self.conditions['price_above_50_sma'] == True and
          self.conditions['price_above_200_sma'] == True and
          self.conditions['50_above_200_sma'] == False and
          self.conditions['50_slope_is_up'] == True and
          self.conditions['50_curved_up'] == True
       )

    # Called after an order is made. ie. self.buy() or self.sell()
    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            print('SELL@price: {:.2f}'.format(order.executed.price))
            return
        
        print('BUY @price: {:.2f}'.format(order.executed.price))

        print(f'low: {self.datas[0]}')
        stop_price = order.executed.price * (1.0 - self.p.stop_loss)
        self.sell(exectype=bt.Order.Stop, price=stop_price)


    def next(self):
        # pprint(self.datas[0][-1]) # Last element

        sma50_diff = lambda i: self.sma50[-i] - self.sma50[-i-1]
        diff1 = sma50_diff(1)
        diff2 = sma50_diff(2)
        double_diff = diff1 - diff2

        self.conditions['price_above_50_sma'] = self.datas[0][-1] > self.sma50[-1]
        self.conditions['price_above_200_sma'] = self.datas[0][-1] > self.sma200[-1]
        self.conditions['50_above_200_sma'] = self.sma50[-1] > self.sma200[-1]
        self.conditions['50_slope_is_up'] = sma50_diff(1) > 0
        self.conditions['50_curved_up'] = (sma50_diff(1) - sma50_diff(2)) > 0

        pprint(self.conditions)
        # set_trace()
        should_enter = self.evaluate_long_position()
        if not self.position and should_enter:
            self.buy()
        
        if len(self.data) == self.data.buflen()-1:
            self.sell()
