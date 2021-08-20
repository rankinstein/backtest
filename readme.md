# Intro
Basic setup for capturing historical binance data.

# Goals
1. Fetch historical data
2. Playback historical data
3. Run strategies against historical data
4. Evaluate effectiveness of strategies
5. Screen data for desired conditions

# Pre-Setup
1. Get binance API keys and copy them to `secrets.py`
```
# secrets.py
api_key = 'KEY_HERE'
api_secret = 'SECRET_HERE'
```
2. The `secrets.py` should look like this:
   ```
   api_key = 'API_KEY_FROM_BINANCE'
   api_secret = 'API_SECRET_FROM_BINANCE'
   ```
2. Create your python virtual env `python3 -m venv .`

# Setup
1. Activate venv: `source bin/activate`
   Note: to close your virtual env `deactivate`
2. Install requirements: `pip3 install -r requirements.txt`

# Scripts
## download_history.py
Save historical data as csv files. Defaults to `BTCUSDT` `1 hour`

Examples:
- `python download_historical.py BTCUSDT 4h`

## realtime_stream.py
Read live streamed data from Binance. Defaults to `BTCUSDT 1-minute`

# References
- Binance WS API: `https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams`
- Basic algo trading tutorial: 
- Capturing historical data: `https://fxgears.com/index.php?threads/how-to-acquire-free-historical-tick-and-bar-data-for-algo-trading-and-backtesting-in-2020-stocks-forex-and-crypto-currency.1229/#post-19305`