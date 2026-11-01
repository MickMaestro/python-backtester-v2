"""Rsi(var) zerolag MA — converted from MQL5: MQL5 Indicators/Rsi(var) Zerolag MA/Rsi(var) zerolag MA.mq5

Rsi(var) zerolag MA
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 101.0}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [50.0], 'description': ['Rsi(var) zerolag MA'], 'name': 'Rsi(var) zerolag MA', 'source': 'MQL5 Indicators/Rsi(var) Zerolag MA/Rsi(var) zerolag MA.mq5', 'folder': 'Rsi(var) Zerolag MA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # RSI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
workZl = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi(var) zerolag MA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _price1 = prices[i]
        _price2 = (prices[i - 1] if (i > 0) else prices[i])
        _bulls = 0.5 * (MathAbs(_price1 - _price2) + (_price1 - _price2))
        _bears = 0.5 * (MathAbs(_price1 - _price2) - (_price1 - _price2))
        _avgBulls = iZeroLag(_bulls, inpPeriod, i, rates_total, 0)
        _avgBears = iZeroLag(_bears, inpPeriod, i, rates_total, 1)
        val[i] = (MathMax(MathMin(_fdiv(100.0, 1 + _fdiv(_avgBears, _avgBulls)), 100), 0) if (_avgBulls != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iZeroLag(price, length, r, bars, instanceNo=0):
    if length <= 1:
        return price
    if ArrayRange(workZl, 0) != bars:
        ArrayResize(workZl, bars)
    instanceNo *= 2
    workZl[r][0 + instanceNo] = price
    median = 0.0
    alpha = _fdiv(2.0, 1.0 + length)
    per = _int((length - 1.0) / 2.0)
    if r < (per + 1):
        workZl[r][1 + instanceNo] = price
    else:
        if _imod(_int(length), 2) == 0:
            median = (workZl[r - per][0 + instanceNo] + workZl[r - per - 1][0 + instanceNo]) / 2.0
        else:
            median = workZl[r - per][0 + instanceNo]
        workZl[r][1 + instanceNo] = workZl[r - 1][1 + instanceNo] + (alpha * ((2.0 * price) - median - workZl[r - 1][1 + instanceNo]))
    return workZl[r][1 + instanceNo]

def getPrice(tprice, open, close, high, low, i, _bars):
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


class RsiVarZerolagMA(_MQL5Indicator):
    name = 'Rsi(var) zerolag MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (-1.0, 101.0)

