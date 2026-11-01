"""Elliot oscillator simple — converted from MQL5: MQL5 Indicators/Elliot Oscillator Simple/Elliot oscillator simple.mq5

Elliot oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [13759441, 12052223], 2: [12632256, 3329330, 42495]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Elliot oscillator fill', 2: 'Elliot oscillator'}, 'levels': [], 'description': ['Elliot oscillator'], 'name': 'Elliot oscillator simple', 'source': 'MQL5 Indicators/Elliot Oscillator Simple/Elliot oscillator simple.mq5', 'folder': 'Elliot Oscillator Simple', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'int', 'default': 5, 'label': 'Fast period', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 34, 'label': 'Slow period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriod = _input('FastPeriod', 5)  # Fast period
SlowPeriod = _input('SlowPeriod', 34)  # Slow period
Price = _input('Price', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Elliot oscillator (' + _str(FastPeriod) + ',' + _str(SlowPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        val[i] = iSma(price, FastPeriod, i, rates_total, 0) - iSma(price, SlowPeriod, i, rates_total, 1)
        fill1[i] = val[i]
        fill2[i] = 0.0
        i += 1
    return i

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 1
    workSma[r][instanceNo + 0] = price
    avg = price
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    avg = _fdiv(avg, float(k))
    return avg

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


class ElliotOscillatorSimple(_MQL5Indicator):
    name = 'Elliot oscillator simple'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 5,  # Fast period
        'SlowPeriod': 34,  # Slow period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

