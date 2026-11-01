"""Schaff trend CCI — converted from MQL5: MQL5 Indicators/Schaff trend CCI/Schaff trend CCI.mq5

Schaff trend CCI
Copyright: Copyright 2018, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 32768, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Schaff trend CCI value'}, 'levels': [], 'description': ['Schaff trend CCI'], 'name': 'Schaff trend CCI', 'source': 'MQL5 Indicators/Schaff trend CCI/Schaff trend CCI.mq5', 'folder': 'Schaff trend CCI', 'inputs': [{'mql': 'CciPeriod', 'py': 'CciPeriod', 'param': 'CciPeriod', 'type': 'double', 'default': 50.0, 'label': 'CCI period', 'sinput': False}, {'mql': 'FastEma', 'py': 'FastEma', 'param': 'FastEma', 'type': 'int', 'default': 23, 'label': 'Fast ema period', 'sinput': False}, {'mql': 'SlowEma', 'py': 'SlowEma', 'param': 'SlowEma', 'type': 'int', 'default': 50, 'label': 'Slow ema period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CciPeriod = _input('CciPeriod', 50.0)  # CCI period
FastEma = _input('FastEma', 23)  # Fast ema period
SlowEma = _input('SlowEma', 50)  # Slow ema period
Price = _input('Price', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workCci = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Schaff trend CCI (' + _str(FastEma) + ',' + _str(SlowEma) + ',' + _str(CciPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        val[i] = iCci(iEma(price, FastEma, i, rates_total, 0) - iEma(price, SlowEma, i, rates_total, 1), CciPeriod, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iCci(price, period, i, bars, instanceNo=0):
    if ArrayRange(workCci, 0) != bars:
        ArrayResize(workCci, bars)
    workCci[i][instanceNo + 0] = price
    avg = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        avg += workCci[i - k][instanceNo]
        k += 1
    avg = _fdiv(avg, period)
    dev = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        dev += MathAbs(workCci[i - k][instanceNo] - avg)
        k += 1
    dev = _fdiv(dev, period)
    cci = (_fdiv(price - avg, 0.015 * dev) if (dev != 0) else 0)
    return cci

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class SchaffTrendCCI(_MQL5Indicator):
    name = 'Schaff trend CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CciPeriod': 50.0,  # CCI period
        'FastEma': 23,  # Fast ema period
        'SlowEma': 50,  # Slow ema period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

