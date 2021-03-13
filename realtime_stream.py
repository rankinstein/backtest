import websocket
import json
import pprint

BASE_SOCKET = 'wss://stream.binance.com:9443'

candles = []

def get_stream_url(ticker, timespan = '1m'):
  return BASE_SOCKET + '/ws/' + ticker.lower() + '@kline_' + timespan

def on_open(ws):
  print('on open')

def on_close(ws):
  print('on close')
  pprint.pprint(candles)

def on_message(ws, message):
  print('on message')
  data = json.loads(message)
  if data.get('e') == 'kline':
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

    if is_last_tick:
      print('last tick of candle')
      candles.append({
        "start": start_time,
        "end": close_time,
        "interval": interval,
        "symbol": symbol,
        "high": high,
        "low": low,
        "open": open,
        "close": close,
        "volume": volume
      })

    print(f'High: {high}')
    print(f'Low: {low}')
    print(f'Open: {open}')
    print(f'Close: {close}')
    print(f'Volume: {volume}')
    print(f'Last tick: {is_last_tick}')

def on_error(ws, error):
  print(error)

if __name__ == '__main__':
    SOCKET_URL = get_stream_url('BTCUSDT')
    print(f'connecting to: {SOCKET_URL}')
    ws = websocket.WebSocketApp(SOCKET_URL, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
    ws.run_forever()