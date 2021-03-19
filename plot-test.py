import pandas as pd
import os
import mplfinance as mpf
from math import pi
from datetime import datetime
from pprint import pprint

from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models.widgets import Dropdown
from bokeh.io import curdoc
from bokeh.layouts import column

from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool
from bokeh.palettes import Category20, Greys
from bokeh.models.formatters import NumeralTickFormatter

# Define constants
W_PLOT = 800
H_PLOT = 600
TOOLS = 'pan,wheel_zoom,hover,reset'

VBAR_WIDTH = 2.5
MARK_OFFSET = 0.00001
RED = Category20[7][6]
GREEN = Category20[5][4]

BLACK = Greys[9][2]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]

def get_df():
  df = pd.read_csv('./price_history/LINKBTC_1h_2021-02-01_to_2021-03-14.csv',index_col=0,parse_dates=True)

  # def convertTS(ts):
  #   try:
  #     return datetime.fromtimestamp(ts)
  #   except ValueError as e:
  #     return ''
  # df.index.map(convertTS)
  pprint(df.index)
  df.index = pd.to_datetime(df.index)
  df.index.name = 'date'
  return df

def plot_stock_price(stock):
   
    p = figure(plot_width=W_PLOT, plot_height=H_PLOT, tools=TOOLS,
               title="Stock price", toolbar_location='above')

    inc = stock.data['close'] > stock.data['open']
    dec = stock.data['open'] > stock.data['close']
    view_inc = CDSView(source=stock, filters=[BooleanFilter(inc)])
    view_dec = CDSView(source=stock, filters=[BooleanFilter(dec)])

    # pprint(stock.data['date'])

    # map dataframe indices to date strings and use as label overrides
    # p.xaxis.major_label_overrides = {
    #     i+int(stock.data['index'][0]): date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(stock['date']))
    # }
    p.xaxis.bounds = (stock.data['date'][0], stock.data['date'][-1])


    p.segment(x0='date', x1='date', y0='low', y1='high', color=BLACK, source=stock, view=view_inc)
    p.segment(x0='date', x1='date', y0='low', y1='high', color=BLACK, source=stock, view=view_dec)

    p.vbar(x='date', width=VBAR_WIDTH, top='open', bottom='close', fill_color=GREEN, line_color=GREEN,
           source=stock,view=view_inc, name="price")
    p.vbar(x='date', width=VBAR_WIDTH, top='open', bottom='close', fill_color=RED, line_color=RED,
           source=stock,view=view_dec, name="price")
    
    p.asterisk(stock.data['date'], stock.data['high'] + MARK_OFFSET)
    p.line(stock.data['date'], stock.data['close'])

    # p.legend.location = "top_left"
    # p.legend.border_line_alpha = 0
    # p.legend.background_fill_alpha = 0
    # p.legend.click_policy = "mute"

    p.yaxis.formatter = NumeralTickFormatter(format='$ 0,0[.]000000000')
    p.x_range.range_padding = 0.05
    p.xaxis.ticker.desired_num_ticks = 40
    p.xaxis.major_label_orientation = 3.14/4
    
    # Select specific tool for the plot
    price_hover = p.select(dict(type=HoverTool))

    # Choose, which glyphs are active by glyph name
    price_hover.names = ["price"]
    # Creating tooltips
    price_hover.tooltips = [("Datetime", "@date{%h:%m}"),
                            ("Open", "@open{$0,0.00000000}"),
                            ("Close", "@close{$0,0.00000000}"),
                           ("Volume", "@volume{(0.00 a)}")]
    price_hover.formatters={"Date": 'datetime'}

    return p

  
stock = ColumnDataSource(
    data=dict(Date=[], Open=[], Close=[], High=[], Low=[],index=[]))
symbol = 'msft'
df = get_df()
stock.data = stock.from_df(df)
elements = list()

# update_plot()
p_stock = plot_stock_price(stock)

elements.append(p_stock)

curdoc().add_root(column(elements))
curdoc().title = 'Bokeh stocks historical prices'

show(p_stock)