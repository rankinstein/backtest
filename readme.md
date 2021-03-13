# Intro
Basic setup for capturing historical binance data.

# Goals
1. Fetch historical data
2. Playback historical data
3. Run strategies against historical data
4. Evaluate effectiveness of strategies

# Pre-Setup
1. Get binance API keys and copy them to secrets.py
2. Create your python virtual env `python3 -m venv .`

# Setup
1. Activate venv: `source bin/activate`
   Note: to close your virtual env `deactivate`
2. Install requirements: `pip3 install -r requirements.txt`

# References
- Binance WS API: `https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams`
- Basic algo trading tutorial: 
- Capturing historical data: `https://fxgears.com/index.php?threads/how-to-acquire-free-historical-tick-and-bar-data-for-algo-trading-and-backtesting-in-2020-stocks-forex-and-crypto-currency.1229/#post-19305`