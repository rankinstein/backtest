#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2020 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
from pprint import pprint
import pandas as pd

import backtrader as bt

def get_df():
  df = pd.read_csv('./price_history/ADABNB_5m_2021-03-16_to_2021-03-18.csv',index_col=0,parse_dates=True)

  # def convertTS(ts):
  #   try:
  #     return datetime.fromtimestamp(ts)
  #   except ValueError as e:
  #     return ''
  # df.index.map(convertTS)
  pprint(df.index)
  df.index = pd.to_datetime(df.index)
  df.index.name = 'datetime'
  return df

class SmaCross(bt.SignalStrategy):
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
        
        if len(self.data) == self.data.buflen():
            self.inposition = False
            self.sell()
        # pprint(self.stoch)
        # self.log('Stoch, %.2f' % self.stoch)
        # if not self.inposition and self.cross == 1:
        #     self.inposition = True
        #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #     self.buy()
        #     pass

        # elif self.inposition and self.cross == -1:
        #     self.inposition = False
        #     self.log('Sell CREATE, %.2f' % self.dataclose[0])
        #     self.sell()
        #     pass

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)
cerebro.addstrategy(SmaCross)

df = get_df()

data0 = bt.feeds.PandasData(
    dataname=df,
    timeframe=bt.TimeFrame.Minutes,
    compression=5)

cerebro.adddata(data0)

cerebro.run()
cerebro.plot()