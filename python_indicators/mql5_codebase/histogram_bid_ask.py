"""histogram_bid_ask — converted from MQL5: MQL5 Indicators/Histogram Bid and Ask prices/histogram_bid_ask.mq5

Histogram bid and ask prices
Copyright: Copyright 2016, DC2008; Link: http://www.mql5.com/ru/users/dc2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, DC2008', 'link': 'http://www.mql5.com/ru/users/dc2008', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Histogram bid and ask prices'], 'name': 'histogram_bid_ask', 'source': 'MQL5 Indicators/Histogram Bid and Ask prices/histogram_bid_ask.mq5', 'folder': 'Histogram Bid and Ask prices', 'inputs': [{'mql': 'histogram', 'py': 'histogram', 'param': 'histogram', 'type': 'int', 'default': 0, 'label': 'Prices for the analysis', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum hPrice
bid_and_ask = 0
high_and_low = 1
open_and_close = 2
_enum('hPrice', {0: 'bid_and_ask', 1: 'high_and_low', 2: 'open_and_close'})

# ---- inputs and global variables
prevTimeBar = 0
histogram = _input('histogram', bid_and_ask)  # Prices for the analysis

def OnInit():
    ObjectsDeleteAll(0, 0, -1)
    ChartRedraw(0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global prevTimeBar
    ArraySetAsSeries(time, True)
    if histogram == bid_and_ask:
        price = MqlTick()
        SymbolInfoTick(Symbol(), price)
        DrawHistogram(True, '+ ask=', price.ask, time[0])
        DrawHistogram(False, '- bid=', price.bid, time[0])
    if histogram == high_and_low:
        ArraySetAsSeries(high, True)
        ArraySetAsSeries(low, True)
        DrawHistogram(True, '+ high=', high[0], time[0])
        DrawHistogram(False, '- low=', low[0], time[0])
    if histogram == open_and_close:
        ArraySetAsSeries(close, True)
        ArraySetAsSeries(open, True)
        DrawHistogram(True, '+ close=', close[0], time[0])
        DrawHistogram(False, '- open=', open[0], time[0])
    if time[0] > prevTimeBar:
        prevTimeBar = time[0]
        for obj in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
            obj_name = ObjectName(0, obj, 0, -1)
            if StringFind(obj_name, '+', 0) >= 0:
                ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, time[0])
                str_ = ObjectGetString(0, obj_name, OBJPROP_TEXT)
                strint = StringSubstr(str_, 1)
                n = StringToInteger(strint)
                ObjectSetInteger(0, obj_name, OBJPROP_TIME, 1, time[0] + (10 * n))
                ObjectSetInteger(0, obj_name, OBJPROP_COLOR, clrLightCoral)
            if StringFind(obj_name, '-', 0) >= 0:
                ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, time[0])
                str_ = ObjectGetString(0, obj_name, OBJPROP_TEXT)
                strint = StringSubstr(str_, 1)
                n = StringToInteger(strint)
                ObjectSetInteger(0, obj_name, OBJPROP_TIME, 1, time[0] - (10 * n))
                ObjectSetInteger(0, obj_name, OBJPROP_COLOR, clrSkyBlue)
    ChartRedraw(0)
    return rates_total

def DrawHistogram(draw, h_name, price, time):
    if draw:
        name = h_name + _str(price)
        ObjectCreate(0, name, OBJ_TREND, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, 2)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price)
        ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price)
        if StringFind(ObjectGetString(0, name, OBJPROP_TEXT), '*', 0) < 0:
            ObjectSetString(0, name, OBJPROP_TEXT, '*1')
            ObjectSetInteger(0, name, OBJPROP_TIME, 1, time + 10)
        else:
            str_ = ObjectGetString(0, name, OBJPROP_TEXT)
            strint = StringSubstr(str_, 1)
            n = StringToInteger(strint)
            n += 1
            ObjectSetString(0, name, OBJPROP_TEXT, '*' + _str(n))
            ObjectSetInteger(0, name, OBJPROP_TIME, 1, time + (10 * n))
    if not draw:
        name = h_name + _str(price)
        ObjectCreate(0, name, OBJ_TREND, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_COLOR, clrBlue)
        ObjectSetInteger(0, name, OBJPROP_BACK, True)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, 2)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price)
        ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price)
        if StringFind(ObjectGetString(0, name, OBJPROP_TEXT), '*', 0) < 0:
            ObjectSetString(0, name, OBJPROP_TEXT, '*1')
            ObjectSetInteger(0, name, OBJPROP_TIME, 1, time - 10)
        else:
            str_ = ObjectGetString(0, name, OBJPROP_TEXT)
            strint = StringSubstr(str_, 1)
            n = StringToInteger(strint)
            n += 1
            ObjectSetString(0, name, OBJPROP_TEXT, '*' + _str(n))
            ObjectSetInteger(0, name, OBJPROP_TIME, 1, time - (10 * n))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HistogramBidAsk(_MQL5Indicator):
    name = 'histogram_bid_ask'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'histogram': _Choice({0: 'bid_and_ask', 1: 'high_and_low', 2: 'open_and_close'}, default=0),  # Prices for the analysis
    }

