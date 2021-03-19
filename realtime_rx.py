import rx
import numpy as np
from pprint import pprint
import realtime_stream

candles = []

def one_at_a_time():
    def _one_at_a_time(source):
        def subscribe(observer, scheduler = None):
            def on_next(value):
                if isinstance(value, list):
                    for val in value:
                        observer.on_next(val)
                else:
                    observer.on_next(value)

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler)
        return rx.create(subscribe)
    return _one_at_a_time

def rolling_buffer(size):
    buffer = []
    def _rolling_buffer(source):
        def subscribe(observer, scheduler = None):
            def on_next(value):
                if len(buffer) >= size:
                    buffer.pop(0)
                buffer.append(value)
                observer.on_next(buffer)

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler)
        return rx.create(subscribe)
    return _rolling_buffer

def calculate_average(key):
    def _calculate_average(source):
        def subscribe(observer, scheduler = None):
            def on_next(raw_value):
                value = raw_value
                values = 'null'
                try:
                    values = list(map(lambda x: x.get(key, ''), value))
                    values = np.array(values)
                    observer.on_next(values.mean())
                except TypeError as e:
                    print("CALCULATE AVERAGE ERROR")
                    print(key)
                    print(type(value))
                    print(value)
                    print(values)
                    print(e)
            
            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler)
        return rx.create(subscribe)
    return _calculate_average
                

def on_subscribe(message):
    try:
        current_candle = candles[-1]
        if current_candle['is_last_tick']:
            candles.append(message)
        else:
            candles[-1] = message
    except IndexError:
        candles.append(message) # An index error will be thrown on the very first event when candles is empty
    pprint(candles)

def log(value):
   print(f"Received {value}") 

def simple_moving_average(stream, period=10):
    return stream.pipe(rolling_buffer(period), calculate_average('close'))

bs = realtime_stream.BinanceStream()
bs.connect('BTCUSDT')

sma50 = simple_moving_average(bs.stream, period=50)
sma200 = simple_moving_average(bs.stream, period=200)
sma50.subscribe(log)
sma200.subscribe(log)

bs.run_forever()

