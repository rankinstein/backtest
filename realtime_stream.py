import asyncio
import websockets
import json
from rx.subject import Subject
import pprint
try:
    import thread
except ImportError:
    import _thread as thread

BASE_SOCKET = 'wss://stream.binance.com:9443'

def get_stream_url(ticker, timespan = '1m'):
  return BASE_SOCKET + '/ws/' + ticker.lower() + '@kline_' + timespan

def parse_kline(message):
    data = json.loads(message)

    candle = data.get('k')

    event_time = data.get('E')
    start_time = candle.get('t')
    close_time = candle.get('T')

    interval = candle.get('i')
    symbol = candle.get('s')

    high = candle.get('h')
    low = candle.get('l')
    open = candle.get('o')
    close = candle.get('c')
    volume = candle.get('v')
    is_last_tick = candle.get('x')
    
    return {
      'tick_time': event_time,
      'open_time': start_time,
      'close_time': close_time,
      'interval': interval,
      'symbol': symbol,
      'high': float(high),
      'low': float(low),
      'open': float(open),
      'close': float(close),
      'volume': float(volume),
      'is_last_tick': is_last_tick
    }

class BinanceStream():
    def __init__(self):
        self.stream = Subject()
        self.sockets = {}
        self.loop = asyncio.get_event_loop()

    async def on_message(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                next_message = parse_kline(message)
                self.stream.on_next(next_message)


            except websockets.ConnectionClosed as cc:
                print('Connection closed')
                self.stream.on_error(cc)

            except Exception as e:
                print('Something happened')
                self.stream.on_error(e)

    async def create_task(self, ticker):
        self.sockets[ticker] = await websockets.connect(get_stream_url(ticker))
        asyncio.ensure_future(self.on_message(self.sockets[ticker]))
    
    def connect(self, ticker):
        self.loop.run_until_complete(self.create_task(ticker))

    def run_forever(self):
        self.loop.run_forever()

if __name__ == '__main__':
    bs = BinanceStream()
    bs.connect('BTCUSDT')
    bs.connect('BNBBTC')
    bs.stream.subscribe(lambda x: pprint.pprint(x))
    bs.run_forever()