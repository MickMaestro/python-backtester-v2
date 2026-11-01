"""Intraday Keltner channel (extended) — converted from MQL5: MQL5 Indicators/Intra-day Keltner channel extended/Intraday Keltner channel (extended).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [7451452], 2: [8421504], 3: [17919]}, 'widths': {}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper band', 2: 'Average', 3: 'Lower band'}, 'levels': [], 'description': [], 'name': 'Intraday Keltner channel (extended)', 'source': 'MQL5 Indicators/Intra-day Keltner channel extended/Intraday Keltner channel (extended).mq5', 'folder': 'Intra-day Keltner channel extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.0, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpMultiplier = _input('inpMultiplier', 1.0)  # ATR multiplier
val = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
tr = Arr(0, 0.0)
prices = Arr(0, 0.0)
_timeFrame = PERIOD_D1
_timeFrameName = 'day'

def OnInit():
    global _timeFrame, _timeFrameName
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, tr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    if Period() == PERIOD_D1:
        _timeFrame = PERIOD_W1
        _timeFrameName = 'week'
    if Period() == PERIOD_W1 or Period() == PERIOD_MN1:
        _timeFrame = PERIOD_MN1
        _timeFrameName = 'month'
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intra-' + _timeFrameName + ' Keltner channel (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _highTfBar = iBarShift(Symbol(), _timeFrame, time[i])
        _highTfTime = iTime(Symbol(), _timeFrame, _highTfBar)
        _firstBar = iBarShift(Symbol(), Period(), _highTfTime)
        prices[i] = getPrice(inpPrice, open, high, low, close, i)
        tr[i] = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        k = 1
        _period = (inpPeriod if (_timeFrame == PERIOD_MN1) else (i - (rates_total - _firstBar - 1) + 1))
        if _period > inpPeriod:
            _period = inpPeriod
        val[i] = prices[i]
        _atr = tr[i]
        while k < _period and i >= k:
            _atr += tr[i - k]
            val[i] += prices[i - k]
            k += 1
        _atr = _fdiv(_atr, float(k))
        val[i] = _fdiv(val[i], float(k))
        valu[i] = val[i] + (inpMultiplier * _atr)
        vald[i] = val[i] - (inpMultiplier * _atr)
        i += 1
    return i

def getPrice(tprice, open, high, low, close, i):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntradayKeltnerChannelExtended(_MQL5Indicator):
    name = 'Intraday Keltner channel (extended)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpMultiplier': 1.0,  # ATR multiplier
    }

