#!/usr/bin/env python
# -------------------
# Example: ./download_historical.py BTCUSDT 1h
#
import pandas as pd
from binance.client import Client
import datetime
import sys
import secrets

# YOUR API KEYS HERE
api_key = secrets.api_key
api_secret = secrets.api_secret

bclient = Client(api_key=api_key, api_secret=api_secret)

start_date = datetime.datetime.strptime('16 Mar 2021', '%d %b %Y')
today = datetime.datetime.today()

BASE_DIR = 'price_history/'

def parseArgs(args):
    ticker = 'BTCUSDT'
    time_period = Client.KLINE_INTERVAL_1HOUR
    if len(sys.argv) > 1:
      ticker = sys.argv[1]
    if len(sys.argv) > 2:
      time_period = sys.argv[2]
    return [ ticker, time_period ]

def binanceBarExtractor(symbol, interval = Client.KLINE_INTERVAL_1MINUTE):
    print('working...')
    filename = f'{symbol}_{interval}_{start_date.strftime("%Y-%m-%d")}_to_{today.strftime("%Y-%m-%d")}.csv'

    klines = bclient.get_historical_klines(symbol, interval, start_date.strftime("%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:%M:%S"), 1000)
    data = pd.DataFrame(klines, columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

    data.set_index('open_time', inplace=True)
    data.to_csv(BASE_DIR + filename)
    print('finished!')

if __name__ == '__main__':
    [ ticker, time_period ] = parseArgs(sys.argv)
    binanceBarExtractor(ticker, time_period)