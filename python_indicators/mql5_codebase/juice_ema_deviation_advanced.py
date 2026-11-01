"""Juice ema deviation - advanced — converted from MQL5: MQL5 Indicators/Juice - EMA deviation - advanced/Juice ema deviation - advanced.mq5

Juice ema deviation indicator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [13759441, 12052223], 2: [12632256, 3329330, 42495]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Juice fill', 2: 'Juice'}, 'levels': [], 'description': ['Juice ema deviation indicator'], 'name': 'Juice ema deviation - advanced', 'source': 'MQL5 Indicators/Juice - EMA deviation - advanced/Juice ema deviation - advanced.mq5', 'folder': 'Juice - EMA deviation - advanced', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Juice period', 'sinput': False}, {'mql': 'inpLevel', 'py': 'inpLevel', 'param': 'inpLevel', 'type': 'int', 'default': 14, 'label': 'Average deviation period (<= 1 for same as juice period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Juice period
inpLevel = _input('inpLevel', 14)  # Average deviation period (<= 1 for same as juice period)
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
sumdev = Arr(0, 0.0)
dev = Arr(0, 0.0)
ª_levelsPeriod = 0

def OnInit():
    global ª_levelsPeriod
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, dev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, sumdev, INDICATOR_CALCULATIONS)
    ª_levelsPeriod = (inpLevel if (inpLevel > 1) else inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Juice ema deviation (' + _str(inpPeriod) + ',' + _str(ª_levelsPeriod) + ')')
    return 0

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        dev[i] = iEmaDeviation(_price, inpPeriod, i)
        if i > ª_levelsPeriod:
            sumdev[i] = sumdev[i - 1] + dev[i] - dev[i - ª_levelsPeriod]
        else:
            sumdev[i] = dev[i]
            k = 1
            while k < ª_levelsPeriod and i >= k:
                sumdev[i] += dev[i - k]
                k += 1
        _level = _fdiv(sumdev[i], float(ª_levelsPeriod))
        fill1[i] = dev[i]
        val[i] = fill1[i]
        valc[i] = (2 if (val[i] < _level) else 1)
        fill2[i] = _level
        i += 1
    return i

def iEmaDeviation(price, period, i, _instance=0):
    _indC = _imod(i, 16)
    if i > period and period > 1:
        _indP = _imod(i - 1, 16)
        _alpha = _fdiv(2.0, 1.0 + period)
        _s_iEmaDeviation_workEmaDeviation[_indC][_instance] = _s_iEmaDeviation_workEmaDeviation[_indP][_instance] + (_alpha * (price - _s_iEmaDeviation_workEmaDeviation[_indP][_instance]))
        _s_iEmaDeviation_workEmaDeviation[_indC][_instance + 1] = _s_iEmaDeviation_workEmaDeviation[_indP][_instance + 1] + (_alpha * ((price * price) - _s_iEmaDeviation_workEmaDeviation[_indP][_instance + 1]))
    else:
        _s_iEmaDeviation_workEmaDeviation[_indC][_instance] = price
        _s_iEmaDeviation_workEmaDeviation[_indC][_instance + 1] = price * price
    return MathSqrt(_fdiv(period * (_s_iEmaDeviation_workEmaDeviation[_indC][_instance + 1] - (_s_iEmaDeviation_workEmaDeviation[_indC][_instance] * _s_iEmaDeviation_workEmaDeviation[_indC][_instance])), ((period - 1.0) if (period > 2) else 1)))

# ---- static local variables
_s_iEmaDeviation_workEmaDeviation = Arr(16, 0.0, dyn=False, dims=(2,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JuiceEmaDeviationAdvanced(_MQL5Indicator):
    name = 'Juice ema deviation - advanced'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Juice period
        'inpLevel': 14,  # Average deviation period (<= 1 for same as juice period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

