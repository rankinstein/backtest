import pandas as pd
from rx.subject import ReplaySubject
import pprint

class HistoricalStream():
    def __init__(self):
        self.stream = ReplaySubject()

    def load(self, path, symbol, interval):
        self.df = pd.read_csv(path)
        for _, row in self.df.iterrows():
            payload = {
                'tick_time': int(row['close_time']),
                'open_time': int(row['open_time']),
                'close_time': int(row['close_time']),
                'interval': interval,
                'symbol': symbol,
                'is_last_tick': True,
                'high': float(row['high']),
                'low': float(row['low']),
                'open': float(row['open']),
                'tick': float(row['close']),
                'volume': float(row['volume'])
            }
            self.stream.on_next(payload)

if __name__ == '__main__':
    hs = HistoricalStream()
    hs.load('price_history/LINKBTC_1h_2021-02-01_to_2021-03-14.csv', 'BTCUSDT', '1h')
    hs.stream.subscribe(lambda x: pprint.pprint(x))