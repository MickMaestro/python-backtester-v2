"""CCI - ema based — converted from MQL5: MQL5 Indicators/CCI - EMA based/CCI - ema based.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'value'}, 'levels': [], 'description': [], 'name': 'CCI - ema based', 'source': 'MQL5 Indicators/CCI - EMA based/CCI - ema based.mq5', 'folder': 'CCI - EMA based', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 100.0, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': -100.0, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # Price
inpLevelUp = _input('inpLevelUp', 100.0)  # Level up
inpLevelDown = _input('inpLevelDown', -100.0)  # Level down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(1,))
workEmaDeviation = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI - ema based (' + _str(inpCciPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpCciPrice, open, close, high, low, i, rates_total)
        avg = iEma(_price, inpCciPeriod, i, rates_total)
        dev = iEmaDeviation(_price, inpCciPeriod, i, rates_total)
        val[i] = (_fdiv(_price - avg, 0.015 * dev) if (dev != 0) else 0)
        levelUp[i] = inpLevelUp
        levelDn[i] = inpLevelDown
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workEma, 0) != bars:
        ArrayResize(workEma, bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iEmaDeviation(price, period, i, bars, instanceNo=0):
    if ArrayRange(workEmaDeviation, 0) != bars:
        ArrayResize(workEmaDeviation, bars)
    instanceNo *= 2
    workEmaDeviation[i][instanceNo + 0] = price
    workEmaDeviation[i][instanceNo + 1] = price
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[i][instanceNo + 0] = workEmaDeviation[i - 1][instanceNo + 0] + (alpha * (price - workEmaDeviation[i - 1][instanceNo + 0]))
        workEmaDeviation[i][instanceNo + 1] = workEmaDeviation[i - 1][instanceNo + 1] + (alpha * ((price * price) - workEmaDeviation[i - 1][instanceNo + 1]))
    return MathSqrt(_fdiv(period * (workEmaDeviation[i][instanceNo + 1] - (workEmaDeviation[i][instanceNo + 0] * workEmaDeviation[i][instanceNo + 0])), MathMax(period - 1, 1)))

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


class CCIEmaBased(_MQL5Indicator):
    name = 'CCI - ema based'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpLevelUp': 100.0,  # Level up
        'inpLevelDown': -100.0,  # Level down
    }

