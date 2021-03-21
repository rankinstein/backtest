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
from strategies import Hodl, SMA

TS_MULTIPLE = 1000000 # Scale the timestamp for correct parsing

def get_df():
  df = pd.read_csv('./price_history/LINKBTC_1h_2021-02-01_to_2021-03-14.csv',index_col=0,parse_dates=True)
  df.index = pd.to_datetime(df.index.map(lambda x: x * TS_MULTIPLE))
  df.index = df.index
  df.index.name = 'datetime'
  return df

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)
cerebro.addstrategy(SMA)

df = get_df()

data0 = bt.feeds.PandasData(
    dataname=df,
    timeframe=bt.TimeFrame.Minutes,
    compression=5)

cerebro.adddata(data0)

cerebro.run()
cerebro.plot(style='candlestick', barup='green')