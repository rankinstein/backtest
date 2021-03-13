import pandas as pd
from binance.client import Client
import datetime
import secrets

# YOUR API KEYS HERE
api_key = secrets.api_key
api_secret = secrets.api_secret

bclient = Client(api_key=api_key, api_secret=api_secret)

start_date = datetime.datetime.strptime('1 Jan 2021', '%d %b %Y')
today = datetime.datetime.today()

BASE_DIR = 'price_history/'

def binanceBarExtractor(symbol, interval = Client.KLINE_INTERVAL_1MINUTE):
    print('working...')
    filename = f'{symbol}_{interval}.csv'

    klines = bclient.get_historical_klines(symbol, interval, start_date.strftime("%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:%M:%S"), 1000)
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    data.set_index('timestamp', inplace=True)
    data.to_csv(BASE_DIR + filename)
    print('finished!')


if __name__ == '__main__':
    # Obviously replace BTCUSDT with whichever symbol you want from binance
    # Wherever you've saved this code is the same directory you will find the resulting CSV file
    binanceBarExtractor('BNBBTC', Client.KLINE_INTERVAL_4HOUR)