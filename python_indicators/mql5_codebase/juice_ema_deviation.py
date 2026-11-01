"""Juice ema deviation — converted from MQL5: MQL5 Indicators/Juice - EMA deviation/Juice ema deviation.mq5

Juice ema deviation indicator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [13759441, 12052223], 2: [12632256, 3329330, 42495]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Juice fill', 2: 'Juice'}, 'levels': [], 'description': ['Juice ema deviation indicator'], 'name': 'Juice ema deviation', 'source': 'MQL5 Indicators/Juice - EMA deviation/Juice ema deviation.mq5', 'folder': 'Juice - EMA deviation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpLevel', 'py': 'inpLevel', 'param': 'inpLevel', 'type': 'double', 'default': 6.0, 'label': 'Level (in pips)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpLevel = _input('inpLevel', 6.0)  # Level (in pips)
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
_workLevel = 0.0
workEmaDeviation = Arr(5, 0.0, dyn=False, dims=(2,))

def OnInit():
    global _workLevel
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    _workLevel = inpLevel * Point() * MathPow(10, _imod(Digits(), 2))
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _workLevel)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Juice ema deviation (' + _str(inpPeriod) + ',' + _str(inpLevel) + ')')
    return 0

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iEmaDeviation(price, inpPeriod, i) - _workLevel
        valc[i] = (2 if (val[i] < _workLevel) else 1)
        fill1[i] = val[i]
        fill2[i] = _workLevel
        i += 1
    return i

def iEmaDeviation(price, period, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 2
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[_indC][_inst + 0] = workEmaDeviation[_indP][_inst + 0] + (alpha * (price - workEmaDeviation[_indP][_inst + 0]))
        workEmaDeviation[_indC][_inst + 1] = workEmaDeviation[_indP][_inst + 1] + (alpha * ((price * price) - workEmaDeviation[_indP][_inst + 1]))
    else:
        for k in range(0, 2):
            workEmaDeviation[_indC][_inst + k] = price
    return MathSqrt(_fdiv(period * (workEmaDeviation[_indC][_inst + 1] - (workEmaDeviation[_indC][_inst + 0] * workEmaDeviation[_indC][_inst + 0])), MathMax(period - 1, 1)))

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


class JuiceEmaDeviation(_MQL5Indicator):
    name = 'Juice ema deviation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Period
        'inpLevel': 6.0,  # Level (in pips)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

